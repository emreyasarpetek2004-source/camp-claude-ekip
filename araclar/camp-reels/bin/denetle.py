#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Basılmış reels'ları ölçer (DENETİM katmanı). Dosya değiştirmez.

Kapılar (her reels):
  R1 format     1080x1920, 30 fps, h264 + aac, faststart
  R2 süre       20-75 sn
  R3 ses        -14 ±1 LUFS, true peak <= -1 dBTP
  R4 sınır      çıktının KENDİ sesi yeniden transkript edilir; ilk 3 ve son 3 kelime beklenenle eşleşir
                (kelime bölünmesi / yarım cümle yakalanır)
  R5 metin      çıktı transkripti ile beklenen metin benzerliği >= 0,80 (iç kesimde tekrar/kayıp yakalanır)
  R6 siyah      blackdetect: 0,3 sn üstü siyah kare yok
  R7 altyazı    ASS konumları IG arayüz güvenli alanında (y 220-1600)
Gözle kontrol için: edit/denetim/reels_<no>_serit.jpg (her 3 sn bir kare) üretilir.

Kullanım: python3 bin/denetle.py <proje>   ->  edit/denetim/rapor.json + ekrana tablo
"""
import difflib
import json
import os
import re
import subprocess
import sys
import tempfile

FFMPEG = os.path.expanduser("~/.local/bin/ffmpeg")
FFPROBE = os.path.expanduser("~/.local/bin/ffprobe")
MLX = os.path.expanduser("~/.local/bin/mlx_whisper")
MODEL = "mlx-community/whisper-large-v3-turbo"


def norm(s):
    s = s.replace("İ", "i").replace("I", "ı").lower()
    s = s.translate(str.maketrans("çğıöşü", "cgiosu"))  # ASR ş/s, ı/i karışıklığına dayanıklı
    return re.findall(r"[a-z0-9']+", s)


def uc_eslesir(a, b):
    """İlk/son 3 kelime: harf düzeyinde >= 0,75 benzerlik (yazım farkı değil, kelime kaybı aranır)."""
    return difflib.SequenceMatcher(None, "".join(a), "".join(b)).ratio() >= 0.75  # "bilir kisiler" = "bilirkisiler"


def probe(yol):
    p = subprocess.run([FFPROBE, "-v", "error", "-show_entries",
                        "stream=codec_type,codec_name,width,height,r_frame_rate:format=duration",
                        "-of", "json", yol], capture_output=True, text=True)
    return json.loads(p.stdout)


def ses_olc(yol):
    p = subprocess.run([FFMPEG, "-nostdin", "-i", yol, "-af", "loudnorm=I=-14:TP=-1.5:print_format=json",
                        "-f", "null", "-"], capture_output=True, text=True)
    j = json.loads(p.stderr[p.stderr.rindex("{"):p.stderr.rindex("}") + 1])
    return float(j["input_i"]), float(j["input_tp"])


def siyah(yol):
    p = subprocess.run([FFMPEG, "-nostdin", "-i", yol, "-vf", "blackdetect=d=0.3:pix_th=0.08", "-an", "-f", "null", "-"],
                       capture_output=True, text=True)
    return re.findall(r"black_start:([\d.]+) black_end:([\d.]+)", p.stderr)


def transkript(yol, dil):
    with tempfile.TemporaryDirectory() as td:
        w = os.path.join(td, "a.wav")
        subprocess.run([FFMPEG, "-nostdin", "-v", "error", "-i", yol, "-ac", "1", "-ar", "16000", "-y", w], check=True)
        subprocess.run([MLX, w, "--model", MODEL, "--language", dil, "-o", td, "-f", "json", "--verbose", "False",
                        "--condition-on-previous-text", "False"], capture_output=True, stdin=subprocess.DEVNULL)
        metin = json.load(open(os.path.join(td, "a.json"))).get("text", "")
    # whisper kapanış kartının sessizliğinde "Altyazı M.K." uyduruyor (hazirla.HALUSINASYON ile aynı)
    return re.sub(r"altyaz[ıi]\s*m\.?\s*k\.?|abone ol\w*|izlediğiniz için teşekkür\w*", " ", metin, flags=re.I)


def senkron(yol, w, dil):
    """Kelimenin beklenen başlangıcı ile çıktı sesindeki başlangıcı arasındaki fark (sn); bulunamazsa None."""
    bas = max(0, w["b"] - 1.0)
    with tempfile.TemporaryDirectory() as td:
        a = os.path.join(td, "a.wav")
        subprocess.run([FFMPEG, "-nostdin", "-v", "error", "-ss", "%.3f" % bas, "-t", "3", "-i", yol, "-ac", "1",
                        "-ar", "16000", "-y", a], check=True)
        subprocess.run([MLX, a, "--model", MODEL, "--language", dil, "--word-timestamps", "True", "-o", td, "-f", "json",
                        "--verbose", "False"], capture_output=True, stdin=subprocess.DEVNULL)
        try:
            d = json.load(open(os.path.join(td, "a.json")))
        except Exception:
            return None
    hedef = norm(w["w"])
    if not hedef:
        return None
    adaylar = [x for sg in d.get("segments", []) for x in sg.get("words", [])
               if difflib.SequenceMatcher(None, " ".join(norm(x["word"])), " ".join(hedef)).ratio() >= 0.75]
    if not adaylar:
        return None
    en = min(adaylar, key=lambda x: abs(bas + x["start"] - w["b"]))
    return round(bas + en["start"] - w["b"], 3)


def kesim_noktasi(yol, kw, t, dil, pay=1.2):
    """İç kesim noktası t'nin iki yanındaki 2'şer kelime çıktının kendi sesinde duyuluyor mu? (kelime yutma kapısı)"""
    once = [w for w in kw if w["e"] <= t + 0.02][-2:]
    sonra = [w for w in kw if w["b"] >= t - 0.02][:2]
    beklenen = [w["w"] for w in once + sonra]
    if not beklenen:
        return True, ""
    bas = max(0, (once[0]["b"] if once else t) - pay)  # whisper pencere başındaki/sonundaki kelimeleri kaçırıyor
    bit = (sonra[-1]["e"] if sonra else t) + max(0.5, pay)
    with tempfile.TemporaryDirectory() as td:
        a = os.path.join(td, "a.wav")
        subprocess.run([FFMPEG, "-nostdin", "-v", "error", "-ss", "%.3f" % bas, "-t", "%.3f" % (bit - bas), "-i", yol, "-ac", "1",
                        "-ar", "16000", "-y", a], check=True)
        subprocess.run([MLX, a, "--model", MODEL, "--language", dil, "-o", td, "-f", "json", "--verbose", "False",
                        "--condition-on-previous-text", "False"], capture_output=True, stdin=subprocess.DEVNULL)
        try:
            duyulan = norm(json.load(open(os.path.join(td, "a.json"))).get("text", ""))
        except Exception:
            duyulan = []
    eksik = [w for w in beklenen if norm(w) and not any(
        difflib.SequenceMatcher(None, "".join(norm(w)), d).ratio() >= 0.7 for d in duyulan)]
    return len(eksik) <= 1, "beklenen '%s' | duyulan '%s'" % (" ".join(beklenen), " ".join(duyulan))


def serit(yol, hedef, sure):
    n = max(4, int(sure // 3))
    subprocess.run([FFMPEG, "-nostdin", "-v", "error", "-y", "-i", yol, "-vf",
                    "fps=1/3,scale=216:384,tile=%dx%d" % (min(n, 8), (n + 7) // 8), "-frames:v", "1", hedef])


def main():
    proje = os.path.abspath(sys.argv[1])
    meta = json.load(open(os.path.join(proje, "proje.json")))
    kj = json.load(open(os.path.join(proje, "edit", "kelimeler.json")))
    kel = [w for c in kj["cumle"] for w in c["kelime"]]
    dz = os.path.join(proje, "edit", "denetim")
    os.makedirs(dz, exist_ok=True)
    rapor = []
    nolar = sorted(int(m.group(1)) for m in (re.match(r"reels_(\d+)\.mp4$", f) for f in os.listdir(os.path.join(proje, "out"))) if m)
    if len(sys.argv) > 2:
        nolar = [int(x) for x in sys.argv[2:]]
    for no in nolar:
        kj_v2 = os.path.join(proje, "edit", "klip_%02d" % no, "klip.json")
        sj_v2 = os.path.join(proje, "edit", "sahne_%02d.json" % no)
        v2 = os.path.exists(kj_v2) and os.path.exists(sj_v2)
        if v2:
            edl = json.load(open(kj_v2))
            sahne = json.load(open(sj_v2))
        else:
            ey = os.path.join(proje, "edit", "reels_%02d_edl.json" % no)
            if not os.path.exists(ey):
                continue
            edl = json.load(open(ey))
        yol = os.path.join(proje, "out", "reels_%02d.mp4" % no)
        if not os.path.exists(yol):
            continue
        k = {}
        pr = probe(yol)
        v = [s for s in pr["streams"] if s["codec_type"] == "video"][0]
        a = [s for s in pr["streams"] if s["codec_type"] == "audio"]
        sure = float(pr["format"]["duration"])
        k["R1"] = (v["width"], v["height"]) == (1080, 1920) and v["r_frame_rate"] == "30/1" and \
            v["codec_name"] == "h264" and bool(a) and a[0]["codec_name"] == "aac"
        with open(yol, "rb") as fh:
            bas = fh.read(4096)
        k["R1"] = k["R1"] and bas.find(b"moov") != -1 and (bas.find(b"mdat") == -1 or bas.find(b"moov") < bas.find(b"mdat"))
        k["R2"] = (22 <= sure <= 80) if v2 else (20 <= sure <= 75)
        lufs, tp = ses_olc(yol)
        k["R3"] = abs(lufs + 14) <= 1.0 and tp <= -1.0
        beklenen = []
        for p in edl["parcalar"]:
            beklenen += [w["w"] for w in kel if p["bas"] <= (w["b"] + w["e"]) / 2 <= p["son"]]
        bn = norm(" ".join(beklenen))
        cn = norm(transkript(yol, meta.get("dil", "tr")))
        k["R4"] = bool(cn) and uc_eslesir(cn[:3], bn[:3]) and uc_eslesir(cn[-3:], bn[-3:])
        benz = difflib.SequenceMatcher(None, bn, cn).ratio()
        k["R5"] = benz >= 0.80
        sy = siyah(yol)
        k["R6"] = not sy
        if v2:
            # R7 v2: altyazı/kart konumu şablonda sabit; burada sahne metin sınırları ölçülür
            uzun = [e for e in sahne["eklemeler"] for kk, sn in (("deger", 10), ("etiket", 30), ("metin", 48))
                    if isinstance(e.get(kk), str) and len(e[kk]) > sn]
            k["R7"] = not uzun and len(sahne["soru_karti"].get("metin", "")) <= 64
            # R8: her görsel doğrulanmış
            cy = os.path.join(proje, "edit", "assets", "%02d" % no, "CREDITS.json")
            cred = {c["dosya"]: c for c in (json.load(open(cy)) if os.path.exists(cy) else [])}
            k["R8"] = all(cred.get(os.path.basename(e["dosya"]), {}).get("dogrulandi") for e in sahne["eklemeler"] if e["tip"] == "gorsel")
            # R9: altyazı senkronu, 3 noktada kelime zamanı (çıktı sesi yeniden çözülür)
            kw = edl["kelimeler"]
            sapma = []
            for j in (len(kw) // 4, len(kw) // 2, 3 * len(kw) // 4):
                w = kw[j]
                sapma.append(senkron(yol, w, meta.get("dil", "tr")))
            olculen = [x for x in sapma if x is not None]
            # whisper kelime zamanı kendi içinde ~±0,2 sn oynar: medyan <= 0,15 ve en kötü <= 0,30
            k["R9"] = len(olculen) >= 2 and sorted(abs(x) for x in olculen)[len(olculen) // 2] <= 0.15 and \
                max(abs(x) for x in olculen) <= 0.30
            # R10: SFX seviye tavanı (sfx/ -20 LUFS; 0,45 kazanç = konuşmanın ~13 dB altı)
            # R12: her iç kesim noktasında kelime yutulmamış (iki yandaki 2'şer kelime duyuluyor)
            kesim_sonuc = []
            for pc in edl["parcalar"][1:]:
                ok, ayr = kesim_noktasi(yol, kw, pc["cikis_bas"], meta.get("dil", "tr"))
                if not ok:  # kısa pencerede whisper kelime kaçırabiliyor: geniş pencereyle bir kez daha
                    ok, ayr = kesim_noktasi(yol, kw, pc["cikis_bas"], meta.get("dil", "tr"), pay=3.0)
                kesim_sonuc.append({"t": pc["cikis_bas"], "ok": ok, "ayrinti": ayr})
            k["R12"] = all(x["ok"] for x in kesim_sonuc)
            # R11: kesit içinde Zoom kamera geçişi yok (katılımcı/moderatör yüzü)
            k["R11"] = not edl.get("kamera_gecisi")
            k["R10"] = all(x.get("seviye", 0.35) <= 0.45 for x in sahne["sfx"])
        else:
            ass = open(os.path.join(proje, "edit", "reels_%02d.ass" % no)).read()
            ys = [int(y) for y in re.findall(r"\\pos\(\d+,(\d+)\)", ass)]
            k["R7"] = bool(ys) and all(220 <= y <= 1600 for y in ys)
        serit(yol, os.path.join(dz, "reels_%02d_serit.jpg" % no), sure)
        satir = {"no": no, "v2": v2, "senkron_sapma": sapma if v2 else None, "kesimler": kesim_sonuc if v2 else None, "duzen": edl["duzen"], "sure": round(sure, 1), "lufs": lufs, "tp": tp,
                 "benzerlik": round(benz, 3), "ilk": " ".join(cn[:4]), "beklenen_ilk": " ".join(bn[:4]),
                 "son": " ".join(cn[-4:]), "beklenen_son": " ".join(bn[-4:]), "siyah": sy, "kapilar": k,
                 "gecti": all(k.values())}
        rapor.append(satir)
        print("reels %02d %-9s %5.1fs  %s  LUFS %.1f  benz %.2f  %s" % (
            no, edl["duzen"], sure, " ".join("%s:%s" % (x, "OK" if y else "XX") for x, y in k.items()),
            lufs, benz, "GEÇTİ" if satir["gecti"] else "KALDI"))
        if v2 and not k.get("R12", True):
            for x in kesim_sonuc:
                if not x["ok"]:
                    print("    kesim %.2f sn: %s" % (x["t"], x["ayrinti"]))
        if not k["R4"]:
            print("    sınır: çıktı '%s ... %s' | beklenen '%s ... %s'" % (satir["ilk"], satir["son"],
                                                                         satir["beklenen_ilk"], satir["beklenen_son"]))
    ry = os.path.join(dz, "rapor.json")  # kısmi çalıştırmada önceki satırlar korunur
    eski = {r["no"]: r for r in (json.load(open(ry)) if os.path.exists(ry) else [])}
    eski.update({r["no"]: r for r in rapor})
    json.dump([eski[n] for n in sorted(eski)], open(ry, "w"), ensure_ascii=False, indent=1)
    print("rapor:", os.path.join(dz, "rapor.json"))
    sys.exit(0 if rapor and all(r["gecti"] for r in rapor) else 1)


if __name__ == "__main__":
    main()

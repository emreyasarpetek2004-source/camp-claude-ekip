#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Hızlı, ölçüme dayalı denetim. Tek komut, kısa rapor.

(21.09.2026 kararı: "bir de denetçi kur ama token ve hız optimasyonu da olsun aşırı uzun
sürmesin")

Tasarım kararı: ÖLÇÜMÜ KOD YAPAR, ajan yalnız özeti okur. Ajanın onlarca kareye bakması
hem yavaş hem pahalı. Burada her kapı bir sayıya indirgenir; yalnız KALAN kapılar için
kare çıkarılır ve göze sunulur.

Kullanım:
    python3 bin/denetle.py <proje_dizini>            # kısa rapor
    python3 bin/denetle.py <proje_dizini> --kare     # kalan kapılar icin kare de cikar
"""
import argparse
import io
import json
import os
import re
import subprocess
import sys

FFMPEG = os.path.expanduser("~/.local/bin/ffmpeg")
FFPROBE = os.path.expanduser("~/.local/bin/ffprobe")


def _probe(yol, alanlar, akis=None):
    """Akış seçimi ŞART: ses akışının r_frame_rate=0/0 değeri videonunkini eziyor."""
    cmd = [FFPROBE, "-v", "error"]
    if akis:
        cmd += ["-select_streams", akis]
    cmd += ["-show_entries", alanlar, "-of", "default=noprint_wrappers=1", yol]
    o = subprocess.run(cmd, capture_output=True, text=True).stdout
    return dict(re.findall(r"^(\w+)=(.*)$", o, re.M))


def _kare(yol, t, vf=None):
    """Kare cikarilamazsa None doner. Bozuk cikti denetciyi COKERTMEMELI."""
    import numpy as np
    from PIL import Image
    cmd = [FFMPEG, "-nostats", "-v", "error", "-ss", str(t), "-i", yol, "-frames:v", "1"]
    if vf:
        cmd += ["-vf", vf]
    cmd += ["-f", "image2pipe", "-vcodec", "png", "-"]
    p = subprocess.run(cmd, capture_output=True)
    if not p.stdout:
        return None
    try:
        return np.asarray(Image.open(io.BytesIO(p.stdout)).convert("RGB")).astype(int)
    except Exception:
        return None


def denetle(proje, kare_cikar=False):
    import numpy as np
    edit = os.path.join(proje, "edit")
    final = os.path.join(edit, "final.mp4")
    if not os.path.exists(final):
        adaylar = sorted(f for f in os.listdir(edit) if f.startswith("final") and f.endswith(".mp4"))
        if not adaylar:
            return ["KALDI  cikti yok: edit/final*.mp4 bulunamadi"], 1
        final = os.path.join(edit, adaylar[-1])
    edl = json.load(open(os.path.join(edit, "edl.json")))
    ham = None
    for k, v in edl["sources"].items():
        if k != "OPENER":
            ham = v
    sat, kalan = [], 0

    def kap(ad, ok, detay):
        nonlocal kalan
        sat.append("%-6s %-22s %s" % ("GECTI" if ok else "KALDI", ad, detay))
        if not ok:
            kalan += 1

    # Once cikti gecerli mi: moov atom yoksa kodlama yarida kesilmis demektir
    gecerli = subprocess.run([FFPROBE, "-v", "error", "-show_entries", "format=duration",
                              "-of", "csv=p=0", final], capture_output=True, text=True)
    if gecerli.returncode != 0 or not gecerli.stdout.strip():
        return ["KALDI  cikti bozuk: %s" % (gecerli.stderr.strip().splitlines() or ["?"])[0][:90],
                "       (kodlama yarida kesilmis, yeniden uretilmeli)"], 1

    fv = _probe(final, "stream=width,height,r_frame_rate", "v:0")
    fa = _probe(final, "stream=channels,sample_rate", "a:0")
    ff = _probe(final, "format=duration,bit_rate")
    f = dict(fv); f.update(fa); f.update(ff)
    w, h = int(f.get("width", 0)), int(f.get("height", 0))
    sure = float(f.get("duration", 0)); brt = int(f.get("bit_rate", 0))
    bekle = sum(float(r["end"]) - float(r["start"]) for r in edl["ranges"])
    # Her birlesme noktasi kare hizasina yuvarlaniyor (24 fps'de kare 0.042 sn), bu
    # yuzden sapma aralik sayisiyla buyuyor. Sabit 0.5 sn, cok kesimli derslerde
    # bosuna kaliyordu (CH01: 15 aralik, 0.63 sn). Kapinin isi kare yuvarlamasini
    # degil, eksik parca gibi kaba hatayi yakalamak.
    _tol = 0.5 + 0.05 * len((edl or {}).get("ranges", []))
    kap("G11 sure", abs(sure - bekle) <= _tol,
        "%.2f / beklenen %.2f sn (tolerans %.2f)" % (sure, bekle, _tol))
    kap("G12 bicim", (w, h) == (1920, 1080) and f.get("r_frame_rate") == "24/1"
        and f.get("sample_rate") == "48000", "%dx%d %s %s Hz" % (w, h, f.get("r_frame_rate"), f.get("sample_rate")))
    if ham and os.path.exists(ham):
        hb = int(_probe(ham, "format=bit_rate").get("bit_rate", 0))
        kap("G12b bit hizi", brt >= hb, "%.2f Mbps / kaynak %.2f Mbps" % (brt / 1e6, hb / 1e6))

    # G12c bant: 3 noktada cropdetect
    bant_ok, bant_d = True, []
    for t in (sure * 0.15, sure * 0.5, sure * 0.85):
        o = subprocess.run([FFMPEG, "-nostats", "-v", "error", "-ss", "%.1f" % t, "-t", "1",
                            "-i", final, "-vf", "cropdetect=24:2:0,metadata=print:file=-",
                            "-an", "-f", "null", "-"], capture_output=True, text=True)
        g = re.findall(r"cropdetect\.w=(\d+)\s+.*?cropdetect\.h=(\d+)", o.stdout, re.S)
        if g:
            cw, ch = int(g[-1][0]), int(g[-1][1])
            bant_d.append("%dx%d" % (cw, ch))
            if abs(cw - w) > 4 or abs(ch - h) > 4:
                bant_ok = False
    kap("G12c bant", bant_ok, (" ".join(bant_d) or "olculemedi") + " (tolerans 4 px)")

    # G12d yalniz balon TASINDIYSA anlamli. Balon kayittaki yerinde kalinca ortada
    # yama da dikis de yoktur; olculen sey balonun kendi kenari olur ve kapi bosuna kalir.
    # (22.09.2026: kullanıcı "hoca kendi goruntusunu nereye koyduysa orada kalsin" dedi.)
    tasindi = False
    try:
        tasindi = bool(json.load(open(os.path.join(edit, "yerlesim.json"))).get("balon_tasindi"))
    except (OSError, ValueError):
        tasindi = False

    plan_yol = os.path.join(edit, "balon_plan.json")
    plan_b = json.load(open(plan_yol)) if os.path.exists(plan_yol) else None

    # G12d balon/hayalet: yamanin solundaki dikis farki.
    # Hayalet kalsaydi yamali bolge komsusundan keskin ayrilirdi. Slaytin kendi ust
    # gradyan bandi yuksek sapma uretiyor, o yuzden "sapma" degil "komsuyla fark" olculur.
    hayalet_ok, farklar = True, []
    rl_yama = bool(plan_b and plan_b.get("yama") and plan_b["yama"].get("tip") == "removelogo")
    if tasindi and rl_yama:
        # removelogo dolgusu (05.10.2026 v2): halka = hayalet maskesi icinde, yeni balonun
        # disinda kalan alan. Dolgu cevreden uretildigi icin rengi hemen disindaki slayta
        # yakin olmali; hayalet (balonun gri duvari/yuz) kalirsa fark buyur. Pembe = dolgu hatasi.
        q = subprocess.run([os.path.expanduser("~/Developer/video-use/.venv/bin/python"),
                            os.path.join(os.path.dirname(os.path.abspath(__file__)), "hayalet_kontrol.py"),
                            edit, "--n", "6"], capture_output=True, text=True)
        farklar.append((q.stdout.strip().splitlines() or ["?"])[0])
        hayalet_ok = q.returncode == 0
        y_ = plan_b["yama"]
        # Pembe yalniz DOLGU halkasinda aranir (alfa maskesi icinde, yeni balonun disinda):
        # slaytin kendi pembe gorseli (CH38 H&E histoloji) dolgu hatasi degildir.
        from PIL import Image as _I
        _am = np.asarray(_I.open(os.path.join(edit, "yama_maske.png"))).astype(float) / 255
        _yy, _xx = np.mgrid[0:y_["h"], y_["x"]:y_["x"] + y_["w"]]
        _bc = (plan_b["x"] + plan_b["cap"] / 2.0, plan_b["y"] + plan_b["cap"] / 2.0, plan_b["cap"] / 2.0)
        _halka = (_am > 0.5) & (((_xx - _bc[0]) ** 2 + (_yy - _bc[1]) ** 2) > (_bc[2] + 2) ** 2)
        for t in [sure * (i + 0.5) / 12 for i in range(12)]:
            im = _kare(final, "%.1f" % t)
            if im is None:
                continue
            bol = im[0:y_["h"], y_["x"]:y_["x"] + y_["w"]].astype(float)
            if (((bol[..., 0] > 200) & (bol[..., 2] > 200) & (bol[..., 1] < 150)) & _halka).sum() > 30:
                farklar.append("PEMBE t=%.0f" % t); hayalet_ok = False
    for t in ((sure * 0.2, sure * 0.55, sure * 0.9) if tasindi and not rl_yama else ()):
        im = _kare(final, "%.1f" % t)
        if im is None:
            farklar.append("kare yok"); hayalet_ok = False; continue
        x0, yh = int(w * 0.854), 200
        if plan_b and plan_b.get("yama"):
            x0, yh = int(plan_b["yama"]["x"]), max(20, int(plan_b["yama"]["h"]))
        ic = im[0:yh, x0:x0 + 6].mean(axis=(0, 1))
        dis = im[0:yh, x0 - 10:x0 - 4].mean(axis=(0, 1))
        fark = float(np.abs(ic - dis).max())
        farklar.append("%.1f" % fark)
        if fark > 22:
            hayalet_ok = False
    kap("G12d balon/hayalet", hayalet_ok,
        (" ".join(farklar) if rl_yama else ("dikis farki " + " ".join(farklar) + "/255 (esik 22)")) if tasindi
        else "balon yerinde, yama yok -> kapi gecersiz")

    # G12e/G12f (05.10.2026, kullanıcı: balon tamamen slayt icinde, kucuk degil; donma/kayma yok)
    if plan_b:
        icerde = (plan_b["x"] >= 0 and plan_b["y"] >= 0 and plan_b["x"] + plan_b["cap"] <= w
                  and plan_b["y"] + plan_b["cap"] <= h and plan_b["olcek"] >= 0.89)
        kap("G12e balon yerlesimi", icerde, "x=%d y=%d cap=%d olcek=%.2f yazi=%.3f"
            % (plan_b["x"], plan_b["y"], plan_b["cap"], plan_b["olcek"], plan_b["yazi_ortusme_p90"]))
        q = subprocess.run([sys.executable if "venv" in sys.executable else os.path.expanduser("~/Developer/video-use/.venv/bin/python"),
                            os.path.join(os.path.dirname(os.path.abspath(__file__)), "balon_senkron.py"),
                            os.path.join(edit, "edl.json"), final, "--n", "16"], capture_output=True, text=True)
        kap("G12f balon senkron/donma", q.returncode == 0, (q.stdout.strip().splitlines() or ["?"])[0][:90]
            + ("" if q.returncode == 0 else " | " + " ".join(q.stdout.strip().splitlines()[1:3])[:120]))

    # G13 ses
    o = subprocess.run([FFMPEG, "-nostats", "-hide_banner", "-i", final,
                        "-af", "loudnorm=print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True)
    m = dict(re.findall(r'"(input_i|input_tp)"\s*:\s*"(-?[\d.]+)"', o.stderr))
    li = float(m.get("input_i", 0)); tp = float(m.get("input_tp", 0))
    kap("G13 ses", -17.5 <= li <= -13.0 and tp <= -0.5,
        "I=%.2f LUFS  TP=%.2f dBTP" % (li, tp)
        + (" (tepe tavani bagladi)" if li < -16.5 and tp >= -1.6 else ""))

    # G7 kesim sinirlari sessizlige oturmus mu
    sy = os.path.join(edit, "sessizlik.json")
    if os.path.exists(sy) and len(edl["ranges"]) > 2:
        ses = json.load(open(sy))
        bos = ses.get("bosluk", [])
        kotu = []
        # Yalniz IC birlesme noktalari denetlenir. Son range'in bitisi videonun sonudur,
        # orada birlesme yoktur, dolayisiyla tik sesi de olamaz.
        # (22.09.2026: CH06 bu yuzden yanlis yere kaldi.)
        son_bitis = float(edl["ranges"][-1]["end"])
        for r in edl["ranges"][1:]:
            for t in (float(r["start"]), float(r["end"])):
                if t <= 0.05 or abs(t - son_bitis) < 0.01:
                    continue
                onay = json.load(open(os.path.join(edit, "g7_onay.json"))) if os.path.exists(os.path.join(edit, "g7_onay.json")) else []
                if any(abs(t - float(o["t"])) <= 0.03 for o in onay):
                    continue   # dikis duyulacagi gibi dinlenip onaylandi
                if not any(b["bas"] - 0.15 <= t <= b["bit"] + 0.15 for b in bos):
                    # Kaba haritada (-35 dB, 0,3 sn) yoksa KELIME ARASI ince bosluga
                    # bakilir (-30 dB, 0,05 sn). Kelime zamanli kesimler (05.10.2026)
                    # tam kelime arasina oturur; kelime ORTASI ise yine yakalanir.
                    kaynak = edl["sources"].get(r["source"])
                    a0 = max(0.0, t - 0.6)
                    q = subprocess.run([FFMPEG, "-nostats", "-v", "info", "-ss", "%.3f" % a0, "-t", "1.2",
                                        "-i", kaynak, "-af", "silencedetect=noise=-30dB:d=0.05",
                                        "-f", "null", "-"], capture_output=True, text=True)
                    ss = [float(x) + a0 for x in re.findall(r"silence_start:\s*(-?[\d.]+)", q.stderr)]
                    se = [float(x) + a0 for x in re.findall(r"silence_end:\s*([\d.]+)", q.stderr)]
                    if not any(x0 - 0.05 <= t <= x1 + 0.05 for x0, x1 in zip(ss, se)):
                        # Son care: sinirin merkezindeki 20 ms'lik enerji. Bitisik iki kelime
                        # arasindaki nefes cukuru (-40 dB civari) 50 ms'den kisa oldugu icin
                        # silencedetect'e takilmaz ama orada kesmek tik yapmaz. Kelime ortasi
                        # -25 dB civarindadir, yine yakalanir. (CH01 3949.28, 05.10.2026)
                        import math, struct
                        a2 = max(0.0, t - 0.25)
                        q2 = subprocess.run([FFMPEG, "-nostats", "-v", "error", "-ss", "%.3f" % a2, "-t", "0.5",
                                             "-i", kaynak, "-vn", "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
                                            capture_output=True)
                        n_ = len(q2.stdout) // 2
                        x_ = struct.unpack("<%dh" % n_, q2.stdout[:n_ * 2])
                        # t +-15 ms icindeki en sessiz 10 ms; kisa kesitte ses karesi hizasi sonucu kaydiriyor
                        dbs = [20 * math.log10(max(1e-9, math.sqrt(sum(y * y for y in x_[k:k + 160]) / 160) / 32768))
                               for k in range(0, n_ - 160, 80) if abs(a2 + (k + 80) / 16000 - t) <= 0.015]
                        db = min(dbs) if dbs else 0.0
                        if db > -32.0:
                            kotu.append("%.2f" % t)
        kap("G7 kesim siniri", not kotu, "sessizlige oturmayan: " + (",".join(kotu) if kotu else "yok"))

    # G14: dikiste soz tekrari. Yeniden cekim kesilirken hocanin ayni gecis cumlesini
    # iki kez soyledigi yerde, dikiste ayni soz ust uste duyulabiliyor.
    # (CH09, 23.09.2026: "Gelelim sorularimiza en sevdiginiz kisim.")
    # Kapi ham transkripte DEGIL, uretilen videonun kendisine bakar: seyircinin
    # duydugu ses tek yetkilidir. ASR segment sinirlari ham kayitta kesim noktasini
    # asiyor ve metin uzerinden yapilan her kiyas yaniltiyor.
    if edl and os.path.exists(final):
        import tempfile
        MLX = os.path.expanduser("~/.local/bin/mlx_whisper")
        dikis, t = [], 0.0
        for r in edl["ranges"][:-1]:
            t += float(r["end"]) - float(r["start"])
            if r.get("source") == "DERS":
                dikis.append(round(t, 3))
        tekrar = []
        if os.path.exists(MLX) and dikis:
            # Her dikis icin ayri mlx_whisper calistirmak modeli her seferinde
            # yeniden yukluyordu (CH01'de 14 dikis = ~7 dk denetim). Tum pencereler
            # 1 sn sessizlikle ayrilip TEK ses dosyasinda birlestiriliyor ve tek
            # geciste cozuluyor; tekrar aramasi her pencere kendi icinde yapiliyor.
            PEN, ARA = 16.0, 1.0
            with tempfile.TemporaryDirectory() as td:
                parcalar, yerler, imlec = [], [], 0.0
                sessiz = os.path.join(td, "bos.wav")
                subprocess.run([FFMPEG, "-v", "error", "-f", "lavfi", "-i",
                                "anullsrc=r=16000:cl=mono", "-t", str(ARA), "-y", sessiz],
                               check=False)
                for i, d in enumerate(dikis):
                    a = max(0.0, d - PEN / 2)
                    w = os.path.join(td, "p%03d.wav" % i)
                    subprocess.run([FFMPEG, "-v", "error", "-ss", "%.3f" % a, "-t", str(PEN),
                                    "-i", final, "-ac", "1", "-ar", "16000", "-y", w],
                                   check=False)
                    if not os.path.exists(w):
                        continue
                    parcalar += [w, sessiz]
                    yerler.append((imlec, imlec + PEN, d))
                    imlec += PEN + ARA
                if parcalar:
                    liste = os.path.join(td, "l.txt")
                    with open(liste, "w") as f:
                        for w in parcalar:
                            f.write("file '%s'\n" % w)
                    hep = os.path.join(td, "hep.wav")
                    subprocess.run([FFMPEG, "-v", "error", "-f", "concat", "-safe", "0",
                                    "-i", liste, "-c", "copy", "-y", hep], check=False)
                    q = subprocess.run([MLX, hep, "--model",
                                        "mlx-community/whisper-large-v3-turbo",
                                        "--language", "tr", "--output-dir", td,
                                        "--output-format", "json", "--verbose", "False"],
                                       capture_output=True, text=True)
                    jy = os.path.join(td, "hep.json")
                    if q.returncode == 0 and os.path.exists(jy):
                        seg = json.load(open(jy)).get("segments", [])
                        # Dinlenip OGRETICI TEKRAR oldugu teyit edilen dikisler (cikti zamani, gerekce):
                        # edit/g14_onay.json [{"t": 875.5, "gerekce": "..."}]  (06.10.2026, CH29)
                        try:
                            g14_onay = [float(x["t"]) for x in json.load(open(os.path.join(edit, "g14_onay.json")))]
                        except (OSError, ValueError, KeyError, TypeError):
                            g14_onay = []
                        for a, b, d in yerler:
                            if any(abs(d - x) < 2.0 for x in g14_onay):
                                continue
                            # Dikis pencerenin ORTASINDA. Aranan sey, ayni sozun dikisin
                            # IKI YANINDA duyulmasi. Pencere icindeki her tekrari saymak
                            # yanlis alarm veriyor: hocanin kendi vurgu tekrari ("cok
                            # onemli bir tuzak" ust uste iki kez) dikisin tek tarafinda
                            # kaliyor ve ogretici tekrardir, kesilmez.
                            # (CH02, 23.09.2026: kapı bu yuzden haksiz yere kalmisti.)
                            orta = (a + b) / 2.0
                            zamanli = []
                            for x in seg:
                                if x["end"] <= a or x["start"] >= b:
                                    continue
                                kl = [w for w in re.sub(r"[^\wçğıöşüÇĞİÖŞÜ ]", " ",
                                                        x["text"].lower()).split()
                                      if len(w) > 2]
                                if not kl:
                                    continue
                                sr = max(0.01, x["end"] - x["start"])
                                for i, w in enumerate(kl):
                                    zamanli.append((x["start"] + sr * (i + 0.5) / len(kl), w))
                            kel = [w for _, w in zamanli]
                            zam = [t_ for t_, _ in zamanli]
                            n, gor = 4, {}
                            for i in range(len(kel) - n + 1):
                                f_ = " ".join(kel[i:i + n])
                                # Tek kelimenin ust uste tekrari ("ekran ekran ekran ekran")
                                # Whisper dongusudur, dikis tekrari degil (CH01 6 Eki: cikti temiz)
                                if len(set(kel[i:i + n])) <= 2:
                                    continue
                                j = gor.get(f_)
                                if (j is not None and i - j <= 12
                                        and zam[j] < orta <= zam[i]):
                                    tekrar.append("%.1f sn: \"%s\"" % (d, f_))
                                    break
                                gor.setdefault(f_, i)
                    else:
                        tekrar.append("ASR calismadi, dikisler dinlenemedi")
            kap("G14 dikis tekrari", not tekrar,
                "%d dikis tek geciste dinlendi · " % len(dikis) +
                ("ayni soz iki kez: " + "; ".join(tekrar) if tekrar else "temiz"))

    if kalan and kare_cikar:
        vy = os.path.join(edit, "verify"); os.makedirs(vy, exist_ok=True)
        for i, t in enumerate((sure * 0.2, sure * 0.55, sure * 0.9)):
            subprocess.run([FFMPEG, "-nostats", "-v", "error", "-ss", "%.1f" % t, "-i", final,
                            "-frames:v", "1", "-vf", "crop=620:420:1300:0,scale=520:-2",
                            "-y", os.path.join(vy, "kose_%d.png" % i)])
        sat.append("kareler: %s/kose_*.png (KALAN kapilar icin goz kontrolu)" % vy)
    return sat, kalan


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("proje")
    ap.add_argument("--kare", action="store_true")
    a = ap.parse_args()
    sat, kalan = denetle(a.proje, a.kare)
    print("DENETIM: %s" % ("GECTI" if not kalan else "KALDI (%d)" % kalan))
    for s in sat:
        print(" ", s)
    sys.exit(1 if kalan else 0)


if __name__ == "__main__":
    main()

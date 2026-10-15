#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Kesim listesinden 1080x1920 reels basar (ÜRETİM katmanı).

Girdi : edit/anlar.json (anlar agent'ının JSON'u), edit/kelimeler.json, edit/yerlesim.json, brands/<marka>.json
Çıktı : out/reels_<no>.mp4, edit/reels_<no>.ass, edit/reels_<no>_edl.json

Düzen (UKCAMP webinar kesiti şablonu, analiz/RAPOR.md):
  paylasim : slayt üstte (y=203), altyazı bandı, konuşmacı altta (y=1035), marka zemini
  konusmaci: konuşmacı 4:5 ortada, altyazı altında
  slayt    : slayt ortada büyük, altyazı altında

Kesim kuralı: sınırlar kelime zamanına oturur, hiçbir kelime bölünmez
  (baş = ilk kelimeden 0,12 sn önce, son = son kelimeden 0,25 sn sonra; komşu kelimeye taşmaz).

Kullanım: python3 bin/uret.py <proje> [--no 2] [--taslak]
"""
import argparse
import json
import os
import re
import subprocess
import sys
from collections import Counter

import numpy as np
from PIL import Image, ImageFilter

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FFMPEG = os.path.expanduser("~/.local/bin/ffmpeg")
FONTLAR = os.path.expanduser("~/Library/Fonts")
W, H = 1080, 1920
ON_PAY, SON_PAY = 0.12, 0.25

# 1080x1920 yerleşim (720x1280 ölçümü x1,5)
SLAYT_Y, SLAYT_H = 203, 608
KONUS_Y, KONUS_H = 1035, 608
ALTYAZI_Y_PAYLASIM = 935     # slayt ile konuşmacı arasındaki bandın ortası
ALTYAZI_Y_TEK = 1500


def hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def zemin(marka, yol):
    """Dikey gradyan + ince grunge doku + yumuşak vurgu lekesi (UKCAMP dokusunun marka renkli karşılığı)."""
    z = marka["zemin"]
    ust, alt, vur = map(np.array, (hex2rgb(z["ust"]), hex2rgb(z["alt"]), hex2rgb(z["vurgu"])))
    t = np.linspace(0, 1, H)[:, None, None]
    img = ust * (1 - t) + alt * t
    img = np.repeat(img, W, axis=1)
    rng = np.random.default_rng(7)
    gurultu = rng.normal(0, 1, (H // 6, W // 6))
    gurultu = np.array(Image.fromarray(((gurultu + 3) * 40).clip(0, 255).astype(np.uint8)).resize((W, H), Image.BICUBIC)
                       .filter(ImageFilter.GaussianBlur(3))).astype(float) / 255 - 0.5
    img = img * (1 + z.get("doku", 0.1) * gurultu[..., None] * 2)
    yy, xx = np.mgrid[0:H, 0:W]
    leke = np.exp(-(((xx - W * 0.2) / 700) ** 2 + ((yy - H * 0.48) / 380) ** 2))[..., None]
    img = img * (1 - 0.45 * leke) + vur * 0.45 * leke
    Image.fromarray(img.clip(0, 255).astype(np.uint8)).save(yol)


def ass_renk(h):
    r, g, b = hex2rgb(h)
    return "&H00%02X%02X%02X" % (b, g, r)


def satirla(kelimeler, maxk):
    """Kelime gruplarını en çok 2 satırlık altyazı bloklarına böler (cümle sonunda ve uzun duraklamada keser)."""
    bloklar, cur = [], []
    for i, w in enumerate(kelimeler):
        cur.append(w)
        metin = " ".join(x["w"] for x in cur)
        sonraki = kelimeler[i + 1] if i + 1 < len(kelimeler) else None
        bitir = (len(metin) >= maxk * 1.6 or re.search(r"[.?!]$", w["w"]) or
                 (sonraki and sonraki["b"] - w["e"] > 0.5) or len(cur) >= 8)
        if bitir or sonraki is None:
            bloklar.append(cur)
            cur = []
    return bloklar


def temizle(s, duzeltme=None):
    s = re.sub(r"[.,;:!…]+$", "", s.strip())
    s = re.sub(r"(\d)\s*([,.])\s+(\d)", r"\1\2\3", s)  # "6 ,5" -> "6,5"
    for bul, yaz in (duzeltme or {}).items():
        s = re.sub(bul, yaz, s, flags=re.I)
    s = re.sub(r"\s+(['’])", r"\1", s)  # whisper eki ayrı kelime veriyor: "Üniversitesi 'nde"
    return s.replace("{", "(").replace("}", ")")


def iki_satir(metin, maxk):
    if len(metin) <= maxk:
        return metin
    k = metin.split()
    en_iyi = min(range(1, len(k)), key=lambda i: abs(len(" ".join(k[:i])) - len(" ".join(k[i:]))))
    return " ".join(k[:en_iyi]) + r"\N" + " ".join(k[en_iyi:])


def ass_yaz(yol, bloklar, marka, y):
    a = marka["altyazi"]
    bas = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: R,{a['font']},{a['punto']},{ass_renk(a['renk'])},&H000000FF,{ass_renk(a['kontur'])},&H96000000,{-1 if a.get('kalin') else 0},0,0,0,100,100,0,0,1,{a['kontur_px']},{a['golge_px']},5,60,60,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

    def ts(t):
        t = max(0, t)
        return "%d:%02d:%05.2f" % (t // 3600, (t % 3600) // 60, t % 60)

    satir = []
    for i, (b, e, metin) in enumerate(bloklar):
        if i + 1 < len(bloklar):
            e = min(max(e, b + 0.4), bloklar[i + 1][0])  # boşlukta önceki blok ekranda kalır
            e = bloklar[i + 1][0] if bloklar[i + 1][0] - e < 0.6 else e
        satir.append("Dialogue: 0,%s,%s,R,,0,0,0,,{\\pos(%d,%d)}%s" % (ts(b), ts(e), W // 2, y,
                                                                       iki_satir(metin, a["max_karakter"])))
    open(yol, "w").write(bas + "\n".join(satir) + "\n")


def kelime_listesi(kj):
    return [w for c in kj["cumle"] for w in c["kelime"]]


def sinirla(parca, kel, bosluk):
    """Parça sınırlarını kelimeye ve sessizliğe oturtur. (bas, son, içerideki kelimeler) döndürür.

    whisper bitişik kelimelere yapışık zaman veriyor (bir kelimenin sonu = sonrakinin başı);
    bu yüzden sınır önce sessizlik haritasında aranır, bulunamazsa kelime zamanı + pay kullanılır.
    """
    b0, s0 = parca["bas"], parca["son"]
    # kelime orta noktası parçanın içindeyse alınır (geniş tolerans sonraki cümlenin ilk kelimesini yutuyordu)
    ic = [i for i, w in enumerate(kel) if b0 - 0.15 <= (w["b"] + w["e"]) / 2 <= s0 + 0.15]
    if not ic:
        raise SystemExit("parça boş: %s" % parca)
    i0, i1 = ic[0], ic[-1]
    ilk, son_k = kel[i0], kel[i1]
    bas = ilk["b"] - ON_PAY
    if i0 > 0:
        bas = max(bas, kel[i0 - 1]["e"] + 0.02)
    g = [x for x in bosluk if ilk["b"] - 0.6 <= x["bit"] <= ilk["b"] + 0.3]
    if g:
        x = max(g, key=lambda x: x["bit"])
        bas = max(x["bit"] - ON_PAY, (x["bas"] + x["bit"]) / 2)
    son = son_k["e"] + SON_PAY
    if i1 + 1 < len(kel):
        son = min(son, kel[i1 + 1]["b"] - 0.03)
    g = [x for x in bosluk if son_k["e"] - 0.3 <= x["bas"] <= son_k["e"] + 0.6]
    if g:
        x = min(g, key=lambda x: x["bas"])
        son = min(x["bas"] + SON_PAY, (x["bas"] + x["bit"]) / 2)
    return round(bas, 3), round(son, 3), kel[i0:i1 + 1]


def duzen(yer, bas, son):
    tipler = [o["tip"] for o in yer["ornek"] if bas - 10 <= o["t"] <= son + 10]
    tipler = [t for t in tipler if t in ("paylasim", "konusmaci", "slayt")] or ["konusmaci"]
    d = Counter(tipler).most_common(1)[0][0]
    if d == "paylasim" and not (yer["kutu"]["slayt"] and yer["kutu"]["konusmaci_kucuk"]):
        d = "konusmaci"
    return d


def crop(k):
    x0, y0, x1, y1 = k
    return "crop=%d:%d:%d:%d" % ((x1 - x0) // 2 * 2, (y1 - y0) // 2 * 2, x0, y0)


def filtre(d, yer, n):
    k = yer["kutu"]
    concat = "".join("[%d:v][%d:a]" % (i + 1, i + 1) for i in range(n)) + "concat=n=%d:v=1:a=1[cv][ca];" % n
    norm = "[cv]fps=30,setsar=1,split=2[v1][v2];"
    if d == "paylasim":
        g = (norm +
             "[v1]%s,scale=%d:%d:flags=lanczos[sl];" % (crop(k["slayt"]), W, SLAYT_H) +
             "[v2]%s,scale=%d:%d:flags=lanczos,unsharp=5:5:0.7[kn];" % (crop(k["konusmaci_kucuk"]), W, KONUS_H) +
             "[0:v][sl]overlay=0:%d[a];[a][kn]overlay=0:%d[b]" % (SLAYT_Y, KONUS_Y))
        ay = ALTYAZI_Y_PAYLASIM
    elif d == "slayt":
        g = ("[cv]fps=30,setsar=1,%s,scale=%d:%d:flags=lanczos[sl];" % (crop(k["slayt"]), W, SLAYT_H) +
             "[0:v][sl]overlay=0:%d[b]" % 640)
        ay = ALTYAZI_Y_TEK - 120
    else:
        x0, y0, x1, y1 = k["konusmaci_tam"] or [0, 0] + yer["kaynak"]
        h = y1 - y0
        w = int(h * 4 / 5)
        cx = (x0 + x1) // 2
        kt = [cx - w // 2, y0, cx + w // 2, y1]
        g = ("[cv]fps=30,setsar=1,%s,scale=%d:%d:flags=lanczos[kn];" % (crop(kt), W, 1350) +
             "[0:v][kn]overlay=0:%d[b]" % 220)
        ay = ALTYAZI_Y_TEK
    return concat + g, ay


def calistir(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True, stdin=subprocess.DEVNULL)
    if p.returncode != 0:
        sys.stderr.write(p.stderr[-3000:])
        raise SystemExit("ffmpeg hata")
    return p


def loudnorm_olc(yol):
    p = subprocess.run([FFMPEG, "-nostdin", "-i", yol, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json",
                        "-f", "null", "-"], capture_output=True, text=True)
    return json.loads(p.stderr[p.stderr.rindex("{"):p.stderr.rindex("}") + 1])


def bas_reels(proje, r, kel, yer, marka, taslak, bosluk):
    meta = json.load(open(os.path.join(proje, "proje.json")))
    edit, out = os.path.join(proje, "edit"), os.path.join(proje, "out")
    zy = os.path.join(edit, "zemin_%s.png" % meta["marka"])
    if not os.path.exists(zy):
        zemin(marka, zy)

    duzeltme = dict(marka.get("duzeltme", {}))
    dy = os.path.join(edit, "duzeltme.json")  # proje özel: Claude altyazıyı okuyup yazar
    if os.path.exists(dy):
        duzeltme.update(json.load(open(dy)))
    parcalar, t_cikis, bloklar = [], 0.0, []
    for p in r["parcalar"]:
        bas, son, ws = sinirla(p, kel, bosluk)
        parcalar.append({"bas": bas, "son": son})
        for blok in satirla(ws, marka["altyazi"]["max_karakter"]):
            metin = temizle(" ".join(w["w"] for w in blok), duzeltme)
            if not metin:
                continue
            b_, e_ = t_cikis + blok[0]["b"] - bas, t_cikis + blok[-1]["e"] - bas
            onceki = bloklar[-1] if bloklar else None
            # tek kelimelik blok ("gibi", "oluyor") ekranda yalnız kalmaz: komşusuna eklenir
            if onceki and len(metin.split()) == 1 and b_ - onceki[1] < 0.6 and \
                    len(onceki[2]) + len(metin) <= marka["altyazi"]["max_karakter"] * 2:
                bloklar[-1] = (onceki[0], e_, onceki[2] + " " + metin)
            elif onceki and len(onceki[2].split()) == 1 and b_ - onceki[1] < 0.6 and \
                    len(onceki[2]) + len(metin) <= marka["altyazi"]["max_karakter"] * 2:
                bloklar[-1] = (onceki[0], e_, onceki[2] + " " + metin)
            else:
                bloklar.append((b_, e_, metin))
        t_cikis += son - bas
    d = duzen(yer, parcalar[0]["bas"], parcalar[-1]["son"])
    graf, ay = filtre(d, yer, len(parcalar))
    no = r["no"]
    ass = os.path.join(edit, "reels_%02d.ass" % no)
    ass_yaz(ass, bloklar, marka, ay)
    edl = {"no": no, "duzen": d, "parcalar": parcalar, "sure": round(t_cikis, 2), "baslik": r.get("baslik"),
           "kanca": r.get("kanca"), "neden": r.get("neden")}
    json.dump(edl, open(os.path.join(edit, "reels_%02d_edl.json" % no), "w"), ensure_ascii=False, indent=1)

    ham = os.path.join(edit, "reels_%02d_ham.mp4" % no)
    cmd = [FFMPEG, "-nostdin", "-v", "error", "-y", "-loop", "1", "-framerate", "30", "-t", "%.3f" % t_cikis, "-i", zy]
    for p in parcalar:
        cmd += ["-ss", "%.3f" % p["bas"], "-t", "%.3f" % (p["son"] - p["bas"]), "-i", meta["video"]]
    ass_esc = ass.replace(":", r"\:").replace("'", r"\'")
    graf += ";[b]subtitles='%s':fontsdir='%s'[son]" % (ass_esc, FONTLAR)
    cmd += ["-filter_complex", graf, "-map", "[son]", "-map", "[ca]", "-t", "%.3f" % t_cikis,
            "-c:v", "libx264", "-preset", "veryfast" if taslak else "slow", "-crf", "23" if taslak else "18",
            "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", ham]
    calistir(cmd)

    # ses: iki geçişli loudnorm -14 LUFS (video yeniden kodlanmaz)
    m = loudnorm_olc(ham)
    af = ("loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=%s:measured_TP=%s:measured_LRA=%s:measured_thresh=%s:"
          "offset=%s:linear=true" % (m["input_i"], m["input_tp"], m["input_lra"], m["input_thresh"], m["target_offset"]))
    hedef = os.path.join(out, "reels_%02d.mp4" % no)
    calistir([FFMPEG, "-nostdin", "-v", "error", "-y", "-i", ham, "-c:v", "copy", "-af", af,
              "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", hedef])
    os.remove(ham)
    print("reels %02d  %-9s %5.1f sn  %s" % (no, d, t_cikis, hedef))
    return hedef


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("proje")
    ap.add_argument("--no", type=int, action="append", default=[])
    ap.add_argument("--taslak", action="store_true")
    a = ap.parse_args()
    proje = os.path.abspath(a.proje)
    meta = json.load(open(os.path.join(proje, "proje.json")))
    marka = json.load(open(os.path.join(KOK, "brands", meta["marka"] + ".json")))
    kel = kelime_listesi(json.load(open(os.path.join(proje, "edit", "kelimeler.json"))))
    yer = json.load(open(os.path.join(proje, "edit", "yerlesim.json")))
    anlar = json.load(open(os.path.join(proje, "edit", "anlar.json")))
    bosluk = json.load(open(os.path.join(proje, "edit", "sessizlik.json")))["bosluk"]
    for r in anlar["reels"]:
        if a.no and r["no"] not in a.no:
            continue
        bas_reels(proje, r, kel, yer, marka, a.taslak, bosluk)


if __name__ == "__main__":
    main()

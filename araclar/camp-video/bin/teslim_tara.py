#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Teslim edilen videoyu yeniden dinleyip KALAN kusurlari bulur.

Ham transkript bu cumleleri bazen hic yazmiyor (CH33: "Surayi bastan aliyorum"
kalip taramasinda hic cikmadi), o yuzden kaynak metne degil URETILEN VIDEOYA
bakilir. Seyircinin duydugu ses tek yetkilidir.

Uc kusur aranir:
  1. Editore soylenen ilanlar ("bastan aliyorum", "burayi keselim", "edit")
  2. Slayt/kitap meta yorumu ("kitapta yok", "burasi yanlis")
  3. Sozsuz ses: ne sessizlik ne kelime olan araliklar (oksuruk, bogaz temizleme)
"""
import json
import os
import re
import subprocess
import sys
import tempfile

KOK = os.path.expanduser("~/camp-video")
TESLIM = os.path.expanduser("~/Downloads/CAMPVERSE Dersler/Editli")
FFMPEG = os.path.expanduser("~/.local/bin/ffmpeg")
FFPROBE = os.path.expanduser("~/.local/bin/ffprobe")
MLX = os.path.expanduser("~/.local/bin/mlx_whisper")
CIKTI = os.path.join(KOK, "takip", "teslim_tarama")

ILAN = re.compile(
    r"baştan al|bastan al|tekrar al|baştan başl|bastan basl|yeniden al|burayı al|burayi al|"
    r"burayı kes|burayi kes|burasını kes|bunu kes|edit yap|editle|edit'?l|kesel|çıkaral|cikaral|"
    r"koymayal|almayal|tekrar çek|tekrar cek|baştan söyl|bastan soyl|tekrar edeceğim|"
    r"tekrar anlatacağım|tekrar alacağım|tekrar alıyorum|baştan alacağım|baştan alıyorum|"
    r"buraya tekrar|burayı tekrar|burayi tekrar|revize", re.I)
META = re.compile(
    r"kitap\w*.{0,30}?(yok|yanlış|yanlis|hata|düzelt|duzelt)|kitab\w*.{0,30}?(yok|yanlış|yanlis|hata|düzelt|duzelt)|"
    r"slayt\w*.{0,30}?(yok|yanlış|yanlis|hata)|slide\w*.{0,30}?(yok|yanlış|yanlis|hata)|"
    r"görsel\w*.{0,20}?hata|gorsel\w*.{0,20}?hata|resim.{0,15}?kay|"
    r"burası yanlış|burasi yanlis|bu kısım yanlış|yanlış yazılmış|yanlis yazilmis|"
    r"hatalı yazılmış|hatali yazilmis|düzeltmenizi|duzeltmenizi|değiştirmenizi|degistirmenizi|"
    r"lütfen silin|lutfen silin", re.I)


def sure(y):
    r = subprocess.run([FFPROBE, "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", y], capture_output=True, text=True)
    return float(r.stdout.strip())


def sessizlikler(y):
    r = subprocess.run([FFMPEG, "-nostats", "-v", "info", "-i", y, "-af",
                        "silencedetect=noise=-35dB:d=0.25", "-f", "null", "-"],
                       capture_output=True, text=True)
    bas, out = None, []
    for m in re.finditer(r"silence_(start|end): (-?[\d.]+)", r.stderr):
        if m.group(1) == "start":
            bas = float(m.group(2))
        elif bas is not None:
            out.append((bas, float(m.group(2)))); bas = None
    return out


def coz(y, toplam, parca=600.0):
    seg = []
    with tempfile.TemporaryDirectory() as td:
        t = 0.0
        while t < toplam:
            u = min(parca, toplam - t)
            w = os.path.join(td, "p.wav")
            subprocess.run([FFMPEG, "-v", "error", "-ss", str(t), "-t", str(u), "-i", y,
                            "-ac", "1", "-ar", "16000", "-y", w], check=False)
            q = subprocess.run([MLX, w, "--model", "mlx-community/whisper-large-v3-turbo",
                                "--language", "tr", "--output-dir", td,
                                "--output-format", "json", "--verbose", "False"],
                               capture_output=True, text=True)
            jy = os.path.join(td, "p.json")
            if q.returncode == 0 and os.path.exists(jy):
                for s in json.load(open(jy)).get("segments", []):
                    seg.append({"bas": round(s["start"] + t, 2),
                                "bit": round(s["end"] + t, 2),
                                "metin": s["text"].strip()})
                os.remove(jy)
            t += u
    return seg


def main():
    ad = sys.argv[1]
    y = os.path.join(TESLIM, ad)
    os.makedirs(CIKTI, exist_ok=True)
    hedef = os.path.join(CIKTI, ad.replace(".mp4", ".json"))
    if os.path.exists(hedef):
        print("zaten var: %s" % ad); return
    toplam = sure(y)
    seg = coz(y, toplam)
    ses = sessizlikler(y)

    bulgu = []
    for s in seg:
        if ILAN.search(s["metin"]):
            bulgu.append({"tur": "ilan", "bas": s["bas"], "bit": s["bit"], "metin": s["metin"]})
        elif META.search(s["metin"]):
            bulgu.append({"tur": "meta", "bas": s["bas"], "bit": s["bit"], "metin": s["metin"]})

    # sozsuz ses: kelimelerin arasinda kalan, sessizlik OLMAYAN araliklar
    seg.sort(key=lambda s: s["bas"])
    for i in range(len(seg) - 1):
        a, b = seg[i]["bit"], seg[i + 1]["bas"]
        if not (0.45 <= b - a <= 3.0):
            continue
        # Oksuruk imzasi: hoca susar, kisa ve yuksek bir ses cikarir, tekrar susar.
        # Yani araligin ORTASINDA ses, IKI YANINDA gercek sessizlik olmali. Bu sart
        # olmadan whisper'in cumle bolme yerleri de aday cikiyordu (CH32'de 73 yanlis
        # alarm). (23.09.2026)
        on = sum(max(0.0, min(a + 0.25, e2) - max(a, b2)) for b2, e2 in ses)
        arka = sum(max(0.0, min(b, e2) - max(b - 0.25, b2)) for b2, e2 in ses)
        orta = sum(max(0.0, min(b - 0.25, e2) - max(a + 0.25, b2)) for b2, e2 in ses)
        ic = max(0.01, (b - 0.25) - (a + 0.25))
        if on >= 0.18 and arka >= 0.18 and orta < ic * 0.45 and (b - a) <= 2.0:
            bulgu.append({"tur": "sozsuz_ses", "bas": round(a, 2), "bit": round(b, 2),
                          "sure": round(b - a, 2), "ic_ses_orani": round(1 - orta / ic, 2)})

    json.dump({"ders": ad, "sure": round(toplam, 2), "bulgu": bulgu,
               "sessizlik": [[round(x, 2), round(y, 2)] for x, y in ses],
               "segment": seg}, open(hedef, "w"), ensure_ascii=False, indent=1)
    print("%-52s %d bulgu (%d ilan, %d meta, %d sozsuz)"
          % (ad[:52], len(bulgu),
             sum(1 for x in bulgu if x["tur"] == "ilan"),
             sum(1 for x in bulgu if x["tur"] == "meta"),
             sum(1 for x in bulgu if x["tur"] == "sozsuz_ses")))


if __name__ == "__main__":
    main()

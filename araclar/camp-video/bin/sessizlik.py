#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sessizlik haritası: kesim sınırlarının TEK yetkili kaynağı.

Kesimin nereye oturacağına transkript değil bu ölçüm karar verir.
ffmpeg silencedetect çıktısı ses dalgasından gelir, dile ve ASR kalitesine bağlı değildir.

Kullanım:
    python3 bin/sessizlik.py <video> [--esik -35] [--sure 0.30] [--out edit/sessizlik.json]
    python3 bin/sessizlik.py <video> --yakin 540      # 9. dakikaya en yakın boşluk
"""
import argparse
import json
import os
import re
import subprocess
import sys

FFMPEG = os.path.expanduser("~/.local/bin/ffmpeg")
FFPROBE = os.path.expanduser("~/.local/bin/ffprobe")

RX_START = re.compile(r"silence_start:\s*(-?[\d.]+)")
RX_END = re.compile(r"silence_end:\s*([\d.]+)\s*\|\s*silence_duration:\s*([\d.]+)")


def sure(video):
    out = subprocess.run([FFPROBE, "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", video], capture_output=True, text=True)
    return float(out.stdout.strip())


def harita(video, esik=-35.0, min_sure=0.30):
    """[{bas, bit, sure}] listesi döndürür."""
    cmd = [FFMPEG, "-v", "info", "-i", video, "-af",
           "silencedetect=noise=%ddB:d=%s" % (int(esik), min_sure), "-f", "null", "-"]
    p = subprocess.run(cmd, capture_output=True, text=True)
    satirlar = (p.stderr or "").splitlines()
    bosluk, acik = [], None
    for s in satirlar:
        m = RX_START.search(s)
        if m:
            acik = float(m.group(1))
            continue
        m = RX_END.search(s)
        if m and acik is not None:
            bit = float(m.group(1))
            bosluk.append({"bas": round(acik, 3), "bit": round(bit, 3),
                           "sure": round(float(m.group(2)), 3)})
            acik = None
    return bosluk


def konusma_sinirlari(bosluk, toplam):
    """İlk konuşmanın başlangıcı ve son konuşmanın bitişi."""
    ilk = 0.0
    if bosluk and bosluk[0]["bas"] <= 0.05:
        ilk = bosluk[0]["bit"]
    son = toplam
    if bosluk and abs(bosluk[-1]["bit"] - toplam) < 1.0:
        son = bosluk[-1]["bas"]
    return round(ilk, 3), round(son, 3)


def en_yakin(bosluk, hedef, pencere=90.0, min_sure=0.30):
    """Hedef saniyeye en yakın, yeterince uzun boşluklar (yakından uzağa)."""
    aday = [b for b in bosluk
            if b["sure"] >= min_sure and abs((b["bas"] + b["bit"]) / 2.0 - hedef) <= pencere]
    aday.sort(key=lambda b: abs((b["bas"] + b["bit"]) / 2.0 - hedef))
    return aday


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--esik", type=float, default=-35.0, help="dB eşiği (varsayılan -35)")
    ap.add_argument("--sure", type=float, default=0.30, help="en kısa boşluk sn (varsayılan 0.30)")
    ap.add_argument("--out", default=None)
    ap.add_argument("--yakin", type=float, default=None, help="bu saniyeye en yakın boşlukları yaz")
    a = ap.parse_args()

    toplam = sure(a.video)
    b = harita(a.video, a.esik, a.sure)
    ilk, son = konusma_sinirlari(b, toplam)

    if a.yakin is not None:
        for x in en_yakin(b, a.yakin)[:8]:
            orta = (x["bas"] + x["bit"]) / 2.0
            print("  %7.2f - %7.2f  (%.2f sn)  orta=%7.2f  [%d:%05.2f]  hedefe %+.1f sn"
                  % (x["bas"], x["bit"], x["sure"], orta, int(orta // 60), orta % 60,
                     orta - a.yakin))
        return

    out = a.out or os.path.join(os.path.dirname(a.video) or ".", "edit", "sessizlik.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as f:
        json.dump({"video": os.path.abspath(a.video), "toplam_sure": round(toplam, 3),
                   "esik_db": a.esik, "min_sure": a.sure,
                   "ilk_konusma": ilk, "son_konusma": son, "bosluk": b}, f, indent=1)
    print("Sure: %.2f sn (%d:%02d)" % (toplam, toplam // 60, toplam % 60))
    print("Bosluk sayisi: %d" % len(b))
    print("Ilk konusma: %.2f sn | Son konusma: %.2f sn (kuyrukta %.1f sn sessizlik)"
          % (ilk, son, toplam - son))
    print("->", out)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gece uretiminin kapanis denetimi: her ders teslim edildi mi, kapilardan gecti mi."""
import json
import os
import re
import subprocess
import sys

KOK = os.path.expanduser("~/camp-video")
TESLIM = os.path.expanduser("~/Downloads/CAMPVERSE Dersler/Editli")
FFPROBE = os.path.expanduser("~/.local/bin/ffprobe")


def sure(y):
    r = subprocess.run([FFPROBE, "-v", "error", "-select_streams", "v:0",
                        "-show_entries", "format=duration:stream=width,height",
                        "-of", "json", y], capture_output=True, text=True)
    try:
        d = json.loads(r.stdout)
        s = d["streams"][0]
        return float(d["format"]["duration"]), s["width"], s["height"]
    except Exception:
        return None, None, None


def main():
    eksik, bozuk, tamam = [], [], []
    for d in sorted(os.listdir(os.path.join(KOK, "projects"))):
        p = os.path.join(KOK, "projects", d)
        m = re.match(r"campverse-ch(\d+)-", d)
        if not m or not os.path.exists(os.path.join(p, "ders.mp4")):
            continue
        no = int(m.group(1))
        aday = [f for f in os.listdir(TESLIM) if f.startswith("%02d - " % no)] \
            if os.path.isdir(TESLIM) else []
        if not aday:
            eksik.append("CH%02d" % no); continue
        y = os.path.join(TESLIM, aday[0])
        sn, w, h = sure(y)
        if sn is None:
            bozuk.append("CH%02d okunamadi" % no)
        elif (w, h) != (1920, 1080):
            bozuk.append("CH%02d %sx%s" % (no, w, h))
        elif sn < 60:
            bozuk.append("CH%02d yalniz %.0f sn" % (no, sn))
        else:
            tamam.append((no, aday[0], sn))

    print("TESLIM EDILEN: %d ders" % len(tamam))
    if eksik:
        print("EKSIK (%d): %s" % (len(eksik), ", ".join(eksik)))
    if bozuk:
        print("BOZUK (%d): %s" % (len(bozuk), ", ".join(bozuk)))
    top = sum(s for _, _, s in tamam)
    print("Toplam sure: %.1f saat · ortalama %.1f dk" %
          (top / 3600, top / 60 / max(1, len(tamam))))
    sys.exit(1 if (eksik or bozuk) else 0)


if __name__ == "__main__":
    main()

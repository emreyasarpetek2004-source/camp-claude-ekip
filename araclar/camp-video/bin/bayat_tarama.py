#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Teslim taramasi guncel mi? mtime GUVENILMEZ: teslim_coz.py dosyayi
yeniden yazinca mtime tazeleniyor ve bayat tarama guncel gorunuyor.
Tek saglam olcut TESLIM VIDEOSUNUN SURESI: kurgu degistiyse sure degisir.
(23.09.2026 - CH34/37/53 bu yuzden eski kurguyla denetlenmisti.)

Cikti: bayat tarama dosyalarinin yolu, satir satir.
"""
import json, os, subprocess, glob, sys

D = os.path.expanduser("~/camp-video/takip/teslim_tarama")
T = os.path.expanduser("~/Downloads/CAMPVERSE Dersler/Editli")

def sure(y):
    return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
        "-of","csv=p=0",y],capture_output=True,text=True).stdout.strip() or 0)

for f in sorted(glob.glob(D + "/*.json")):
    try: d = json.load(open(f))
    except Exception: print(f); continue
    yol = os.path.join(T, d.get("ders",""))
    if not os.path.exists(yol) or not isinstance(d.get("segment"), list):
        print(f); continue
    if abs(sure(yol) - d.get("sure", 0)) > 1.0:
        print(f)

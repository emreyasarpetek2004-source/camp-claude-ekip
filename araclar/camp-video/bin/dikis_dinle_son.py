#!/usr/bin/env python3
"""Sinira degen kelimeli dikisleri 'duyulacagi gibi' (ham [bas-3,bas] + [bit,bit+3]) birlestirip
cozer; dikisin iki yanindaki kelimeleri yazar (05.10.2026)."""
import glob, json, os, subprocess, sys, tempfile
FF = os.path.expanduser("~/.local/bin/ffmpeg"); MLX = os.path.expanduser("~/.local/bin/mlx_whisper")
for f in sorted(glob.glob(os.path.expanduser("~/camp-video/projects/*/edit/kesim_metni_son.json"))):
    km = json.load(open(f)); ham = os.path.join(os.path.dirname(os.path.dirname(f)), "ders.mp4")
    for i, k in enumerate(km, 1):
        o = k["once"][-1] if k["once"] else None; s = k["sonra"][0] if k["sonra"] else None
        if not ((o and o[1] > k["bas"] + 0.05) or (s and s[0] < k["bit"] - 0.05)): continue
        with tempfile.TemporaryDirectory() as td:
            a = td + "/a.wav"; b = td + "/b.wav"; c = td + "/c.wav"
            subprocess.run([FF, "-v", "error", "-y", "-ss", "%.3f" % max(0, k["bas"] - 3), "-to", "%.3f" % k["bas"], "-i", ham, "-ac", "1", "-ar", "16000", a])
            subprocess.run([FF, "-v", "error", "-y", "-ss", "%.3f" % k["bit"], "-t", "3", "-i", ham, "-ac", "1", "-ar", "16000", b])
            subprocess.run([FF, "-v", "error", "-y", "-i", a, "-i", b, "-filter_complex", "concat=n=2:v=0:a=1", c])
            q = subprocess.run([MLX, c, "--language", "tr", "--model", "mlx-community/whisper-large-v3-turbo", "--output-dir", td,
                                "--output-format", "txt", "--verbose", "False", "--condition-on-previous-text", "False"], capture_output=True, text=True)
            t = open(td + "/c.txt").read().strip().replace("\n", " ") if os.path.exists(td + "/c.txt") else "?"
        print("%s #%d  [%s | %s]  ->  %s" % (f.split("/")[-3][10:30], i, o[2] if o else "", s[2] if s else "", t), flush=True)

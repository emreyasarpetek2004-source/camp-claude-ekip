#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mevcut kesim sinirinin DIKISINI kurup dinletir: akiyor mu, yarim mi kaliyor.

9 saniyelik pencere tam kesimde bittigi icin cumle her zaman yarim gorunuyor;
tek guvenilir olcut, kesimin iki yanini birlestirip okumak. (23.09.2026)
"""
import json, os, subprocess, sys, tempfile

KOK = os.path.expanduser("~/camp-video")
FFMPEG = os.path.expanduser("~/.local/bin/ffmpeg")
MLX = os.path.expanduser("~/.local/bin/mlx_whisper")


def dikis(video, once_bas, kes_bas, kes_bit, sonra=6.0):
    with tempfile.TemporaryDirectory() as td:
        a, b, l = (os.path.join(td, x) for x in ("a.wav", "b.wav", "l.txt"))
        subprocess.run([FFMPEG, "-v", "error", "-ss", "%.2f" % once_bas,
                        "-t", "%.2f" % (kes_bas - once_bas), "-i", video,
                        "-ac", "1", "-ar", "16000", "-y", a], check=False)
        subprocess.run([FFMPEG, "-v", "error", "-ss", "%.2f" % kes_bit,
                        "-t", "%.2f" % sonra, "-i", video,
                        "-ac", "1", "-ar", "16000", "-y", b], check=False)
        open(l, "w").write("file '%s'\nfile '%s'\n" % (a, b))
        d = os.path.join(td, "d.wav")
        subprocess.run([FFMPEG, "-v", "error", "-f", "concat", "-safe", "0",
                        "-i", l, "-c", "copy", "-y", d], check=False)
        q = subprocess.run([MLX, d, "--model", "mlx-community/whisper-large-v3-turbo",
                            "--language", "tr", "--output-dir", td,
                            "--output-format", "txt", "--verbose", "False"],
                           capture_output=True, text=True)
        ty = os.path.join(td, "d.txt")
        return " ".join(open(ty).read().split()) if (q.returncode == 0 and os.path.exists(ty)) else None


def main():
    adaylar = [x for x in json.load(open(os.path.join(KOK, "takip", "yarim_cumle.json")))
               if x["yarim"]]
    for a in adaylar:
        proje = os.path.join(KOK, "projects", a["ders"])
        v, ey = os.path.join(proje, "ders.mp4"), os.path.join(proje, "edit", "edl.json")
        S = float(a["kesim"])
        rs = json.load(open(ey))["ranges"]
        bit = next((float(rs[i + 1]["start"]) for i in range(len(rs) - 1)
                    if abs(float(rs[i]["end"]) - S) < 0.01), None)
        if bit is None:
            print("== %-40s %8.2f  EDL'de bulunamadi" % (a["ders"][:40], S)); continue
        m = dikis(v, max(0, S - 9), S, bit)
        print("== %-40s kesim %8.2f -> %8.2f\n   %s\n" % (
            a["ders"].replace("campverse-", "")[:40], S, bit, m or "(cozulemedi)"))


if __name__ == "__main__":
    main()

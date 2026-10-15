#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Aday kesimlerin oncesini SESTEN dinleyip cumle yarim mi bakar.

Metin uzerinden karar vermek yaniltiyor (cumle birlestirme uzun bloklar uretiyor).
Tek guvenilir olcut: kesimden onceki 9 saniyeyi cozup son cumlenin tamamlanip
tamamlanmadigina bakmak.
"""
import json, os, re, subprocess, sys, tempfile

KOK = os.path.expanduser("~/camp-video")
FFMPEG = os.path.expanduser("~/.local/bin/ffmpeg")
MLX = os.path.expanduser("~/.local/bin/mlx_whisper")
BITIS = re.compile(r"[.!?]\s*$")
YARIM = re.compile(r"\b(ve|ama|eğer|çünkü|ki|de|da|ile|için|yani|bu|şu|o|bir)\s*$", re.I)


def son_cumle(video, t):
    with tempfile.TemporaryDirectory() as td:
        w = os.path.join(td, "a.wav")
        subprocess.run([FFMPEG, "-v", "error", "-ss", "%.2f" % max(0, t - 9), "-t", "9",
                        "-i", video, "-ac", "1", "-ar", "16000", "-y", w], check=False)
        q = subprocess.run([MLX, w, "--model", "mlx-community/whisper-large-v3-turbo",
                            "--language", "tr", "--output-dir", td,
                            "--output-format", "txt", "--verbose", "False"],
                           capture_output=True, text=True)
        ty = os.path.join(td, "a.txt")
        if q.returncode != 0 or not os.path.exists(ty):
            return None
        return " ".join(open(ty).read().split())


def main():
    adaylar = json.load(open(sys.argv[1]))
    out = []
    for a in adaylar:
        v = os.path.join(KOK, "projects", a["ders"], "ders.mp4")
        m = son_cumle(v, a["kesim"])
        if m is None:
            continue
        yarim = not BITIS.search(m) or bool(YARIM.search(m))
        out.append(dict(a, metin=m[-110:], yarim=yarim))
        print("%-42s %8.2f  %s  ...%s"
              % (a["ders"].replace("campverse-", "")[:42], a["kesim"],
                 "YARIM" if yarim else "tam  ", m[-80:]))
    json.dump(out, open(os.path.join(KOK, "takip", "yarim_cumle.json"), "w"),
              ensure_ascii=False, indent=1)
    print("\nYARIM: %d / %d" % (sum(1 for x in out if x["yarim"]), len(out)))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Yarim cumle ustunde baslayan kesimler icin YENI SINIR onerir.

Kesimden onceki 16 saniye cozulur, TAMAMLANAN son cumlenin bitisi bulunur ve
kesimin basi oraya cekilir. Sinir sessizlige oturtulur.
(23.09.2026 kararı: "yeniden cekim ilanindan onceki yarim cumle de gitmeli.")
"""
import json, os, re, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hat import ince_bosluklar

KOK = os.path.expanduser("~/camp-video")
FFMPEG = os.path.expanduser("~/.local/bin/ffmpeg")
MLX = os.path.expanduser("~/.local/bin/mlx_whisper")
BITIS = re.compile(r"[.!?]\s*$")


def coz(video, a, sure):
    with tempfile.TemporaryDirectory() as td:
        w = os.path.join(td, "a.wav")
        subprocess.run([FFMPEG, "-v", "error", "-ss", "%.2f" % a, "-t", "%.2f" % sure,
                        "-i", video, "-ac", "1", "-ar", "16000", "-y", w], check=False)
        q = subprocess.run([MLX, w, "--model", "mlx-community/whisper-large-v3-turbo",
                            "--language", "tr", "--output-dir", td,
                            "--output-format", "json", "--verbose", "False"],
                           capture_output=True, text=True)
        jy = os.path.join(td, "a.json")
        if q.returncode != 0 or not os.path.exists(jy):
            return []
        return [{"bas": s["start"] + a, "bit": s["end"] + a, "metin": s["text"].strip()}
                for s in json.load(open(jy)).get("segments", [])]


def main():
    adaylar = [x for x in json.load(open(os.path.join(KOK, "takip", "yarim_cumle.json")))
               if x["yarim"]]
    oneri = []
    for a in adaylar:
        proje = os.path.join(KOK, "projects", a["ders"])
        v = os.path.join(proje, "ders.mp4")
        S = float(a["kesim"])
        seg = coz(v, max(0, S - 16), min(17.0, S))
        tam = [s for s in seg if BITIS.search(s["metin"]) and s["bit"] <= S - 0.3]
        if not tam:
            print("  %-42s %8.2f  TAM CUMLE BULUNAMADI" % (a["ders"][:42], S)); continue
        bit = tam[-1]["bit"]
        bos = [b for b in ince_bosluklar(v, bit, yaricap=2.0) if b["sure"] >= 0.10]
        yakin = [b for b in bos if abs(b["bas"] - bit) <= 1.6 or abs(b["bit"] - bit) <= 1.6]
        if yakin:
            b = min(yakin, key=lambda x: min(abs(x["bas"] - bit), abs(x["bit"] - bit)))
            yeni = round((b["bas"] + b["bit"]) / 2.0, 2)
        else:
            yeni = round(bit + 0.10, 2)
        if yeni >= S - 0.2:
            print("  %-42s %8.2f  degisiklik gerekmiyor" % (a["ders"][:42], S)); continue
        oneri.append({"ders": a["ders"], "eski": S, "yeni": yeni,
                      "kalan": tam[-1]["metin"][-60:],
                      "atilan": " ".join(s["metin"] for s in seg if s["bas"] >= bit)[:110]})
        print("  %-42s %8.2f -> %8.2f  (%.1f sn once)\n      kalan: ...%s\n      atilan: %s"
              % (a["ders"].replace("campverse-", "")[:42], S, yeni, S - yeni,
                 tam[-1]["metin"][-55:], oneri[-1]["atilan"][:95]))
    json.dump(oneri, open(os.path.join(KOK, "takip", "yarim_cumle_oneri.json"), "w"),
              ensure_ascii=False, indent=1)
    print("\n%d oneri -> takip/yarim_cumle_oneri.json" % len(oneri))


if __name__ == "__main__":
    main()

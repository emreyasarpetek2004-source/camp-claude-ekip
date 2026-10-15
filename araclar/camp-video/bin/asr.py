#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pencere bazlı yerel transkript (ücretsiz, mlx-whisper).

Tam dersi çözmez: yalnız karar için gereken pencereleri çözer.
Dil DAİMA açıkça verilir; otomatik algılama tıbbi terimlerde İngilizceye kayıyor.

Bu transkript kesim SINIRINI belirlemez (o sessizlik ölçümünden gelir).
Tek işi "burada ders mi anlatılıyor, yoksa kesinti mi" sorusunu cevaplamak.

Kullanım:
    python3 bin/asr.py <video> --pencere 0:90 --pencere 530:560
    python3 bin/asr.py <video> --nokta 540 --yaricap 90
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile

FFMPEG = os.path.expanduser("~/.local/bin/ffmpeg")
MLX = os.path.expanduser("~/.local/bin/mlx_whisper")
VARSAYILAN_MODEL = "mlx-community/whisper-large-v3-turbo"


def pencere_coz(video, bas, bit, model, dil="tr"):
    sure = max(0.5, bit - bas)
    with tempfile.TemporaryDirectory() as td:
        wav = os.path.join(td, "p.wav")
        subprocess.run([FFMPEG, "-v", "error", "-ss", str(bas), "-t", str(sure),
                        "-i", video, "-ac", "1", "-ar", "16000", "-y", wav], check=True)
        cmd = [MLX, wav, "--model", model, "--language", dil,
               "--output-dir", td, "--output-format", "json", "--verbose", "False"]
        p = subprocess.run(cmd, capture_output=True, text=True)
        if p.returncode != 0:
            sys.stderr.write(p.stderr[-2000:])
            raise SystemExit("mlx_whisper hata verdi")
        js = os.path.join(td, "p.json")
        d = json.load(open(js))
    for s in d.get("segments", []):
        s["start"] = round(s["start"] + bas, 2)
        s["end"] = round(s["end"] + bas, 2)
    return {"bas": bas, "bit": bit, "metin": (d.get("text") or "").strip(),
            "segment": [{"bas": s["start"], "bit": s["end"], "metin": s["text"].strip()}
                        for s in d.get("segments", [])]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--pencere", action="append", default=[],
                    help="bas:bit saniye, birden fazla verilebilir")
    ap.add_argument("--nokta", action="append", type=float, default=[],
                    help="kesim noktasi; +-yaricap kadar pencere acilir")
    ap.add_argument("--yaricap", type=float, default=90.0)
    ap.add_argument("--model", default=VARSAYILAN_MODEL)
    ap.add_argument("--dil", default="tr")
    ap.add_argument("--tam", action="store_true",
                    help="tum dersi cozumle (tekrar avi icin sart)")
    ap.add_argument("--out", default=None)
    ap.add_argument("--parca", type=float, default=600.0,
                    help="--tam icin dilim uzunlugu sn (0 = bolme)")
    ap.add_argument("--sessizlik", default=None,
                    help="dilim sinirlarini secmek icin sessizlik.json")
    a = ap.parse_args()

    pencereler = []
    for p in a.pencere:
        b, e = p.split(":")
        pencereler.append((float(b), float(e)))
    for n in a.nokta:
        pencereler.append((max(0.0, n - a.yaricap), n + a.yaricap))

    if a.tam:
        import subprocess as _sp
        sure = float(_sp.run([os.path.expanduser("~/.local/bin/ffprobe"), "-v", "error",
                              "-show_entries", "format=duration", "-of", "csv=p=0", a.video],
                             capture_output=True, text=True).stdout.strip())
        # Tum dersi tek pencerede cozmek mel spektrogramini bir kerede bellege aliyor;
        # 16 GB'lik makinede bu swap'e dusuyor ve is 2.5x gercek zamana kadar yavasliyor.
        # Kayit ~parca saniyelik dilimlere bolunur. Sinirlar SESSIZLIKTEN secilir, boylece
        # hicbir kelime ikiye bolunmez ve ortusme (dolayisiyla sahte tekrar) olmaz.
        if a.parca and sure > a.parca * 1.5:
            bos = []
            sy = a.sessizlik or os.path.join(os.path.dirname(a.video) or ".",
                                             "edit", "sessizlik.json")
            if os.path.exists(sy):
                try:
                    bos = json.load(open(sy)).get("bosluk", [])
                except Exception:
                    bos = []
            sinir, t = [0.0], float(a.parca)
            while t < sure - a.parca * 0.4:
                yakin = [b for b in bos if abs((b["bas"] + b["bit"]) / 2 - t) <= 45]
                if yakin:
                    b = max(yakin, key=lambda x: x["sure"])
                    kes = round((b["bas"] + b["bit"]) / 2, 2)
                else:
                    kes = round(t, 2)
                if kes > sinir[-1] + 30:
                    sinir.append(kes)
                t = kes + a.parca
            sinir.append(sure)
            pencereler = list(zip(sinir[:-1], sinir[1:]))
            sys.stderr.write("... %d parcaya bolundu (sessizlik sinirli)\n" % len(pencereler))
        else:
            pencereler = [(0.0, sure)]
    if not pencereler:
        raise SystemExit("En az bir --pencere ya da --nokta ver")

    sonuc = []
    for b, e in pencereler:
        sys.stderr.write("... %0.1f-%0.1f cozuluyor\n" % (b, e))
        sonuc.append(pencere_coz(a.video, b, e, a.model, a.dil))

    out = a.out or os.path.join(os.path.dirname(a.video) or ".", "edit", "transkript.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    mevcut = {}
    if os.path.exists(out):
        mevcut = json.load(open(out))
    mevcut.setdefault("pencere", [])
    mevcut["model"] = a.model
    mevcut["dil"] = a.dil
    mevcut["pencere"] = [p for p in mevcut["pencere"]
                         if not any(abs(p["bas"] - s["bas"]) < 0.01 for s in sonuc)] + sonuc
    mevcut["pencere"].sort(key=lambda p: p["bas"])
    with open(out, "w") as f:
        json.dump(mevcut, f, ensure_ascii=False, indent=1)

    for s in sonuc:
        print("\n### %d:%02d - %d:%02d" % (s["bas"] // 60, s["bas"] % 60, s["bit"] // 60, s["bit"] % 60))
        for g in s["segment"]:
            print("  [%6.1f] %s" % (g["bas"], g["metin"]))
    print("\n->", out)


if __name__ == "__main__":
    main()

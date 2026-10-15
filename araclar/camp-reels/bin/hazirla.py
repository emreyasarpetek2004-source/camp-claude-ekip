#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Webinar kaydını reels kurgusuna hazırlar (OLGU katmanı, karar vermez).

Üretir (projects/<ad>/edit/):
  probe.json       ffprobe envanteri
  sessizlik.json   kesim sınırlarının tek yetkili kaynağı (camp-video/bin/sessizlik.py)
  kelimeler.json   kelime zamanlı tam transkript (mlx-whisper, 10 dk parçalar, sessizlikte bölünür)
  ses.wav          16 kHz mono (ASR ve denetim için)

Kullanım:
  python3 bin/hazirla.py <kayit.mp4> --marka dentcamp [--ad dentcamp-2209-ingiltere]
"""
import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import unicodedata

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FFMPEG = os.path.expanduser("~/.local/bin/ffmpeg")
FFPROBE = os.path.expanduser("~/.local/bin/ffprobe")
MLX = os.path.expanduser("~/.local/bin/mlx_whisper")
MODEL = "mlx-community/whisper-large-v3-turbo"
PARCA = 600.0

sys.path.insert(0, os.path.expanduser("~/camp-video/bin"))
from sessizlik import harita  # noqa: E402

# whisper müzik/sessizlikte bunları uyduruyor (analizde ölçüldü: "Altyazı M.K.")
HALUSINASYON = re.compile(r"altyaz[ıi]\s*m\.?\s*k\.?|abone ol|izlediğiniz için teşekkür", re.I)


def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:50]


def probe(video):
    out = subprocess.run([FFPROBE, "-v", "error", "-show_entries",
                          "stream=index,codec_type,width,height,r_frame_rate:format=duration",
                          "-of", "json", video], capture_output=True, text=True, check=True)
    return json.loads(out.stdout)


def parca_sinirlari(sure, bosluk):
    """~10 dk dilimler; sınır en uzun yakın sessizliğin ortası (kelime bölünmez)."""
    sinir, t = [0.0], PARCA
    while t < sure - PARCA * 0.4:
        yakin = [b for b in bosluk if abs((b["bas"] + b["bit"]) / 2 - t) <= 45]
        if yakin:
            en = max(yakin, key=lambda x: x["sure"])
            kes = round((en["bas"] + en["bit"]) / 2, 2)
        else:
            kes = round(t, 2)
        if kes > sinir[-1] + 30:
            sinir.append(kes)
        t = kes + PARCA
    sinir.append(sure)
    return list(zip(sinir[:-1], sinir[1:]))


def coz(wav, bas, bit, dil, sozluk=""):
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "p.wav")
        subprocess.run([FFMPEG, "-nostdin", "-v", "error", "-ss", str(bas), "-t", str(bit - bas),
                        "-i", wav, "-y", p], check=True)
        r = subprocess.run([MLX, p, "--model", MODEL, "--language", dil, "--word-timestamps", "True",
                            "--condition-on-previous-text", "False",
                            "--hallucination-silence-threshold", "2",
                            "--initial-prompt", sozluk,
                            "-o", td, "-f", "json", "--verbose", "False"],
                           capture_output=True, text=True, stdin=subprocess.DEVNULL)
        if r.returncode != 0:
            sys.stderr.write(r.stderr[-1500:])
            raise SystemExit("mlx_whisper hata verdi (%.0f-%.0f)" % (bas, bit))
        d = json.load(open(os.path.join(td, "p.json")))
    cumleler = []
    for sg in d.get("segments", []):
        metin = sg["text"].strip()
        if not metin or HALUSINASYON.search(metin):
            continue
        ws = [{"w": w["word"].strip(), "b": round(w["start"] + bas, 3), "e": round(w["end"] + bas, 3),
               "p": round(w.get("probability", 1.0), 3)} for w in sg.get("words", []) if w["word"].strip()]
        if ws:
            cumleler.append({"b": ws[0]["b"], "e": ws[-1]["e"], "metin": metin, "kelime": ws})
    return cumleler


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--marka", required=True, choices=["dentcamp", "ukcamp", "auscamp"])
    ap.add_argument("--ad", default=None)
    ap.add_argument("--dil", default="tr")
    a = ap.parse_args()

    video = os.path.abspath(a.video)
    marka = json.load(open(os.path.join(KOK, "brands", a.marka + ".json")))
    ad = a.ad or "%s-%s" % (a.marka, slug(os.path.splitext(os.path.basename(video))[0]))
    proje = os.path.join(KOK, "projects", ad)
    edit = os.path.join(proje, "edit")
    os.makedirs(edit, exist_ok=True)
    os.makedirs(os.path.join(proje, "out"), exist_ok=True)
    meta = {"video": video, "marka": a.marka, "ad": ad, "dil": a.dil}
    json.dump(meta, open(os.path.join(proje, "proje.json"), "w"), ensure_ascii=False, indent=1)

    pr = probe(video)
    json.dump(pr, open(os.path.join(edit, "probe.json"), "w"), indent=1)
    sure = float(pr["format"]["duration"])
    print("kayit: %.0f dk, %s" % (sure / 60, [(s["codec_type"], s.get("width"), s.get("height")) for s in pr["streams"]]))

    wav = os.path.join(edit, "ses.wav")
    if not os.path.exists(wav):
        subprocess.run([FFMPEG, "-nostdin", "-v", "error", "-i", video, "-vn", "-ac", "1", "-ar", "16000",
                        "-y", wav], check=True)

    sj = os.path.join(edit, "sessizlik.json")
    if not os.path.exists(sj):
        bos = harita(wav)
        json.dump({"bosluk": bos}, open(sj, "w"), indent=1)
    bos = json.load(open(sj))["bosluk"]
    print("sessizlik: %d boşluk" % len(bos))

    kj = os.path.join(edit, "kelimeler.json")
    mevcut = json.load(open(kj)) if os.path.exists(kj) else {"parca": {}}
    for b, e in parca_sinirlari(sure, bos):
        k = "%.2f" % b
        if k in mevcut["parca"]:
            continue
        sys.stderr.write("... %d:%02d-%d:%02d çözülüyor\n" % (b // 60, b % 60, e // 60, e % 60))
        mevcut["parca"][k] = coz(wav, b, e, a.dil, marka.get("sozluk", ""))
        json.dump(mevcut, open(kj, "w"), ensure_ascii=False)  # parça parça kaydet (devam edilebilir)
    tum = [c for k in sorted(mevcut["parca"], key=float) for c in mevcut["parca"][k]]
    mevcut["cumle"] = tum
    json.dump(mevcut, open(kj, "w"), ensure_ascii=False)
    print("transkript: %d cümle, %d kelime -> %s" % (len(tum), sum(len(c["kelime"]) for c in tum), kj))
    print("PROJE", proje)


if __name__ == "__main__":
    main()

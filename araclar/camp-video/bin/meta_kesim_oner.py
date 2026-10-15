#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Teslim taramasindaki META repliklerini ham zamana cevirip kesim onerir.

Kullanıcı (23.09.2026): kitap/slayt hatasi ara sozleri videoda kalmamali.
Her oneri icin DIKIS kurulup okunur; karar insana birakilir.
"""
import json, os, re, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hat import ince_bosluklar
from dikis_dinle import dikis

KOK = os.path.expanduser("~/camp-video")
TAR = os.path.join(KOK, "takip", "teslim_tarama")


def proje_bul(ad):
    no = ad.split(" - ")[0]
    for d in os.listdir(os.path.join(KOK, "projects")):
        if d.startswith("campverse-ch%s-" % no):
            return d
    return None


def e2h(edl, x):
    t = 0.0
    for r in edl["ranges"]:
        d = float(r["end"]) - float(r["start"])
        if t <= x < t + d:
            return float(r["start"]) + (x - t)
        t += d
    return None


def ince_coz(video, a, sure):
    with tempfile.TemporaryDirectory() as td:
        w = os.path.join(td, "a.wav")
        subprocess.run([os.path.expanduser("~/.local/bin/ffmpeg"), "-v", "error",
                        "-ss", "%.2f" % a, "-t", "%.2f" % sure, "-i", video,
                        "-ac", "1", "-ar", "16000", "-y", w], check=False)
        q = subprocess.run([os.path.expanduser("~/.local/bin/mlx_whisper"), w,
                            "--model", "mlx-community/whisper-large-v3-turbo",
                            "--language", "tr", "--output-dir", td,
                            "--output-format", "json", "--verbose", "False"],
                           capture_output=True, text=True)
        jy = os.path.join(td, "a.json")
        if q.returncode != 0 or not os.path.exists(jy):
            return []
        return [{"bas": x["start"] + a, "bit": x["end"] + a, "metin": x["text"].strip()}
                for x in json.load(open(jy)).get("segments", [])]


def sinir(v, t, yon):
    b = [x for x in ince_bosluklar(v, t, yaricap=2.0) if x["sure"] >= 0.10]
    if not b:
        return round(t, 2)
    yonlu = [x for x in b if (x["bit"] <= t + 0.35) if yon == "bas"] or \
            [x for x in b if (x["bas"] >= t - 0.35)] if yon == "bit" else \
            [x for x in b if x["bit"] <= t + 0.35]
    ad = yonlu or b
    k = min(ad, key=lambda x: min(abs(x["bas"] - t), abs(x["bit"] - t)))
    return round((k["bas"] + k["bit"]) / 2.0, 2)


def main():
    hedef = sys.argv[1] if len(sys.argv) > 1 else None
    out = []
    for f in sorted(os.listdir(TAR)):
        if not f.endswith(".json"):
            continue
        d = json.load(open(os.path.join(TAR, f)))
        if not isinstance(d.get("segment"), list):
            continue
        metalar = [b for b in d.get("bulgu", []) if b["tur"] == "meta"]
        if not metalar:
            continue
        proje = proje_bul(d["ders"])
        if hedef and proje != hedef:
            continue
        if not proje:
            continue
        ey = os.path.join(KOK, "projects", proje, "edit", "edl.json")
        v = os.path.join(KOK, "projects", proje, "ders.mp4")
        if not (os.path.exists(ey) and os.path.exists(v)):
            continue
        edl = json.load(open(ey))
        for m in metalar:
            hb, hs = e2h(edl, m["bas"]), e2h(edl, m["bit"])
            if hb is None or hs is None:
                continue
            # Teslim segmentinin sinirlari kaba: replik cogu zaman tasiyor.
            # Ham videodan dar pencere cozup CUMLENIN kendi sinirlarini bul.
            seg2 = ince_coz(v, max(0, hb - 10), min(26.0, (hs - hb) + 20))
            anah = [w for w in re.findall(r"\w+", m["metin"].lower()) if len(w) > 4][:4]
            vurus = [x for x in seg2
                     if sum(1 for w in anah if w in x["metin"].lower()) >= max(1, len(anah) // 2)]
            if vurus:
                hb, hs = vurus[0]["bas"], vurus[-1]["bit"]
            a, b = sinir(v, hb, "bas"), sinir(v, hs, "bit")
            if b - a < 0.4:
                continue
            metin = dikis(v, max(0, a - 8), a, b, sonra=6.0)
            out.append({"proje": proje, "ders": d["ders"], "bas": a, "bit": b,
                        "replik": m["metin"][:90], "dikis": metin})
            print("== %-40s %8.2f-%8.2f  (%.1f sn)\n   replik: %s\n   dikis : %s\n"
                  % (proje.replace("campverse-", "")[:40], a, b, b - a,
                     m["metin"][:88], metin))
    json.dump(out, open(os.path.join(KOK, "takip", "meta_oneri.json"), "w"),
              ensure_ascii=False, indent=1)
    print("%d oneri -> takip/meta_oneri.json" % len(out))


if __name__ == "__main__":
    main()

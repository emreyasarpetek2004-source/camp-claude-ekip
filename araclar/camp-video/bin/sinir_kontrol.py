#!/usr/bin/env python3
"""Basimdan ONCE tum EDL ic sinirlarini G7 olcutuyle denetler (05.10.2026).
Kaba harita (-35 dB/0,3 sn, +-0,15) VEYA ince bosluk (-30 dB/0,05 sn, +-0,05) VEYA
20 ms enerji <= -35 dB. Kalan sinirlari listeler."""
import glob, json, math, os, re, struct, subprocess, sys
FF = os.path.expanduser("~/.local/bin/ffmpeg")
def db(ham, t):
    a = max(0.0, t - 0.25)
    q = subprocess.run([FF, "-nostats", "-v", "error", "-ss", "%.3f" % a, "-t", "0.5", "-i", ham,
                        "-vn", "-ac", "1", "-ar", "16000", "-f", "s16le", "-"], capture_output=True)
    n = len(q.stdout) // 2
    x = struct.unpack("<%dh" % n, q.stdout[:n * 2])
    v = []
    for i in range(0, n - 160, 80):
        c = a + (i + 80) / 16000
        if abs(c - t) <= 0.015:
            v.append(20 * math.log10(max(1e-9, math.sqrt(sum(y * y for y in x[i:i + 160]) / 160) / 32768)))
    return min(v) if v else 0.0
def ince(ham, t):
    a0 = max(0.0, t - 0.6)
    q = subprocess.run([FF, "-nostats", "-v", "info", "-ss", "%.3f" % a0, "-t", "1.2", "-i", ham, "-af",
                        "silencedetect=noise=-30dB:d=0.05", "-f", "null", "-"], capture_output=True, text=True)
    ss = [float(x) + a0 for x in re.findall(r"silence_start:\s*(-?[\d.]+)", q.stderr)]
    se = [float(x) + a0 for x in re.findall(r"silence_end:\s*([\d.]+)", q.stderr)]
    return any(x0 - 0.05 <= t <= x1 + 0.05 for x0, x1 in zip(ss, se))
hedef = sys.argv[1:] or sorted(glob.glob(os.path.expanduser("~/camp-video/projects/*")))
for p in hedef:
    e = os.path.join(p, "edit")
    try:
        edl = json.load(open(e + "/edl.json")); bos = json.load(open(e + "/sessizlik.json"))["bosluk"]
    except Exception:
        continue
    ham = os.path.join(p, "ders.mp4")
    d = [r for r in edl["ranges"] if r["source"] == "DERS"]
    kotu = []
    onay = json.load(open(e + "/g7_onay.json")) if os.path.exists(e + "/g7_onay.json") else []
    for i in range(len(d) - 1):
        for t in (d[i]["end"], d[i + 1]["start"]):
            if any(b["bas"] - 0.15 <= t <= b["bit"] + 0.15 for b in bos): continue
            if any(abs(t - float(o["t"])) <= 0.03 for o in onay): continue
            if ince(ham, t): continue
            v = db(ham, t)
            if v > -32: kotu.append((round(t, 2), round(v, 1)))
    if kotu: print(os.path.basename(p)[10:45], kotu, flush=True)

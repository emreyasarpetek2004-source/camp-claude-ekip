#!/usr/bin/env python3
"""yeniden_tarama.json'daki asr_bozuk araliklarini dar pencerede yeniden cozer.

Tam transkriptte dongu/uydurma/bos cikan ama sessizlik haritasinda konusma olan
araliklar (5 Ekim 2026 yeniden taramasi) her biri ayri, kosullama kapali ve
konu ipucuyla cozulur. Cikti: edit/asr_bozuk_cozum.json. Var olan atlanir.
"""
import glob, json, os, subprocess, sys, tempfile
KOK = os.path.expanduser("~/camp-video")
FF = os.path.expanduser("~/.local/bin/ffmpeg")
MLX = os.path.expanduser("~/.local/bin/mlx_whisper")
for f in sorted(glob.glob(KOK + "/projects/*/edit/yeniden_tarama.json")):
    edit = os.path.dirname(f); out = edit + "/asr_bozuk_cozum.json"
    try: r = json.load(open(f))
    except Exception: continue
    ar = r.get("asr_bozuk") or []
    onceki = json.load(open(out)) if os.path.exists(out) else []
    ar = [a for a in ar if not any(abs(a["bas"] - o["bas"]) < 0.5 and abs(a["bit"] - o["bit"]) < 0.5 for o in onceki)]
    if not ar: continue
    ham = os.path.join(os.path.dirname(edit), "ders.mp4")
    if not os.path.exists(ham): print("ham yok", edit); continue
    sonuc = list(onceki)
    with tempfile.TemporaryDirectory() as td:
        for a in ar:
            b0, b1 = max(0, a["bas"] - 1.5), a["bit"] + 1.5
            if b1 - b0 > 60:   # uzun araliklar 60 sn'lik dilimlerle (dongu riskini azaltir)
                parca = []
                t = b0
                while t < b1:
                    parca.append((t, min(b1, t + 60))); t += 60
            else:
                parca = [(b0, b1)]
            satir = []
            for c0, c1 in parca:
                subprocess.run([FF, "-nostats", "-v", "error", "-y", "-ss", str(c0), "-t", str(c1 - c0),
                                "-i", ham, "-vn", "-ac", "1", "-ar", "16000", td + "/c.wav"])
                q = subprocess.run([MLX, td + "/c.wav", "--language", "tr", "--model", "mlx-community/whisper-large-v3-turbo",
                                    "--condition-on-previous-text", "False", "--output-dir", td,
                                    "--output-format", "json", "--verbose", "False",
                                    "--initial-prompt", "Tıp dersi, AMC sınavı."], capture_output=True, text=True)
                sg = json.load(open(td + "/c.json")).get("segments", []) if q.returncode == 0 else []
                satir += [[round(c0 + x["start"], 1), round(c0 + x["end"], 1), x["text"].strip()] for x in sg]
            sonuc.append({"bas": a["bas"], "bit": a["bit"], "satirlar": satir})
            continue
            w = td + "/p.wav"
            subprocess.run([FF, "-nostats", "-v", "error", "-y", "-ss", str(b0), "-t", str(b1 - b0),
                            "-i", ham, "-vn", "-ac", "1", "-ar", "16000", w])
            q = subprocess.run([MLX, w, "--language", "tr", "--model", "mlx-community/whisper-large-v3-turbo",
                                "--condition-on-previous-text", "False", "--output-dir", td,
                                "--output-format", "json", "--verbose", "False",
                                "--initial-prompt", "Tıp dersi, AMC sınavı."], capture_output=True, text=True)
            seg = json.load(open(td + "/p.json")).get("segments", []) if q.returncode == 0 else []
            sonuc.append({"bas": a["bas"], "bit": a["bit"],
                          "satirlar": [[round(b0 + s["start"], 1), round(b0 + s["end"], 1), s["text"].strip()] for s in seg]})
    json.dump(sonuc, open(out, "w"), ensure_ascii=False, indent=1)
    print("ok", os.path.basename(os.path.dirname(edit)), len(sonuc))

#!/usr/bin/env python3
"""Her kesimin cevresini HAM kayittan dar pencerede, kelime zamanli yeniden cozer.

Neden: tam transkriptin zaman damgalari uzun derslerde birkac saniye kayiyor
(5 Ekim 2026 yeniden taramasi: CH61'de dogru doz kesilip yanlis doz kalmis,
CH70'te talimat kesimi temiz cumlenin basini goturmus). Sinir karari kelime
zamanina dayanmali; bu arac her kesim icin

    once:  kesimden onceki son kelimeler   (zamanli)
    ic:    kesilen kelimeler               (zamanli)
    sonra: kesimden sonraki ilk kelimeler  (zamanli)

uretir. Adaylar: mevcut EDL bosluklari + yeniden_tarama.json ek_kesimler/geri_al.
Tum pencereler tek ses dosyasinda birlestirilip TEK mlx_whisper gecisinde cozulur
(model her pencerede yeniden yuklenmesin diye, bkz. denetle.py G14).

Kullanim: bin/kesim_metni.py projects/<proje> [--pay 8]
Cikti:    edit/kesim_metni.json
"""
import argparse, json, os, subprocess, sys, tempfile

FF = os.path.expanduser("~/.local/bin/ffmpeg")
MLX = os.path.expanduser("~/.local/bin/mlx_whisper")


def adaylar(edit):
    edl = json.load(open(os.path.join(edit, "edl.json")))
    d = [r for r in edl["ranges"] if r["source"] == "DERS"]
    out = []
    for i in range(len(d) - 1):
        out.append({"kaynak": "mevcut", "bas": d[i]["end"], "bit": d[i + 1]["start"]})
    yt = os.path.join(edit, "yeniden_tarama.json")
    if os.path.exists(yt):
        r = json.load(open(yt))
        for k in r.get("ek_kesimler", []):
            out.append({"kaynak": "ek", "bas": k["bas"], "bit": k["bit"], "gerekce": k.get("gerekce", "")})
        for k in r.get("geri_al", []):
            out.append({"kaynak": "geri_al", "bas": k["bas"], "bit": k["bit"], "gerekce": k.get("gerekce", "")})
    return sorted(out, key=lambda x: x["bas"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("proje")
    ap.add_argument("--pay", type=float, default=8.0)
    ap.add_argument("--son", action="store_true", help="yalniz EDL'deki NIHAI kesimler -> kesim_metni_son.json")
    a = ap.parse_args()
    edit = os.path.join(a.proje, "edit")
    ham = os.path.join(a.proje, "ders.mp4")
    ad = adaylar(edit)
    if a.son:
        ad = [k for k in ad if k["kaynak"] == "mevcut"]
    if not ad:
        json.dump([], open(os.path.join(edit, "kesim_metni_son.json" if a.son else "kesim_metni.json"), "w")); return
    ARA = 1.0
    with tempfile.TemporaryDirectory() as td:
        sessiz = os.path.join(td, "s.wav")
        subprocess.run([FF, "-v", "error", "-f", "lavfi", "-i", "anullsrc=r=16000:cl=mono",
                        "-t", str(ARA), "-y", sessiz], check=False)
        parca, yer, imlec = [], [], 0.0
        for i, k in enumerate(ad):
            b0 = max(0.0, k["bas"] - a.pay); b1 = k["bit"] + a.pay
            w = os.path.join(td, "p%03d.wav" % i)
            subprocess.run([FF, "-nostats", "-v", "error", "-y", "-ss", "%.3f" % b0, "-t", "%.3f" % (b1 - b0),
                            "-i", ham, "-vn", "-ac", "1", "-ar", "16000", w], check=False)
            parca += [w, sessiz]; yer.append((imlec, imlec + (b1 - b0), b0)); imlec += (b1 - b0) + ARA
        liste = os.path.join(td, "l.txt")
        open(liste, "w").write("".join("file '%s'\n" % w for w in parca))
        hep = os.path.join(td, "hep.wav")
        subprocess.run([FF, "-v", "error", "-f", "concat", "-safe", "0", "-i", liste, "-c", "copy", "-y", hep])
        q = subprocess.run([MLX, hep, "--model", "mlx-community/whisper-large-v3-turbo", "--language", "tr",
                            "--word-timestamps", "True", "--condition-on-previous-text", "False",
                            "--output-dir", td, "--output-format", "json", "--verbose", "False"],
                           capture_output=True, text=True)
        if q.returncode != 0:
            sys.exit("ASR calismadi: " + q.stderr[-300:])
        kel = [w for s in json.load(open(os.path.join(td, "hep.json")))["segments"] for w in s.get("words", [])]
    sonuc = []
    for k, (p0, p1, b0) in zip(ad, yer):
        ws = [(round(w["start"] - p0 + b0, 2), round(w["end"] - p0 + b0, 2), w["word"].strip())
              for w in kel if p0 <= (w["start"] + w["end"]) / 2 < p1]
        mid = lambda w: (w[0] + w[1]) / 2
        k2 = dict(k)
        k2["once"] = [w for w in ws if mid(w) < k["bas"]][-14:]
        k2["ic"] = [w for w in ws if k["bas"] <= mid(w) <= k["bit"]]
        k2["sonra"] = [w for w in ws if mid(w) > k["bit"]][:14]
        sonuc.append(k2)
    json.dump(sonuc, open(os.path.join(edit, "kesim_metni_son.json" if a.son else "kesim_metni.json"), "w"),
              ensure_ascii=False, indent=1)
    print("%s: %d kesim" % (os.path.basename(a.proje), len(sonuc)))


if __name__ == "__main__":
    main()

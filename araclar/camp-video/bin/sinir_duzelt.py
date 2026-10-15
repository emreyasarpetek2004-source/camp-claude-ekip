#!/usr/bin/env python3
"""sinir_kontrol.log'daki kalan sinirlari en yakin enerji cukuruna (<= -35 dB, 10 ms)
tasir; kesim_nihai.json'u gunceller. Cukur bulunamazsa listeler (05.10.2026)."""
import glob, json, math, os, re, struct, subprocess
FF = os.path.expanduser("~/.local/bin/ffmpeg")
KOK = os.path.expanduser("~/camp-video")
def rms(ham, a, b):
    q = subprocess.run([FF, "-nostats", "-v", "error", "-ss", "%.3f" % a, "-t", "%.3f" % (b - a), "-i", ham,
                        "-vn", "-ac", "1", "-ar", "16000", "-f", "s16le", "-"], capture_output=True)
    n = len(q.stdout) // 2; x = struct.unpack("<%dh" % n, q.stdout[:n * 2]); out = []
    for i in range(0, n - 160, 80):   # 10 ms pencere, 5 ms adim
        w = x[i:i + 160]; r = math.sqrt(sum(v * v for v in w) / len(w)) or 1
        out.append((a + (i + 80) / 16000, 20 * math.log10(r / 32768)))
    return out
satirlar = [l for l in open(KOK + "/takip/sinir_kontrol.log") if l.startswith("ch")]
bulunamayan = []
for l in satirlar:
    ad, liste = l.split(" ", 1); noktalar = eval(liste)
    p = [x for x in glob.glob(KOK + "/projects/campverse-*") if os.path.basename(x)[10:45] == ad.strip()][0]
    nf = p + "/edit/kesim_nihai.json"; n = json.load(open(nf)); ham = p + "/ders.mp4"; degisti = False
    for t, _ in noktalar:
        en = rms(ham, t - 0.25, t + 0.25)
        # en az 15 ms suren cukur: 3 ardisik 10 ms pencere (5 ms adim) esigin altinda
        aday = [(en[i][0], en[i][1]) for i in range(1, len(en) - 1)
                if en[i - 1][1] <= -32 and en[i][1] <= -32 and en[i + 1][1] <= -32]
        if not aday:
            bulunamayan.append((ad, t, round(min(v for _, v in en), 1))); continue
        # Yon: kalan sesi KORUYAN tarafa. Kesimin basi (bas) ancak ILERI, sonu (bit) ancak
        # GERI kayabilir; ters yonde en yakin cukur kelime icindeki p/t/k kapanmasi olabilir
        # ve kalan kelimenin ilk hecesini yer (05.10.2026 dikis denetimi: 'Hi-lal', 'Flu-mazenil').
        for k in n["kesimler"]:
            for alan in ("bas", "bit"):
                if abs(k[alan] - t) <= 0.45:
                    yon = [z for z in aday if (z[0] >= t - 0.01 if alan == "bas" else z[0] <= t + 0.01)]
                    if not yon:
                        bulunamayan.append((ad, t, alan)); continue
                    k[alan] = round(min(yon, key=lambda z: abs(z[0] - t))[0], 3); degisti = True
        print(ad, t, "duzeltildi")
    if degisti:
        json.dump(n, open(nf, "w"), ensure_ascii=False, indent=1)
print("BULUNAMAYAN:", bulunamayan)

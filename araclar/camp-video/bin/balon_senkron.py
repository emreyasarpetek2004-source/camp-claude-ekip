#!/usr/bin/env python3
"""Ciktidaki hoca balonu ham kayitla SENKRON mu, DONMA var mi? (05.10.2026)

Kullanıcı: "hocanin videosunda donma, takilma ya da kaymalar olmasin, asiri dikkat et balona".

Yontem: ciktida N an secilir; her an EDL ile ham kayittaki ana eslenir. Ciktidaki balon
dairesi (balon_plan.json) ile ham kayittaki balon (ayni boyuta olceklenmis) karsilastirilir.
  - KAYMA: ham tarafta -0,3..+0,3 sn (1/24 adim) kaydirilip en iyi esleme aranir; en iyi
    kaydirma 0'dan >1 kare ise kayma var.
  - DONMA: ciktida ayni ana 0,5 sn arayla iki kare; balon hic degismiyorsa (ham kayitta
    degisiyorken) donma var.
Kullanim: bin/balon_senkron.py <edl.json> <final.mp4> [--n 24]
"""
import argparse, json, os, subprocess, sys
import numpy as np

FF = os.path.expanduser("~/.local/bin/ffmpeg")


def kare(video, t, crop, boy):
    q = subprocess.run([FF, "-nostats", "-v", "error", "-ss", "%.3f" % t, "-i", video, "-frames:v", "1",
                        "-vf", "crop=%s,scale=%d:%d,format=gray" % (crop, boy, boy), "-f", "rawvideo", "-"],
                       capture_output=True)
    a = np.frombuffer(q.stdout, np.uint8)
    return a[:boy * boy].reshape(boy, boy).astype(float) if a.size >= boy * boy else None


def benzer(a, b, m):
    a = a[m]; b = b[m]; a = a - a.mean(); b = b - b.mean()
    return float((a * b).sum() / (np.sqrt((a * a).sum() * (b * b).sum()) + 1e-9))


def dizi(video, t, sure, crop, boy):
    q = subprocess.run([FF, "-nostats", "-v", "error", "-ss", "%.3f" % t, "-t", "%.3f" % sure, "-i", video,
                        "-vf", "fps=24,crop=%s,scale=%d:%d,format=gray" % (crop, boy, boy), "-an",
                        "-f", "rawvideo", "-"], capture_output=True)
    a = np.frombuffer(q.stdout, np.uint8); n = a.size // (boy * boy)
    return a[:n * boy * boy].reshape(n, boy, boy).astype(float)


def ses(video, t, sure):
    q = subprocess.run([FF, "-nostats", "-v", "error", "-ss", "%.3f" % max(0.0, t), "-t", "%.3f" % sure, "-i", video,
                        "-vn", "-ac", "1", "-ar", "8000", "-f", "s16le", "-"], capture_output=True)
    return np.frombuffer(q.stdout, np.int16).astype(float)


def ses_ofset(video, t, ham, s0, ara=1.5):
    """Ciktinin t anindaki 3 sn sesi hamda s0 +-ara icinde nerede? (sn, 1 ms cozunurluk)"""
    A = ses(video, t, 3.0); H = ses(ham, s0 - ara, 3.0 + 2 * ara)
    if len(A) < 8000 or len(H) < len(A) + 16 or A.std() < 1:
        return 0.0
    A = A - A.mean(); H = H - H.mean()
    n = len(H) - len(A) + 1
    c = np.correlate(H, A, mode="valid")[:n]
    return (int(np.argmax(c)) / 8000.0) - ara


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("edl"); ap.add_argument("video")
    ap.add_argument("--n", type=int, default=24); ap.add_argument("--ayrinti", action="store_true"); a = ap.parse_args()
    edl = json.load(open(a.edl)); kok = os.path.dirname(os.path.abspath(a.edl))
    plan = json.load(open(os.path.join(kok, "balon_plan.json")))
    ham = edl["sources"]["DERS"]; ham = ham if os.path.isabs(ham) else os.path.join(kok, ham)
    bx, by, br = plan["balon_kaynak"]; br -= 3
    # olustur.py ile ayni: kirpim kadraj icinde kalsin (CH02 balon tepesi kadraj disinda)
    q = subprocess.run([os.path.expanduser("~/.local/bin/ffprobe"), "-v", "error", "-select_streams", "v:0",
                        "-show_entries", "stream=width,height", "-of", "csv=p=0", ham], capture_output=True, text=True)
    gw, gh = [int(v) for v in q.stdout.strip().split(",")[:2]]
    br = min(br, bx, by, gw - bx, gh - by)
    B = 96
    crop_ham = "%d:%d:%d:%d" % (2 * br, 2 * br, bx - br, by - br)
    crop_out = "%d:%d:%d:%d" % (plan["cap"], plan["cap"], plan["x"], plan["y"])
    yy, xx = np.ogrid[0:B, 0:B]; m = ((xx - B / 2) ** 2 + (yy - B / 2) ** 2) <= (B / 2 - 4) ** 2
    # cikti -> ham eslemesi
    seg, t0 = [], 0.0
    for r in edl["ranges"]:
        d = float(r["end"]) - float(r["start"])
        if r["source"] == "DERS": seg.append((t0, t0 + d, float(r["start"])))
        t0 += d
    toplam = t0
    anlar = [toplam * (i + 0.5) / a.n for i in range(a.n)]
    def olc(t):
        s0 = next(((t - o0) + h0 for o0, o1, h0 in seg if o0 + 1.2 <= t <= o1 - 2.6), None)
        if s0 is None: return None
        # Parcalar kare sinirina yuvarlandigi icin cikti zaman cizelgesi EDL'e gore
        # birkac yuz ms esner (CH02: 70 dk'da 0,9 sn); ses ve goruntu birlikte kayar.
        # Ham karsiligi SESLE bulunur, balon ona gore kiyaslanir: olculen dudak senkronu.
        s0 += ses_ofset(a.video, t, ham, s0)
        if any(x0 - 2 <= s0 <= x1 + 2 for x0, x1 in plan.get("balonsuz") or []):
            return None                                   # hoca balonu tasimis, yerlesim yok
        O = dizi(a.video, t, 2.0, crop_out, B)            # cikti: 48 kare
        H = dizi(ham, s0 - 0.5, 3.0, crop_ham, B)         # ham: 72 kare, 12 kare once baslar
        if len(O) < 40 or len(H) < 60: return None
        hareket = float(np.abs(np.diff(H, axis=0))[:, m].mean())
        # Ham kamera akisinin kendi donmasi: ardisik >=7 karede (~290 ms) degisim yok -> kayma olculemez
        dh = np.abs(np.diff(H, axis=0))[:, m].mean(axis=1) < 0.3
        uzun, kos = 0, 0
        for v in dh:
            kos = kos + 1 if v else 0; uzun = max(uzun, kos)
        ham_donuk = uzun >= 7          # Loom kamerasi ~14 fps: 3-4 karelik tekrar normal
        puan = []
        for k in range(-10, 11):
            j0 = 12 + k
            if j0 < 0 or j0 + len(O) > len(H): puan.append(-2); continue
            puan.append(np.mean([benzer(O[x], H[j0 + x], m) for x in range(0, len(O), 2)]))
        k_en = int(np.argmax(puan)) - 10; en = max(puan)
        cdon = float(np.abs(np.diff(O, axis=0))[:, m].mean())
        donma = hareket > 0.6 and cdon < 0.25 * hareket
        # Ham Loom kaydinin kamera akisi kendisi takiliyor (CH02 1210 sn: 7 karelik donmalar);
        # o pencerede her kaydirma neredeyse esit eslesir, en iyisi rastgele cikar. Kayma
        # ancak sifir kaydirmadan BELIRGIN iyiyse sayilir.
        # Durgun sahnede (hareket <1,2) ya da en iyi kaydirma arama sinirina (+-10) dusunce
        # eslesme egrisi duzdur, tepe yoktur (CH06 1407 sn: hareket 0,65, +10): olculemez.
        kayma = (abs(k_en) > 1 and abs(k_en) < 10 and hareket > 1.2 and puan[10] < en - 0.005
                 and not ham_donuk)
        return dict(t=t, s0=s0, en=en, k=k_en, cdon=cdon, hareket=hareket, uzun=uzun, donma=donma, kayma=kayma)

    kotu, sonuc = [], []
    for t in anlar:
        r = olc(t)
        if r is None: continue
        if r["kayma"]:
            # Dogrulama (6 Eki 2026, CH06): tek olcum dusuk benzerlikte birkac saniyede
            # -150..+250 ms ziplayabiliyor; gercek uretim kaymasi bir parca icinde sabittir.
            # 3 sn once ve sonra da ayni yonde >1 kare degilse kayma sayilmaz.
            # 6 Eki: CH10'da ayni aralikta 3 olcum ayni yonde ama -250..-50 ms dagiliyordu.
            # Gercek kayma SABITTIR: 5 olcumun hepsi ayni yonde, >1 kare ve dagilim <=2 kare olmali.
            kom = [r] + [olc(t + d) for d in (-6.0, -3.0, 3.0, 6.0)]
            ks = [x["k"] for x in kom if x is not None]
            if not (len(ks) == 5 and all(abs(k) > 1 and (k > 0) == (r["k"] > 0) for k in ks)
                    and max(ks) - min(ks) <= 2):
                r["kayma"] = False
        sonuc.append((round(t, 1), round(r["s0"], 1), round(r["en"], 3), r["k"], round(r["cdon"], 2),
                      round(r["hareket"], 2), r["uzun"]))
        # benzerlik tabani 0,75 (6 Eki): bazi derslerde isik/sikistirma ile saglam balon 0,83-0,85; bozuk balon <0,5
        if r["donma"] or r["kayma"] or r["en"] < 0.75:
            kotu.append((round(t, 1), "kayma %+d kare" % r["k"] if r["kayma"] else "", "DONMA" if r["donma"] else "",
                         "benzerlik %.2f" % r["en"] if r["en"] < 0.75 else ""))
    print("balon senkron: %d an olculdu, sorunlu %d" % (len(sonuc), len(kotu)))
    if "--ayrinti" in sys.argv:
        for x in sonuc: print("   t=%s ham=%s benzerlik=%s kaydirma=%+d cikti_hareket=%s ham_hareket=%s ham_en_uzun_donma=%s" % x)
    for x in kotu: print("   ", x)
    sys.exit(1 if kotu else 0)


if __name__ == "__main__":
    main()

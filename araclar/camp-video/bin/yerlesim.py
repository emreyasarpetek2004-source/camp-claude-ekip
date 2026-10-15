#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Loom ders kaydının yerleşimini ölçer: slayt kartı ve hocanın kamera balonu.

Neden: Loom kaydı kartı koyu bir tarayıcı zemininin ortasına koyuyor ve kamera balonunu
kartın DIŞINA, sağ üste taşırıyor. Karta tam oturmak bandı kaldırır ama balonun tepesini
keser. Bu yüzden balon ayrı çıkarılıp daire maskesiyle kartın İÇİNE yerleştirilir.

(21.09.2026 kararı: "Hocanın kafasını komple slayt içine taşı ve asla gri bant koyma")

Ölçüm her kayıt için ayrı yapılır: pencere geometrisi kayıttan kayda değişiyor.
"""
import io
import os
import subprocess

FFMPEG = os.path.expanduser("~/.local/bin/ffmpeg")
FFPROBE = os.path.expanduser("~/.local/bin/ffprobe")


def _kare(video, t):
    import numpy as np
    from PIL import Image
    p = subprocess.run([FFMPEG, "-nostats", "-v", "error", "-ss", str(t), "-i", video,
                        "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"],
                       capture_output=True)
    return np.asarray(Image.open(io.BytesIO(p.stdout)).convert("L"))


def _sure(video):
    return float(subprocess.run([FFPROBE, "-v", "error", "-show_entries", "format=duration",
                                 "-of", "csv=p=0", video],
                                capture_output=True, text=True).stdout.strip())


def kart_kutusu(video, ornek=None):
    """Slayt kartı: koyu tarayıcı zeminiyle kart arasındaki sınır.

    Eşik 55: kartın beyazı da koyu yeşil başlık bandı da bunun üstünde kalır. Daha yüksek
    eşik (ör. 180) yeşil üst/alt bantları dışarıda bırakıp kartı yanlış ölçüyor.
    """
    import numpy as np
    sure = _sure(video)
    ornek = ornek or [x for x in (300, 600, 900, 1200) if x < sure - 5] or [sure / 2]
    adaylar = []
    for t in ornek:
        g = _kare(video, t)
        h, w = g.shape
        ic = g > 55
        sat = ic[:, int(w * 0.38):int(w * 0.62)].mean(axis=1)
        sut = ic[int(h * 0.35):int(h * 0.80), :].mean(axis=0)
        if not (sat > 0.6).any() or not (sut > 0.6).any():
            continue
        u = int(np.argmax(sat > 0.6)); a = h - 1 - int(np.argmax(sat[::-1] > 0.6))
        s = int(np.argmax(sut > 0.6)); sg = w - 1 - int(np.argmax(sut[::-1] > 0.6))
        adaylar.append((s, u, sg - s + 1, a - u + 1))
    if not adaylar:
        return None
    # En sık ölçülen kutu (kararlı olan) seçilir. Her kenardan 2 px içeri: aksi halde
    # kartın üst kenarındaki koyu tarayıcı zemini çıktının en üstünde ince bir çizgi
    # olarak kalıyordu (05.10.2026).
    x, y, w_, h_ = max(set(adaylar), key=adaylar.count)
    return (x + 2, y + 2, w_ - 4, h_ - 4)


def balon_cemberi(video, kart, ornek=None):
    """Kamera balonu: kartın ÜSTÜNDEKİ koyu şeritte kesit alıp çember uydurur.

    O şeritte karttan hiçbir şey yok, yalnız balon parlak. Kart kenarına değen satırlar
    (kesit aniden genişler) elenir, yoksa uydurma bozulur.
    """
    import numpy as np
    if not kart:
        return None
    kx, ky, kw, kh = kart
    if ky < 8:
        return None
    sure = _sure(video)
    ornek = ornek or [x for x in (300, 600, 900) if x < sure - 5] or [sure / 2]
    P = []
    for t in ornek:
        g = _kare(video, t)
        h, w = g.shape
        for y in range(4, ky - 2):
            # Arama sag tarafta: ortadaki Loom "Page x of y" etiketi de bu seritte parlak
            # ve uydurmayi bozuyordu (CH64, 05.10.2026: r=279 cikti).
            x_bas = int(w * 0.70)
            satir = g[y, x_bas:] > 120
            if satir.sum() < 5:
                continue
            xs = np.nonzero(satir)[0] + x_bas
            if xs.max() - xs.min() + 1 > w * 0.22:    # kart kenarına değdi, at
                continue
            P.append((xs.min(), y)); P.append((xs.max(), y))
    if len(P) < 8:
        return None
    P = np.array(P, dtype=float)
    A = np.c_[2 * P[:, 0], 2 * P[:, 1], np.ones(len(P))]
    b = P[:, 0] ** 2 + P[:, 1] ** 2
    sol, *_ = np.linalg.lstsq(A, b, rcond=None)
    cx, cy = float(sol[0]), float(sol[1])
    r = float(np.sqrt(sol[2] + cx * cx + cy * cy))
    if not (0 < r < min(kw, kh) / 2.0) or not (40 <= r <= 140):
        return None
    # Loom balonu ekran GENISLIGIYLE olceklenir: 1152 px kayitta r=79,2 (70 dersin
    # ortancasi), 1284 px kayitta 88,4 (CH02, gozle olculdu ~89). Kartin ustundeki serit
    # kisaysa (CH25: 5 px) uydurma az noktayla sapiyor (r=73,6). Sapma 1,5 px'i asarsa
    # yaricap sabitlenir, merkez yuksekligi balonun TEPESINDEN hesaplanir.
    r0 = 79.2 * w / 1152.0
    if abs(r - r0) > 1.5:
        ust = float(P[:, 1].min())
        r, cy = r0, ust + r0
    return cx, cy, r


def maske_uret(cap, yol):
    """Kenarı yumuşatılmış daire maskesi (alphamerge için gri tonlu)."""
    from PIL import Image, ImageDraw, ImageFilter
    kat = 4
    b = Image.new("L", (cap * kat, cap * kat), 0)
    ImageDraw.Draw(b).ellipse((0, 0, cap * kat - 1, cap * kat - 1), fill=255)
    b = b.resize((cap, cap), Image.LANCZOS).filter(ImageFilter.GaussianBlur(0.6))
    os.makedirs(os.path.dirname(yol), exist_ok=True)
    b.save(yol)
    return yol


def geometri(video):
    kart = kart_kutusu(video)
    balon = balon_cemberi(video, kart)
    return {"kart": kart, "balon": balon}


if __name__ == "__main__":
    import sys
    g = geometri(sys.argv[1])
    k = g["kart"]
    print("KART : x=%d y=%d %dx%d  oran=%.3f" % (k[0], k[1], k[2], k[3], k[2] / float(k[3])) if k else "KART : bulunamadi")
    b = g["balon"]
    if b:
        print("BALON: merkez=(%.0f, %.0f) yaricap=%.0f  kutu x %.0f..%.0f y %.0f..%.0f"
              % (b[0], b[1], b[2], b[0] - b[2], b[0] + b[2], b[1] - b[2], b[1] + b[2]))
        if k:
            print("       kartin ustunde kalan: %.0f px" % max(0, k[1] - (b[1] - b[2])))
    else:
        print("BALON: bulunamadi")


def _kart_kare(video, kart, t):
    import numpy as np
    from PIL import Image
    kx, ky, kw, kh = kart
    p = subprocess.run([FFMPEG, "-nostats", "-v", "error", "-ss", str(t), "-i", video,
                        "-frames:v", "1", "-vf", "crop=%d:%d:%d:%d" % (kw, kh, kx, ky),
                        "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True)
    return np.asarray(Image.open(io.BytesIO(p.stdout)).convert("L")).astype(int)


def balon_olcek_oner(video, kart, balon, pay_orani=0.015, esik_yuzde=0.05,
                     alt=0.50, ust=0.85, ornek=9):
    """Ders başına en uygun balon boyutu: yazının üstüne BİNMEYEN en büyük daire.

    (21.09.2026 kararı: "hocanın resmini biraz daha küçültelim yazıların üstüne gelip
    onları kapamasın optimal şekilde ayarla her ders için")

    Ölçüm: kart örneklenir, gerçek yazı maskesi çıkarılır (hocanın kendi görüntüsü ve
    dekoratif üst/alt bantlar HARİÇ, yoksa ölçüm şişer), sonra aday boyutlar denenir.
    En kötü karede bile eşiğin altında kalan en büyük boyut seçilir.
    """
    import numpy as np
    if not (kart and balon):
        return ust
    kx, ky, kw, kh = kart
    bx, by, br = balon
    sure = _sure(video)
    anlar = [sure * (i + 1) / (ornek + 1.0) for i in range(ornek)]
    kareler = [_kart_kare(video, kart, t) for t in anlar]
    H, W = kareler[0].shape
    yy, xx = np.ogrid[0:H, 0:W]
    eski = ((xx - (bx - kx)) ** 2 + (yy - (by - ky)) ** 2) <= (br + 6) ** 2
    bant = np.zeros((H, W), bool)
    bant[0:int(H * 0.035), :] = True
    bant[int(H * 0.93):, :] = True
    haric = eski | bant
    masks = []
    for im in kareler:
        m = (np.abs(im - np.median(im)) > 40) & ~haric
        masks.append(m)
    toplam = [max(1, m.sum()) for m in masks]
    pay = int(round(pay_orani * W))
    secim = alt
    for oran in [x / 100.0 for x in range(int(ust * 100), int(alt * 100) - 1, -5)]:
        cap = int(round(2 * br * oran))
        x0, y0 = W - cap - pay, pay
        mrk = ((xx - (x0 + cap / 2.0)) ** 2 + (yy - (y0 + cap / 2.0)) ** 2) <= (cap / 2.0) ** 2
        en_kotu = max(100.0 * (m & mrk).sum() / t for m, t in zip(masks, toplam))
        if en_kotu <= esik_yuzde:
            secim = oran
            break
    return secim

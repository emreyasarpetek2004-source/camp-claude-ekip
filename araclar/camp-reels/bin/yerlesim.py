#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Zoom kaydının yerleşim haritası (OLGU katmanı).

Her ~20 sn'de bir kareyi ölçer ve o anki düzeni etiketler:
  paylasim   : ekran paylaşımı + küçük konuşmacı kutusu  (slayt kutusu + konuşmacı kutusu)
  konusmaci  : yalnız konuşmacı (tam kare)
  slayt      : yalnız paylaşım, kamera yok
Kutular kaynak piksel cinsinden [x0, y0, x1, y1].

Kural: siyah olmayan alanın kapsayıcı kutusu doluysa (tek dikdörtgen) ya konuşmacı ya slayttır;
ayrım hareketle yapılır (konuşmacı 1 sn'de değişir, slayt değişmez).
Dolu değilse L biçimi: konuşmacı kutusu sağ üstte, slayt geri kalanı.

Elle düzeltme: proje.json'a "yerlesim_elle": {"slayt": [...], "konusmaci": [...]} yazılırsa kutular onu kullanır.

Kullanım: python3 bin/yerlesim.py <proje_dizini> [--aralik 20]
Çıktı: edit/yerlesim.json + edit/yerlesim_kontrol.jpg (gözle kontrol için)
"""
import argparse
import json
import os
import subprocess
from collections import Counter

import numpy as np
from PIL import Image, ImageDraw

FFMPEG = os.path.expanduser("~/.local/bin/ffmpeg")
OLCEK_EN = 480  # ölçüm çözünürlüğü


def kare_al(video, t, en, boy, n=2):
    """t ve t+1 sn karelerini (n adet) ölçüm çözünürlüğünde döndürür."""
    h = int(round(boy * OLCEK_EN / en))
    r = subprocess.run([FFMPEG, "-nostdin", "-v", "error", "-ss", "%.2f" % t, "-i", video, "-t", "%.2f" % (n - 0.5),
                        "-vf", "fps=1,scale=%d:%d" % (OLCEK_EN, h), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                       capture_output=True)
    a = np.frombuffer(r.stdout, np.uint8)
    k = a.size // (OLCEK_EN * h * 3)
    return a[: k * OLCEK_EN * h * 3].reshape(k, h, OLCEK_EN, 3).astype(np.int16), h


def bbox(m):
    ys, xs = np.nonzero(m)
    if len(xs) == 0:
        return None
    return [int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1]


def olc(kareler):
    f = kareler[0]
    m = f.max(axis=2) > 22
    B = bbox(m)
    if B is None:
        return {"tip": "bos"}
    x0, y0, x1, y1 = B
    alan = m[y0:y1, x0:x1]
    dolu = alan.mean()
    hareket = float(np.abs(kareler[1] - kareler[0]).mean()) if len(kareler) > 1 else 0.0
    if dolu > 0.95:
        return {"tip": "tek", "kutu": B, "hareket": hareket}
    # L biçimi: sütun doluluğu. Konuşmacı sütunları yalnız üst satırlarda dolu.
    kol = alan.mean(axis=0)
    slayt_kol = np.nonzero(kol > 0.85)[0]
    if len(slayt_kol) == 0:
        return {"tip": "belirsiz", "kutu": B}
    sx1 = x0 + int(slayt_kol.max()) + 1
    # konuşmacı kutusu slaytın sağ üst köşesine biner; satırları o sütunlar olmadan ölç
    sm = m[:, x0:max(x0 + 1, sx1 - int(0.04 * m.shape[1]))]
    sb = bbox(sm)
    sy1 = sb[3]
    sy0 = max(sb[1], sy1 - int(round((sx1 - x0) * 9 / 16)))  # slayt 16:9, alttan hizalı
    slayt = [x0, sy0, sx1, sy1]
    # konuşmacı: slaytın sağındaki sütunlar
    km = m[:, sx1:x1]
    kb = bbox(km)
    if kb is None or (kb[2] - kb[0]) < 20:
        return {"tip": "belirsiz", "kutu": B}
    ky0, ky1 = kb[1], kb[3]
    kh = ky1 - ky0
    kw = int(round(kh * 16 / 9))  # Zoom küçük kutusu 16:9; slayta binen kısmı geri kazan
    kx1 = sx1 + kb[2]
    konusmaci = [max(0, kx1 - kw), ky0, kx1, ky1]
    return {"tip": "paylasim", "slayt": slayt, "konusmaci": konusmaci, "hareket": hareket}


def rafine(m, k, pay=10, esik=0.8, iceri=3):
    """Kutuyu tam çözünürlük maskesinde daralt: satır/sütun doluluğu >= esik olan en geniş aralık, sonra iceri px."""
    H, W = m.shape
    x0, y0, x1, y1 = max(0, k[0] - pay), max(0, k[1] - pay), min(W, k[2] + pay), min(H, k[3] + pay)
    for _ in range(2):
        alan = m[y0:y1, x0:x1]
        kol = np.nonzero(alan.mean(axis=0) >= esik)[0]
        sat = np.nonzero(alan.mean(axis=1) >= esik)[0]
        if len(kol) == 0 or len(sat) == 0:
            return k
        x0, x1 = x0 + int(kol.min()), x0 + int(kol.max()) + 1
        y0, y1 = y0 + int(sat.min()), y0 + int(sat.max()) + 1
    return [x0 + iceri, y0 + iceri, x1 - iceri, y1 - iceri]


def mod_kutu(kutular):
    """Kutuların 4 px'e yuvarlanmış en sık değeri (gürültüye dayanıklı)."""
    if not kutular:
        return None
    c = Counter(tuple(int(round(v / 4.0)) * 4 for v in k) for k in kutular)
    return list(c.most_common(1)[0][0])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("proje")
    ap.add_argument("--aralik", type=float, default=20.0)
    a = ap.parse_args()
    meta = json.load(open(os.path.join(a.proje, "proje.json")))
    pr = json.load(open(os.path.join(a.proje, "edit", "probe.json")))
    v = [s for s in pr["streams"] if s["codec_type"] == "video"][0]
    en, boy = v["width"], v["height"]
    sure = float(pr["format"]["duration"])
    olcek = en / OLCEK_EN

    ornek = []
    t = 5.0
    while t < sure - 3:
        kareler, _ = kare_al(meta["video"], t, en, boy)
        if len(kareler):
            o = olc(kareler)
            o["t"] = round(t, 1)
            ornek.append(o)
        t += a.aralik

    pay = [o for o in ornek if o["tip"] == "paylasim"]
    slayt_kutu = mod_kutu([o["slayt"] for o in pay])
    kons_kutu = mod_kutu([o["konusmaci"] for o in pay])
    # tek dikdörtgen: slayt kutusuyla örtüşüyor ve hareketsizse slayt, değilse konuşmacı
    tek = [o for o in ornek if o["tip"] == "tek"]
    for o in tek:
        ayni = slayt_kutu and all(abs(p - q) <= 12 for p, q in zip(o["kutu"], slayt_kutu))
        o["tip"] = "slayt" if (ayni or o["hareket"] < 0.4) else "konusmaci"
    tam_kutu = mod_kutu([o["kutu"] for o in tek if o["tip"] == "konusmaci"])

    def buyut(k):
        return [int(round(x * olcek)) for x in k] if k else None

    kutu = {"slayt": buyut(slayt_kutu), "konusmaci_kucuk": buyut(kons_kutu), "konusmaci_tam": buyut(tam_kutu)}
    # tam çözünürlükte rafine et: ölçüm 480 px'te yapıldı (±4 px); Zoom yeşil noktası ve kenar çizgisi kutuyu şişiriyor
    for tip, anahtarlar in (("paylasim", ("slayt", "konusmaci_kucuk")), ("konusmaci", ("konusmaci_tam",))):
        aday = [x for x in ornek if x["tip"] == tip]
        if not aday:
            continue
        o = aday[len(aday) // 2] if tip == "paylasim" else max(aday, key=lambda x: x.get("hareket", 0))
        r = subprocess.run([FFMPEG, "-nostdin", "-v", "error", "-ss", str(o["t"]), "-i", meta["video"], "-frames:v", "1",
                            "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True)
        m = np.frombuffer(r.stdout, np.uint8)[: en * boy * 3].reshape(boy, en, 3).max(axis=2) > 22
        for ad in anahtarlar:
            if kutu[ad]:
                kutu[ad] = rafine(m, kutu[ad])
    if kutu["slayt"] and kutu["konusmaci_kucuk"]:
        s, k = kutu["slayt"], kutu["konusmaci_kucuk"]
        if k[0] < s[2] and k[3] > s[1]:  # konuşmacı kutusu slayta biniyor: slaytı onun soluna kırp
            s[2] = k[0] - 4

    elle = meta.get("yerlesim_elle") or {}
    sonuc = {
        "kaynak": [en, boy],
        "kutu": {
            "slayt": elle.get("slayt") or kutu["slayt"],
            "konusmaci_kucuk": elle.get("konusmaci") or kutu["konusmaci_kucuk"],
            "konusmaci_tam": elle.get("konusmaci_tam") or kutu["konusmaci_tam"],
        },
        "ornek": [{"t": o["t"], "tip": o["tip"]} for o in ornek],
    }
    sonuc["dagilim"] = dict(Counter(o["tip"] for o in ornek))
    json.dump(sonuc, open(os.path.join(a.proje, "edit", "yerlesim.json"), "w"), indent=1)
    print("dagilim:", sonuc["dagilim"])
    print("kutular:", sonuc["kutu"])

    # kontrol görseli: her tipten bir kare, kutular çizili
    gorsel = []
    for tip in ("paylasim", "konusmaci", "slayt"):
        aday = [x for x in ornek if x["tip"] == tip]
        if not aday:
            continue
        o = aday[len(aday) // 2] if tip == "paylasim" else max(aday, key=lambda x: x.get("hareket", 0))
        r = subprocess.run([FFMPEG, "-nostdin", "-v", "error", "-ss", str(o["t"]), "-i", meta["video"],
                            "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True)
        import io
        im = Image.open(io.BytesIO(r.stdout)).convert("RGB")
        d = ImageDraw.Draw(im)
        renk = {"slayt": "lime", "konusmaci_kucuk": "red", "konusmaci_tam": "orange"}
        for ad, k in sonuc["kutu"].items():
            if k and ((tip == "paylasim" and ad != "konusmaci_tam") or (tip == "konusmaci" and ad == "konusmaci_tam")
                      or (tip == "slayt" and ad == "slayt")):
                d.rectangle(k, outline=renk[ad], width=6)
        d.text((20, 20), "%s @ %ss" % (tip, o["t"]), fill="yellow")
        gorsel.append(im.resize((960, int(960 * im.height / im.width))))
    if gorsel:
        H = sum(g.height for g in gorsel)
        out = Image.new("RGB", (960, H))
        y = 0
        for g in gorsel:
            out.paste(g, (0, y))
            y += g.height
        out.save(os.path.join(a.proje, "edit", "yerlesim_kontrol.jpg"), quality=85)
        print("kontrol:", os.path.join(a.proje, "edit", "yerlesim_kontrol.jpg"))


if __name__ == "__main__":
    main()

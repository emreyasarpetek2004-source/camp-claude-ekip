#!/usr/bin/env python3
"""Hocanin kamera balonu icin ders basina YERLESIM PLANI (05.10.2026).

Kullanıcı: "hocanin ful goruntusunu minimum yama gerekecek sekilde her derste slayt icine
tasiyalim; tasmasin ya da kesilmesin ama yazilari engellemesin ya da kucuk de olmasin."

Olcutler (cikti 1920x1080 koordinatinda):
  1. Balon TAMAMEN karede, kenarlardan PAY px icerde (tasma/kesilme yok).
  2. Boyut orijinalin en az %85'i (kucuk olmasin).
  3. Yazi: dersin 12 karesinden yazi maskesi; aday dairenin altinda kalan yazi orani
     (karelerin %90'lik dilimi) cezalanir.
  4. Yama: orijinal balonun kart icinde kalan izi (hayalet) yeni dairenin ORTMEDIGI
     kismi kadar yamalanir; o alan cezalanir. Yama dikdortgen degil, tam o piksellerin
     maskesi (yanindaki slayt icerigine dokunulmaz).
Cikti: edit/balon_plan.json + edit/yama_maske.png
Kullanim: bin/balon_plan.py projects/<proje> [--goster]
"""
import json, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import yerlesim

OW, OH = 1920, 1080
PAY = 28                      # kenar payi (px)
OLCEKLER = [1.00, 0.95, 0.90, 0.85]
OLCEK_B, UST_PAY, YAN_PAY = 0.90, 10, 14
K = 2                         # hesap cozunurlugu bolucu (960x540)


def daire(H, W, cx, cy, r):
    yy, xx = np.ogrid[0:H, 0:W]
    return ((xx - cx) ** 2 + (yy - cy) ** 2) <= r * r


def plan(proje, goster=False):
    ham = os.path.join(proje, "ders.mp4"); edit = os.path.join(proje, "edit")
    g = yerlesim.geometri(ham)
    if not (g["kart"] and g["balon"]):
        return None
    kx, ky, kw, kh = g["kart"]; bx, by, br = g["balon"]
    sc = OW / float(kw)
    # hayalet (cikti koordinati), kenar golgesi icin +5 px
    hcx, hcy, hr = (bx - kx) * sc, (by - ky) * sc, br * sc + 5
    W, H = OW // K, OH // K
    hay = daire(H, W, hcx / K, hcy / K, hr / K)
    # yazi maskesi
    sure = yerlesim._sure(ham)
    anlar = [sure * (i + 1) / 13.0 for i in range(12)]
    maskeler = []
    for t in anlar:
        im = yerlesim._kart_kare(ham, g["kart"], t)
        pil = Image.fromarray(im.astype(np.uint8)).resize((W, H), Image.BILINEAR)
        im = np.asarray(pil).astype(int)
        bul = np.asarray(pil.filter(ImageFilter.GaussianBlur(3))).astype(int)
        # Yazi = harf CIZGISI (yerel kontrast); duz renkli bant/cubuk yazi sayilmaz
        m = (np.abs(im - bul) > 28) & ~hay
        m[: int(H * 0.012), :] = False
        maskeler.append(m)
    # Kullanıcı secimi (05.10.2026): B -- %90 boy, alt kenar kayittaki yerinde, tamamen icerde.
    s = OLCEK_B
    R = br * sc * s
    alt = hcy - 5 + br * sc                      # kayittaki alt kenar (cikti koordinati)
    cy = max(UST_PAY + R, alt - R)
    cx = min(max(hcx, YAN_PAY + R), OW - YAN_PAY - R)
    d = daire(H, W, cx / K, cy / K, R / K); alan = d.sum()
    yazi = np.percentile([(m & d).sum() / float(alan) for m in maskeler], 90)
    yama = (hay & ~daire(H, W, cx / K, cy / K, R / K - 1)).sum() / float(alan)
    cap = int(round(2 * R)) // 2 * 2
    x0, y0 = int(round(cx - cap / 2.0)), int(round(cy - cap / 2.0))
    # Hayalet dolgusu (05.10.2026 v2): gerilmis serit yazi cizgisi birakiyordu (CH02 "Rhythm").
    # Simdi tum hayalet diski ffmpeg removelogo ile cevresindeki slayt piksellerinden
    # doldurulur. removelogo karenin ust kenarini kaynak saymaz (tepede pembe ucgen), o yuzden
    # ust UST satir (slaytin kenar bandi, yazisiz) soldaki 16x16 ornegin yatay gerilmesiyle
    # ayrica tamamlanir. Bolge hayaletten 40 px genis: removelogo'ya yeterli baglam.
    UST, KEN = 16, 40
    hrF = br * sc + 8
    yx0 = max(0, int(hcx - hrF) - KEN); yx1 = min(OW, int(hcx + hrF) + KEN)
    yy1 = min(OH, int(hcy + hrF) + KEN)
    # removelogo tam cozunurlukte ders basina saatler suruyor (10 dk'da 12 sn video);
    # dolgu zaten yumusak bir yuzey, hesap 1/4 olcekte yapilir (bolge 8'in kati).
    if yx1 >= OW:      # sag kenara dayaniyorsa yuvarlama SOLDAN: en sag sutunlar yamasiz kalmasin
        yx0 = yx1 - (yx1 - yx0) // 8 * 8
    else:
        yx1 = yx0 + (yx1 - yx0) // 8 * 8
    yy1 = yy1 // 8 * 8
    if yx1 > OW:
        yx0 -= 8; yx1 -= 8
    w, h = yx1 - yx0, yy1
    yyF, xxF = np.ogrid[0:h, yx0:yx1]
    hm = ((xxF - hcx) ** 2 + (yyF - hcy) ** 2) <= hrF * hrF
    ust = hm[:UST].copy(); rl = hm.copy(); rl[:UST] = False
    # Sag kenar (06.10.2026, CH24): bolge kadrajin sag kenarina dayanirsa removelogo orada da
    # kaynak bulamaz (pembe serit). En sag SAG sutun, bolgenin sag alt kosesindeki slayt kenar
    # boslugu orneginin dikey gerilmesiyle ayrica dolar.
    SAG = 16
    sag_var = (hcx + hrF + KEN) > OW and bool(hm[:, -SAG:].any())
    if sag_var:
        sagm = hm[:, -SAG:].copy(); rl[:, -SAG:] = False
        Image.fromarray((sagm * 255).astype(np.uint8)).save(os.path.join(edit, "yama_sag.png"))
    # alfa maskesi (tam boy, 2 px yumusak kenar): dolgu yalniz hayaletin icine konur
    # Hayaletin her pikseli TAM alfa almali: yumusak kenar hayaletin icine duserse balonun
    # acik gri kenari sizip ince bir cizgi/silik daire biraktiriyordu (CH02 testi). Maske 3 px
    # genisletilir, gecis temiz slayt pikselinde olur; ust bant ile 3 satir harmanlanir.
    alm = np.asarray(Image.fromarray((hm * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(7))).copy()
    alm[:UST - 3] = 0
    if sag_var:
        alm[:, -(SAG - 3):] = 0
    al = Image.fromarray(alm).filter(ImageFilter.GaussianBlur(1.0))
    al.save(os.path.join(edit, "yama_maske.png"))
    Image.fromarray((ust * 255).astype(np.uint8)).save(os.path.join(edit, "yama_ust.png"))
    # removelogo maskesi (1/4): blokta tek hayalet pikseli varsa blok maskeli
    kc = rl.reshape(h // 4, 4, w // 4, 4).any(axis=(1, 3))
    Image.fromarray((kc * 255).astype(np.uint8)).save(os.path.join(edit, "yama_kucuk.png"))
    sx = max(0, yx0 - 20)
    yama_plan = {"tip": "removelogo", "x": int(yx0), "y": 0, "w": int(w), "h": int(h), "ust": UST,
                 "sx": int(sx), "sw": 16, "piksel": int(hm.sum()), "sag": SAG if sag_var else 0}
    p = {"kart": [kx, ky, kw, kh], "balon_kaynak": [bx, by, br], "olcek": round(s, 2),
         "cap": cap, "x": x0, "y": y0, "yazi_ortusme_p90": round(float(yazi), 4),
         "yama_orani": round(float(yama), 3), "yama": yama_plan}
    eski = os.path.join(edit, "balon_plan.json")
    if os.path.exists(eski):                       # bin/balon_yok.py olcumu korunur
        try:
            b = json.load(open(eski)).get("balonsuz")
            if b is not None: p["balonsuz"] = b
        except ValueError:
            pass
    json.dump(p, open(os.path.join(edit, "balon_plan.json"), "w"), indent=1)
    if goster:
        t = sure * 0.4
        im = Image.fromarray(yerlesim._kart_kare(ham, g["kart"], t).astype(np.uint8)).resize((OW, OH)).convert("RGB")
        dr = ImageDraw.Draw(im)
        dr.ellipse((hcx - hr, hcy - hr, hcx + hr, hcy + hr), outline=(255, 0, 0), width=3)
        dr.ellipse((x0, y0, x0 + cap, y0 + cap), outline=(0, 160, 0), width=4)
        im.resize((960, 540)).save(os.path.join(edit, "balon_plan.png"))
    return p


if __name__ == "__main__":
    for pr in [x for x in sys.argv[1:] if not x.startswith("--")]:
        r = plan(pr.rstrip("/"), "--goster" in sys.argv)
        print(os.path.basename(pr.rstrip("/"))[10:40], r and {k: r[k] for k in ("olcek", "cap", "x", "y", "yazi_ortusme_p90", "yama_orani")})

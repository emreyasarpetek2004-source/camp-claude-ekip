#!/usr/bin/env python3
"""Dört ülke için dalgalı bayrak görseli üretir (kapak köşesi).

AUSCAMP kataloğundaki bayrak, direğe çekilmiş dalgalı bir bayrağın fotoğrafıydı.
Dört ülke için dört ayrı fotoğraf bulmak yerine aynı işlem dört bayrağa da
uygulanıyor: SVG -> raster -> dalga deformasyonu + kumaş gölgesi -> direk.
Böylece dört katalog yan yana konduğunda bayraklar aynı aileden görünüyor.

Geometri modeli (düz sinüs kaydırmadan farkı):
  · İki harmonikli dalga — tek sinüs "kurdele" gibi duruyor.
  · Yay uzunluğu sıkışması — dalganın dik olduğu yerde kumaş ekranda daralır.
    Bu olmadan bayrak esnetilmiş bir görüntü gibi görünüyor.
  · Yüzey normaline göre gölge — parlak/koyu bantlar kıvrımı takip eder.
  · Bükülme noktalarında hafif dikey daralma + fly ucuna doğru perspektif.
  · Her şey 3x süperörneklemeyle çizilip küçültülür (kenarlar pürüzsüz).

Tuval 1033x1549 ve bayrağın kadraj içindeki yeri AUSCAMP'teki
bayrak_onarilmis.png ile birebir aynı — kapak CSS'i değişmeden çalışsın diye.

Kullanım:  python3 tools/make_flags.py
Çıktı:     assets/img/bayrak_<ulke>.png
"""
import math
import pathlib
import subprocess

from PIL import Image, ImageEnhance, ImageFilter

ROOT = pathlib.Path(__file__).resolve().parent.parent
IMG = ROOT / "assets" / "img"
TMP = ROOT / "tools" / "_tmp"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# --- tuval / yerleşim: AUSCAMP bayrak_onarilmis.png ölçüldü ------------------
CANVAS = (1033, 1549)
POLE_X = 311           # direk ekseni
POLE_TOP = 398         # direk tepesi (topuz hariç)
FLAG_TOP = 476         # bayrağın hoist kenarının üst ucu
FLAG_H = 300           # dalgalanmadan önceki nominal bayrak yüksekliği
SS = 3                 # süperörnekleme katsayısı

# --- dalga ------------------------------------------------------------------
CYCLES = 1.45          # hoist -> fly arası tam dalga sayısı
AMP = 34.0             # fly ucundaki birinci harmonik genliği (px)
AMP2 = 0.32            # ikinci harmoniğin oranı
PHASE = 0.55
DROOP = 30.0           # fly ucunun yerçekimiyle düşmesi
TAPER = 0.88           # fly ucunda dikey daralma (perspektif)
TWIST = 0.13           # bükülme noktalarındaki ek dikey daralma
LIGHT = 0.62           # ışığın soldan gelme miktarı
SHADE_LO, SHADE_HI = 0.55, 1.15     # gölge / ışık uçları


# ---------------------------------------------------------------- bayrak SVG

UNION_JACK = """
<defs><clipPath id="uj"><path d="M30,15 h30 v15 z v15 h-30 z h-30 v-15 z v-15 h30 z"/></clipPath></defs>
<rect width="60" height="30" fill="#012169"/>
<path d="M0,0 L60,30 M60,0 L0,30" stroke="#fff" stroke-width="6"/>
<path d="M0,0 L60,30 M60,0 L0,30" clip-path="url(#uj)" stroke="#C8102E" stroke-width="4"/>
<path d="M30,0 v30 M0,15 h60" stroke="#fff" stroke-width="10"/>
<path d="M30,0 v30 M0,15 h60" stroke="#C8102E" stroke-width="6"/>
"""


def star(cx, cy, r_out, points, rot=0.0):
    """İç yarıçapı dışın 4/9'u olan çok köşeli yıldız (bayrak standardı)."""
    r_in = r_out * 4 / 9
    pts = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        a = rot - math.pi / 2 + i * math.pi / points
        pts.append(f"{cx + r * math.cos(a):.3f},{cy + r * math.sin(a):.3f}")
    return f'<polygon points="{" ".join(pts)}" fill="#fff"/>'


def svg_uk():
    return 60, 30, UNION_JACK


def svg_aus():
    """Flags Act 1953 Schedule 1: Commonwealth Star çapı 3H/10, Güney Haçı H/7,
    Epsilon H/12; canton sol üst çeyrek."""
    H, W = 30.0, 60.0
    s = [f'<rect width="{W}" height="{H}" fill="#00247D"/>',
         f'<g transform="scale(0.5)">{UNION_JACK}</g>',
         star(W / 4, 3 * H / 4, 3 * H / 20, 7)]
    for fx, fy, pts in [(0.7500, 0.8333, 7), (0.6875, 0.2500, 7),
                        (0.7500, 0.1667, 7), (0.8125, 0.3750, 7),
                        (0.7875, 0.5750, 5)]:
        s.append(star(fx * W, fy * H, H / 24 if pts == 5 else H / 14, pts))
    return W, H, "".join(s)


def svg_usa():
    H, W = 100.0, 190.0
    red, blue = "#B31942", "#0A3161"
    s = [f'<rect width="{W}" height="{H}" fill="#fff"/>']
    sh = H / 13
    for i in range(0, 13, 2):
        s.append(f'<rect y="{i * sh:.4f}" width="{W}" height="{sh:.4f}" fill="{red}"/>')
    cw, ch = W * 2 / 5, sh * 7
    s.append(f'<rect width="{cw:.4f}" height="{ch:.4f}" fill="{blue}"/>')
    r = 0.0616 * H / 2                                           # yıldız dış ÇAPI 0.0616H
    for row in range(9):
        cy = ch * (row + 1) / 10
        cols = range(1, 12, 2) if row % 2 == 0 else range(2, 11, 2)
        for c in cols:
            s.append(star(cw * c / 12, cy, r, 5))
    return W, H, "".join(s)


def svg_deu():
    H, W = 30.0, 50.0
    b = H / 3
    return W, H, (f'<rect width="{W}" height="{b}" fill="#000"/>'
                  f'<rect y="{b}" width="{W}" height="{b}" fill="#DD0000"/>'
                  f'<rect y="{2 * b}" width="{W}" height="{b}" fill="#FFCE00"/>')


FLAGS = {"aus": svg_aus, "uk": svg_uk, "usa": svg_usa, "deu": svg_deu}


# ---------------------------------------------------------------- rasterize

def render(name, vb_w, vb_h, body, h_px):
    """SVG'yi Chrome ile rasterize eder (clip-path'i doğru işleyen tek yol)."""
    TMP.mkdir(parents=True, exist_ok=True)
    w = int(round(h_px * vb_w / vb_h))
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {vb_w} {vb_h}" '
           f'width="{w}" height="{h_px}" shape-rendering="geometricPrecision">'
           f'{body}</svg>')
    html = TMP / f"{name}.html"
    html.write_text(f'<!doctype html><meta charset="utf-8">'
                    f'<style>*{{margin:0;padding:0}}html,body{{background:transparent}}</style>'
                    f'<body>{svg}</body>', encoding="utf-8")
    png = TMP / f"{name}.png"
    subprocess.run([CHROME, "--headless", "--disable-gpu", f"--screenshot={png}",
                    "--default-background-color=00000000", "--hide-scrollbars",
                    f"--window-size={w},{h_px}", "--force-device-scale-factor=1",
                    "--virtual-time-budget=4000", str(html)],
                   check=True, capture_output=True)
    return Image.open(png).convert("RGB").resize((w, h_px), Image.LANCZOS)


# ---------------------------------------------------------------- dalga modeli

def wave_profile(n, width):
    """Örneklenmiş dalga: (z, dz/dx, malzeme koordinatı) dizileri döndürür.

    z ve türev ekran pikseli cinsinden; malzeme koordinatı yay uzunluğuyla
    normalize edilir — kumaşın dik bölgelerde ekranda sıkışmasını sağlar.
    """
    zs, dzs = [], []
    for i in range(n):
        u = i / (n - 1)
        a = AMP * (u ** 1.15)
        ph = 2 * math.pi * CYCLES * u + PHASE
        z = a * (math.sin(ph) + AMP2 * math.sin(2 * ph + 0.6)) + DROOP * (u ** 1.9)
        zs.append(z)
        # analitik türev (dz/du), sonra piksel başına çevrilir
        da = AMP * 1.15 * (u ** 0.15) if u > 0 else 0.0
        w = 2 * math.pi * CYCLES
        dz = (da * (math.sin(ph) + AMP2 * math.sin(2 * ph + 0.6))
              + a * (w * math.cos(ph) + AMP2 * 2 * w * math.cos(2 * ph + 0.6))
              + DROOP * 1.9 * (u ** 0.9))
        dzs.append(dz / width)
    # yay uzunluğu -> malzeme koordinatı
    arc, acc = [0.0], 0.0
    for i in range(1, n):
        du = 1.0 / (n - 1)
        acc += math.hypot(du, (zs[i] - zs[i - 1]) / width)
        arc.append(acc)
    mat = [a / acc for a in arc]
    return zs, dzs, mat


def shade_mask(src_w, src_h, n, dzs, mat):
    """Yüzey normaline göre parlaklık maskesi — MALZEME uzayında üretilir,
    böylece deformasyondan önce düz görsele uygulanabilir."""
    lx, lz = -LIGHT, 1.0
    ln = math.hypot(lx, lz)
    raw, idx = [], []
    j = 0
    for sx in range(src_w):
        m = sx / max(1, src_w - 1)
        while j < n - 1 and mat[j] < m:          # malzeme -> örnek indeksi
            j += 1
        d = dzs[j]
        nn = math.hypot(d, 1.0)
        raw.append(((-d) * lx + 1.0 * lz) / (nn * ln))
        idx.append(j)
    # kontrastı profile göre otomatik ger: genlik değişse de bantlar aynı güçte kalsın
    lo, hi = min(raw), max(raw)
    span = max(1e-6, hi - lo)
    vals = []
    for sx, dot in enumerate(raw):
        t = ((dot - lo) / span) ** 0.85
        u = idx[sx] / (n - 1)
        t *= 1.0 - 0.16 * u                      # fly ucuna doğru hafif kararma
        if u < 0.06:                             # hoist'ta kumaş toplanması
            t *= 0.70 + 0.30 * (u / 0.06)
        vals.append(int(round(255 * max(0.0, min(1.0, t)))))
    row = Image.new("L", (src_w, 1))
    row.putdata(vals)
    return row.resize((src_w, src_h), Image.BILINEAR)


def warp(flat):
    """Düz bayrağı dalgalandırır. Her hedef sütun için kaynak dilim, yay uzunluğu
    haritasından seçilir; dikey konum ve yükseklik dalgadan gelir."""
    src_w, src_h = flat.size
    n = 2048
    zs, dzs, mat = wave_profile(n, src_w)

    # gölgeyi deformasyondan ÖNCE uygula (malzeme uzayında hesaplandı)
    mask = shade_mask(src_w, src_h, n, dzs, mat)
    lit = ImageEnhance.Brightness(flat).enhance(SHADE_HI)
    dim = ImageEnhance.Brightness(flat).enhance(SHADE_LO)
    flat = Image.composite(lit, dim, mask)
    flat = flat.convert("RGBA")

    pad = int(AMP * (1 + AMP2) + DROOP + 6 * SS)
    out_h = src_h + 2 * pad
    mesh = []
    for x in range(src_w):
        u = x / (src_w - 1)
        i = int(u * (n - 1))
        z = zs[i]
        half = (src_h / 2) * (1 - (1 - TAPER) * u)
        ph = 2 * math.pi * CYCLES * u + PHASE
        half *= 1 - TWIST * abs(math.sin(ph))    # bükülmede dikey daralma
        yc = pad + src_h / 2 + z
        y0, y1 = int(round(yc - half)), int(round(yc + half))
        if y1 <= y0:
            continue
        sx0 = mat[i] * (src_w - 1)
        sx1 = mat[min(n - 1, int(((x + 1) / (src_w - 1)) * (n - 1)))] * (src_w - 1)
        if sx1 <= sx0:
            sx1 = sx0 + 0.5
        mesh.append(((x, y0, x + 1, y1),
                     (sx0, 0, sx0, src_h, sx1, src_h, sx1, 0)))

    return flat.transform((src_w, out_h), Image.MESH, mesh, Image.BILINEAR), pad


def pole(canvas):
    """Silindirik gölgeli ince metal direk + topuz."""
    d = canvas.load()
    w, h = canvas.size
    for y in range(POLE_TOP, h):
        t = (y - POLE_TOP) / (h - POLE_TOP)
        half = 5.2 - 1.9 * t                              # perspektifle incelir
        x0, x1 = int(POLE_X - half) - 1, int(POLE_X + half) + 2
        for x in range(max(0, x0), min(w, x1)):
            r = abs(x - POLE_X) / half
            if r > 1:
                continue
            # silindir: sol tarafta parlama, sağa doğru koyulaşma
            s = (x - POLE_X) / half
            # beyaz kart üzerinde kaybolmasın diye orta gri tabanlı
            v = 196 - 122 * (s * 0.55 + 0.45) ** 2 - 30 * r ** 3
            a = 255 if r < 0.80 else int(255 * (1 - r) / 0.20)
            v = max(40, min(226, int(v)))
            d[x, y] = (v, v + 2, v + 7, max(0, min(255, a)))
    for y in range(POLE_TOP - 15, POLE_TOP + 3):          # topuz
        for x in range(POLE_X - 8, POLE_X + 9):
            if (x - POLE_X) ** 2 / 49 + (y - (POLE_TOP - 6)) ** 2 / 81 <= 1:
                s = (x - POLE_X) / 7.0
                v = max(76, min(224, int(200 - 104 * (s * 0.6 + 0.4) ** 2)))
                d[x, y] = (v, v + 2, v + 7, 255)


def build(key):
    vb_w, vb_h, body = FLAGS[key]()
    flat = render(key, vb_w, vb_h, body, FLAG_H * SS)
    waved, pad = warp(flat)
    waved = waved.filter(ImageFilter.GaussianBlur(0.6 * SS))
    w, h = waved.size
    waved = waved.resize((w // SS, h // SS), Image.LANCZOS)

    canvas = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    pole(canvas)
    canvas.alpha_composite(waved, (POLE_X + 2, FLAG_TOP - pad // SS))
    out = IMG / f"bayrak_{key}.png"
    canvas.save(out)
    print(f"{out.name}  bayrak {waved.size[0]}x{waved.size[1]}px")


if __name__ == "__main__":
    IMG.mkdir(parents=True, exist_ok=True)
    for k in FLAGS:
        build(k)

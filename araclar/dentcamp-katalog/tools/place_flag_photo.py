#!/usr/bin/env python3
"""Gerçek bayrak fotoğrafını kapak köşesindeki kadraja yerleştirir.

Gökyüzü rembg ile silinir, kalan bayrak+direk AUSCAMP kataloğundaki
bayrak_onarilmis.png ile AYNI kutuya oturtulur — böylece kapak CSS'i
(.cv-flag: left:-161.9pt top:-220.8pt width:496.7pt height:745pt) hiç
değişmeden dört ülkede de doğru kadrajı verir.

rembg sistem Python'unda yok; AUSCAMP kataloğundaki .venv kullanılıyor.

Kullanım:
  ~/auscamp-specialist-katalog/.venv/bin/python tools/place_flag_photo.py kaynak.jpg uk [derece]
"""
import pathlib
import sys
from collections import deque

from PIL import Image, ImageEnhance, ImageFilter

ROOT = pathlib.Path(__file__).resolve().parent.parent
IMG = ROOT / "assets" / "img"

# Ölçüler AUSCAMP bayrak_onarilmis.png'den; hepsi SS ile ölçekleniyor.
# Tuval 1033px iken kapakta 496.7pt'ye yerleşiyordu = 150 dpi. Kaynaklar yüksek
# çözünürlüklü olduğu için tuvali 2x basıyoruz -> ~300 dpi, baskıya uygun.
SS = 2
CANVAS = (1033 * SS, 1549 * SS)
# Bayrak ALTTAN hizalanır: alt kenar başlık şeridinin hemen üstünde durur,
# fazlası sayfanın üstünden taşar. Üstten hizalamada bayrağı büyütmek
# doğrudan başlığa bindiriyordu.
FLAG_X0, FLAG_W = 314 * SS, 620 * SS            # hoist sayfa kenarında; genişlik hedefi
FLAG_BOTTOM = 742 * SS                     # alt kenar (başlık şeridinin üstü)
FLAG_TOP = 464 * SS                        # üst sınır: sayfanın üst kenarı (tuval y=459)
                                      # Bayrak bunun üstüne taşarsa tepesi kırpık çıkıyor.
MAX_RISE = 170 * SS                      # çakışmada yukarı kaydırma payı
PILL_X = 579 * SS                           # başlık pill'inin sol ucu (tuval koordinatı)
PILL_Y = 752 * SS                           # başlık pill'inin üst kenarı
MIN_RUN = 140                          # bir satırı "bayrak" saymak için opak piksel
                                       # (kalın direkler 60'ı aşıp bayrak sanılıyordu)


def vision_cutout(src):
    """Apple Vision'ın özne maskesiyle keser (tools/_bin/kesici).

    Üçüncü yöntem, İngiltere bayrağı için eklendi. Diğer ikisi o karede
    çalışmıyor: gökyüzü silme, soluk gökyüzünden bayrağın BEYAZ bantlarına
    sızıp bayrağı delik deşik ediyor (Union Jack'in beyazı sayfanın en büyük
    yüzeyi); rembg ise mentör portrelerinde de görüldüğü gibi ek bağımlılık ve
    model indirmesi istiyor. Vision bayrağı direğiyle birlikte tek parça, temiz
    kenarla çıkarıyor ve makinede hazır.
    """
    import subprocess
    import tempfile
    kesici = ROOT / "tools" / "_bin" / "kesici"
    with tempfile.TemporaryDirectory() as t:
        g = pathlib.Path(t) / "g.png"
        c = pathlib.Path(t) / "c.png"
        src.save(g)
        r = subprocess.run([str(kesici), str(g), str(c)], capture_output=True, text=True)
        if r.returncode:
            sys.exit(f"kesici: {r.stderr.strip()}")
        return Image.open(c).convert("RGBA")


def sky_cutout(src, tol=20):
    """Gökyüzünü KENARDAN yayılarak siler.

    rembg, bayrağın beyaz şeritlerini ve yıldızlarını gökyüzü sanıp içeride delik
    açıyordu. Gökyüzü görüntü kenarlarına değen tek parça bir bölge; bayrağın içi
    ona bağlı değil. Bu yüzden kenar piksellerinden başlayıp KOMŞUSUNA benzeyen
    piksellere yayılıyoruz — degrade gökyüzünü baştan sona yürür, bayrak kenarındaki
    sert renk sıçramasında durur ve iç bölgelere hiç girmez.
    """
    im = src.convert("RGB")
    w, h = im.size
    px = im.load()
    sky = bytearray(w * h)
    q = deque()
    for x in range(w):
        for y in (0, h - 1):
            if not sky[y * w + x]:
                sky[y * w + x] = 1; q.append((x, y))
    for y in range(h):
        for x in (0, w - 1):
            if not sky[y * w + x]:
                sky[y * w + x] = 1; q.append((x, y))
    while q:
        x, y = q.popleft()
        r0, g0, b0 = px[x, y]
        for nx, ny in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
            if 0 <= nx < w and 0 <= ny < h and not sky[ny * w + nx]:
                r1, g1, b1 = px[nx, ny]
                if abs(r1-r0) + abs(g1-g0) + abs(b1-b0) < tol:
                    sky[ny * w + nx] = 1
                    q.append((nx, ny))
    a = Image.new("L", (w, h))
    a.putdata([0 if s else 255 for s in sky])
    a = a.filter(ImageFilter.MinFilter(3))          # gökyüzü halkasını içeri al
    a = a.filter(ImageFilter.GaussianBlur(0.8))     # kenarı yumuşat
    out = im.convert("RGBA")
    out.putalpha(a)
    return out


def cutout(path, rot=0.0, crop=None, flip=False, bright=1.0, sat=1.0, sky=False,
           vision=False):
    raw = Image.open(path)
    # Kaynak zaten kesilmiş gelmişse (şeffaf zeminli PNG/WebP) yeniden kesme —
    # rembg ya da gökyüzü silme hazır alfayı bozar.
    pre = raw.mode in ("RGBA", "LA") and raw.convert("RGBA").getchannel("A").getextrema()[0] < 250
    src = raw.convert("RGB")
    if crop:
        src = src.crop(crop)          # yan binaları / ikinci bayrağı dışarıda bırak
    if bright != 1.0:
        # Dört fotoğraf farklı gün ve pozlamadan geliyor; set olarak eşitlemek için
        src = ImageEnhance.Brightness(src).enhance(bright)
    if sat != 1.0:
        src = ImageEnhance.Color(src).enhance(sat)
    if flip:
        # Direği sola getirmek için yatay ayna. YALNIZ yatay simetrik bayraklarda
        # (Almanya) güvenli; Union Jack ve ABD bayrağı aynalanamaz.
        src = src.transpose(Image.FLIP_LEFT_RIGHT)
    if rot:
        # Dik sarkan bayraklar köşeyi dolduramıyor; hafif döndürmek onları
        # yatırır ve direk duvara monte gibi eğik durur — doğal görünüyor.
        src = src.rotate(rot, resample=Image.BICUBIC, expand=True,
                         fillcolor=(135, 178, 214))
    if pre:
        out = src.convert("RGBA")
        a = raw.convert("RGBA").getchannel("A")
        if crop:
            a = a.crop(crop)
        if flip:
            a = a.transpose(Image.FLIP_LEFT_RIGHT)
        if rot:
            a = a.rotate(rot, resample=Image.BICUBIC, expand=True, fillcolor=0)
        out.putalpha(a)
        return out
    if vision:
        return vision_cutout(src)
    if sky:
        return sky_cutout(src)
    from rembg import new_session, remove
    src.thumbnail((2600, 2600), Image.LANCZOS)     # rembg için yeterli, hızlı
    sess = new_session("isnet-general-use")        # gökyüzünde temiz kenar verir
    return remove(src, session=sess,
                  alpha_matting=True, alpha_matting_foreground_threshold=250,
                  alpha_matting_background_threshold=15,
                  alpha_matting_erode_size=6)


def overlaps_pill(canvas):
    """Bayrak, başlık şeridinin üstüne biniyor mu?"""
    a = canvas.split()[3]
    px = a.load()
    for y in range(PILL_Y, min(CANVAS[1], PILL_Y + 260 * SS), 3 * SS):
        for x in range(PILL_X, CANVAS[0], 3 * SS):
            if px[x, y] > 60:
                return True
    return False


def flag_bbox(im):
    """Direği saymadan bayrağın sınırlarını bulur (geniş opak satırlar)."""
    a = im.split()[3]
    w, h = im.size
    px = a.load()
    xs0, xs1, ys = w, 0, []
    for y in range(h):
        run = [x for x in range(w) if px[x, y] > 40]
        if len(run) > MIN_RUN:
            ys.append(y)
            xs0 = min(xs0, min(run))
            xs1 = max(xs1, max(run))
    if not ys:
        raise SystemExit("bayrak bulunamadı — kesim başarısız")
    return xs0, ys[0], xs1, ys[-1]


def place(path, key, rot=0.0, crop=None, flip=False, bright=1.0, sat=1.0,
          zoom=1.0, sky=False, vision=False):
    cut = cutout(path, rot, crop, flip, bright, sat, sky, vision)
    bx0, by0, bx1, by1 = flag_bbox(cut)
    bw, bh = bx1 - bx0, by1 - by0
    tw = FLAG_W
    # AUSCAMP kataloğundaki kurgu: bayrak köşeyi DOLDURUR ve sol kenardan taşar,
    # direk kadraj dışında kalır. Kutuya sığdırmak (contain) bayrağı ortada küçük
    # bırakıp etrafında boşluk yaratıyordu — burada kutuyu kaplıyoruz (cover) ve
    # sağ kenara hizalayıp fazlasını soldan taşırıyoruz.
    def render(z, bottom):
        # Genişliği doldur AMA yüksekliği de kadraja sığdır. Yalnız genişliğe göre
        # ölçeklenince uzun bayrakların TEPESİ sayfa dışında kalıp kırpık çıkıyordu.
        s = min(tw / bw, (FLAG_BOTTOM - FLAG_TOP) / bh) * z
        im = cut.resize((max(1, int(cut.width * s)), max(1, int(cut.height * s))),
                        Image.LANCZOS)
        fx, fy = bx0 * s, by0 * s                  # ölçekli görselde bayrağın sol-üstü
        c = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
        c.alpha_composite(im, (int(round(FLAG_X0 - fx)),           # hoist kenara
                               int(round(bottom - bh * s - fy))))  # alta yasla
        return c, s

    # Başlık pill'i sayfada x=116.3pt / y=140.7pt'de başlıyor. Bayrak o noktanın
    # SAĞINDA aşağı sarkarsa başlığın üstüne biniyor; sol tarafta sarkması sorun
    # değil (AUSCAMP orijinalinde de öyle). Sığana kadar küçültülür.
    # Çakışma olursa önce YUKARI kaydır (boyut korunur, fazlası sayfa üstünden taşar);
    # taşma sınırına gelinirse ancak o zaman küçült.
    bottom = FLAG_BOTTOM
    canvas, s = render(zoom, bottom)
    for _ in range(40):
        if not overlaps_pill(canvas):
            break
        if bottom > FLAG_BOTTOM - MAX_RISE:
            bottom -= 10 * SS
        else:
            zoom *= 0.95
        canvas, s = render(zoom, bottom)
    out = IMG / f"bayrak_{key}.png"
    canvas.save(out)
    print(f"{out.name}  bayrak {int(bw * s)}x{int(bh * s)}px  zoom={zoom:.2f}")


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("src"); ap.add_argument("key")
    ap.add_argument("--rot", type=float, default=0.0, help="derece (CCW), yatırmak için")
    ap.add_argument("--crop", help="x0,y0,x1,y1 — kesimden önce kırp")
    ap.add_argument("--flip", action="store_true", help="yatay ayna (direği sola al)")
    ap.add_argument("--bright", type=float, default=1.0, help="parlaklık çarpanı")
    ap.add_argument("--sat", type=float, default=1.0, help="doygunluk çarpanı")
    ap.add_argument("--zoom", type=float, default=1.0, help="kutuyu kaplama çarpanı")
    ap.add_argument("--sky", action="store_true",
                    help="gökyüzünü kenardan yayılarak sil (rembg yerine)")
    ap.add_argument("--vision", action="store_true",
                    help="Apple Vision özne maskesiyle kes (beyaz bantlı bayraklar)")
    a = ap.parse_args()
    place(a.src, a.key, a.rot,
          tuple(int(v) for v in a.crop.split(",")) if a.crop else None, a.flip,
          a.bright, a.sat, a.zoom, a.sky, a.vision)

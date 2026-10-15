#!/usr/bin/env python3
"""Mentör portrelerini katalog ölçüsüne normalize eder.

Kaynak: ~/Downloads/Mentör Biyografi ve fotoğraflar 2/  (kullanıcının Drive indirmesi)
Hedef : assets/img/m_<ad>.jpg  — 480x600 (4:5), JPEG q88

Neden 4:5 ve 480x600:
  Kart CSS'i (build.py .mphoto img) `object-fit:cover; object-position:50% 10%`
  kullanıyor. 4:5 bir görsel 86,6pt'lik kare dairede dikeyde taşar ve görünen
  bölge görselin yüksekliğinin ~%2–%82 aralığı olur; yüz bu yüzden kırpımın
  ÜST yarısında durmalı. 12 portrenin aynı oranda olması, kartların birebir aynı
  davranmasını sağlıyor.
  480 px, 86,6pt daire için ~400 dpi -> qa_check.py'nin 200 dpi alt sınırının
  iki katı. Eskiden portreler 900x1125 PNG'ydi ve PDF'leri ~5 MB'a çıkarıyordu;
  12 fotoğrafla o yol ~20 MB demekti.

yuz:
  (fcx, fcy, fw) = yüzün kaynak içindeki normalize konumu ve GENİŞLİĞİ.
  fcx/fw kaynak genişliğine, fcy kaynak yüksekliğine göre; fcy göz hattı.
  Kırpım bunlardan hesaplanır: yüz, kare dairenin çapının YUZ_ORAN kadarını
  kaplar ve göz hattı kırpımın YUZ_Y'sine oturur. Kaynaklar tam boy fotoğraftan
  yakın plana kadar değiştiği için sabit bir kırpım penceresi çalışmıyordu;
  yüz kutusundan hesaplamak 12 portrede aynı kadrajı veriyor.
"""
import pathlib
import unicodedata

from PIL import Image, ImageOps

ROOT = pathlib.Path(__file__).resolve().parent.parent
IMG = ROOT / "assets" / "img"
SRC = pathlib.Path.home() / "Downloads" / "Mentör Biyografi ve fotoğraflar 2"

W, H = 480, 600            # 4:5
Q = 88
YUZ_ORAN = 0.42            # yüz genişliği / kırpım genişliği (= daire çapı)
YUZ_Y = 0.30               # göz hattının kırpım içindeki dikey konumu

# (ad, kaynak yol, yuz) — ad, katalogda basılan addır; dosya adı buradan türetilir.
KADRO = [
    ("Beste Su Ulu",        "DEU/Beste Su Ulu.jpg",            (0.490, 0.287, 0.150)),
    ("Enes Yildiz",         "DEU/Enes Yıldız.jpg",             (0.530, 0.324, 0.178)),
    ("Ilke Aydin Demirel",  "DEU/İlke Aydın Demirel.jpg",      (0.520, 0.220, 0.300)),
    # Berlin karesi (kullanıcı, 24 Ağustos 2026): önceki kare yakın plan selfie'di,
    # saç tepesi kadrajın dışındaydı ve baş 12'li grid'de ötekilerin iki katıydı.
    ("Gizem Subasi",        "DEU/Gizemnur Subaşı berlin.jpeg",  (0.531, 0.640, 0.078)),
    ("Merve Olcay Duman",   "DEU/Merve Olcay Duman.jpg.jpeg",  (0.490, 0.339, 0.185)),
    ("Gulce Ugurlu",        "DEU/Gülçe Uğurlu.jpeg",           (0.531, 0.453, 0.115)),
    ("Ayse Nil Kocak",      "USA/AYŞE NİL KOÇAK.jpg",          (0.500, 0.374, 0.120)),
    ("Mustafa Kemal Atay",  "USA/Dt. Mustafa Kemal Atay.jpg",  (0.650, 0.279, 0.168)),
    ("Buse Yazici",         "USA/Buse Yazıcı.pdf",             (0.500, 0.355, 0.120)),
    ("Damla Engin Arpaci",  "UK/R.Damla Engin Arpacı.jpg",     (0.470, 0.373, 0.130)),
    ("Anita Gozubuyuk",     "AUS/Dt.Anita Gözübüyük.jpg",      (0.569, 0.316, 0.145)),
    ("Semanur Terzi",       "Semanur Terzi.jpg",               (0.520, 0.327, 0.170)),
]


def slug(ad):
    s = unicodedata.normalize("NFKD", ad).encode("ascii", "ignore").decode()
    return "m_" + s.lower().replace(" ", "_").replace(".", "") + ".jpg"


def load(rel):
    """JPEG'i doğrudan, PDF'i gömülü görselinden açar (Buse Yazıcı PDF olarak geldi)."""
    p = SRC / rel
    if p.suffix.lower() != ".pdf":
        # exif_transpose şart: Semanur Terzi'nin karesi Orientation=6 ile geliyor,
        # ham okunduğunda 90 derece yatık.
        return ImageOps.exif_transpose(Image.open(p)).convert("RGB")
    import io

    import fitz
    doc = fitz.open(p)
    xref = doc[0].get_images(full=True)[0][0]
    return Image.open(io.BytesIO(doc.extract_image(xref)["image"])).convert("RGB")


def kirp(im, yuz):
    """Yüz kutusundan 4:5 kırpım penceresi hesaplar ve 480x600'e ölçekler."""
    fcx, fcy, fw = yuz
    cw = fw * im.width / YUZ_ORAN
    ch = cw * H / W
    if cw > im.width or ch > im.height:               # pencere kaynağa sığmıyor
        k = min(im.width / cw, im.height / ch)
        cw, ch = cw * k, ch * k
    x = fcx * im.width - cw / 2
    y = fcy * im.height - YUZ_Y * ch
    x = min(max(x, 0), im.width - cw)                 # kenardan taşmayı içeri al
    y = min(max(y, 0), im.height - ch)
    box = (round(x), round(y), round(x + cw), round(y + ch))
    return im.crop(box).resize((W, H), Image.LANCZOS), box


def main():
    for ad, rel, yuz in KADRO:
        out = IMG / slug(ad)
        im = load(rel)
        kirpik, box = kirp(im, yuz)
        kirpik.save(out, "JPEG", quality=Q, optimize=True, progressive=True)
        eff = (box[2] - box[0]) / 1.2028      # 86,6pt = 1,2028 inç -> etkin dpi
        print(f"{out.name:28s} kırpım {box[2] - box[0]:>4d}x{box[3] - box[1]:<4d}"
              f" etkin {eff:>4.0f} dpi  {out.stat().st_size / 1024:>3.0f} KB")


if __name__ == "__main__":
    main()

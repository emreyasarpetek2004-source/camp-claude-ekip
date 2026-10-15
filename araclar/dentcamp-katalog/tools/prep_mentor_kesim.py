#!/usr/bin/env python3
"""Mentör portresini üretir: arka planı silinmiş mentör + düz yeşil daire zemin.

Akış:
  kaynak jpg -> exif_transpose -> tools/_bin/kesici (Vision özne maskesi)
             -> yüz kutusundan KARE çerçeveleme -> beyaz kontur
             -> yeşil zemin -> kart_<ad>.jpg

Kart KARE basılıyor, daireye çevirmeyi CSS yapıyor (.mkart img border-radius:50%).
Bayrak burada BASILMIYOR: dört ortak rozet dosyası (fdisc_/fchip_) CSS'te
konumlanıyor. Böylece bayrağın yeri ve biçimi 12 kartı yeniden kesmeden
değiştirilebiliyor ve dosya sayısı 12 yerine 4'te kalıyor.

Neden JPEG: alfa kanallı PNG olarak bırakıldığında (12 dosya, ~400 KB) dört PDF
8,6-9,5 MB'a çıkıyordu. Kart zemini zaten opak, o yüzden bindirme Python'da
yapılıyor ve kart tek opak JPEG olarak gidiyor; PDF'ler 3 MB civarına dönüyor.

Neden Vision: rembg ek bağımlılık ve ~170 MB model indirmesi istiyor; Apple'ın
segmentasyonu saç kenarlarında belirgin biçimde daha temiz ve makinede hazır.

Çerçeveleme mantığı: kişi dairenin ALT kenarından taşar, baş üstünde nefes payı
kalır; omuzlar daire kenarıyla kesiliyor. Yüzü kadraja getirmek için
kırpım baştan aşağı ölçülüyor, gövdenin tamamı değil: kaynaklar tam boydan
yakın plana kadar değişiyor.
"""
import pathlib
import subprocess
import sys
import tempfile
import unicodedata

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageOps

ROOT = pathlib.Path(__file__).resolve().parent.parent
IMG = ROOT / "assets" / "img"
SRC = pathlib.Path.home() / "Downloads" / "Mentör Biyografi ve fotoğraflar 2"
KESICI = ROOT / "tools" / "_bin" / "kesici"
sys.path.insert(0, str(ROOT / "tools"))

W, H = 560, 560              # kare portre (baskıda 104pt daire -> ~388 dpi)
Q = 88
KART_PT_W = 104.0
BAS_ORAN = 0.355             # baş yüksekliği / daire çapı
GOZ_Y = 0.315                # göz hattının daire içindeki dikey konumu
BAS_BOY = 0.95               # baş yüksekliği / Vision yüz kutusu genişliği
KONTUR_PT = 1.6              # kişinin çevresindeki beyaz kontur

# Kadrajı diğerlerinden farklı olması gereken kayıt kalmadı: 12 portrenin hepsi
# standart BAS_ORAN/GOZ_Y ile kesiliyor. Gizem Subaşı'nın eski karesi (yakın plan
# selfie) istisna gerektiriyordu; Berlin karesiyle o istisna kalktı.
OZEL = {}

from prep_mentors import KADRO   # noqa: E402  (ad, kaynak, elle ölçüm — artık okunmuyor)

# Yüz kutuları: tools/_bin/yuz_olc (Apple Vision) ile ölçüldü, elle DEĞİL.
#   (fcx, goz_y, fw) — fcx/fw kaynak genişliğine, goz_y kaynak yüksekliğine göre.
# Tabloyu yenilemek için:  python3 tools/prep_mentor_kesim.py olc
#
# Neden makine ölçümü: değerler prep_mentors.py'de tek tek elle girilmişti ve
# aynı şeyi ölçmüyorlardı. Vision kutusuna oranları 1,31 ile 1,92 arasında
# değişiyor, yani 12 portrede baş ölçeği %45'e varan farkla oynuyordu; grid'de
# bu, kimi mentörün yakın plan kimininse uzak durması demek. Vision kutusunun
# tanımı sabit olduğu için tek bir BAS_BOY katsayısı 12'sini de hizalıyor.
YUZ = {
    "Beste Su Ulu":        (0.515, 0.293, 0.196),
    "Enes Yildiz":         (0.540, 0.332, 0.263),
    "Ilke Aydin Demirel":  (0.505, 0.320, 0.487),
    "Gizem Subasi":        (0.531, 0.640, 0.078),
    "Merve Olcay Duman":   (0.489, 0.334, 0.341),
    "Gulce Ugurlu":        (0.499, 0.455, 0.167),
    "Ayse Nil Kocak":      (0.489, 0.426, 0.163),
    "Mustafa Kemal Atay":  (0.621, 0.263, 0.247),
    "Buse Yazici":         (0.471, 0.377, 0.193),
    "Damla Engin Arpaci":  (0.481, 0.400, 0.201),
    "Anita Gozubuyuk":     (0.508, 0.342, 0.211),
    "Semanur Terzi":       (0.522, 0.340, 0.327),
}


def slug(ad):
    s = unicodedata.normalize("NFKD", ad).encode("ascii", "ignore").decode()
    return s.lower().replace(" ", "_")


def ulkeler():
    """Kartın hangi bayrağı alacağı content/_common.py'deki kadro tablosundan gelir;
    ülke bilgisi tek yerde dursun."""
    sys.path.insert(0, str(ROOT))
    from content._common import MENTORLER
    return {m["foto"]: m["ulke"] for m in MENTORLER}


def yukle(rel):
    p = SRC / rel
    if p.suffix.lower() != ".pdf":
        return ImageOps.exif_transpose(Image.open(p)).convert("RGB")
    import io

    import fitz
    doc = fitz.open(p)
    xref = doc[0].get_images(full=True)[0][0]
    return Image.open(io.BytesIO(doc.extract_image(xref)["image"])).convert("RGB")


def kes(im):
    """Vision ile arka planı siler, RGBA döner."""
    with tempfile.TemporaryDirectory() as t:
        g = pathlib.Path(t) / "g.png"
        c = pathlib.Path(t) / "c.png"
        im.save(g)
        r = subprocess.run([str(KESICI), str(g), str(c)],
                           capture_output=True, text=True)
        if r.returncode:
            raise RuntimeError(f"kesici: {r.stderr.strip()}")
        return Image.open(c).convert("RGBA")


TEPE_ESIK = 0.25            # maskenin üst kenara değdiği genişlik / kaynak genişliği


def tepeyi_tamamla(rgba):
    """Kaynağın üst kenarında kesilmiş saç tepesini kubbe olarak tamamlar.

    Yakın plan selfie'lerde (Gizem Subaşı) baş, karenin üst kenarını aşıyor: saç
    tepesi fotoğrafta YOK. Kadrajı açmak onu geri getirmiyor, yalnız düz kesilmiş
    saç çizgisini dairenin içine sokuyor; olduğu gibi bırakmak da başı dairenin
    tepesinden kesiyor ve o portre 12'li grid'de tek başına ayrık duruyor.

    Yapılan: maskenin üst kenara değdiği aralık ölçülüyor, üstüne o aralığın
    yarıçapından türetilen bir elips kubbe ekleniyor, kubbenin içi de mevcut üst
    banttan aynalanarak dolduruluyor. Saç dokusu kişinin kendi saçı, silüet
    elipsin kendisi. Baskıda baş ~38pt, yani kubbe birkaç puntoluk bir yay.

    Uydurma piksel üretmek kural olarak yanlış, burada gerekçesi şu: alternatif,
    kişinin başını kesik basmak. Kesik baş da doğru bilgi değil, üstelik göze
    batıyor. Kaynak yenilenirse (yarım boy, saç tepesi kadrajda) bu işlev
    kendiliğinden devre dışı kalır: üst kenara değme olmaz, koşul tutmaz.
    """
    a = rgba.split()[3]
    px = a.load()
    w, h = rgba.size
    xs = [x for x in range(w) if px[x, 0] > 8]
    if len(xs) < TEPE_ESIK * w:
        return rgba
    x0, x1 = xs[0], xs[-1]
    rx = (x1 - x0) / 2.0
    cx = (x0 + x1) / 2.0
    # Kubbe yüksekliği: yarıçapın %62'si. Tam yarımküre balon gibi duruyor,
    # %30 hâlâ düz okunuyor; %62 saçlı bir tepe kavsi veriyor.
    ry = rx * 0.62
    pad = int(round(ry)) + 2

    genis = Image.new("RGBA", (w, h + pad), (0, 0, 0, 0))
    genis.paste(rgba, (0, pad))

    # Kubbenin içi SÜTUN SÜTUN doldurulur: her sütunda yukarıdan aşağı ilk KATI
    # piksel (alfa > 200) bulunup rengi yukarı taşınıyor, tepeye doğru koyulaşıyor.
    # İki yol denendi ve bırakıldı: (1) üst bandı aynalamak, alın ile saç çizgisini
    # de aynalayıp tepede sahte bir ikinci saç çizgisi bırakıyordu; (2) doğrudan
    # en üst satırı çoğaltmak, o satır kesim saçağı olduğu için yarı saydam ve
    # arka planla kirlenmiş renkler veriyordu.
    arr = np.asarray(genis).astype(np.float32)
    kati = arr[pad:pad + 60, :, 3] > 200
    ilk = np.argmax(kati, axis=0)
    var = kati.any(axis=0)
    renk = arr[pad + ilk, np.arange(w), :3]
    # Sütun renklerini yatayda yumuşat: tek piksellik saç telleri dikey şerit bırakıyor.
    cek = 25
    yast = np.pad(np.where(var[:, None], renk, np.nan), ((cek, cek), (0, 0)),
                  constant_values=np.nan)
    duz = np.stack([
        np.array([np.nanmean(yast[i:i + 2 * cek + 1, c]) if var[i] else 0.0
                  for i in range(w)]) for c in range(3)], axis=1)

    # Kubbe, gerçek saçın üstüne `gecis` piksel BİNİYOR ve o bantta alfası sıfıra
    # iniyor. Bindirme olmadan iki bölgenin arasında yatay bir dikiş çizgisi
    # kalıyordu: üstte düz örneklenmiş renk, altta gerçek saç dokusu.
    gecis = max(24, pad // 4)
    boy = pad + gecis
    yy = np.arange(boy)[:, None, None]
    koyuluk = 1.0 - 0.30 * (1 - np.clip(yy / pad, 0, 1)) ** 2      # tepede %30 koyu
    tepe = np.zeros((boy, w, 4), np.float32)
    tepe[:, :, :3] = duz[None, :, :] * koyuluk
    tepe[:, :, 3] = 255.0
    tepe[pad:, :, 3] = np.linspace(255, 0, gecis)[:, None]

    maske = Image.new("L", (w, boy), 255)
    ImageDraw.Draw(maske).rectangle((0, 0, w, pad), fill=0)
    ImageDraw.Draw(maske).ellipse(
        (round(cx - rx), 2, round(cx + rx), 2 + round(2 * ry)), fill=255)
    tepe[:, :, 3] *= np.asarray(maske).astype(np.float32) / 255.0
    tepe[:, ~var, 3] = 0

    genis.alpha_composite(Image.fromarray(tepe.clip(0, 255).astype(np.uint8)), (0, 0))
    return genis


def cercevele(rgba, yuz_px, ozel=None):
    """Yüz kutusundan 4:5 kart kadrajı. Baş, kart yüksekliğinin BAS_ORAN kadarını
    kaplar ve göz hattı GOZ_Y'ye oturur; böylece 12 kartta baş ölçeği aynı olur.
    Kişi kartın alt kenarından taşar, arkasında duruyormuş gibi.

    Alfa sınırına göre çerçeveleme denendi ve bırakıldı: kolların açık ya da
    kavuşmuş olması kişi genişliğini çok değiştiriyor, baş ölçeği kart kart
    tutmuyordu."""
    # yuz_px PİKSEL cinsinden: (yüz merkezi x, göz hattı y, yüz kutusu genişliği).
    # Normalize değer kullanılmıyor çünkü tepeyi_tamamla() tuvali büyütüyor ve
    # normalize göz hattı o an kayıyor.
    fcx, gozp, fw = yuz_px
    bas_oran, goz_y = ozel or (BAS_ORAN, GOZ_Y)
    bas_boy = fw * BAS_BOY
    yuk = bas_boy / bas_oran
    gen = yuk * W / H
    box = (round(fcx - gen / 2), round(gozp - goz_y * yuk), 0, 0)
    box = (box[0], box[1], box[0] + round(gen), box[1] + round(yuk))
    box = icine_kaydir(box, rgba.size)
    # Kadraj kaynağın dışına taşabilir (yakın plan fotoğraflar); şeffaf tuvale
    # oturtuyoruz, kırpmıyoruz.
    tuval = Image.new("RGBA", (round(gen), round(yuk)), (0, 0, 0, 0))
    kes_box = (max(box[0], 0), max(box[1], 0),
               min(box[2], rgba.width), min(box[3], rgba.height))
    ic = (kes_box[0] - box[0], kes_box[1] - box[1],
          kes_box[2] - box[0], kes_box[3] - box[1])
    tuval.paste(rgba.crop(kes_box), ic[:2])
    tuval = kenarlari_uzat(tuval, ic)
    return kontur(olcekle(tuval))


def olcekle(tuval):
    """RGBA'yı ÖN ÇARPILMIŞ olarak ölçekler.

    Düz RGBA'yı LANCZOS ile küçültmek, alfası sıfır piksellerin rengini kenardaki
    yarı saydam piksellere karıştırıyor. Kesim maskesinin dışında kalan renk
    kaynağın arka planı, yani İlke Aydın Demirel'in karesinde klinik duvarı: kontur
    onu beyazın üstüne basınca dairenin içine gri-mavi bir bant düşüyordu. "RGBa"
    modu (küçük a) ön çarpılmış RGBA'dır; o modda ölçeklenen kenar doğru ağırlanıyor.
    """
    buyutme = W / max(1, tuval.width)
    kes = tuval.convert("RGBa").resize((W, H), Image.LANCZOS).convert("RGBA")
    if buyutme > 1.15:
        kes = keskinlestir(kes, buyutme)
    return kes


def keskinlestir(kes, buyutme):
    """Kadraj büyütülerek üretildiyse yumuşamayı telafi eder.

    Kaynaklar 767 ile 4160 px arasında; kimi kare 560 px'lik portreye küçültülüyor,
    kimi büyütülüyor. Gizem Subaşı'nın Berlin karesinde kadraj 251 px, yani 2,2 kat
    büyütme var ve kart yan yana durduğu portrelerden gözle görülür yumuşak
    kalıyor. Maskeleme yalnız RGB'ye uygulanıyor: alfaya uygulanırsa kesim kenarı
    tırtıklanıyor ve beyaz kontur boncuklanıyor.
    """
    r, g, b, a = kes.split()
    yarici = min(1.6, 0.7 * buyutme)
    guc = min(120, round(45 * buyutme))
    rgb = Image.merge("RGB", (r, g, b)).filter(
        ImageFilter.UnsharpMask(radius=yarici, percent=guc, threshold=2))
    return Image.merge("RGBA", (*rgb.split(), a))


def icine_kaydir(box, boyut):
    """Kadraj kaynağın içine sığıyorsa taşan ekseni kaydırarak içeri alır.

    Yakın plan kaynaklarda (Gizem Subaşı) kadraj kaynağın kenarını birkaç yüz
    piksel aşıyordu; taşan yer kenar pikselinin çoğaltılmasıyla dolduruluyor ve
    dairenin tepesinde bulanık bir bant bırakıyordu. Kaydırmak yüzü ideal
    noktadan biraz oynatır ama uydurma piksel üretmez: doğru takas bu.

    Sığmayan eksene dokunulmuyor (İlke Aydın Demirel'in karesi kadrajdan dar);
    orada iki yanda kalan boşluk zaten şeffaf, yani yeşil zemin görünüyor.
    """
    x0, y0, x1, y1 = box
    gw, gh = boyut
    if x1 - x0 <= gw:
        x0, x1 = (max(0, x0), max(0, x0) + (x1 - x0))
        if x1 > gw:
            x0, x1 = gw - (x1 - x0), gw
    if y1 - y0 <= gh:
        y0, y1 = (max(0, y0), max(0, y0) + (y1 - y0))
        if y1 > gh:
            y0, y1 = gh - (y1 - y0), gh
    return (x0, y0, x1, y1)


def kenarlari_uzat(tuval, ic):
    """Kaynak, kadrajı doldurmuyorsa silüeti çerçeve kenarına kadar sürdürür.

    Kadraj kaynaktan büyük olabiliyor (yakın plan kareler geniş kadraja açıldığında).
    O zaman kaynağın DİKDÖRTGEN kenarı kadrajın ortasında kalıyor ve beyaz kontur
    kişinin değil fotoğrafın kenarını çiziyor: dairenin içinde kutu köşesi gibi
    duran çizgiler. Her yönde doğru olan şey farklı:

      üst   — HİÇBİR ŞEY. Baş tepesi tepeyi_tamamla() ile zaten kapatıldı, üstte
              kalan yer arka plan olmalı. Çoğaltma yapılırsa kubbenin tepesi
              yukarı doğru şerit şerit sürünüyor.
      yan   — YUVARLATILMIŞ ÇOĞALTMA. Kenar sütunu çoğaltılıyor ama alfası elips
              bir yay ile kısıtlanıyor, yani saç kütlesi yuvarlanarak bitiyor.
              İki yol denendi ve bırakıldı: düz çoğaltma yatay leke ve lekenin
              başladığı yerde basamak bırakıyor; aynalama ise saç tellerini
              görünür biçimde kopyalıyor.
      alt   — DÜZ ÇOĞALTMA. Gövde aşağı devam eder ve zaten daire tarafından
              kesilir; orada yuvarlatmak gövdeyi havada bitirirdi.
    """
    sol, ust, sag, alt = ic
    if alt < tuval.height:
        tuval.paste(tuval.crop((sol, alt - 1, sag, alt))
                    .resize((sag - sol, tuval.height - alt), Image.NEAREST), (sol, alt))
    for pay, sutun_x, hedef_x, ters in ((sol, sol, 0, True),
                                        (tuval.width - sag, sag - 1, sag, False)):
        if pay <= 0:
            continue
        sutun = tuval.crop((sutun_x, 0, sutun_x + 1, tuval.height))
        serit = sutun.resize((pay, tuval.height), Image.NEAREST)
        serit.putalpha(ImageChops.multiply(serit.split()[3], yan_yay(pay, sutun, ters)))
        tuval.alpha_composite(serit, (hedef_x, 0))
    return tuval


def yan_yay(pay, sutun, ters):
    """Yan uzatmanın alfa maskesi: silüetin bittiği yerde elips bir yay.

    Kenar sütununda opak olan y aralığı ölçülüyor; uzatma o aralığın ortasında
    tam `pay` kadar, uçlarında sıfır uzunlukta oluyor. Sonuç, yatay bir leke
    yerine kütlenin yuvarlanarak bitmesi.
    """
    a = sutun.split()[3]
    ys = [y for y in range(a.height) if a.getpixel((0, y)) > 8]
    maske = Image.new("L", (pay, a.height), 0)
    if not ys:
        return maske
    y0, y1 = ys[0], ys[-1]
    ImageDraw.Draw(maske).ellipse((-pay if ters else 0, y0,
                                   (pay - 1) if ters else (2 * pay - 1), y1), fill=255)
    return maske


def kontur(kes):
    """Kişinin çevresine beyaz kontur basar (alfa genişletme).

    Kontur olmadan koyu saçlar Almanya bayrağının siyah bandına karışıyor ve başın
    sınırı kayboluyor; ABD bayrağının beyaz şeritlerinde de aynı sorun ters yönde
    çıkıyor. CSS ile keyfi alfa biçiminin çevresine kontur çizilemediği için PNG'ye
    gömülüyor."""
    kes = sacagi_at(kes)
    k = max(1, round(KONTUR_PT * W / KART_PT_W))
    genis = kes.split()[3].filter(ImageFilter.MaxFilter(2 * k + 1))
    alt = Image.new("RGBA", kes.size, (255, 255, 255, 255))
    alt.putalpha(genis)
    alt.alpha_composite(kes)
    return alt


SACAK = 90                  # bu alfanın altındaki kenar pikselleri saçak sayılır


def sacagi_at(kes):
    """Kesim kenarındaki düşük alfalı saçağı temizler.

    Vision maskesi kenarda yarı saydam bir bant bırakıyor ve o bandın RENGİ
    kaynağın arka planından geliyor. Beyaz konturun üstüne bindiğinde arka plan
    tonu portrenin içine sızıyor. Alfa ikili yapılmıyor (saç kenarı tırtıklanır);
    eşiğin altı sıfıra çekilip üstü yeniden gerdiriliyor, yani yumuşak geçiş
    duruyor, yalnız saçak düşüyor.
    """
    r, g, b, a = kes.split()
    a = a.point(lambda v: 0 if v < SACAK else round((v - SACAK) * 255 / (255 - SACAK)))
    return Image.merge("RGBA", (r, g, b, a))


DARK = (0, 91, 82)          # theme.DARK — tüm mentör portrelerinin zemini


def zemin():
    """Düz DENTCAMP yeşili daire zemini.

    Önceki kurgu kartı ülke bayrağıyla TAMAMEN dolduruyordu, sonra bayrak karta
    gömülü minik bir kupüre indi. İkisi de bırakıldı (kullanıcı, 24 Ağustos 2026):
    zemin tek renk marka yeşili, ülke bilgisi CSS'teki ortak bayrak rozetiyle
    veriliyor. 12 portre böylece tek bir yüzey gibi okunuyor.
    """
    return Image.new("RGBA", (W, H), DARK + (255,))


def olc():
    """Yüz tablosunu Vision ile yeniden ölçer ve yapıştırılabilir biçimde basar."""
    for ad, rel, _ in KADRO:
        with tempfile.TemporaryDirectory() as t:
            g = pathlib.Path(t) / "g.png"
            yukle(rel).save(g)
            r = subprocess.run([str(ROOT / "tools" / "_bin" / "yuz_olc"), str(g)],
                               capture_output=True, text=True)
        if r.returncode:
            print(f'    # {ad}: ÖLÇÜLEMEDİ ({r.stderr.strip()})'); continue
        v = [f"{float(x):.3f}" for x in r.stdout.split()]
        print(f'    "{ad}":{" " * (22 - len(ad))}({", ".join(v)}),')


def hazirla(ad, rel):
    """Kaynağı kesip, gerekiyorsa tepesini tamamlar; yüz ölçümünü piksele çevirir."""
    rgba = kes(yukle(rel))
    fcx, fcy, fw = YUZ[ad]
    yuz_px = (fcx * rgba.width, fcy * rgba.height, fw * rgba.width)
    h0 = rgba.height
    rgba = tepeyi_tamamla(rgba)
    return rgba, (yuz_px[0], yuz_px[1] + (rgba.height - h0), yuz_px[2])


def main():
    for ad, rel, _ in KADRO:
        dosya = f"kart_{slug(ad)}.jpg"
        kart = zemin()
        rgba, yuz_px = hazirla(ad, rel)
        kart.paste(kesim := cercevele(rgba, yuz_px, OZEL.get(ad)), (0, 0), kesim)
        out = IMG / dosya
        kart.convert("RGB").save(out, "JPEG", quality=Q, optimize=True,
                                 progressive=True)
        print(f"{out.name:30s} {out.stat().st_size / 1024:4.0f} KB")


if __name__ == "__main__":
    (olc if len(sys.argv) > 1 and sys.argv[1] == "olc" else main)()

#!/usr/bin/env python3
"""DENTCAMP ülke kataloğu: HTML/CSS derleyici (tasarım sistemi).

Geometri AUSCAMP Specialist Pathway kataloğundan birebir devralındı
(A4 595.5x842.25 pt; kapak, mentör grid'i, road map ve köşe dekorları aynı ölçülerde).
Değişen: renk paleti (theme.py) ve metin (content/<ulke>.py).

Font eşlemesi AUSCAMP'teki gibi:
  kapak başlık   League Spartan Bold 46.8pt
  H1 / bar       Open Sans ExtraBold 25/14pt
  mentör isim    Arimo Bold 8.4pt
  gövde          Archivo 12.4pt
"""
import html as _h
import os
import importlib
import pathlib
import re

import theme as T

ROOT = pathlib.Path(__file__).parent

LOGO_W, LOGO_H = 151.9, 24.8          # dentcamp.png 3528x576 -> 6.125 oranı
LOGO_X = (595.5 - LOGO_W) / 2

# ---------------------------------------------------------------- markup yardımcıları


def md(t):
    """**kalın** -> <b>, satır sonlarını boşluğa çevirir."""
    t = _h.escape(" ".join(t.split()))
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)


def H1(t, sub=None):
    s = f"<h1>{_h.escape(t)}</h1>"
    if sub:
        s += f'<div class="h1sub">{_h.escape(sub)}</div>'
    return s


def BAR(t):
    return f'<div class="bar">{_h.escape(t)}</div>'


def P(t):
    return f"<p>{md(t)}</p>"


def SUB(t):
    return f'<div class="sub">{md(t)}</div>'


def UL(items):
    return "<ul>" + "".join(f"<li>{md(i)}</li>" for i in items) + "</ul>"


def DL(pairs):
    out = [f'<li><b>{md(a)}</b><br><span class="dd">{md(b)}</span></li>' for a, b in pairs]
    return f'<ul class="terms">{"".join(out)}</ul>'


# Bayrak rozetinin biçimi: disc | chip | wave. Üçü de aynı portreyle çalışıyor,
# tasarım denetimi hangisinin basılacağına karar veriyor (bkz. .mflag CSS'i).
MFLAG = os.environ.get("MFLAG", "disc")

# Rozet dosyasının ön eki. wave, kapak ve sayfa köşelerindeki dalgalı bayrağın
# aynısını kullanıyor; disc/chip tools/make_mentor_flags.py'den geliyor.
MFLAG_ON = {"disc": "fdisc", "chip": "fchip", "wave": "fwave"}

MD = 108.0                   # portre dairesinin çapı (pt)
# Kolon 124,75pt; 108pt çap iki daire arasında 16,75pt bırakıyor.
# Üst sınır 112,75pt (12pt boşluk), ama sayfa boşluğu çapla kapanmıyor:
# 104'ten 112'ye çıkmak satır başına yalnız 8pt kazandırıyor.


def mflag_gecmeleri():
    """Rozetin (sol, üst, genişlik, yükseklik, ek css) değerleri.

    disc: merkez dairenin kenarında, sağ altta 45 derece. Yarısı içeride.
    chip: aynı merkez, 4:3 kutu. Bayrağın tamamı görünüyor, kırpım riski yok.
    wave: gönderli dalgalı bayrak, dairenin SAĞ ÜSTÜNDE, dışarıda. Kadraj yüzü
          üst yarıya oturttuğu için bu köşede bayrak başın hizasına giriyor;
          gölgesi ve gönderi de grid'i kalabalıklaştırıyor. Karşılaştırma için
          duruyor, varsayılan değil.
    """
    r = MD / 2
    if MFLAG == "wave":
        g = 36.0
        return (MD - g + 6.0, -8.0, g, g, "border:0;box-shadow:none;")
    g = 30.0 if MFLAG == "disc" else 31.0
    y = g if MFLAG == "disc" else g * 0.75
    cx = cy = r + r * 0.7071            # rozet merkezi: daire kenarı, 45 derece
    return (round(cx - g / 2, 2), round(cy - y / 2, 2), g, round(y, 2),
            "border-radius:50%;" if MFLAG == "disc" else "border-radius:2.5pt;")


def bayrak(m):
    """Rozetin hangi bayrağı basacağı. `ulke` hedef ülkeyi (dört broşürden biri)
    gösterir ve kart sıralamasını sürer; koordinatörün hedef ülkesi yok ama bayrağı
    var. İki bilgi bu yüzden ayrı: rozet önce `bayrak`, yoksa `ulke`."""
    return m.get("bayrak") or m.get("ulke")


def MGRID(mentorler):
    """Mentör portreleri. Biyografi YOK, dört broşürde de tüm kadro basılır.

    Portre YUVARLAK: arka planı silinmiş mentör düz DENTCAMP yeşili bir dairenin
    içinde duruyor ve dairenin alt kenarından taşıyor. Ülke, dairenin kenarına
    oturan küçük bayrak rozetiyle veriliyor; rozet 12 portrede de aynı noktada.

    Bırakılan iki kurgu:
      - Kartı baştan sona dolduran bayrak zemini: 12'li grid dört ayrı bayrak
        deseninden oluşan alacalı bir yüzeye dönüyordu, portreler desene karışıyordu.
      - Bayrağın karta gömülmesi: kartın boş köşesine göre yer değiştiriyordu,
        yani her portrede başka yerdeydi (kullanıcı: "bayrakları saçma sapan
        yerleştirmişsin"). Rozet artık CSS'te, sabit noktada.

    Rozetin bayrağı `bayrak(m)` ile seçiliyor: koordinatörün hedef ülkesi yok
    ama Türk bayrağı rozeti var (kullanıcı, 24 Ağustos 2026).
    """
    kart = "".join(
        f'<div class="mcard"><div class="mkart">'
        f'<img class="mp" src="assets/img/{m["foto"]}">'
        + (f'<img class="mflag" src="assets/img/{MFLAG_ON[MFLAG]}_{bayrak(m)}.png">'
           if bayrak(m) else "")
        + f'</div>'
        f'<div class="mname">{_h.escape(m["ad"])}</div>'
        f'<div class="mdet">{"<br>".join(_h.escape(x) for x in m["alt"])}</div></div>'
        for m in mentorler)
    return f'<div class="mgrid">{kart}</div><!--/mgrid-->'


def CARDS3(items):
    """Üç kutuluk kart şeridi. Sayfa 2'deki üç paragraf düz akıyordu; aynı bilgi
    kart olarak hem daha hızlı okunuyor hem sayfayı dolduruyor."""
    return ('<div class="cards3">' + "".join(
        f'<div class="c3"><div class="c3t">{_h.escape(a)}</div>'
        f'<div class="c3x">{md(b)}</div></div>' for a, b in items)
            + "</div><!--/cards3-->")


def MCTA():
    """İletişim şeridi: DETAYLI BİLGİ İÇİN + site + CAMP hattı.

    Hem kurum tanıtımı sayfasında hem MENTÖRLERİMİZ sayfasında basılıyor, bu yüzden
    tek yerde duruyor. İç içe <div> KULLANMA: build_optimal'daki blok ayrıştırıcı
    `.*?</div>` ile eşleşiyor ve ilk kapanışta duruyor.
    """
    return (f'<div class="mcta"><span class="mctal">DETAYLI BİLGİ İÇİN</span>'
            f'<span class="mctar">{T.SITE} &nbsp;·&nbsp; CAMP HATTI {T.CAMP_LINE}</span>'
            f'</div>')


def BOX(t):
    return f'<div class="box">{md(t)}</div>'


def STATS(items):
    """Rakam kartları: sayfa altındaki boşluğu taranabilir bilgiye çevirir.

    Metnin içinde kaybolan kritik sayıları (süre, ücret, geçme oranı) öne çıkarır;
    okuyucu sayfayı tararken önce bunları görür. İç içe <div> yok: blok
    ayrıştırıcı `.*?</div>` ile eşleştiği için içeride yalnız <span> olmalı.
    """
    cards = "".join(
        f'<span class="stat"><span class="statv">{md(v)}</span>'
        f'<span class="statl">{md(l)}</span></span>' for v, l in items)
    return f'<div class="stats">{cards}</div>'


def KARSI(basliklar, satirlar):
    """Dört ülkeyi yan yana koyan karşılaştırma tablosu (yalnız toplu katalogda).

    Ülke katalogları tek yolu anlatıyor, karşılaştıracak bir şey yok; toplu
    katalogda okuyucunun ilk sorusu "hangisi bana uygun" olduğu için tablo
    ülke sayfalarından ÖNCE geliyor.

    İç içe <div> KULLANMA: build_optimal'daki blok ayrıştırıcı `.*?</div>` ile
    eşleşiyor ve ilk kapanışta duruyor; tablo ikiye bölünüp akıştan düşer.
    Satır çizgisi yerine satır zebrası kullanılıyor — hücre sayısı sabit
    olmadığı için CSS nth-child'a güvenmek yerine sınıf Python'da basılıyor.
    """
    h = "".join(f'<span class="kh">{_h.escape(b)}</span>' for b in basliklar)
    g = []
    for i, satir in enumerate(satirlar):
        z = " kz" if i % 2 else ""
        for j, hucre in enumerate(satir):
            cls = "kc kad" if j == 0 else "kc"
            g.append(f'<span class="{cls}{z}">{md(hucre)}</span>')
    return f'<div class="ktab">{h}{"".join(g)}</div>'


def MINIMAP(adimlar):
    """Sayfa içi yatay yol şeridi: numaralı daireler + kesikli hat.

    Tam sayfa road map'in (Catalog.page_roadmap) küçültülmüş hâli. Toplu
    katalogda her ülke tek sayfa aldığı için sürecin şeması metnin İÇİNDE
    duruyor; dört ülkeye dört tam sayfa road map verilseydi katalog 14 sayfa
    olurdu.

    `adimlar`: [(başlık, alt satır), ...] — 4 ile 6 arası. Altı adımda etiket
    genişliği 78pt'ye düşüyor, daha fazlası okunmuyor.

    İç içe <div> KULLANMA (bkz. KARSI).
    """
    if not 4 <= len(adimlar) <= 6:
        raise ValueError(f"MINIMAP 4-6 adım ister, {len(adimlar)} verildi")
    ad = "".join(
        f'<span class="mstep"><span class="mcirc">{i + 1}</span>'
        f'<span class="mt">{md(t)}</span><span class="mmd">{md(d)}</span></span>'
        for i, (t, d) in enumerate(adimlar))
    return f'<div class="mmap"><span class="mline"></span>{ad}</div>'


def CTA(line):
    """Katalog ortasına konan çağrı şeridi.

    Denetim şunu gösterdi: iletişim yalnız son sayfadaydı. Okuyucu kararı 4. sayfada
    verdiğinde geri dönmek zorunda kalıyordu. Bu şerit, hizmetler anlatıldıktan hemen
    sonra bir sonraki adımı verir.
    """
    # İç içe <div> KULLANMA: build_optimal'daki blok ayrıştırıcı `.*?</div>` ile
    # eşleşiyor ve ilk kapanışta duruyor; şerit ikiye bölünüp akıştan düşüyor.
    return (f'<div class="ctaband"><span class="ctatext">{md(line)}</span>'
            f'<span class="ctainfo"><span class="ctanum">{T.CAMP_LINE}</span>'
            f'<span class="ctasite">{T.SITE}</span></span></div>')


# ---------------------------------------------------------------- sayfalar


class Catalog:
    """Bir ülkenin kataloğu: theme.Country + content/<ulke>.py"""

    def __init__(self, key):
        self.key = key
        # T.ALL = dört ülke + toplu katalog. COUNTRIES'e eklenmedi: argümansız
        # derleme ve qa_check paleti oradan okuyor ve yalnız ülkeleri kastediyor.
        self.c = T.ALL[key]
        self.m = importlib.import_module(f"content.{key}")

    # -- kapak ---------------------------------------------------------------
    def page_cover(self):
        cv = self.m.COVER
        title = cv["title"].replace("\n", "<br>")
        # Toplu katalogda bayrak tek değil dört: ayrı kutu, ayrı ölçü.
        # COVER["bayrak"]=False ise kapakta hiç bayrak basılmaz (toplu katalog,
        # 2 Eylül 2026: kapak fotoğrafı dört bayrağı zaten taşıyor).
        flagcls = "cv-flags" if cv.get("flags") else "cv-flag"
        flagimg = ("" if cv.get("bayrak", True) is False
                   else f'<img class="{flagcls}" src="assets/img/{self.c.flag}">')
        kunye = "".join(
            f'<div class="kn"><span class="knl">{_h.escape(a)}</span>'
            f'<span class="knv">{_h.escape(b)}</span></div>'
            for a, b in cv.get("kunye", []))
        return f"""
<section class="page cover cover-{self.c.key}">
  <div class="cv-blob cv-b1"></div><div class="cv-blob cv-b2"></div>
  <div class="cv-blob cv-b3"></div><div class="cv-blob cv-b4"></div>
  <div class="cv-blob cv-b5"></div>
  <div class="cv-card"></div>
  {flagimg}
  <div class="cv-pill">{_h.escape(cv["pill"])}</div>
  <div class="cv-title">{title}</div>
  <div class="cv-logoline">
    <img src="assets/img/logo.png"><span>{_h.escape(cv["tag"])}</span>
  </div>
  <div class="cv-sub">{cv["sub"].replace(chr(10), "<br>")}</div>
  <div class="cv-accent"></div>
  <div class="cv-photo"><img src="assets/img/{self.c.cover_photo}"></div>
  <div class="cv-kunye">{kunye}</div>
</section>"""

    # -- kurum tanıtımı + mentörler -----------------------------------------
    def page_mentors(self):
        """Kurum tanıtımı sayfası.

        Mentör fotoğrafı/biyografisi BASILMIYOR: referans aldığımız AUSCAMP
        Specialist Pathway kataloğunda da mentör kartı yok; mentörlük
        HİZMETLERİMİZ içindeki "A'DAN Z'YE MENTÖRLÜK DESTEĞİ" bölümünde
        metin olarak anlatılıyor. Kart basmak hem sayfa şişiriyor hem de
        mentör sayısı eksikken boşluk bırakıyordu.
        """
        return self.inner("".join(self.m.INTRO) + MCTA(), top=66.0)

    # -- road map ------------------------------------------------------------
    # Daire merkezleri AUSCAMP Standart s8'den ölçüldü (33.2pt çap, sol/sağ şerit).
    # Dikey aralık adım sayısına göre yeniden dağıtılır: İngiltere ve ABD 6 adımlı.
    DIA = 33.2
    CX_L, CX_R = 148.3, 447.2          # sol / sağ daire merkez x'i
    CY_TOP, CY_BOT = 153.8, 604.0      # ilk ve son dairenin merkez y'si

    def circles(self, n):
        step = (self.CY_BOT - self.CY_TOP) / (n - 1)
        out = []
        for i in range(n):
            side = "l" if i % 2 == 0 else "r"
            cx = self.CX_L if side == "l" else self.CX_R
            out.append((cx - self.DIA / 2, self.CY_TOP + i * step - self.DIA / 2, side))
        return out

    def roadmap_path(self, n):
        """Daireleri bağlayan kesikli yol. AUSCAMP'te sabit 5 adımlık bir bitmap'ti;
        adım sayısı ülkeye göre değiştiği için SVG olarak üretiliyor."""
        step = (self.CY_BOT - self.CY_TOP) / (n - 1)
        r = 18.0                                   # köşe yarıçapı
        d = []
        for i in range(n - 1):
            y0 = self.CY_TOP + i * step
            y1 = y0 + step
            ym = (y0 + y1) / 2
            x0 = self.CX_L if i % 2 == 0 else self.CX_R
            x1 = self.CX_R if i % 2 == 0 else self.CX_L
            right = x1 > x0                        # yatay gidiş yönü
            sx = r if right else -r
            d.append(f"M{x0:.1f},{y0 + self.DIA / 2:.1f} V{ym - r:.1f} "
                     f"Q{x0:.1f},{ym:.1f} {x0 + sx:.1f},{ym:.1f} "
                     f"H{x1 - sx:.1f} Q{x1:.1f},{ym:.1f} {x1:.1f},{ym + r:.1f} "
                     f"V{y1 - self.DIA / 2:.1f}")
        return (f'<svg class="rpath" viewBox="0 0 595.5 842.25">'
                f'<path d="{" ".join(d)}" fill="none" stroke="{T.STEP}" stroke-width="3.4" '
                f'stroke-dasharray="9 6.5" stroke-linecap="round"/></svg>')

    def roadmap_specs(self):
        """Ülke bir ya da birden çok road map tanımlayabilir.

        ABD üç ayrı yol anlatıyor; tek bir birleşik şema hem kalabalık hem yanıltıcı
        oluyordu. ROADMAPS tanımlıysa her biri kendi sayfasına basılır, iletişim
        bloğu yalnız sonuncuya konur.
        """
        if hasattr(self.m, "ROADMAPS"):
            return self.m.ROADMAPS
        return [(self.m.ROADMAP_TITLE, self.m.ROADMAP_SUB, self.m.ROADMAP)]

    def roadmap_pages(self):
        """Kapaktan sonra gelen SABİT sayfalar: ülke kataloglarında road map,
        toplu katalogda kapanış sayfası.

        İkisi de akan gövdenin ARDINA ekleniyor ve `rmpage` sınıfını kullanıyor;
        böylece iletişim bloğu (.contact) sayfaya göre konumlanıyor ve birleştirme
        adımı ikisine de küçük köşe dekorunu (_sm) basıyor."""
        if hasattr(self.m, "CLOSING"):
            return [self.page_closing()]
        specs = self.roadmap_specs()
        return [self.page_roadmap(s, last=(i == len(specs) - 1))
                for i, s in enumerate(specs)]

    def page_closing(self):
        """Toplu kataloğun son sayfası: bir sonraki adım + iletişim.

        Ülke kataloglarında bu iş son road map sayfasının altındaki .contact
        bloğuna düşüyor. Toplu katalogda tam sayfa road map yok (her ülkenin
        şeması kendi sayfasında MINIMAP olarak duruyor), bu yüzden kapanış
        kendi sayfası: başlık, üç adımlık "bundan sonra ne oluyor" ve aynı
        iletişim bloğu.
        """
        cl = self.m.CLOSING
        adim = "".join(
            f'<div class="cls"><div class="clsn">{i + 1}</div>'
            f'<div class="clst">{_h.escape(t)}</div>'
            f'<div class="clsx">{md(x)}</div></div>'
            for i, (t, x) in enumerate(cl["steps"]))
        extra = "".join(
            f'<div class="cinfo"><div class="crow">'
            f'<img src="assets/img/icon_whatsapp.png"><b>{_h.escape(lbl)}</b></div>'
            f'<div class="cnum">{_h.escape(num)}</div></div>'
            for lbl, num in self.m.PHONES)
        contact = f"""<div class="contact">
  <div class="cnext">{md(cl["next"])}</div>
  <div class="cta"><span>DETAYLI BİLGİ İÇİN</span><span>BİZE ULAŞIN!</span></div>
  <div class="cinfo">
    <div class="crow"><span class="globe"></span>{T.SITE}</div>
    <div class="crow"><img src="assets/img/icon_instagram.png">{T.INSTAGRAM}</div>
  </div>
  {extra}
</div>"""
        body = (f'<h1 class="ctr">{_h.escape(cl["title"])}</h1>'
                f'<div class="hl"><span class="hlin">{_h.escape(cl["sub"])}</span></div>'
                f'<div class="clead">{md(cl["lead"])}</div>'
                f'<div class="cgrid">{adim}</div>{contact}')
        return self.inner(body, roadmap=True)

    def page_roadmap(self, spec=None, last=True):
        title_txt, sub_txt, rows = spec or self.roadmap_specs()[0]
        steps = []
        for (n, title, l1, l2, icon), (cx, cy, side) in zip(
                rows, self.circles(len(rows))):
            steps.append(f'<div class="rnum" style="left:{cx}pt;top:{cy}pt">{n}</div>')
            # AUSCAMP'te etiketler kısaydı (425pt sınırı yetiyordu); DENTCAMP etiketleri
            # daha uzun olduğu için kutular genişletildi — yoksa "soru" gibi tek kelimeler
            # alt satıra düşüp satırlar tırtıklı görünüyor.
            if side == "l":
                pos = (f'style="left:{cx + 43.2:g}pt;top:{cy - 15:g}pt;'
                       f'width:{470 - (cx + 43.2):g}pt;text-align:left"')
            else:
                pos = f'style="left:130pt;top:{cy - 25:g}pt;width:{cx - 6 - 130:g}pt;text-align:right"'
            steps.append(f"""<div class="rstep r{side}" {pos}>
  <div class="rtitle">{title}</div>
  <div class="rrow">
    <img class="ricon" src="assets/img/{icon}">
    <div class="rtext"><b>{l1}</b><br>{l2}</div>
  </div>
</div>""")

        if not last:                     # iletişim bloğu yalnız son road map'te
            body = (f'<h1 class="ctr">{_h.escape(title_txt)}</h1>'
                    f'<div class="hl"><span class="hlin">{_h.escape(sub_txt)}</span></div>'
                    f'{self.roadmap_path(len(rows))}{"".join(steps)}')
            return self.inner(body, roadmap=True)

        extra = "".join(
            f'<div class="cinfo"><div class="crow">'
            f'<img src="assets/img/icon_whatsapp.png"><b>{_h.escape(lbl)}</b></div>'
            f'<div class="cnum">{_h.escape(num)}</div></div>'
            for lbl, num in self.m.PHONES)
        # "İlk görüşme ücretsiz" cümlesi kaldırıldı: bu broşür ilk görüşmeyi
        # zaten yapmış kişilere gönderiliyor, oraya ilk görüşme daveti anlamsız.
        # Buna karşılık kapanışta okuyucuya BİR SONRAKİ ADIMI söyleyen cümle yoktu;
        # sayfa yalnızca telefon/site veriyordu.
        contact = f"""<div class="contact">
  <div class="cnext">Bir sonraki adım, <b>kişiye özel yol planınızın çıkarılmasıdır:</b>
    plan, mevcut durumunuz ve hedef takviminiz üzerinden hazırlanır.</div>
  <div class="cta"><span>DETAYLI BİLGİ İÇİN</span><span>BİZE ULAŞIN!</span></div>
  <div class="cinfo">
    <div class="crow"><span class="globe"></span>{T.SITE}</div>
    <div class="crow"><img src="assets/img/icon_instagram.png">{T.INSTAGRAM}</div>
  </div>
  {extra}
</div>"""

        body = (f'<h1 class="ctr">{_h.escape(title_txt)}</h1>'
                f'<div class="hl"><span class="hlin">{_h.escape(sub_txt)}</span></div>'
                f'{self.roadmap_path(len(rows))}'
                f'{"".join(steps)}{contact}')
        return self.inner(body, roadmap=True)

    # -- gövde ---------------------------------------------------------------
    def body_pages(self):
        """Akan gövde: kurum tanıtımı + content modülündeki BODY listesi.

        "DENTCAMP NEDİR?" eskiden sabit sayfaydı; mentör kartları kalkınca sayfanın
        481pt'si boş kaldı. Akışa alınınca arkasından gelen bölüm aynı sayfada
        devam ediyor ve katalog bir sayfa kısalıyor."""
        secs = [list(self.m.INTRO)] + [list(x) for x in self.m.BODY]
        # Mentör kadrosu 12 kart / 610pt, yani kendi sayfasını istiyor ve hiçbir
        # bölümle sayfa paylaşamıyor. Girişin hemen ardına konunca sayfa 2'de
        # yalnız 185pt'lik giriş kalıyor; kadrodan ÖNCE bir bölüm daha geçince
        # sayfa 2 doluyor. Kadro hangi BODY bölümünden sonra basılacağı ülke
        # dosyasındaki MENTOR_YERI ile belirlenir: kadro sayfa paylaşamadığı için
        # kendisinden önceki bölümün sayfa sonunda kuyruk bırakmaması gerekiyor
        # (ABD'de MENTOR_YERI=0 iken sayfa 3 yalnız %15 doluydu).
        secs.insert(getattr(self.m, "MENTOR_YERI", 0) + 2,
                    list(self.m.MENTORLER_BOLUM))
        return [self.inner("".join(sec)) for sec in secs]

    def inner(self, body, faq=False, roadmap=False, top=None):
        deco = """
  <div class="d-tr-circle"></div><div class="d-tr-green"></div><div class="d-tr-yellow"></div>
  <div class="d-bl-yellow"></div><div class="d-bl-green"></div><div class="d-bl-circle"></div>
  <img class="pglogo" src="assets/img/logo.png">"""
        if faq:
            deco = deco.replace(
                '<div class="d-tr-circle"></div><div class="d-tr-green"></div>'
                '<div class="d-tr-yellow"></div>',
                '<div class="d-faq">?</div><div class="d-faq2">?</div>')
        cls = "page" + (" rmpage" if roadmap else "")
        st = f' style="top:{top:.0f}pt"' if top is not None else ""
        return f'<section class="{cls}">{deco}<div class="content"{st}>{body}</div></section>'

    # -- CSS -----------------------------------------------------------------
    def css(self, body_pt=12.4):
        lh = round(body_pt * 14.3 / 12.0, 2)
        pm = round(body_pt * 6.0 / 12.0, 2)
        mf = mflag_gecmeleri()
        return (CSS
                .replace("__DARK__", T.DARK).replace("__BRIGHT__", T.BRIGHT)
                .replace("__MINT__", T.MINT).replace("__STEP__", T.STEP)
                .replace("__ACC__", T.ACCENT).replace("__ACCFG__", T.ACCENT_FG)
                .replace("__B1__", T.BLOB["b1"]).replace("__B2__", T.BLOB["b2"])
                .replace("__B3__", T.BLOB["b3"]).replace("__B4__", T.BLOB["b4"])
                .replace("__B5__", T.BLOB["b5"])
                .replace("__LOGOW__", f"{LOGO_W:g}").replace("__LOGOH__", f"{LOGO_H:g}")
                .replace("__LOGOX__", f"{LOGO_X:g}")
                .replace("__BP__", f"{body_pt:g}")
                .replace("__LH2__", f"{round(lh * 0.955, 2):g}")
                .replace("__LH3__", f"{round(lh * 0.925, 2):g}")
                .replace("__PM3__", f"{round(pm * 0.6, 2):g}")
                .replace("__LH__", f"{lh:g}").replace("__PM__", f"{pm:g}")
                .replace("__MD__", f"{MD:g}")
                .replace("__MFX__", f"{mf[0]:g}").replace("__MFY__", f"{mf[1]:g}")
                .replace("__MFW__", f"{mf[2]:g}").replace("__MFH__", f"{mf[3]:g}")
                .replace("__MFR__", mf[4]))


CSS = """
@font-face{font-family:'OS';src:url('assets/fonts/OpenSans-ExtraBold.ttf')format('truetype');
  font-weight:800;font-style:normal}
@font-face{font-family:'LS';src:url('assets/fonts/LeagueSpartan-Bold.ttf')format('truetype');
  font-weight:700;font-style:normal}
@font-face{font-family:'AR';src:url('assets/fonts/Arimo-Bold.ttf')format('truetype');
  font-weight:700;font-style:normal}
@font-face{font-family:'BODY';src:url('assets/fonts/Archivo-Regular.ttf')format('truetype');
  font-weight:400;font-style:normal}
@font-face{font-family:'BODY';src:url('assets/fonts/Archivo-Bold.ttf')format('truetype');
  font-weight:700;font-style:normal}

*{margin:0;padding:0;box-sizing:border-box}
@page{size:595.5pt 842.25pt;margin:0}
html,body{width:595.5pt}
body{font-family:'BODY';color:__DARK__;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{position:relative;width:595.5pt;height:842.25pt;overflow:hidden;background:#fff;
  page-break-after:always;break-after:page}
.page:last-child{page-break-after:auto;break-after:auto}

/* --- iç sayfa dekorları (ölçüler AUSCAMP kataloğundan) --- */
.d-tr-circle{position:absolute;left:385pt;top:26.8pt;width:27pt;height:27pt;border-radius:50%;
  background:__ACC__}
.d-tr-green{position:absolute;left:421.4pt;top:0;width:52.5pt;height:52.5pt;background:__DARK__;
  border-radius:0 0 0 52.5pt}
.d-tr-yellow{position:absolute;left:489.3pt;top:0;width:106.2pt;height:53.1pt;background:__BRIGHT__;
  border-radius:0 0 53.1pt 53.1pt}
.d-bl-yellow{position:absolute;left:0;top:799.6pt;width:89.8pt;height:44.9pt;background:__BRIGHT__;
  border-radius:44.9pt 44.9pt 0 0}
.d-bl-green{position:absolute;left:102.8pt;top:799.6pt;width:44.4pt;height:44.4pt;background:__DARK__;
  border-radius:44.4pt 0 0 0}
.d-bl-circle{position:absolute;left:159.9pt;top:796.2pt;width:27pt;height:27pt;border-radius:50%;
  background:__BRIGHT__}
.pglogo{position:absolute;left:__LOGOX__pt;top:797.3pt;width:__LOGOW__pt;height:__LOGOH__pt}
/* road map sayfası: geniş H1'e yer açmak için küçük köşe dekoru */
.s-tr-circle{position:absolute;left:430.6pt;top:21pt;width:21.2pt;height:21.2pt;border-radius:50%;
  background:__ACC__}
.s-tr-green{position:absolute;left:459.1pt;top:0.4pt;width:41.2pt;height:41.2pt;background:__DARK__;
  border-radius:0 0 0 41.2pt}
.s-tr-yellow{position:absolute;left:512.3pt;top:0;width:83.2pt;height:41.6pt;background:__BRIGHT__;
  border-radius:0 0 41.6pt 41.6pt}
.d-faq{position:absolute;right:22pt;top:-2pt;font-family:'OS';font-weight:800;font-size:78pt;
  color:__BRIGHT__;line-height:1;transform:rotate(9deg)}
.d-faq2{position:absolute;right:74pt;top:26pt;font-family:'OS';font-weight:800;font-size:52pt;
  color:__BRIGHT__;line-height:1;transform:rotate(-13deg)}

.content{position:absolute;left:49.7pt;top:66pt;width:498pt}
.rmpage .content{top:52pt}

h1{font-family:'OS';font-weight:800;font-size:25pt;line-height:1.12;text-transform:uppercase;
  color:__DARK__;letter-spacing:-.2pt}
h1.ctr{text-align:center;font-size:26.6pt}
.h1sub{font-family:'OS';font-weight:800;font-size:14pt;color:__DARK__;margin:1pt 0 6pt}
.bar{display:block;width:fit-content;font-family:'OS';font-weight:800;font-size:14pt;
  line-height:21.4pt;color:#fff;background:__DARK__;border-radius:999pt;padding:0 13pt;
  margin:7pt 0 4pt 0}
p{font-size:__BP__pt;line-height:__LH__pt;margin:0 0 __PM__pt}
.sub{font-family:'BODY';font-weight:700;font-size:__BP__pt;line-height:__LH__pt;margin:5pt 0 2pt}
ul{list-style:none;margin:0 0 6pt}
li{font-size:__BP__pt;line-height:__LH__pt;padding-left:18pt;position:relative;margin-bottom:1pt}
li:before{content:"";position:absolute;left:9.6pt;top:5.6pt;width:3pt;height:3pt;border-radius:50%;
  background:__DARK__}
b{font-weight:700}
ul.terms li{margin-bottom:3.4pt}
ul.terms .dd{font-weight:400}
/* Bir sayfadan azıcık taşan uzun listeler (SSS / kavramlar) için sıkıştırma
   kademeleri. build_optimal ölçümden sonra en hafif yeterli kademeyi uygular;
   hiçbiri yetmezse bölüm iki sayfaya bölünür. */
.sq1 ul.terms li{margin-bottom:1.6pt}
.sq2 ul.terms li{margin-bottom:0.6pt}
.sq2 li,.sq2 p{line-height:__LH2__pt}
.sq3 ul.terms li{margin-bottom:0.2pt}
.sq3 li,.sq3 p{line-height:__LH3__pt}
.sq3 p{margin-bottom:__PM3__pt}
.box{background:__MINT__;border-radius:9pt;padding:8pt 11pt;font-size:__BP__pt;
  line-height:__LH__pt;margin-top:8pt}

/* --- rakam kartları --- */
.stats{display:flex;gap:9pt;margin:13pt 0 4pt}
.stat{flex:1 1 0;display:block;background:__MINT__;border-radius:9pt;padding:11pt 9pt;
  text-align:center}
.statv{display:block;font-family:'OS';font-weight:800;font-size:21pt;line-height:24pt;
  color:__DARK__;letter-spacing:-.3pt}
.statl{display:block;font-size:9.6pt;line-height:12.2pt;color:__DARK__;margin-top:3pt}

/* --- karşılaştırma tablosu (toplu katalog) --- */
/* Kolon genişlikleri ölçüldü: ülke adı en dar, "ana sınav" en geniş sütun.
   Grid kullanılıyor çünkü <table> TOKEN'da yok ve blok ayrıştırıcı tabloyu
   satırlarına bölerdi. */
/* Kolon genişlikleri hücre içeriğine göre ölçüldü: "belirleyici şart" en uzun
   metni taşıyor, "hedef" tek kelime. İlk denemede 76pt verilen şart sütunu dört
   satıra sarıyor ve Avustralya satırını iki katına çıkarıyordu. Toplam 498pt. */
.ktab{display:grid;grid-template-columns:68pt 104pt 132pt 122pt 72pt;
  margin:12pt 0 6pt;border-radius:9pt;overflow:hidden}
.kh{background:__DARK__;color:#fff;font-family:'AR';font-weight:700;font-size:7.4pt;
  letter-spacing:.11em;padding:6pt 7pt;text-transform:uppercase}
.kc{font-size:9.2pt;line-height:12.2pt;padding:7pt;background:#fff}
.kc.kz{background:__MINT__}
.kad{font-family:'OS';font-weight:800;font-size:10.4pt;line-height:12.6pt;color:__DARK__}

/* --- sayfa içi mini yol şeridi (toplu katalog) --- */
/* Tam sayfa road map'in küçültülmüş hâli: aynı numaralı daire + kesikli hat
   dili, tek satırda. Hat, dairelerin ARKASINDA kalsın diye .mstep konumlu. */
.mmap{position:relative;display:flex;justify-content:space-between;gap:5pt;
  margin:13pt 0 7pt}
.mline{position:absolute;left:32pt;right:32pt;top:14.6pt;height:0;
  border-top:2.2pt dashed __STEP__}
.mstep{position:relative;flex:1 1 0;text-align:center}
.mcirc{display:block;width:29.4pt;height:29.4pt;margin:0 auto 5pt;border-radius:50%;
  background:__STEP__;color:#fff;font-family:'OS';font-weight:800;font-size:14.6pt;
  line-height:29.4pt;text-align:center}
.mt{display:block;font-family:'BODY';font-weight:700;font-size:8.4pt;line-height:10.4pt;
  color:__DARK__}
.mmd{display:block;font-size:7.6pt;line-height:9.6pt;color:#3f7d75;margin-top:2pt}

/* --- katalog ortası çağrı şeridi --- */
.ctaband{display:flex;align-items:center;justify-content:space-between;gap:14pt;
  background:__DARK__;border-radius:9pt;padding:10pt 14pt;margin:12pt 0 4pt}
.ctatext{display:block;font-family:'OS';font-weight:800;font-size:13pt;line-height:16pt;
  color:#fff;flex:1 1 auto}
.ctainfo{display:block;flex:0 0 auto;text-align:right}
.ctanum{display:block;font-family:'OS';font-weight:800;font-size:15pt;color:__BRIGHT__}
.ctasite{display:block;font-family:'BODY';font-weight:700;font-size:10.5pt;
  color:rgba(255,255,255,.88);margin-top:1pt}

/* --- mentör bloğu (gerçek kişi) --- */
.mrow{display:flex;gap:19pt;align-items:flex-start;margin-top:17pt}
.mpic{flex:0 0 auto}
.mpic img{width:150pt;height:187.5pt;object-fit:cover;border-radius:14pt;
  box-shadow:0 5pt 15pt rgba(0,0,0,.17)}
.mbody{flex:1 1 auto}
.mname2{font-family:'OS';font-weight:800;font-size:19pt;line-height:22pt;color:__DARK__}
.mmeta{display:inline-block;background:__MINT__;color:__DARK__;font-family:'AR';
  font-weight:700;font-size:8.4pt;letter-spacing:.05em;padding:3.4pt 10pt;
  border-radius:99pt;margin:6pt 0 10pt}
.mbody p{font-size:11pt;line-height:15.2pt;margin-bottom:6.5pt}
.mbody p:last-child{margin-bottom:0}

.cards3{display:flex;gap:11pt;margin-top:14pt}
.c3{flex:1 1 0;background:__MINT__;border-radius:11pt;padding:12pt 13pt 13pt}
.c3t{font-family:'OS';font-weight:800;font-size:11.4pt;color:__DARK__;margin-bottom:5pt;
  line-height:13.6pt}
.c3x{font-size:10.4pt;line-height:14.2pt;color:__DARK__}

.mcta{display:flex;align-items:center;gap:12pt;margin-top:26pt;padding:11pt 16pt;
  background:__MINT__;border-radius:12pt}
.mctal{font-family:'OS';font-weight:800;font-size:10pt;letter-spacing:.05em;
  color:__DARK__;flex:0 0 auto}
.mctar{font-family:'AR';font-weight:700;font-size:10.6pt;color:__DARK__}

/* minmax(0,1fr): .mname nowrap olduğu için 1fr track'in ASGARİ genişliğini en uzun
   isim belirliyordu; kolonlar 121,5-133,6pt arasında oynuyor ve dört mentör sayfası
   birbirini tutmuyordu. */
.mgrid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));row-gap:28pt;
  margin-top:20pt}
.mcard{text-align:center}
/* Portre KARE bir JPEG (560x560, ~388 dpi); daireye çevirmeyi CSS yapıyor.
   İçinde düz yeşil zemin + beyaz kontur + arka planı silinmiş mentör var,
   tools/prep_mentor_kesim.py bindiriyor. Alfa kanallı PNG olarak bırakıldığında
   PDF'ler 8,6-9,5 MB'a çıkıyordu, bu yüzden tek opak JPEG. */
.mkart{position:relative;width:__MD__pt;height:__MD__pt;margin:0 auto}
.mkart img.mp{display:block;width:__MD__pt;height:__MD__pt;border-radius:50%;
  box-shadow:0 0 0 .7pt rgba(0,91,82,.28)}
/* Rozet mutlak konumlu ve 12 portrede AYNI noktada: merkezi, dairenin kenarı
   üzerinde sağ altta 45 derecede duruyor (yarıçap x cos45 = yarıçap x sin45).
   Yarısı dairenin içinde, yarısı dışında; beyaz halka ikisini ayırıyor.
   Sağ alt seçildi çünkü kadraj yüzü üst yarıya oturtuyor, alt yarı gövde. */
/* Gölgenin yanına marka renginde kıl çizgi: Alman rozetinin altın bandı beyaz
   sayfaya karşı 1,49:1 kontrast veriyor ve rozetin dairenin dışında kalan çeyreği
   siluetsiz basılıyordu. Aynı numara .mkart img.mp üzerinde de var. __MFR__ kuralın
   SONUNDA: başta olsaydı sonraki border/box-shadow bildirimleri onu ezerdi. */
.mflag{position:absolute;left:__MFX__pt;top:__MFY__pt;width:__MFW__pt;height:__MFH__pt;
  border:1.6pt solid #fff;
  box-shadow:0 0 0 .6pt rgba(0,91,82,.45),0 .8pt 2.4pt rgba(0,0,0,.18);__MFR__}
.mname{display:table;white-space:nowrap;margin:9pt auto 0;position:relative;background:__MINT__;
  font-family:'AR';font-weight:700;font-size:8pt;line-height:12.2pt;padding:0 4pt;color:__DARK__;
  border-radius:1.5pt}
.mdet{font-family:'AR';font-weight:700;font-size:6.3pt;line-height:8.6pt;margin-top:1.5pt}

/* --- kapak --- */
.cover{background:__DARK__}
.cv-card{position:absolute;left:59.5pt;top:-77.8pt;width:610.7pt;height:861.1pt;background:#fcfcfc;
  border-radius:34pt}
.cv-blob{position:absolute;left:2.8pt}
.cv-b1{top:140.7pt;width:70.8pt;height:70.8pt;border-radius:50%;background:__B1__}
.cv-b2{top:232.2pt;width:71.5pt;height:143.1pt;background:__B2__;border-radius:0 71.5pt 71.5pt 0}
.cv-b3{left:-2.7pt;top:424.4pt;width:43.1pt;height:43.1pt;border-radius:50%;background:__B3__}
.cv-b4{top:487.8pt;width:70.8pt;height:70.8pt;border-radius:50%;background:__B4__}
.cv-b5{top:579.3pt;width:71.5pt;height:143.1pt;background:__B5__;border-radius:0 71.5pt 71.5pt 0}
/* Bayrak: TAM görünür, sağ üstte. Eskiden sayfa dışına taşan dev bir tuvaldi ve
   dört ülkede de kırpık çıkıyordu; artık yüksekliği sabit, genişliği bayrağın kendi
   oranından geliyor. Kaynak: tools/make_wave_flags.py (kamuya açık resmî vektör). */
/* Bayrak: TAM görünür, sağ üstte, gölgeli. Eski kurgu sayfa dışına taşan dev bir
   tuvaldı ve dört ülkede de kırpık çıkıyordu (Almanya'nın fly ucu kesikti, ABD'de
   direk artığı vardı). Artık yükseklik sabit, genişlik bayrağın kendi oranından
   geliyor; kaynak tools/make_wave_flags.py: kamuya açık resmî vektör. */
.cv-flag{position:absolute;left:-161.9pt;top:-220.8pt;width:496.7pt;height:745pt}
/* Toplu katalog: tek bayrak yerine dört bayraklı şerit, sayfanın üst bandında.
   Ölçü tools/make_flags_toplu.py çıktısının TAM boyu (2066x621px, 4 px/pt);
   tuval kırpılmış olduğu için burada verilen kutu bayrakları birebir ölçekler.
   top:-30pt ile şerit üstten hafifçe taşıyor ve 125pt'de bitiyor: pill 140.7pt'de
   başladığı için çakışma yok. */
.cv-flags{position:absolute;left:-18pt;top:-30pt;width:516.5pt;height:155.25pt}
.cv-pill{position:absolute;left:116.3pt;top:140.7pt;width:409pt;height:65.8pt;background:__DARK__;
  border-radius:33pt;font-family:'LS';font-weight:700;font-size:46.8pt;color:#fff;text-align:center;
  line-height:65.8pt}
.cv-title{position:absolute;left:98.7pt;top:210pt;width:430pt;font-family:'LS';font-weight:700;
  font-size:40pt;line-height:44pt;color:__DARK__;text-align:center}
.cv-logoline{position:absolute;left:98.7pt;top:302pt;width:430pt;display:flex;align-items:center;
  justify-content:center;gap:7pt}
.cv-logoline img{width:__LOGOW__pt;height:__LOGOH__pt}
.cv-logoline span{font-family:'OS';font-weight:800;font-size:22pt;color:__DARK__}
.cv-sub{position:absolute;left:98.7pt;top:340pt;width:430pt;text-align:center;font-size:18.6pt;
  line-height:24pt;color:__DARK__;font-weight:400}
.cv-accent{position:absolute;left:112pt;top:428pt;width:104pt;height:104pt;background:__BRIGHT__;
  border-radius:50% 50% 0 50%}
.cv-photo{position:absolute;left:88pt;top:450pt;width:452pt;height:252pt;border-radius:16pt;
  overflow:hidden;transform:rotate(-1.4deg);box-shadow:0 7pt 20pt rgba(0,0,0,.24)}
.cv-photo img{width:100%;height:100%;object-fit:cover;object-position:50% 50%}
/* Toplu katalog kapağı (2 Eylül 2026): bayrak şeridi kalkınca üstte ~140pt ölü
   bant kalıyordu. Blok yukarı çekildi ve fotoğraf 452x339pt'ye büyütüldü: bu ölçü
   kaynağın oranı (1448x1086 = 1,3333) olduğu için kare HİÇ KIRPILMIYOR, dört
   simge de tam görünüyor. Alt sınır 725pt, künye bandı 795pt'de başlıyor. */
.cover-toplu .cv-pill{top:92pt}
.cover-toplu .cv-title{top:162pt}
.cover-toplu .cv-logoline{top:254pt}
.cover-toplu .cv-sub{top:292pt}
.cover-toplu .cv-accent{top:364pt}
.cover-toplu .cv-photo{top:386pt;height:339pt}
/* Kapağın alt bandı boştu; satış belgesinde ilk sayfada iletişim olmalı. */
.cv-cta{position:absolute;left:88pt;top:734pt;width:452pt;display:flex;align-items:center;
  justify-content:center;gap:12pt;font-family:'AR';font-weight:700;font-size:11pt;
  letter-spacing:.04em;color:__DARK__}
.cv-kunye{position:absolute;left:88pt;top:795pt;width:452pt;display:flex;
  justify-content:space-between;gap:10pt}
.kn{display:flex;flex-direction:column;gap:1.5pt}
.knl{font-family:'AR';font-weight:700;font-size:7pt;letter-spacing:.16em;color:#7fd8ca}
.knv{font-family:'OS';font-weight:800;font-size:11.4pt;color:#fff}
.cv-cta i{display:inline-block;width:4.6pt;height:4.6pt;border-radius:50%;background:__BRIGHT__;
  font-style:normal}

/* --- road map --- */
.rmpage .content{position:static}
.rmpage h1.ctr{position:absolute;left:0;top:52pt;width:595.5pt;text-align:center;font-size:26.6pt}
.hl{position:absolute;left:0;top:88pt;width:595.5pt;text-align:center}
.hlin{display:inline-block;background:__ACC__;font-family:'OS';font-weight:800;font-size:17pt;
  line-height:25.5pt;padding:0 10pt;color:__ACCFG__}
.rpath{position:absolute;left:0;top:0;width:595.5pt;height:842.25pt}
.rnum{position:absolute;width:33.2pt;height:33.2pt;border-radius:50%;background:__STEP__;color:#fff;
  font-family:'OS';font-weight:800;font-size:21.1pt;line-height:33.2pt;text-align:center}
.rstep{position:absolute}
.rtitle{font-family:'OS';font-weight:800;font-size:14.6pt;line-height:16.6pt;color:__DARK__}
.rrow{display:flex;align-items:center;gap:7pt;margin-top:5pt}
.rl .rrow{justify-content:flex-start}
.rr .rrow{flex-direction:row-reverse;justify-content:flex-start}
.ricon{height:34pt;width:auto;flex:0 0 auto}
.rtext{font-size:12.6pt;line-height:14.6pt}
.rtext b{font-family:'OS';font-weight:800}

/* --- kapanış sayfası (yalnız toplu katalog) --- */
/* Ülke kataloglarında son sayfa tam sayfa road map; toplu katalogda her ülkenin
   şeması kendi sayfasında MINIMAP olarak durduğu için son sayfa boş kalıyordu.
   Üç adım, road map'in numaralı daire dilini koruyarak dikey diziliyor:
   y=196'dan 640'a kadar sayfayı dolduruyor, altında .contact 686pt'de. */
.clead{position:absolute;left:88pt;top:132pt;width:420pt;text-align:center;
  font-size:13pt;line-height:17.4pt;color:__DARK__}
.clead b{font-family:'OS';font-weight:800}
/* Kart yüksekliği İÇERİĞE bırakılınca (ilk hâli) üç kart 499pt'de bitiyor ve
   .contact'a kadar ~190pt ölü bant kalıyordu. min-height ile kartlar sayfayı
   612pt'ye kadar dolduruyor; metin dikeyde ortalanıyor. */
.cgrid{position:absolute;left:76pt;top:198pt;width:444pt;display:flex;
  flex-direction:column;gap:24pt}
.cls{display:flex;align-items:center;gap:15pt;background:__MINT__;border-radius:13pt;
  padding:16pt 20pt;min-height:122pt}
.clsn{flex:0 0 auto;width:37pt;height:37pt;border-radius:50%;background:__STEP__;color:#fff;
  font-family:'OS';font-weight:800;font-size:22pt;line-height:37pt;text-align:center}
.clst{font-family:'OS';font-weight:800;font-size:16pt;line-height:19pt;color:__DARK__;
  flex:0 0 124pt}
/* 11,4pt denendi: kartlar 122pt yüksekliğinde içi boş duruyordu. Gövde puntosu
   (12,4pt) metni dört satıra çıkarıp kartı dolduruyor. */
.clsx{flex:1 1 auto;font-size:12.4pt;line-height:16.4pt;color:__DARK__}
.clsx b{font-weight:700}

.closing{position:absolute;left:76pt;top:672pt;width:444pt;font-family:'BODY';
  font-size:12.4pt;line-height:16pt;color:__DARK__}
.closing b{font-family:'OS';font-weight:800}
.contact{position:absolute;left:76pt;top:686pt;width:444pt;display:flex;flex-wrap:wrap;
  align-items:flex-start;gap:14pt}
/* 10pt denendi: kataloğun tek dönüşüm cümlesi sayfanın en küçük yazısıydı
   (road map adımları 12,6pt, gövde 12,4pt). */
.cnext{flex:0 0 100%;font-size:12.4pt;line-height:16pt;color:__DARK__;margin-bottom:3pt}
.cta{display:flex;flex-direction:column;gap:3pt;flex:0 0 auto}
.cta span{background:__ACC__;font-family:'OS';font-weight:800;font-size:9.4pt;line-height:15pt;
  padding:0 6pt;color:__ACCFG__;display:table}
.cinfo{flex:1 1 auto;font-size:10pt;line-height:14pt}
.crow{display:flex;align-items:center;gap:4pt}
.crow img{width:10.5pt;height:10.5pt}
.cnum{font-family:'BODY';font-weight:700;font-size:11.6pt;margin-top:1pt}
.globe{width:10.5pt;height:10.5pt;border-radius:50%;border:1.1pt solid __DARK__;
  display:inline-block;position:relative}
.globe:before{content:"";position:absolute;left:3.9pt;top:-.1pt;width:2.2pt;height:10.3pt;
  border:1.1pt solid __DARK__;border-radius:50%}
"""


def main(key="aus"):
    cat = Catalog(key)
    pages = ([cat.page_cover(), cat.page_mentors()]
             + cat.body_pages() + cat.roadmap_pages())
    doc = (f'<!doctype html><html lang="tr"><head><meta charset="utf-8">'
           f'<title>DENTCAMP: {cat.c.name}</title>'
           f'<style>{cat.css()}</style></head><body>{"".join(pages)}</body></html>')
    out = ROOT / f"katalog_{key}.html"
    out.write_text(doc, encoding="utf-8")
    print(f"yazıldı: {out}  ({len(doc)} bayt, {len(pages)} bölme)")


if __name__ == "__main__":
    import sys
    main(sys.argv[1] if len(sys.argv) > 1 else "aus")

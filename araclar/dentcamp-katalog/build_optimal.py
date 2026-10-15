#!/usr/bin/env python3
"""DENTCAMP ülke kataloğu — ölçüm tabanlı sayfalama + PDF derleme.

Sayfa sayısı içerikten çıkar; sabit bölme yoktur. Her bölüm önce çok uzun bir
ölçüm sayfasına basılıp gerçek yüksekliği okunur, sonra 719pt'lik alana sığdığı
kadar bölüm yerleştirilir. Her H1 yeni sayfa açar, hiçbir bölüm ikiye bölünmez.

Akış:
  1. fixed.html -> kapak + mentörler + road map (3 sabit tasarım sayfası)
  2. flow.html  -> gövde, Chrome kendi sayfalayıcısıyla böler
  3. deco.png   -> köşe dekorları, şeffaf zeminle screenshot
  4. birleştir  -> kapak, mentörler, [akan sayfalar], road map + her sayfaya dekor/logo

Kullanım:
  python3 build_optimal.py deu        # tek ülke
  python3 build_optimal.py            # dördü birden
  BODY_PT=13 python3 build_optimal.py aus
"""
import os
import pathlib
import re
import subprocess
import sys

import fitz

import build as B

BODY_PT = float(os.environ.get("BODY_PT", "12.4"))

ROOT = pathlib.Path(__file__).parent
WORK = ROOT / "_work"
OUTDIR = ROOT / "out"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

W, H = 595.5, 842.25
TOP = 66.0                                   # akan sayfa üst boşluğu

DECO_TR = (370.0, 0.0, 595.5, 56.0)          # sağ üst kırpma penceresi
DECO_TR_FAQ = (330.0, 0.0, 595.5, 122.0)     # SSS soru işaretleri daha geniş alan ister
DECO_TR_SM = (420.0, 0.0, 595.5, 44.0)       # road map: küçük dekor
DECO_BL = (0.0, 793.0, 190.0, 842.25)        # sol alt kırpma penceresi
LOGO = fitz.Rect(B.LOGO_X, 797.3, B.LOGO_X + B.LOGO_W, 797.3 + B.LOGO_H)

MAXH = 785.25 - TOP                          # kullanılabilir içerik yüksekliği (719.25pt)
ARTIFACT_BAND = 82.0                         # sayfa dibindeki bu bant artefakt sayılır
MAX_EXTRA = 48.0                             # bölüm arası ek boşluk üst sınırı
H1_ROOM = 235.0        # devam eden bir H1 için sayfada kalması gereken en az yer
H1_LEAD = 22.0         # sayfa ortasında başlayan H1'in üstündeki nefes payı
SPLIT_MIN = 115.0      # bölmeye değecek en az boşluk (pt)
MIN_TAIL  = 170.0      # bölünen bölümün kuyruğu bundan küçükse hiç bölme
# "Başlık tek başına kalmaz" kuralı blok SAYISINA bakıyordu (j>=2) ve
# H1 + alt başlık + tek giriş cümlesi bu kuralı geçiyordu: İngiltere'de
# KAVRAMLAR & TERİMLER başlığı sayfanın alt üçte birinde açılıp terim listesinin
# tamamı sonraki sayfaya geçiyordu. Kural artık başlık olmayan blok sayısına
# bakıyor; salt yükseklik eşiği (200pt denendi) gap dolduran meşru bölmeleri de
# engelliyor ve Almanya'da %48, İngiltere'de %32'lik sayfa açıyordu.
MIN_HEAD_BLOK = 2      # bölünen bölümün başında en az bu kadar başlık-dışı blok olmalı
BASLIK_ON = ('<h1>', '<div class="h1sub">', '<div class="bar">', '<div class="sub">')
# Başlığından koparılmaması gereken görsel bloklar. Mentör grid'i 12 karttan
# oluşan tek bir tablo; paragraf sınırından bölününce başlık ve metin bir sayfada,
# 12 daire bir sonraki sayfada kalıyor ve o sayfanın bölüm adı bile yanlış çıkıyor.
BOLUNMEZ_ISARET = ('<div class="mgrid">',)
EYEBROW_W = 285.0      # bölüm adı etiketinin sığması gereken genişlik (x=76 -> 361pt)
SIL_MIN   = 150.0      # silüet konacak en az boşluk (pt)
SIL_MAX_H = 132.0      # silüet yüksekliği üst sınırı
PAY       = 0.0        # emniyet payı denendi, ABD 16->17 sayfaya çıktı; kapalı
# 95pt denendi ve geri alındı: ölçüm izole gruplara, gerçek yerleşim ise birleşik
# sayfaya bakıyor. Pay büyüyünce aradaki sapma birikip son grubu bir sonraki sayfaya
# itti — dört katalog da birer sayfa uzadı ve %15 dolulukta sayfalar çıktı.
MEASURE_H = 2400.0                           # ölçüm sayfası yüksekliği


def chrome(html, pdf=None, png=None, scale=4):
    cmd = [CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer"]
    if pdf:
        cmd += [f"--print-to-pdf={pdf}", "--virtual-time-budget=8000"]
    else:
        cmd += [f"--screenshot={png}", "--default-background-color=00000000",
                f"--window-size={int(W * 96 / 72)},{int(H * 96 / 72)}",
                f"--force-device-scale-factor={scale}", "--hide-scrollbars",
                "--virtual-time-budget=8000"]
    cmd.append(str(html))
    subprocess.run(cmd, check=True, capture_output=True)


DECO_TAGS = ['<div class="d-tr-circle"></div>', '<div class="d-tr-green"></div>',
             '<div class="d-tr-yellow"></div>', '<div class="d-bl-yellow"></div>',
             '<div class="d-bl-green"></div>', '<div class="d-bl-circle"></div>',
             '<div class="d-faq">?</div>', '<div class="d-faq2">?</div>',
             '<img class="pglogo" src="assets/img/logo.png">']


def strip_deco(html):
    """Sabit sayfalardan dekor/logo çıkarılır — hepsi sonradan tek elden basılacak."""
    for tag in DECO_TAGS:
        html = html.replace(tag, "")
    return html


FLOW_CSS = """
@page{size:595.5pt 842.25pt;margin:66pt 47.5pt 57pt 50pt}
html,body{width:auto}
body{background:transparent}
h1,.h1sub,.bar,.sub{break-after:avoid;page-break-after:avoid}
.box,li{break-inside:avoid;page-break-inside:avoid}
p{orphans:2;widows:2}
h1{margin-top:0}
.pa{break-after:page;page-break-after:always}
body>div:last-child{break-after:auto;page-break-after:auto}
"""

MEASURE_CSS = f"@page{{size:595.5pt {MEASURE_H:g}pt;margin:66pt 47.5pt 57pt 49.7pt}}"

TOKEN = re.compile(
    r'(<h1>.*?</h1>|<div class="h1sub">.*?</div>|<div class="bar">.*?</div>'
    r'|<div class="sub">.*?</div>|<p>.*?</p>|<ul[^>]*>.*?</ul>'
    r'|<div class="box">.*?</div>|<div class="ctaband">.*?</div>'
    # .mcta buraya sonradan eklendi: TOKEN'da olmayan blok sessizce DÜŞÜYOR.
    # Mentör sayfasına konan iletişim şeridi bu yüzden hiç basılmamıştı.
    r'|<div class="mcta">.*?</div>'
    r'|<div class="cards3">.*?<!--/cards3-->'
    r'|<div class="mgrid">.*?<!--/mgrid-->'
    r'|<div class="stats">.*?</div>'
    # Toplu kataloğun iki bloğu. İkisi de yalnız <span> içeriyor, bu yüzden
    # `.*?</div>` ilk kapanışta doğru yerde duruyor.
    r'|<div class="ktab">.*?</div>'
    r'|<div class="mmap">.*?</div>)', re.S)


def group_blocks(html):
    """Blokları bölümlere ayırır: her <h1> ve her bar yeni grup başlatır.
    Grup = sayfa içinde bölünmeyen birim."""
    toks = [t for t in TOKEN.findall(html) if t.strip()]
    groups, cur = [], []
    for t in toks:
        if (t.startswith("<h1>") or t.startswith('<div class="bar">')) and cur:
            groups.append(cur)
            cur = []
        cur.append(t)
    if cur:
        groups.append(cur)
    return [{"html": "".join(g), "h1": g[0].startswith("<h1>")} for g in groups]


def pack(groups, hs, gap=4.0):
    """Her H1 yeni sayfa açar; bar bölümleri sığdığı sürece aynı sayfada kalır.
    Artan boşluk bölüm aralarına dağıtılır — sayfa altında blok beyazlık kalmasın.

    Bir sayfadan uzun bölümler (uzun SSS / kavram listeleri) Chrome tarafından madde
    bazında bölünür; burada kaç sayfa kapladıkları ve son sayfada ne kadar yer
    bıraktıkları hesaba katılır, dikey yayma bunlara uygulanmaz."""
    breaks, pages, cur, used = set(), [], [], 0.0
    extra_pages = 0
    h1_cont = set()                        # aynı sayfada devam eden H1 bölümleri
    for i, g in enumerate(groups):
        h = hs[i]
        if i == 0:
            cur, used = [i], h
            continue
        room = MAXH - PAY - (used + gap)
        if g["h1"]:
            # H1 eskiden KOŞULSUZ yeni sayfa açıyordu. Kısa bölümler arka arkaya
            # gelince sayfanın yarısı boş kalıyordu (ABD s7'de 366pt). Artık H1 da
            # sığıyorsa aynı sayfada devam eder — ama sayfanın dibine sıkışmasın
            # diye en az H1_ROOM kadar yer kalmış olmalı.
            cut = h > room or room < H1_ROOM
        else:
            cut = h > room
        if cut:
            breaks.add(i)
            pages.append(cur)
            cur, used = [i], h
        else:
            if g["h1"]:
                h1_cont.add(i)
                used += H1_LEAD           # devam eden H1'in üstünde nefes payı
            cur.append(i)
            used = used + gap + h
        if h > MAXH:                       # bölüm birden çok sayfaya taşıyor
            spans = int(-(-h // MAXH))
            extra_pages += spans - 1
            used = h - (spans - 1) * MAXH  # son sayfada dolan yükseklik
    pages.append(cur)

    extras = {}
    for pg in pages:
        fit = [i for i in pg if hs[i] <= MAXH]
        if len(fit) < 2 or len(fit) != len(pg):
            continue                        # taşan bölüm varsa yayma yapma
        slack = MAXH - (sum(hs[i] for i in pg) + gap * (len(pg) - 1))
        per = min(slack * 0.9 / (len(pg) - 1), MAX_EXTRA)
        if per > 1.0:
            for i in pg[:-1]:
                extras[i] = per
    for i in h1_cont:                       # H1 devam ediyorsa üstündeki boşluğu garanti et
        extras[i - 1] = max(extras.get(i - 1, 0.0), H1_LEAD)
    return breaks, extras, len(pages) + extra_pages


DECO_VARIANTS = {
    "": '<div class="d-tr-circle"></div><div class="d-tr-green"></div>'
        '<div class="d-tr-yellow"></div>',
    "_faq": '<div class="d-faq">?</div><div class="d-faq2">?</div>',
    "_sm": '<div class="s-tr-circle"></div><div class="s-tr-green"></div>'
           '<div class="s-tr-yellow"></div>',
}
DECO_BOX = {"": DECO_TR, "_faq": DECO_TR_FAQ, "_sm": DECO_TR_SM}


class Builder:
    def __init__(self, key):
        self.cat = B.Catalog(key)
        self.key = key
        # SINIF niteliğiydi: dört ülke aynı süreçte derlendiği için set paylaşılıyor,
        # üstelik id() çöpe giden dict'lerden geri dönüştürülüyordu; bir ülkede
        # bölünemez işaretlenen bir id başka ülkede sağlam bir grubu susturabiliyordu.
        self._bolunmez = set()
        self.css = self.cat.css(BODY_PT)
        self.dir = WORK / key
        self.dir.mkdir(parents=True, exist_ok=True)

    def doc(self, body, extra_css=""):
        return (f'<!doctype html><html lang="tr"><head><meta charset="utf-8">'
                f'<base href="{ROOT.as_uri()}/">'
                f'<style>{self.css}{extra_css}</style></head><body>{body}</body></html>')

    # -- gövde ---------------------------------------------------------------
    def flow_doc(self, groups, breaks, extras=None):
        """breaks: sayfa başlatan grup indeksleri. extras: grup sonrası ek boşluk (pt).
        Sayfa sonu, kıran grubun BİR ÖNCESİNE break-after olarak yazılır — böylece
        sonraki H1'in İ/Ş aksanları önceki sayfanın dibine sızmaz."""
        after = {i - 1 for i in breaks}
        extras = extras or {}
        body = "".join(
            f'<div class="{"pa " if i in after else ""}{g.get("sq", "")}"'
            + (f' style="margin-bottom:{extras[i]:.1f}pt"' if extras.get(i) else "")
            + f'>{g["html"]}</div>'
            for i, g in enumerate(groups))
        return self.doc(body, FLOW_CSS)

    def measure(self, groups):
        """Her grubu kendi (uzun) sayfasına basıp gerçek yüksekliğini ölçer."""
        html = self.flow_doc(groups, set(range(1, len(groups) + 1)))
        html = html.replace("</style>", MEASURE_CSS + "</style>")
        (self.dir / "measure.html").write_text(html, encoding="utf-8")
        chrome(self.dir / "measure.html", pdf=self.dir / "measure.pdf")
        d = fitz.open(self.dir / "measure.pdf")
        hs = []
        for p in d:
            # Sonraki sayfanın H1 aksanları (İ, Ş) bu sayfanın DİBİNE sızıyor; ölçümde yok
            # sayılır, çıktıda redaction ile silinir. Eşik sayfa yüksekliğine göre alınmalı:
            # sabit 760 kullanılırsa ölçüm sayfasında 694pt'den uzun her bölüm kırpılır.
            limit = p.rect.height - ARTIFACT_BAND
            bot = max([l["bbox"][3] for b in p.get_text("dict")["blocks"]
                       for l in b.get("lines", []) if l["bbox"][1] <= limit] or [TOP])
            hs.append(bot - TOP)
        d.close()
        assert len(hs) == len(groups), (
            f"ölçüm {len(hs)} != grup {len(groups)} — bir bölüm ölçüm sayfasına sığmadı")
        return hs

    def squeeze(self, groups, hs):
        """Bir sayfadan AZ taşan bölümleri sıkıştırıp sığdırır.

        Uzun SSS / kavram listeleri sayfayı birkaç puan aşınca, kalan içerik bir
        sonraki sayfaya tek madde olarak düşüyor ve neredeyse boş bir sayfa çıkıyor.
        Burada en hafif yeterli sıkıştırma kademesi uygulanıp yeniden ölçülür."""
        cand = [i for i, h in enumerate(hs) if MAXH < h <= MAXH * 1.16]
        if not cand:
            return hs
        for lvl in ("sq1", "sq2", "sq3"):
            for i in cand:
                groups[i]["sq"] = lvl           # sığanlar bir önceki kademede kalır
            hs = self.measure(groups)
            fixed = [i for i in cand if hs[i] <= MAXH]
            if fixed:
                print(f"  {lvl}: {len(fixed)} bölüm sayfaya sığdırıldı")
            cand = [i for i in cand if hs[i] > MAXH]
            if not cand:
                break
        return hs

    def split_pass(self, groups, hs, tur=8):
        """Sayfaya sığmayan bölümleri paragraf sınırından böler.

        Bölümler eskiden ATOMİKTİ: 350pt'lik bir bölümün ardından 400pt'lik bölüm
        gelince ikisi 719pt'ye sığmıyor, ikincisi komple sonraki sayfaya atlıyor ve
        birinci sayfada 366pt boş kalıyordu (ABD s7, İngiltere s8...).

        Burada sığmayan bölüm, sayfada kalan yere kadar olan kısmı ve devamı olmak
        üzere ikiye ayrılır. Kurallar:
          · başlık (h1/bar) tek başına kalmaz — yanında en az bir blok taşır,
          · devamda en az bir blok kalır, yoksa bölmenin anlamı yok,
          · yalnızca kalan yer SPLIT_MIN'den büyükse bölünür; küçük artıklar için
            sayfa kırmak daha temiz durur.
        """
        # Önce SAYFADAN UZUN bölümler: bunlar Chrome tarafından kesiliyor ve kuyruk
        # çoğu zaman 2-3 satır kalıp neredeyse boş bir sayfa üretiyordu
        # (Avustralya s3). Dengeli ikiye bölünce iki sayfa da doluyor.
        for _ in range(6):
            uzun = [i for i, h in enumerate(hs)
                    if h > MAXH and id(groups[i]) not in self._bolunmez]
            if not uzun:
                break
            i = uzun[0]
            parca = self._bol(groups[i], hs[i] / 2.0, dengeli=True)
            if parca is None:
                self._bolunmez.add(id(groups[i]))
                continue
            groups = groups[:i] + list(parca) + groups[i + 1:]
            hs = self.measure(groups)
            print(f"  sayfadan uzun bölüm {i} dengeli ikiye bölündü")

        for _ in range(tur):
            hedef = self._split_hedef(groups, hs)
            if hedef is None:
                return groups, hs
            i, room = hedef
            parca = self._bol(groups[i], room)
            if parca is None:
                self._bolunmez.add(id(groups[i]))
                continue
            a, b = parca
            groups = groups[:i] + [a, b] + groups[i + 1:]
            hs = self.measure(groups)
            print(f"  bölüm {i} paragraf sınırından bölündü "
                  f"({room:.0f}pt boşluk dolduruldu)")
        return groups, hs

    def _split_hedef(self, groups, hs, gap=4.0):
        """Sayfada en çok boşluk bırakan, bölünebilir bölümü bulur."""
        used = 0.0
        en_iyi = None
        for i, g in enumerate(groups):
            h = hs[i]
            if i == 0:
                used = h
                continue
            room = MAXH - PAY - (used + gap)
            sigmiyor = h > room or (g["h1"] and room < H1_ROOM)
            if sigmiyor:
                if (h > room and room >= SPLIT_MIN and h <= MAXH
                        and id(g) not in self._bolunmez
                        and (en_iyi is None or room > en_iyi[1])):
                    en_iyi = (i, room)
                used = h
            else:
                used = used + gap + h + (H1_LEAD if g["h1"] else 0.0)
        return en_iyi

    @staticmethod
    def _parcala(html):
        """Bölünebilir en küçük parçalar. Uzun SSS/kavram listeleri TEK token
        olduğu için eskiden hiç bölünemiyordu (İngiltere s8'de 357pt boşluk);
        burada <ul> kendi maddelerine ayrılıyor."""
        out = []
        for t in [x for x in TOKEN.findall(html) if x.strip()]:
            m = re.match(r"(<ul[^>]*>)(.*)(</ul>)$", t, re.S)
            if m:
                bas, gov, son = m.groups()
                lis = re.findall(r"<li>.*?</li>", gov, re.S)
                if len(lis) >= 2:
                    out.extend(bas + li + son for li in lis)
                    continue
            out.append(t)
        return out

    @staticmethod
    def _birlestir(parts):
        """Ardışık aynı <ul> parçalarını tek listeye geri toplar."""
        out = []
        for t in parts:
            m = re.match(r"(<ul[^>]*>)(.*)(</ul>)$", t, re.S)
            if m and out:
                p = re.match(r"(<ul[^>]*>)(.*)(</ul>)$", out[-1], re.S)
                if p and p.group(1) == m.group(1):
                    out[-1] = p.group(1) + p.group(2) + m.group(2) + m.group(3)
                    continue
            out.append(t)
        return "".join(out)

    def _bol(self, g, room, gap=4.0, dengeli=False):
        # NOT: <li> seviyesinde bölmeyi İKİ KEZ denedim (kuyruk koruması olmadan ve
        # onunla birlikte); ikisinde de ABD 16->17 sayfaya çıktı ve 690pt boş sayfa
        # oluştu. Liste bölmek toplamda daha kötü sonuç veriyor, token seviyesinde
        # kalıyoruz. KAVRAMLAR sonrası boşluk bu yüzden duruyor.
        #
        # ÜÇÜNCÜ DENEME (21 Ağustos 2026), daraltılmış hâli: yalnız başka türlü
        # bölünemeyen `<ul class="terms">` bölümlerinde, iki yanda en az N madde
        # kalmak koşuluyla. N=3 İngiltere s.10'u %88'den %95'e çıkardı ama ABD
        # s.14'ü %38'e düşürdü; N=2 SSS'nin ilk sayfasını hiç düzeltmedi ve ABD'yi
        # yine bozdu. Net etki eksi, geri alındı. _parcala/_birlestir bu yüzden
        # duruyor ama çağrılmıyor.
        if any(x in g["html"] for x in BOLUNMEZ_ISARET):
            return None
        toks = [t for t in TOKEN.findall(g["html"]) if t.strip()]
        if len(toks) < 3:
            return None
        sub = [{"html": t, "h1": False} for t in toks]
        th = self.measure(sub)
        acc, j = 0.0, 0
        for k, h in enumerate(th):
            if acc + (gap if k else 0) + h > room:
                break
            acc += (gap if k else 0) + h
            j = k + 1
        if j < 2 or j >= len(toks):        # başlık yalnız kalmasın, devam boş olmasın
            return None
        # Kuyruk çok küçükse bölme: tek başına sayfaya düşüp neredeyse boş bir
        # sayfa üretiyor (Avustralya s3'te 3 satır kalmıştı).
        kuyruk = sum(th[j:]) + gap * (len(th) - j - 1)
        if not dengeli and kuyruk < MIN_TAIL:
            return None
        if not dengeli and sum(
                1 for t in toks[:j] if not t.startswith(BASLIK_ON)) < MIN_HEAD_BLOK:
            return None
        a = {"html": "".join(toks[:j]), "h1": g.get("h1", False)}
        b = {"html": "".join(toks[j:]), "h1": False}
        if g.get("sq"):
            a["sq"] = b["sq"] = g["sq"]
        return a, b

    def build_flow(self):
        parts = [pg.split('<div class="content">', 1)[1].rsplit("</div></section>", 1)[0]
                 for pg in self.cat.body_pages()]
        groups = group_blocks("".join(parts))
        hs = self.measure(groups)
        hs = self.squeeze(groups, hs)
        groups, hs = self.split_pass(groups, hs)
        breaks, extras, npages = pack(groups, hs)
        over = [(i, round(h)) for i, h in enumerate(hs) if h > MAXH]
        if over:
            print(f"  sayfadan uzun bölüm(ler) madde bazında bölünüyor: {over}")
        print(f"  {len(groups)} bölüm -> {npages} akan sayfa "
              f"(gövde {BODY_PT:g}pt, en uzun bölüm {max(hs):.0f}/{MAXH:.0f}pt, "
              f"dikey yayma {len(extras)} aralıkta)")
        (self.dir / "flow.html").write_text(
            self.flow_doc(groups, breaks, extras), encoding="utf-8")

    def build_fixed(self):
        rm = [strip_deco(p) for p in self.cat.roadmap_pages()]
        self.n_roadmap = len(rm)
        pages = [strip_deco(self.cat.page_cover())] + rm
        (self.dir / "fixed.html").write_text(self.doc("".join(pages)), encoding="utf-8")

    # -- dekor ---------------------------------------------------------------
    def build_deco(self, tag):
        d = DECO_VARIANTS[tag] + ('<div class="d-bl-yellow"></div><div class="d-bl-green"></div>'
                                  '<div class="d-bl-circle"></div>')
        html = self.doc(f'<section class="page">{d}</section>',
                        "html,body{background:transparent}.page{background:transparent}")
        name = self.dir / f"deco{tag or 'x'}.html"
        name.write_text(html, encoding="utf-8")
        png = self.dir / f"deco{tag or 'x'}.png"
        chrome(name, png=png)
        crop(png, DECO_BOX[tag], self.dir / f"deco_tr{tag}.png")
        crop(png, DECO_BL, self.dir / f"deco_bl{tag}.png")

    # -- birleştir -----------------------------------------------------------
    def run(self):
        print(f"[{self.key}] {self.cat.c.name}")
        self.build_fixed()
        self.build_flow()
        for tag in DECO_VARIANTS:
            self.build_deco(tag)

        chrome(self.dir / "fixed.html", pdf=self.dir / "fixed.pdf")
        chrome(self.dir / "flow.html", pdf=self.dir / "flow.pdf")

        fixed = fitz.open(self.dir / "fixed.pdf")
        flow = fitz.open(self.dir / "flow.pdf")

        out = fitz.open()
        out.insert_pdf(fixed, from_page=0, to_page=0)        # yalnız kapak
        out.insert_pdf(flow)                                  # akan gövde
        out.insert_pdf(fixed, from_page=1,                    # road map (1 ya da 3)
                       to_page=self.n_roadmap)

        flow_pages = range(1, 1 + flow.page_count)
        faq_pages = {i for i, p in enumerate(out) if "SIK SORULAN SORULAR" in p.get_text()}
        # artefakt bandını metin katmanından da sil: yalnız üstünü kapatmak yetmez,
        # kopyalayınca sayfa sonlarında başıboş "İ" çıkar. Dekor bundan SONRA basılır.
        for i in flow_pages:
            out[i].add_redact_annot(fitz.Rect(0, 786.0, W, H))
            out[i].apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE)

        for i, p in enumerate(out):
            if i == 0:
                continue                                     # kapağın kendi dekoru var
            rm_first = out.page_count - self.n_roadmap
            tag = "_sm" if i >= rm_first else ("_faq" if i in faq_pages else "")
            p.insert_image(fitz.Rect(*DECO_BOX[tag]), filename=str(self.dir / f"deco_tr{tag}.png"),
                           keep_proportion=False, overlay=True)
            p.insert_image(fitz.Rect(*DECO_BL), filename=str(self.dir / f"deco_bl{tag}.png"),
                           keep_proportion=False, overlay=True)
            p.insert_image(LOGO, filename=str(ROOT / "assets/img/logo.png"), overlay=True)

        # --- sayfa mobilyası -------------------------------------------------
        # 47 sayfanın hiçbirinde sayfa numarası ya da bölüm adı yoktu; 12 sayfa
        # doğrudan bir pill ile açıldığı için okuyucu hangi bölümde olduğunu
        # bilmiyordu. Altbilgi PyMuPDF ile basılıyor — logo ve dekorla aynı yerde,
        # tek elden; CSS'e dokunmaya gerek yok.
        fontfile = str(ROOT / "assets/fonts/Arimo-Bold.ttf")
        N = out.page_count
        bolum = ""
        # Silüet dolgusu boşluğu kapatmıyor, boşluğu İŞARETLİYOR: ABD'de aynı
        # gökdelen vinyeti beş sayfada, İngiltere'de aynı Big Ben iki sayfada
        # çıkıyordu. En büyük iki boşlukla sınırlandırıldı; kalan boşluklar
        # sayfalama düzeltilerek kapatılır, tekrar eden çizimle örtülmez.
        aday = []
        for i, p in enumerate(out):
            if i == 0 or i >= out.page_count - self.n_roadmap:
                continue
            ys = [l["bbox"][3] for b in p.get_text("dict")["blocks"]
                  for l in b.get("lines", []) if 60 < l["bbox"][3] < 790]
            if ys:
                aday.append((782 - max(ys), i))
        aday.sort(reverse=True)
        # Ardışık sayfa kuralı: ABD'de iki dolgu s.13 ve s.14'e düşünce aynı çizim
        # yan yana iki sayfada görünüyordu ve tekrar en görünür hâline geliyordu.
        SIL_SAYFA = set()
        for _, i in aday:
            if len(SIL_SAYFA) >= 2:
                break
            if all(abs(i - j) > 1 for j in SIL_SAYFA):
                SIL_SAYFA.add(i)
        for i, p in enumerate(out):
            if i == 0:
                continue
            for satir in p.get_text().splitlines():
                t = satir.strip()
                if len(t) > 3 and t == t.upper() and any(c.isalpha() for c in t):
                    bolum = t
                    break
            # Bölüm adı ÜSTTE: alt bantta sol dekor (0-190pt) ve ortadaki logo
            # (222-374pt) yer bırakmıyor. Üstte sağ köşe dekoru 370pt'den başlıyor,
            # sol taraf boş.
            # Eskiden [:42] karakterden kesiliyordu ve marka/bölüm adları yarım
            # basılıyordu ("... X ALMANG", "(CAAPID / ADEA PA", "(ALTERNATİ").
            # Etiket x=76pt'de başlıyor, sağ üst köşe dekoru 370pt'de; ölçüye göre
            # kesmek 42 karakterin (~170pt) çok ötesine izin veriyor.
            ad = re.sub(r"^\d+\.\s*", "", bolum)
            while ad and fitz.get_text_length(
                    ad, fontname="helv", fontsize=6.8) * 1.02 > EYEBROW_W:
                ad = ad[:-1]
            p.insert_text((76, 46), ad, fontname="AR", fontfile=fontfile,
                          fontsize=6.8, color=(0.45, 0.50, 0.53))
            # Bölüm bitip sonraki sığmadığında altta kalan boşluğa ülke silüeti.
            # Sayfayı bomboş bırakmaktansa markaya ait açık tonlu bir çizim durur.
            ys = [l["bbox"][3] for b in p.get_text("dict")["blocks"]
                  for l in b.get("lines", []) if 60 < l["bbox"][3] < 790]
            son = max(ys) if ys else 0
            bosluk = 782 - son
            sil = ROOT / f"assets/img/sil_{self.key}.png"
            if son and bosluk > SIL_MIN and i in SIL_SAYFA and sil.exists():
                yuk = min(bosluk - 34, SIL_MAX_H)
                gen = yuk * 3.0
                if gen > 396:
                    gen, yuk = 396.0, 132.0
                x0 = (W - gen) / 2
                y0 = son + (bosluk - yuk) / 2 + 6
                p.insert_image(fitz.Rect(x0, y0, x0 + gen, y0 + yuk),
                               filename=str(sil), overlay=True)

            etiket = f"SAYFA {i + 1:02d} / {N}"
            gen = fitz.get_text_length(etiket, fontname="helv", fontsize=6.8) * 1.02
            p.insert_text((519.9 - gen, 812), etiket, fontname="AR", fontfile=fontfile,
                          fontsize=6.8, color=(0.45, 0.50, 0.53))

        out.set_metadata({
            "title": (self.cat.c.doc_title
                      or f"DENTCAMP — {self.cat.c.name}'da Diş Hekimliği Kariyeri"),
            "author": "CAMP GROUP",
            "subject": "Denklik ve lisans süreci rehberi — diş hekimliği öğrencileri "
                       "ve diş hekimleri için",
            "keywords": f"DENTCAMP, CAMP GROUP, {self.cat.c.name}, diş hekimliği, "
                        f"denklik, lisans",
            "creator": "DENTCAMP",
        })

        OUTDIR.mkdir(exist_ok=True)
        name = self.cat.c.name.replace("İ", "I").replace("ç", "c")
        pdf = OUTDIR / f"DENTCAMP_{name}_Katalog.pdf"
        out.subset_fonts()
        out.save(pdf, garbage=4, deflate=True)
        print(f"  yazıldı: {pdf.name}  ({pdf.stat().st_size / 1e6:.2f} MB, "
              f"{out.page_count} sayfa)")
        return out.page_count


def crop(png, box, out):
    from PIL import Image
    im = Image.open(png).convert("RGBA")
    sx, sy = im.width / W, im.height / H
    im.crop((int(box[0] * sx), int(box[1] * sy),
             int(box[2] * sx), int(box[3] * sy))).save(out)


def main(keys):
    for k in keys:
        Builder(k).run()


if __name__ == "__main__":
    # Argümansız derleme yalnız DÖRT ÜLKE kataloğunu üretir; toplu katalog
    # ayrıca istenir (`python3 build_optimal.py toplu`).
    args = sys.argv[1:] or list(B.T.COUNTRIES)
    main(args)

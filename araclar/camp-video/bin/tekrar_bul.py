#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Hocanın tekrar ettiği / baştan aldığı yerleri bulur.

(21.09.2026 kararı: "hocanın 'aa baştan aldım' 'tekrar ya' bunları demeden direkt tekrar
ettiği yerleri bul")

İlk derslerde WhatsApp'ta kesim dakikası verilmemiş. Bu yüzden kesilecek yerler transkriptten
çıkarılır. İki dedektör çalışır:

  A) AÇIK İŞARET  — "baştan alıyorum", "pardon", "tekrar" gibi ifadeler
  B) ÖRTÜLÜ TEKRAR — hiçbir şey demeden aynı cümleyi yeniden kurma

B'nin mantığı: bozuk çekimde hoca cümleyi yarıda bırakır ve biraz sonra neredeyse aynı
cümleyi tekrar kurar. Yakın iki metin parçası yüksek benzerlik gösteriyorsa, ÖNCEKİ parça
bozuk çekimdir, sonraki temiz olandır. Kesilecek olan öncekidir.

Bu betik KARAR VERMEZ, ADAY üretir. Kesin sınır sessizlik ölçümünden gelir, son söz kullanıcının.
"""
import argparse
import difflib
import json
import os
import re
import unicodedata

# Açık işaretler: hoca kendi hatasını söylüyor
ACIK = re.compile(
    r"(ba[şs]tan al|ba[şs]a al|ba[şs]tan oku|ba[şs]tan anlat|ba[şs][ıi]n[ıi] al|"
    r"tekrar a[çc][ıi]kla|tekrar anlat|tekrar oku|be[ğg]enmedim|iyi olmad[ıi]|"
    r"tekrar al|tekrar ed|tekrar ya|yeniden al|yeniden ba[şs]l|yeniden anlat|"
    r"pardon|[öo]z[üu]r|yanl[ıi][şs] s[öo]yle|yanl[ıi][şs] dedim|hata yapt|"
    r"bir daha s[öo]yl|[şs]unu kes|buray[ıi] kes|bunu [çc][ıi]kar|kesin buray)", re.I)

# ÖĞRETİCİ TEKRAR KORUMASI — bunlar geçiyorsa KESİLMEZ.
# (21.09.2026 kararı: "hocanın kendi akışta yaptığı ve ders için yapılan tekrarlara dikkat
#  edelim onları kırpma yanlış")
# 21.09.2026 CH28 doğrulaması: örtülü tekrar dedektörünün iki bulgusu da yanlış pozitifti.
# İkisinde de hoca bilerek tekrar ediyordu ve yanında "Dikkat / Önemli / Hatırlayın" vardı.
KORUMA = re.compile(
    r"(dikkat|[öo]nemli|hat[ıi]rlay[ıi]n|unutmay[ıi]n|akl[ıi]n[ıi]zda|not al|"
    r"tekrar ediyorum|tekrarl[ıi]yorum|bir daha s[öo]yl[üu]yorum|[öo]zetle|[öo]zetliyorum|"
    r"tamam m[ıi]|alt[ıi]n[ıi] [çc]iz|vurgulu|s[ıi]navda [çc][ıi]k)", re.I)

# Karşılaştırmada gürültü sayılan dolgu sözcükleri
DOLGU = {"şey", "yani", "işte", "ee", "eee", "aa", "aaa", "ıı", "ııı", "hani", "tamam",
         "evet", "peki", "mesela", "sonra", "şimdi", "de", "da", "ki", "bir"}


def segmentleri_birlestir(seg, bosluk_esigi=0.4, en_fazla_kelime=18, en_fazla_sn=12.0):
    """ASR bazen CUMLE, bazen KELIME donduruyor. Dedektorler cumle bekliyor.

    (22.09.2026, CH15: transkript kelime kelime cikinca tekrar dedektoru tamamen kor
     kaldi; hocanin hiperkalsemiyi bastan anlatmasi hic gorulmedi. Olculdu: 19 dersin
     3'u tamamen kelime bazli, birkaci da sinirda.)

    Ardisik segmentler, aralarindaki bosluk kucukse tek birime toplanir.
    """
    if not seg:
        return seg
    out = []
    for s in seg:
        m = (s.get("metin") or "").strip()
        if not m:
            continue
        if out:
            o = out[-1]
            if (s["bas"] - o["bit"] <= bosluk_esigi
                    and len(o["metin"].split()) < en_fazla_kelime
                    and o["bit"] - o["bas"] < en_fazla_sn):
                o["metin"] = (o["metin"] + " " + m).strip()
                o["bit"] = s["bit"]
                continue
        out.append({"bas": s["bas"], "bit": s["bit"], "metin": m})
    return out


def _sadelestir(metin):
    m = unicodedata.normalize("NFKC", (metin or "")).lower()
    m = m.replace("ı", "i").replace("İ", "i").replace("ş", "s").replace("ğ", "g")
    m = m.replace("ü", "u").replace("ö", "o").replace("ç", "c")
    m = re.sub(r"[^a-z0-9\s]", " ", m)
    return [w for w in m.split() if w not in DOLGU and len(w) > 1]


def _benzerlik(a, b):
    if not a or not b:
        return 0.0
    return difflib.SequenceMatcher(None, a, b).ratio()


def _bosluk_var(bosluklar, t, geri=1.5, en_az=0.6):
    """t anından hemen önce gerçek bir duraklama var mı?

    Gerçek tekrar çekimde hoca durur, toparlanır, yeniden başlar. Öğretici tekrarda
    duraklama yoktur, akış kesintisizdir. Ayırt edici en güçlü sinyal budur.
    """
    for b in bosluklar:
        if b["sure"] >= en_az and (t - geri) <= b["bit"] <= (t + 0.2):
            return True
    return False


def ortulu_tekrarlar(seg, pencere=12.0, esik=0.72, en_az_kelime=5, en_uzun_kesim=45.0,
                     bosluklar=None):
    """Yakın iki parça neredeyse aynıysa, ÖNCEKİ bozuk çekimdir.

    ÖNEMLİ: pencere DAR tutulur. Gerçek tekrar çekimde bozuk parça ile düzeltmesi arka
    arkaya gelir. Pencere genişletilirse hocanın dakikalar sonra aynı kavrama dönmesi
    "tekrar" sanılır ve aradaki gerçek ders içeriği kesilir.
    (21.09.2026 pilotunda yaşandı: 46 sn arayla iki "plak" cümlesi yanlış eşleşti.)"""
    kelime = [_sadelestir(s["metin"]) for s in seg]
    aday = []
    for i in range(len(seg)):
        if len(kelime[i]) < en_az_kelime:
            continue
        for j in range(i + 1, len(seg)):
            if seg[j]["bas"] - seg[i]["bit"] > pencere:
                break
            if len(kelime[j]) < en_az_kelime:
                continue
            if (seg[j]["bas"] - seg[i]["bit"]) > pencere:
                continue
            if (seg[j]["bas"] - seg[i]["bas"]) > en_uzun_kesim:
                continue
            b = _benzerlik(kelime[i], kelime[j])
            if b < esik:
                continue
            # KORUMA 1: aralikta ogretici tekrar isareti varsa dokunma
            araya = " ".join(x["metin"] or "" for x in seg
                             if seg[i]["bas"] - 3.0 <= x["bas"] <= seg[j]["bit"] + 3.0)
            if KORUMA.search(araya):
                continue
            # KORUMA 2: duzeltmenin hemen oncesinde gercek bir duraklama olmali
            if bosluklar is not None and not _bosluk_var(bosluklar, seg[j]["bas"]):
                continue
            if True:
                aday.append({
                    "tur": "ortulu_tekrar", "benzerlik": round(b, 3),
                    "bas": seg[i]["bas"], "bit": seg[j]["bas"],
                    "kesilen": seg[i]["metin"].strip(),
                    "kalan": seg[j]["metin"].strip(),
                    "ara_sn": round(seg[j]["bas"] - seg[i]["bit"], 2),
                })
                break
    return aday


def yeniden_cekim(seg, geri=200.0, esik=0.72, en_az_kelime=4):
    """Hoca 'bastan okuyacagim / tekrar aciklayacagim' deyip yeniden basliyorsa,
    bozuk cekimin TAMAMI kesilir.

    Sinir tahminle degil TEKRARLANAN CUMLE ile bulunur: isaretten sonraki ilk cumle,
    isaretten once soylenmis bir cumleyle ayni ise, kesim o ilk soyleyisten baslar.
    (22.09.2026, CH09: 126 saniyelik bozuk cekim bu sekilde bulundu.)
    """
    out = []
    for i, s in enumerate(seg):
        if not ACIK.search(s.get("metin") or ""):
            continue
        # isaretten sonraki ilk anlamli cumle
        sonraki = None
        for t in seg[i + 1:i + 8]:
            if len(_sadelestir(t.get("metin") or "")) >= en_az_kelime:
                sonraki = t
                break
        if not sonraki:
            continue
        hedef = _sadelestir(sonraki["metin"])
        # ayni cumle daha once soylenmis mi
        for k in range(i, -1, -1):
            if s["bas"] - seg[k]["bas"] > geri:
                break
            if len(_sadelestir(seg[k].get("metin") or "")) < en_az_kelime:
                continue
            if _benzerlik(_sadelestir(seg[k]["metin"]), hedef) >= esik:
                out.append({"tur": "yeniden_cekim", "benzerlik": None,
                            "bas": round(seg[k]["bas"], 2), "bit": round(sonraki["bas"], 2),
                            "kesilen": (s.get("metin") or "").strip(),
                            "kalan": sonraki["metin"].strip(), "ara_sn": None})
                break
    return out


def acik_isaretler(seg, geri=25.0):
    """İşaretin kendisi ve ondan ÖNCEKİ bozuk parça kesilir."""
    aday = []
    for i, s in enumerate(seg):
        m = ACIK.search(s["metin"] or "")
        if not m:
            continue
        cevre = " ".join(x["metin"] or "" for x in seg
                         if s["bas"] - 6.0 <= x["bas"] <= s["bit"] + 6.0)
        if KORUMA.search(cevre) and not re.search(r"(pardon|[öo]z[üu]r|yanl[ıi][şs]|hata)", cevre, re.I):
            continue
        bas = s["bas"]
        for k in range(i - 1, -1, -1):
            if s["bas"] - seg[k]["bas"] > geri:
                break
            bas = seg[k]["bas"]
        aday.append({
            "tur": "acik_isaret", "isaret": m.group(0), "benzerlik": None,
            "bas": bas, "bit": s["bit"],
            "kesilen": " ".join(x["metin"].strip() for x in seg if bas <= x["bas"] < s["bit"])[:400],
            "kalan": (seg[i + 1]["metin"].strip() if i + 1 < len(seg) else ""),
            "ara_sn": None,
        })
    return aday


# LOJISTIK: hoca ders anlatmiyor, is yapiyor (kalem ariyor, slaytta dolasiyor, bekletiyor)
# (22.09.2026 kararı: "hocanin kalemle ugrastigi ders anlatmadigi bir bolum var kesmemisiz")
# Tek basina kelime yetmez: "kalem" 80 kez geciyor, cogu ders anlatirken. Ayirt edici
# isaret, ifadenin YANINDA duraklama olmasi; hoca bir sey ararken susuyor.
LOJISTIK = re.compile(
    r"(kalem\w*\s+(nereye|bulamad|kayb)|bulamad[ıi]m|nereye gitti|nereye gitmi[şs]|"
    r"bir saniye|1 dakika|bir dakika|"
    r"kalemi(mi|mizi)?\s*(al[ıi]yorum|alay[ıi]m|alaca[ğg][ıi]m|alal[ıi]m)|"
    r"sil(elim|eyim)|ge[çc](elim|iyorum) buray|dur(ay[ıi]m|al[ıi]m)|"
    r"[şs]arj|internet|mikrofon|kay[ıi]t sorunu|sesim)", re.I)


def lojistik(seg, bosluklar, en_az_duraklama=0.8, en_uzun=45.0, pencere=12.0):
    """Ders anlatilmayan lojistik anlar: ifade + yanindaki duraklama birlikte kesilir."""
    if not bosluklar:
        return []
    out = []
    for s in seg:
        m = LOJISTIK.search(s.get("metin") or "")
        if not m:
            continue
        yakin = [b for b in bosluklar
                 if s["bas"] - pencere <= b["bas"] <= s["bit"] + pencere
                 and b["sure"] >= en_az_duraklama]
        if not yakin:
            continue
        b = max(yakin, key=lambda x: x["sure"])
        bas = min(s["bas"], b["bas"])
        bit = max(s["bit"], b["bit"])
        # Bolge, KISA laflar ve UZUN bosluklar devam ettikce uzar: hoca hala ugrasiyor.
        # (22.09.2026 kararı: "3.20 de 3.30 arasi da kesilmeli" - yaziyla ugrasma suruyordu)
        i = seg.index(s)
        for t in seg[i + 1:]:
            if t["bas"] - bit > 4.0:
                break
            kelime = len((t.get("metin") or "").split())
            onceki_bosluk = max([x["sure"] for x in bosluklar
                                 if bit - 0.5 <= x["bas"] <= t["bas"] + 0.5] or [0])
            if kelime <= 6 or onceki_bosluk >= 1.5:
                bit = max(bit, t["bit"])
            else:
                break
        if bit - bas > en_uzun:
            bit = bas + en_uzun
        out.append({"tur": "lojistik", "benzerlik": None, "bas": round(bas, 2),
                    "bit": round(bit, 2), "kesilen": (s.get("metin") or "").strip(),
                    "kalan": "", "ara_sn": None, "duraklama": round(b["sure"], 2)})
    return out


def konu_yeniden_baslama(seg, bosluklar, en_az_duraklama=1.5, pencere=45.0,
                         en_az_ortak=2, en_uzun=75.0):
    """Hoca ayni KONUYU farkli kelimelerle bastan anlatiyorsa yakalar.

    (22.09.2026 kararı: "dakika yazmayanlarda tum kaydi asiri detayli incelemelisin")
    CH15'te hoca hiperkalsemiyi anlatip durdu ve bastan anlatti; kelimeler farkliydi,
    kelime benzerligi dusuk kaldi, klasik tekrar dedektoru goremedi.

    Yontem: duraklamadan SONRAKI cumle, duraklamadan ONCEKI blokta gecen NADIR terimleri
    yeniden kullaniyorsa bu bir yeniden baslamadir. Nadir terim = derste az gecen kelime,
    yani konuya ozgu olan. Sik gecen kelimeler (ve, bir, hasta...) sayilmaz.
    """
    from collections import Counter
    if not seg or not bosluklar:
        return []
    sayac = Counter()
    for s in seg:
        sayac.update(set(_sadelestir(s.get("metin") or "")))
    nadir = {k for k, v in sayac.items() if v <= 6 and len(k) >= 6}
    out = []
    for b in bosluklar:
        if b["sure"] < en_az_duraklama:
            continue
        sonra = next((x for x in seg if x["bas"] >= b["bit"] - 0.2), None)
        if not sonra:
            continue
        onceki = [x for x in seg if b["bas"] - pencere <= x["bas"] < b["bas"]]
        if not onceki:
            continue
        sonra_t = set(_sadelestir(sonra.get("metin") or "")) & nadir
        if len(sonra_t) < en_az_ortak:
            continue
        for k in range(len(onceki)):
            blok = onceki[k:]
            blok_t = set()
            for x in blok:
                blok_t |= set(_sadelestir(x.get("metin") or "")) & nadir
            ortak = sonra_t & blok_t
            if len(ortak) >= en_az_ortak and (b["bit"] - blok[0]["bas"]) <= en_uzun:
                cevre = " ".join(x.get("metin") or "" for x in blok) + " " + (sonra.get("metin") or "")
                if KORUMA.search(cevre):
                    break
                out.append({"tur": "konu_yeniden", "benzerlik": None,
                            "bas": round(blok[0]["bas"], 2), "bit": round(b["bit"] - 0.15, 2),
                            "kesilen": (blok[0].get("metin") or "")[:160],
                            "kalan": (sonra.get("metin") or "")[:160], "ara_sn": None,
                            "ortak_terim": sorted(ortak)[:5]})
                break
    return out


def olu_zaman(sessizlik_yolu, en_az=4.0, birak=0.35):
    """Uzun ölü zaman: hiç konuşma yok, sadece sessizlik.

    Bazı kesimler SÖZEL DEĞİL. CH28'de WhatsApp "12. dakika" demiş; transkriptte ne bir
    işaret ne bir tekrar var, ama 12:59'da 7,93 sn sessizlik duruyor. Hoca susmuş.
    (21.09.2026 doğrulaması.)

    Sessizlik tamamen silinmez, iki yana `birak` kadar nefes bırakılır.
    Konuşma kesilmediği için bu kesimler güvenlidir, ayrı onay gerektirmez.
    """
    import os
    if not os.path.exists(sessizlik_yolu):
        return []
    ses = json.load(open(sessizlik_yolu))
    toplam = ses.get("toplam_sure", 0)
    out = []
    for b in ses.get("bosluk", []):
        if b["sure"] < en_az:
            continue
        if b["bas"] < 2.0 or b["bit"] > toplam - 2.0:
            continue          # bas/son kirpmasi ayri is
        bas, bit = b["bas"] + birak, b["bit"] - birak
        if bit - bas < 0.5:
            continue
        out.append({"tur": "olu_zaman", "benzerlik": None, "bas": round(bas, 2),
                    "bit": round(bit, 2), "kesilen": "(konusma yok, %.1f sn sessizlik)" % b["sure"],
                    "kalan": "", "ara_sn": None})
    return out


# Otonom karar: hangi aday ONAYSIZ uygulanir?
# (21.09.2026 kararı: "hayır önüme getirme hepsini bana aşırı yorucu olur sen dikkat et")
# İlke: EMİN DEĞİLSEN KESME. Birkaç saniyelik takılmayı bırakmak, gerçek ders içeriğini
# kesmekten kat kat iyidir. Atlanan aday sessizce geçilir, sayısı raporda görünür.
KESIN_HATA = re.compile(r"(pardon|[öo]z[üu]r|yanl[ıi][şs]|hata yapt|kar[ıi][şs]t[ıi]r|"
                        r"ba[şs]tan al|ba[şs]a al|ba[şs]tan oku|ba[şs]tan anlat|"
                        r"ba[şs][ıi]n[ıi] al|tekrar a[çc][ıi]kla|tekrar anlat|tekrar oku|"
                        r"be[ğg]enmedim|iyi olmad[ıi]|yeniden ba[şs]l|yeniden anlat)", re.I)


def karar_ver(a, en_uzun_konusma=40.0, en_uzun_olu=30.0, benzerlik_esigi=0.80,
              en_uzun_ortulu=25.0):
    """Her aday icin 'uygula' ya da 'atla' + gerekce."""
    t, sure = a["tur"], a["bit"] - a["bas"]
    if t == "lojistik":
        if sure > 45.0:
            return "atla", "lojistik kesim cok uzun (%.1f sn)" % sure
        return "uygula", "ders anlatilmiyor (duraklama %.1f sn)" % (a.get("duraklama") or 0)
    if t == "olu_zaman":
        if sure > en_uzun_olu:
            return "atla", "olu zaman cok uzun (%.1f sn), elle bakilmali" % sure
        return "uygula", "konusma yok"
    if t == "konu_yeniden":
        if sure > 75.0:
            return "atla", "konu yeniden baslama cok uzun (%.1f sn)" % sure
        return "uygula", "ayni konu bastan anlatildi (ortak terim: %s)" % ", ".join(a.get("ortak_terim") or [])
    if t == "yeniden_cekim":
        if sure > 200.0:
            return "atla", "yeniden cekim cok uzun (%.1f sn)" % sure
        return "uygula", "hoca bastan aldi, bozuk cekim kesildi"
    if t == "acik_isaret":
        if not KESIN_HATA.search(a.get("kesilen", "") + " " + str(a.get("isaret", ""))):
            return "atla", "isaret kesin hata bildirmiyor"
        if sure > en_uzun_konusma:
            return "atla", "kesim cok uzun (%.1f sn)" % sure
        return "uygula", "hocanin kendi bildirdigi hata"
    if t == "ortulu_tekrar":
        b = a.get("benzerlik") or 0
        if b < benzerlik_esigi:
            return "atla", "benzerlik dusuk (%.2f)" % b
        if sure > en_uzun_ortulu:
            return "atla", "kesim cok uzun (%.1f sn)" % sure
        return "uygula", "duraklamali birebir tekrar (%.2f)" % b
    if t == "karma":
        # Birden fazla dedektor ayni yeri isaretlediyse kanit daha guclu demektir
        if sure > 45.0:
            return "atla", "karma kesim cok uzun (%.1f sn)" % sure
        return "uygula", "birden fazla dedektor ayni yeri isaretledi"
    return "atla", "bilinmeyen tur"


def birlestir(adaylar, bosluk=1.0):
    adaylar = sorted(adaylar, key=lambda a: a["bas"])
    out = []
    for a in adaylar:
        if out and a["bas"] <= out[-1]["bit"] + bosluk:
            o = out[-1]
            if a["bit"] > o["bit"]:
                o["bit"] = a["bit"]
                o["kalan"] = a["kalan"]
            if "yeniden_cekim" in (o["tur"], a["tur"]):
                o["tur"] = "yeniden_cekim"      # en guclu kanit kazanir
            elif o["tur"] != a["tur"]:
                o["tur"] = "karma"
            o["kesilen"] = (o["kesilen"] + " / " + a["kesilen"])[:600]
        else:
            out.append(dict(a))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("transkript")
    ap.add_argument("--out", default=None)
    ap.add_argument("--esik", type=float, default=0.72)
    ap.add_argument("--pencere", type=float, default=12.0,
                    help="bozuk parca ile duzeltmesi arasindaki en fazla bosluk (sn)")
    ap.add_argument("--en-uzun-kesim", type=float, default=45.0)
    ap.add_argument("--sessizlik", default=None, help="edit/sessizlik.json yolu")
    ap.add_argument("--olu-esik", type=float, default=4.0)
    ap.add_argument("--en-uzun", type=float, default=90.0,
                    help="bundan uzun aday supheli sayilir, bayraklanir")
    a = ap.parse_args()

    d = json.load(open(a.transkript))
    seg = []
    for p in d.get("pencere", []):
        seg.extend(p.get("segment", []))
    seg.sort(key=lambda s: s["bas"])
    ham_sayi = len(seg)
    seg = segmentleri_birlestir(seg)
    if ham_sayi != len(seg):
        print("segment birlestirme: %d -> %d" % (ham_sayi, len(seg)))
    print("segment: %d  ·  sure: %.1f dk" % (len(seg), (seg[-1]["bit"] / 60.0) if seg else 0))

    sy = a.sessizlik or os.path.join(os.path.dirname(a.transkript), "sessizlik.json")
    bosluklar = json.load(open(sy))["bosluk"] if os.path.exists(sy) else None
    adaylar = birlestir(yeniden_cekim(seg)
                        + acik_isaretler(seg)
                        + ortulu_tekrarlar(seg, a.pencere, a.esik,
                                           en_uzun_kesim=a.en_uzun_kesim,
                                           bosluklar=bosluklar)
                        + olu_zaman(sy, a.olu_esik)
                        + lojistik(seg, bosluklar or [])
                        + konu_yeniden_baslama(seg, bosluklar or []))
    for x in adaylar:
        x["sure"] = round(x["bit"] - x["bas"], 2)
        x["supheli"] = x["sure"] > a.en_uzun
        x["karar"], x["gerekce"] = karar_ver(x)
    uygulanan = [x for x in adaylar if x["karar"] == "uygula"]
    atlanan = [x for x in adaylar if x["karar"] == "atla"]
    toplam = sum(x["sure"] for x in uygulanan)

    out = a.out or a.transkript.replace(".json", "_tekrar.json")
    json.dump({"aday": adaylar, "uygulanan": uygulanan, "toplam_sn": round(toplam, 1)},
              open(out, "w"), ensure_ascii=False, indent=1)

    print("aday: %d  ·  UYGULANAN: %d (%.1f sn)  ·  atlanan: %d"
          % (len(adaylar), len(uygulanan), toplam, len(atlanan)))
    for x in adaylar:
        print("\n  [%02d:%05.2f -> %02d:%05.2f] %.1f sn · %s · %s (%s)"
              % (x["bas"] // 60, x["bas"] % 60, x["bit"] // 60, x["bit"] % 60, x["sure"],
                 x["tur"], x["karar"].upper(), x["gerekce"]))
        print("     KESILEN: %s" % x["kesilen"][:160])
        print("     KALAN  : %s" % (x["kalan"] or "")[:160])
    print("\n->", out)


if __name__ == "__main__":
    main()

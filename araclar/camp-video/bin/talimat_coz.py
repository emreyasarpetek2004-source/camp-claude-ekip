#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""WhatsApp kesim talimatlarını çözümler.

KARAR VERMEZ, ADAY ÜRETİR. Kesin sınır sessizlik ölçümünden gelir,
son onay kullanıcıdadır. Burada yalnız "hangi dakikada bir şey var" sorusu cevaplanır.

Gerçek külliyattan çıkarılmış kalıplar (21.09.2026 taraması, 56 kayıt):
    "26.dk ve 33.dk edit"      -> 26, 33
    "4-21-25-40-51-56 Edit"    -> tire AYIRAÇ, aralık değil
    "12 ve 15 edit"            -> çıplak sayılar dakika
    "5.dakika 50.sn edit"      -> bileşik, 5*60+50
    "16dk edit"                -> bitişik
    "40.dk edit saniyelik"     -> kusur ~1 sn uzunlukta
    "24.dakika şarjım bitiyordu ... edite gerek yok"  -> yine de 24 işaretlenir
    "20.dakika kitap hatası"   -> KESİM DEĞİL, kitap hatası notu
    "18 ve 25 gibi ... tam emin değilim"  -> belirsiz işaretlenir
    "dakika yazamadım"         -> tam tarama gerekir
"""
import json
import re
import sys

# Kesim niyeti bildiren kelimeler
KESIM = re.compile(r"\b(edit\w*|edt|revize\w*|revizyon|revision)\b", re.I)
# Kesim DEĞİL: kitap hatası ayrı dosyaya işlenir, slayta/videoya dokunulmaz
KITAP_HATASI = re.compile(r"kitap\s+hata\w*", re.I)
# Güvenilirlik düşürenler
BELIRSIZ = re.compile(r"(emin de[ğg]ilim|yazamad[ıi]m|gibi bi|san[ıi]r[ıi]m|tam hat[ıi]rlam)", re.I)
TARAMA_GEREK = re.compile(r"(dakika\s+yazamad[ıi]m|dakikalar[ıi]n[ıi]\s+yazamad|nerede oldu[ğg]unu bilmiyorum)", re.I)
# "51. Ders" gibi ders numarasını dakika sanmamak için
DERS_NO = re.compile(r"\b\d{1,3}\s*\.?\s*ders\b", re.I)
# "1 saat 15 dakika", "1-1.5 saate", "2-3 saate" -> KAYIT SÜRESİ, kesim değil
SURE = re.compile(r"\b\d{1,2}(?:[.,]\d)?\s*(?:-\s*\d{1,2}(?:[.,]\d)?\s*)?saat\w*"
                  r"(?:\s*\d{1,3}\s*\.?\s*(?:dk|dakika)\w*)?", re.I)
# Kesim kelimesi geçmese de sorun bildiren ifadeler
SORUN = re.compile(r"(b[öo]l[üu]nd[üu]\w*|durakla\w*|hata ver\w*|yar[ıi]da kesti|tak[ıi]ld\w*|"
                   r"m[üu]dahale|araya girdi|[şs]arj[ıi]m bitiyor)", re.I)

# Bileşik: 5.dakika 50.sn
BILESIK = re.compile(r"\b(\d{1,3})\s*\.?\s*(?:dk|dakika)\w*\s+(\d{1,2})\s*\.?\s*(?:sn|saniye)\w*", re.I)
# Tekil: 26.dk / 16dk / 20.dakika / 9. Dakika / 17çdk (klavye kaymasi, 04.10.2026)
DK = re.compile(r"\b(\d{1,3})\s*\.?\s*[çÇ]?\s*(?:dk|dakika)\w*", re.I)
# mm:ss
SAAT = re.compile(r"\b(\d{1,2}):(\d{2})(?::(\d{2}))?\b")
# Çıplak sayı listesi: "4-21-25-40-51-56", "12 ve 15", "2, 19, 26"
CIPLAK = re.compile(r"\b\d{1,3}\b")


def _maskele(metin):
    """Dakika sanılmaması gereken parçaları metinden düşürür."""
    m = re.sub(r"https?://\S+", " ", metin)
    m = re.sub(r"@\d+", " ", m)            # mention id'leri
    m = DERS_NO.sub(" ", m)                # "51. Ders"
    m = SURE.sub(" ", m)                   # "1 saat 15 dakika" = kayıt süresi
    m = re.sub(r"\b\d{1,2}[./]\d{1,2}(?:[./]\d{2,4})?\b", " ", m)  # tarih
    return m


def coz(metin):
    """Tek mesajdan aday kesim noktaları çıkarır."""
    ham = metin or ""
    if KITAP_HATASI.search(ham):
        return {"tur": "kitap_hatasi", "noktalar": [], "not": ham.strip(), "belirsiz": False}

    _m = _maskele(ham)
    if not (KESIM.search(ham) or DK.search(_m) or SAAT.search(_m)
            or BELIRSIZ.search(ham) or TARAMA_GEREK.search(ham) or SORUN.search(ham)):
        return None

    m = _maskele(ham)
    noktalar = []
    tuketilen = []

    for x in BILESIK.finditer(m):
        noktalar.append({"saniye": int(x.group(1)) * 60 + int(x.group(2)), "kaynak": x.group(0)})
        tuketilen.append(x.span())
    for x in SAAT.finditer(m):
        if any(a <= x.start() < b for a, b in tuketilen):
            continue
        g = x.groups()
        sn = int(g[0]) * 3600 + int(g[1]) * 60 + int(g[2] or 0) if g[2] else int(g[0]) * 60 + int(g[1])
        noktalar.append({"saniye": sn, "kaynak": x.group(0)})
        tuketilen.append(x.span())
    for x in DK.finditer(m):
        if any(a <= x.start() < b for a, b in tuketilen):
            continue
        noktalar.append({"saniye": int(x.group(1)) * 60, "kaynak": x.group(0)})
        tuketilen.append(x.span())

    # Çıplak sayılar: yalnız kesim kelimesi varsa ve henüz tüketilmemişse
    if KESIM.search(ham) or BELIRSIZ.search(ham) or SORUN.search(ham):
        for x in CIPLAK.finditer(m):
            if any(a <= x.start() < b for a, b in tuketilen):
                continue
            n = int(x.group(0))
            if 1 <= n <= 240:
                noktalar.append({"saniye": n * 60, "kaynak": x.group(0)})

    gor, tekil = set(), []
    for p in sorted(noktalar, key=lambda p: p["saniye"]):
        if p["saniye"] in gor:
            continue
        gor.add(p["saniye"])
        tekil.append(p)

    return {
        "tur": "kesim" if tekil else "belirsiz",
        "noktalar": tekil,
        "not": ham.strip(),
        "belirsiz": bool(BELIRSIZ.search(ham)),
        "tam_tarama_gerek": bool(TARAMA_GEREK.search(ham)),
        "saniyelik": bool(re.search(r"saniyelik", ham, re.I)),
    }


def kayit_coz(kayit):
    """Bir Loom kaydının tüm talimat mesajlarını birleştirir."""
    sonuc = {"noktalar": [], "kitap_hatasi": [], "belirsiz": False,
             "tam_tarama_gerek": False, "saniyelik": False, "ham": []}
    for t in kayit.get("talimat_ham", []):
        c = coz(t.get("metin", ""))
        if not c:
            continue
        sonuc["ham"].append(t["metin"].strip())
        if c["tur"] == "kitap_hatasi":
            sonuc["kitap_hatasi"].append(c["not"])
            continue
        sonuc["noktalar"].extend(c["noktalar"])
        sonuc["belirsiz"] |= c["belirsiz"]
        sonuc["tam_tarama_gerek"] |= c["tam_tarama_gerek"]
        sonuc["saniyelik"] |= c["saniyelik"]
    gor, tekil = set(), []
    for p in sorted(sonuc["noktalar"], key=lambda p: p["saniye"]):
        if p["saniye"] in gor:
            continue
        gor.add(p["saniye"])
        tekil.append(p)
    sonuc["noktalar"] = tekil
    return sonuc


if __name__ == "__main__":
    yol = sys.argv[1] if len(sys.argv) > 1 else "takip/ders_kayitlari.json"
    d = json.load(open(yol))
    ozet = {"kesimli": 0, "kesimsiz": 0, "belirsiz": 0, "tarama": 0, "kitap": 0}
    for k in d["kayit"]:
        c = kayit_coz(k)
        k["talimat_cozum"] = c
        if c["noktalar"]:
            ozet["kesimli"] += 1
        else:
            ozet["kesimsiz"] += 1
        ozet["belirsiz"] += bool(c["belirsiz"])
        ozet["tarama"] += bool(c["tam_tarama_gerek"])
        ozet["kitap"] += bool(c["kitap_hatasi"])
    with open(yol, "w") as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
    print("Cozum:", ozet)
    for k in d["kayit"]:
        c = k["talimat_cozum"]
        if c["noktalar"] or c["kitap_hatasi"] or c["tam_tarama_gerek"]:
            dk = ", ".join("%d:%02d" % (p["saniye"] // 60, p["saniye"] % 60) for p in c["noktalar"])
            bayrak = "".join(["?" if c["belirsiz"] else "", "T" if c["tam_tarama_gerek"] else "",
                              "K" if c["kitap_hatasi"] else "", "s" if c["saniyelik"] else ""])
            print("  %s %-8s %-2s %s" % (k["link_tarih"][:10], k["loom_vid"][:8], bayrak, dk or "-"))

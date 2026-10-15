#!/usr/bin/env python3
"""CAMP GROUP — metin hümanize denetçisi (stdlib-only).

Makinenin kesin yakalayabildiği şeyleri yakalar: literal AI kalıpları, ritim
ölçümleri ve marka kuralları. Yargı gerektiren kısım (somutluk, ton) SKILL.md'de,
ajanın işi.

Kullanım:
    python3 humanize_check.py metin.txt
    python3 humanize_check.py metin.txt --marka dentcamp
    cat caption.txt | python3 humanize_check.py - --marka dentcamp

Çıkış kodu: bulgu varsa 1, temizse 0.
"""
import argparse
import re
import sys
import unicodedata

# ---------------------------------------------------------------- AI kalıpları
# (etiket, regex, açıklama)  — hepsi marka-bağımsız
AI_KALIPLARI = [
    ("KALIP-AÇILIŞ", r"(?:^|[.!?]\s|\n)\s*(Günümüzde|Günümüz dünyasında|Bilindiği üzere|"
     r"Hepimizin bildiği gibi|Bildiğiniz gibi|Gelin (?:birlikte )?bakalım|İşte detaylar|"
     r"Bu (?:yazıda|gönderide) ele alacağız|Sizler için derledik)",
     "AI'nin klasik açılış kalıbı. Tek somut gerçekle aç."),

    ("ŞİŞİRME-SIFAT", r"\b(önemli bir|kritik bir|hayati bir|eşsiz|benzersiz|kapsamlı bir|"
     r"titizlikle|özenle|profesyonel bir şekilde|en iyi şekilde|mükemmel bir)\b",
     "İçi boş nitelik. Ya somutla ya sil."),

    ("ANTİTEZ", r"\bsadece\b[^.!?\n]{0,80}\bdeğil\b[^.!?\n]{0,20}\baynı zamanda\b",
     "'sadece X değil, aynı zamanda Y' — en güçlü AI işareti. Cümleyi böl."),

    ("BÜROKRATİK-ÇEKİM", r"\w+(?:mektedir|maktadır|mekte|makta)\b",
     "Resmî yazışma çekimi. Düz zamana çevir: 'yürütülmektedir' → 'yürütüyoruz'."),

    ("NOMİNAL-ŞİŞME", r"\b(\w+(?:ılması|ilmesi|ulması|ülmesi|lanması|lenmesi)) "
     r"(?:gerek\w+|sağlan\w+|önem\w+)",
     "İsim-fiil yığını. Doğrudan fiil kullan."),

    ("MEKANİK-BAĞLAÇ", r"(?:^|\n)\s*(Ayrıca|Bunun yanı sıra|Öte yandan|Sonuç olarak|"
     r"Özetle|Kısacası|Diğer taraftan|Bununla birlikte)[,\s]",
     "Satır başı mekanik bağlaç. At; cümleler zaten sıralı."),

    ("DUYGUSAL-YÜKSELTME", r"\b(hayalleriniz\w*|hayalinizdeki|yolculuğunuz\w*|"
     r"başarı hikayeniz\w*|kariyer yolculuğu\w*|hedeflerinize giden yol)\b",
     "Motivasyon edebiyatı. CAMP GROUP markalarında yasak."),

    ("RETORİK-SORU", r"\bPeki[,\s][^?\n]{0,60}\?\s*(?:Şu demek|Cevap|İşte|Çünkü)\b",
     "'Peki …? Şu demek:' ikilisi AI kalıbı. Soruyu sil, cevabı yaz."),

    ("TOPLAYICI-KAPANIŞ", r"\b(Unutmayın ki|Unutmayınız|büyük önem taşı\w+|"
     r"göz ardı edilmemelidir|dikkat edilmesi gereken en önemli)\b",
     "Klişe kapanış. Kapanışta somut çağrı olsun."),
]

# Somut sayı yoksa boş niceleyici sayılır
BOŞ_NİCELEYİCİ = re.compile(r"\b(birçok|pek çok|çeşitli|bazı|birtakım|birkaç)\b", re.I)

# ---------------------------------------------------------------- marka profilleri
# Marka adı yazımı BÜYÜK/küçük harfe duyarlıdır — o desenler `cs=True` ile işaretlenir
# ve IGNORECASE olmadan çalışır. Aksi hâlde doğru yazılmış "DENTCAMP" kendi
# yasak listesine takılıyordu.
MARKALAR = {
    "dentcamp": {
        "site": "dentcamp.com.tr",
        "cta": "🌐 dentcamp.com.tr 📞 +90 552 000 78 38",
        "yasak": [
            ("MARKA-YAZIM", r"\b(Dentcamp|DentCamp|dentCamp|Camp Group|Camp group|Medcamp|MedCamp|Almango)\b",
             "Marka adları her yerde BÜYÜK: DENTCAMP, CAMP GROUP, MEDCAMP, ALMANGO.", True),
            ("YANLIŞ-TERİM", r"\b(aday(?:ı|ın|a|lar\w*)?|rezidansl\w+)\b",
             "'aday' → 'diş hekimi'/'danışan'; 'rezidanslık' → 'asistanlık'.", False),
            # Olumsuzlanmış kullanım vaat değil, dürüstlüktür — markanın kendi
            # cümlesi: "otomatik bir iş garantisi vermez". Bu yüzden ardından
            # olumsuzlama gelen eşleşmeler elenir.
            ("VAAT", r"\b(kolayca|garanti\w*|kesinlikle geçer\w*)\b(?![^.!?\n]{0,30}"
             r"\b(?:verm[ei]\w*|yok|değil|olmuyor|olmaz|sunmuyor|sunmaz)\b)|"
             r"(?:^|\s)(kolay|hemen)(?=[\s,.!?])(?![^.!?\n]{0,30}\b(?:değil|olmuyor|olmaz)\b)",
             "Vaat sözü. 'kolay/garanti/hemen' yasak (olumsuzlanmışsa sorun değil).", False),
            ("YANLIŞ-HAT", r"(552\s?253\s?0\s?337|552\s?253\s?03\s?37|info@|@camp2aus|@camp2uk)",
             "DENTCAMP CTA'sında e-posta ve başka marka hattı olmaz.", False),
            # HİZMET-ABARTMA kuralı 18.08.2026'da KALDIRILDI (kullanıcı kararı).
            # Gerekçe: "süreçleri uçtan uca planlıyor ve yönetiyoruz" dili artık
            # standart caption kalıbının parçası. Önceki "mentörlük veririz,
            # süreci üstlenmeyiz" sınırı pazarlama yüzeyinde uygulanmıyor.
            ("YASAKLI-OLGU", r"(1 (?:Kasım|Temmuz) 2026)|"
             r"(%\s?25[^.\n]{0,40}(?:sınav|yazılı|pratik))",
             "Yasaklı olgu (Almanya yürürlük tarihi / %25'in hangi sınava ait olduğu).", False),
        ],
    },
    "auscamp": {"site": "auscamp.com.tr", "cta": None, "yasak": [
        ("MARKA-YAZIM", r"\b(Auscamp|AusCamp|Camp Group|Camp group|Medcamp|MedCamp)\b",
         "Marka adları BÜYÜK: AUSCAMP, CAMP GROUP, MEDCAMP.", True),
    ]},
    "ukcamp": {"site": "ukcamp.com.tr", "cta": None, "yasak": [
        ("MARKA-YAZIM", r"\b(Ukcamp|UkCamp|Camp Group|Camp group|Medcamp|MedCamp)\b",
         "Marka adları BÜYÜK: UKCAMP, CAMP GROUP, MEDCAMP.", True),
    ]},
}

# URL, hashtag ve @handle içindeki yazımlar marka kuralına takılmaz — onlar
# teknik dizge, marka adı değil. Denetimden önce maskelenir.
MASKE = re.compile(r"(https?://\S+|\b\w+\.(?:com|com\.tr|org|net)\b|#\w+|@\w+)")


def emoji_say(metin):
    """Görünen emoji sayısı.

    Bayraklar (🇩🇪) iki 'regional indicator' kod noktasından oluşur; tek emoji
    sayılmaları gerekir. Varyasyon seçicisi (U+FE0F) ve ZWJ birleşimleri de
    ayrı sayılmaz — yoksa 4 bayraklı bir gönderi 8 emoji gibi görünüyordu.
    """
    n, i, N = 0, 0, len(metin)
    RI = range(0x1F1E6, 0x1F200)  # regional indicator
    while i < N:
        o = ord(metin[i])
        if o in RI:
            i += 2 if i + 1 < N and ord(metin[i + 1]) in RI else 1
            n += 1
            continue
        if unicodedata.category(metin[i]) == "So" or 0x1F300 <= o <= 0x1FAFF:
            n += 1
            i += 1
            # varyasyon seçici + ZWJ ile birleşen parçaları tek emoji say
            while i < N and (ord(metin[i]) == 0xFE0F or ord(metin[i]) == 0x200D):
                i += 2 if ord(metin[i]) == 0x200D and i + 1 < N else 1
            continue
        i += 1
    return n


def cumleler(metin):
    duz = re.sub(r"[•\-•]\s*", "", metin)
    parts = [c.strip() for c in re.split(r"(?<=[.!?])\s+|\n+", duz) if c.strip()]
    return [p for p in parts if len(p.split()) >= 3]


def maddeler(metin):
    """Madde satırları.

    Klasik işaretlerin (•, 📌, ✅, numara) yanında **emoji ile başlayan satırlar**
    da madde sayılır: dört ülkeli gönderilerde satırlar ülke bayrağıyla açılıyor
    ve bunlar madde olarak görülmezse emoji izni hatalı biçimde 3'e düşüyordu.
    """
    out = []
    for satir in metin.split("\n"):
        s = satir.strip()
        if not s:
            continue
        m = re.match(r"^(?:[•\-•]|📌|✅|\d+[.)])\s*(.+)$", s)
        if m:
            out.append(m.group(1).strip())
            continue
        # emoji ile başlayan satır (bayrak dâhil) — madde kabul edilir
        o = ord(s[0])
        if 0x1F1E6 <= o < 0x1F200 or unicodedata.category(s[0]) == "So" or 0x1F300 <= o <= 0x1FAFF:
            govde = s.lstrip("".join(ch for ch in s[:4] if not ch.isalnum())).strip()
            if govde:
                out.append(govde)
    return out


def denetle(metin, marka=None):
    bulgular = []

    def ekle(tip, etiket, sat, kanit, oneri):
        bulgular.append((tip, etiket, sat, kanit.strip()[:90], oneri))

    satir_no = lambda i: metin[:i].count("\n") + 1

    for etiket, desen, oneri in AI_KALIPLARI:
        for m in re.finditer(desen, metin, re.I | re.M):
            ekle("AI", etiket, satir_no(m.start()), m.group(0), oneri)

    for m in BOŞ_NİCELEYİCİ.finditer(metin):
        pencere = metin[max(0, m.start() - 60):m.end() + 60]
        if not re.search(r"\d", pencere):
            ekle("AI", "BOŞ-NİCELEYİCİ", satir_no(m.start()), m.group(0),
                 "Somut sayı ver ya da ifadeyi sil.")

    # --- ritim ---
    cs = cumleler(metin)
    if len(cs) >= 4:
        uz = [len(c.split()) for c in cs]
        ort = sum(uz) / len(uz)
        yayilim = max(uz) - min(uz)
        if yayilim <= 4:
            ekle("RİTİM", "TEK-DÜZE-CÜMLE", 0, f"{len(cs)} cümle, uzunluk {min(uz)}-{max(uz)}",
                 f"Cümleler aynı boyda (ort {ort:.0f} kelime). Kısa-uzun-kısa yap; "
                 "bir tane çok kısa cümle ekle.")

    ms = maddeler(metin)
    if len(ms) >= 3:
        ilk = [m.split()[0].lower().strip(":,") for m in ms if m.split()]
        art = 1
        for i in range(1, len(ilk)):
            art = art + 1 if ilk[i] == ilk[i - 1] else 1
            if art >= 3:
                ekle("RİTİM", "PARALEL-MADDE", 0, f"'{ilk[i]}' ile başlayan {art} madde",
                     "Ardışık maddeler aynı kelimeyle başlıyor. Simetriyi boz.")
                break

    # Emoji sınırı sabit sayı değil, yapıya bağlı: her madde başına bir + bayrak,
    # web ve telefon için üç tane. Sabit ≤6 kuralı, madde sayısı arttığında
    # işlevsel emojileri hatalı biçimde işaretliyordu.
    e = emoji_say(metin)
    izin = len(ms) + 3
    if e > izin:
        ekle("RİTİM", "EMOJİ-FAZLA", 0, f"{e} emoji ({len(ms)} madde → izin {izin})",
             "Süs emoji var. Emoji yalnız madde başında, ülke bayrağında ve CTA'da olsun.")

    # --- marka ---
    if marka:
        p = MARKALAR.get(marka)
        if not p:
            sys.exit(f"HATA: bilinmeyen marka '{marka}'. Seçenekler: {', '.join(MARKALAR)}")
        # Maskeleme: URL/hashtag/@handle aynı uzunlukta '·' ile değiştirilir, böylece
        # satır ve karakter konumları bozulmaz.
        maskeli = MASKE.sub(lambda m: "·" * len(m.group(0)), metin)
        for etiket, desen, oneri, buyuk_kucuk_duyarli in p["yasak"]:
            bayrak = re.M if buyuk_kucuk_duyarli else (re.I | re.M)
            for m in re.finditer(desen, maskeli, bayrak):
                ekle("MARKA", etiket, satir_no(m.start()), m.group(0), oneri)
        if p["cta"] and p["cta"] not in metin and "🌐" in metin:
            ekle("MARKA", "CTA-BLOĞU", 0, "CTA bloğu birebir değil",
                 f"Sabit blok: {p['cta']}")

        # Mentör sayısı: kullanıcı 18.08.2026'da 13 olarak güncelledi (önceki 11).
        # Sayı yasak değil, ama YANLIŞ sayı yazmak yasak. Yazıyla ve rakamla ara.
        if marka == "dentcamp":
            # "bir" listede YOK: Türkçede "bir mentör" sayı değil, belirsiz
            # artikeldir ("bir mentör size eşlik ediyor"). Rakamla yazılan 1 yakalanır.
            YAZI = {"iki": 2, "üç": 3, "dört": 4, "beş": 5, "altı": 6,
                    "yedi": 7, "sekiz": 8, "dokuz": 9, "on": 10, "on bir": 11,
                    "onbir": 11, "on iki": 12, "on üç": 13, "onüç": 13}
            for m in re.finditer(r"\b(\d{1,3}|on bir|onbir|on iki|on üç|onüç|iki|üç|dört|beş|"
                                 r"altı|yedi|sekiz|dokuz|on)\s+(?:farklı\s+)?ment[öo]r",
                                 metin, re.I):
                ham = m.group(1).lower()
                sayi = int(ham) if ham.isdigit() else YAZI.get(ham)
                if sayi is not None and sayi != 13:
                    ekle("MARKA", "MENTÖR-SAYISI", satir_no(m.start()), m.group(0),
                         "DENTCAMP mentör sayısı 13'tür (18.08.2026). "
                         "Farklı sayı yazma; isim listesi hâlâ izin gerektirir.")
    return bulgular


def main():
    ap = argparse.ArgumentParser(description="CAMP GROUP metin hümanize denetçisi")
    ap.add_argument("dosya", help="metin dosyası, '-' ile stdin")
    ap.add_argument("--marka", choices=sorted(MARKALAR), help="marka kurallarını da uygula")
    a = ap.parse_args()

    metin = sys.stdin.read() if a.dosya == "-" else open(a.dosya, encoding="utf-8").read()
    bulgular = denetle(metin, a.marka)

    if not bulgular:
        print("TEMİZ — makine bulgusu yok.")
        print("Not: somutluk ve ton yargı işidir; SKILL.md'deki ritim kurallarını elle geçir.")
        return 0

    print(f"{len(bulgular)} BULGU\n")
    for tip in ("MARKA", "AI", "RİTİM"):
        grup = [b for b in bulgular if b[0] == tip]
        if not grup:
            continue
        print(f"── {tip} ({len(grup)})")
        for _, etiket, sat, kanit, oneri in grup:
            yer = f"satır {sat}" if sat else "genel"
            print(f"  [{etiket}] {yer}: {kanit}")
            print(f"      → {oneri}")
        print()
    return 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""DENTCAMP renk kimliği ve ülke tanımları.

Geometri AUSCAMP Specialist Pathway kataloğuyla birebir aynı; değişen yalnız renk.
AUSCAMP yeşil/sarı ikilisinin yerini DENTCAMP koyu turkuaz / parlak turkuaz alır.

Ülke rengi KULLANILMIYOR (kullanıcı kararı, Ağustos 2026): dört katalog da yalnız DENTCAMP
paletiyle basılıyor. Daha önce bayrak renkleri dar yüzeylerde (köşe dairesi, road map
bandı, CTA çipleri) aksan olarak kullanılıyordu; artık hepsi parlak turkuaz.
`Country.accent` alanı geriye dönük uyumluluk için duruyor ama CSS'te okunmuyor.
"""
from dataclasses import dataclass, field

# --- DENTCAMP markası (dentcamp.svg'den) ------------------------------------
DARK = "#005b52"       # AUSCAMP #016531 yerine
BRIGHT = "#00d9bd"     # AUSCAMP #ffcb00 yerine
MINT = "#d6f2ed"       # kutu zemini, mentör isim pill'i (AUSCAMP #d4ece0 yerine)

# kapak sol kenarındaki blob ailesi (AUSCAMP'te sarı tonlarıydı)
BLOB = {
    "b1": "#00d9bd",
    "b2": "#a8f2e7",
    "b3": "#00b49e",
    "b4": "#6fe8d6",
    "b5": "#00d9bd",
}

STEP = "#2bbfa8"       # road map numaralı daireleri (AUSCAMP #78ac4b yerine)
PATH = (43, 191, 168)  # road map kesikli yol — yeşil grafiğin boyanacağı renk

# --- ortak iletişim bilgisi -------------------------------------------------
SITE = "dentcamp.com.tr"
INSTAGRAM = "dentcamptr"
CAMP_LINE = "+90 552 000 78 38"


# Ülke rengi yerine geçen ortak aksan (bkz. modül başlığı)
ACCENT = BRIGHT
ACCENT_FG = DARK


@dataclass
class Country:
    key: str
    name: str            # "Almanya"
    accent: str          # ARTIK KULLANILMIYOR — tasarımda ortak ACCENT geçerli
    accent_fg: str       # ARTIK KULLANILMIYOR
    flag: str            # assets/img/ içindeki bayrak dosyası
    cover_photo: str     # assets/img/ içindeki kapak fotoğrafı
    lines: list = field(default_factory=list)   # road map iletişim bloğu ek hattı
    # PDF künyesindeki başlık. Ülke katalogları "<Ülke>'da Diş Hekimliği Kariyeri"
    # kalıbını kullanıyor; toplu katalogda ülke adı olmadığı için başlık elle verilir.
    doc_title: str = ""


COUNTRIES = {
    "aus": Country("aus", "Avustralya", "#00247d", "#ffffff",
                   "bayrak_aus.png", "kapak_aus.jpg"),
    "uk":  Country("uk",  "İngiltere",  "#c8102e", "#ffffff",
                   "bayrak_uk.png",  "kapak_uk.jpg"),
    "usa": Country("usa", "ABD",        "#0a3161", "#ffffff",
                   "bayrak_usa.png", "kapak_usa.jpg"),
    "deu": Country("deu", "Almanya",    "#ffce00", "#005b52",
                   "bayrak_deu.png", "kapak_deu.jpg"),
}


# Toplu katalog: dört ülkeyi tek belgede anlatan 10 sayfalık özet. Ayrı sözlükte
# duruyor çünkü COUNTRIES üzerinde dönen her yer (argümansız derleme, qa_check
# paleti) yalnız DÖRT ülke kataloğunu kastediyor.
EXTRA = {
    "toplu": Country("toplu", "Toplu", ACCENT, ACCENT_FG,
                     # Kapak kartı: dört ülkenin tek kadrajda birleştiği kare
                     # (tools/make_cover_toplu_foto.py). Dört panelli eski kart
                     # kapak_toplu.jpg olarak duruyor, kullanılmıyor.
                     "bayrak_toplu.png", "kapak_toplu_foto.jpg",
                     doc_title="DENTCAMP — Yurt Dışında Diş Hekimliği Kariyeri "
                               "(Almanya · Avustralya · İngiltere · ABD)"),
}

# Derlenebilir her katalog. COUNTRIES'in kendisi DEĞİŞMEDEN kalmalı.
ALL = {**COUNTRIES, **EXTRA}

#!/usr/bin/env python3
"""Road map ikon setini üretir — düz çizgi, tek dil, DENTCAMP renkleri.

Neden: eski set gri takım elbiseli klipart insanlardı. Diş hekimliği kataloğunda
"iş adamı" ikonu yanlış duruyordu, ayrıca ABD'de aynı ikon tek sayfada üç kez
tekrar ediyordu. Ton analizinde ikonların %10-45'i nötr griydi; çevredeki düz
turkuaz grafiklerle aynı dilde değildi.

Burada her adım kendi konusuna ait bir ikon alır. Hepsi aynı çizgi kalınlığı,
aynı köşe yarıçapı ve aynı iki renkle çizilir.

    python3 tools/make_icons.py

Çıktı: assets/img/ic_<ad>.png  (şeffaf zemin, 4x çözünürlük)
"""
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "img"
WORK = ROOT / "_work" / "icons"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

DARK = "#005b52"
BRIGHT = "#00d9bd"
SIZE = 96          # mantıksal boyut (px); 4x basılır -> 384px

# Her ikon: viewBox 0 0 48 48, stroke tabanlı. Dolgu gerektiren vurgular BRIGHT.
ICONS = {
    # belge / dosya değerlendirmesi
    "belge": """
      <path d="M12 5h16l8 8v30a2 2 0 0 1-2 2H12a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2z"/>
      <path d="M28 5v9h8"/>
      <path d="M16 24h16M16 31h16M16 38h10"/>""",
    # yazılı sınav / soru kâğıdı
    "sinav": """
      <path d="M9 8h30a2 2 0 0 1 2 2v28a2 2 0 0 1-2 2H9a2 2 0 0 1-2-2V10a2 2 0 0 1 2-2z"/>
      <path d="M14 18h9M14 25h9M14 32h9"/>
      <circle cx="32" cy="21" r="5" class="acc"/>
      <path d="M29.6 21.2l1.8 1.8 3.2-3.6" class="on"/>""",
    # pratik sınav / diş
    "dis": """
      <path d="M24 9c-4-3-11-3-13 2-2 5 0 10 1 15 1 4 1 9 3 12 2 2 4 1 5-2l3-8c.4-1 1.6-1 2 0
               l3 8c1 3 3 4 5 2 2-3 2-8 3-12 1-5 3-10 1-15-2-5-9-5-13-2z"/>""",
    # dil yeterliliği / konuşma
    "dil": """
      <path d="M8 12a3 3 0 0 1 3-3h26a3 3 0 0 1 3 3v16a3 3 0 0 1-3 3H21l-9 8v-8h-1a3 3 0 0 1-3-3z"/>
      <path d="M17 20h14M17 14h9"/>""",
    # lisans / kayıt kartı
    "lisans": """
      <path d="M7 11h34a2 2 0 0 1 2 2v22a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V13a2 2 0 0 1 2-2z"/>
      <circle cx="17" cy="21" r="4.5"/>
      <path d="M10 32c1.5-3.5 4-5 7-5s5.5 1.5 7 5"/>
      <path d="M29 18h9M29 24h9M29 30h6"/>""",
    # denklik başvurusu / mühür
    "muhur": """
      <circle cx="24" cy="19" r="12"/>
      <path d="M18.5 19.5l3.6 3.6 7.4-7.6" class="on"/>
      <path d="M17 30l-3 13 10-4 10 4-3-13"/>""",
    # takvim / randevu
    "takvim": """
      <path d="M9 11h30a2 2 0 0 1 2 2v27a2 2 0 0 1-2 2H9a2 2 0 0 1-2-2V13a2 2 0 0 1 2-2z"/>
      <path d="M7 21h34M16 6v9M32 6v9"/>
      <rect x="15" y="27" width="7" height="7" rx="1.5" class="acc"/>""",
    # seyahat / uçuş
    "ucak": """
      <path d="M6 26l36-13-6 15 4 12-7-3-4 6-3-9-12-4z"/>""",
    # mentör / birebir rehberlik
    "mentor": """
      <circle cx="18" cy="16" r="6"/>
      <path d="M7 39c1.5-7 6-10.5 11-10.5S27.5 32 29 39"/>
      <circle cx="34" cy="19" r="4.5" class="acc2"/>
      <path d="M28.5 36c1-4.5 3-7 5.5-7s4.5 2.5 5.5 7"/>""",
    # maliyet / bütçe
    "butce": """
      <path d="M24 6v36"/>
      <path d="M32 14c-1.5-2.5-4.5-4-8-4-4.5 0-8 2.4-8 6s3 5 8 6 8 2.4 8 6-3.5 6-8 6
               c-3.5 0-6.5-1.5-8-4"/>""",
}

TPL = """<!doctype html><meta charset="utf-8">
<style>html,body{{margin:0;padding:0;background:transparent}}
svg{{display:block;width:{s}px;height:{s}px}}
g{{fill:none;stroke:{dark};stroke-width:2.6;stroke-linecap:round;stroke-linejoin:round}}
.acc{{fill:{bright};stroke:{bright}}}
.acc2{{fill:none;stroke:{bright}}}
.on{{stroke:#fff;stroke-width:2.8}}
</style>
<svg viewBox="0 0 48 48"><g>{body}</g></svg>"""


def build():
    WORK.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    for ad, body in ICONS.items():
        html = WORK / f"{ad}.html"
        html.write_text(TPL.format(s=SIZE, dark=DARK, bright=BRIGHT, body=body),
                        encoding="utf-8")
        png = OUT / f"ic_{ad}.png"
        subprocess.run([
            CHROME, "--headless", "--disable-gpu", f"--screenshot={png}",
            f"--window-size={SIZE},{SIZE}", "--force-device-scale-factor=4",
            "--default-background-color=00000000", "--hide-scrollbars",
            "--virtual-time-budget=4000", str(html)],
            check=True, capture_output=True)
        print(f"ic_{ad}.png")


if __name__ == "__main__":
    build()

#!/usr/bin/env python3
"""Ülkeye özgü silüetleri üretir — sayfa altında kalan boşluğu dolduran filigran.

Bazı sayfalarda bölüm bitiyor ama sonraki bölüm sığmıyor; altta 150-360pt boşluk
kalıyor (Almanya s8, Avustralya s6). Sayfayı bomboş bırakmak yerine oraya ülkeye
ait açık tonlu bir silüet konuyor.

Silüetler elle çiziliyor: hazır kaynaklar ya lisanslı ya da baskı için yetersiz.
Hepsi tek renk, düz, DENTCAMP nane tonunda; metnin önüne geçmeyecek kadar açık.

    python3 tools/make_siluet.py

Çıktı: assets/img/sil_<ulke>.png  (şeffaf zemin, 3x çözünürlük)
"""
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "img"
WORK = ROOT / "_work" / "siluet"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

W, H = 900, 300
RENK = "#bfe6de"          # nane tonu; gövde metninin çok altında kalır

# viewBox 0 0 300 100 — zemin çizgisi y=92
SILUET = {
    # Brandenburg Kapısı: basamak, 6 sütun, saçaklık, quadriga kütlesi
    "deu": """
      <rect x="86" y="24" width="128" height="9"/>
      <rect x="92" y="33" width="116" height="5"/>
      <rect x="90" y="38" width="120" height="4"/>
      <rect x="98" y="42" width="7" height="50"/>
      <rect x="114" y="42" width="7" height="50"/>
      <rect x="130" y="42" width="7" height="50"/>
      <rect x="163" y="42" width="7" height="50"/>
      <rect x="179" y="42" width="7" height="50"/>
      <rect x="195" y="42" width="7" height="50"/>
      <rect x="86" y="88" width="128" height="4"/>
      <rect x="140" y="12" width="20" height="12" rx="2"/>
      <rect x="136" y="9" width="28" height="4" rx="2"/>""",
    # Sydney Opera Binası: kabuklar + rıhtım
    "aus": """
      <path d="M60 92c0-26 16-46 38-52-10 14-14 32-14 52z"/>
      <path d="M96 92c0-30 18-52 44-59-12 16-17 36-17 59z"/>
      <path d="M138 92c0-34 21-59 50-67-14 18-20 41-20 67z"/>
      <path d="M186 92c0-24 14-42 34-48-9 13-12 29-12 48z"/>
      <rect x="52" y="88" width="180" height="4"/>""",
    # ABD: kule silüetleri (skyline)
    "usa": """
      <rect x="74" y="52" width="20" height="40"/>
      <rect x="100" y="38" width="16" height="54"/>
      <rect x="106" y="22" width="4" height="16"/>
      <rect x="122" y="60" width="18" height="32"/>
      <path d="M148 92V34l11-16 11 16v58z"/>
      <rect x="157" y="10" width="4" height="8"/>
      <rect x="176" y="46" width="20" height="46"/>
      <rect x="202" y="58" width="16" height="34"/>
      <rect x="60" y="88" width="170" height="4"/>""",
    # İngiltere: Big Ben ve köprü ayakları
    "uk": """
      <rect x="138" y="30" width="24" height="62"/>
      <rect x="134" y="24" width="32" height="7"/>
      <rect x="141" y="33" width="18" height="16" rx="2"/>
      <path d="M139 24l11-16 11 16z"/>
      <rect x="148" y="2" width="4" height="7"/>
      <rect x="70" y="66" width="12" height="26"/>
      <rect x="218" y="66" width="12" height="26"/>
      <path d="M82 78c22-14 44-20 68-20s46 6 68 20" fill="none"
            stroke="%s" stroke-width="4"/>
      <rect x="58" y="88" width="184" height="4"/>""",
}

TPL = """<!doctype html><meta charset="utf-8">
<style>html,body{{margin:0;padding:0;background:transparent}}
svg{{display:block;width:{w}px;height:{h}px}}
g{{fill:{renk}}}</style>
<svg viewBox="0 0 300 100"><g>{body}</g></svg>"""


def build():
    WORK.mkdir(parents=True, exist_ok=True)
    for ad, body in SILUET.items():
        if "%s" in body:
            body = body % RENK
        html = WORK / f"{ad}.html"
        html.write_text(TPL.format(w=W, h=H, renk=RENK, body=body), encoding="utf-8")
        png = OUT / f"sil_{ad}.png"
        subprocess.run([
            CHROME, "--headless", "--disable-gpu", f"--screenshot={png}",
            f"--window-size={W},{H}", "--force-device-scale-factor=3",
            "--default-background-color=00000000", "--hide-scrollbars",
            "--virtual-time-budget=4000", str(html)],
            check=True, capture_output=True)
        print(f"sil_{ad}.png")


if __name__ == "__main__":
    build()

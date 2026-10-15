#!/usr/bin/env python3
"""Road map için 6. ikon: onay mührü (rozet + kurdele).

AUSCAMP'ten devralınan ikon havuzu 5 taneydi; ABD ve İngiltere road map'i 6 adımlı
olduğu için bir adım başka bir adımın ikonunu tekrar ediyordu. Bu ikon o boşluğu
kapatıyor. Stil mevcutlarla aynı: koyu turkuaz kontur, beyaz gövde, orta turkuaz
aksan, beyaz tik, hafif gölge.
"""
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "img" / "icon_onay_muhru.png"
TMP = ROOT / "tools" / "_tmp"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

DARK = "#1e5f57"      # mevcut ikonların kontur rengi
MID = "#4bb3a8"       # aksan dolgu
W, H = 360, 300

SVG = f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 300" width="{W}" height="{H}">
  <defs>
    <filter id="sh" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="6" stdDeviation="6" flood-color="#0b3b36"
                    flood-opacity="0.18"/>
    </filter>
  </defs>
  <g filter="url(#sh)">
    <!-- arka belge (derinlik için, kalkan ikonundaki gibi soluk) -->
    <rect x="42" y="26" width="150" height="196" rx="14"
          fill="#dceeeb" stroke="{DARK}" stroke-width="9"/>
    <rect x="76" y="20" width="150" height="196" rx="14"
          fill="#ffffff" stroke="{DARK}" stroke-width="9"/>
    <g stroke="{MID}" stroke-width="11" stroke-linecap="round">
      <line x1="104" y1="66" x2="196" y2="66"/>
      <line x1="104" y1="102" x2="196" y2="102"/>
      <line x1="104" y1="138" x2="166" y2="138"/>
    </g>

    <!-- kurdele uçları -->
    <path d="M212 214 L212 288 L246 262 L280 288 L280 214 Z"
          fill="{MID}" stroke="{DARK}" stroke-width="9" stroke-linejoin="round"/>

    <!-- tırtıklı mühür -->
    <g transform="translate(246,166)">
      <circle r="82" fill="{MID}" stroke="{DARK}" stroke-width="9"/>
      <circle r="60" fill="none" stroke="#ffffff" stroke-width="7" opacity="0.75"/>
      <path d="M-30 4 L-8 27 L32 -22" fill="none" stroke="#ffffff" stroke-width="17"
            stroke-linecap="round" stroke-linejoin="round"/>
    </g>
  </g>
</svg>
"""


def main():
    TMP.mkdir(parents=True, exist_ok=True)
    html = TMP / "seal.html"
    html.write_text(
        '<!doctype html><meta charset="utf-8">'
        '<style>*{margin:0;padding:0}html,body{background:transparent}</style>'
        f"<body>{SVG}</body>", encoding="utf-8")
    subprocess.run([CHROME, "--headless", "--disable-gpu", f"--screenshot={OUT}",
                    "--default-background-color=00000000", "--hide-scrollbars",
                    f"--window-size={W},{H}", "--force-device-scale-factor=2",
                    "--virtual-time-budget=4000", str(html)],
                   check=True, capture_output=True)
    print(f"yazıldı: {OUT.name}")


if __name__ == "__main__":
    main()

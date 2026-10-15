#!/usr/bin/env python3
"""DENTCAMP kataloğu mekanik denetim.

Gözle bakmadan yakalanabilecek her şeyi ölçer: taşma, düşük çözünürlük, yarım boş
sayfa, yer tutucu kalıntısı, palet dışı renk, eksik iletişim bloğu, gömülmemiş font.
Estetik ve satış dili bu scriptin işi değil — onu denetçi agent gözle yapar.

Kullanım:
  python3 qa_check.py                       # out/ altındaki dört katalog
  python3 qa_check.py out/DENTCAMP_ABD_Katalog.pdf
  python3 qa_check.py --json                # makine okunur çıktı
"""
import glob
import json
import pathlib
import sys

import fitz

import theme as T

ROOT = pathlib.Path(__file__).parent

W, H = 595.5, 842.25
SAFE = (49.7, 66.0, 547.8, 786.0)      # gövde metninin kalması gereken alan
MIN_DPI = 200                          # baskı için alt sınır
THIN_PAGE = 0.45                       # kullanılabilir yüksekliğin altındaki doluluk
USABLE_H = 719.25

PLACEHOLDERS = ["[metin bekleniyor", "[Bölüm metni", "[Soru]", "[Cevap]",
                "İÇERİK BEKLENİYOR", "TBD", "Lorem"]


def hexc(v):
    return "#%06x" % v


def palette():
    ok = {T.DARK, T.BRIGHT, T.MINT, T.STEP, "#ffffff", "#fcfcfc", "#000000"}
    ok |= {c.accent for c in T.COUNTRIES.values()}
    ok |= set(T.BLOB.values())
    return {c.lower() for c in ok}


def check(path):
    doc = fitz.open(path)
    name = pathlib.Path(path).name
    out = {"katalog": name, "sayfa": doc.page_count, "bulgular": []}
    add = lambda kat, sayfa, msg: out["bulgular"].append(
        {"kategori": kat, "sayfa": sayfa, "mesaj": msg})

    pal = palette()
    full_text = []

    for i, page in enumerate(doc, 1):
        txt = page.get_text()
        full_text.append(txt)

        # --- taşma: gövde metni güvenli alanın dışına çıkmış mı ---------------
        # Son sayfa (road map) bilerek geniş yerleşim kullanır; muaf.
        for b in ([] if i == doc.page_count else page.get_text("dict")["blocks"]):
            for l in b.get("lines", []):
                x0, y0, x1, y1 = l["bbox"]
                if x0 < SAFE[0] - 2 or x1 > SAFE[2] + 2 or y1 > SAFE[3] + 2:
                    s = "".join(sp["text"] for sp in l["spans"])[:48]
                    if s.strip():
                        add("TAŞMA", i,
                            f"satır güvenli alan dışında ({x0:.0f},{y0:.0f})–"
                            f"({x1:.0f},{y1:.0f}): \"{s}\"")

        # --- görsel çözünürlüğü ------------------------------------------------
        for img in page.get_images(full=True):
            xref = img[0]
            try:
                rects = page.get_image_rects(xref)
            except Exception:
                continue
            info = doc.extract_image(xref)
            for r in rects:
                if r.width < 20:
                    continue
                dpi = info["width"] / (r.width / 72.0)
                if dpi < MIN_DPI:
                    add("ÇÖZÜNÜRLÜK", i,
                        f"görsel {info['width']}x{info['height']}px, "
                        f"{r.width:.0f}x{r.height:.0f}pt yerleşimde ~{dpi:.0f} dpi "
                        f"(sınır {MIN_DPI})")

        # --- yarım boş sayfa ---------------------------------------------------
        lines = [l for b in page.get_text("dict")["blocks"] for l in b.get("lines", [])]
        body = [l for l in lines if l["bbox"][1] > 60 and l["bbox"][3] < 790]
        if body and i > 2:
            bot = max(l["bbox"][3] for l in body)
            fill = (bot - 66.0) / USABLE_H
            if fill < THIN_PAGE:
                add("BOŞ SAYFA", i,
                    f"sayfa doluluğu %{fill*100:.0f} (metin {bot:.0f}pt'de bitiyor)")

        # --- yer tutucu kalıntısı ---------------------------------------------
        for ph in PLACEHOLDERS:
            if ph.lower() in txt.lower():
                add("YER TUTUCU", i, f"\"{ph}\" metinde duruyor")

        # --- palet dışı renk ---------------------------------------------------
        for d in page.get_drawings():
            for key in ("fill", "color"):
                c = d.get(key)
                if not c:
                    continue
                h = "#%02x%02x%02x" % tuple(int(round(v * 255)) for v in c)
                if h.lower() not in pal and d.get("rect") and d["rect"].width > 8:
                    add("RENK", i, f"palet dışı {h} ({key})")

    # --- belge geneli ----------------------------------------------------------
    joined = "\n".join(full_text)
    if T.SITE not in joined:
        add("İLETİŞİM", 0, f"site adresi ({T.SITE}) hiçbir sayfada yok")
    if T.CAMP_LINE.replace(" ", "") not in joined.replace(" ", ""):
        add("İLETİŞİM", 0, f"telefon ({T.CAMP_LINE}) hiçbir sayfada yok")

    # CTA yalnız son sayfadaysa satış açısından zayıf
    cta_pages = [i for i, t in enumerate(full_text, 1)
                 if T.CAMP_LINE.replace(" ", "") in t.replace(" ", "")]
    if len(cta_pages) <= 1:
        add("SATIŞ", 0,
            f"iletişim/CTA yalnız {len(cta_pages)} sayfada (sayfa {cta_pages}); "
            f"okuyucu kataloğun ortasında karar verirse geri dönmek zorunda")

    # gömülü font
    fonts = {f[3] for p in doc for f in p.get_fonts(full=True)}
    if any(not f for f in fonts):
        add("FONT", 0, "adsız font referansı var")
    for f in doc:
        for fn in f.get_fonts(full=True):
            if fn[1] == "n/a":
                add("FONT", 0, f"gömülü olmayan font: {fn[3]}")
                break

    doc.close()
    return out


def main(paths, as_json=False):
    reports = [check(p) for p in paths]
    if as_json:
        print(json.dumps(reports, ensure_ascii=False, indent=2))
        return 0
    total = 0
    for r in reports:
        print(f"\n=== {r['katalog']}  ({r['sayfa']} sayfa)")
        if not r["bulgular"]:
            print("  TEMİZ")
            continue
        by = {}
        for b in r["bulgular"]:
            by.setdefault(b["kategori"], []).append(b)
        for kat in sorted(by):
            print(f"  [{kat}] {len(by[kat])}")
            for b in by[kat][:12]:
                loc = f"s.{b['sayfa']}" if b["sayfa"] else "genel"
                print(f"     {loc}: {b['mesaj']}")
            if len(by[kat]) > 12:
                print(f"     … +{len(by[kat]) - 12} tane daha")
        total += len(r["bulgular"])
    print(f"\ntoplam bulgu: {total}")
    return 0


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    paths = args or sorted(glob.glob(str(ROOT / "out" / "*.pdf")))
    sys.exit(main(paths, "--json" in sys.argv))

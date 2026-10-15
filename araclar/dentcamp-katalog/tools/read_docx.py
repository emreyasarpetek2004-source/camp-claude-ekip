#!/usr/bin/env python3
"""docx -> düz metin (paragraf ve tablo sırası korunarak)."""
import re
import sys
import zipfile
from xml.etree import ElementTree as ET

NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}


def text_of(el):
    return "".join(t.text or "" for t in el.iter(f'{{{NS["w"]}}}t'))


def style_of(p):
    s = p.find("w:pPr/w:pStyle", NS)
    return s.get(f'{{{NS["w"]}}}val') if s is not None else ""


def bold_run_ratio(p):
    runs = p.findall("w:r", NS)
    if not runs:
        return 0.0
    bold = sum(1 for r in runs if r.find("w:rPr/w:b", NS) is not None and (r.find("w:t", NS) is not None))
    have = sum(1 for r in runs if r.find("w:t", NS) is not None)
    return bold / have if have else 0.0


def dump(path):
    z = zipfile.ZipFile(path)
    root = ET.fromstring(z.read("word/document.xml"))
    body = root.find("w:body", NS)
    for el in body:
        tag = el.tag.split("}")[1]
        if tag == "p":
            t = text_of(el).strip()
            if not t:
                continue
            st = style_of(el)
            mark = ""
            if st.startswith("Heading") or st.startswith("Balk"):
                mark = f"[{st}] "
            elif bold_run_ratio(el) > 0.85:
                mark = "[B] "
            num = el.find("w:pPr/w:numPr", NS)
            if num is not None:
                mark += "- "
            print(mark + t)
        elif tag == "tbl":
            print("[TABLO]")
            for row in el.findall("w:tr", NS):
                cells = [re.sub(r"\s+", " ", text_of(c)).strip()
                         for c in row.findall("w:tc", NS)]
                print("  | " + " | ".join(cells))


if __name__ == "__main__":
    for p in sys.argv[1:]:
        print(f"\n{'=' * 70}\n### {p}\n{'=' * 70}")
        dump(p)

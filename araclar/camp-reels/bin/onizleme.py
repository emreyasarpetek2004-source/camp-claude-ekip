#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""out/ONIZLEME.html: reels'ları yan yana oynatır; kanca, süre, neden ve denetim sonucunu gösterir.
Kullanım: python3 bin/onizleme.py <proje>
"""
import html
import json
import os
import re
import sys


def main():
    proje = os.path.abspath(sys.argv[1])
    meta = json.load(open(os.path.join(proje, "proje.json")))
    rp = os.path.join(proje, "edit", "denetim", "rapor.json")
    rapor = {r["no"]: r for r in json.load(open(rp))} if os.path.exists(rp) else {}
    kart = []
    kartlar = {}
    for f in sorted(os.listdir(os.path.join(proje, "edit"))):
        m = re.match(r"reels_(\d+)_edl\.json$", f)
        if m:
            kartlar[int(m.group(1))] = json.load(open(os.path.join(proje, "edit", f)))
    for f in sorted(os.listdir(os.path.join(proje, "edit"))):  # v2 aynı numarada v1'in önüne geçer
        m = re.match(r"klip_(\d+)$", f)
        kj = os.path.join(proje, "edit", f, "klip.json")
        if m and os.path.exists(kj) and os.path.exists(os.path.join(proje, "edit", "sahne_%s.json" % m.group(1))):
            k = json.load(open(kj))
            kartlar[int(m.group(1))] = {"no": k["no"], "baslik": k.get("baslik"), "kanca": k.get("soru") or k.get("kanca"),
                                       "sure": k["sure"], "duzen": "v2 " + k["duzen"], "neden": k.get("kanca")}
    for no in sorted(kartlar):
        e = kartlar[no]
        if not os.path.exists(os.path.join(proje, "out", "reels_%02d.mp4" % no)):
            continue
        r = rapor.get(e["no"], {})
        durum = "GEÇTİ" if r.get("gecti") else ("KALDI" if r else "denetlenmedi")
        kart.append(f"""<div class="k"><video src="reels_{e['no']:02d}.mp4" controls preload="metadata"></video>
<h3>#{e['no']} {html.escape(e.get('baslik') or '')}</h3>
<p class="kanca">“{html.escape(e.get('kanca') or '')}”</p>
<p>{e['sure']:.0f} sn · {e['duzen']} · <b class="{'ok' if r.get('gecti') else 'xx'}">{durum}</b></p>
<p class="n">{html.escape(e.get('neden') or '')}</p></div>""")
    sayfa = f"""<!doctype html><html lang="tr"><meta charset="utf-8"><title>{meta['marka'].upper()} reels önizleme</title>
<style>body{{font-family:-apple-system,Helvetica,sans-serif;background:#111;color:#eee;margin:24px}}
.g{{display:flex;flex-wrap:wrap;gap:20px}}.k{{width:300px;background:#1c1c1c;padding:12px;border-radius:10px}}
video{{width:100%;border-radius:6px;background:#000}}h3{{font-size:15px;margin:10px 0 4px}}
.kanca{{color:#9fe;font-style:italic;font-size:14px}}.n{{color:#aaa;font-size:13px}}.ok{{color:#5d5}}.xx{{color:#f66}}</style>
<h1>{html.escape(meta['ad'])}</h1><div class="g">{''.join(kart)}</div></html>"""
    out = os.path.join(proje, "out", "ONIZLEME.html")
    open(out, "w").write(sayfa)
    print(out)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bölüme eşleşmemiş Loom kayıtlarını müfredatla eşleştirir.

loom_mapped.json 4 Eylul'de cikarilmisti; sonrasinda cekilen dersler eslesmiyor ve
uretim sirasina hic girmiyor. (22.09.2026: kullanıcı "52 ders var" deyince fark edildi.)

Yontem: Loom paylasim sayfasinin og:title'i bolum adini tasiyor
("Preview - CHxx BOLUM ADI.pdf"). Baslik cekilir, mufredatla eslestirilir.

TUZAK: basili kitabin 119'luk numaralandirmasi ile 164'luk liste FARKLI.
Eslestirme bolum ADIYLA yapilir, numaraya guvenilmez.
"""
import json
import os
import re
import subprocess
import sys
import time
import unicodedata

KOK = os.path.expanduser("~/camp-video")
MUF = os.path.expanduser("~/campverse-slides/mufredat/AUSCAMP-AMC-MCQ-mufredat.tsv")
LM = os.path.expanduser("~/campverse-slides/mufredat/loom_mapped.json")


def sade(m):
    """Mufredat '&' kullaniyor, Loom basligi 'AND' yaziyor: ikisi ayni sayilmali.
    (22.09.2026: 'Dizziness & Vertigo' ile 'DIZZINESS AND VERTIGO' bu yuzden tutmuyordu.)"""
    m = unicodedata.normalize("NFKD", (m or "").upper())
    m = m.replace("&", " AND ")
    m = re.sub(r"\bAND\b", "", m)      # her iki tarafta da AND atilir
    return re.sub(r"[^A-Z0-9]", "", m)


def mufredat():
    out = []
    with open(MUF) as f:
        bas = f.readline().rstrip("\n").split("\t")
        for satir in f:
            h = satir.rstrip("\n").split("\t")
            d = dict(zip(bas, h))
            try:
                out.append({"no": int(d["Bölüm No"]), "ad": d["Bölüm Adı"].strip(),
                            "kitap": int(d["Kitap No"])})
            except (ValueError, KeyError):
                pass
    return out


def baslik_cek(vid):
    r = subprocess.run(["curl", "-sL", "--max-time", "25", "-A",
                        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
                        "https://www.loom.com/share/%s" % vid],
                       capture_output=True, text=True)
    h = r.stdout or ""
    for kalip in (r'<meta[^>]+property="og:title"[^>]+content="([^"]+)"',
                  r'<meta[^>]+content="([^"]+)"[^>]+property="og:title"',
                  r"<title>([^<]+)</title>"):
        m = re.search(kalip, h, re.I)
        if m:
            return m.group(1).strip()
    return ""


def main():
    wa = json.load(open(os.path.join(KOK, "takip/ders_kayitlari.json")))["kayit"]
    lm = json.load(open(LM))
    eslesen = {x["vid"] for x in lm if x.get("no")}
    esz = [k for k in wa if k["loom_vid"] not in eslesen]
    muf = mufredat()
    print("eslesmeyen kayit: %d · mufredat bolumu: %d" % (len(esz), len(muf)), flush=True)

    yeni, bulunamadi = [], []
    for i, k in enumerate(esz, 1):
        b = baslik_cek(k["loom_vid"])
        s = sade(b)
        aday = [m for m in muf if s and sade(m["ad"]) and sade(m["ad"]) in s]
        if aday:
            en = max(aday, key=lambda m: len(sade(m["ad"])))
            yeni.append({"vid": k["loom_vid"], "no": en["no"], "chapter": en["ad"],
                         "kitap": en["kitap"], "date": k["link_tarih"][:10],
                         "url": k["url"], "baslik": b})
            print("  %2d/%d  CH%02d %-36s <- %s" % (i, len(esz), en["no"], en["ad"][:36], b[:44]), flush=True)
        else:
            bulunamadi.append({"vid": k["loom_vid"], "tarih": k["link_tarih"][:10], "baslik": b})
            print("  %2d/%d  ESLESMEDI  %s  baslik=%s" % (i, len(esz), k["loom_vid"][:8], b[:50]), flush=True)
        time.sleep(20)

    json.dump({"yeni": yeni, "bulunamadi": bulunamadi},
              open(os.path.join(KOK, "takip/yeni_eslesme.json"), "w"),
              ensure_ascii=False, indent=1)
    print("\nESLESEN: %d · ESLESMEYEN: %d" % (len(yeni), len(bulunamadi)))


if __name__ == "__main__":
    main()

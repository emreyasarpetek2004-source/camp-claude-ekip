#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""WhatsApp'ta yazili her kesim dakikasi gercekten kesilmis mi, tek tabloda goster.

Yazili dakika EMIRDIR (22.09.2026 kararı: "nereleri kesmeni istedigin bile yazilmis").
Bu rapor, 51 dersin hicbirinde o emrin atlanmadigini kanitlar.
"""
import json
import os
import sys

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(KOK, "bin"))
import hat  # noqa: E402

PENCERE = 90.0  # kesim bu kadar yakinsa o dakika karsilanmis sayilir


def isaretli_dakikalar(edit):
    """Modelin ACIKCA bir talimat dakikasina bagladigi kesimler.

    Yazili dakika kayittaki gercek yerle ortusmeyebiliyor (CH16: mesajda 6. dk,
    kusur 11. dakikada). Kapinin isi sessiz atlamayi yakalamak, gerekcelendirilmis
    eslemeyi bozmak degil; hat.py --model ile ayni kural.
    """
    y = os.path.join(edit, "model_kesim.json")
    if not os.path.exists(y):
        return set()
    d = json.load(open(y))
    for ad in ("kesimler", "kesim", "kesim_listesi", "cuts"):
        if isinstance(d.get(ad), list):
            liste = d[ad]
            break
    else:
        return set()
    cik = set()
    for k in liste:
        t = k.get("talimat", k.get("talimat_dakika"))
        if t is None:
            continue
        t = int(t)
        cik.add(t if t < 200 else t // 60)
    return cik


def kesimleri_oku(edit):
    y = os.path.join(edit, "model_kesim.json")
    if not os.path.exists(y):
        return None
    d = json.load(open(y))
    for ad in ("kesimler", "kesim", "kesim_listesi", "cuts"):
        if isinstance(d.get(ad), list):
            liste = d[ad]
            break
    else:
        return []
    cik = []
    for k in liste:
        if k.get("karar") in ("atla", "kesme", "reddedildi"):
            continue
        b = k.get("bas", k.get("bas_s"))
        e = k.get("bit", k.get("bit_s"))
        if b is None or e is None:
            continue
        cik.append((float(b), float(e)))
    return cik


def main():
    rapor, acik = [], 0
    for ad in sorted(os.listdir(os.path.join(KOK, "projects"))):
        proje = os.path.join(KOK, "projects", ad)
        edit = os.path.join(proje, "edit")
        if not os.path.isdir(edit):
            continue
        vid = ad.split("-")[-1]
        kayit = next((k for k in hat.kayitlar()
                      if k.get("loom_vid", "").startswith(vid)), None) \
            if hasattr(hat, "kayitlar") else hat.kayit_bul(vid)
        if not kayit:
            continue
        dakikalar = hat.talimat_dakikalari(kayit)
        kes = kesimleri_oku(edit)
        sat = {"ders": ad, "talimat_dakika": [int(s // 60) for s in dakikalar],
               "kesim_listesi": "yok" if kes is None else "%d kesim" % len(kes)}
        if not dakikalar:
            sat["durum"] = "talimat yok"
        elif kes is None:
            sat["durum"] = "BEKLIYOR (kesim listesi uretilmedi)"
            acik += 1
        else:
            isaretli = isaretli_dakikalar(edit)
            eksik = [int(s // 60) for s in dakikalar
                     if not any(b - PENCERE <= s <= e + PENCERE for b, e in kes)
                     and int(s // 60) not in isaretli]
            sat["karsilanmayan"] = eksik
            sat["durum"] = "TAMAM" if not eksik else "EKSIK"
            if eksik:
                acik += 1
        rapor.append(sat)

    out = os.path.join(KOK, "takip", "talimat_kapsama.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump({"pencere_s": PENCERE, "acik": acik, "ders": rapor},
              open(out, "w"), ensure_ascii=False, indent=1)

    for s in rapor:
        if s["durum"] in ("TAMAM", "talimat yok"):
            continue
        print("  %-52s %-12s talimat %s %s"
              % (s["ders"][:52], s["durum"], s["talimat_dakika"],
                 ("karsilanmayan " + str(s["karsilanmayan"])) if s.get("karsilanmayan") else ""))
    tamam = sum(1 for s in rapor if s["durum"] == "TAMAM")
    yok = sum(1 for s in rapor if s["durum"] == "talimat yok")
    print("TALIMAT KAPSAMA: %d tamam · %d talimatsiz · %d acik  ->  %s"
          % (tamam, yok, acik, out))
    sys.exit(1 if acik else 0)


if __name__ == "__main__":
    main()

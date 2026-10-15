#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TESLIM EDILEN videoda acilisi ve HER kesim sinirini denetler.

Kullanıcı (23.09.2026): "acilis ve kesim yerlerine de dikkat etmelisin tum derslerde."

Veri kaynagi teslim taramasindaki tam cozumleme; ek ASR gerekmez.
  ACILIS : ilk 25 saniyede yanlis baslangic izi var mi (dur/bastan/pardon/bir dakika),
           ya da ders cumle ortasindan mi basliyor.
  KESIM  : her dikiste, oncesindeki son soz yarim mi kaliyor.
"""
import json, os, re, sys

KOK = os.path.expanduser("~/camp-video")
TAR = os.path.join(KOK, "takip", "teslim_tarama")
BITIS = re.compile(r"[.!?]\s*$")
YARIM = re.compile(r"\b(ve|ama|eğer|çünkü|ki|de|da|ile|için|yani|bu|şu|o|bir|hem|ya)\s*$", re.I)
KOTU_ACILIS = re.compile(r"\bdur\b|baştan|bastan|bir dakika|pardon|özür|ozur|tamam dur|"
                         r"başlıyorum|basliyorum|geldim|hazır mıyız|hazir miyiz", re.I)
BASHARF = re.compile(r"^[a-zçğıöşü]")


def edl_dikisleri(proje):
    ey = os.path.join(KOK, "projects", proje, "edit", "edl.json")
    if not os.path.exists(ey):
        return []
    rs = json.load(open(ey))["ranges"]
    t, out = 0.0, []
    for r in rs[:-1]:
        t += float(r["end"]) - float(r["start"])
        if r.get("source") == "DERS":
            out.append(round(t, 2))
    return out


def proje_bul(ad):
    no = ad.split(" - ")[0]
    for d in os.listdir(os.path.join(KOK, "projects")):
        if d.startswith("campverse-ch%s-" % no):
            return d
    return None


def main():
    acilis_sorun, kesim_sorun = [], []
    for f in sorted(os.listdir(TAR)):
        if not f.endswith(".json"):
            continue
        d = json.load(open(os.path.join(TAR, f)))
        if not isinstance(d.get("segment"), list) or not d["segment"]:
            continue
        ad = d["ders"]
        seg = sorted(d["segment"], key=lambda s: s["bas"])

        # --- ACILIS
        # Ilk 6 sn CAMPVERSE openeri: whisper oraya muzik uzerine "abone ol" uyduruyor.
        bas_metin = " ".join(x["metin"] for x in seg if 6.2 <= x["bas"] < 30
                             and "abone ol" not in x["metin"].lower())
        m = KOTU_ACILIS.search(bas_metin[:200])
        if m or BASHARF.match(bas_metin.strip()):
            acilis_sorun.append((ad, bas_metin[:150], m.group(0) if m else "kucuk harfle basliyor"))

        # --- KESIMLER
        proje = proje_bul(ad)
        if not proje:
            continue
        for T in edl_dikisleri(proje):
            onc = [s for s in seg if s["bit"] <= T + 0.35 and s["bit"] > T - 7]
            if not onc:
                continue
            son = onc[-1]["metin"].strip()
            agir = bool(YARIM.search(son))
            if agir or not BITIS.search(son):
                sonra = next((s["metin"] for s in seg if s["bas"] >= T - 0.35), "")
                kesim_sorun.append((ad, T, son[-70:], sonra[:60], "A" if agir else "B"))

    print("=== ACILIS SUPHELI (%d)" % len(acilis_sorun))
    for ad, met, iz in acilis_sorun:
        print("  %-44s [%s]\n      %s" % (ad[:44], iz, met[:120]))
    print("\n=== KESIM SINIRI SUPHELI (%d)" % len(kesim_sorun))
    for tier in ("A", "B"):
        alt = [x for x in kesim_sorun if x[4] == tier]
        print("\n  -- oncelik %s (%d): %s" % (tier, len(alt),
              "baglacla bitiyor, neredeyse kesin bozuk" if tier == "A" else "noktalama yok, cogu yanlis alarm"))
        for ad, T, son, sonra, _ in alt:
            print("     %-38s %d:%05.2f  ...%s  ||  %s" % (ad[:38], T // 60, T % 60, son, sonra))
    json.dump({"acilis": acilis_sorun, "kesim": kesim_sorun},
              open(os.path.join(KOK, "takip", "acilis_kesim.json"), "w"),
              ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()

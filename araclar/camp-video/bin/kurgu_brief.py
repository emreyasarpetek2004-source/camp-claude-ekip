#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Modele verilecek kurgu brief'ini uretir.

Karar modelin, kanit bu dosyanin. (Plan: sezgisel kaliplardan model kararina gecis,
22.09.2026 — yedi dedektor yedi kez yetersiz kaldi cunku soru semantik.)

Brief icerigi:
  - zaman damgali cumleler (ASR kelime kelime donse bile birlestirilmis)
  - her cumleden ONCEKI duraklama suresi (yeniden cekimin en guclu isareti)
  - slayt degisim anlari (hoca slaytlarda geziniyorsa gorunur)
  - WhatsApp talimatindaki dakikalar (EMIR)
  - mevcut sezgisel dedektorlerin bulgulari (IPUCU, karar degil)

Kullanim: python3 bin/kurgu_brief.py <proje_dizini> [--out brief.md]
"""
import argparse
import json
import os
import re
import subprocess
import sys

KOK = os.path.expanduser("~/camp-video")
sys.path.insert(0, os.path.join(KOK, "bin"))
FFMPEG = os.path.expanduser("~/.local/bin/ffmpeg")


def slayt_degisimleri(video, esik=0.10):
    p = subprocess.run([FFMPEG, "-nostats", "-v", "error", "-i", video, "-vf",
                        "select='gt(scene,%.2f)',metadata=print:file=-" % esik,
                        "-an", "-f", "null", "-"], capture_output=True, text=True)
    return [round(float(m), 1) for m in re.findall(r"pts_time:([\d.]+)", p.stdout or "")]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("proje")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    edit = os.path.join(a.proje, "edit")
    ham = os.path.join(a.proje, "ders.mp4")

    from tekrar_bul import segmentleri_birlestir
    seg = [x for w in json.load(open(os.path.join(edit, "transkript_tam.json")))["pencere"]
           for x in w["segment"]]
    seg.sort(key=lambda s: s["bas"])
    seg = segmentleri_birlestir(seg)
    ses = json.load(open(os.path.join(edit, "sessizlik.json")))
    bos = ses["bosluk"]

    # talimat
    import hat
    vid = os.path.basename(a.proje).split("-")[-1]
    kayit = hat.kayit_bul(vid)
    talimat = hat.talimat_dakikalari(kayit) if kayit else []
    ham_talimat = " / ".join((t.get("metin") or "").strip()[:100]
                             for t in (kayit or {}).get("talimat_ham", [])[:3])

    # ipuclari (karar degil)
    ipucu = []
    try:
        k = json.load(open(os.path.join(edit, "kesimler.json")))
        for x in k.get("aday", []):
            ipucu.append((x["bas"], x["bit"], x["tur"]))
    except (OSError, ValueError):
        pass

    if not os.path.exists(ham):
        # Sessizce bos slayt listesiyle brief basmak, modeli gecis duraklamasini
        # ritim kesilmesinden ayiramaz hale getiriyor. (23.09.2026: 16 brief bu
        # yuzden 0 slayt degisimiyle uretilmisti, ham disk acmak icin silinmisti.)
        raise SystemExit("HATA: ham video yok: %s — Downloads/Ham'dan geri baglanmali" % ham)
    slayt = slayt_degisimleri(ham)
    if not slayt:
        print("UYARI: slayt degisimi bulunamadi (%s)" % ham)

    L = []
    L.append("# KURGU BRIEF")
    L.append("sure: %.1f dk · ilk konusma %.2f sn · son konusma %.2f sn"
             % (ses["toplam_sure"] / 60, ses["ilk_konusma"], ses["son_konusma"]))
    L.append("")
    L.append("## TALIMAT (WhatsApp, EMIR)")
    if talimat:
        L.append("kesilmesi istenen dakikalar: %s" % ", ".join(str(t // 60) for t in talimat))
        L.append("ham mesaj: %s" % ham_talimat)
    else:
        L.append("YOK — bu derste yazili talimat yok, tum kaydi kendin tarayacaksin")
    L.append("")
    L.append("## SLAYT DEGISIM ANLARI (sn)")
    L.append(", ".join("%.1f" % t for t in slayt[:120]) or "yok")
    L.append("")
    L.append("## SEZGISEL IPUCLARI (karar degil, sadece dikkat cekmek icin)")
    for b, e, t in ipucu[:40]:
        L.append("  %.1f-%.1f  %s" % (b, e, t))
    if not ipucu:
        L.append("  yok")
    L.append("")
    L.append("## TRANSKRIPT")
    L.append("bicim: [baslangic-bitis] (onceki duraklama sn) metin")
    onceki_bit = 0.0
    for s in seg:
        d = max([b["sure"] for b in bos if onceki_bit - 0.3 <= b["bas"] <= s["bas"] + 0.3] or [0])
        isaret = " <<< %.1f sn DURAKLAMA" % d if d >= 1.5 else ""
        L.append("[%.1f-%.1f] (%.1f)%s %s" % (s["bas"], s["bit"], d, isaret, s["metin"]))
        onceki_bit = s["bit"]

    out = a.out or os.path.join(edit, "brief.md")
    open(out, "w").write("\n".join(L))
    print("brief: %s · %d cumle · %d slayt degisimi · %d talimat dakikasi"
          % (out, len(seg), len(slayt), len(talimat)))


if __name__ == "__main__":
    main()

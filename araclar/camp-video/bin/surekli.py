#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Kesintisiz üretim gözetmeni.

(22.09.2026 kararı: "sürekli kesilmeyecek bir döngü oluştur")

İlkeler:
  - Tek bir dersin hatası TÜM seriyi durdurmaz, sıradakine geçer.
  - Üst üste hata olursa BEKLER (Loom hız sınırı böyle geçer), sonra devam eder.
  - Teslim edilmiş dersi atlar, yani her zaman kaldığı yerden sürer.
  - Bir tur bitince hata alanları YENIDEN dener; ilerleme kalmayınca durur.
  - Durumu her ders sonrası dosyaya yazar, disk doluluğunu kollar.
"""
import json
import os
import subprocess
import time

KOK = os.path.expanduser("~/camp-video")
LOG = "/tmp/surekli.log"
DURUM = os.path.join(KOK, "takip/surekli_durum.json")
EN_AZ_DISK_GB = 6


def yaz(m):
    s = "%s  %s" % (time.strftime("%H:%M"), m)
    print(s, flush=True)
    with open(LOG, "a") as f:
        f.write(s + "\n")


def disk_gb():
    v = os.statvfs(os.path.expanduser("~"))
    return v.f_bavail * v.f_frsize / 1e9


def dersler():
    wa = json.load(open(os.path.join(KOK, "takip/ders_kayitlari.json")))["kayit"]
    lm = json.load(open(os.path.expanduser("~/campverse-slides/mufredat/loom_mapped.json")))
    vid = {k["loom_vid"] for k in wa}
    d = [x for x in lm if x.get("no") and x["vid"] in vid]
    return sorted(d, key=lambda x: x["no"])


def teslim_edildi(x):
    return os.path.exists(os.path.join(KOK, "teslim/campverse",
                                       "%02d - %s.mp4" % (x["no"], x["chapter"].strip())))


def main():
    tur = 0
    while True:
        tur += 1
        kalan = [x for x in dersler() if not teslim_edildi(x)]
        if not kalan:
            yaz("TAMAM: tum dersler teslim edildi")
            return
        yaz("TUR %d basliyor · kalan ders: %d" % (tur, len(kalan)))
        ilerleme, pes_pese = 0, 0

        for x in kalan:
            while disk_gb() < EN_AZ_DISK_GB:
                yaz("disk %.1f GB, 5 dk bekleniyor" % disk_gb())
                time.sleep(300)
            t = time.time()
            r = subprocess.run(["python3", os.path.join(KOK, "bin/hat.py"), x["vid"]],
                               capture_output=True, text=True)
            ok = "TESLIM:" in r.stdout
            ozet = ""
            for satir in r.stdout.splitlines():
                if "kesim:" in satir:
                    ozet = satir.strip()
            if ok:
                ilerleme += 1
                pes_pese = 0
                yaz("CH%02d %-38s OK  %.1f dk  %s"
                    % (x["no"], x["chapter"][:38], (time.time() - t) / 60, ozet))
            else:
                pes_pese += 1
                son = [l for l in (r.stdout + r.stderr).splitlines() if l.strip()][-1:] or ["?"]
                yaz("CH%02d %-38s SORUN  %s" % (x["no"], x["chapter"][:38], son[0][:110]))
                bekle = min(600, 120 * pes_pese)
                yaz("  %d sn bekleniyor (ust uste %d hata)" % (bekle, pes_pese))
                time.sleep(bekle)
            json.dump({"tur": tur, "kalan": len(kalan) - ilerleme,
                       "son": "CH%02d" % x["no"], "guncelleme": time.strftime("%H:%M")},
                      open(DURUM, "w"), ensure_ascii=False, indent=1)

        if ilerleme == 0:
            yaz("TUR %d: hic ilerleme yok, 10 dk bekleyip yeniden denenecek" % tur)
            time.sleep(600)
            if tur >= 6:
                yaz("DUR: 6 turdur ilerleme yok, elle bakilmali")
                return


if __name__ == "__main__":
    main()

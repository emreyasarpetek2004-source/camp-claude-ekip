#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""META YAPI: iki hat aynı anda, FARKLI derslerde çalışır.

(22.09.2026 kararı: "gözetimi bir agent yaparken 2. agent diğer dersi yapıcak
 şekilde bir meta yapı kurabilir misin")

Bölünme ders bazında DEĞİL, kaynak bazında yapıldı. Sebebi ölçüm: bu makinede
16 GB RAM'in 0,1 GB'ı boş, takas alanının 7,1/8 GB'ı dolu. İki dersi baştan sona
paralel işlemek bugün üç kez yaşanan SIGKILL'i garantiler.

Oysa aşamalar farklı kaynak kullanıyor:
    HAZIRLIK hattı : indirme (ağ) + transkripsiyon (GPU/Metal) + kesim çözümü
    URETIM   hattı : kodlama (islemci) + denetim + teslim

Bu ikisi farklı derslerde aynı anda koşabilir ve birbirinin kaynağını yemez.
Kuyruk sınırlı tutulur (varsayılan 2), yoksa disk dolar.
"""
import json
import os
import queue
import subprocess
import threading
import time

import sys
KOK = os.path.expanduser("~/camp-video")
sys.path.insert(0, os.path.join(KOK, "bin"))
import hat
LOG = "/tmp/meta.log"
DURUM = os.path.join(KOK, "takip/meta_durum.json")
KUYRUK = 2
EN_AZ_DISK_GB = 6

kilit = threading.Lock()
durum = {"indirilen": None, "hazirlanan": None, "uretilen": None, "teslim": 0, "sorun": []}


def yaz(m):
    s = "%s  %s" % (time.strftime("%H:%M"), m)
    with kilit:
        print(s, flush=True)
        with open(LOG, "a") as f:
            f.write(s + "\n")


def disk_gb():
    v = os.statvfs(os.path.expanduser("~"))
    return v.f_bavail * v.f_frsize / 1e9


def dersler():
    wa = json.load(open(os.path.join(KOK, "takip/ders_kayitlari.json")))["kayit"]
    lm = json.load(open(os.path.join(KOK, "takip/dersler.json")))
    vid = {k["loom_vid"] for k in wa}
    return sorted([x for x in lm if x.get("no") and x["vid"] in vid], key=lambda x: x["no"])


def teslim_edildi(x):
    return os.path.exists(os.path.join(KOK, "teslim/campverse",
                                       "%02d - %s.mp4" % (x["no"], x["chapter"].strip())))


def calistir(vid, mod):
    return subprocess.run(["python3", os.path.join(KOK, "bin/hat.py"), vid, mod],
                          capture_output=True, text=True)


INDIRME_PARALEL = 2   # ag seridi: bellege yuk bindirmez, ama Loom hiz siniri var


def _tek_indir(x, kuyruk, kilit_sayac):
    while disk_gb() < EN_AZ_DISK_GB + 2:
        yaz("INDIRME: disk %.1f GB, bekliyor" % disk_gb())
        time.sleep(180)
    with kilit_sayac:
        durum.setdefault("inenler", []).append("CH%02d" % x["no"])
    t = time.time()
    r = calistir(x["vid"], "--indir")
    with kilit_sayac:
        try:
            durum["inenler"].remove("CH%02d" % x["no"])
        except ValueError:
            pass
    if "INDI:" in r.stdout or "TESLIM:" in r.stdout:
        yaz("INDI    CH%02d %-34s %.1f dk" % (x["no"], x["chapter"][:34],
                                              (time.time() - t) / 60))
        kuyruk.put(x)
    else:
        son = [l for l in (r.stdout + r.stderr).splitlines() if l.strip()][-1:] or ["?"]
        yaz("SORUN   CH%02d indirme: %s" % (x["no"], son[0][:100]))
        durum["sorun"].append("CH%02d indirme" % x["no"])
        time.sleep(90)


def indirme_hatti(kuyruk, liste):
    """Ag seridi: iki indirme paralel. Loom hiz sinirina takilmamak icin
    baslatmalar arasinda 15 sn beklenir (22.09.2026'da 32 indirme birden
    baslatmak 404 duvarina carpmisti)."""
    from concurrent.futures import ThreadPoolExecutor
    kilit_sayac = threading.Lock()
    for tur in (1, 2, 3):
        hedef = [x for x in liste if not teslim_edildi(x)
                 and not os.path.exists(os.path.join(
                     KOK, "projects", "campverse-%s-%s" % (hat.slug("CH%02d %s" % (x["no"], x["chapter"])), x["vid"][:8]), "ders.mp4"))]
        if not hedef:
            break
        if tur > 1:
            yaz("INDIRME turu %d: %d ders yeniden denenecek" % (tur, len(hedef)))
            time.sleep(120)
        with ThreadPoolExecutor(max_workers=INDIRME_PARALEL) as ex:
            isler = []
            for x in hedef:
                isler.append(ex.submit(_tek_indir, x, kuyruk, kilit_sayac))
                time.sleep(15)
            for i in isler:
                i.result()
    kuyruk.put(None)
    durum["indirilen"] = None


def hazirlik_hatti(gelen, kuyruk):
    """GPU seridi: sessizlik + transkript + kesim cozumu."""
    while True:
        x = gelen.get()
        if x is None:
            break
        durum["hazirlanan"] = "CH%02d" % x["no"]
        t = time.time()
        r = calistir(x["vid"], "--hazirla")
        if "HAZIR:" in r.stdout:
            kesim = next((l.strip() for l in r.stdout.splitlines() if "kesim:" in l), "")
            yaz("HAZIR   CH%02d %-34s %.1f dk  %s"
                % (x["no"], x["chapter"][:34], (time.time() - t) / 60, kesim))
            kuyruk.put(x)
        else:
            son = [l for l in (r.stdout + r.stderr).splitlines() if l.strip()][-1:] or ["?"]
            yaz("SORUN   CH%02d hazirlik: %s" % (x["no"], son[0][:100]))
            durum["sorun"].append("CH%02d hazirlik" % x["no"])
            time.sleep(30)
    kuyruk.put(None)
    durum["hazirlanan"] = None


def uretim_hatti(kuyruk):
    while True:
        x = kuyruk.get()
        if x is None:
            break
        durum["uretilen"] = "CH%02d" % x["no"]
        t = time.time()
        r = calistir(x["vid"], "--uret")
        if "TESLIM:" in r.stdout:
            durum["teslim"] += 1
            yaz("TESLIM  CH%02d %-34s %.1f dk" % (x["no"], x["chapter"][:34],
                                                  (time.time() - t) / 60))
        else:
            son = [l for l in (r.stdout + r.stderr).splitlines() if l.strip()][-1:] or ["?"]
            yaz("SORUN   CH%02d uretim: %s" % (x["no"], son[0][:100]))
            durum["sorun"].append("CH%02d uretim" % x["no"])
        json.dump(durum, open(DURUM, "w"), ensure_ascii=False, indent=1)
    durum["uretilen"] = None


def main():
    liste = dersler()
    kalan = [x for x in liste if not teslim_edildi(x)]
    yaz("META basliyor · %d ders · 3 serit (indirme | cozum | uretim) · kuyruk %d"
        % (len(kalan), KUYRUK))
    inen = queue.Queue(maxsize=KUYRUK)      # indirilmis, cozulmeyi bekleyen
    hazir = queue.Queue(maxsize=KUYRUK)     # cozulmus, uretilmeyi bekleyen
    i = threading.Thread(target=indirme_hatti, args=(inen, liste), daemon=True)
    h = threading.Thread(target=hazirlik_hatti, args=(inen, hazir), daemon=True)
    u = threading.Thread(target=uretim_hatti, args=(hazir,), daemon=True)
    i.start(); h.start(); u.start()
    i.join(); h.join(); u.join()
    yaz("META bitti · teslim: %d · sorun: %d" % (durum["teslim"], len(durum["sorun"])))
    if durum["sorun"]:
        yaz("sorunlu: " + ", ".join(durum["sorun"]))


if __name__ == "__main__":
    main()

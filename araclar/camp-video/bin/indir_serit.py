#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Yalniz indirme seridi: hami olmayan dersleri ikili paralel, araliklarla indirir.
Kurgu kuyruklariyla cakismaz cunku uretime hic dokunmaz."""
import json, os, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
KOK = os.path.expanduser("~/camp-video")
sys.path.insert(0, os.path.join(KOK, "bin")); import hat

def disk_gb():
    v = os.statvfs(os.path.expanduser("~")); return v.f_bavail * v.f_frsize / 1e9

def proje(x):
    return os.path.join(KOK, "projects", "campverse-%s-%s"
                        % (hat.slug("CH%02d %s" % (x["no"], x["chapter"])), x["vid"][:8]))

def yaz(m):
    s = "%s  %s" % (time.strftime("%H:%M"), m)
    print(s, flush=True)
    open("/tmp/indirme.log", "a").write(s + "\n")

def indir(x):
    while disk_gb() < 10:
        yaz("disk %.1f GB, bekleniyor" % disk_gb()); time.sleep(300)
    t = time.time()
    r = subprocess.run(["python3", os.path.join(KOK, "bin/hat.py"), x["vid"], "--indir"],
                       capture_output=True, text=True)
    if "INDI:" in r.stdout:
        yaz("INDI  CH%02d %-38s %.1f dk" % (x["no"], x["chapter"][:38], (time.time()-t)/60))
    else:
        son = [l for l in (r.stdout+r.stderr).splitlines() if l.strip()][-1:] or ["?"]
        yaz("SORUN CH%02d %s" % (x["no"], son[0][:90]))

def main():
    d = json.load(open(os.path.join(KOK, "takip/dersler.json")))
    ed = os.path.expanduser("~/Downloads/CAMPVERSE Dersler/Editli")
    tes = {int(f[:2]) for f in os.listdir(ed) if f[:2].isdigit() and f[:2] != "00"}
    for tur in (1, 2, 3):
        hedef = [x for x in d if x["no"] not in tes
                 and not os.path.exists(os.path.join(proje(x), "ders.mp4"))]
        if not hedef:
            yaz("TAMAM: indirilecek ders kalmadi"); return
        yaz("TUR %d · %d ders indirilecek" % (tur, len(hedef)))
        with ThreadPoolExecutor(max_workers=2) as ex:
            isler = []
            for x in hedef:
                isler.append(ex.submit(indir, x)); time.sleep(15)
            for i in isler: i.result()
        time.sleep(60)

if __name__ == "__main__":
    main()

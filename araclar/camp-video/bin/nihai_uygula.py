#!/usr/bin/env python3
"""kesim_nihai.json'u (kelime zamanli dogrulama) model_kesim.json'a isler ve EDL'i kurar.

05.10.2026 yeniden taramasi. Akis:
  1. model_kesim.json -> model_kesim.pre1005.json (bir kez yedek)
  2. kesimler = kesim_nihai.kesimler (her biri "kesin": true, dar hizalama)
     bas_kirpma / son_kirpma aynen korunur; supheli listeleri birlestirilir
  3. hat.py --model --kuru (EDL)
  4. KONTROL: her nihai kesim EDL'de bir bosluga +-0,4 sn icinde oturmus mu?
     Sapan varsa rapor eder, cikis kodu 2 (uretime gonderilmez).
Kullanim: bin/nihai_uygula.py projects/<proje> [--kuru-yok]
"""
import json, os, shutil, subprocess, sys
p = sys.argv[1].rstrip("/"); edit = os.path.join(p, "edit")
n = json.load(open(os.path.join(edit, "kesim_nihai.json")))
mk_yol = os.path.join(edit, "model_kesim.json")
yedek = os.path.join(edit, "model_kesim.pre1005.json")
if not os.path.exists(yedek):
    shutil.copy2(mk_yol, yedek)
eski = json.load(open(yedek))
yeni = {k: v for k, v in eski.items() if k in ("bas_kirpma", "son_kirpma")}
yeni["kesimler"] = []
toplam = json.load(open(os.path.join(edit, "sessizlik.json")))["toplam_sure"]
for k in sorted(n["kesimler"], key=lambda x: x["bas"]):
    # Dersin basina ya da sonuna dayanan "kesim" aslinda kirpmadir.
    eski_son = float((eski.get("son_kirpma") or {}).get("bitis_s") or toplam) if (eski.get("son_kirpma") or {}).get("yapildi") else toplam
    if float(k["bit"]) >= min(toplam, eski_son) - 0.3:
        yeni["son_kirpma"] = {"yapildi": True, "bitis_s": round(float(k["bas"]), 3),
                              "gerekce": "05.10.2026 dogrulama: " + k.get("gerekce", "")}
        continue
    if float(k["bas"]) <= 0.3:
        yeni["bas_kirpma"] = {"yapildi": True, "baslangic_s": round(float(k["bit"]), 3),
                              "gerekce": "05.10.2026 dogrulama: " + k.get("gerekce", "")}
        continue
    y = {"bas": round(float(k["bas"]), 3), "bit": round(float(k["bit"]), 3),
         "tur": k.get("tur", "model"), "supheli": False, "kesin": True,
         "gerekce": k.get("gerekce", "")}
    if k.get("talimat") not in (None, "", "null"):
        y["talimat"] = k["talimat"]
    yeni["kesimler"].append(y)
yeni["supheli"] = (eski.get("supheli") or []) + (n.get("supheli") or []) + \
    [{"bas": b["bas"], "bit": b["bit"], "gerekce": "birakildi: " + b.get("neden", "")}
     for b in (n.get("birakilan") or [])]
yeni["yeniden_tarama"] = "05.10.2026 kelime zamanli dogrulama"
json.dump(yeni, open(mk_yol, "w"), ensure_ascii=False, indent=1)

vid = os.path.basename(p).split("-")[-1]
k = json.load(open(os.path.expanduser("~/camp-video/takip/ders_kayitlari.json")))["kayit"]
loom = next(x["loom_vid"] for x in k if x["loom_vid"].startswith(vid))
r = subprocess.run(["python3", os.path.expanduser("~/camp-video/bin/hat.py"), loom, "--model", "--kuru"],
                   capture_output=True, text=True)
if r.returncode != 0:
    print("HATA hat.py:", (r.stdout + r.stderr)[-600:]); sys.exit(3)
edl = json.load(open(os.path.join(edit, "edl.json")))
d = [x for x in edl["ranges"] if x["source"] == "DERS"]
gaps = [(d[i]["end"], d[i + 1]["start"]) for i in range(len(d) - 1)]
sapma = []
for c in yeni["kesimler"]:
    g = min(gaps, key=lambda g: abs(g[0] - c["bas"]) + abs(g[1] - c["bit"]), default=None)
    if g is None or abs(g[0] - c["bas"]) > 0.4 or abs(g[1] - c["bit"]) > 0.4:
        sapma.append((c["bas"], c["bit"], g))
fazla = [g for g in gaps if not any(abs(g[0] - c["bas"]) <= 0.4 and abs(g[1] - c["bit"]) <= 0.4
                                    for c in yeni["kesimler"])]
print("%s: %d nihai kesim, EDL %d bosluk, sapan %d, fazladan %d"
      % (os.path.basename(p)[10:40], len(yeni["kesimler"]), len(gaps), len(sapma), len(fazla)))
for s in sapma: print("   SAPMA", s)
for g in fazla: print("   FAZLA", g)
sys.exit(2 if sapma or fazla else 0)

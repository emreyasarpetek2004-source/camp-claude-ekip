#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Kesit yeniden kesildiğinde (dolgu/duraklama kesimi) yönetmen planındaki zamanları yeni zaman çizelgesine taşır.

Çapa: kelimeler. Eski klip (klip_onceki.json) ile yeni klip.json'daki aynı kelimelerin başlangıçları eşlenir,
aradaki zamanlar doğrusal ara değerlenir. Kelime dizileri farklıysa difflib ile hizalanır.
Giriş (soru kartı, t < 2,9) ve kapanış sesleri (eski sürenin son 0,5 sn'si) kaydırılmaz / sona yapıştırılır.
yonetmen_NN.json yerinde güncellenir, öncesi yonetmen_NN.onceki.json'a yazılır.

Kullanım: python3 bin/zaman_esle.py <proje> --no 1
"""
import argparse
import bisect
import difflib
import json
import os
import shutil


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("proje")
    ap.add_argument("--no", type=int, required=True)
    a = ap.parse_args()
    e = os.path.join(os.path.abspath(a.proje), "edit")
    no = "%02d" % a.no
    kd = os.path.join(e, "klip_" + no)
    eski = json.load(open(os.path.join(kd, "klip_onceki.json")))
    yeni = json.load(open(os.path.join(kd, "klip.json")))
    yy = os.path.join(e, "yonetmen_%s.json" % no)
    plan = json.load(open(yy))

    # yönetmen planı kendi zaman çizelgesini (_parcalar) saklıyorsa o esas alınır: kaynak zamanı üzerinden KESİN eşleme.
    # (klip_onceki.json yalnız son kes.py çalışmasını tutar; aynı kesit iki kez kesilince yanlış taban olur, 9 Eki 2026)
    if plan.get("_parcalar"):
        def kaynaga(t, pp):
            p = [x for x in pp if x["cikis_bas"] <= t + 1e-6][-1]
            return p["bas"] + (t - p["cikis_bas"])

        def yeniye(sk):
            for x in yeni["parcalar"]:
                if x["bas"] - 1e-6 <= sk <= x["son"] + 1e-6:
                    return round(x["cikis_bas"] + sk - x["bas"], 3)
            sonraki = [x for x in yeni["parcalar"] if x["bas"] > sk]  # kesilen aralığa düştü: sonraki parçanın başı
            return round(sonraki[0]["cikis_bas"], 3) if sonraki else yeni["sure"]
        eski_sure = plan.get("_sure", eski["sure"])

        def f(t):
            if t <= 2.9:
                return t
            if t >= eski_sure - 0.5:
                return round(yeni["sure"] - (eski_sure - t), 3)
            return yeniye(kaynaga(t, plan["_parcalar"]))
        capa_yok = True
    else:
        capa_yok = False
    ew, nw = eski["kelimeler"], yeni["kelimeler"]
    sm = difflib.SequenceMatcher(None, [w["w"] for w in ew], [w["w"] for w in nw], autojunk=False)
    capa = [(0.0, 0.0)]
    idx = {}
    for blk in sm.get_matching_blocks():
        for k in range(blk.size):
            i, j = blk.a + k, blk.b + k
            capa.append((ew[i]["b"], nw[j]["b"]))
            capa.append((ew[i]["e"], nw[j]["e"]))
            idx[i] = j
    capa.append((eski["sure"], yeni["sure"]))
    capa = sorted(set(capa))
    xs = [c[0] for c in capa]

    def f_kelime(t):
        if t <= 2.9:
            return t
        if t >= eski["sure"] - 0.5:
            return round(yeni["sure"] - (eski["sure"] - t), 3)
        i = bisect.bisect_right(xs, t) - 1
        i = max(0, min(i, len(capa) - 2))
        (x0, y0), (x1, y1) = capa[i], capa[i + 1]
        return round(y0 + (t - x0) * (y1 - y0) / (x1 - x0), 3) if x1 > x0 else round(y0, 3)

    if not capa_yok:
        f = f_kelime
    shutil.copy(yy, yy.replace(".json", ".onceki.json"))
    for x in plan.get("eklemeler", []):
        x["bas"], x["bit"] = f(x["bas"]), f(x["bit"])
    for z in plan.get("zoom", []):
        z["bas"], z["bit"] = f(z["bas"]), f(z["bit"])
    for s in plan.get("sfx", []):
        s["t"] = f(s["t"])
    for k in ("vurgu", "gizle"):
        if k in plan:
            plan[k] = sorted({idx[i] for i in plan[k] if i in idx})
    plan["_parcalar"] = [{"bas": x["bas"], "son": x["son"], "cikis_bas": x["cikis_bas"]} for x in yeni["parcalar"]]
    plan["_sure"] = yeni["sure"]
    json.dump(plan, open(yy, "w"), ensure_ascii=False, indent=1)
    print("yönetmen %s: %.1f sn -> %.1f sn, %d kelime eşlendi / %d" % (no, eski["sure"], yeni["sure"], len(idx), len(ew)))


if __name__ == "__main__":
    main()

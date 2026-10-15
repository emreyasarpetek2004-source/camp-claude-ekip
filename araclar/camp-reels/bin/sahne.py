#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v2: yönetmen JSON'unu (edit/yonetmen_NN.json) doğrulayıp render'a hazır sahne_NN.json'a çevirir.

- ai_gorsel / acik_kaynak istekleri: edit/assets/NN/CREDITS.json'da dogrulandi=true dosyası varsa `gorsel`e döner,
  yoksa istek edit/gorsel_istek_NN.json'a yazılır ve ekleme ŞİMDİLİK çıkarılır (render görselsiz de çalışır).
- Kurallar zorlanır: zaman sınırı, çakışma (sonraki kırpılır/atılır), en kısa 2,2 sn, metin uzunlukları, em tire,
  SFX aralığı, vurgu indeksleri, kapanış.
Kullanım: python3 bin/sahne.py <proje> --no 1        (çıkış kodu 2 = bekleyen görsel isteği var)
"""
import argparse
import json
import os
import re
import sys

EMOJI_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "emoji")
TWEMOJI = "https://cdn.jsdelivr.net/gh/jdecked/twemoji@latest/assets/svg/%s.svg"


def emoji_dosya(e):
    """Emoji karakterini Twemoji SVG dosyasına çevirir (headless Chrome renkli emoji fontu içermiyor).
    Dosya adı Twemoji kuralı: kod noktaları küçük hex, '-' ile; FE0F tek başına eklenmez. İlk kullanımda indirilir."""
    import urllib.request
    cps = [c for c in e if ord(c) != 0xFE0F] if "\u200d" not in e else list(e)
    ad = "-".join("%x" % ord(c) for c in cps)
    yol = os.path.join(EMOJI_DIR, ad + ".svg")
    if not os.path.exists(yol):
        os.makedirs(EMOJI_DIR, exist_ok=True)
        try:
            req = urllib.request.Request(TWEMOJI % ad, headers={"User-Agent": "CAMP-REELS/1.0"})
            open(yol, "wb").write(urllib.request.urlopen(req, timeout=20).read())
        except Exception:
            return None
    return "emoji/%s.svg" % ad


UZUNLUK = {"deger": 10, "etiket": 30, "alt": 34, "metin": 48, "baslik": 30, "madde": 28, "aciklama": 32}
SESLER = {"whoosh", "swoosh_out", "pop", "tick", "ding", "riser", "shutter", "impact"}


def tire(s):
    return s.replace("—", ", ").replace("–", "-") if isinstance(s, str) else s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("proje")
    ap.add_argument("--no", type=int, required=True)
    a = ap.parse_args()
    edit = os.path.join(os.path.abspath(a.proje), "edit")
    no = "%02d" % a.no
    y = json.load(open(os.path.join(edit, "yonetmen_%s.json" % no)))
    klip = json.load(open(os.path.join(edit, "klip_%s" % no, "klip.json")))
    sure = klip["sure"]
    nk = len(klip["kelimeler"])
    uyar = []

    cred_y = os.path.join(edit, "assets", no, "CREDITS.json")
    cred = {c["id"]: c for c in (json.load(open(cred_y)) if os.path.exists(cred_y) else []) if c.get("id")}

    eklemeler, istek = [], []
    for e in sorted(y.get("eklemeler", []), key=lambda e: e["bas"]):
        e = {k: tire(v) for k, v in e.items()}
        if e["tip"] in ("ai_gorsel", "acik_kaynak"):
            c = cred.get(e.get("id"))
            if c and c.get("dogrulandi") and c.get("dosya"):
                e = {"tip": "gorsel", "bas": e["bas"], "bit": e["bit"], "dosya": "assets/%s/%s" % (no, c["dosya"]),
                     "aciklama": e.get("aciklama"), "kunye": c.get("kunye")}
            else:
                if not c:
                    istek.append(e)
                uyar.append("görsel yok, çıkarıldı: %s %s" % (e.get("id"), e["tip"]))
                continue
        e["bas"] = round(max(3.0 if e["tip"] != "slayt_zoom" else 2.9, e["bas"]), 2)
        e["bit"] = round(min(sure - 0.8, e["bit"]), 2)
        if e["bit"] - e["bas"] < 2.2:
            uyar.append("çok kısa, atıldı: %s @%.1f" % (e["tip"], e["bas"]))
            continue
        if eklemeler and e["tip"] != "slayt_zoom":
            onceki = [x for x in eklemeler if x["tip"] != "slayt_zoom"]
            if onceki and e["bas"] < onceki[-1]["bit"] + 0.8:
                yeni_bas = onceki[-1]["bit"] + 0.8
                if e["bit"] - yeni_bas < 2.2:
                    uyar.append("çakışma, atıldı: %s @%.1f" % (e["tip"], e["bas"]))
                    continue
                e["bas"] = round(yeni_bas, 2)
        for k, sinir in UZUNLUK.items():
            if isinstance(e.get(k), str) and len(e[k]) > sinir:
                uyar.append("uzun metin (%s %d>%d): %s" % (k, len(e[k]), sinir, e[k]))
        if e["tip"] == "adimlar":
            e["maddeler"] = [tire(m) for m in e["maddeler"][:4]]
            for m in e["maddeler"]:
                if len(m) > UZUNLUK["madde"]:
                    uyar.append("uzun madde: %s" % m)
        if e["tip"] == "slayt_zoom" and klip["duzen"] in ("konusmaci", "gorsel"):
            uyar.append("slayt yok, slayt_zoom atıldı")
            continue
        if e.get("emoji"):
            ed = emoji_dosya(e["emoji"])
            if ed:
                e["emoji_dosya"] = ed
            else:
                uyar.append("emoji indirilemedi: %s" % e["emoji"])
        eklemeler.append(e)

    sfx, son_t = [], -9
    for s in sorted(y.get("sfx", []), key=lambda s: s["t"]):
        if s["ses"] not in SESLER:
            uyar.append("bilinmeyen ses: %s" % s["ses"])
            continue
        t = s["t"]
        if t > 2.9 and t < sure and t - son_t < 1.2:
            continue
        if t >= sure:
            pass  # kapanış sesleri
        sfx.append({"t": round(t, 2), "ses": s["ses"], "seviye": min(0.45, max(0.15, s.get("seviye", 0.3)))})
        if t < sure:
            son_t = t
    # görselsiz kalan eklemenin sesi de gitsin: ekleme başlangıcına 0,3 sn'den yakın olmayan whoosh'ları ayıkla
    bas_lar = [e["bas"] for e in eklemeler] + [0.0, 2.6] + [z["bas"] for z in y.get("zoom", [])]
    sfx = [s for s in sfx if s["t"] >= sure - 0.5 or s["ses"] not in ("whoosh", "pop", "ding", "impact", "tick")
           or any(abs(s["t"] - b) <= 0.35 for b in bas_lar)]

    zoom = [z for z in y.get("zoom", []) if z["bit"] <= sure and 1.0 < z["olcek"] <= 1.15][:4]
    vurgu = sorted({i for i in y.get("vurgu", []) if 0 <= i < nk})
    sk = y.get("soru_karti") or {"metin": klip.get("soru") or "", "bas": 0, "bit": 2.7}
    sk["metin"] = tire(sk.get("metin", ""))
    if len(sk["metin"].replace("*", "")) > 64:
        uyar.append("soru uzun: %d" % len(sk["metin"]))
    gizle = sorted({i for i in y.get("gizle", []) if 0 <= i < nk})  # hocanın sürçmesi: ses kalır, altyazıda gösterilmez
    sahne = {"soru_karti": sk, "vurgu": vurgu, "gizle": gizle, "eklemeler": eklemeler, "zoom": zoom, "sfx": sfx,
             "kapanis": y.get("kapanis") or {"sure": 2.2}, "tepe": []}
    if not sahne["kapanis"].get("baslik"):
        sahne["kapanis"]["baslik"] = klip.get("webinar")

    # düzen "gorsel": üst panel slayt yerine doğrulanmış görsellerden akış; her biri ~5,5 sn, sırayla döner
    if klip["duzen"] == "gorsel":
        havuz = [c for c in cred.values() if c.get("dogrulandi") and c.get("dosya")]
        tepe, t, i = [], 0.0, 0
        if havuz:
            while t < sure:
                c = havuz[i % len(havuz)]
                tepe.append({"dosya": "assets/%s/%s" % (no, c["dosya"]), "bas": round(t, 2), "bit": round(min(sure, t + 5.5), 2),
                             "kunye": c.get("kunye")})
                t += 5.5
                i += 1
        else:
            uyar.append("gorsel düzeni ama doğrulanmış görsel yok")
        sahne_tepe = tepe
    else:
        sahne_tepe = []
    sahne["tepe"] = sahne_tepe
    for x in sahne_tepe[1:]:  # görsel geçişlerine hafif swoosh (yakında başka ses yoksa)
        if 3.5 < x["bas"] < sure - 1 and not any(abs(s_["t"] - x["bas"]) < 1.2 for s_ in sahne["sfx"]):
            sahne["sfx"].append({"t": x["bas"], "ses": "swoosh_out", "seviye": 0.2})
    sahne["sfx"].sort(key=lambda s_: s_["t"])

    # tempo raporu
    olay = sorted([0.0] + [e["bas"] for e in eklemeler] + [z["bas"] for z in zoom])
    bosluk = max([b - a for a, b in zip(olay, olay[1:])] + [sure - olay[-1]])
    if bosluk > 8:
        uyar.append("tempo: %.1f sn olaysız boşluk" % bosluk)

    json.dump(sahne, open(os.path.join(edit, "sahne_%s.json" % no), "w"), ensure_ascii=False, indent=1)
    if istek:
        json.dump(istek, open(os.path.join(edit, "gorsel_istek_%s.json" % no), "w"), ensure_ascii=False, indent=1)
    print("sahne %s: %d ekleme, %d zoom, %d sfx, en uzun boşluk %.1f sn" % (no, len(eklemeler), len(zoom), len(sfx), bosluk))
    for u in uyar:
        print("  ! " + u)
    if istek:
        print("  bekleyen görsel isteği: %d -> %s" % (len(istek), os.path.join(edit, "gorsel_istek_%s.json" % no)))
    sys.exit(2 if istek else 0)


if __name__ == "__main__":
    main()

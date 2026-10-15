#!/usr/bin/env python3
"""AUSCAMP Ders Çekim grubundan Loom linklerini ve kesim talimatlarını çeker.

Salt okunur: campwa sözleşmesi gereği hiçbir mesaj gönderilmez, silinmez.
Tek Chrome oturumu kuralı için WaLock alınır.

Kullanım:
    python3 bin/wa_ders_cek.py --scroll 30
    python3 bin/wa_ders_cek.py --gun 60 --out takip/ders_kayitlari.json

Çıktı: her Loom linki için bir kayıt. Talimat metni HAM haliyle saklanır;
zaman jetonları yalnız ADAY olarak çıkarılır, kesim kararı burada verilmez.
"""
import argparse
import json
import os
import re
import sys
import time

sys.path.insert(0, os.path.expanduser("~/camp-wa-core"))

from campwa import wa
from campwa.lock import WaLock

GRUP_ADI = "AUSCAMP Ders Çekim"
LOOM = re.compile(r"https?://(?:www\.)?loom\.com/share/([0-9a-f]{20,40})", re.I)

# Zaman jetonu adayları. Karar vermez, sadece işaret eder.
JETONLAR = [
    # 12:30, 1:02:30
    (re.compile(r"\b(\d{1,2}):(\d{2})(?::(\d{2}))?\b"), "saat_biçimi"),
    # 12. dk, 12 dakika, 12.dakikadan
    (re.compile(r"\b(\d{1,3})\s*\.?\s*(?:dk|dakika\w*)\b", re.I), "dakika"),
    # 90 sn, 90 saniye
    (re.compile(r"\b(\d{1,4})\s*\.?\s*(?:sn|saniye\w*)\b", re.I), "saniye"),
]


def jeton_saniye(kind, m):
    if kind == "saat_biçimi":
        a, b, c = m.group(1), m.group(2), m.group(3)
        if c is not None:
            return int(a) * 3600 + int(b) * 60 + int(c)
        return int(a) * 60 + int(b)
    if kind == "dakika":
        return int(m.group(1)) * 60
    if kind == "saniye":
        return int(m.group(1))
    return None


def zaman_adaylari(metin):
    out = []
    for rx, kind in JETONLAR:
        for m in rx.finditer(metin or ""):
            out.append({
                "ham": m.group(0),
                "tur": kind,
                "saniye": jeton_saniye(kind, m),
                "konum": m.start(),
            })
    out.sort(key=lambda x: x["konum"])
    return out


def grubu_bul(s):
    adaylar = wa.find_chats(s, GRUP_ADI) or []
    gruplar = [c for c in adaylar if c.get("isGroup")]
    if not gruplar:
        gruplar = [c for c in (wa.groups(s) or [])
                   if GRUP_ADI.lower() in (c.get("name") or "").lower()]
    if not gruplar:
        raise SystemExit("HATA: '%s' grubu bulunamadi. WhatsApp Web acik mi?" % GRUP_ADI)
    if len(gruplar) > 1:
        print("UYARI: birden fazla eslesme, ilki kullanilyor:")
        for g in gruplar:
            print("   -", g.get("name"), g.get("id"))
    return gruplar[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scroll", type=int, default=25,
                    help="gecmise kac sayfa kaydirilacak (varsayilan 25)")
    ap.add_argument("--gun", type=int, default=0,
                    help="son N gunun mesajlari (0 = yuklenen tum gecmis)")
    ap.add_argument("--out", default=os.path.expanduser(
        "~/camp-video/takip/ders_kayitlari.json"))
    ap.add_argument("--takip-mesaj", type=int, default=15,
                    help="link sonrasi kac mesaj talimat olarak toplanacak")
    args = ap.parse_args()

    since_ms = 0
    if args.gun:
        since_ms = int((time.time() - args.gun * 86400) * 1000)

    with WaLock("camp-video"):
        s = wa.connect()
        wa.assert_alive(s)
        grup = grubu_bul(s)
        print("Grup:", grup.get("name"), grup.get("id"))

        wa.load_chat(s, grup["id"], max_earlier=args.scroll)
        msgs = wa.chat_messages(s, grup["id"], since_ms, limit=2000)
        print("Mesaj:", len(msgs))

    # Loom linki tasiyan mesajlarin indeksleri
    link_idx = [i for i, m in enumerate(msgs) if LOOM.search(m.get("body") or "")]
    kayitlar = []
    for n, i in enumerate(link_idx):
        m = msgs[i]
        body = m.get("body") or ""
        vid = LOOM.search(body).group(1)
        # Talimat penceresi: bu mesajdan sonraki mesajlar, bir sonraki linke kadar
        son = link_idx[n + 1] if n + 1 < len(link_idx) else len(msgs)
        son = min(son, i + 1 + args.takip_mesaj)
        pencere = [msgs[i]] + msgs[i + 1:son]
        talimat = []
        for p in pencere:
            t = (p.get("body") or "").strip()
            if not t:
                continue
            talimat.append({
                "ts_ms": p.get("tsMs"),
                "yazan": p.get("authorName") or p.get("author"),
                "metin": t,
                "zaman_adaylari": zaman_adaylari(t),
            })
        kayitlar.append({
            "loom_vid": vid,
            "url": "https://www.loom.com/share/%s" % vid,
            "link_ts_ms": m.get("tsMs"),
            "link_tarih": time.strftime("%d.%m.%Y %H:%M",
                                        time.localtime((m.get("tsMs") or 0) / 1000)),
            "paylasan": m.get("authorName") or m.get("author"),
            "talimat_ham": talimat,
        })

    out = os.path.expanduser(args.out)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as f:
        json.dump({"grup": grup.get("name"), "cekim_ts": int(time.time()),
                   "kayit": kayitlar}, f, ensure_ascii=False, indent=1)

    print("Loom linki:", len(kayitlar), "->", out)
    for k in kayitlar[-5:]:
        ad = len([a for t in k["talimat_ham"] for a in t["zaman_adaylari"]])
        print("  %s  %s  talimat mesaji=%d  zaman adayi=%d"
              % (k["link_tarih"], k["loom_vid"][:8], len(k["talimat_ham"]), ad))


if __name__ == "__main__":
    main()

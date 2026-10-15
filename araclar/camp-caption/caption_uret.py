#!/usr/bin/env python3
"""
CAMP GROUP caption ureticisi -- Claude API ile 5 varyant.

Ne yapar: Asana'daki (ya da elle verilen) postu alir, markanin caption-uretici
agent tanimini + marka rehberini system prompt olarak yollar, 5 caption varyanti
uretir ve ekrana + dosyaya yazar.

Ne YAPMAZ: yayinlamaz, zamanlamaz, Asana'ya yazmaz. Caption'i kullanıcı secer.
(bkz. feedback-auscamp-onaysiz-planlama-yok / feedback-auscamp-paylas-akisi)

TASARIM -- marka kurallari burada YAZILI DEGIL:
Kurallar zaten ~/.claude/agents/<marka>-caption-uretici.md ve marka rehberinde
duruyor. Script bu dosyalari calisma aninda okuyup system prompt'a koyar. Boylece
tek kaynak vardir: agent tanimi guncellenince bu script de guncellenmis olur.
Kurallari buraya kopyalamak iki yerde tutmak demekti -- er ya da geç ayrisirlardi.

Prompt caching: marka rehberi buyuk ve her cagride ayni -> system blogunun sonuna
cache_control konur. Postun kendisi (degisken kisim) user mesajinda, cache'lenen
prefix'ten SONRA gelir. Ters sirada olsa cache hic tutmazdi.

Kurulum:
    pip install anthropic
    # API anahtari: ANTHROPIC_API_KEY ya da `ant auth login` profili.
    # Anthropic() ikisini de kendisi bulur.

Kullanim:
    # Asana task'indan (tercih edilen -- post zaten Asana'da hazir)
    python3 caption_uret.py --marka auscamp --task 1211234567890

    # Elle metinden
    python3 caption_uret.py --marka dentcamp --metin "15.08 Almanya Approbation sureci..."
    python3 caption_uret.py --marka ukcamp --dosya post.txt

    # Tek varyant
    python3 caption_uret.py --marka auscamp --task 121... --adet 1
"""

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

HOME = os.path.expanduser("~")
MODEL = "claude-opus-5"
MAX_TOKENS = 16000  # streaming'siz guvenli ust sinir (SDK HTTP timeout'u altinda)

# Marka -> (agent tanimi, ek baglam dosyalari, asana token yolu)
# Yollar agent tanimlarindaki "ZORUNLU oku" satirlarindan alindi.
MARKALAR = {
    "auscamp": {
        "agent": f"{HOME}/.claude/agents/auscamp-caption-uretici.md",
        "baglam": [f"{HOME}/Documents/AUSCAMP Claude/01_Caption_ve_Dil_Rehberi.md"],
        "asana_token": f"{HOME}/Documents/AUSCAMP Claude/.asana_token",
    },
    "ukcamp": {
        "agent": f"{HOME}/.claude/agents/ukcamp-caption-uretici.md",
        "baglam": [f"{HOME}/Documents/UKCAMP Claude/01_Caption_ve_Dil_Rehberi.md"],
        "asana_token": f"{HOME}/Documents/UKCAMP Claude/.asana_token",
    },
    "dentcamp": {
        "agent": f"{HOME}/.claude/agents/dentcamp-caption-uretici.md",
        "baglam": [
            f"{HOME}/.claude/skills/dentcamp-marka-sesi/SKILL.md",
            f"{HOME}/Documents/DENTCAMP Claude/01_Caption_ve_Dil_Rehberi.md",
        ],
        "asana_token": f"{HOME}/Documents/DENTCAMP Claude/.asana_token",
    },
}

CAPTION_SEMA = {
    "type": "object",
    "properties": {
        "varyantlar": {
            "type": "array",
            "description": "Caption varyantlari, istenen sirayla.",
            "items": {
                "type": "object",
                "properties": {
                    "no": {"type": "integer", "description": "1'den baslayan sira"},
                    "aci": {
                        "type": "string",
                        "description": "Hook acisi: soru / mit / surec / karar-kriteri / biliyor-muydunuz vb.",
                    },
                    "caption": {
                        "type": "string",
                        "description": (
                            "Yayina hazir caption'in TAMAMI: hook, govde, imza, CTA, hashtag. "
                            "Satir aralilari (bos satirlar) agent tanimindaki Bicimlendirme "
                            "kuralina gore gercek newline olarak korunur."
                        ),
                    },
                },
                "required": ["no", "aci", "caption"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["varyantlar"],
    "additionalProperties": False,
}


def oku(path, zorunlu=True):
    if not os.path.exists(path):
        if zorunlu:
            sys.exit(
                f"HATA: gerekli dosya yok: {path}\n"
                "  Marka rehberi ya da agent tanimi tasinmis olabilir -- MARKALAR sozlugunu guncelle."
            )
        return None
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def frontmatter_sil(metin):
    """Agent .md dosyasinin basindaki YAML frontmatter'ini at, govdeyi dondur.

    Frontmatter model icin gurultu: name/description/tools alanlari Claude Code'un
    agent kaydi icin, caption yazari icin degil.
    """
    if metin.startswith("---"):
        parcalar = metin.split("---", 2)
        if len(parcalar) == 3:
            return parcalar[2].lstrip("\n")
    return metin


def system_bloklari(marka):
    """System prompt'u kurar. Son bloga cache_control konur -> tools+system cache'lenir."""
    cfg = MARKALAR[marka]
    bloklar = [
        {
            "type": "text",
            "text": (
                "Asagida bir Instagram caption yazarinin gorev tanimi ve marka rehberi var. "
                "Bu kurallara BIREBIR uy. Kurallarla bu mesajdaki talimat catisirsa kurallar kazanir.\n\n"
                "=== GOREV TANIMI ===\n" + frontmatter_sil(oku(cfg["agent"]))
            ),
        }
    ]
    for yol in cfg["baglam"]:
        bloklar.append(
            {
                "type": "text",
                "text": f"=== REFERANS: {os.path.basename(yol)} ===\n" + oku(yol),
            }
        )
    # Cache breakpoint: buraya kadarki her sey her cagride ayni.
    bloklar[-1]["cache_control"] = {"type": "ephemeral"}
    return bloklar


# --- Asana ---------------------------------------------------------------


def asana_task(marka, gid):
    """Task'in adini ve notes'unu ceker. Caption kaynagi post'un kendisidir."""
    token_yolu = MARKALAR[marka]["asana_token"]
    ham = oku(token_yolu, zorunlu=False)
    if not ham:
        sys.exit(
            f"HATA: Asana token'i yok: {token_yolu}\n"
            "  --task yerine --metin / --dosya kullanabilirsin."
        )
    token = ham.strip()

    url = f"https://app.asana.com/api/1.0/tasks/{gid}?opt_fields=name,notes,due_on,permalink_url"
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode("utf-8"))["data"]
    except urllib.error.HTTPError as exc:
        govde = exc.read().decode("utf-8", "replace")
        if exc.code == 401:
            sys.exit(f"HATA (401): Asana token'i reddedildi ({token_yolu}).")
        if exc.code == 404:
            sys.exit(f"HATA (404): task bulunamadi: {gid}\n  GID dogru mu? Yanit: {govde}")
        sys.exit(f"HATA ({exc.code}) Asana: {govde}")
    except urllib.error.URLError as exc:
        sys.exit(f"HATA: Asana'ya baglanilamadi: {exc.reason}")

    notlar = (data.get("notes") or "").strip()
    if not notlar:
        sys.exit(
            f"HATA: task '{data.get('name')}' bos (notes yok).\n"
            "  Caption kaynagi task'in brief'i -- bos task'tan caption uretmek uydurmak olur."
        )
    return data.get("name") or "", notlar, data.get("permalink_url") or ""


# --- Claude --------------------------------------------------------------


def uret(marka, baslik, govde, adet):
    try:
        import anthropic
    except ImportError:
        sys.exit("HATA: anthropic paketi yok. Kur: pip install anthropic")

    # Anahtari ANTHROPIC_API_KEY'den ya da `ant auth login` profilinden alir.
    client = anthropic.Anthropic()

    istek = (
        f"Asagidaki post icin {adet} caption varyanti uret.\n\n"
        f"POST BASLIGI: {baslik or '(yok)'}\n\n"
        f"POST ICERIGI (Asana brief'i -- olgular BUNDAN gelir, "
        f"disindan bilgi/rakam EKLEME):\n{govde}\n\n"
        f"Kurallar: {adet} varyantin hepsi ayni konuya, ayni olgulara, ayni CTA ve "
        f"hashtag mantigina sadik kalir; yalnizca hook ve govde acisi degisir. "
        f"Satir aralarini (bos satirlari) gercek newline olarak yaz -- kopyala-yapistir hazir olsun."
    )

    try:
        yanit = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            thinking={"type": "adaptive"},
            output_config={
                "effort": "high",
                "format": {"type": "json_schema", "schema": CAPTION_SEMA},
            },
            system=system_bloklari(marka),
            messages=[{"role": "user", "content": istek}],
        )
    except anthropic.AuthenticationError:
        sys.exit(
            "HATA: Claude API kimlik dogrulamasi basarisiz.\n"
            "  ANTHROPIC_API_KEY'i export et ya da `ant auth login` yap."
        )
    except anthropic.RateLimitError as exc:
        bekle = exc.response.headers.get("retry-after", "?")
        sys.exit(f"HATA: hiz siniri. {bekle} sn sonra tekrar dene.")
    except anthropic.APIStatusError as exc:
        sys.exit(f"HATA (API {exc.status_code}): {exc.message}")
    except anthropic.APIConnectionError:
        sys.exit("HATA: Claude API'ye baglanilamadi (ag).")

    if yanit.stop_reason == "refusal":
        kategori = getattr(yanit.stop_details, "category", None) if yanit.stop_details else None
        sys.exit(f"HATA: model istegi reddetti (kategori: {kategori}).")
    if yanit.stop_reason == "max_tokens":
        sys.exit(
            f"HATA: cikti {MAX_TOKENS} token sinirina takildi, JSON yarim kaldi.\n"
            "  --adet dusur ya da MAX_TOKENS'i buyut (>16000 icin streaming gerekir)."
        )

    metin = next((b.text for b in yanit.content if b.type == "text"), None)
    if not metin:
        sys.exit("HATA: yanitta metin blogu yok.")
    return json.loads(metin)["varyantlar"], yanit.usage


def main():
    ap = argparse.ArgumentParser(description="CAMP GROUP caption ureticisi (Claude API)")
    ap.add_argument("--marka", required=True, choices=sorted(MARKALAR))
    kaynak = ap.add_mutually_exclusive_group(required=True)
    kaynak.add_argument("--task", help="Asana task GID -- post'u oradan ceker")
    kaynak.add_argument("--metin", help="Post icerigini dogrudan ver")
    kaynak.add_argument("--dosya", help="Post icerigini dosyadan oku (utf-8)")
    ap.add_argument("--adet", type=int, default=5, help="Varyant sayisi (varsayilan 5)")
    ap.add_argument("--out", help="Cikti dosyasi (varsayilan caption_<marka>.txt)")
    args = ap.parse_args()

    if args.adet < 1 or args.adet > 10:
        sys.exit("HATA: --adet 1-10 arasinda olmali.")

    baslik, permalink = "", ""
    if args.task:
        baslik, govde, permalink = asana_task(args.marka, args.task)
    elif args.dosya:
        govde = oku(args.dosya).strip()
    else:
        govde = args.metin.strip()
    if not govde:
        sys.exit("HATA: post icerigi bos.")

    print(f"Marka   : {args.marka}")
    if baslik:
        print(f"Post    : {baslik}")
    if permalink:
        print(f"Asana   : {permalink}")
    print(f"Varyant : {args.adet}")
    print(f"Kaynak  : {len(govde)} karakter brief")
    print("Uretiliyor...\n")

    varyantlar, usage = uret(args.marka, baslik, govde, args.adet)

    if len(varyantlar) != args.adet:
        print(
            f"UYARI: {args.adet} istendi, {len(varyantlar)} geldi. Sema adet zorlayamiyor "
            f"(JSON Schema'da minItems/maxItems desteklenmiyor) -- gelenler asagida.\n"
        )

    out = args.out or f"caption_{args.marka}.txt"
    with open(out, "w", encoding="utf-8") as fh:
        for v in varyantlar:
            blok = "=" * 72
            print(blok)
            print(f"VARYANT {v['no']}  ({v['aci']})")
            print(blok)
            print(v["caption"])
            print()
            fh.write(f"--- VARYANT {v['no']} ({v['aci']}) ---\n{v['caption']}\n\n")

    print(f"Dosyaya yazildi: {out}")
    print(
        f"Token: girdi {usage.input_tokens} · cikti {usage.output_tokens} · "
        f"cache yazma {usage.cache_creation_input_tokens} · cache okuma {usage.cache_read_input_tokens}"
    )
    if usage.cache_read_input_tokens == 0 and usage.cache_creation_input_tokens == 0:
        print(
            "  NOT: cache hic tutmadi -- marka rehberi cache alt sinirinin altinda olabilir."
        )

    print("\nSIRADAKI ADIM (elle):")
    if args.marka == "dentcamp":
        print(f"  python3 ~/.claude/skills/camp-humanize/humanize_check.py {out} --marka dentcamp")
        print("  MARKA bulgulari bloklayicidir -- duzeltmeden yayina gitmez.")
    else:
        print(f"  python3 ~/.claude/skills/camp-humanize/humanize_check.py {out} --marka {args.marka}")
    print("  Sonra kullanıcı bir varyant secer; yayin ayri adim (bu script yayinlamaz).")


if __name__ == "__main__":
    main()

---
name: camp-humanize
description: Use when writing or reviewing any CAMP GROUP marketing copy in Turkish — Instagram caption, tasarım brief'i, web metni, reklam metni, e-posta — for AUSCAMP, UKCAMP or DENTCAMP. Also use when text reads as AI-generated, sounds robotic or bureaucratic, or when the user says "yapay zeka gibi durmuş", "kurumsal kaçmış", "hümanize et", "AI kokuyor".
---

# CAMP GROUP — Hümanize Geçişi

Kurumsal metni insan ağzından çıkmış hâle getirir. İki katman: makine literal kalıpları yakalar, sen ritmi ve somutluğu düzeltirsin.

**Çekirdek ilke:** İnsan düzensiz yazar. AI simetrik yazar. Simetriyi boz.

## Sıra

1. **Metni bir dosyaya yaz**, sonra tara:
   ```bash
   python3 ~/.claude/skills/camp-humanize/humanize_check.py metin.txt --marka dentcamp
   ```
   `--marka` seçenekleri: `dentcamp`, `auscamp`, `ukcamp`. Marka kuralı gerekmiyorsa bayrağı at.

2. **Her bulguyu düzelt.** MARKA bulguları bloklayıcıdır — düzeltmeden yayına gitmez.

3. **Ritmi elle geçir** (script yakalayamaz — aşağıdaki kurallar).

4. **Tek satır özet ver:** ne değişti. Olgulara, rakamlara ve CTA bloğuna dokunma.

## Ritim kuralları (yargı işi)

| Kural | Nasıl uygulanır |
|---|---|
| **Cümle uzunluğu değişsin** | Kısa, uzun, kısa. Hepsi ±3 kelime içindeyse metin makine gibi okunuyor. |
| **Bir tane çok kısa cümle** | Tek başına duran. Bunun gibi. |
| **Bağlaçla başla** | "Ama", "Çünkü", "Yine de" ile cümle açmak serbest. |
| **Somut > genel** | "Melbourne'da tek merkez" ✅ · "sınırlı sayıda merkez" ❌ |
| **Simetriyi boz** | Üç madde aynı kalıpta kurulmasın; biri farklı uzunlukta olsun. |
| **Sayı kaynağıyla anlamlı** | Kaynaksız rakam yazma. Rakam yoksa nitel anlat. |

## Yaygın hata

**En sık yapılan:** bulguları düzeltirken metni daha da cilalamak. Hümanize etmek *daha düzgün* yazmak değil, *daha az düzgün* yazmaktır. Düzeltilmiş metin öncekinden daha simetrikse yanlış yöne gitmişsin.

**İkinci sık hata:** olguyu değiştirmek. Sen üslubu düzeltirsin; rakam, tarih, süreç adımı ve CTA aynen kalır.

## Script neyi yakalar

Kalıp açılışlar ("Günümüzde", "Bilindiği üzere") · şişirme sıfatlar ("eşsiz", "titizlikle") · `sadece X değil aynı zamanda Y` antitezi · `-mektedir/-maktadır` · nominal şişme ("hazırlanması gerekmektedir") · satır başı mekanik bağlaçlar ("Ayrıca", "Sonuç olarak") · duygusal yükseltme ("hayalinizdeki", "yolculuğunuz") · retorik soru–cevap ikilisi · klişe kapanış · somut sayısız "birçok/çeşitli" · emoji fazlalığı (>6) · ardışık paralel maddeler · tek düze cümle uzunluğu · marka adı yazımı, yasak terimler, vaat sözleri, CTA bloğu.

Ayrıntı için: `humanize_check.py --help`

## Marka sesiyle ilişkisi

Bu skill **nasıl yazılmayacağını** söyler; markanın **ne söyleyeceğini** değil. DENTCAMP için ses tanımı ayrı: `dentcamp-marka-sesi` skill'i. Önce ses, sonra bu geçiş.

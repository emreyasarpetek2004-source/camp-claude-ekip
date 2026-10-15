# AUSCAMP — Asana Yapısı & Statik Post Üretim Otomasyonu Tasarımı

> 19 Haziran 2026, canlı AUSCAMP Asana projesi incelenerek hazırlandı.
> Proje: **AUSCAMP** (`<ID>`) — Workspace `<ID>` — 117 task (114 tamamlanmış).

---

## 1. MEVCUT ASANA YAPISI (gözlemlenen)

### Section'lar
| Section | GID | İçerik |
|---------|-----|--------|
| VİDEO | <ID> | Reklam videoları |
| TAKVİM | <ID> | Aylık takvim postları |
| **DOKTOR POST** | <ID> | **Ana statik post akışı (asıl üretim)** |
| **YAŞAM POST** | <ID> | Yaşam/kültür statik postları |
| Story | <ID> | (az kullanılıyor) |
| Video | <ID> | Reels + kapaklar |
| Misc | <ID> | Karışık |
| Untitled section | <ID> | Boş |

### Custom Field
- **Priority** (enum): High / Medium / Low — `<ID>`

### Ekip (atananlar)
- **Tasarımcı A** (`<ID>`) — tasarım, postların **çoğu** ona atanıyor
- **Tasarımcı B** (`<ID>`) — tasarım
- Tasarımcı C, ekip üyesi, koordinatör, video ekibi, ekip üyesi

### Gerçek Task İsimlendirme Deseni
```
GG.AA.YYYY, [kısa açıklama]
```
Örnekler (gerçek):
- `01.04.2026, Webinar post`
- `11.03.2026, pratisyen post`
- `25.03.2026, Denklik Post`
- `30.03.2026, Nisan webinar takvimi`
- `06.04.2026, Anita Gözübüyük AUSCAMP'te!`
- `25.03.2026, Avustralya'da Doktor Olmanın 10 Avantajı #3`

> Not: Context dosyasındaki "pipe" formatı (`[Tip]|[Segment]|[Konu]`) **gerçekte kullanılmıyor** — gerçek stil "tarih, açıklama". Otomasyon gerçek stile sadık kalmalı.

### Brief Formatı (task description) — İKİ TİP

**Tip A — Tam Carousel Brief** (bilgilendirme, başarı, 10 avantaj vb.) — GERÇEK ANATOMİ:
```
[Açılış notu — sade ekip tonu, KALP/SEVGİ EMOJİSİ YOK. Önceki örneği eklediğini belirt:
 "Selam, ... Serinin 7.'si için yaptığını ekledim, aynı şablon olsun. Eline sağlık, teşekkürler."]

SAYFA 1 – Kapak:
Başlık:
[Ana başlık]
Alt Başlık:
[BİLGİ/BAĞLAM veren alt başlık — kapak boş kalmaz, mutlaka alt başlık olur]
(Görsel yönü: koyu yeşil zemin, [ilgili görsel/illüstrasyon], arka planda flu Avustralya haritası/silüeti.
 "[anahtar kelime]" sarı highlight olabilir mi? Seri no varsa: üst sağ #N. Sağ alta 👉)

SAYFA 2:
Başlık:
[Alt başlık]
• [gerçek bilgi maddesi — rakam/veri dahil]
• [madde]
[kapanış/özet cümlesi]
(Görsel: [o slayta uygun görsel önerisi])

SAYFA 3:
... (aynı kalıp)

SON SAYFA – Kapanış:
AUSCAMP olarak ... yanınızdayız.
[SABİT CTA] Avustralya'da doktorluk hakkında detaylı bilgi almak için bize ulaşın.
📞 +90 552 253 03 37 (WhatsApp logosu)
🌐 www.auscamp.com.tr
[Ek dosyalar: referans/önceki örnek + varsa çekilen gerçek ilan/kaynak görseli]
```
**Kritik kurallar:** ① Kapakta Başlık + **Alt Başlık** zorunlu (bilgi içerir). ② Her slayta **(Görsel: ...)** notu. ③ Maddeler gerçek bilgi + rakam. ④ Mit-yıkma'da SAYFA 2 "Yanlış: '...'" (ortada, dikkat çekici) + alt maddeler; SAYFA 3 "Gerçek: '...'" + alt maddeler. ⑤ Açılışta önceki örnek eklenir, "aynı şablon" denir.

**Tip B — Şablon Güncelleme Brief** (tekrarlayan webinar/takvim):
```
Selamlaaar 😇
Ekteki tasarımı sadece [tarih/mentör/konu] olacak şekilde güncelleyebilir miyiz?
Çok teşekkürler şimdiden
```

### Teslim akışı
- Tasarımcı yorumda dosya/proof linki paylaşır → koordinatör onaylar ("eline sağlık 💓")
- Koordinasyon notu: "başlıklara teslim tarihlerini girelim" (koordinasyon) → tarih + teslim takibi isteniyor

---

## 2. STATİK POST ÜRETİM OTOMASYONU — TASARIM

### Akış
```
[Sen: konu + segment + tarih]  ←→  veya  [Sen: tema → Claude konu önerir]
        ↓
Claude: doğru ŞABLON TİPİNİ (T1–T10) seçer
        ↓
Claude: SAYFA-SAYFA brief üretir (görsel sisteme + caption diline sadık)
        ↓
Claude: caption + CTA + hashtag (segment bazlı) üretir
        ↓
Asana'ya task açar: "GG.AA.YYYY, [açıklama]" + brief (description) + Priority + Tasarımcı A'ya ata + due date
        ↓
[Sen onaylarsın → tasarımcı üretir → yorumda teslim]
```

### Otomasyonun üreteceği standart task (şablon)
- **Başlık:** `GG.AA.YYYY, [Konu] [#seri no varsa]`
- **Atanan:** Tasarımcı A (varsayılan) / Tasarımcı B
- **Due date:** yayın/teslim tarihi
- **Priority:** High (varsayılan)
- **Description (brief):**
  - Samimi açılış notu (marka içi ton)
  - Şablon tipi referansı (ör. "T3 Bilgilendirme — yeşil zemin, mevcut kapak stili")
  - SAYFA-SAYFA döküm (BAŞLIK + gövde + maddeler)
  - Görsel notlar (renk, segment ikonu, vurgu kelimeleri, next-arrow)
  - Caption + CTA + hashtag (ayrı blok)
- **Ekler:** referans görsel/montaj linki (gerekirse)

### Şablon tipi → brief eşleştirmesi
| İçerik | Şablon | Brief tipi |
|--------|--------|-----------|
| Webinar duyurusu | T1 | B (güncelleme) |
| Aylık takvim | T2 | B/A karması |
| Bilgilendirme/yaşam | T3 | A (tam) |
| Mit-yıkma | T4 | A (tam) |
| Başarı/denklik | T5 | A (tam) |
| Mentör tanıtım | T6 | A (tam) |
| Ekip | T7 | A (tam) |
| Hizmet/işbirliği | T8 | A (tam) |
| Canlı yayın | T9 | B |
| Kampanya | T10 | A (tam) |

---

## 3. ÖNERİLEN İYİLEŞTİRMELER (opsiyonel, onayına bağlı)
1. **Custom field eklenebilir:** `Segment` (Uzman/Pratisyen/Diş/NZ/Yaşam), `Kanal` (Statik/Carousel/Webinar), `İçerik Tipi` (T1–T10) → filtreleme + raporlama
2. **Teslim tarihi** başlığa veya ayrı alana (koordinasyonun isteği)
3. **Brief şablonu** standardı (Tip A/B) — otomasyon zaten bunu üretecek
4. Section'lar tip bazlı kalabilir; istenirse aşama bazlı (Brief→Tasarım→Onay→Planlandı→Yayında) bir görünüm eklenebilir

> Bu değişiklikler canlı Asana'da YAZMA gerektirir — yalnızca onayınla yapılır.
---

## ⛔ KAPSAM SINIRI — KARARI KULLANICININ VERDİĞİ POSTLAR (18.08.2026, GLOBAL — AUSCAMP · UKCAMP · DENTCAMP)

Bu tipler **kullanıcı açıkça istemedikçe üretilmez, önerilmez, planlanmaz, Asana'ya girilmez**:
yeni hoca/mentör/eğitmen/ekip tanıtımı · webinar–etkinlik–canlı yayın duyurusu ve takvimi · kampanya/indirim/fiyat · lansman ve yeni hizmet-ürün duyurusu · iş birliği duyurusu · danışan başarısı/tebrik postu.

Otomasyonun serbest üretim kapsamı = **bilgilendirme/eğitici içerik** (süreç, sınav, denklik, karşılaştırma, yaşam, kariyer, mit-yıkma, olgu kartı, mevcut hizmet anlatımı). Boş slot doldurmak için bu tiplere başvurulmaz.

**AUSCAMP ek sınırı:** **Diş hekimliği içeriği AUSCAMP'te yok** (18.08.2026). ADC yolu, diş hekimi denkliği, "Diş" segmenti → tamamı **DENTCAMP** (@dentcamp) tarafına aittir. AUSCAMP segment seti: Uzman / Pratisyen / NZ / Yaşam. Eski diş postları yeniden paylaşıma da alınmaz.

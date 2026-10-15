# UKCAMP — Asana Yapısı & Statik Post Üretim Otomasyonu Tasarımı

> 20 Temmuz 2026, canlı UKCAMP Asana projesi incelenerek hazırlandı.
> Proje: **UKCAMP** (`<ID>`) — Workspace `<ID>` (AUSCAMP ile aynı workspace) — 154 task (153 tamamlanmış).
> Permalink: https://app.asana.com/1/<ID>/project/<ID>

---

## 1. MEVCUT ASANA YAPISI (gözlemlenen)

### Section'lar
| Section | GID | İçerik |
|---------|-----|--------|
| Untitled section | <ID> | Boş/karışık |
| **Post** | <ID> | **Ana statik/carousel post akışı (asıl üretim)** |
| Story | <ID> | Story içerikleri |
| Video | <ID> | Reels + video + kapaklar |
| Misc | <ID> | Karışık |

> AUSCAMP'ten fark: UKCAMP'te tek **"Post"** section'ı var; AUSCAMP'teki DOKTOR POST / YAŞAM POST / TAKVİM ayrımı YOK. Tüm feed postları "Post"a girer.

### Custom Field
- **Priority** (enum): High / Medium / Low — `<ID>` (AUSCAMP ile paylaşılan alan)
  - High `<ID>` · Medium `<ID>` · Low `<ID>`

### Ekip (atananlar — gerçek atamalardan)
- **Tasarımcı B** (`<ID>`) — **UKCAMP'in birincil tasarımcısı** (postların çoğu ona atanıyor)
- **Tasarımcı A** (`<ID>`) — tasarım (ikincil; AUSCAMP'in de tasarımcısı)
- Diğer üyeler: ekip üyeleri (atama yapılmaz).

### Gerçek Task İsimlendirme Deseni
```
[PAYLAŞILDI ]GG.AA [Konu]
```
Örnekler (gerçek):
- `10.07 PLAB 2 Nerede Gerçekleşir?`
- `PAYLAŞILDI 07.07 İngiltere'de Doktorluk İçin Merak Edilenler: Non-Training'de Kaç Yıl Kalınabilir?`
- `PAYLAŞILDI 23.06 Türkiye'deki Tıp Diplomanız İngiltere'de Geçerli Mi?`
- `PAYLAŞILDI 12.05 Core Surgical Training'de Yayın Türüne Göre Kaç Puan Alırsınız?`

> **AUSCAMP'ten farklar (ÖNEMLİ):**
> - Tarih formatı **GG.AA** (yıl yok) — AUSCAMP'te `GG.AA.YYYY`.
> - Yayınlanınca başa **`PAYLAŞILDI`** ön-eki ekleniyor (bazen typo: `PAYLAŞIDI`).
> - **Assignee KULLANILIYOR** (çoğu Tasarımcı B) — AUSCAMP feedback'i "assignee yok" diyordu; UKCAMP'te aksine atama var.
> - **Due date KULLANILIYOR** (her task'ta yayın tarihi var).
> - Başlıklar uzun/açıklayıcı; "Merak Edilenler:" serisi yaygın.

### Brief Formatı (task description) — İKİ TİP
Yapı AUSCAMP ile aynı (bkz. detay `01`/`02`):

**Tip A — Tam Carousel Brief** (bilgilendirme, mit-yıkma, süreç):
```
[Açılış notu — sade ekip tonu]
SAYFA 1 – Kapak: Başlık + Alt Başlık (bilgi içerir) + (Görsel yönü: mavi zemin/Union Jack, doktor cutout, 🇬🇧)
SAYFA 2..N: Başlık + • gerçek bilgi maddeleri + (Görsel notu)
SON SAYFA – Kapanış: "…her adımda yanınızdayız." + sabit CTA:
  🌐 ukcamp.com.tr   📲 +90 552 253 0 337   📩 info@ukcamp.com.tr
```
**Tip B — Şablon Güncelleme Brief** (webinar/takvim): "Ekteki tasarımı sadece [tarih/mentör/konu] olacak şekilde güncelleyebilir miyiz?"

---

## 2. STATİK POST ÜRETİM OTOMASYONU — TASARIM

### Akış
```
[Sen: konu + segment + tarih]  ←→  veya  [tema → Claude konu önerir]
        ↓  Claude: ŞABLON TİPİ (T1–T10) seçer
        ↓  Claude: SAYFA-SAYFA brief (görsel + dil sistemine sadık)
        ↓  Claude: caption + CTA + hashtag (segment bazlı, 5 varyant)
        ↓  Asana'ya task: "GG.AA [Konu]" + brief + Priority [+ assignee + due date*]
        ↓  [Sen onaylarsın → tasarımcı üretir → yorumda teslim → yayında "PAYLAŞILDI" ön-eki]
```

### Otomasyonun üreteceği standart task (şablon)
- **Başlık:** `GG.AA [Konu]` (UKCAMP deseni; yıl yok)
- **Section:** Post (`<ID>`)
- **Priority:** High (varsayılan)
- **Description (brief):** açılış notu + şablon tipi + SAYFA-SAYFA döküm + görsel notlar + caption/CTA/hashtag bloğu
- **Assignee & Due date:** **GİRİLMEZ (boş bırakılır).** kullanıcı kararı (20.07.2026): UKCAMP task otomasyonu AUSCAMP kuralıyla aynı — assignee yok, due date yok. Atamayı/tarihi kullanıcı/ekip sonra yapar. (UKCAMP ekibi elle Tasarımcı B'a atayıp tarih girse de otomasyon bunu YAPMAZ.)
- **Ekler:** referans görsel/montaj (gerekirse; attachment upload REST + `.asana_token`)

### Şablon tipi → brief eşleştirmesi
| İçerik | Şablon | Brief tipi |
|--------|--------|-----------|
| Webinar duyurusu | T1 | B |
| Aylık takvim | T2 | B/A |
| Bilgilendirme/süreç/NHS | T3 | A |
| Mit-yıkma ("… mı?") | T4 | A |
| Başarı/GMC | T5 | A |
| Mentör tanıtım | T6 | A |
| Ekip | T7 | A |
| Hizmet/işbirliği | T8 | A |
| Canlı yayın | T9 | B |
| Kampanya | T10 | A |

---

## 3. KARARLAR (sabitlendi)
- **Assignee YOK, Due date YOK** (20.07.2026). Otomasyon task'ı yalnız başlık + brief + Priority(High) + Post section ile açar.
- Task başlığı: `GG.AA [Konu]` (yıl yok). "PAYLAŞILDI" ön-ekini otomasyon EKLEMEZ (o, yayın sonrası ekip işareti).
- **Onaysız planlama/yazma yok:** canlı Asana'ya task ancak kullanıcı onayıyla girilir.
---

## ⛔ KAPSAM SINIRI — KARARI KULLANICININ VERDİĞİ POSTLAR (18.08.2026, GLOBAL — AUSCAMP · UKCAMP · DENTCAMP)

Bu tipler **kullanıcı açıkça istemedikçe üretilmez, önerilmez, planlanmaz, Asana'ya girilmez**:
yeni hoca/mentör/eğitmen/ekip tanıtımı · webinar–etkinlik–canlı yayın duyurusu ve takvimi · kampanya/indirim/fiyat · lansman ve yeni hizmet-ürün duyurusu · iş birliği duyurusu · danışan başarısı/tebrik postu.

Otomasyonun serbest üretim kapsamı = **bilgilendirme/eğitici içerik** (süreç, sınav, denklik, karşılaştırma, yaşam, kariyer, mit-yıkma, olgu kartı, mevcut hizmet anlatımı). Boş slot doldurmak için bu tiplere başvurulmaz.

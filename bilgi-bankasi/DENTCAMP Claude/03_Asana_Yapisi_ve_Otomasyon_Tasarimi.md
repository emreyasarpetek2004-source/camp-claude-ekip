# DENTCAMP Asana Yapısı & Otomasyon Tasarımı

> Proje 10.08.2026'da oluşturuldu. AUSCAMP/UKCAMP yapısıyla paralel.
> Permalink: https://app.asana.com/1/<ID>/project/<ID>

## 1. Asana sabitleri (DENTCAMP)

| Nesne | GID |
|---|---|
| **Workspace** | `<ID>` (MediaCamp) |
| **Team** | `<ID>` (MediaCamp) |
| **DENTCAMP projesi** | `<ID>` |
| Section — **Post** *(ana, varsayılan)* | `<ID>` |
| Section — **Video / Reels** | `<ID>` |
| Section — **Misc** | `<ID>` |

**Kardeş projeler (referans):** AUSCAMP `<ID>` · UKCAMP `<ID>` · ALL BRANDS ARCHIVE `<ID>`

**Kişiler:** atama YAPILMAZ.

### ⚠️ Priority custom field'ı YOK
AUSCAMP/UKCAMP projelerinde `Priority` (`<ID>`, High `<ID>`) alanı var. MediaCamp workspace'i **custom field eklemeye izin vermiyor** (`custom_fields_premium_only` — API 10.08.2026). O alanlar eski bir premium döneminden kalma.

**Sonuç:** DENTCAMP task'larında Priority alanı **set edilmez**. Agent'lar custom_fields parametresini boş geçer. Asana planı yükseltilirse alan projeye eklenip agent'lara eklenebilir.

## 2. Task standardı

| Alan | Kural |
|---|---|
| **Başlık** | `GG.AA [Konu] [#seri]` — ör. `18.08 Almanya'da Approbation Nedir? #1`. **Yıl yazılmaz.** "PAYLAŞILDI" ön-eki eklenmez. |
| **Section** | Varsayılan **Post**. Story içeriği → Story, Reels/video → Video / Reels, aylık takvim → Takvim. |
| **notes** | **Tam tasarım brief'i** (sayfa sayfa). Format: `02_Gorsel_Tasarim_Sistemi.md` §9 + brief şablonu (aşağıda). |
| **Caption** | **Asana'ya GİRMEZ.** Caption doğrudan kullanıcıya/yayın paketine gider. |
| **assignee** | **YOK** — atama yapılmaz (kullanıcı kararı). |
| **due_on / due_at** | **YOK** — tarih verilmez (kullanıcı kararı). |
| **Priority** | Set edilmez (alan projede yok, bkz. §1). |
| **Ek (attachment)** | Seri postlarda önceki sayının kapağı eklenir; referans görsel varsa eklenir. MCP ile yüklenemez → REST API + `.asana_token` (bkz. §5). |

## 3. Brief formatı (task notes'a hazır)

```
🎨 ŞABLON: T[n] — [şablon adı]
🌍 ÜLKE: [ALMANYA | AVUSTRALYA | ABD | İNGİLTERE | 4 ÜLKE]
🎯 KİTLE: [Diş hekimliği öğrencisi | Diş hekimi | İkisi]
🖼️ GÖRSEL REFERANS: [varsa ek/dosya adı]

SAYFA 1 — KAPAK
[Başlık metni]
• [madde]
• [madde]
[Görsel yönü: bayrak / blob / fotoğraf]

SAYFA 2 — [alt başlık]
[Bağlam cümlesi]
• [madde 1]
• [madde 2]
• [madde 3]
• [madde 4]

… (sayfa başına 4–5 madde + bir bağlam cümlesi)

SON SAYFA — CTA
[Tek çağrı cümlesi]
🌐 dentcamp.com.tr   📲 +90 552 000 78 38

Kaynak: [kullanılan kaynak alan adları]
```

**Tip A (yeni tasarım):** yukarıdaki tam format.
**Tip B (mevcut şablon güncellemesi):** "Ekteki şablonu kullan; yalnız değişen alanları güncelle" + değişen alanların listesi.

### Brief kuralları
- **Tasarımı tasarımcıya bırak.** İçerik ve niyet verilir; kompozisyon, hizalama, piksel ölçüsü yazılmaz.
- **Ölçü brief'e YAZILMAZ.** Standart sabittir (post 1080×1350 / story 1080×1920) ve tasarımcı tarafından bilinir; her brief'te tekrarlanmaz.
- **Seri numarası brief üreticisinin bilgisi değildir** — Asana erişimi yoktur. Seri no'yu planlayıcı veya kullanıcı verir; verilmediyse brief'te `#?` bırakılır ve sorulur.
- **Kişi adı yazılmaz** brief içinde (atama zaten yok).
- Sayfa başına **4–5 madde + bağlam cümlesi** — sığ bırakılmaz.
- Her rakamın arkasında `Kaynak:` satırı olur.
- Brief'e "(güncellendi)" / "teyitli" gibi notlar **yazılmaz** — veri değişikliği kullanıcıya sohbette bildirilir.

## 4. Otomasyon akışı

```
[içerik fikri]
   ↓ dentcamp-icerik-arastirmaci   (3-5 fikir, kaynaklı)
   ↓ dentcamp-haftalik-planlayici  (gün/tip/ülke/kitle/şablon)
   ↓ dentcamp-takvim-denetci       (çakışma + tekrar kontrolü)  ← ASANA'YA GİRMEDEN ÖNCE
   ↓ dentcamp-brief-uretici        (sayfa sayfa brief)
   ↓ dentcamp-caption-uretici      (5 varyant caption)
   ↓ [KULLANICI ONAYI]                  ← ZORUNLU KAPI
   ↓ dentcamp-asana-task           (task oluştur + ek yükle)
   ↓ dentcamp-yayinci              (yalnız onayla; Business Suite veya Graph API)
```

**Kalite kapıları**
1. Asana'ya girmeden önce takvim denetimi (çakışma/tekrar).
2. Kullanıcı onayı olmadan task açılmaz.
3. Kullanıcı onayı olmadan hiçbir şey planlanmaz/yayınlanmaz.
4. Hazır asset'te hata/şüphe görülürse **yayından önce** bildirilir.

## 5. Attachment yükleme (MCP yetmiyor)

MCP'nin `get_attachments` aracı yalnız okur. Gerçek dosya eklemek için Asana REST API:

```bash
TOKEN=$(tr -d ' \t\r\n' < ~/Documents/"DENTCAMP Claude"/.asana_token)
curl -s -X POST "https://app.asana.com/api/1.0/attachments" \
  -H "Authorization: Bearer $TOKEN" \
  -F "parent=<TASK_GID>" -F "file=@<LOCAL_PATH>;type=image/jpeg"
```
Dönen `data.gid` = attachment gid; `get_attachments` ile doğrulanır.
Asana'daki bir dosyayı indirmek için: `get_attachments` → süreli `download_url` → `curl -L`.

## 6. Çakışma kontrolü (task açmadan önce)
1. `search_tasks` ile DENTCAMP projesinde aynı tarihe/konuya task var mı?
2. Son ~3 ayda aynı konu işlenmiş mi?
3. Ardışık üç postta aynı ülke tekrarlanıyor mu?
4. Seri numarası devam ediyor mu (aynı numara iki kez kullanılmamış mı)?
---

## ⛔ KAPSAM SINIRI — KARARI KULLANICININ VERDİĞİ POSTLAR (18.08.2026, GLOBAL — AUSCAMP · UKCAMP · DENTCAMP)

Bu tipler **kullanıcı açıkça istemedikçe üretilmez, önerilmez, planlanmaz, Asana'ya girilmez**:
yeni hoca/mentör/eğitmen/ekip tanıtımı · webinar–etkinlik–canlı yayın duyurusu ve takvimi · kampanya/indirim/fiyat · lansman ve yeni hizmet-ürün duyurusu · iş birliği duyurusu · danışan başarısı/tebrik postu.

Otomasyonun serbest üretim kapsamı = **bilgilendirme/eğitici içerik** (süreç, sınav, denklik, karşılaştırma, yaşam, kariyer, mit-yıkma, olgu kartı, mevcut hizmet anlatımı). Boş slot doldurmak için bu tiplere başvurulmaz.

**DENTCAMP istisnası:** mentör yasağı **dış** mentörler içindir; kurucu **Sema** (diş hekimi, co-founder) içerikleri serbesttir. Mentör sayısı/isim listesi hiçbir içerikte geçmez.

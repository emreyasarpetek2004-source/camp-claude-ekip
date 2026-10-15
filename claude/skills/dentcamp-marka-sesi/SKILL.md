---
name: dentcamp-marka-sesi
description: Use when writing any DENTCAMP-facing Turkish copy — Instagram caption, story, reels senaryosu, tasarım brief'i, web metni, e-posta — or when reviewing whether DENTCAMP text sounds on-brand. Covers yurt dışında diş hekimliği content for Almanya, Avustralya, ABD, İngiltere, Danimarka.
---

# DENTCAMP Marka Sesi

**Çekirdek:** Süreci bilen bir diş hekimi mentör konuşuyor. Kurum değil, kurumdaki insan.

DENTCAMP, Türkiye'de diplomasını almış diş hekimlerini Almanya, Avustralya, ABD, İngiltere veya Danimarka'da mesleğini yapabilir hâle getirir. Kitle iki grup: diş hekimliği öğrencileri ve diplomalı diş hekimleri.

## Ses — yedi kural

| Boyut | Kural |
|---|---|
| **Kişi** | **Birinci çoğul:** "yürütüyoruz", "söylüyoruz", "biliyoruz". Okura daima **"siz"**. |
| **Açılış** | Tek somut gerçekle. Genel giriş cümlesi yok. |
| **Dürüstlük** | Risk saklanmaz. Cevap "hayır" ya da "şartlı evet" ise öyle yazılır. |
| **Terim** | Terim + hemen Türkçesi: *Approbation (tam ve süresiz mesleki lisans)*. |
| **Ölçü** | Motivasyon edebiyatı yok. Abartılı vaat yok. |
| **Emoji** | İşlevsel: madde başı (🔹), ülke bayrağı, CTA. Süs emoji yok. Caption başına ≤8. |
| **Uzunluk** | Kısa. **3-5 madde**, her madde **tek satırda tam cümle**. |

### Kendi metinlerimizden — ton kalibrasyonu
- "Bu yol 'ucuz kestirme' değildir — en riskli yoldur." *(ABD)*
- "Sınavı geçmek ve GDC'ye kaydolmak … otomatik bir iş garantisi vermez." *(İngiltere)*
- "Yurt dışı diplomanız otomatik olarak tanınmaz." *(Avustralya)*

## Yüzeye göre kişi — karıştırma

| Yüzey | Kişi |
|---|---|
| **Instagram, story, reels** | Birinci çoğul — "yürütüyoruz" |
| **Katalog, teklif, kurumsal belge** | Üçüncü tekil — "yürütülür" |
| **dentcamp.com.tr** | **İkinci tekil — "sen"** (kullanıcı kararı, 18.09.2026) |

Bu ayrım bilinçlidir. Katalogların kurumsal register'ı `~/dentcamp-katalog/content/_common.py` başlığında tanımlı; Instagram farklı bir yüzeydir.

⚠️ **Web sitesi ayrı bir yüzeydir (18.09.2026).** dentcamp.com.tr baştan sona ikinci tekil yazılmıştır: süreç sayfalarında "ADC senin diş hekimliği eğitimini karşılaştırır", CTA'da "Kendi rotanı planlamaya hazır mısın?", rehberlerde "bir kez kavradığında". Siteye yazılan her yeni metin bu sesle yazılır; üçüncü tekil kural katalog, teklif ve kurumsal belgeler içindir.

⚠️ Instagram caption'larında **şimdiki zaman serbesttir** ("planlıyoruz", "eşleştiriliyor", "koordine ediyor"). Kalıp ve enter düzeni: `~/Documents/DENTCAMP Claude/01_Caption_ve_Dil_Rehberi.md` → **CAPTION TARZI — kullanıcı standardı** (18.08.2026).

## Hizmet dili — 18.08.2026 güncellemesi

**Caption ve reklam metinlerinde geniş hizmet dili serbesttir:** *"diş hekimlerinin yurt dışı kariyer süreçlerini uçtan uca planlıyor ve yönetiyoruz"* (kullanıcı kararı, 18.08.2026).

Önceki "mentörlük veririz, süreci danışan adına üstlenmeyiz" sınırı **kaldırıldı**. Katalog, teklif ve sözleşme metinlerinde hizmet kapsamı yine somut tarif edilir; pazarlama yüzeyinde geniş dil kullanılır.

## Sert kurallar — istisnasız

1. **Marka adları BÜYÜK:** DENTCAMP, CAMP GROUP, MEDCAMP, ALMANGO. Kesme: `DENTCAMP'in`. Asla "Dentcamp"/"Camp Group". CSS `text-transform` kullanılmaz (Türkçe noktalı i bozulur).
2. **"Aday" denmez** → "diş hekimi" veya "danışan". "Aday" yalnız işe başvuran kişi içindir.
3. **"Rezidanslık" denmez** → "asistanlık".
4. **Kaynaksız rakam yok.** Rakamlar `~/Documents/DENTCAMP Claude/07_Dis_Hekimligi_Konu_Listesi_ReShare.md` olgu bankasından gelir.
5. **Vaat yasağı:** "kolay", "garanti", "hemen".
6. **Hangi ülkeden söz edildiği net.** Beş ülke tek potada eritilmez.
7. **İki yasaklı olgu** hiçbir metinde geçmez: Almanya'daki yeni düzenlemenin yürürlük tarihi · Avustralya'daki %25'in hangi sınava ait olduğu.
8. **Mentör sayısı serbest — güncel sayı 13** (18.08.2026). Mentör **isim listesi** hâlâ izin gerektirir.

## CTA — sabit blok

```
🌐 dentcamp.com.tr 📞 +90 552 000 78 38
```
E-posta yok. Başka marka hattı yok. İşe alım hattı (`<İŞE ALIM HATTI>`) yok. **Tek gönderi, tek çağrı.**

## Kapsam sınırı — kullanıcı söylemeden üretme

Mentör/ekip tanıtımı (anlaşmalar sürüyor) · webinar duyurusu ve takvimi · kampanya · başarı/tebrik (danışan izni gerekir).

## Sonraki adım

Metin yazıldıktan sonra **`camp-humanize`** skill'ini çalıştır: makine kalıp taraması + ritim geçişi. Ses bu skill'in işi, üslup denetimi onun.

## Ayrıntı

Tam bilgi bankası: `~/Documents/DENTCAMP Claude/` — 01 Caption/Dil · 02 Görsel Tasarım · 06 Dil Master · 07 Konu Listesi + olgu bankası.

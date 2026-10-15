# UKCAMP (@camp2uk) — TÜM GEÇMİŞ Instagram Analizi

> Kaynak: Apify Instagram Scraper ile çekilen **495 @camp2uk postu** (Şubat 2024 → Temmuz 2026). 20 Temmuz 2026. Caption + tip + beğeni + yorum + tarih + hashtag + kapak görselleri analiz edildi. Ham veri: `veri_arsivi/ukcamp_posts.json`.

## 1. Hacim & Ritim
- **495 post / ~29 ay** → istikrarlı **~22-24 post/ay (~5-6/hafta, reels dahil)**.
- 2024: 84 · 2025: 254 · 2026: 157. Son aylar 21-29/ay bandında stabil (AUSCAMP ile neredeyse aynı tempo).

## 2. Format Dağılımı
| Tip | Adet | Pay |
|-----|------|-----|
| Video / Reels | 241 | %48 |
| Carousel (Sidecar) | 181 | %36 |
| Tekli görsel | 73 | %14 |

Carousel ortalama **5.3 slayt** (max 9) — AUSCAMP'ten (3.9) daha uzun carousel'ler.

## 3. Etkileşim Gerçeği
- Ortalama **35 beğeni**, medyan 15, max **1000**. Yorum medyanı **0** (AUSCAMP gibi pasif kitle).
- **Tip bazında medyan beğeni: Video 20 > Carousel 12 > Tekli 7.**
- ➡️ AUSCAMP'teki gibi **Video/Reels en yüksek etkileşim**; carousel en çok ikinci üretilen ama post başına düşük getiren format. Tekli görsel en düşük.

## 4. NE İŞE YARIYOR — En Çok Beğeni Alan Postlar
| ♥ | Tip | Konu |
|---|-----|------|
| 1000 | Carousel | "İngiltere'de Doktorluk Hedefiniz mi Var?" — **2 haftalık ücretsiz deneme** (kampanya + değer önermesi) |
| 908 | Görsel | "UKCAMP'e Yeni Yıl Fırsatıyla Katıl!" — **kampanya/indirim** |
| 754 | Video | Mentör **Dr. İpek İnan** tanıtımı |
| 531 | Video | Mentör **Dr. Utku Timurçin** tanıtımı |
| 492 | Carousel | "Mezun olunca Birleşik Krallık'ta doktorluk yapabilir miyim?" — **mit/soru** |
| 406 | Video | "İngiltere'de **Aile Hekimi** nasıl olunur? CREST sertifikası" |
| 394 | Görsel | "**PLAB 2** hakkında merak edilenler" Q&A |
| 369 | Carousel | **Aylık webinar takvimi** |

**Kazanan formül:** ① kampanya/fırsat (ücretsiz deneme, yeni yıl) · ② gerçek mentör videoları (isimli tanıtım) · ③ "yapabilir miyim?" mit-yıkma soruları · ④ PLAB/GMC süreç bilgilendirme · ⑤ webinar takvimi.

## 5. Tema Dağılımı (caption bazlı, çok temalı)
NHS/kariyer %88 · **Mentör/eğitmen %79** · **PLAB %76** · Yaşam/şehir/maaş %54 · Webinar %37 · Uzman/specialist %24 · GMC/registration %21 · **UKMLA %17** · Başarı/tebrik %13 · Aile hekimi/GP %7 · OET/IELTS %6 · Vize %3.

➡️ AUSCAMP'ten temel fark: **PLAB ve mentör içeriği baskın**; AUSCAMP'te "sınavsız denklik" varken UKCAMP **sınav-hazırlık odaklı** ve mentör-yoğun.

## 6. Hashtag Sistemi
- **Çekirdek:** #ukcamp (341), #plab2 (288), #plab (277), #doktor (243), #ingilterededoktorolmak (233), #tıpeğitimi (211), #ingilterededoktor (197), #tıp (193), #ingilterededoktorluk (184), #medicine (175), #nhs (174), #yurtdışındadoktorluk (166), #plab1 (150), #ingiltere (145).
- Öneri çekirdek set: `#UKCAMP #İngilteredeDoktorluk #PLAB #NHS #DoctorLife #YurtdışındaDoktorluk` + segment (#PLAB1 #PLAB2 #GMC #OET).

## 7. Görsel Kimlik (kapak analizinden)
UKCAMP = **Union Jack teması: royal/lacivert mavi + kırmızı + beyaz** (AUSCAMP'in yeşil+altınından tamamen farklı).
- **Logo:** beyaz yuvarlatılmış kutuda **"UK"** (Union Jack bayrak dokusu, kırmızı/mavi) + **"CAMP"** (lacivert). AUS CAMP logosunun UK karşılığı.
- **Baskın hex (görsellerden):** lacivert/royal mavi ~`#1E4FA0`→`#10357A` gradyan, kırmızı ~`#E01B2E`, beyaz `#FFFFFF`.
- **Tekrarlayan öğeler:** 🇬🇧 Union Jack bayrağı, doktor cutout (beyaz önlük + stetoskop), yuvarlatılmış **pill/konuşma-balonu başlık kutuları** (kırmızı & mavi dönüşümlü), **kırmızı kurdele/şerit** vurgular, alt **kırmızı CTA barı**.
- **İki şablon stili:** (A) foto-zemin + kırmızı/mavi pill başlıklar + alt kırmızı CTA barı; (B) mavi gradyan + doktor cutout + bayrak + kırmızı kurdele.
- Güçlü, oturmuş ve AUSCAMP'ten bağımsız bir kimlik → korunmalı, yeşil-tema taşınmamalı.

---

## 8. STRATEJİK ÇIKARIMLAR
1. **Video'ya ağırlık** — en yüksek etkileşim video/mentör tanıtımında.
2. **#1 duygusal kanca UK'de farklı:** "sınavsız" DEĞİL; UKCAMP'te kazanan **kampanya/fırsat + mentör güveni + 'her adımda yanınızdayız' kesintisiz destek**.
3. **PLAB süreç bilgilendirme + mit-yıkma ("… yapabilir miyim?")** güçlü carousel sütunu.
4. **Webinar takvimi** düzenli lead motoru (AUSCAMP gibi).
5. **Yorum ~0** → etkileşim CTA'ları ekle (algoritma için).
6. **Başarı/tebrik (%13) ve GMC (%21)** artırılabilir — güven inşası.
7. **Görsel kimlik: Union Jack (mavi+kırmızı+beyaz)** — AUSCAMP şablonlarını renk olarak KOPYALAMA; UK kimliğini koru.

# AUSCAMP Görsel Tasarım Sistemi (@camp2aus)

> Kaynak: 34 feed postu / ~110 carousel slaytı, 3 Mart – 17 Haziran 2026. Slaytlar tek tek indirilip görsel olarak incelendi (19 Haziran 2026).
> Amaç: Statik post üretim otomasyonunun **bu görsel kimliği birebir korumasını** sağlamak. Bu doküman tasarımcı brief'lerinin görsel referans omurgasıdır.

---

## 1. RENK PALETİ
| Renk | Kullanım | Yaklaşık |
|------|----------|----------|
| **Koyu Zümrüt Yeşil** | Baskın zemin, metin (beyaz üstü değil) | ~#147A3C |
| **Parlak/Açık Yeşil** | Gradient, vurgu, pill | ~#3DBе63 |
| **Altın / Sarı** | CTA, highlight blokları, next-arrow, takvim kutusu, "%14" | ~#F4B70C |
| **Beyaz** | Yeşil üstü metin, logo kutusu, pill, polaroid çerçeve | #FFFFFF |
| **Kırmızı** | ■ madde işareti (bilgi/co-brand), ❌ ikon | ~#E1281F |

Co-brand renkleri: **MEDCAMP/MEDICAMP English** (kırmızı+yeşil), **DUSDATA** (mavi+kırmızı).

## 2. LOGO
- **"AUS CAMP"** — `AUS` yeşil, `CAMP` altın/sarı; **beyaz yuvarlatılmış dikdörtgen** kutu içinde.
- Konum: **üst-orta** (içerik slaytları) veya **üst-sol** (kapaklar).
- Co-brand gerektiğinde yanında MEDICAMP English / DUSDATA logosu.

## 3. SABİT GÖRSEL ÖĞELER
- 🇦🇺 **Avustralya bayrağı:** kapak slaytının üst köşesi (sağ veya sol).
- ▶ **Next-arrow:** sarı daire içinde ok, **sağ-alt köşe** — çok-slaytlı içeriklerde "kaydır" sinyali.
- **Dekor:** köşe diyagonal şeritler, dalga/doku desenli zemin, şehir silüeti (yaşam içeriği), kanguru ikonu, sarı soru-işareti baloncukları (mit-yıkma).

## 4. TİPOGRAFİ
- Başlık: **kalın sans-serif**, BÜYÜK HARF veya Title Case.
- Kontrast kuralı: **yeşil zemin → beyaz metin**, **beyaz zemin → koyu yeşil metin**.
- Vurgu: anahtar kelimeye **sarı marker bloğu** veya **yeşil/beyaz pill** arka plan.
- El yazısı/script aksanı: "Congratulations" (altın script), "Şimdi bir adım atın" (sarı altı çizili).

## 5. MADDE İŞARETİ SİSTEMİ
| İşaret | Bağlam |
|--------|--------|
| ✓ (sarı/beyaz) | Fayda / özellik listeleri |
| → (sarı ok) | Mit-yıkma, soru listeleri |
| ■ (kırmızı kare) | Bilgi / co-brand postları |
| • / ▪ | Genel maddeler |
| Emoji-başlı (📅📚🏥) | Yaşam / kültür içerikleri |

## 6. SLAYT ANATOMİSİ (çok-slaytlı carousel standardı)
1. **KAPAK:** bayrak + büyük başlık (vurgulu kelimelerle) + destekleyici foto/illüstrasyon + opsiyonel **seri no** (#3, #7, #9).
2. **İÇERİK:** logo (üst) + alt başlık + madde gövde + görsel + sağ-altta next-arrow.
3. **KAPANIŞ / CTA:** koyu yeşil zemin + "Bizimle iletişime geçin / Bizi takipte kalın" + 📞 `+90 552 253 03 37` (pill) + 🌐 `www.auscamp.com.tr` (pill) + logo.

## 7. FOTOĞRAF STİLİ
- **Mentör:** arka planı silinmiş (cutout) portre, **sarı daire / yarım-daire** üstünde.
- **Yaşam:** beyaz **polaroid çerçeve**, hafif eğik, kırmızı/turuncu raptiye.
- **Stok:** parlak yeşil tonlamalı; doktor, şehir silüeti, doğa.

---

## 8. ŞABLON TAKSONOMİSİ (10 tip) — otomasyonun çıktı tipleri

### T1 — Webinar Duyurusu (tek slayt veya 2-slayt)
Sarı üst/alt şerit + bayrak köşe + logo üst-orta + **audience pill** (`HERKESE AÇIK, ÜCRETSİZ!` yeşil / `AUSCAMP DANIŞANLARINA ÖZEL`) + ■ büyük başlık + **mentör cutout** (sarı yarım-daire, sağ) + **takvim kutusu** (📅 tarih + ⏰ saat, sol-alt) + mentör adı (yeşil pill) + rol (italik). Zoom ise 💻, değilse platform.

### T2 — Aylık Webinar Takvimi
**Kapak BEYAZ zemin:** büyük ay ("04 NİSAN") + "Konferans Takvimi" + 4 webinarın listesi (mini mentör fotoğrafı + tarih + başlık + audience etiketi) + footer web/telefon. Ardından her webinar için T1 tarzı ayrı slayt.

### T3 — Bilgilendirme (Yaşam / Sistem / Süreç)
Yeşil zemin. Kapak: bayrak + başlık + foto/illüstrasyon. İçerik: başlık + ✓/→ madde + görsel + next-arrow. Bazı seriler (Biliyor Muydunuz) **beyaz içerik zemini** kullanır. Son slayt koyu yeşil CTA. Veri içeren alt-tip: yatay **bar chart** + harita (ör. talep/sıralama).

### T4 — Mit-Yıkma ("Doğru Bilinen Yanlışlar #N")
Kapak: **sarı→yeşil gradient**, büyük beyaz başlık + yeşil pill "YANLIŞLAR #N" + uçuşan sarı ? baloncukları. İçerik: `YANLIŞ` (kırmızı pill + ❌) vs `GERÇEK` (yeşil pill + ✅), → sarı ok maddeler, polaroid foto.

### T5 — Başarı / Denklik ("Congratulations")
Slayt 1: altın **script "Congratulations"** + beyaz pill'lerde denklik başlığı + konfeti + **tasdik belgesi ekran görüntüsü** (bantlı). Slayt 2: "Denklik Süreci Nasıl İlerledi?" **noktalı timeline** (aylık milestone'lar) veya sarı **konuşma balonunda danışan mesajı**. Son: koyu yeşil CTA.

### T6 — Mentör Tanıtımı
Slayt 1: yeşil + logo sol-üst + büyük isim (beyaz) + altın **"AUSCAMP'te!"** banner + mentör cutout (sağ) + bayrak sol-alt + köşe şeritleri. Slayt 2: "[İsim]'i Tanıyalım." + biyografi (beyaz, ortalı). Slayt 3: **"Bize Ulaşın!"** illüstrasyonlu CTA (kişi tabela tutuyor) + web/telefon.

### T7 — Ekip Tanıtımı
Kapak: "AUSCAMP Ekibini Tanıyalım" + grup. Ardından **her mentöre 1 slayt**: yeşil konum etiketi (📍 Melbourne/Brisbane), sarı daire foto, isim + rol + kısa bio. (13 slayta kadar.)

### T8 — Hizmet / İşbirliği (DUSDATA tarzı)
**Beyaz zemin**, co-brand (AUS CAMP + DUSDATA). Kapak: foto + başlık. İçerik: "Size Neler Sunuyoruz?" + yeşil kalın tireli hizmet listesi + yeşil footer bar. Son: "Yalnız Değilsiniz" + sarı highlight + WhatsApp/web/iş-ortağı hattı.

### T9 — Canlı Yayın (Instagram Live)
T1 benzeri ama "**Canlı Yayın!**" pill + `📷 LIVE @camp2aus` + "Kaçırmamak için takip edin". Soru slaytı: → maddelerle "Bu Yayında Neleri Netleştireceğiz?".

### T10 — Kampanya / Dönemsel
Daha **dramatik/koyu** zemin (parlak yeşil glow + foto), büyük **sarı indirim bloğu** ("%14"), tarih aralığı, "Tıp Bayramımız Kutlu Olsun!" tarzı duygusal kapanış + CTA.

---

## 9. OTOMASYON İÇİN GÖRSEL STANDART ÇIKARIMI
Tasarımcı brief'i her zaman şunları belirtmeli:
1. **Şablon tipi** (T1–T10) — böylece mevcut tasarım yeniden kullanılır, sıfırdan başlanmaz.
2. **Slayt sayısı ve her slaytın rolü** (kapak / içerik / CTA).
3. **Zemin:** yeşil (varsayılan) / beyaz (takvim kapağı, "biliyor muydunuz", hizmet).
4. **Sabitler:** logo konumu, bayrak köşesi, next-arrow, CTA pill'leri (telefon+web).
5. **Segment görsel ipucu:** diş 🦷, NZ 🇳🇿 + harita, pratisyen/AMC stetoskop, yaşam şehir/doğa.
6. **Vurgu kelimeleri:** sarı marker / pill ile işaretlenecek anahtar kelimeler.
7. **Ölçü:** 1080×1350 (4:5 dikey) — indirilen slaytlar 1440×1800 oranında. **Sabit standarttır, brief'e YAZILMAZ.** `auscamp-orkestra-sefi` ve `auscamp-asana-task` "piksel ölçüsü (1080x1350) yazma" diyor; ölçü tasarımcı tarafından bilinir, her brief'te tekrarlanmaz.

## 10. TUTARLILIK NOTLARI (görselde gözlenen)
- Genel kurumsal kimlik **çok tutarlı** — renk, logo, CTA yapısı her postta korunmuş. ✅
- Küçük varyasyonlar: next-arrow bazen ▶ bazen →; CTA pill bazen yeşil bazen sarı; bilgi serileri zemin (yeşil vs beyaz) değişken. Otomasyonda sabitlenebilir ama marka kimliğini bozmaz.
- Co-brand kullanımı net kurallı: OET→MEDCAMP, Diş→DUSDATA.

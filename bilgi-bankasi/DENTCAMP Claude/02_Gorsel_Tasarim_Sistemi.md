# DENTCAMP Görsel Tasarım Sistemi (@dentcamptr)

> Kaynak: `~/dentcamp-katalog/theme.py` + `build.py` + `README.md` (4 ülke kataloğu, Ağustos 2026) ve `~/dentcamp-vaka/theme.py`. Amaç: statik post üretim otomasyonunun **DENTCAMP görsel kimliğini birebir korumasını** sağlamak. Tasarımcı brief'lerinin görsel referans omurgası.
>
> ⚠️ **Bu doküman kurucu niteliktedir.** @dentcamptr'te henüz paylaşım yok (lansman 15 Ağustos 2026). AUSCAMP/UKCAMP'te bu doküman yüzlerce eski posttan çıkarılmıştı; DENTCAMP'te **basılı katalog tasarım sisteminden türetildi.** İlk 20-30 post yayınlandıktan sonra gerçek feed'e göre revize edilmeli.
>
> ⚠️ DENTCAMP kimliği AUSCAMP ve UKCAMP'ten **bağımsızdır** — AUSCAMP'in yeşil/altını ve UKCAMP'in Union Jack'i (mavi/kırmızı/beyaz) DENTCAMP'e ASLA taşınmaz.

---

## 1. RENK PALETİ (petrol yeşili + turkuaz)

| Renk | Kod | Kullanım |
|------|-----|----------|
| **Koyu petrol yeşili** | `#005b52` | Baskın zemin, başlık metni, pill kutuları, gövde metni |
| **Parlak turkuaz** | `#00d9bd` | Aksan, blob, vurgu şeridi, ikon dolgusu, CTA çipi |
| **Mint** | `#d6f2ed` | Kutu/kart zemini, isim pill'i, açık yüzeyler |
| **Adım turkuazı** | `#2bbfa8` | Numaralı daireler (yol haritası), süreç adımları |
| **Beyaz** | `#FFFFFF` | Metin (koyu zeminde), kart zemini, kontrast |

**Blob ailesi** (kapak sol kenarındaki organik lekeler): `#00d9bd` · `#a8f2e7` · `#00b49e` · `#6fe8d6`

**Nötrler** (vaka belgesinden, gerekirse): ink `#22303c` · ink-soft `#5b6b78` · çizgi `#dde5ec`

### Ülke rengi KULLANILMAZ
Kullanıcının Ağustos 2026 kararı: dört ülke de yalnız DENTCAMP paletiyle basılır. Bayrak renkleri (Avustralya lacivert, İngiltere kırmızı vb.) dar yüzeylerde aksan olarak kullanılıyordu, **terk edildi.** Ülke ayrımı **yalnız bayrak görseliyle** yapılır.

### CAMP GROUP renkleri (yalnız kurumsal bağlamda)
Lacivert `#06539f` · koyu lacivert `#03386e` · yumuşak `#e8f0f9` · kırmızı `#e31e26`.
Sadece "CAMP GROUP markasıyız" tipi kurumsal içeriklerde geçiş bandı olarak kullanılır; normal DENTCAMP postunda yeri yoktur.

---

## 2. LOGO
- **DENTCAMP** logosu — iki dolgu rengi var: `#005b52` ve `#00d9bd`.
- Master dosya: `~/Downloads/DENTCAMP/dentcamp.svg` (ayrıca `.ai`, `.png`, `.jpg`)
- Kullanılan kopyalar: `~/dentcamp-katalog/assets/img/logo.png`, `~/dentcamp-vaka/assets/img/dentcamp.png`
- Konum: **üst-orta** (içerik slaytları) veya **üst-sol / alt-sol** (kapaklar).
- CAMP GROUP logosu: `~/dentcamp-vaka/assets/img/campgroup{.png,.svg,_beyaz.svg,_mono.svg}`

## 3. SABİT GÖRSEL ÖĞELER
- 🏳️ **Ülke bayrağı:** dalgalı bayrak, kapağın **sol kenarından** girer. Dosyalar: `~/dentcamp-katalog/assets/img/bayrak_{aus,uk,usa,deu}.png` (gerçek Pexels fotoğrafları, alfa temizlenmiş).
- **Turkuaz blob:** kapağın sol/köşe kenarında organik leke ailesi — DENTCAMP'in en tanınır öğesi.
- **Pill başlık kutuları:** yuvarlatılmış; mint zemin + petrol yeşili metin, veya petrol yeşili zemin + beyaz metin.
- **Numaralı daireler:** `#2bbfa8` — süreç/adım anlatımlarında (yol haritası mantığı).
- **Çizgi ikon seti:** `~/dentcamp-katalog/assets/img/ic_*.png` (10 adet) — hizmet/süreç maddelerinde.
- **Alt CTA barı:** petrol yeşili zemin + 🌐 dentcamp.com.tr · 📲 +90 552 000 78 38 · 📷 @dentcamptr

## 4. TİPOGRAFİ
| Rol | Font |
|-----|------|
| Kapak başlığı | **League Spartan Bold** |
| H1 / pill başlık | **Open Sans ExtraBold** |
| İsim / künye | **Arimo Bold** |
| Gövde metni | **Archivo** |

Dosyalar: `~/dentcamp-katalog/assets/fonts/` ve `~/dentcamp-vaka/assets/fonts/`. Hepsi açık lisanslı.

- Kontrast: **petrol yeşili zemin → beyaz metin**, **mint/beyaz kutu → petrol yeşili metin**.
- Vurgu: anahtar kelimeye **turkuaz veya mint pill** arka plan.
- ⚠️ **CSS `text-transform` ASLA kullanılmaz** — Türkçe noktalı i bozuluyor. Büyük harf gerekiyorsa metin doğrudan büyük yazılır.
- Tırnak ve kesme işaretleri **tipografik**: `" "` ve `'` — düz `"` ve `'` kullanılmaz.

## 5. MADDE İŞARETİ SİSTEMİ
| İşaret | Bağlam |
|--------|--------|
| ✅ | Fayda / gereklilik listeleri |
| • (beyaz) | Genel maddeler (petrol yeşili zemin) |
| 📌 | Bilgi / uyarı maddeleri |
| ① ② ③ (turkuaz daire) | Sıralı süreç adımları |
| Emoji-başlı (🦷 📋 🗣️ 🏥 📄) | Hizmet / süreç içerikleri |

## 6. SLAYT ANATOMİSİ (carousel standardı — **en fazla 5 slayt**)
> kullanıcı kararı (12.08.2026): "genel olarak 5'i geçmeyelim, çok gerekirse geçilebilir."
> Varsayılan: **4 slayt** = kapak + 2 içerik + CTA. Konu gerektiriyorsa 5. 5'i aşmak için gerçek bir gerekçe olmalı ve brief'te tek satırla yazılmalı.
1. **KAPAK:** logo + ülke bayrağı (sol kenar) + turkuaz blob + başlık + alt başlık + opsiyonel seri no.
   **Metin yalnız iki satır:** başlık (ülke geçen, **isim öbeği** — cümle değil) + alt başlık (2-5 kelime, konunun açısı). Kapakta **madde ve açıklama YOK**; içerik SAYFA 2'den başlar. Dört ülkeli postlarda çapa "Yurt Dışında …" / "Dört Ülkede …". *(AUSCAMP kuralından uyarlandı, 13.08.2026.)*
2. **İÇERİK:** logo (üst) + alt başlık + madde gövde + ikon/görsel. Sayfa başına **3 madde** (istisnaen 4), her madde **tek satır**; en fazla tek kısa bağlam satırı. *(10.08.2026 global "kısa/to-the-point" kuralı.)*
3. **KAPANIŞ / CTA:** petrol yeşili zemin + tek çağrı + sabit CTA bloğu + logo.

## 7. FOTOĞRAF STİLİ
- **Klinik/hekim görseli:** aydınlık modern klinik, lacivert scrub'lı diş hekimi. Katalog kapaklarında **aynı iki Türk diş hekimi** (kadın + erkek, 30'lu yaşların başı, Ege/İzmir görünümü) tekrar eder — bu bir marka öğesidir. Üretim prompt'ları: `~/dentcamp-katalog/assets/kapak_kaynak/PROMPTLAR.md`
- **Instagram kapağında fotoğraf ZORUNLU DEĞİL.** Bayrak + blob + güçlü tipografi tek başına yeterlidir. Fotoğraf kullanılacaksa yukarıdaki iki hekim tercih edilir (marka tutarlılığı).
- **Ülke işareti:** pencereden görünen landmark — Opera House & Harbour Bridge (AUS) · Big Ben & Westminster (UK) · Empire State & Manhattan (ABD) · Brandenburg Kapısı & Fernsehturm (DEU).
- **Mentör:** yuvarlak kesim portre, mint pill üzerinde isim + künye. **Biyografi yok** — kataloglarda toplu liste hâlinde.
- **Yasak:** gösterişli/parlak yüzeyler, stok "gülümseyen mutlu insan" klişesi. Marka sesi: "Sade duruyor. Gösterişli ve parlak yüzeylerden kaçınıyoruz."

---

## 8. ŞABLON TAKSONOMİSİ (10 tip) — otomasyonun çıktı tipleri
> Numaralandırma AUSCAMP/UKCAMP T1–T10 ile **paralel**; renk = DENTCAMP paleti, içerik = diş hekimliği + 4 ülke.
> ⚠️ Bunlar henüz üretilmemiş şablonlardır — ilk kez tasarlanacaklar. Brief'te "mevcut şablonu kullan" değil, "bu tipi kur" denir; ikinci kullanımdan itibaren "T3 şablonunu kullan" geçerli olur.

### T1 — Webinar Duyurusu
Bayrak (sol kenar) + logo + **kitle pill'i** (`HERKESE AÇIK, ÜCRETSİZ!` / `DENTCAMP DANIŞANLARINA ÖZEL`) + büyük başlık + **mentör yuvarlak portre** + **takvim kutusu** (📅 tarih + ⏰ saat) + mentör adı (mint pill) + künye. Zoom ise 💻.

### T2 — Aylık Webinar Takvimi
Kapak: büyük ay adı + "Webinarları" + webinar listesi (mini mentör fotoğrafı + tarih + başlık + kitle etiketi) + alt CTA barı. Ardından her webinar için T1 tarzı slayt.

### T3 — Bilgilendirme — üç alt tipe ayrılır
En çok kullanılacak tip. Görsel olarak birbirinden farklı üç deste olduğu için **alt tip adıyla anılır** (yalnız "T3" demek ikinci kullanımdan sonra anlamını yitirir).

**T3a — SÜREÇ / SINAV (tek ülke).** Zemin: **petrol yeşili** (Stil B). Kapak: bayrak (sol kenar) + başlık + blob; fotoğraf opsiyoneldir, zorunlu değil. İçerik: alt başlık + ✅/📌 madde. Sıralı süreçler (Approbation adımları, ADC aşamaları, ORE bölümleri, ABD'nin üç yolu) **numaralı turkuaz dairelerle**.

**T3b — 4 ÜLKE KARŞILAŞTIRMA.** Zemin: **beyaz/mint kart** (Stil C) — dört ülke yan yana okunacağı için açık zemin. Dört bayrak + kolon kolon aynı ölçüt (süre / sınav / maliyet / risk). Kapak dışında ülke başına 1 slayt.

**T3c — VERİ.** Zemin: **beyaz/mint** (Stil C). Bar/kolon grafik (ör. ülke ülke süre aralığı). Rakamların kaynağı brief'te `Kaynak:` satırıyla verilir.

### T4 — Mit-Yıkma ("… yapabilir miyim?")
Kapak: petrol yeşili zemin + hekim görseli + tırnak içi büyük beyaz soru + ülke bayrağı + **turkuaz şerit "Sorunuzu İnceliyoruz!"**. İçerik: soru → net cevap + ✅ maddeler. DENTCAMP'in dürüstlük ilkesi burada işler: cevap "hayır" ya da "şartlı evet" ise öyle yazılır.

### T5 — Başarı / Lisans Tebrik
Slayt 1: kutlama başlığı (Approbation aldı / ADC pratik sınavını geçti / GDC kaydı tamamlandı / eyalet lisansı alındı) + konfeti + varsa belge/danışan mesajı. Slayt 2: süreç timeline. Son: CTA barı.
⚠️ Danışan izni olmadan isim/görsel kullanılmaz.

### T6 — Mentör Tanıtımı
Slayt 1: petrol yeşili + logo + büyük isim (beyaz) + **"DENTCAMP'te!"** banner + yuvarlak portre + ülke bayrağı. Slayt 2: mentörün bulunduğu ülke/şehir + uzmanlık. Slayt 3: CTA.
⚠️ **Mentör anlaşmaları sürüyor** — bu tip kullanıcı söylemeden üretilmez (bkz. `feedback-dentcamp-icerik-kapsam`).

### T7 — Ekip Tanıtımı
Kapak: "DENTCAMP Ekibini Tanıyalım" + grup. Her mentöre 1 slayt: 📍 şehir/ülke etiketi, portre, isim + künye.

### T8 — Hizmet / İşbirliği
Kapak: fotoğraf + başlık. İçerik: "Size Neler Sunuyoruz?" — denklik/lisans süreç yönetimi, sınav hazırlığı, belge yönetimi, **kişiye özel WhatsApp grubu**, A'dan Z'ye mentörlük.
**Co-brand:** dil konusu geçtiğinde — AUS/UK/ABD → **MEDCAMP** (OET, @medcampenglish) · Almanya → **ALMANGO** (A1–B2 + FSP, ÖSD sınav merkezi).

### T9 — Canlı Yayın (Instagram Live)
T1 benzeri ama "**Canlı Yayın!**" pill + `📷 LIVE @dentcamptr` + "Kaçırmamak için takip edin". Soru slaytı: → maddelerle gündem.

### T10 — Kampanya / Dönemsel
Kampanya kapağı (fotoğraf + büyük turkuaz/mint pill) + süre/tarih + fayda listesi + güçlü CTA.
⚠️ Kampanya içeriği kullanıcı söylemeden üretilmez.

---

## 9. OTOMASYON İÇİN GÖRSEL STANDART

### 9a. Brief'in belirteceği (yalnız bunlar)
1. **Şablon tipi** (T1–T10; T3 ise alt tip: T3a/T3b/T3c) — ikinci kullanımdan itibaren mevcut tasarım yeniden kullanılır.
2. **Slayt sayısı ve rolü** (kapak / içerik / CTA).
3. **Ülke:** ALMANYA / AVUSTRALYA / ABD / İNGİLTERE — hangi bayrak kullanılacak.
4. **Kitle:** öğrenci / diş hekimi.
5. İçerik zorunlu kılıyorsa **tek satırlık** görsel ipucu.

### 9b. Tasarımcının alanı (brief'te YAZILMAZ)
Yerleşim, kompozisyon, renk dağılımı, tipografi, ikon seçimi, **stil seçimi** (Stil A foto-zemin + pill / Stil B petrol yeşili zemin + blob / Stil C beyaz-mint kart), **vurgu kelimesi işaretlemesi**.
**Ölçü de brief'e yazılmaz** — sabittir: post 1080×1350 (4:5), story 1080×1920.
Sabitler (logo, sol kenardan ülke bayrağı, turkuaz blob, alt CTA barı) marka standardıdır; nasıl uygulanacağı tasarımcıya aittir.

### 9c. Kurulmuş şablonlar (her yeni tip kurulunca güncelle)
> Brief üreticisi "bu tipi kur" mu yoksa "mevcut şablonu kullan" mı diyeceğini buradan bilir. Asana erişimi olmadığı için tek kaynak bu listedir.

| Şablon | Durum | İlk kurulum |
|---|---|---|
| T1 · T2 · T3a · T3b · T3c · T4 · T5 · T6 · T7 · T8 · T9 · T10 | **hiçbiri kurulmadı** | — |

## 10. TUTARLILIK NOTLARI
- DENTCAMP kimliği: petrol yeşili + turkuaz + mint, DENTCAMP logosu, sol kenardan dalgalı bayrak, turkuaz blob, pill başlıklar, alt CTA barı.
- **AUSCAMP'in yeşil/altını ve UKCAMP'in mavi/kırmızısı DENTCAMP'e ASLA taşınmaz.**
- Ülke renkleri kullanılmaz; ülke ayrımı bayrakla yapılır.
- `text-transform` yasak (Türkçe i sorunu).
- Co-brand kuralı: OET/İngilizce → MEDCAMP · Almanca/FSP → ALMANGO.
- Marka adları her yerde büyük harf: DENTCAMP, CAMP GROUP, MEDCAMP, ALMANGO, AUSCAMP, UKCAMP.

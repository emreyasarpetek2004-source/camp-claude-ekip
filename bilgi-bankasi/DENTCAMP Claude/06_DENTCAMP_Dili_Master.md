# DENTCAMP Dili Master

> Kaynak: `~/dentcamp-vaka/content/metin.py` (`SES` bloğu — markanın yazılı ses spec'i), 4 ülke kataloğu (`~/dentcamp-katalog/content/`), `~/dentcamp-vaka/content/ulkeler.py`.
> Bu doküman **detay referanstır**; günlük caption üretiminde `01_Caption_ve_Dil_Rehberi.md` kullanılır.

---

## A. İKİ REGİSTER — hangisi nerede

DENTCAMP iki farklı yüzeyde iki farklı tonda konuşur. Karıştırılmaz.

| Yüzey | Register | Örnek |
|---|---|---|
| **Katalog, web, teklif, kurumsal belge** | **Ölçülü kurumsal.** Üçüncü tekil ("yürütülür"), motivasyon edebiyatı yok, riski açıkça söyler. | "Bu yol 'ucuz kestirme' değildir — en riskli yoldur." |
| **Instagram (post, caption, story, reels)** | **Kurumsal-hümanize.** Süreci bilen bir meslektaş konuşuyor — kurum değil, kurumdaki insan. **Birinci çoğul** ("yürütüyoruz"), okura "siz". Emoji işlevsel, ≤6. | "Almanya'da diş hekimi olarak çalışmak için önce dil şartını geçmeniz gerekiyor. 🇩🇪" |

> **Karar (12.08.2026):** DENTCAMP Instagram dili **UKCAMP kalıbından çıkarıldı.** 10 Ağustos'ta "UKCAMP stilini birebir uygula" denmişti; 12 Ağustos'ta kurumsal-hümanize sese geçildi. Emoji-yoğun, motive edici ton **artık geçerli değil.** Vaka belgesindeki ses spec'i Instagram'da da geçerli — tek fark: katalog üçüncü tekil ("yürütülür"), Instagram birinci çoğul ("yürütüyoruz").
>
> Ses tanımı artık skill'de: `~/.claude/skills/dentcamp-marka-sesi/SKILL.md`. Üslup denetimi: `camp-humanize`.

### Register'dan bağımsız — HER YERDE geçerli sert kurallar
1. **Marka adları büyük harf:** DENTCAMP, CAMP GROUP, MEDCAMP, ALMANGO, AUSCAMP, UKCAMP, USCAMP, DEUCAMP, NURSECAMP, PHYSIOCAMP, RESEARCHCAMP. Kesme: `DENTCAMP'in`, `DENTCAMP'te`. Asla "Dentcamp"/"DentCamp"/"Camp Group".
2. **Hitap "siz".** Motivasyon cümlelerinde nadiren "sen" kullanılabilir (UKCAMP'te olduğu gibi), ama varsayılan "siz"dir.
3. **"Aday" denmez.** Yurt dışına gidecek kişi **"diş hekimi"** ya da **"danışan"**tır. "Aday" yalnız işe başvuran kişi için kullanılır.
4. **"Rezidanslık" değil "asistanlık".** (kullanıcının tercihi.)
5. **Kaynaksız rakam yazılmaz.** Her sayı ya `07_Dis_Hekimligi_Konu_Listesi_ReShare.md` olgu bankasından gelir ya da brief'te `Kaynak:` satırıyla verilir.
6. **Hangi ülkeden söz edildiği net söylenir.** Dört ülke tek potada eritilmez.
7. **Üç olgu hiçbir içerikte geçmez** (kaynaklar çelişiyor): Almanya'daki yeni düzenlemenin yürürlük tarihi · Avustralya'daki %25'in hangi sınava ait olduğu · mentör sayısı ve isim listesi.
8. **Tipografik tırnak:** `" "` ve `'`.

---

## B. DÖRT İLKE (markanın kendi tanımı)

| İlke | Tanım |
|---|---|
| **Dürüstlük** | Riski gizlemiyoruz. Kendi metinlerimizde "bu en riskli yoldur" diyen cümleler var. |
| **Nezaket** | Danışana **siz** diye hitap ediyoruz. |
| **Sadelik** | Terimi kullanıyoruz; hemen ardından Türkçesini veriyoruz: *Approbation (tam ve süresiz mesleki lisans)*. |
| **Ölçü** | Motivasyon edebiyatı yapmıyoruz. Abartılı vaat vermiyoruz. |

> Instagram register'ı "Ölçü" ilkesini gevşetir (emoji, hook, coşku serbest) — ama **abartılı vaat** yasağı kalkmaz. "Kolay", "garanti", "6 ayda diploma" gibi ifadeler Instagram'da da yazılmaz. Coşku üsluptadır, vaatte değil.

### Kendi metinlerimizden — ton kalibrasyonu
- "Bu yol 'ucuz kestirme' değildir — en riskli yoldur." *(ABD süreci)*
- "Sınavı geçmek ve GDC'ye kaydolmak, İngiltere'de yasal olarak çalışabilmenizi sağlar; ancak otomatik bir iş garantisi vermez." *(İngiltere süreci)*
- "Yurt dışı diplomanız otomatik olarak tanınmaz; ancak ABD'den farklı olarak yeniden diş fakültesi okumanız gerekmez." *(Avustralya süreci)*

---

## C. TERİM SÖZLÜĞÜ — terim + hemen ardından Türkçesi

### Almanya
| Terim | Açılım |
|---|---|
| **Approbation** | tam ve süresiz mesleki lisans |
| **FSP** (Fachsprachprüfung) | mesleki Almanca sınavı |
| **Kenntnisprüfung** | bilgi sınavı — yazılı, sözlü ve pratik üç bölüm |
| **Bildungsgutschein** | Agentur für Arbeit'in kurs desteği belgesi |
| **Berufserlaubnis** | geçici çalışma izni |
| **ÖSD / telc / Goethe** | Almanca dil sınavları |

### Avustralya
| Terim | Açılım |
|---|---|
| **ADC** (Australian Dental Council) | Avustralya Diş Hekimliği Konseyi |
| **AHPRA** | sağlık meslekleri sicil kurumu — kayıt buradan yapılır |
| **ADC Pathway** | belge değerlendirmesi → yazılı sınav → pratik sınav |
| **OET** | sağlık profesyonellerine özel tıbbi İngilizce sınavı |

### İngiltere
| Terim | Açılım |
|---|---|
| **GDC** (General Dental Council) | İngiltere diş hekimliği sicili |
| **ORE** (Overseas Registration Exam) | yurt dışı mezunları için iki bölümlü sınav |
| **LDS** | ORE'ye eşdeğer, üç bölümlü alternatif sınav |
| **IELTS Academic** | genel 7,0 ve her bölümde en az 6,5 |

### ABD
| Terim | Açılım |
|---|---|
| **DENTPIN** | ABD sınav sisteminin kimlik numarası |
| **INBDE** | ABD ulusal diş hekimliği sınavı |
| **course-by-course** | ders bazlı diploma değerlendirme raporu |
| **Advanced Standing** (CAAPID) | CODA akreditasyonlu fakültede yeniden diş hekimliği |
| **AEGD / GPR** | mezuniyet sonrası genel diş hekimliği programları |
| **CODA** | ABD diş hekimliği eğitim akreditasyon kurumu |

### Kurum içi
- **CAMP Hattı:** +90 552 000 78 38
- **MEDCAMP** (@medcampenglish): tıbbi İngilizce / OET
- **ALMANGO:** Almanca A1–B2 + FSP, ÖSD sınav merkezi akreditasyonlu

---

## D. KİME ANLATIYORUZ — iki kitle

| Kitle | Durum | İçerikte nasıl görünür |
|---|---|---|
| **Diş hekimliği öğrencileri** | Henüz mezun değiller. Yolu şimdiden planlıyorlar. | "Mezun olmadan başlanabilecek adımlar", dil hazırlığı, ülke seçimi, zaman planı |
| **Diş hekimleri** | Diplomaları ellerinde. Soruları: hangi ülke, hangi yol? | Süreç adımları, sınav detayı, maliyet, belge yönetimi, karar kriterleri |

Her içerik hangi gruba seslendiğini belli etmeli. İki gruba birden seslenen içerik yazılabilir, ama "kime" sorusunun cevabı brief'te yazılı olur.

---

## E. YAPIN / KAÇININ

**YAPIN**
- Tek bir somut gerçekle açın.
- Kullandığınız her sayının bir kaynağı olsun.
- Hangi ülkeden söz ettiğinizi net söyleyin.
- Okura "siz" diye hitap edin.
- Terimi kullanın, hemen Türkçesini verin.

**KAÇININ**
- Kaynağı olmayan rakam.
- Dört ülkeyi tek potada eriten genellemeler.
- "Kolay", "garanti", "hemen" gibi vaat sözleri.
- Süreyi/maliyeti olduğundan kısa/ucuz gösteren ifadeler.
- Mentör sayısı/isim iddiası (anlaşmalar sürüyor).

---

## F. MARKANIN DURUMU (Ağustos 2026)
- `dentcamp.com.tr` yayında.
- Dört ülkenin süreçleri çıkarıldı, kataloglar basıldı.
- Mentör anlaşmaları **sürüyor**.
- Lansman **15 Ağustos 2026**.
- Sosyal medyada **henüz tek bir içerik yok** — sıfırdan başlıyoruz.

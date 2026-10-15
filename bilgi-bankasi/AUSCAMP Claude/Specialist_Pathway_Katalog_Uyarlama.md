# AUSCAMP — SPECIALIST PATHWAY KATALOG
## Sayfa-Sayfa Tasarım Uyarlaması

**Kaynak tasarım:** `AUSCAMP_Standart_Pathway.pdf` (8 sayfa)
**Kaynak içerik:** `Spealist_pathway_katalog.pdf` (ham taslak)
**Üretilen PDF:** `AUSCAMP_Specialist_Pathway.pdf` — **11 sayfa**, A4 596×842, fontlar gömülü.

> ### Bölüm bütünlüğü kuralı
>
> **Hiçbir bölüm iki sayfaya bölünmüyor.** Her sayfa bir başlıkla (H1 veya yeşil bar) başlıyor,
> o bölüm aynı sayfada bitiyor. Sayfa altlarında kalan boşluk bunun bedeli — bilinçli tercih.
>
> Sayfa sonları tahminle değil ölçümle konuyor: her bölüm önce kendi sayfasına basılıp gerçek
> yüksekliği ölçülüyor, sonra 719pt'lik kullanılabilir alana sığdığı kadar bölüm yerleştiriliyor.
>
> | PDF sayfası | Bölümler |
> |---|---|
> | 1 | Kapak |
> | 2 | AUSCAMP Nedir? + Mentörlerimiz |
> | 3 | Specialist Pathway · Değerlendirme Neye Dayanır? · Uygunluk Görüşmesi · Ne Sağlar? |
> | 4 | Neden Olmadan İlerlenmemelidir? · Bu Neden Çok Önemli? + "Kısaca" kutusu |
> | 5 | Süreç Nasıl İlerler? · 1. Dil Yeterliliği · 2. Kolej Değerlendirmesi ve Uzmanlık Mülakatı |
> | 6 | 3. Denklik Sonucu · 4. İş Başvuruları & Mülakatlar · 5. Avustralya'da Uzman Olarak Çalışma |
> | 7 | Hizmetlerimiz · 1. Dil Yeterliliği Süreci · 2. Kolej Başvuru Süreci · 3. Kolej Mülakatı Koçluğu |
> | 8 | 4. Denklik Sonrası Süreç & Yerleşme · A'dan Z'ye Mentörlük Desteği |
> | 9 | Kavramlar & Terimler (12 terim) |
> | 10 | Sık Sorulan Sorular (12 soru) |
> | 11 | Specialist Pathway Road Map + iletişim |
>
> Aşağıdaki bölüm planı bu sayfalamayla **birebir örtüşüyor** — Canva'da doğrudan uygulanabilir.

**Nasıl kullanılır:** Canva'da Standart Pathway katalogunu çoğalt. Aşağıdaki her sayfa için
belirtilen slota karşılık gelen metni yapıştır. `**kalın**` işaretli yerler Telegraf **Bold**,
gerisi Telegraf Regular. `⚠` işaretli satırlar taslaktan değiştirilmiş yerler — sonundaki
**Düzeltme Listesi** bölümünde gerekçesiyle listelendi.

---

# SAYFA 1 — KAPAK

**Tasarım:** Standart kapak birebir. Sol yeşil şerit + sarı blob'lar, beyaz yuvarlak kart,
fotoğraf kolajı.

▸ **YEŞİL PILL** (beyaz Telegraf Bold ~47 pt, yuvarlak köşeli `#016531` dolgu)

```
Avustralya'da
```

▸ **ANA BAŞLIK** (yeşil `#016531` Telegraf Bold, iki satır, ~40 pt) ⚠

```
Sınavsız Uzman
Doktor Denkliği
```

> ⚠ Standart'ta tek satır ("Doktorluk Kariyeri", 47 pt). Bu başlık daha uzun olduğu için
> iki satıra bölünüp punto ~40 pt'ye düşürülür. Pill genişliği aynı kalır.

▸ **LOGO SATIRI** (AUSCAMP logosu + yeşil OpenSans ExtraBold ~25 pt)

```
[AUSCAMP logosu] | SPECIALIST PATHWAY
```

▸ **ALT SATIR** (yeşil Telegraf Regular ~17 pt, iki satır, ortalı)

```
(Uzman ve kıdemli asistan hekimler için
denklik ve süreç rehberi)
```

▸ **GÖRSEL KOLAJ** ⚠ **(değişti — onaylandı)**

Standart kapakta genç pratisyen görünümlü iki hekim var; uzman katalogunda kıdemli/uzman
izlenimi veren görsel kullanılacak.

**Kullanılacak asset:**

```
~/auscamp-web-migration/ai_foto/uzman-orj.jpg     (2752 × 1536)
```

Olgun/kıdemli hekim grubu, arkada Opera Binası + Harbour Bridge, merkezde Türk tipli figür.
Elindeki uzman görselleri arasında kapağa uygun olan tek dosya bu.

**Kullanma yöntemi — önerilen:** Canva'da **"Arka Planı Kaldır"** uygulayıp hekimleri kesme
görsel (cut-out) hâline getir, Standart kapaktaki iki hekimin yerine koy. **Sydney kolaj
kartları aynen kalsın** — böylece kapak kompozisyonu Standart katalogla birebir aynı olur.

**Kadraj:** 5 figürün tamamı Standart'taki iki-hekim alanına göre fazla geniş kalır.
**Ortadaki 3 figürü** (sakallı merkez figür + iki yanındaki erkek hekim) kırp — uzman/kıdemli
okuması en güçlü grup bu.

> ⚠ **Baskı notu:** Ortadaki 3 figür kırpıldığında yaklaşık 1050 × 1536 px kalıyor. Dijital
> PDF ve ekran kullanımı için fazlasıyla yeterli; **300 dpi matbaa baskısında** bu alan için
> ideal ~1390 × 1530 px gerekiyor, yani hafif yumuşak çıkabilir. Katalog basılacaksa bu
> görseli büyütmek (upscale) veya 5 figürü koruyup fotoğraf alanını genişletmek gerekir.

**Kullanılamaz olan diğer iki dosya** (kontrol ettim, not düşüyorum ki tekrar bakmayasın):

| Dosya | Neden olmaz |
|---|---|
| `stok_foto/uzman-hero.jpg` | Elinde farmakoloji kitabı olan genç öğrenci grubu — uzman değil, öğrenci okuması veriyor |
| `stok_foto/uzman-b2.jpg` | Önlükte **"Urologic Oncology Branch — National Cancer Institute"** rozeti var; gerçek bir ABD kurumunun markası, AUSCAMP katalogunda kullanılamaz |

---

# SAYFA 2 — AUSCAMP NEDİR? + MENTÖRLERİMİZ

**Tasarım:** Standart s2 birebir. Sağ üst blob · alt orta logo.

▸ **H1** (yeşil Telegraf Bold ~25 pt, BÜYÜK HARF)

```
AUSCAMP NEDİR?
```

▸ **GÖVDE** (3 paragraf, Telegraf Regular 12 pt)

```
AUSCAMP, Avustralya'da kariyer yapmak isteyen hekimler için nitelikli çözümler sunan ve
**tamamen hekimler tarafından kurulmuş profesyonel bir eğitim ve danışmanlık kurumudur.**

Sınav süreçlerinden işe yerleşime, lisans adımlarından Avustralya'daki yeni hayatınıza
uzanan bu yolculukta, **her aşamayı doğru sırayla ve eksiksiz bir yönetim anlayışıyla
baştan sona sizinle birlikte yürütür.**

Bugün AUSCAMP, Avustralya'da aktif olarak çalışan deneyimli hekim mentörlerimiz ile
Türkiye'de süreci koordine eden güçlü ekibimizin oluşturduğu entegre bir yapı olarak,
danışanlarına **kişiye özel rehberlik sunmaktadır.**
```

▸ **H1**

```
MENTÖRLERİMİZ
```

▸ **INTRO PARAGRAF** ⚠ (Standart s2'de bu paragraf yok — grid ~3 satır aşağı kayar)

```
AUSCAMP mentör ağı, Avustralya'da aktif olarak çalışan ve bu süreci bizzat tamamlamış
hekimlerden oluşur. Her mentör, adayın ihtiyacı olan pathway üzerinden danışanlara
rehberlik eder; **denklik sürecinden işe yerleşmeye, kolej mülakatlarından sistem
adaptasyonuna kadar gerçek saha deneyimini** paylaşır.
```

> ⚠ Taslakta "sınav sürecinden işe yerleşmeye, mülakatlardan..." yazıyordu. Specialist
> Pathway sınavsız bir yol olduğu için "denklik sürecinden... kolej mülakatlarından..."
> olarak düzeltildi.

▸ **MENTÖR GRID** — 4'lü satırlar. Foto: yeşil daire + sarı yarım halka. İsim: açık nane
`#d4ece0` pill içinde yeşil Arimo Bold. Altında 3 satır küçük bold yeşil.
**Specialist katalog olduğu için Specialist Pathway mentörleri ilk satıra alınır** ⚠

| | | | |
|---|---|---|---|
| **Doç. Dr. İbrahim Ethem Cakcak**<br>Genel Cerrah & Mentör<br>Wollongong, NSW<br>(Specialist Pathway) | **Uzm. Dr. Tolga Karacan**<br>KHD Uzmanı & Mentör<br>Canberra, ACT<br>(Specialist Pathway) | **Uzm. Dr. Duygu Batu**<br>Dahiliye Uzmanı & Mentör<br>Avustralya (farklı eyaletler)<br>(Specialist Pathway) | **Dr. Fidan Şenova**<br>Co-Founder & Mentör<br>Melbourne, VIC<br>(Standard Pathway) |
| **Dr. Gizem Pehlivan**<br>Kırsal Aile Hekimliği Asistanı & Mentör<br>Melbourne, VIC<br>(Standard Pathway) | **Dr. Onur Uysal**<br>Acil Tıp Asistanı & Mentör<br>Queensland, QLD<br>(Standard Pathway) | **Dr. İlayda Ertürk**<br>Mentör<br>Genel Cerrahi - RMO<br>Yeni Zelanda | **Dr. Çağlar Aktuna**<br>Mentör<br>Melbourne, VIC<br>(Standard Pathway) |
| **Dr. Furkan Hamamcı**<br>Co - Founder<br>İstanbul | **Dr. Burak Şenocak**<br>Co - Founder & Genel Koordinatör<br>İstanbul | **Dr. Başak Karazağ**<br>Danışan Koordinatörü<br>İstanbul | |

---

# SAYFA 3 — SPECIALIST PATHWAY

**Tasarım:** Standart s3 birebir. Sağ üst blob · alt orta logo.

▸ **H1**

```
SPECIALIST PATHWAY
```

▸ **H1 ALT SATIRI** (yeşil Telegraf Regular ~14 pt)

```
(Uzman Hekimler · Kıdemli Asistan Hekimler)
```

▸ **GÖVDE**

```
Specialist Pathway, Türkiye'de uzmanlığını tamamlamış hekimlerin Avustralya'da uzman
doktor olarak çalışabilmeleri için kullanılan **sınavsız, resmi denklik yoludur.** Bu yol;
uzmanlık eğitiminin içeriği, klinik deneyim, mesleki yetkinlikler ve ilgili kolejin yaptığı
değerlendirmeler doğrultusunda ilerler. **Avustralya'da her uzmanlık alanı kendi kolejine
sahiptir.** Uzman hekimlerin değerlendirmesi, başvurulan kolejin belirlediği kriterlere göre
yapılır ve her branş için süreç farklılık gösterebilir.
```

▸ **YEŞİL BAR**

```
DEĞERLENDİRME NEYE DAYANIR?
```

▸ **GÖVDE + MADDE LİSTESİ** ⚠ (taslakta tek uzun cümleydi, Standart'ın madde düzenine çevrildi)

```
Değerlendirme süreci sınavlardan ziyade şu üç unsur üzerinden yürütülür:

 •  Adayın akademik ve mesleki geçmişini detaylı şekilde ortaya koyan **başvuru
    belgelerinin incelenmesi**
 •  Klinik deneyim ve yetkinliklerin **portfolyo üzerinden değerlendirilmesi**
 •  Kolej tarafından gerçekleştirilen **yapılandırılmış mülakatlar**
```

▸ **YEŞİL BAR**

```
UYGUNLUK GÖRÜŞMESİ
```

▸ **ALT SATIR** (yeşil Telegraf Bold 12 pt, bar'ın altında)

```
(Specialist Pathway'de neden ilk ve en kritik adımdır?)
```

▸ **GÖVDE**

```
Specialist Pathway, sınav odaklı bir süreç değildir. Bu yol, tamamen uzmanlık eğitimi,
klinik deneyim ve ilgili kolejin değerlendirmesi üzerinden ilerler.

Bu nedenle sürece başlamadan önce atılacak en önemli adım, **adayın branşına ve geçmişine
özel uygunluğun doğru şekilde analiz edilmesidir.** Bu nedenle AUSCAMP olarak, Specialist
Pathway sürecine doğrudan başlatmak yerine, **ilk olarak Uygunluk Görüşmesi ile başlarız.**
```

---

# SAYFA 4 — UYGUNLUK GÖRÜŞMESİ (devam)

**Tasarım:** Standart s5 gibi — H1 yok, s3'ten devam. Sağ üst blob · alt orta logo.

▸ **YEŞİL BAR**

```
AUSCAMP UYGUNLUK GÖRÜŞMESİ NE SAĞLAR?
```

▸ **GÖVDE + MADDE LİSTESİ**

```
Bu görüşmede;

 •  Uzmanlık eğitiminizin **süresi ve içeriği**
 •  **Klinik deneyiminizin** kapsamı
 •  Branşınıza uygun **Avustralya kolejleri**
 •  Olası denklik senaryoları (**Substantial / Partial**)
 •  **Gerçekçi riskler ve güçlü yönler** detaylı şekilde değerlendirilir.

Amaç, adayın yanlış umutlarla değil; **doğru beklenti, doğru strateji ve güvenli bir yol
haritası** ile sürece başlamasını sağlamaktır.
```

▸ **YEŞİL BAR**

```
NEDEN UYGUNLUK GÖRÜŞMESİ OLMADAN İLERLENMEMELİDİR?
```

▸ **GÖVDE + MADDE LİSTESİ**

```
Avustralya'daki her uzmanlık alanı kendi kolejine sahiptir ve her kolejin;

 •  kabul kriterleri
 •  uzmanlık süresi beklentileri
 •  klinik sorumluluk tanımları
 •  denklik yaklaşımı

birbirinden farklıdır. Bir aday, kendi branşının detayları ve kolejin beklentileri
netleşmeden sürece girerse;

 •  **Yanlış kolej başvurusu** yapılabilir
 •  **Eksik veya uygun olmayan belgeyle** başvuru gerçekleşebilir
 •  **Gerçekçi olmayan denklik beklentisi** oluşabilir

ve en kritik risk: **Kolejden olumsuz (red) bir değerlendirme alınabilir.**
```

▸ **YEŞİL BAR**

```
BU NEDEN ÇOK ÖNEMLİ?
```

▸ **GÖVDE + MADDE LİSTESİ**

```
**Kolej değerlendirmeleri kayıt altına alınır.** Uygunluk analizini yapmadan, yanlış
stratejiyle yapılan bir ilk başvuru;

 •  adayın **zamanını**
 •  ciddi **maddi kaynaklarını**
 •  ve en önemlisi **gelecekte aynı koleje yapılacak başvuruların şansını**

olumsuz etkileyebilir. Ne yazık ki, ilk başvuruda alınan kötü bir değerlendirme, sonraki
başvurularda adayın aleyhine çalışabilir.
```

▸ **VURGU KUTUSU** ⚠ (açık nane `#d4ece0` dolgulu yuvarlak kutu, içinde yeşil Telegraf Bold —
Standart'ta bu öğe yok, kapak pill'i ve mentör pill'i ile aynı dilde yeni bir kutu)

```
Kısaca: Uygunluk görüşmesi yapılmadan atılan her adım, geri dönüşü zor riskler barındırır.
AUSCAMP, adayın zamanını ve emeğini korumak için bu adımı sürecin merkezine koyar.
```

---

# SAYFA 5 — SÜREÇ NASIL İLERLER? (1–2)

**Tasarım:** Standart s3/s4 birebir. Sağ üst blob · alt orta logo.

▸ **H1**

```
SÜREÇ NASIL İLERLER?
```

▸ **H1 ALT SATIRI**

```
(Uygunluk Görüşmesi Olumlu Geçtikten Sonra)
```

▸ **GÖVDE**

```
Uygunluk görüşmesi sonucunda adayın Avustralya Specialist Pathway sürecine uygun bulunması
halinde, adayı **planlı ve kontrollü** bir süreç bekler.
```

▸ **YEŞİL BAR**

```
1. DİL YETERLİLİĞİ (OET / IELTS)
```

▸ **GÖVDE**

```
Doktorlara özel tıbbi İngilizce sınavı olan **OET** için süreç, adayın mevcut seviyesinin
belirlenmesiyle başlar. **MEDCAMP** bünyesinde, adayın seviyesine ve hedef takvimine uygun
bir çalışma planı oluşturulur.
```

▸ **ARA BAŞLIK** (yeşil Telegraf Bold 12 pt, bar değil)

```
Eğitim süreci:
```

▸ **MADDE LİSTESİ**

```
 •  **Seviye Tespiti** ile başlangıç noktası belirlenir.
 •  Uzman mentörümüzün rehberliğinde **kişiye özel çalışma programı** hazırlanır.
 •  Eğitimler haftada **2–3 gün, online Zoom dersleri** şeklinde yürütülür.
 •  **Speaking, Writing, Reading, Listening** becerileri OET formatına uygun şekilde çalışılır.
 •  Eğitimler, yabancı ve Türk **OET Teacher sertifikalı** eğitmen tarafından verilir.
 •  İhtiyaca göre **birebir mentörlük** desteği sağlanır.
 •  **OET Study Portal** üzerinden **80'den fazla** kayıtlı derse erişim sağlanır.
 •  **İnteraktif testler ve deneme sınavları** sayesinde adaylar OET formatına birebir
    pratik yapma imkânı bulur.

Amaç; yalnızca sınavı geçmek değil, **klinik ortamda güvenli ve etkili iletişim kurabilecek
dil yeterliliğini** kazandırmaktır.
```

▸ **YEŞİL BAR**

```
2. KOLEJ DEĞERLENDİRMESİ VE UZMANLIK MÜLAKATI
```

▸ **GÖVDE**

```
Avustralya'da her uzmanlık alanının kendi koleji bulunur ve uzman hekimlerin değerlendirmesi
bu kolejin belirlediği mesleki standartlara göre yapılır. Bu aşamada adayın **uzmanlık
eğitimini ve klinik pratiğini gösteren resmî belgeler** incelenir. Kolej, adayın uzmanlık
süresi, eğitim içeriği, klinik sorumluluk düzeyi ve uzmanlık pratiğinin kapsamını kendi
eğitim müfredatıyla karşılaştırır.

Belge incelemesinin ardından aday, **uzmanlık mülakatına** alınır. **Bu mülakat bir bilgi
sınavı değildir.** Amaç; adayın belgelerle ortaya koyduğu uzmanlık pratiğini, Avustralya
sağlık sistemi içinde **güvenli, tutarlı ve hasta güvenliği odaklı** şekilde sürdürebilip
sürdüremeyeceğini değerlendirmektir. Kolej, belge incelemesi ve mülakatı birlikte ele alarak
adayın Avustralya'da uzman doktor olarak çalışmaya uygunluğuna karar verir.
```

---

# SAYFA 6 — SÜREÇ NASIL İLERLER? (3–5)

**Tasarım:** H1 yok, s5'ten devam. Sağ üst blob · alt orta logo.

▸ **YEŞİL BAR**

```
3. DENKLİK SONUCU
```

▸ **GÖVDE**

```
Kolej tarafından yapılan belge incelemesi ve uzmanlık mülakatı sonucunda aday için bir
**denklik sonucu** belirlenir. Bu sonuç, adayın uzmanlık eğitiminin Avustralya
standartlarıyla hangi ölçüde uyumlu olduğunu ifade eder. Specialist Pathway'de en sık
karşılaşılan iki denklik sonucu bulunur:
```

▸ **ARA BAŞLIK + GÖVDE** ⚠

```
**Substantial Denklik**
Bu sonuç, adayın uzmanlık eğitimi ve klinik pratiğinin Avustralya'daki uzmanlık
standartlarıyla **büyük ölçüde örtüştüğünü** gösterir. Aday, **9–12 ay** süren gözetimli
çalışma döneminin ardından **tam uzmanlık denkliği** alarak Avustralya'da uzman doktor
olarak daha bağımsız şekilde çalışmaya devam eder.
```

> ⚠ Taslakta "maksimum bir yılı bulan gözetimli çalışma" yazıyordu → **9–12 ay** olarak
> düzeltildi (AUSCAMP'in tüm içeriklerinde kullanılan rakam).

▸ **ARA BAŞLIK + GÖVDE** ⚠

```
**Partial Denklik**
Bu sonuç, adayın uzmanlık eğitiminin **büyük oranda kabul edildiğini** ancak bazı alanlarda
tamamlanması gereken **ek gereklilikler** bulunduğunu ifade eder. Partial denklik ile aday,
sürece **kıdemli asistan (registrar) pozisyonunda** başlar; belirlenen eksik alanları
tamamladıktan sonra **uzman doktor olarak** çalışmaya devam eder ve sürecin sonunda tam
denklik elde edebilir. Bu ek gereklilikler, başvurulan branşın ve ilgili kolejin
kriterlerine bağlı olarak değişebilir. Bazı branşlarda süreç; gözetimli çalışma, portfolyo
değerlendirmesi veya ek sınav/uygulamalara tabi tutulmayı da içerebilir.
```

> ⚠ **Karar gerektiriyor.** Taslağın gövdesi "Partial denklik ile aday uzman doktor olarak
> çalışmaya başlayabilir" diyordu; SSS bölümü ise "aday ilk yıl kıdemli asistan (registrar)
> pozisyonunda başlar" diyordu — aynı katalogda çakışıyordu. **SSS versiyonunda
> birleştirildi.** Ters tercih edilirse bu paragraf ve SSS'deki ilgili cevap birlikte
> değişmeli.

▸ **YEŞİL BAR**

```
4. İŞ BAŞVURULARI & MÜLAKATLAR
```

▸ **GÖVDE**

```
Dil ve klinik değerlendirmelerin tamamlanmasının ardından aday, Avustralya sağlık sistemi
içinde çalışabileceği pozisyonlara başvurular yapmaya başlar. Bu aşama, **teorik
yeterliliklerin pratiğe taşındığı kritik bir geçiş noktasıdır.** İşe alım sürecinde
gerçekleştirilen mülakatlar; **klinik senaryolar, hasta güvenliği, iletişim becerileri ve
ekip çalışmasına uyum** gibi başlıklar üzerinden değerlendirilir.
```

▸ **YEŞİL BAR**

```
5. AVUSTRALYA'DA UZMAN OLARAK ÇALIŞMA
```

▸ **GÖVDE**

```
Denklik süreci ve işe alım aşamalarının tamamlanmasının ardından aday, Avustralya'da
**uzman doktor olarak çalışmaya başlar.** Bu aşamada aday, Avustralya'daki hastane ve sağlık
kuruluşlarında aktif görev alır; **multidisipliner ekiplerle** çalışır ve klinik
uygulamalarını Avustralya standartlarına uygun şekilde yürütür. Kolej tarafından tanımlanan
koşulların tamamlanmasıyla birlikte aday, **tam uzmanlık denkliği** alarak Avustralya'da
uzman doktor olarak daha bağımsız ve uzun vadeli bir kariyere devam edebilir.
```

---

# SAYFA 7 — HİZMETLERİMİZ (SPECIALIST PATHWAY)

**Tasarım:** Standart s4 birebir. Sağ üst blob · alt orta logo.

▸ **H1**

```
HİZMETLERİMİZ
```

▸ **H1 ALT SATIRI** (yeşil Telegraf Bold ~14 pt)

```
(SPECIALIST PATHWAY)
```

▸ **GÖVDE**

```
AUSCAMP, Specialist Pathway sürecini; uzman hekimlerin Avustralya'daki denklik ve yerleşme
sürecini **doğru stratejiyle, kontrollü ve şeffaf şekilde** ilerletebilmeleri için
yapılandırır. Bu kapsamda sunulan hizmetler, sürecin her aşamasının birbiriyle uyumlu
şekilde ilerlemesini hedefler.

Specialist Pathway, **sınav odaklı değil; belge, içerik ve mülakat temelli** bir süreçtir.
Bu nedenle süreç yönetimi, doğru yönlendirme ve sistem bilgisi kritik önem taşır.
```

▸ **YEŞİL BAR**

```
1. DİL YETERLİLİĞİ SÜRECİ (OET) X MEDCAMP
```

▸ **GÖVDE**

```
Doktorlara özel tıbbi İngilizce sınavı olan **OET** için seviye tespiti yapılır. Bu
doğrultuda, **MEDCAMP** bünyesinde sunulan OET eğitimi kapsamında adayın seviyesine ve hedef
takvimine uygun bir çalışma programı oluşturulur. Online dersler, kayıtlar ve materyallerle
süreç sistemli şekilde ilerler. Amaç, sınavı geçmenin yanı sıra **klinik ortamda güvenli ve
etkili iletişim** kurabilecek dil yeterliliğini sağlamaktır.
```

▸ **YEŞİL BAR**

```
2. KOLEJ BAŞVURU SÜRECİ
```

▸ **GÖVDE + MADDE LİSTESİ**

```
Adayın branşına uygun Avustralya koleji belirlenerek başvuru süreci planlanır. Kolej
başvuruları, her branşın kendi prosedürleri ve beklentileri doğrultusunda ilerler.

Bu aşamada;

 •  **Başvuru dosyasının bütünlüğü**
 •  **Kolejin talep ettiği ek belgeler**
 •  **Yazışmalar ve güncellemeler**

sürecin akışına uygun şekilde takip edilir. Başvurunun **doğru kolej, doğru zamanlama ve
doğru içerikle** yapılması, denklik sonucunu doğrudan etkileyen unsurlar arasındadır.
```

▸ **YEŞİL BAR**

```
3. KOLEJ MÜLAKATI KOÇLUĞU & SİMÜLASYONLAR
```

▸ **GÖVDE + MADDE LİSTESİ**

```
Kolej mülakatları, **Specialist Pathway sürecinin en kritik aşamasıdır.** Bu mülakatlar
bilgi sınavı değildir; adayın uzmanlık pratiğini Avustralya sağlık sistemi içinde güvenli ve
uygun şekilde sürdürebilip sürdüremeyeceği değerlendirilir.

Bu nedenle adaylar;

 •  Uzmanlık alanına özgü **klinik senaryolar**
 •  **Vaka yönetimi ve klinik karar alma** yaklaşımı
 •  **Hasta güvenliği ve etik sorumluluk**

başlıklarında mülakata hazırlanır. **Mock interview** çalışmalarıyla adayın mülakat pratiği
güçlendirilir ve adayın uzmanlık pratiğini net ve tutarlı şekilde ifade edebilmesi hedeflenir.
```

---

# SAYFA 8 — HİZMETLERİMİZ (devam)

**Tasarım:** H1 yok üstte, s7'den devam. Sağ üst blob · alt orta logo.

▸ **YEŞİL BAR**

```
4. DENKLİK SONRASI SÜREÇ, İŞ BAŞVURULARI & YERLEŞME
```

▸ **GÖVDE**

```
AUSCAMP, kolej değerlendirmesi sonucunda alınan **Substantial veya Partial** denklik
kararına göre süreci iş başvuruları ve yerleşme aşamasına taşır. Denklik sonucuna uygun
uzman pozisyonları belirlenir ve başvurular bu çerçevede planlanarak yürütülür.

**Substantial** denklik durumunda adayın gözetimli çalışma süreci ve tam denklik adımları
planlanır. **Partial** denklik durumunda ise çalışırken tamamlanması gereken ek
gereklilikler dikkate alınarak sürecin kesintisiz ilerlemesi sağlanır.

Amaç, adayın Avustralya'da uzman doktor olarak kariyerine **planlı, güvenli ve
sürdürülebilir** şekilde başlamasını sağlamaktır.
```

▸ **YEŞİL BAR**

```
A'DAN Z'YE MENTÖRLÜK DESTEĞİ
```

▸ **GÖVDE**

```
AUSCAMP Specialist Pathway süreci boyunca adaylara, **Avustralya'da bu yolu bizzat
tamamlamış uzman hekim mentörler** eşlik eder. Mentörlük desteği; denklik sürecinden kolej
mülakatlarına, iş başvurularından Avustralya'da uzman olarak çalışmaya başlanana kadar tüm
kritik aşamaları kapsar.

Bu destek, teorik yönlendirmelerden ziyade **gerçek saha deneyimine dayalı** bir rehberlik
sunar. Amaç, adayın süreci yalnız başına değil; **Avustralya sistemini içeriden bilen
hekimlerin deneyimiyle** güvenli ve bilinçli şekilde ilerletmesini sağlamaktır.

Mentörlük desteği yalnızca mesleki adımlarla sınırlı değildir. Uzman hekimler çoğunlukla
aileleriyle birlikte taşındığı için, **ev kiralama, ulaşım, araç edinme, yaşam düzeni ve
şehir adaptasyonu** gibi başlıklarda mentörlerin Avustralya deneyimine dayalı rehberlik
sağlanır.

Ayrıca adayların Avustralya'ya yerleştikten sonra network kurabilmesi için, Türkiye'den
Avustralya'ya gitmiş diğer sağlık profesyonelleriyle (mentörlerimizce kurulmuş olan
**Turkish Australian Medical Association** aracılığıyla) bağlantı kurulmasına destek olunur.
Bu sayede adaylar, mesleki olduğu kadar sosyal anlamda da daha hızlı ve güvenli bir
adaptasyon süreci yaşar.
```

---

# SAYFA 9 — KAVRAMLAR & TERİMLER

**Tasarım:** Standart s6 birebir. Sağ üst blob · alt orta logo.

▸ **H1**

```
KAVRAMLAR & TERİMLER
```

▸ **H1 ALT SATIRI**

```
(SPECIALIST PATHWAY)
```

▸ **GÖVDE**

```
Specialist Pathway sürecinde sık karşılaşılan bazı kavramlar, ilk etapta kafa karıştırıcı
olabilir. Aşağıda uzman hekimlerin en çok karşılaştığı temel terimler sade şekilde
açıklanmıştır.
```

▸ **MADDE LİSTESİ** (terim adı bold, altında açıklama — Standart s6 düzeni)

```
 •  **Specialist Pathway**
    Türkiye'de uzmanlığını tamamlamış hekimlerin, Avustralya'da uzman doktor olarak
    çalışabilmeleri için izlenen resmi denklik yoludur. Süreç sınavlara değil, belge ve
    mülakat değerlendirmelerine dayanır.

 •  **College (Kolej)**
    Avustralya'da her uzmanlık alanını düzenleyen yetkili meslek kuruluşudur (ör. RACP,
    RACS, ANZCA). Uzmanlık denklik değerlendirmeleri kolejler tarafından yapılır.

 •  **Substantial Denklik**
    Uzmanlık eğitiminin Avustralya standartlarıyla büyük ölçüde uyumlu bulunduğunu gösteren
    denklik sonucudur. 9–12 ay süren gözetimli çalışmanın ardından tam denklik sağlanır. ⚠

 •  **Partial Denklik**
    Uzmanlık eğitiminin büyük oranda kabul edildiği, ancak bazı alanlarda ek gerekliliklerin
    tanımlandığı denklik sonucudur. Aday, kıdemli asistan (registrar) pozisyonunda
    başlayarak bu gereklilikleri tamamlar; başvurulan branşın ve ilgili kolejin
    kriterlerine bağlı olarak süreç teorik ve/veya klinik sınavları da içerebilir. ⚠

 •  **OET / IELTS Academic**
    Uzman hekimlerin klinik ortamda güvenli iletişim kurabildiğini gösteren dil yeterliliği
    sınavlarıdır. Branşa ve koleje göre gereklilik değişebilir.

 •  **Supervisor**
    Gözetimli çalışma sürecinde adayın klinik pratiğini izleyen ve değerlendiren sorumlu
    uzman hekimdir.

 •  **Conditional / Limited Registration**
    Denklik sonucuna bağlı olarak, belirli koşullar altında uzman olarak çalışmayı sağlayan
    lisans türüdür.

 •  **Full Recognition (Tam Denklik)**
    Kolej tarafından tüm gerekliliklerin tamamlandığının kabul edilmesiyle verilen, tam
    uzmanlık yetkisini ifade eder.

 •  **AHPRA (Australian Health Practitioner Regulation Agency)**
    Avustralya'da sağlık mesleklerinin lisanslanması, kayıt altına alınması ve
    denetlenmesinden sorumlu resmî devlet kurumudur.

 •  **IMG (International Medical Graduate)**
    Avustralya dışında bir ülkede tıp eğitimini tamamlamış doktorları tanımlayan resmî
    terimdir. Türkiye mezunları bu kapsamdadır.

 •  **Registrar (Kıdemli Asistan)**
    Uzmanlık eğitimi sürecinde ileri kademede görev alan hekim pozisyonudur. Partial
    denklikte adayın ilk dönem çalıştığı pozisyondur.

 •  **Fellowship (FRACP / FRACS / FANZCA vb.)**
    İlgili kolejin tam üyeliğini ve uzmanlık yetkisini ifade eden unvandır.
```

> ⚠ Son 4 terim (AHPRA · IMG · Registrar · Fellowship) taslak sözlükte yoktu, senin onayınla
> eklendi. Bu yüzden sözlük kendi sayfasına alındı ve SSS s10'a taşındı — katalog 11 sayfa.

---

# SAYFA 10 — SIK SORULAN SORULAR

**Tasarım:** Standart s7 birebir. **Sağ üst köşe: sarı soru işareti kompozisyonu** (blob
yerine) · alt orta logo.

▸ **H1**

```
SIK SORULAN SORULAR
```

▸ **H1 ALT SATIRI**

```
(SPECIALIST PATHWAY)
```

▸ **MADDE LİSTESİ** (soru bold, altında cevap — Standart s7 düzeni)

```
 •  **Specialist Pathway gerçekten sınavsız mı?**
    Evet. Başvuru ve ilk değerlendirme aşamasında klinik bilgi sınavı yoktur. Değerlendirme,
    adayın belgeleri ve uzmanlık mülakatı üzerinden yapılır. Ancak Partial denklik verilmesi
    durumunda, başvurulan branşın ve ilgili kolejin kriterlerine bağlı olarak süreç
    içerisinde teorik ve/veya klinik sınavlar talep edilebilir.

 •  **Bu süreç ne kadar sürer?** ⚠
    Süre; adayın branşına, ilgili kolejin takvimine ve belge hazırlık hızına bağlı olarak
    değişir. Uygunluk görüşmesi olumlu geçen ve planlı ilerleyen adaylar için süreç
    yönetilebilir ve öngörülebilirdir. Substantial denklik alan adaylar, **9–12 ay** süren
    gözetimli çalışma döneminin ardından tam uzmanlık denkliğine ulaşır.

 •  **Denklik alınca hemen işe başlanır mı?**
    Hayır. Denklik sonrası iş başvuruları ve mülakat süreci yürütülür.

 •  **Partial denklik almak kötü bir sonuç mu?**
    Hayır. Partial denklik, sürecin kontrollü şekilde tamamlanmasını sağlayan yaygın bir
    sonuçtur.

 •  **Partial ile uzman olarak çalışabilir miyim?**
    Evet. Partial denklik kapsamında aday, sürece ilk yıl kıdemli asistan (registrar)
    pozisyonunda başlar. Tanımlanan ek gereklilikleri tamamladıktan sonra uzman doktor
    olarak çalışmaya devam eder.

 •  **Her uzmanlık alanının denkliği var mı?**
    Hayır. Denklik durumu branşa ve kolejin kriterlerine göre değişir.

 •  **Uzmanlık sürem kısa, yine de başvurabilir miyim?**
    Branşa göre değişir. Uygunluk, belge incelemesiyle netleşir.

 •  **Akademik yayın şart mı?**
    Hayır. Yayınlar artı sağlar ancak zorunlu değildir.

 •  **Yaş sınırı var mı?**
    Uzman olarak çalışmak için yaş sınırı yoktur; vize türüne göre sınırlamalar olabilir.

 •  **Ailemle birlikte gidebilir miyim?**
    Evet. Eş ve çocuklarla taşınmak mümkündür; vize türüne göre planlanır.

 •  **Avustralya'da uzman olarak uzun vadeli kalmak zorunda mıyım?**
    Hayır. Süreç, adayın kariyer hedeflerine göre şekillendirilebilir.
```

---

# SAYFA 11 — ROAD MAP + İLETİŞİM

**Tasarım:** Standart s8 birebir. Zigzag kesikli yeşil çizgi · numaralı yeşil daireler ·
her adımın yanında ikon · sağ üst blob · alt orta logo. **Bu sayfa taslakta yoktu, sıfırdan
kuruldu** ⚠

▸ **H1** (ortalı, yeşil Telegraf Bold ~25 pt)

```
SPECIALIST PATHWAY ROAD MAP
```

▸ **SARI VURGU ŞERİDİ** (`#ffcb00` dolgu, yeşil Telegraf Bold ~14 pt, ortalı)

```
Avustralya'da Sınavsız Uzman Denkliği Süreci
```

▸ **5 ADIM** — Standart s8'deki zigzag düzeni: 1 sol · 2 sağ · 3 sol · 4 sağ · 5 sol.
Her adımda: numaralı yeşil daire · yeşil Telegraf Bold başlık · ikon · yanında bold+regular
iki satır.

| # | Başlık (Telegraf Bold, yeşil) | Detay satırı |
|---|---|---|
| 1 | **Uygunluk Görüşmesi** | **Branş & Kolej Analizi**<br>Denklik senaryosu ve risk değerlendirmesi |
| 2 | **Dil Yeterliliği (OET / IELTS)** | **OET: B+ \| IELTS: 7.5+**<br>İngilizce iletişim yeterliliği |
| 3 | **Kolej Başvurusu &<br>Uzmanlık Mülakatı** | **Belge İncelemesi + Mülakat**<br>Sınav değil, portfolyo değerlendirmesi |
| 4 | **Denklik Sonucu** | **Substantial / Partial**<br>Gözetimli çalışma dönemi |
| 5 | **Avustralya'da Uzman<br>Olarak Çalışma** | **Full Recognition**<br>Tam uzmanlık denkliği |

> ⚠ Adım 2'deki puan eşikleri (OET B+ / IELTS 7.5+) Standart katalogdan taşındı; taslakta
> uzman hekimler için puan verilmemişti. Branşa/koleje göre değişebildiği için sözlükteki
> "OET / IELTS Academic" terimi bu farkı zaten belirtiyor.

▸ **İLETİŞİM BLOĞU** (Standart s8'den aynen)

```
[Sarı vurgulu iki satır]  DETAYLI BİLGİ İÇİN
                          BİZE ULAŞIN!

🌐 auscamp.com.tr          CAMP Hattı:              AUSCAMP Bilgi Hattı:
📷 camp2aus                +90 552 253 03 37        <WHATSAPP NUMARASI>
```

---
---

# DÜZELTME LİSTESİ

Taslaktan değiştirilen / eklenen her şey. Sırayla gözden geçir.

### 1. ⚠ Partial denklik çelişkisi — **kararını bekliyorum**

Taslak iki farklı şey söylüyordu:

| Yer | Ne diyor |
|---|---|
| Gövde (taslak s4) | "Partial denklik ile aday **uzman doktor olarak çalışmaya başlayabilir**" |
| SSS (taslak s7) | "aday sürece **ilk yıl kıdemli asistan (registrar)** pozisyonunda başlar" |

Aynı katalogda çakışıyordu. **SSS versiyonunda birleştirildi** (registrar başlangıcı) — kolej
partial comparability pratiğine daha yakın ve daha temkinli bir söz. Etkilenen yerler:
**s6 Partial Denklik paragrafı**, **s9 sözlükteki Partial Denklik terimi**, **s10 SSS cevabı**.

✅ **Kullanıcı onayladı (29.07.2026): registrar versiyonu kalıyor, değişiklik yok.**

### 2. Denklik süresi → 9–12 ay

Taslak: "maksimum bir yılı bulan gözetimli çalışma" → **"9–12 ay süren gözetimli çalışma"**.
AUSCAMP'in tüm içerik ve web metinlerinde kullanılan rakam bu. Geçtiği yerler: s6 Substantial
paragrafı, s8 sözlük, s9 SSS.

### 3. Eksik SSS eklendi: "Bu süreç ne kadar sürer?"

Standart katalogda var, uzman taslağında yoktu — satış görüşmelerinde en çok gelen soru.
s9'a ikinci soru olarak yerleşti, 9–12 ay bilgisi buraya oturdu.

### 4. Mentör intro cümlesi düzeltildi

Taslak: "sınav sürecinden işe yerleşmeye, mülakatlardan sistem adaptasyonuna kadar" →
**"denklik sürecinden işe yerleşmeye, kolej mülakatlarından sistem adaptasyonuna kadar"**.
Specialist Pathway sınavsız bir yol; "sınav süreci" ifadesi katalogun ana mesajıyla çelişiyordu.

### 5. Mentör grid sırası değişti

Specialist katalog olduğu için ilk satır Specialist Pathway mentörleri: İbrahim Ethem Cakcak ·
Tolga Karacan · Duygu Batu · Fidan Şenova. Fotoğraflar ve bilgiler aynı, sadece sıra.

### 6. Tekrar temizliği

"Avustralya'da her uzmanlık alanı kendi kolejine sahiptir" taslakta 3 yerde tam cümle olarak
geçiyordu (giriş · Kolej Değerlendirmesi · College terimi). Girişte tam bıraktım, diğerlerinde
akışa gömülü kısa hâlde kaldı.

### 7. Bir cümle madde listesine çevrildi

Taslakta "Değerlendirme süreci; sınavlardan ziyade... başvuru belgelerinin incelenmesi, klinik
deneyim... portfolyo... yapılandırılmış mülakatlar üzerinden yürütülür" tek uzun cümleydi.
Standart katalogun madde düzenine çevirdim (s3) — okunurluk için, kelimeler korundu.

### 8. Üretim notları silindi

"SPECIALIST PATHWAY KATALOG TASLAK" · "KAPAK" · "Her mentör için aynı şablon kullanalım /
Mentör Fotoğrafı olsun / Mentör Adı Soyadı olsun" · "GÖRSEL SADECE ÖRNEKTİR.."

### 9. Sıfırdan kurulan öğeler

| Öğe | Nerede | Neden |
|---|---|---|
| **Road Map sayfası** | s11 | Taslakta yoktu, Standart katalogun kapanış sayfası. 5 adım Specialist sürecine göre yazıldı. |
| **"Kısaca" vurgu kutusu** | s4 | Taslakta düz paragraftı; Uygunluk Görüşmesi bölümünün kapanış vurgusu olduğu için kutuya alındı. |
| **Kapak başlığı iki satıra** | s1 | "Sınavsız Uzman Doktor Denkliği" tek satıra sığmıyor. |

### 10. Eklenen öneriler — onaylandı 29.07.2026

- ✅ **4 ek sözlük terimi eklendi** (AHPRA · IMG · Registrar · Fellowship). Taslak sözlükte
  yoktu; uzman hekimin süreçte mutlaka karşılaştığı terimler. Sığdırmak için sözlük kendi
  sayfasına alındı (s9) ve SSS s10'a taşındı → **katalog 10 değil 11 sayfa.**

- ✅ **Yerleşme & network paragrafı eklendi** (s8, "A'dan Z'ye Mentörlük Desteği" bloğunun
  sonuna). Standart katalogda olan ama uzman taslağında hiç olmayan iki satış argümanı:
  (1) ev kiralama, ulaşım, araç edinme, yaşam düzeni, şehir adaptasyonu desteği;
  (2) **Turkish Australian Medical Association** üzerinden network kurulması. Uzman hekim
  çoğunlukla aileyle taşındığı için bu argümanlar uzman segmentinde daha güçlü.

- ✅ **Kapak görseli değişti.** Standart kapaktaki genç pratisyen fotoğrafı yerine
  `~/auscamp-web-migration/ai_foto/uzman-orj.jpg` kullanılacak (olgun hekim grubu + Sydney).
  Canva'da arka planı kaldırıp ortadaki 3 figür kırpılır, Sydney kolaj kartları korunur.
  Detay + baskı çözünürlüğü notu s1'de.

### 11. Açık kalan tek konu

- **Baskı çözünürlüğü.** Katalog matbaada basılacaksa kapak görselinin kırpılmış hâli 300 dpi
  için hafif yetersiz (1050 × 1536 px, ideal ~1390 × 1530). Sadece dijital PDF olarak
  kullanılacaksa sorun yok. Basılacaksa söyle — upscale ederim veya fotoğraf alanını
  genişletecek alternatif kadraj çıkarırım.

---

# TASARIM SİSTEMİ REFERANSI

Yeni sayfa kurmak veya bir öğeyi sıfırdan çizmek gerekirse.

| Öğe | Spesifikasyon |
|---|---|
| Sayfa | A4 · 595 × 842 pt · sol/sağ margin 50 pt |
| **Yeşil (ana)** | `#016531` — tüm gövde metni, başlıklar, bar dolguları |
| **Sarı** | `#ffcb00` — blob'lar, vurgu şeritleri, yarım halkalar |
| Açık nane | `#d4ece0` — mentör isim pill'i, vurgu kutusu |
| Kısık yeşil | `#3e604d` · Aksan yeşil `#78ac4b` · Turuncu `#fdb256` |
| Gövde | Telegraf Regular **12 pt** · vurgular Telegraf Bold (aynı punto) |
| H1 | Telegraf Bold ~25 pt · BÜYÜK HARF · yeşil · sola dayalı (x = 50 pt) |
| H1 alt satırı | Parantez içinde · Telegraf Bold/Regular ~14 pt · yeşil |
| Yeşil bar | Yuvarlak köşeli `#016531` dolgu · içinde **beyaz** Telegraf Bold ~12 pt |
| Madde | Yeşil nokta bullet · girinti ~18 pt |
| Kapak ana başlık | Telegraf Bold ~40–47 pt |
| Mentör kartı | Yeşil daire foto + sarı yarım halka · isim `#d4ece0` pill · 3 satır küçük bold |
| Sağ üst köşe | Sarı/yeşil blob kompozisyonu (her iç sayfada aynı) |
| Sol alt köşe | Sarı/yeşil blob + ortada AUSCAMP logosu (315 × 60) |
| SSS sayfası | Sağ üstte sarı soru işareti kompozisyonu (blob yerine) |

**Sayfa doluluk bütçesi:** Standart katalogun gövde sayfaları 2.200–2.735 karakter taşıyor.
Bir sayfa Canva'da taşarsa son bloğu bir sonraki sayfanın başına kaydır.

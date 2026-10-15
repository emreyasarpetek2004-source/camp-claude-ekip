# DENTCAMP — Ülke Katalogları (PDF derleyici)

Almanya, Avustralya, ABD ve İngiltere için dört ayrı A4 katalog, ayrıca dördünü
tek belgede özetleyen 10 sayfalık **toplu katalog** üretir.
Tasarım, AUSCAMP Specialist Pathway kataloğundan **birebir geometriyle** devralındı;
değişen yalnız renk paleti ve metin.

## Kullanım

```sh
python3 build_optimal.py            # dört ÜLKE kataloğunu derle
python3 build_optimal.py deu        # tek ülke
python3 build_optimal.py toplu      # toplu katalog (10 sayfa)
BODY_PT=13 python3 build_optimal.py aus   # gövde puntosunu değiştirerek dene
```

Argümansız çalıştırma bilerek yalnız dört ülkeyi derler; toplu katalog ayrıca
istenir.

Çıktılar `out/` altına yazılır.

## Yapı

| Dosya | Ne yapar |
|---|---|
| `theme.py` | DENTCAMP paleti + dört ülkenin tanımı (renk, bayrak, kapak) |
| `build.py` | Tasarım sistemi: CSS, kapak, mentör grid'i, road map, markup yardımcıları |
| `build_optimal.py` | Ölçüm tabanlı sayfalama + PDF birleştirme |
| `content/<ulke>.py` | **Sadece metin.** Değiştirilecek tek yer burası. |
| `content/toplu.py` | Toplu kataloğun metni (10 sayfa) |
| `tools/make_flags_toplu.py` | (kullanılmıyor) toplu kapağın dört bayraklı şeridi |
| `tools/make_cover_toplu_foto.py` | Toplu kapağın fotoğraf kartı (tek kadraj, dört ülke) |
| `tools/make_cover_toplu.py` | (kullanılmıyor) dört panelli eski kapak kartı |
| `content/_common.py` | Dört ülkede ortak metin (DENTCAMP nedir, MEDCAMP, mentörlük) |
| `tools/place_flag_photo.py` | Gerçek bayrak fotoğrafını kesip kapak köşesine oturtur |
| `tools/make_flags.py` | (kullanılmıyor) sentetik dalgalı bayrak üretici — yedek |
| `tools/prep_assets.py` | Logo, ikonlar; AUSCAMP'in yeşil ikonlarını turkuaza çevirir |
| `tools/prep_mentors.py` | Mentör portrelerini yüz kutusundan 480×600 (4:5) kırpar |
| `tools/make_flag_discs.py` | Mentör kartının bayrak halkası için kare bayrak kırpımı |
| `tools/prep_covers.py` | Kapak fotoğraflarını 452×252pt kart oranına kırpar |
| `tools/clean_watermark.py` | Gemini'nin sağ alt köşe parıltı filigranını siler |
| `tools/read_docx.py` | Kaynak broşürleri düz metne çevirir |
| `qa_check.py` | Mekanik denetim: taşma, çözünürlük, boş sayfa, yer tutucu, palet, CTA |

Varlıklar bir kez üretilir; sonrasında yalnız `build_optimal.py` çalıştırmak yeterli.

## Metin düzenleme

`content/<ulke>.py` içinde `BODY` listesi bölümlerden oluşur:

```python
H1("APPROBATION PATHWAY", "(Diş Hekimliği Öğrencileri)")   # yeni sayfa açar
BAR("1. ALMANCA DİL YETERLİLİĞİ")                          # koyu turkuaz pill
P("Metin. **kalın** otomatik <b>'ye döner.")
SUB("Ara başlık:")
UL(["madde", "madde"])
DL([("Terim", "Açıklama")])                                # SSS ve kavramlar
BOX("Vurgulu kutu (açık turkuaz zemin).")
```

Sayfalama **ölçümle** yapılır: metin uzayıp kısaldığında sayfa sonlarını elle
ayarlamaya gerek yok, `build_optimal.py` yeniden dağıtır.

## Renk

| Rol | Değer | AUSCAMP karşılığı |
|---|---|---|
| Koyu (H1, pill, gövde) | `#005b52` | `#016531` |
| Parlak (bloblar, dekor) | `#00d9bd` | `#ffcb00` |
| Kutu zemini | `#d6f2ed` | `#d4ece0` |
| Road map daireleri | `#2bbfa8` | `#78ac4b` |

**Ülke rengi kullanılmıyor** (kullanıcı kararı): dört katalog da yalnız DENTCAMP paletiyle
basılıyor. Önceden bayrak renkleri dar yüzeylerde (köşe dairesi, road map bandı, CTA
çipleri) aksan olarak geçiyordu; hepsi parlak turkuaza çevrildi. `theme.ACCENT`
tek noktadan yönetiliyor; `Country.accent` alanı duruyor ama CSS'te okunmuyor.

## Bayraklar

Dördü de **gerçek fotoğraf** — üçünün kaynağını kullanıcı verdi (`~/Downloads/`).

İngiltere iki kez değiştirildi (25-26 Ağustos 2026). İlk kaynak 600×600'lük,
direğe asılı, hiç dalgalanmayan bir kumaş bayrak karesiydi; kapakta bayrak değil
pano gibi duruyordu (kullanıcı: "bez bayrak olmasın"). İkinci deneme MOD arşivinden
dalgalı bir kareydi, o da beğenilmedi: lacivert ağırlıklı ve donuk kalıyordu.
Şimdiki kaynak Wikimedia Commons'taki Londra 2016 karesi — canlı kırmızı, net
dalga, hoist sayfa kenarına oturuyor. **Lisans: CC BY-SA 4.0** — ticari
kullanıma açık ama ATIF ve aynı lisansla paylaşım şartı var; künyeye satır
gerekip gerekmediği kullanıcının kararı.

Denenip elenen diğer adaylar `~/Downloads/uk_aday_*.jpg`: A (CC0) ışığa karşı
çekilmiş, bayrak koyu ve dürülü çıkıyor; C (CC0) bayrak kareyi tamamen
dolduruyor, kesilecek arka plan olmadığı için kapak kurgusuna girmiyor.


| Ülke | Kaynak | Çözünürlük | Kesim yöntemi |
|---|---|---|---|
| Avustralya | `Country-National-Flag-of-Australia-…avif` | 1000×1000 | rembg (bulanık şehir fonu) |
| İngiltere | `uk_londra_2016.jpg` | 5096×3398 | `--vision` |
| ABD | `usa.webp` | 600×600 | `--sky` |
| Almanya | `photo-1663493955721-110e7e1ae36c.avif` | 3000×1688 | `--sky` |

**Hangi kesim yöntemi?** İki tane var ve seçim görsele bağlı:

- `--sky` — gökyüzünü **kenardan yayılarak** siler. Gökyüzü tek parça ve görüntü
  kenarlarına değiyor; bayrağın içi ona bağlı değil. Temiz gökyüzü fonlu görsellerde
  bunu kullan. rembg bu görsellerde bayrağın **beyaz şeritlerini ve yıldızlarını**
  gökyüzü sanıp içeride delik açıyordu.
- `--vision` — Apple Vision özne maskesi (`tools/_bin/kesici`). İngiltere için
  eklendi: Union Jack'in beyazı bayrağın en büyük yüzeyi, `--sky` soluk gökyüzünden
  o beyaz bantlara sızıp bayrağı delik deşik ediyor. Vision bayrağı direğiyle
  birlikte tek parça çıkarıyor, ek bağımlılık istemiyor.
- (varsayılan) **rembg** — bulanık şehir/bina fonlu görsellerde. Gökyüzü silme orada
  düz bir bölge bulamıyor. Ayrıca koyu bantlı bayraklarda (siyah-kırmızı-altın) düşük
  çözünürlüklü kaynakta gökyüzü silme siyah bandı yutabiliyor; öyle bir durumda rembg'ye
  geç.

Kesim sonrası `tools/clean_flag_alpha.py` alfa kanalındaki kopuk küçük adaları siler —
kapakta bayrağın altında serbest gezen gri lekeler olarak görünüyorlardı.

`tools/place_flag_photo.py` gökyüzünü rembg ile siler ve bayrağı kapak köşesine
AUSCAMP orijinaliyle aynı kurguda oturtur:

```sh
~/auscamp-specialist-katalog/.venv/bin/python tools/place_flag_photo.py \
    kaynak.jpg deu --crop 850,150,2400,1400 --flip --rot 12 --bright 1.06
```

Yerleşim mantığı — AUSCAMP kapağındaki kurgu birebir taklit ediliyor:

- Bayrak **genişliği doldurur** (kutuya sığdırılmaz), hoist sayfa kenarına yaslanır ve
  soldan hafifçe taşar; direk kadrajın büyük ölçüde dışında kalır.
- Başlık pill'i sayfada x=116.3pt / y=140.7pt'de başlıyor. Bayrak o noktanın **sağında**
  aşağı sarkarsa başlığın üstüne biniyor; `overlaps_pill()` bunu ölçüp sığana kadar
  otomatik küçültüyor. Sol tarafta sarkması sorun değil — orijinalde de öyle.
- Dik sarkan bayraklar (İngiltere, Almanya) `--rot` ile hafifçe yatırılıyor; yoksa
  otomatik küçültme devreye girip onları diğerlerinden ufak bırakıyor.

Seçenekler: `--crop` (yan bina / ikinci bayrak / uzun direk), `--flip` (direği sola al),
`--rot` (yatır), `--bright` / `--sat` (dört fotoğrafın pozlamasını eşitle),
`--zoom` (otomatik küçültmenin başlangıç değeri).

Kullanılan ayarlar:

| Ülke | Komut ekleri |
|---|---|
| Avustralya | `--bright 1.30 --sat 1.15` |
| İngiltere | `--vision` (kaynak zaten yatay dalgalanıyor, döndürme gerekmiyor) |
| ABD | (yok) |
| Almanya | `--crop 850,150,2400,1400 --flip --rot 12 --bright 1.06` |

`tools/make_flags.py` (SVG'den sentetik dalgalı bayrak üretici) artık kullanılmıyor;
gerçek fotoğrafların yanında yapay duruyordu. Dosya, kaynak fotoğraf bulunamayan bir
ülke çıkarsa yedek olarak duruyor.

## Sayfalama notları

- Kullanılabilir içerik yüksekliği 719.25pt; her `H1()` yeni sayfa açar.
- **Ölçüm eşiği sayfa yüksekliğine göre alınır.** AUSCAMP'te sabit `y>760`
  artefakt sayılıyordu; ölçüm sayfası 2400pt olduğu için bu, 694pt'den uzun her
  bölümü sessizce kırpıyordu. DENTCAMP'te SSS ve kavram listeleri o eşiği aştığı
  için eşik `sayfa yüksekliği − 82pt` olarak hesaplanıyor.
- Sayfadan **az** taşan uzun listeler (`sq1`, `sq2` kademeleri) satır aralığı ve
  madde boşluğu kısılarak sığdırılır; yetmezse bölüm iki sayfaya bölünür ve
  paketleme bunu sayfa sayısına katar.
- Chrome, büyük puntolu İ/Ş aksanlarını sayfa sonlarında önceki sayfaya sızdırıyor;
  alt band (y>786) metin katmanından redaction ile siliniyor, dekor/logo sonra
  basılıyor.
- Road map yolu SVG olarak üretilir (AUSCAMP'te 5 adıma sabit bir bitmap'ti).
  İngiltere ve ABD 6 adımlı; daire konumları ve yol adım sayısına göre yeniden
  dağıtılır.

## ABD kataloğu — üç yol

ABD'de tek bir rota yok; katalog üç yolu birlikte anlatır ve ortak dört adımı
(DENTPIN → ECE/WES → TOEFL → INBDE) öne alır:

| Yol | Ne | Kritik nokta |
|---|---|---|
| 1. Advanced Standing (CAAPID) | CODA fakültesinde 2–3 yıl, ABD diploması | Her eyalette geçerli; öğrenim ücreti en büyük kalem |
| 2. Uzmanlık rezidanslığı (ADEA PASS) | Mevcut diplomayla uzmanlık programı | Genellikle maaşlı; ama çoğu eyalette genel lisans vermez (Texas istisna) |
| 3. AEGD / GPR | 1–2 yıllık genel rezidanslık | En kısa/ucuz görünen ama en riskli; ~16 eyalet kabul eder, Texas ve New York kapalı |

Road map bu yapıyı yansıtır: dört ortak adım, sonra yol seçimi, sonra eyalet lisansı.
Kaynak belgeler "danışman rehberi" olarak yazılmıştı; katalog danışana gittiği için
metin danışan diline çevrildi.

## Denetim

İki katman:

```sh
python3 qa_check.py            # mekanik: ölçülebilen her şey
python3 qa_check.py --json     # makine okunur
```

Gözle bakılması gerekenler (estetik, satış dili, kaynak uygunluğu) için **denetçi agent**
var: `~/.claude/agents/dentcamp-katalog-denetci.md`. "katalogları denetle" dendiğinde
çağrılır; tasarım, marka tutarlılığı, kaynak belgeye uygunluk ve **satış etkinliğini**
denetleyip kanıtlı bulgu listesi verir. Düzeltmeyi yapmaz, raporlar.

`qa_check.py` kategorileri: `TAŞMA`, `YER TUTUCU`, `İLETİŞİM` bloklayıcı; `ÇÖZÜNÜRLÜK`
baskıda bloklayıcı; `BOŞ SAYFA`, `RENK`, `SATIŞ` uyarı (bazıları kasıtlı olabilir, gözle
teyit gerekir). Road map sayfası bilerek geniş yerleşim kullandığı için taşma denetiminden
muaftır.

## Blok tipleri

`content/<ulke>.py` içinde kullanılabilecek bloklar:

| Blok | Ne yapar |
|---|---|
| `H1(t, sub)` | Bölüm başlığı — **yeni sayfa açar** |
| `BAR(t)` | Koyu turkuaz pill alt başlık |
| `P` / `SUB` / `UL` / `DL` | Paragraf, ara başlık, madde, terim listesi |
| `BOX(t)` | Açık turkuaz vurgu kutusu |
| `STATS([(değer, etiket), …])` | Rakam kartları — 2–4 kart yan yana |
| `CTA(satır)` | Koyu turkuaz çağrı şeridi + telefon + site |

**Yeni blok eklerken iki kural:** (1) HTML'i iç içe `<div>` içermemeli — `build_optimal`
blok ayrıştırıcısı `.*?</div>` ile eşleşiyor ve non-greedy olduğu için ilk kapanışta
duruyor, iç içe div kullanılırsa blok ikiye bölünüp akıştan sessizce düşüyor; içeride
yalnız `<span>` olmalı. (2) `TOKEN` regex'ine yeni sınıfı eklemeyi unutma, yoksa blok
hiç render edilmez.

`STATS` sayfa altındaki boşluğu doldurmak için değil, **metnin içinde kaybolan kritik
sayıyı öne çıkarmak** için var (sınav süresi, ücret, geçme oranı). Boşluk dolsun diye
alakasız yere konursa sayfa şişer ve bölümü bir sonraki sayfaya itebilir — Avustralya'da
bir kez oldu, ikinci kart kaldırıldı.

## Road map — tek ya da çok

Ülke dosyası `ROADMAP_TITLE` / `ROADMAP_SUB` / `ROADMAP` tanımlarsa tek sayfa basılır.
`ROADMAPS = [(başlık, alt başlık, adımlar), …]` tanımlarsa her biri kendi sayfasına
gider ve **iletişim bloğu yalnız sonuncuya** konur.

ABD üç yol anlattığı için üç road map kullanıyor. İlk üç adım (`_ORTAK`) üçünde de
aynı; ayrım 4. adımda başlıyor — okuyucu ortak gövdeyi ve nerede ayrıldığını yan yana
görüyor. Tek birleşik şema hem kalabalık hem yanıltıcı oluyordu.

## Satış şeridi (CTA)

Denetim, iletişimin yalnız son sayfada olduğunu gösterdi — okuyucu kataloğun ortasında karar
verdiğinde geri dönmek zorunda kalıyordu. `CTA()` bloğu, hizmetler anlatıldıktan hemen sonra
koyu turkuaz bir şerit basar (`content/_common.py` → `whatsapp_and_mentorship` sonu), dört
katalogda birden görünür.

**Dikkat:** CTA'nın HTML'i iç içe `<div>` içermemeli. `build_optimal.py`'deki blok
ayrıştırıcı `<div class="ctaband">.*?</div>` ile eşleşiyor ve non-greedy olduğu için ilk
kapanışta duruyor; iç içe div kullanılırsa şerit ikiye bölünüp akıştan sessizce düşüyor.
Bu yüzden içeride yalnız `<span>` var.

## Denetim sonrası düzeltmeler (Ağustos 2026)

Denetçi agent 24 bulgu çıkardı; 20'si kapatıldı. Kayda değer olanlar:

- **Türkçe ek uyumu** — `_common.py` ekleri sabit yazılmıştı ("ABD'daki", "İngiltere'ya").
  `loc()` / `locd()` / `dat()` yardımcılarıyla ülke başına doğru ek üretiliyor.
- **Hizmet numaralandırması** — `medcamp()` numarasızdı, AUS ve UK'de 1 → boş → 3 akıyordu.
  Artık `num` parametresi var.
- **sq3 sıkıştırma kademesi** — SSS bölümleri büyüyünce %11'in üstüne taştı; sıkıştırma
  penceresi %10'du ve devreye girmiyordu. Pencere %16'ya çıkarıldı, üçüncü kademe eklendi.
- **UK/ABD SSS ikiye ayrıldı** — 969 ve 942pt; ara başlıkla bölünüyor. Bölünme birebir
  dengeli DEĞİL (ölçüm izole `<ul>` parçalarına bakıyor, her parça kendi kenar boşluğunu
  da taşıyor); SSS'nin ilk sayfası dört katalogda da yarım kalıyor.
- **6. road map ikonu** — havuz 5 ikondu, 6 adımlı ABD ve UK'de tekrar oluyordu.
  `tools/make_icon_seal.py` onay mührü ikonunu aynı dilde üretiyor. Havuz 10 ikona
  çıktıktan sonra da atamada tekrar kalmıştı (İngiltere road map'inde `ic_sinav` üç
  kez, ABD'de `ic_mentor` üçer kez); 21 Ağustos 2026'da her road map'te ikonlar
  benzersiz olacak şekilde yeniden atandı. Yeni adım eklenirken kontrol edilmeli.
- **Bayrak kesim artıkları** — `tools/clean_flag_alpha.py` alfa kanalındaki kopuk küçük
  adaları siliyor (UK'de 7, ABD'de 8 tane vardı).
- **Tek CTA, son sayfada** — kullanıcının kararı: bu broşür ilk görüşmeden SONRA gönderiliyor,
  gövdede CTA verilmez, ara sayfalar süreci anlatır. `CTA()` yardımcısı bu yüzden hiçbir
  ülke dosyasında çağrılmıyor; duruyor ama kullanılmıyor. (README eskiden "üç CTA noktası"
  diyordu, öyle bir şey yoktu.) Kapanışa 21 Ağustos 2026'da `.cnext` satırı eklendi:
  okuyucuya bir sonraki adımı söyleyen tek cümle. Öncesinde kapanış yalnızca telefon,
  site ve Instagram veriyordu.
- **Başlık artık tek başına sayfada kalmıyor** — `_bol()` "başlık yalnız kalmasın" kuralı
  blok SAYISINA bakıyordu (j>=2) ve H1 + alt başlık + tek giriş cümlesi bu kuralı
  geçiyordu; İngiltere'de KAVRAMLAR & TERİMLER başlığı sayfanın alt üçte birinde açılıp
  terim listesinin tamamı sonraki sayfaya geçiyordu. Kural `MIN_HEAD_BLOK` ile başlık
  olmayan blok sayısına bağlandı. Salt yükseklik eşiği (200pt) denendi ve geri alındı:
  gap dolduran meşru bölmeleri de engelliyordu.
- **Silüet dolgusu katalog başına en fazla iki sayfa** — dolgu boşluğu kapatmıyor, boşluğu
  işaretliyor: ABD'de aynı gökdelen vinyeti beş sayfada, İngiltere'de aynı Big Ben iki
  sayfada çıkıyordu. En büyük iki boşlukla sınırlandırıldı.
- **`_bolunmez` sınıf niteliğiydi** — dört ülke aynı süreçte derlendiği için set
  paylaşılıyor, üstelik `id()` çöpe giden dict'lerden geri dönüştürülüyordu; bir ülkede
  bölünemez işaretlenen bir id başka ülkede sağlam bir grubu susturabiliyordu. Artık
  Builder örneğine ait.
- **Madde seviyesinde bölme üçüncü kez denendi ve geri alındı** — SSS'nin ilk sayfası dört
  katalogda da yarım kalıyor; daraltılmış hâli (yalnız `terms` listeleri, iki yanda en az
  N madde) İngiltere s.10'u %88'den %95'e çıkardı ama ABD s.14'ü %38'e düşürdü. Net etki
  eksi. `_parcala` / `_birlestir` bu yüzden duruyor ama çağrılmıyor.
- **MAX_EXTRA denemesi geri alındı** — 48 → 95 yapılınca ölçüm ile gerçek yerleşim arasındaki
  sapma birikti ve dört katalog da birer sayfa uzadı. 48'de kalmalı.

Kalan mekanik bulgu: kapak bayrağı ~150 dpi (kaynak görsellerin çözünürlüğü).

Kapak tag'ine "PATHWAY" eklenemiyor: `.cv-logoline` 430pt, logo 151,9pt yer alıyor,
tag'e 267pt kalıyor. "| GDC REGISTRATION PATHWAY" 22pt Open Sans ExtraBold'da 352pt,
"| APPROBATION PATHWAY" 299pt, "| US LICENSURE PATHWAY" 293pt. Üçü de taşıyor, o yüzden
kapaklar kısa hâlde (APPROBATION / ADC PATHWAY / GDC REGISTRATION / US LICENSURE); tam
adlar bölüm başlıklarında ve road map'te geçiyor.

21 Ağustos 2026 (12 kişilik mentör kadrosu) sonrası sayfa dolulukları, 8 Ağustos
sürümüyle karşılaştırmalı: Avustralya 9 -> 9, Almanya 11 -> 11 (ikisinde de mentör
sayfası eklendi ve eskiden %50 dolan "A'DAN Z'YE MENTÖRLÜK DESTEĞİ" sayfası kapandı),
ABD 16 -> 17, İngiltere 10 -> 11. İngiltere'de "A'DAN Z'YE MENTÖRLÜK DESTEĞİ" sayfası
%50'de kaldı; `MENTOR_YERI=1` denendi ve daha kötüsünü verdiği için geri alındı.
SSS'nin ilk sayfası dört katalogda da eskiden beri yarım kalıyor.

## Mentör sayfası

Kadro dört katalogda da **aynı 12 kişi**; değişen tek şey sıra. `content/_common.py`:

- `MENTORLER` — 12 kayıt. Her kayıtta `foto`, `ulke` (`deu/usa/uk/aus`, koordinatörde
  `None`), `ad`, `alt` (iki künye satırı). Şehirler mentörlerin kendi biyografilerinden
  alındı, uydurulmadı.
- `mentor_sirasi(country)` — broşürün ülkesinin mentörleri başa, kalanlar
  `MENTOR_SIRA` sırasıyla arkaya, ülkesi olmayan kayıt (mentör koordinatörü) en sona.
  12 kart = tam 3 satır × 4 kolon, hangi broşür olursa olsun boş hücre kalmıyor.
- `mentorler(country)` — bölüm `H1` ile açılıyor, yani **kendi sayfasında**. Eskiden
  `BAR` ile sayfa 2'nin altındaydı ve üç kişiyle grid'in dördüncü hücresi boş kalıyordu.
- `MENTORLER_BOLUM` + `MENTOR_YERI` (ülke dosyalarında) — bölüm 610pt, yani hiçbir
  bölümle sayfa paylaşamıyor. Girişin (185pt) hemen ardına konunca sayfa 2'nin dörtte
  üçü boşa gidiyordu; `Catalog.body_pages()` bu yüzden kadroyu `MENTOR_YERI`'nin
  gösterdiği BODY bölümünden SONRA yerleştiriyor. Dört katalogda da 0.
  **Bu sayı ülkeye göre ölçülerek seçildi:** kadro sayfa paylaşamadığı için
  kendisinden önceki bölümün sayfa sonunda kuyruk bırakmaması gerekiyor. Bir ülkede
  sayfa sayısı beklenmedik şekilde artarsa ilk bakılacak yer burası.
  **2 Eylül 2026:** ABD'de YERI 1 idi; dil yeterliliği hizmet bölümü çıkınca sayfa
  akışı değişti ve yeniden ölçüldü — 0 -> 16 sayfa ve zayıf sayfa YOK, 1 -> 17 sayfa
  ve s.11 %32, 2 -> 17 sayfa ve s.4 %24, 11 -> 17 sayfa ve s.11 %32. YERI=0 yapıldı,
  böylece kadro sayfasının ORTAK İLK ADIMLAR'ı ortasından kesmesi ödüncü de kalktı.
  (Eski ölçüm, bölüm hâlâ dururkendi: İngiltere 1 -> s.3 %22; ABD 0 -> 18 sayfa ve
  s.3 %15, ABD 2 -> 18 sayfa ve s.4 %26.)
- `build_optimal.BOLUNMEZ_ISARET` — mentör grid'i `_bol()` tarafından bölünemez.
  Guard olmadan sayfalayıcı bölümü paragraf sınırından ikiye ayırıp başlık ile metni
  bir sayfada, 12 daireyi sonraki sayfada bırakıyordu; üstelik o sayfanın bölüm adı
  bir sonraki başlıktan geliyordu.

Kart tasarımı (**21 Ağustos 2026, ikinci tur**): mentörün arka planı silinmiş ve kendi
ülkesinin bayrağının önüne oturtulmuş. Kart 104×130pt (4:5), köşe yarıçapı 9pt, dışında
hairline. Ülkesi olmayan kayıt (mentör koordinatörü) bayrak yerine koyu turkuaz zemin alır.

Önce yuvarlak portre + bayraklı halka yapıldı ve BIRAKILDI: halka yarıçapın yalnız dış
%19'u olduğu için bayraklar küçük kalıyordu (kullanıcı: "bayraklar olmamış"). Halkanın kendisi
teknik olarak çalışıyordu, sorun ölçekti.

Varlıklar:

- `tools/kesici.swift` → `tools/_bin/kesici` (derleme: `swiftc -O tools/kesici.swift -o
  tools/_bin/kesici`). macOS Vision'ın `VNGenerateForegroundInstanceMaskRequest`
  maskesiyle arka planı siler. rembg denenmedi çünkü ek bağımlılık ve ~170 MB model
  indirmesi istiyor; Vision makinede hazır ve saç kenarlarında belirgin biçimde temiz.
  macOS 14+ gerekir.
- `tools/prep_mentor_kesim.py` — kaynak → `exif_transpose` → kesici → yüz kutusundan 4:5
  çerçeveleme → beyaz kontur → bayrağa bindirme → `assets/img/kart_<ad>.jpg` (448×560,
  ~310 dpi, 36–58 KB).
  · **Kadraj yüz kutusundan hesaplanıyor** (`prep_mentors.py` içindeki `KADRO` tablosu,
    tek tek ölçüldü): baş kart yüksekliğinin %25,5'i, göz hattı %21,5'te. Böylece 12
    kartta baş ölçeği aynı. Alfa sınırından çerçeveleme denendi ve bırakıldı: kolların
    açık ya da kavuşmuş olması kişi genişliğini çok değiştiriyor.
  · **Beyaz kontur 1,6pt, PNG'ye değil JPEG'e gömülü.** CSS keyfi alfa biçiminin
    çevresine kontur çizemiyor. Kontur olmadan koyu saçlar Almanya bayrağının siyah
    bandına karışıyor, başın sınırı kayboluyor.
  · **Bindirme neden Python'da:** kesimler alfa kanallı PNG olarak bırakıldığında
    (12 dosya, ~400 KB) dört PDF 8,6–9,5 MB'a çıkıyordu. Bayrak zemini zaten opak,
    tek JPEG olarak gidince PDF'ler 2,2–3,0 MB'a döndü.
  · `OZEL` sözlüğü: kadrajı farklı olması gereken kayıtlar. **Gizem Subaşı** — iki
    karesi de kesim kartına uymuyor (biri gövdesiz yakın plan selfie, diğerinde yüz
    ~90 px). Kullanıcının kararı: yakın planı kullan, kartı farklı dursun. Sonuç: kartı
    tamamen yüzüyle doluyor, bayrak yalnız kenarda ince bir şerit olarak görünüyor.
    Bel hizasına kadar bir kare gelirse `OZEL`den satırı silmek yeterli.
- `tools/make_flag_discs.py` → `assets/img/fkart_<key>.png` (448×560). 2:1 bayraktan
  yalnız %40 genişlik alındığı için kırpım konumu ülkeye göre ayarlı: `usa` 0.0 (canton
  kadrajda kalsın), `aus` **0.5**, `deu`/`uk` 0.5. **Avustralya'da sola dayalı kırpım
  denendi ve bırakıldı:** kartta yalnız Union Jack parçaları kalıyor ve İngiltere
  kartından ayırt edilemiyor; ortadan kırpımda solda Union Jack, sağda Commonwealth
  Yıldızı ve Güney Çaprazı görünüyor. Kare kırpımı 4:5'e ölçeklemek bayrağı dikeyde
  %25 gerdiği için ayrı varlık üretiliyor.
- Emekli olan daire tasarımının varlıkları (`m_*.jpg`, `fdisc_*.png`) silindi; üreten
  kod (`prep_mentors.py`, `make_flag_discs.py` içindeki `KIRPIM`) duruyor, gerekirse
  yeniden üretir. `prep_mentors.py` ayrıca yüz kutusu tablosunun tek kaynağı.

Yerleşim: `.mgrid` 4 kolon `minmax(0,1fr)`, `row-gap:16pt`, `margin-top:18pt`; isim pill'i
karttan 8pt aşağıda. `.mname` 8pt: 8,4pt'de en uzun iki isim komşu kolona 4,8pt kalıyordu.
**İsim kalıbı** kurallı: unvan sonda ise (DDS/BDS) başta "Dt." yazılmaz.

## Açık kalemler

1. **Mentörler** — KAPANDI (21 Ağustos 2026). Kadro 12 kişi ve dört broşürde de tamamı
   basılıyor; ayrıntı aşağıdaki "Mentör sayfası" bölümünde. Kalan iki küçük eksik:
   Gizem Subaşı ve Damla Engin Arpacı'nın biyografisinde şehir geçmediği için künyede
   yalnız ülke yazıyor.
2. **Almanya yasa tarihi** — iki kaynak çelişiyor: broşür taslağı 1 Kasım 2026,
   yol haritası 1 Temmuz 2026 diyor. Katalogda broşür taslağının tarihi kullanıldı.
3. **Dil eğitimi kapsamı — 2 Eylül 2026 (kullanıcı): DENTCAMP İNGİLTERE VE ABD SÜRECİNDE
   DİL DESTEĞİ SAĞLAMIYOR.** Dil ŞARTI değişmedi: mevzuat bölümlerindeki
   "1. İNGİLİZCE YETERLİLİĞİ (IELTS / OET)" (uk) ve "3. İNGİLİZCE YETERLİLİĞİ (TOEFL)"
   (usa) aynen duruyor, karşılaştırma tablosundaki dil satırları da. Kalkan yalnız
   HİZMETLERİMİZ altındaki dil EĞİTİMİ bloğu; iki katalogda da hizmet numaraları
   yeniden dizildi (3/4/5 -> 2/3/4). Dil eğitimi yalnız **Avustralya (MEDCAMP)** ve
   **Almanya (MEDCAMP DEUTSCH)** paketlerinde var; MEDCAMP adı da yalnız `aus.py`'de
   basılıyor. `_common.medcamp()` -> `dil_yeterliligi(exam, num, marka)`; `marka=None`
   dalı ara adımdan kaldı, şu an kimse kullanmıyor. Toplu katalogda bölüm
   "2. DİL EĞİTİMİ (AVUSTRALYA VE ALMANYA PAKETLERİNDE)" oldu ve İngiltere/ABD'de
   eğitimin yer almadığı açıkça yazıyor.
   Sayfa etkisi: İngiltere 11 -> 10, ABD 17 -> 16 (MENTOR_YERI=0 ile birlikte).
   Aşağıdaki eski not kaydı tutuluyor: AUS ve UK'de OET üzerinden tam bölüm var. ABD'de TOEFL isteniyor;
   MEDCAMP "medikal İngilizce altyapısı" olarak konumlandı. Denetçi, OET bloğundan
   kopyalanan doğrulanmamış vaatleri (Zoom sıklığı, "80+ kayıtlı ders", eğitmen
   sertifikasyonu) yakaladı — ABD bölümünden çıkarıldı. TOEFL tarafında bunlar fiilen
   varsa geri eklenebilir. Almanya'da dil Almanca olduğu için MEDCAMP yerine
   **MEDCAMP DEUTSCH** var (ÖSD sınav merkezi akreditasyonu — kullanıcı teyit etti).
   **2 Eylül 2026:** bu hizmetin adı ALMANGO iken MEDCAMP DEUTSCH oldu (kullanıcı).
   Basılan her yerde ad değişti; `content/_common.py` içindeki fonksiyon da
   `almango()` -> `medcamp_deutsch()`. Almanya ve toplu katalog yeniden derlendi,
   diğer üçünde bu ad hiç geçmiyordu.

## Kapak fotoğrafları

Dördü de ülkeye özel: aynı hekim çifti, aynı kadraj, pencerede o ülkenin sembol yapısı
(Opera House & Harbour Bridge · Big Ben & Westminster · Empire State & Chrysler ·
Brandenburg & Fernsehturm). Promptlar `assets/kapak_kaynak/PROMPTLAR.md` içinde.

Yenilemek için: üretilen görseli `assets/kapak_kaynak/<ulke>.jpg` olarak bırak, sonra

```sh
python3 tools/clean_watermark.py ~/Downloads/<dosya>.png assets/kapak_kaynak/<ulke>.jpg
python3 tools/prep_covers.py && python3 build_optimal.py
```

`clean_watermark.py`, Gemini'nin sağ alt köşeye bastığı parıltı rozetini siler: rozeti
sabit oranlı dar bir pencerede yerel medyan farkıyla bulur, çevredeki **en düz komşu
alandan klonlayarak** doldurur (difüzyonla doldurmak komşu ten rengini içeri çekip leke
bırakıyordu), sonra kenara denk gelip kırpılan uçlar için bir despeckle geçişi yapar.

## Kaynaklar

| Ne | Nereden |
|---|---|
| Tasarım geometrisi | `~/auscamp-specialist-katalog` (AUSCAMP Specialist Pathway) |
| Metin (AUS/UK/DEU + ABD 1. yol) | `~/Downloads/BROŞÜR/BROŞÜR VE TANITIM/<ulke>/*.docx` |
| ABD 2. yol (uzmanlık) | `~/Downloads/Yol2_Uzmanlik_ADEA_PASS.docx` |
| ABD 3. yol (AEGD/GPR) | `~/Downloads/Yol3_AEGD_GPR.docx` |
| Logo | `~/Downloads/DENTCAMP/dentcamp.png` |
| İkonlar, fontlar | AUSCAMP kataloğundan (ikonlar turkuaza boyandı) |
| Kapak fotoğrafları | Gemini üretimi (kullanıcı) → `assets/kapak_kaynak/<ulke>.jpg` |

## Fontlar

AUSCAMP'ten aynen devralındı: League Spartan Bold (kapak), Open Sans ExtraBold
(H1/pill), Arimo Bold (mentör), Archivo (gövde 12.4pt). Dördü de açık lisanslı.
Çıktıda Type0 subset olarak gömülü, matbaaya uygun.


## Toplu katalog (10 sayfa)

Dört ülkeyi tek belgede anlatan özet. **Görüşme sonrası** gönderilir: ülke
kataloglarıyla aynı politika, gövdede satış şeridi yok, tek iletişim kapanışta.

```
1  Kapak (bayraksız, dört şehir tek kare)  6  İngiltere — GDC Registration
2  DENTCAMP nedir + kimler başvuruyor  7  ABD — US Licensure (üç rota)
3  Dört ülke karşılaştırma tablosu     8  Mentör kadrosu (12 kart)
4  Almanya — Approbation               9  Hizmetlerimiz (dört ülkede ortak)
5  Avustralya — ADC Pathway           10  Kapanış / iletişim
```

**Olgu kaynağı ülke katalogları.** `content/toplu.py` içindeki her rakam ve her
sınav adı `deu.py` / `aus.py` / `uk.py` / `usa.py` içinde de geçiyor; toplu
katalog için yeniden araştırma yapılmadı. Ülke dosyalarındaki bir rakam
değişirse toplu kataloğun da elden geçmesi gerekir, otomatik senkron YOK.

### Sayfa başına tam bir bölüm

10 sayfa ölçümle tutturuluyor, sabitlenmiş değil. `pack()` bir H1'i ancak
sayfada `H1_ROOM` (235pt) kalmadıysa yeni sayfaya atıyor; `split_pass` ise
`SPLIT_MIN` (115pt) üstündeki boşluğu sonraki bölümü bölerek dolduruyor. Yani
her bölümün **en az ~605pt** olması gerekiyor, yoksa iki ülke aynı sayfaya
düşüyor.

İlk sürümde ülke bölümleri 400–445pt idi ve sonuç 9 sayfa oldu: Avustralya
ikiye bölündü, İngiltere onun kuyruğuyla aynı sayfaya girdi, ABD tek başına
%58'de kaldı. Bölümlere kavram sözlüğü (`DL`) ve birer madde eklenerek hepsi
563–622pt'ye çıkarıldı; ölçülen değerler:

| Bölüm | Yükseklik | Sayfada kalan |
|---|---|---|
| DENTCAMP NEDİR? (3 grup) | 635pt | 84pt |
| DÖRT ÜLKE, DÖRT YOL | 609pt | 110pt |
| ALMANYA | 626pt | 93pt |
| AVUSTRALYA | 613pt | 107pt |
| İNGİLTERE | 628pt | 91pt |
| ABD | 613pt | 107pt |
| MENTÖRLERİMİZ | 697pt | 22pt |
| HİZMETLERİMİZ (7 grup) | 693pt | 27pt |

Sekizinin de kalanı 115pt'nin altında, yani bölme hiç devreye girmiyor ve
10 sayfa yapısal olarak garanti. **Bir bölüm kısaltılacaksa 605pt'nin altına
inmemeli.**

Ara bir sürümde DÖRT ÜLKE bölümü 545pt'ye düşmüştü (tablo kolonları
dengelenince satırlar daraldı) ve 174pt kalıyordu; katalog yine 10 sayfa
çıktı ama bu tesadüftü: `_bol()` Almanya'yı bölmeye çalışıp `MIN_HEAD_BLOK`
kuralına takıldığı için vazgeçmişti. Bölüme iki madde eklenip 609pt'ye
çıkarıldı, güvence tesadüfe değil ölçüye bağlandı. Ölçüm:

```sh
python3 -c "
import build_optimal as BO, re
b = BO.Builder('toplu')
parts = [p.split('<div class=\"content\">',1)[1].rsplit('</div></section>',1)[0]
         for p in b.cat.body_pages()]
g = BO.group_blocks(''.join(parts)); hs = b.measure(g)
[print(f'{h:7.1f}pt', re.sub('<[^>]+>',' ',x['html'])[:44].strip()) for x,h in zip(g,hs)]"
```

### İki yeni blok

| Blok | Ne yapar |
|---|---|
| `KARSI(başlıklar, satırlar)` | 5 kolonlu karşılaştırma tablosu (68/104/132/122/72pt) |
| `MINIMAP(adımlar)` | Sayfa içi yatay yol şeridi: numaralı daire + kesikli hat, 4–6 adım |

İkisi de yalnız `<span>` içeriyor (blok ayrıştırıcı kuralı) ve `TOKEN`
regex'ine eklendi. `MINIMAP`, tam sayfa road map'in yerini tutuyor: dört ülkeye
dört tam sayfa şema verilseydi katalog 14 sayfa olurdu.

Kolon genişlikleri hücre içeriğine göre ölçüldü. "Belirleyici şart" sütununa
ilk denemede 76pt verilmişti; metin dört satıra sarıp Avustralya satırını iki
katına çıkarıyordu.

### Kapak

Kapakta **bayrak yok**, yalnız dört ülkenin **tek kadrajda birleştiği fotoğraf**.

**2 Eylül 2026 (kullanıcı): kapağın üstündeki dört bayraklı şerit kaldırıldı.** Kapak
fotoğrafı dört bayrağı kendi içinde taşıyor, şeritle birlikte bayraklar kapakta
iki kez geçiyordu (üstelik sıraları da farklıydı). `COVER["flags"]=False`
denendiğinde şeridin yerine ülke kalıbındaki tek büyük dalgalı bayrak geliyordu;
bu yüzden `build.py`'a `COVER["bayrak"]=False` eklendi: kapak `<img>`'i hiç
basılmıyor. Şerit üreticisi `tools/make_flags_toplu.py` ve `bayrak_toplu.png`
duruyor, artık kullanılmıyor.

Bayrak kalkınca üstte ~140pt ölü bant kaldığı için kapak bloğu yukarı çekildi ve
fotoğraf büyütüldü. `build.py` kapak `<section>`'ına katalog anahtarını sınıf olarak
basıyor (`cover-toplu`), ölçüler yalnız o sınıfta eziliyor; ülke kataloglarının
kapağı değişmedi. Yeni değerler: pill 92pt, başlık 162pt, logo satırı 254pt, alt
başlık 292pt, aksan 364pt, fotoğraf 386pt'de başlayıp **452x339pt**. Bu ölçü
kaynağın oranı (1448x1086 = 1,3333) olduğu için kare **hiç kırpılmıyor**, dört simge
de tam görünüyor; `make_cover_toplu_foto.py` içindeki `UST` payı 0'a indi. Fotoğrafın
alt sınırı 725pt, künye bandı 795pt'de başlıyor.

**2 Eylül 2026:** kart fotoğrafı kullanıcının verdiği görselle değişti
(`assets/img/kapak_toplu_src.png`, 1448×1086 px). Özgürlük Anıtı, Westminster,
Brandenburg Kapısı ve Opera Binası aynı kadrajda; sağ altta ünitede çalışan
hekim. Dört panelli eski kart (`make_cover_toplu.py`, `kapak_toplu.jpg`) yerinde
duruyor ama `theme.py` artık `kapak_toplu_foto.jpg`'yi gösteriyor.

- `tools/make_cover_toplu_foto.py` — kaynağı kart oranına (452/252 = 1,794)
  yalnız DİKEYDE kırpar. `UST=90` px: bayrakların tamamı, meşale ve alttaki
  hekim–hasta kadrajda kalır. `UST=0` hastanın koltuğunu, `UST=140` meşaleyi
  kesiyordu (dört değer render edilip karşılaştırıldı). Çıktı 1448×807 px =
  kartta ~231 dpi, `qa_check.MIN_DPI` (200) üstünde ama eski dört panelli
  karttan (300 dpi) düşük; kaynak daha büyüğü vermiyor.
- Fotoğraf dört bayrağı KENDİ İÇİNDE taşıyor, üstteki şerit de dört bayrak
  gösteriyor: kapakta bayraklar iki kez geçiyor ve sıraları farklı (şerit
  Almanya·Avustralya·İngiltere·ABD, fotoğraf ABD·İngiltere·Almanya·Avustralya).
  `COVER["flags"]=False` denendi: şerit kalkınca yerine ülke kalıbındaki tek
  büyük dalgalı bayrak (`bayrak_toplu.png`) geliyor ve kapağın sol üstünü
  kaplıyor, daha kötü. Şerit bu yüzden korundu.

- `tools/make_flags_toplu.py` — `bayrak_*.png` dosyalarını bbox'undan kırpıp
  560px genişliğe ölçekler, 58px bindirmeyle yan yana dizer, tuvali kırpar.
  Çıktı 2066×621px = 516,5×155,25pt; **CSS'teki `.cv-flags` ölçüsü bu olmalı,**
  tuval kırpıldığı için verilen kutu bayrakları birebir ölçekler.
- `tools/make_cover_toplu.py` — (ARTIK KULLANILMIYOR) dört kapak fotoğrafını
  dikey panele böler.
  **Ortadan kırpım DENENDİ VE BIRAKILDI:** dört fotoğraf da aynı kliniği, aynı
  üniteyi ve aynı iki hekimi gösteriyor, ortadan kırpınca kart tek fotoğrafın
  dört kopyası gibi duruyordu. Ülkeyi ayırt ettiren tek şey camdaki manzara ve
  o kadrajın solunda: `ODAK` sözlüğü her paneli kendi manzarasına (Brandenburg
  Kapısı, Opera Binası, Westminster, Empire State) oturtuyor. `ZOOM=1.3` ve
  `DIKEY=0.34` alt üçteki zemin bandını kadraj dışında bırakıyor.

Kapak tag'i `| 4 ÜLKE`; `.cv-logoline` sınırı (logo sonrası 267pt) uzun ada
izin vermiyor. Künye bandı üç değil **dört** kalem taşıyor: her ülke ve hedefi.

### Kapanış sayfası

`content/toplu.py` içindeki `CLOSING` sözlüğü tanımlıysa `roadmap_pages()` tam
sayfa road map yerine `page_closing()` basar. Sayfa `rmpage` sınıfını kullanır,
böylece `.contact` bloğu ülke kataloglarıyla aynı yerde (686pt) durur.

Kartlara `min-height:122pt` verildi: yükseklik içeriğe bırakılınca üç kart
499pt'de bitiyor ve iletişim bloğuna kadar ~190pt ölü bant kalıyordu. Kart
metni 11,4pt'den gövde puntosuna (12,4pt) çıkarıldı, kartların içi de doldu.

### Ülke kataloglarına dokunulmadı

Motor değişikliklerinin hepsi ekleme: `T.ALL` sözlüğü (COUNTRIES aynen duruyor),
`Country.doc_title` (varsayılanı boş, ülkelerde eski başlık kalıbı çalışıyor),
`CLOSING` kancası (`hasattr`), iki yeni TOKEN ve yeni CSS sınıfları. Dört
katalog değişiklik sonrası yeniden derlendi: sayfa sayıları 9 / 11 / 17 / 11,
yani aynı. (2 Eylül 2026'daki dil eğitimi kararından sonra İngiltere 10, ABD 16
oldu; Avustralya 9 ve Almanya 11 aynı kaldı.)

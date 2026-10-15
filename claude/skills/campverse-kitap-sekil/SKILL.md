---
name: campverse-kitap-sekil
description: First Step AMC CAT MCQ kitabına yeni bölüm şekli üretirken kullan — kitabın dizgisiyle birebir uyumlu vektör şekil (SVG) kuralları, palet, tipografi, anatomik doğruluk kapıları ve doğrulama adımları. "şekil üret", "figür çiz", "bölüme görsel ekle" taleplerinde çağrılır.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
---

# CAMPVERSE — kitap şekli üretimi

Kitabın kendi şekilleri InDesign'da çizilmiş vektörler. Yeni bölümlerin
şekilleri onlardan ayırt edilememeli. Bu skill o standardı taşır.

## Değişmezler

1. **Vektör, raster değil.** `bookgen/svgfig.py` ile SVG üret. Raster PNG
   baskıda yumuşar ve sayfanın fontuyla dizilmez.
2. **SVG sayfaya GÖMÜLÜ konur** (`("svgfig", dict(svg=..., cap=...))`).
   Dışarıdan bağlanan SVG sayfanın `@font-face` tanımını göremez ve şeklin
   yazısı yedek fontla dizilir.
3. **Yazı ölçümü fontun kendi metrikleriyle.** `svgfig.measure()` ve
   `svgfig.wrap()` hmtx + GPOS kerning okur; Chrome ile birebir aynı sonucu
   verir. Karakter genişliği TAHMİN ETME — kutular taşar.
4. **Palet yalnız `bookgen/palette.py`.** Renkler kitabın beş cildinin
   çizimleri sayılarak çıkarıldı; yeni renk uydurma.
5. **Punto:** kutu başlığı 9.0–9.5 Cond-Bold lacivert (`P.NAVY`), gövde 9.0
   Regular (`P.INK`), etiket 7.6–8.5. Satır aralığı 10.5pt.
6. **Genişlik:** tam sütun `svgfig.COL_W` (518.7pt). Dar şekil sayfada
   ortalanır; `COL_W`yi ASLA aşma.
7. **Şekil numarası elle yazılmaz** — motor Part başına yürütür
   (`fig_start`). Kitapta Part 1 Fig 1.122'de kalmış.
8. **Altyazı biçimi:** `Fig <part>.<n>: Başlık Sözcükleri Büyük` — kitap
   başlık biçimi kullanıyor.

## Anatomik doğruluk kapısı

Önden görünüş çizerken **hastanın sağı izleyicinin solundadır.** Bu bir kez
ters çizildi ve aort odağı yanlış tarafa düştü. Her anatomik şekilde şunu
kontrol et:

- Aort odağı (2. **sağ** interkostal aralık) → şekilde **solda**
- Pulmoner odak (2. **sol** aralık) → şekilde **sağda**
- Kalp orta hattın **sağında** (hastanın solu), apeks aşağı-sağa
- Karaciğer sağda → şekilde solda; dalak solda → şekilde sağda

Şekli ürettikten sonra **görüntüyü aç ve gözle doğrula.** Metin doğru
görünüyor diye anatominin doğru olduğunu varsayma.

## Şablonlar

`bookgen/svgfig.py` içinde hazır: `flow` (akış kutuları), `panels` (başlıklı
kutular ızgarası), `compare` (iki sütun), `matrix` (satır/sütun başlıklı
ızgara). Özel çizim için `Svg` sınıfı: `rect · line · path · circle · arrow ·
text · para`.

**Uzun `path` dizesini tek bir biçim dizesiyle kurma.** Yer tutucu sayısını
tutturmak kırılgan; bir kez sessizce yanlış eğri üretti. Parçaları listeye
ekleyip birleştir (`C(*pts)` yardımcısı gibi).

## Üretim akışı

```bash
# 1. şekli yaz: chapters/figs/<bolum>_svg.py
# 2. bölümde kullan:  ("svgfig", dict(svg=FIG.name().markup(), cap="..."))
# 3. derle ve denetle
python3 -c "import sys;sys.path.insert(0,'.');from bookgen import engine,qa; ..."
# 4. GÖZLE DOĞRULA — sayfayı png'ye render edip aç
# 5. dizgi sadakatini koru
python3 bookfidelity.py 40      # ortalama sapma %0.05'in altında kalmalı
```

## Kalite kapıları

- `qa.report()` sıfır bulgu — özellikle **OLCEK**: sayfaya sığmayan tek bir
  öğe Chrome'u tüm sayfayı küçültmeye zorlar, dizgi sessizce bozulur.
- Şeklin hiçbir parçası `COL_W` dışına taşmamalı (etiketler dahil; bir kez
  sol etiketler viewBox dışında kalıp kırpıldı).
- Kutu içindeki yazı kutudan taşmamalı — kutu yüksekliğini sarmalanan satır
  sayısından hesapla, sabit verme.
- Şekil sayfada tek başına kalıp altyazısından kopmamalı.

## Harf ve kelime aralığı

Kitap metninde her harf ve kelime arası fontun kendi genişliği artı kitabın
kerning'i olmalı; başka hiçbir şey aralığa dokunmamalı.

- **`letter-spacing` kullanma.** Etiket şeritlerine konan 0.25pt aralık
  sayfada tek düze olmayan bir ritim üretiyordu.
- **PyMuPDF'in `insert_text`'i kerning UYGULAMIYOR.** Koşu başlığı son katta
  bu yolla basılıyordu ve kerningsiz kalıyordu: gövde kerningli, sayfa
  tepesindeki bölüm adı kerningsiz. "Va" çiftinde 47/1000 em fazla boşluk
  görünüyordu. `engine._kerned_text()` karakterleri tek tek, kerning eklenmiş
  konumlara basar; son katta yazı basan her yer bunu kullanmalı.
- Denetim: bütün PDF taranıp her karakter çiftinin gerçek ilerlemesi fontun
  hmtx + GPOS değeriyle karşılaştırılır. Sapma sıfır olmalı.

## Uzun tire yok

Kitap metninde **em tire (—) kullanılmaz**. Açıklama getiren tire yerine iki
nokta, ara söz yerine virgül. Bu yalnız üslup değil: em tire ProximaNova
italiğinde yok ve künye satırında Times'a düşüyordu.

## İnternetten referans görsel

Klinik fotoğraf, röntgen, ekokardiyogram çizilemez. `bookimg.py` Wikimedia
Commons'tan **referans** çeker; kitaba nihai hâliyle girmez.

- Sayfaya `("refimg", dict(name=..., cap=...))` ile konur: kehribar şerit
  **REFERENCE ONLY: TO BE REDRAWN BY THE DESIGN TEAM**, kesikli çerçeve ve
  künye satırı. Referans bulunamazsa `("refslot", dict(cap=..., brief=...))`
  ile sayfada yer tutucu bırakılır.
- **Sayfaya yazılan her metin İNGİLİZCE olmalı.** Kitabın font altkümesinde
  Türkçe glif yok; Türkçe brief yazınca Chrome sessizce Times'a düşüyor ve
  QA FONT bulgusu veriyor. Türkçe brief `MEDYA-BRIEF.md`'de kalır.
- Künye satırı italik diziliyor; ProximaNova italiği **orta nokta (·) ve em
  tire (—) taşımıyor** — `_sep_safe()` bunları en tireye çeviriyor.

**Lisans içeriği denetlemez.** Süzgeçten geçen görsellerin çoğu yanlış çıktı:
akciğer röntgeni "kıymık kanaması" olarak, miksomatöz histoloji "romatizmal
mitral darlık" olarak, tarihsel bir portre "tırnak kanaması" olarak geldi.
**Her görseli kontak sayfasına basıp gözle doğrula.** Reddettiklerini
`bookimg.REJECT` içine sebebiyle yaz — arama aynı sonucu tekrar getiriyor.

Kaynak düzeyinde elenenler: filigranlı koleksiyonlar (ECGpedia, ECHOpedia,
CardioNetworks, Radiopaedia…) ve Latin dışı etiketli sürümler (`-ar.`,
`-fa.`…). Aynı Commons dosyası iki yuvaya düşmesin — `used` kümesi buna
bakar. Künyede olmayan dosyalar `_prune()` ile silinir; yoksa reddedilen
adaylar teslim klasörüne sızıp ekibi yanıltıyor.

## Yapma

- Klinik fotoğraf/röntgen gerekiyorsa **çizme** — Wikimedia Commons'tan
  lisansı ticari kullanıma açık (CC0 / kamu malı / CC BY / CC BY-SA) bir
  görsel al, künyesini yaz, **gözle doğrula**. NC ve ND asla.
- Emergency Focus'u kaynak olarak yazma; Avustralya kılavuzlarını yaz
  (eTG, RACGP, RANZCO, ANZCOR, ASCIA, NHMRC).

## Ölçek ve punto (ölçülmüş, tahmin değil)

- **SVG genişliği PUNTO birimiyle yazılır**: `width="518.70pt"`. Birimsiz değer
  CSS pikseli sayılır (518.70 px = 389 pt), şekil %75 ölçekte basılır ve 9
  puntoluk metin 6.75 puntoya düşer. Bu hata sayfaları aşırı sıkışık
  gösteriyordu ve "yazılar kayık" şikayetinin bir kısmının kaynağıydı.
- Kitabın ölçülen punto dağılımı: **8.0 pt %38.7, 9.0 pt %50.6**.
  Karşılığı: gövde metni 9 pt, **şekil ve içerik tablosu metni 8 pt**,
  Rapid Review tablosu 9 pt. `svgfig.FIG_SIZE = 8.0` bunun için var.
- Kitap sayfa başına ~1985 karakter koyuyor; bölüm ortalaması 9.3 sayfa,
  medyan 10. Metin matrisi ağırlıklı şekil aynı içeriği daha az sayfaya
  sıkıştırır: sayfa hedefine ulaşmak için gerçek çizim payı artırılır.

## Gerçek çizim modülü: `bookgen/figart.py`

Metin matrisi yerine kullanılacak çizimler burada: `ecg_panel` (18 şerit),
`heart_coronary`, `cord_section`, `brain_lateral`, `lung_zones`,
`flow_loops`, `pleura`.

Bu modülü yazarken düşülen tuzaklar:

- **Bölge boyaması clipPath ile kırpılır.** Dikdörtgen şeritler doğrudan
  çizilince siluetin dışına taşıyor. `Svg.clip(name, paths)` +
  `group(clip=...)` bunun için eklendi.
- **Kırpılan bölgeler siluetin tamamını kaplayacak kadar taşırılır**,
  yoksa kenarlarda boyanmamış beyaz kamalar kalır.
- **Uzun tek parça Bezier format dizesi sessizce yanlış eğri üretir.**
  Noktalar liste hâlinde `_C(*pts)` ile birleştirilir. Yonca şeklinde
  çıkan gri madde bu yüzdendi.
- **Kesirli kuvvette taban kırpılır**: `(1-u)` kayan noktada -2e-16
  üretip karmaşık sayıya dönüyor. `_pw(base, exp)` bunu engeller.
- **Yön etiketleri şeklin DIŞINA konur** ("Dorsal (posterior)" gri
  maddeyle çakışıyordu).
- **Efsane genişliği sütuna sığdırılır**; taşan efsane metni kırpılıyor.

Her yeni çizim üretimden önce PNG'ye basılıp GÖZLE denetlenir. Bu turda
gözle bakmasa fark edilmeyecek kusurlar: akciğer şeritlerinin taşması,
atriyumun düz çizgiye dönmesi, havada duran büyük damarlar, okunmayan
flutter testeresi, beyindeki beyaz kamalar.

## Eksik glif haritası (ölçülmüş)

Kitaptan çıkarılan font altkümeleri her karakteri taşımıyor. Şeklin metnini
yazmadan önce bu tabloya bak, yoksa Chrome sessizce Times'a düşer ve QA'nın
FONT kapısı yakalar:

| Font | Taşımadığı karakterler |
|---|---|
| ProximaNova-Regular | yok |
| ProximaNova-Bold | yok |
| **ProximaNovaCond-Bold** | **`=` `>`** |
| ProximaNova-Semibold | `=` `+` `–` |
| ProximaNova-Medium | `+` `%` `>` |
| ProximaNova-RegularIt | `+` `%` `5-9` |
| ProximaNova-BoldIt | rakamlar ve çoğu işaret |
| ProximaNovaCond-Regular / Medium / Black | rakamlar ve çoğu işaret |
| DINPro | yalnız rakam taşıyor (sayfa numarası için) |

Pratik kural: **içinde `=` ya da `>` geçen etiketi `S.COND` ile dizme**,
`S.BODY` + weight 700 kullan. Türkçe karakterler (ç ğ ı ö ş ü) hiçbir
altkümede yok, sayfa metni İngilizce kalır.

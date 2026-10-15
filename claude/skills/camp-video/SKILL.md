---
name: camp-video
description: Use when editing CAMPVERSE ders (lecture) videos or any CAMP GROUP video - Loom kaydını indirip kurgulama, kesim talimatlarını uygulama, opener ekleme, takip tablosuna işleme. Triggers - "ders videosunu kurgula", "Loom kaydını edit et", "bölüm videosunu hazırla", "şu videoyu temizle", "video edit", "kesim talimatlarını uygula", "dersleri kurgula".
---

# CAMP VIDEO

**Zanaat kuralları `~/Developer/video-use/SKILL.md`'dedir. ÖNCE onu oku.**
Bu dosya onu KOPYALAMAZ, yalnız CAMP'e özgü farkları tanımlar. Çelişkide bu dosya kazanır.

## Ne iş

CAMPVERSE AMC ders kayıtları Loom'a çıkar, linkleri **"AUSCAMP Ders Çekim"** WhatsApp grubuna
düşer, **kesilecek yerler aynı mesajlarda kabaca dakika olarak** verilir. İş: kaba dakikayı
kesin sınıra oturtmak, başı sonu kırpmak, başa marka openerı koymak, teslim etmek.

Genel amaçlı video işlerinde bu skill devreye girmez, `video-use` tek başına çalışır.

## Çalışma zamanları (KARIŞTIRMA)

| İş | Yorumlayıcı | Neden |
|---|---|---|
| WhatsApp çekimi | `~/camp-lead-crm/.venv/bin/python` | `websocket-client` yalnız burada |
| Video, ASR, ayrıştırma | `~/Developer/video-use/.venv/bin/python` | 3.13 + video bağımlılıkları |
| Takip tablosu | `python3` (sistem) | `openpyxl` yalnız burada |

Araçlar: `~/.local/bin/{ffmpeg,ffprobe,yt-dlp,mlx_whisper}`. Node YOK, Homebrew YOK.

## Akış

```
1 TOPLA    bin/wa_ders_cek.py  → takip/ders_kayitlari.json (link + HAM talimat)
2 ÇÖZ      bin/talimat_coz.py  → kesim noktası adayları
3 İNDİR    yt-dlp              → projects/<proje>/ders.mp4
4 ÖLÇ      bin/sessizlik.py    → edit/sessizlik.json   (SINIRIN TEK YETKİLİSİ)
5 OKU      bin/asr.py          → edit/transkript.json  (yalnız pencereler)
6 YERLESIM bin/yerlesim.py     → kart ve balon geometrisi (kayit basina olculur)
7 KURGULA  edit/edl.json       → bin/olustur.py        → edit/final.mp4  (TEK GECIS)
8 DENETLE  kapılar + görseller → rapor → KULLANICI ONAYI
9 TESLİM   teslim/ + Drive + takip tablosu
```

## Kesim talimatı sözlüğü (21.09.2026'da 56 kayıtlık külliyattan çıkarıldı)

Kesim bildiren kelimeler: **edit, edt, revize, revizyon, revision**

| Gerçek mesaj | Anlamı |
|---|---|
| `26.dk ve 33.dk edit` | 26. ve 33. dakika |
| `4-21-25-40-51-56 Edit` | tire **AYIRAÇ**, aralık DEĞİL: altı ayrı nokta |
| `12 ve 15 edit` | çıplak sayılar dakika |
| `5.dakika 50.sn edit` | bileşik: 5*60+50 |
| `16dk edit` | bitişik yazım |
| `40.dk edit saniyelik` | kusur yaklaşık 1 sn uzunlukta |
| `20.dakika kitap hatası` | **KESİM DEĞİL**, kitap hatası notu |
| `18 ve 25 gibi ... tam emin değilim` | aday, ama **belirsiz** işaretlenir |
| `Bikaç yerde durakladım ama dakika yazamadım` | tam tarama gerekir, kullanıcıya sor |
| `1 saat 15 dakika sorry` | **KAYIT SÜRESİ**, kesim değil |
| `51. Ders sırası karışmasın` | **DERS NUMARASI**, dakika değil |

## Sınırı sessizlik belirler, transkript değil

Kesimin nereye oturacağına `silencedetect` ölçümü karar verir. Transkriptin tek işi
**"burada ders mi anlatılıyor, yoksa kesinti mi"** sorusunu cevaplamaktır.

Sebep: dersler Türkçe, yerel ASR Türkçede tıbbi terimleri kaçırıyor ("STEMI" → "STMI",
"koroner" → "korner", "fibrinolitik" → "fibronitik"). Bu hatalar anlamı bozmuyor, ama zaman
damgasına güvenilmez. Sınır kararını dalga formundan alınca bu zayıflık işi etkilemiyor.

Kural: kaba dakikanın ±90 sn penceresindeki **≥300 ms** boşluklar listelenir, kesim en yakın
boşluğun **ortasına** oturur, kelime ortasından asla kesilmez.

**GÜVENLİK KAPISI:** her kesim için kesilen aralığın transkript metni rapora yazılır.
Metin ders anlatımı gibi görünüyorsa ajan **kesmez**, kullanıcıya sorar. Yanlış yorumlanmış tek bir
talimat ders içeriğini götürür.

## Baş ve son kırpma

İlk konuşmadan **1,0 sn önce** başla, son konuşmadan **1,5 sn sonra** bitir.
Pratikte çoğu kayıt zaten temiz başlıyor (pilotta konuşma 0,64 sn'de), o zaman kırpma yapma.

## Kanvas ve yerleşim: 1920x1080, BANT YOK, kafa slaytın İÇİNDE

Çıktı **her zaman 1920x1080**, asla altına düşmez. Bant yok. Hocanın kamera balonu
**tamamen slaytın içinde** durur. (21.09.2026 kararı: "1080p olsun asla altına düşmesin ...
gri bantlara fln gerek yok" ve "Hocanın kafasını komple slayt içine taşı")

Loom bu dersleri **en fazla 1152x720** veriyor, 1080p yok. Bu Loom tavanı, bizim seçimimiz
değil: aynı sınır kullanıcının referans videosunun kaynağında da ölçüldü (5b45e963, 1152x720).
Yani referans teslim de bir büyütmedir.

### Kaydın anatomisi (21.09.2026'da iki kayıtta ölçüldü, aynı çıktı)

| Parça | Konum |
|---|---|
| Slayt kartı | x=18 y=47, **1115x627, oran tam 16:9** |
| Kamera balonu | merkez (1053, 94), yarıçap 79 |
| Balonun kart dışında kalan tepesi | ~32 px |

**Kart zaten 16:9.** Karta tam oturunca ne bant kalır ne esneme olur, ne de içerikten piksel
gider. Ölçümü `bin/yerlesim.py` her kayıt için yeniden yapar, sabit sayı gömülmez.

> Tuzak: kartı **parlaklık eşiği 180** ile ölçme. Yeşil üst ve alt bantları dışarıda bırakıp
> kartı 1115x577 (oran 1,93) gösterir, sen de 16:9 tutturmak için bant koymak zorunda kalırsın.
> Doğru eşik **55**: koyu tarayıcı zeminiyle kartı ayırır.

### Balonun taşınması ve hayalet yaması

Kart kırpılınca balonun tepesi kesilir. Balon ayrı çıkarılır, daire maskesiyle kartın içine,
sağ üste `%1,5` payla yerleştirilir.

Ama orijinal balonun kart İÇİNDE kalan parçası (hayalet) hâlâ görünür. Bu parça çıktının üst
kenarına değdiği için **daha büyük bir daireyle örtülemez**: üst kenara değen bir bölgeyi
içeren her daire kendisi de üst kenara değer, o zaman da balon "içeride" olmaz. Geometrik
olarak imkânsız, denemeye kalkma.

Çözüm: hayalet bölgesi, slaytın **kendi arka planından** alınan dar bir dikey şeridin yatay
gerilmesiyle kapatılır, sonra balon üstüne konur. Beyaz içerik slaytında, koyu yeşil başlık
slaytında ve kapanış slaytında ayrı ayrı sınandı, üçünde de dikişsiz.

## Kalite: tek geçiş, CRF 14

**En kritik kural.** 21.09.2026'da normalize + render.py zinciri kullanıldı, yani kaynak
İKİ KEZ kodlandı. Sonuç: kaynak 1,10 Mbps iken çıktı 0,55 Mbps'e düştü, kullanıcı kaliteyi geri
istedi. Bir daha olmayacak.

| Dosya | Bit hızı |
|---|---|
| Kullanıcının referans teslimi | 3,29 Mbps |
| Ham Loom indirmesi | 1,10 Mbps |
| Çift kodlanmış kötü çıktı (21.09) | 0,55 Mbps |

Kural: **ara dosya yok, ikinci kodlama yok.** `bin/olustur.py` zinciri tek tutar:
kaynak → kırp → ölçekle (lanczos) → birleştir → kodla. Varsayılan `--crf 14 --preset slow`.
Ses için iki geçiş vardır ama ilk geçiş yalnız ölçüm yapar, video kodlamaz.

`render.py` bu hatta **kullanılmaz**: `scale=1920:-2` dayatıyor, 16:10 kaynakta 1920x1200
verir ve araya normalleştirme adımı zorlar. O adım da ikinci kodlama demektir.

## Opener

`~/camp-video/brand/campverse/opener.mp4` — 6,006 sn, kullanıcının
`02.09.2026 Camverese Örnek Ders Introlu.mp4` teslim videosundan birebir çıkarıldı.

EDL'e **ayrı source** olarak, `ranges`'in **başına** konur. Overlay KULLANILMAZ:
`render.py` overlay'de `-map 0:a` yapıyor, overlay klibinin sesini atıyor ve süre eklemiyor.

`"grade": "none"` sabit. `"auto"` her range'i ayrı analiz edip marka lacivertini kaydırır.

**Kapanış kartı YOK.** Referans teslimde ayrı marka kapanışı yok, ders hocanın kendi
"Thank You" slaytıyla bitiyor. (21.09.2026 kararı: kapanış uydurma, aynı şekilde bırak.)

## EDL iskeleti

```json
{
 "version": 1,
 "sources": {
  "OPENER": "~/camp-video/brand/campverse/opener.mp4",
  "DERS": "~/camp-video/projects/<proje>/edit/ders_1080.mp4"
 },
 "ranges": [
  {"source":"OPENER","start":0.0,"end":6.006,"beat":"OPENER","reason":"CAMPVERSE acilisi"},
  {"source":"DERS","start":0.0,"end":540.2,"beat":"BODY","reason":"..."},
  {"source":"DERS","start":547.8,"end":1086.087,"beat":"BODY","reason":"9. dk kesildi: ..."}
 ],
 "grade": "none", "overlays": [], "subtitles": false, "total_duration_s": 0
}
```

`sources` anahtarları dosya adına giriyor: boşluksuz, `OPENER` / `DERS`.

## Kesim adaylarını bulma (talimat yoksa)

İlk derslerde WhatsApp'ta dakika verilmemiş. Kesimler `bin/tekrar_bul.py` ile transkriptten
ve sessizlik haritasından çıkarılır. **Üç dedektör birlikte çalışır, biri tek başına yetmez.**

| Dedektör | Ne yakalar | Neden gerekli |
|---|---|---|
| Açık işaret | "baştan alıyorum", "pardon", "karıştırdım" | en kolay vaka |
| Örtülü tekrar | hiçbir şey demeden cümleyi yeniden kurma | hoca çoğu zaman bir şey demiyor |
| Ölü zaman | ≥4 sn sessizlik | **bazı kesimler hiç sözel değil** |

**Doğrulama (21.09.2026, CH28).** WhatsApp'ta "9, 12, 19" yazılmış. Sistem bu bilgiyi
görmeden üçünü de buldu: 09:38 açık işaret, 13:00 **7,9 sn sessizlik**, 19:08 açık işaret.
12. dakika ilk taramada kaçtı; sebebi transkriptte ne işaret ne tekrar olmamasıydı, hoca
sadece sekiz saniye susmuştu. Ölü zaman dedektörü bu yüzden var.

### ÖĞRETİCİ TEKRAR KORUNUR (kullanıcının sert kuralı)

(21.09.2026 kararı: "hocanın kendi akışta yaptığı ve ders için yapılan tekrarlara dikkat
edelim onları kırpma yanlış ve hocanın ritim kestiği yerleri keselim asla hata olmamalı")

Hoca öğretmek için çok tekrar ediyor. Bunlar KESİLMEZ. Aynı gün ölçülen iki gerçek örnek:

- 22:32'de aynı cümleyi 5,5 sn arayla iki kez söylüyor, **arada sessizlik yok**, hemen
  öncesinde "Dikkat. Çok önemli.", sonrasında "Önemli." diyor. Bilerek vurguluyor.
- 20:13'te bir liste maddesine dönüyor, aradaki 17 saniye **tamamen gerçek ders**.

Örtülü tekrar dedektörünün ilk sürümü ikisini de kesecekti. İki koruma eklendi:

1. **Duraklama şartı.** Düzeltmeden hemen önce ≥0,6 sn gerçek sessizlik olmalı. Gerçek
   tekrar çekimde hoca durur ve toparlanır; öğretici tekrarda akış kesilmez. En güçlü sinyal.
2. **İşaret şartı.** Çevrede "dikkat, önemli, hatırlayın, unutmayın, tamam mı, tekrar
   ediyorum, özetle, aklınızda kalsın" geçiyorsa dokunulmaz.

Ayrıca 5 kelimeden kısa parçalar hiç değerlendirilmez; "Ne ile?" gibi retorik tekrarlar
böyle korunur.

**Konuşma kesen her aday kullanıcıya metniyle gösterilir.** Ölü zaman kesimleri güvenlidir
(orada konuşma yok), onlar onaysız uygulanabilir.

## Denetim: ölçümü kod yapar

`bin/denetle.py <proje>` altı kapıyı **30 saniyede** ölçer ve yirmi satırlık rapor verir.
Ajan onlarca kareye bakmaz; yalnız KALAN bir kapı varsa kare çıkarılır.
(21.09.2026 kararı: "denetçi kur ama token ve hız optimasyonu da olsun")

Bu araçta düzeltilmiş iki hata, tekrarlama:
- `ffprobe` akış seçimi olmadan çağrılırsa **ses akışının `r_frame_rate=0/0` değeri videonunkini
  eziyor** ve biçim kapısı boşuna kalıyor. `-select_streams v:0` şart.
- Hayalet testi "üst şeridin sapması" ile yapılamaz: slaytın kendi gradyan bandı yüksek sapma
  üretir. Doğru ölçü **yamanın komşusuyla farkı** (eşik 22/255).

## Süreler (21.09.2026'da ölçüldü)

| Adım | Hız |
|---|---|
| Yerel ASR (mlx-whisper large-v3-turbo) | ~20x gerçek zaman (18 dk ders → 63 sn) |
| Kodlama (x264 preset slow, crf 14, 1080p) | ~8,6x gerçek zaman |
| Denetim | 30 sn |

Ortalama 48 dakikalık bir ders uçtan uca **yaklaşık 16-18 dakika** makine zamanı.
`preset medium` ile hız yalnız %15 artıyor ve dosya aynı boyutta kalıyor, yani `slow` bırakılır.

## Kalite kapıları

| # | Kapı | Eşik |
|---|---|---|
| G1 | İndirilen süre beklenenle uyumlu | ±%3 |
| G2 | Çözünürlük | Loom tavanı 1152x720; altı varsa dur |
| G3 | Disk boş alanı | ≥15 GB |
| G4 | Sessizlik haritası çıkarıldı, konuşma sınırları bulundu | zorunlu |
| G5 | Gereken pencereler çözüldü, dil `tr` zorlandı | istisnasız |
| G6 | Her kesim için kesilen metin rapora yazıldı | istisnasız |
| G7 | Kesimler ≥300 ms boşluğa oturdu, kelime ortası yok | ihlal 0 |
| G8 | Kesim oranı | %3-25, üstü insan incelemesi |
| G9 | EDL tutarlı: `end>start`, örtüşme yok | ±0,05 sn |
| G10 | İlk range OPENER | zorunlu |
| G11 | Çıktı süresi EDL toplamıyla uyumlu | ±0,5 sn |
| G12 | 1920x1080, 24 fps, 48 kHz stereo | tam eşleşme, 1080p altı ASLA |
| G12b | Çıktı bit hızı | ham kaynağın altına düşmez |
| G12c | Siyah bant yok (`cropdetect` çıktıda tam kare verir) | zorunlu |
| G12d | Balon tamamen kare içinde, hayalet (ikinci kafa) yok | gözle, sağ üst köşe |
| G13 | Ses seviyesi | I = -14 ±1 LUFS |
| G14 | Her kesim sınırında `timeline_view` görseline BAKILDI | sıçrama, pop yok |
| G15 | İlk kare opener, son kare dersin kapanışı | gözle |
| G16 | Takip tablosu ve TSV güncellendi | doğrulandı |
| G17 | Ara dosyalar silindi | `df` ile teyit |

En fazla 3 düzeltme turu, sonra kullanıcıya bildir.

## Tuzaklar (hepsi 21.09.2026'da yaşandı)

- **Loom kısa kimlik çalışmaz.** 8 karakterli önek 404 verir, 32 karakterin tamamı şart.
- **ffmpeg ilerleme çıktısı bağlamı şişiriyor.** Daima `-nostats`, uzun işte `> log 2>&1`.
- **`timeline_view` çıktıyı `<video klasörü>/edit/verify` altına yazar.** Proje içinden
  `edit/final.mp4` verirsen `edit/edit/verify/` oluşur. Şaşırma.
- **Marka klipleri proje klasörüne KONMAZ.** video-use'un toplu transkripti klasör kökündeki
  tüm videoları tarar; orada duran opener boşuna işlenir.
- **`aresample=...:resampler=soxr` bu ffmpeg derlemesinde YOK.** Düz `aresample=48000` kullan.
- **`pgrep -f "<desen>"` KENDİ komutunu da yakalar.** `until [ -z "$(pgrep -f 'x.py')" ]`
  döngüsü kendini görüp sonsuza kadar döner. Süreç bekleyeceksen çıktı dosyasının varlığına
  ya da `pgrep -x ffmpeg`'e bak. 21.09.2026'da bir teslim bu yüzden yarım saat bekledi.
- **`-af` ile `-filter_complex` çıktısı birlikte kullanılamaz.** loudnorm grafiğin içine yazılır.
- **loudnorm JSON'unu süslü parantez arayarak ayrıştırma**, alan bazlı regex kullan.
- **WhatsApp tek oturum kuralı.** `WaLock` alınmadan dokunulmaz; ikinci Chrome profili
  CAMP LEAD'in şifreli anket geçmişini kalıcı bozar.

## ⛔ YASAKLAR

- **Kullanıcı onaylamadan hiçbir video yüklenmez, paylaşılmaz.** (21.09.2026 kararı: "önce ben izleyeyim")
- **Paylaşılan müfredat tablosuna YAZILMAZ.** Salt okunur. Kendi takip tablomuz tutulur,
  satırları kullanıcı kendisi taşır. (21.09.2026 kararı: "sen ayrı bir tabloda tut")
- **Ücretli transkript kullanılmaz.** Yerel `mlx_whisper` varsayılandır.
  (21.09.2026 kararı: "para vermek istemiyorum")
- **Loom kayıt kontrolleri ve kalem paleti kırpılmaz, bulanıklaştırılmaz.**
  (21.09.2026 kararı: "olduğu gibi kalsın")
- **İki kez kodlama YOK.** Ara normalleştirme dosyası üretme, `render.py` kullanma.
- **1080p altına inme.** Kaynak ne olursa olsun çıktı 1920x1080.
- **Yan/gri bant koyma.** Kart zaten 16:9, karta otur.
- **Hocanın kafasını kesme.** Balon tamamen kare içinde olacak.
- **Hayaleti örtmek için büyük daire deneme.** İmkânsız, yama kullan.
- **Talimatta olmayan yer kesilmez.** Kendi kafana göre "şurası da sürçme" deyip kesme.
- **Kitap hatası notu kesime çevrilmez**, ayrı not olarak taşınır.
- **Ham dosya, Drive linki doğrulanmadan silinmez.**

## Teslim kapısı (doğrulanabilir)

```bash
ffprobe -v error -show_entries format=duration,bit_rate:stream=width,height,r_frame_rate,channels,sample_rate \
  -of default=noprint_wrappers=1 edit/final.mp4     # 1920x1080, 24/1, 2, 48000, bit_rate >= kaynak
ffmpeg -nostats -v error -ss 300 -t 2 -i edit/final.mp4 -vf cropdetect=24:2:0,metadata=print:file=- \
  -an -f null - 2>&1 | grep cropdetect.w=           # 1920 olmali: bant yok demektir
ffmpeg -nostats -hide_banner -i edit/final.mp4 -af loudnorm=print_format=json -f null - 2>&1 \
  | grep input_i                                     # -14 ±1
df -h ~ | tail -1                                    # ≥15 GB
```

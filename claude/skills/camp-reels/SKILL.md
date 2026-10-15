---
name: camp-reels
description: Use when turning a CAMP GROUP webinar recording (Zoom, DENTCAMP / UKCAMP / AUSCAMP) into Instagram reels - "webinardan reels çıkar", "webinar kesiti", "önemli dakikaları reels yap", "bu kayıttan reels üret", "premium reels". Runs ~/camp-reels pipeline: transcript, moment selection, director scene plan, AI/açık kaynak görsel, Remotion render (soru kartı, kelime vurgulu altyazı, hareketli grafik, SFX), audit gates, preview. Never publishes.
---

# CAMP REELS: webinar kaydından premium reels

Format kaynağı: `~/camp-reels/analiz/RAPOR.md` (@camp2uk 23 webinar kesiti analizi). v2 kararları (kullanıcı, 8 Eki 2026): dört görsel türü de (grafik, AI, açık kaynak, slayt zoom), kelime kelime vurgulu altyazı, yalnız SFX (müziği kullanıcı IG'de ekler), girişte soru kartı, sonda 2 sn marka kartı.

## Akış (olgu → karar → üretim → denetim)
```bash
cd ~/camp-reels
# 1) OLGU: ses, sessizlik, kelime zamanlı transkript (marka sözlüğüyle), Zoom yerleşimi, brief
python3 bin/hat.py "<kayit.mp4>" --marka dentcamp --ad dentcamp-GGAA-konu
#    edit/yerlesim_kontrol.jpg'yi GÖZLE aç. proje.json'a "hoca": {"ad","unvan"} ve "webinar" yaz.
# 2) ANLAR: camp-reels-anlar agent'ı edit/brief.md -> JSON (soru, hook_puani dahil) -> edit/anlar.json
# 3) KES: python3 bin/hat.py projects/<ad> --kes   -> edit/klip_NN/ (slayt.mp4, konusmaci.mp4, ses.wav, klip.json, slayt_serit.jpg)
#    ⚠ KAMERA GEÇİŞİ uyarısı = Zoom başka birine geçti (moderatör "evet" der). Gözle bak, parçayı böl (anlar.json) ve yeniden --kes.
#    Altyazı metnini oku: kelime düzeltmesi edit/duzeltme.json, çok kelimelik düzeltme edit/ifade.json [["Berufsel Lappnis","Berufserlaubnis"]].
# 4) YÖNETMEN: her reels için camp-reels-yonetmen (paralel) -> edit/yonetmen_NN.json
#    Hocanın sürçmesi: "gizle": [kelime idx] (ses kalır, altyazıda gösterilmez).
# 5) GÖRSEL: ai_gorsel istekleri -> Higgsfield generate_image_batch (gpt_image_2_5, 16:9, use_unlim:false, ~0,25 kredi)
#    -> edit/assets/NN/<id>.png ; GÖZLE aç ; edit/assets/NN/CREDITS.json {id, dosya, dogrulandi, karar, kunye:"Temsili görsel"}
#    acik_kaynak istekleri -> camp-reels-gorsel agent'ı (Wikimedia, lisans kontrolü, gözle doğrulama)
# 6) ÜRET + DENETLE: python3 bin/hat.py projects/<ad> --v2 [--no 2] [--taslak]
#    sahne.py (kural zorlama) -> remotion/render.mjs -> denetle.py R1-R11 -> out/ONIZLEME.html
# 7) GÖZ: camp-reels-denetci agent'ı (soru kartı, her ekleme, altyazı, kapanış kareleri) -> düzelt -> kullanıcı
```
Süreler: 83 dk kayıt ~4 dk ASR; reels başına render ~1,5 dk (tam), ~2,5 dk (ilk seferde Chrome indirme).

## Ekran (1080x1920)
Slayt paneli y 203-811 (eklemeler buraya biner) · altyazı bandı y≈925 · konuşmacı paneli y 1040-1603 (yuvarlak köşe, turkuaz çerçeve, zoom punch-in) · düzen `konusmaci` ise konuşmacı 4:5 tam, eklemeler üstte kart. Remotion bileşenleri: `remotion/src/bilesen/` (SoruKarti, Altyazi, Ekleme: stat/adimlar/karsilastirma/rozet/gorsel, HocaEtiketi, Kapanis). Marka renkleri `brands/<marka>.json` → `v2`.

**Yalnız konuşmacı olan kesit (soru-cevap):** `anlar.json`'da `"duzen_zorla": "gorsel"` ver (kullanıcı, 9 Eki 2026).
- Düzen aynı kalır, hoca altta 1000x563'tür ve Zoom'un tam karesinden kırpılır (daha keskin).
- Üst panelde slayt yerine `edit/assets/NN/` doğrulanmış görsellerden 5,5 sn'lik Ken Burns akışı döner; geçişlerde kayma ve swoosh var (`TepeAkis`).
- Akışın boş kalmaması için en az 4-5 görsel üret.

## Kapılar (bin/denetle.py)
R1 1080x1920/30fps/h264+aac/faststart · R2 22-80 sn · R3 -14±1 LUFS, TP ≤ -1 · R4 ilk/son 3 kelime (çıktının kendi sesi) · R5 metin benzerliği ≥ 0,80 · R6 siyah kare yok · R7 kart metin sınırları · R8 her görsel CREDITS'te doğrulanmış · R9 altyazı senkronu ≤ 150 ms (3 nokta) · R10 SFX seviye ≤ 0,45 · R11 kesitte Zoom kamera geçişi yok · R12 her iç kesim noktasında kelime yutulmamış.

## Ölçülmüş tuzaklar
- **Dolgu kesimi (9 Eki 2026 son hali, `kes.sabit_unlu_bul`):**
  - "eee/ııı" akustik olarak bulunur: sesli + tını sabit (spektral akı < %60 medyan) + perde düz (100 ms'de < 2 Hz), ≥ 0,3 sn.
  - Kesim sesli harfin İÇİNDEN yapılır, iki uçta 60 ms ünlü kalır; bitişik uzun sessizlik de kısaltılır.
  - Uzatılmış kelime sesi ("aaaama") de kısalır; kelime, süresinin 80 ms+'ı kalıyorsa altyazıdan düşmez.
- **Altyazı tamamlama (`kes.altyazi_tamamla`):** genel 80 dk transkript bazı cümleleri hiç yazmıyor. Klip sesi kısa bağlamda yeniden çözülür, 2+ kelimelik eksikler eklenir. Elle ifade düzeltmesi yaparken sesi dinlemeden tahmin etme ("beni sizin" → "bence sizin" yanlıştı; doğrusu "tecrübeniz sizin").
- **Zaman eşleme:** `zaman_esle.py` yönetmen planına `_parcalar` yazar ve sonraki eşlemede kaynak zamanı üzerinden kesin eşler. Aynı kesit iki kez kesilse de zamanlar kaymaz.
- **KELİME YUTMA (8 Eki 2026, kullanıcı: "kelimeleri çok yutmuş"):** "kelimeler arası sesli boşluk = dolgu" kuralı 14 kesimin 7'sinde gerçek konuşma yuttu ("2020", "Yeni", Fachsprachprüfung...). whisper bazı kelimeleri hiç yazmıyor, boşluk sesli diye dolgu değil. Kural kaldırıldı. Dolgu artık şöyle kesilir:
  - yalnız dolgu-yönlendirmeli whisper açıkça "eee/ııı/ähm" yazdıysa
  - sınır enerji vadisine oturur; tabanın 12 dB üstündeyse kesilmez
  - kesilecek ses iki whisper'la (normal + dolgu prompt) yeniden çözülür, gerçek kelime çıkarsa kesilmez
  - kesilmeyenler `klip.json` "kesilmeyen" listesine yazılır
  - R12 kapısı her iç kesimin iki yanındaki 2'şer kelimeyi çıktı sesinde arar
- whisper bitişik kelimelere yapışık zaman verir: sınır sessizlik haritasına oturur (`uret.sinirla`), kelime orta noktayla seçilir.
- whisper kelime başına "..." koyar, ekleri ayırır ("'nde"), sayıları böler ("450 -500"): `kes.py` temizler; terimler (`Berufserlaubnis`, `Kenntnisprüfung`) ifade.json ile.
- Zoom aktif konuşmacı geçişi ~1 sn gecikir: moderatörün "evet"inden sonra hoca konuşsa da kamera 2-3 sn başkasında kalır. Parçayı geçiş bitince başlat (kamera_gecisi listesine bak).
- Altyazı sayfası en çok 5 kelime / 2 satır; 40 karakteri geçerse punto 56'ya iner. Daha uzunu panellere taşar.
- AI görseller (DENTCAMP Almanya) penceresine hep Köln Katedrali koyuyor: prompt'a "no landmarks" ekleyerek çeşitlendir.
- Yeni agent dosyası aynı oturumda yüklenmez: general-purpose agent'a `~/.claude/agents/<ad>.md` okut.
- Node: `~/.local/node/bin` (sistemde yok). Python numpy/PIL: `~/Developer/video-use/.venv/bin/python`.

## ⛔ Yapılmaz
Yayın yok (paylaşım ayrı akış: caption-üretici 5 varyant → kullanıcı seçer → make_publish .sh, kullanıcı `!` ile, `--cover-ms 0`). Asana'ya yazma yok. Kapak eklenmez. Hocanın söylemediği bilgi/rakam ekrana konmaz. Doğrulanmamış görsel konmaz. Katılımcı (ekip dışı) yüzü olan reels kullanıcıya sorulmadan teslim edilmez. Mentör/webinar içeriği kullanıcı istemeden üretilmez.

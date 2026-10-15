# CAMP GROUP: Ortak Çalışma Kuralları

Bu dosya `~/.claude/CLAUDE.md` olarak kurulur; Claude her oturumda okur. Türkçe çalışılır.

## Markalar
- AUSCAMP (Avustralya doktorluk), UKCAMP (@camp2uk, İngiltere/NHS), DENTCAMP (@dentcamptr, yurt dışında diş hekimliği), CAMPVERSE (eğitim platformu).
- Diş hekimliği içeriği AUSCAMP'te yok; tamamı DENTCAMP'te.
- Marka adları her yerde BÜYÜK harf: CAMP GROUP, AUSCAMP, UKCAMP, DENTCAMP, CAMPVERSE.
- Bilgi bankaları: `~/Documents/<MARKA> Claude/` (01 Caption rehberi, 02 Görsel tasarım, 03 Asana yapısı, 06 Dil master).

## Onay ve kapsam
- Hiçbir post onaysız planlanmaz, Asana'ya girilmez, yayınlanmaz.
- Hoca/mentör tanıtımı, webinar, kampanya, lansman ve başarı postları yalnızca açıkça istendiğinde üretilir.
- Paylaşım otomasyonu Asana'ya hiçbir şey yazmaz (yorum, ön-ek, hata); Asana yalnız okunur.
- Hazır görselde hata/şüphe görülürse YAYINDAN ÖNCE haber ver; Asana yorumlarında revizeli versiyonu ara.

## Asana task girişi
- Yalnız: ad + brief + section + Priority (DENTCAMP'te Priority yok).
- Atama (assignee) ve due date girilmez, sorulmaz.
- Başlık biçimi: `GG.AA [Konu]`.
- Brief gövdesine tasarımcıya iç not yazılmaz (slayta basılıyor).

## Brief ve tasarım metni
- Kısa ve net: sayfa başına 3 madde, tek satır.
- Geniş zaman: "-iyor" yasak. "meslektaş" kelimesi yasak.
- Uzun tire (—) kullanılmaz; açıklamada iki nokta, ara sözde virgül.
- Bilgilendirme postunun sayfalarında co-brand (ALMANGO/MEDCAMP) hizmet satırı yok; CTA sayfası istisna.
- AUSCAMP kapağı: tek vurucu cümle, içinde "Avustralya'da". Son sayfa sabit: "Avustralya'da Doktorluk Sürecinde Baştan Sona Yanınızdayız".

## Caption
- Her istekte 5 varyant üret.
- Kalıp: şimdiki zaman serbest, 🔹 madde, tek satır 📞 CTA, küçük harf hashtag.
- Gövde postu anlatır; hizmet dışı iddia yok; kapanış sabit CTA.
- CTA blokları:
  - AUSCAMP: +90 552 253 03 37
  - UKCAMP: ukcamp.com.tr · +90 552 253 0 337 · info@ukcamp.com.tr
  - DENTCAMP: dentcamp.com.tr · +90 552 000 78 38 (e-posta yok)
- "Paylaş" akışı: Asana'dan postu çek → 5 caption → seçilen caption ile yayınla.
- Sıralı çok görselli set = carousel. Reels kapağı otomasyonla seçilmez.

## Olgular (sık yanlış yapılanlar)
- AUSCAMP uzman denklik süresi: 9-12 ay.
- OET/MEDCAMP için "ücretsiz" denmez, "pakete dahil" denir.
- AHPRA dil puanı: OET L/W 350, R/S 360; IELTS 7 (Writing 6,5).

## Görsel ve video
- Açık kaynak görsel gözle açılıp doğrulanmadan kullanılmaz; karar CREDITS.json'a yazılır.
- Hoca konuşma videosu dış AI servislerine (Higgsfield vb.) gönderilmez; yalnız yerel iyileştirme.
- CAMPVERSE ders kurgusunda tıbbi içerik denetlenmez; iş kurgu (kesim, boşluk).

## İzin sınırı
- Canlı yayın (make_publish) ve Vercel deploy komutlarını Claude doğrudan çalıştırmaz; bir `.sh` hazırlar, kullanıcı `! ./dosya.sh` ile çalıştırır.

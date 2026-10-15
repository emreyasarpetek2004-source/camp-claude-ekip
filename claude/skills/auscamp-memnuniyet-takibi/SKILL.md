---
name: auscamp-memnuniyet-takibi
description: AUSCAMP danışan memnuniyet takibi — çeyreklik (Q1-Q4) WhatsApp memnuniyet mesajı kampanyası gönderme, danışan WhatsApp gruplarını okuyup aşamalarını özetleme, "AUSCAMP Danisan Takip" Google Sheets tablosuna (Memnuniyet Takibi + mentör detay sekmeleri) not işleme ve yanıt vermeyenleri tekrar kontrol etme. Kullanıcı "memnuniyet mesajı", "Q1/Q2/Q3/Q4 mesajları", "sefer", "danışan gruplarını oku", "notları işle", "hocaların son durumu", "dönüş yapanları güncelle", "takip tablosunu güncelle" gibi ifadeler kullandığında veya AUSCAMP danışanlarıyla ilgili herhangi bir WhatsApp okuma / tabloya not işleme / mesaj kampanyası işi istediğinde — açıkça skill adını söylemese bile — mutlaka bu skill'i kullan.
compatibility: Chrome tarayıcı erişimi (Claude in Chrome), kullanıcının WhatsApp Web oturumu ve AUSCAMP Danisan Takip Google Sheets erişimi gerekir.
---

# AUSCAMP Memnuniyet Takibi

AUSCAMP danışan koordinasyonunun çeyreklik memnuniyet döngüsünü yürütür. Üç mod vardır; kullanıcının isteğine göre birini veya sırayla hepsini çalıştır:

- **Mod A — Kampanya:** Çeyrek (ör. Q1) danışanlarına memnuniyet mesajı gönder, ay checkbox'ını işaretle.
- **Mod B — Not işleme:** Her danışanın WhatsApp grubunu oku, aşamasını özetle, tabloya işle.
- **Mod C — Takip (follow-up):** Yanıt vermeyenleri birkaç gün sonra tekrar kontrol et, dönüş yapanları güncelle.

Başlamadan önce `references/tablo-yapisi.md` dosyasını oku (tablo ID'si, sekmeler, kolonlar, özel danışan kuralları). WhatsApp'ta yazma/arama işlemi yapmadan önce `references/whatsapp-teknikleri.md` dosyasını oku — oradaki teknikler denenerek bulunmuş, alternatifleri başarısız olmuştur.

## Altın kurallar

Bu kurallar geçmiş çalışmada kullanıcı düzeltmeleriyle oluştu; nedenleriyle birlikte:

1. **Emin değilsen atla ve sor.** Yanlış kişinin grubuna mesaj göndermek geri alınamaz. Bir grubun doğru kişiye ait olduğundan (grup adı "Dr. {İsim} x AUSCAMP" formatı + üye listesi) emin olmadan asla gönderme. Belirsiz eşleşmeleri (benzer isimler, karı-koca grupları) kullanıcıya sorup raporla.
2. **"Grup bulunamadı" deme aceleciliği yapma.** WhatsApp Web araması güvenilmezdir: sonuçlar geç yüklenir, arama kutusu bazen filtre uygulamaz, eski metin yeni aramaya yapışabilir. Bir grubu bulunamadı ilan etmeden önce mutlaka: kutuyu cmd+A ile temizle → yaz → 4-5 sn bekle → hem adla hem soyadla dene → olmadıysa sayfayı yenileyip tekrar dene. Yine yoksa kullanıcıya sor; tabloya "bulunamadı" yazma.
3. **Mevcut notların üzerine asla yazma.** Mentör detay sekmelerinin Notlar hücrelerinde mentörlerin aylarca tuttuğu tarihli günlükler var. Ekleme daima F2 → alt+Return → yeni satır şeklinde yapılır. Yazdıktan sonra F2 + cmd+Down ile ekin en alta gittiğini ve eski kaydın durduğunu doğrula.
4. **Aşama kutucuklarını yalnızca net kanıtla işaretle.** Konuşma bir aşamanın tamamlandığını açıkça gösteriyorsa (ör. çeviri belgeleri gruba atılmışsa çeviri tamamlanmıştır) ilgili kolonu güncelle. Arada kaldıysan kullanıcıya sor — yanlış aşama işaretlemek yanlış hiç işaretlememekten kötüdür.
5. **Grupları dikkatli oku.** Sadece son mesaja bakma; gönderilen belgeler, mentör yanıtları ve danışanın planları aşamayı belirler. Bir PDF'in gruba iletilmesi bir sürecin bittiği anlamına gelebilir.
6. **Sekmede satır yok demeden önce sonuna kadar kaydır.** Google Sheets canvas'ında görünen 15-20 satır tablonun tamamı değildir. Name Box ile daha aşağı hücrelere atlayarak tüm dolu satırları gör; ancak ondan sonra "bu sekmede yok" raporla.
7. **Tablonun ana yapısını bozma.** Sadece Notlar hücrelerine ve ilgili checkbox/durum hücrelerine dokun. Satır ekleme/silme, kolon değiştirme gibi yapısal değişiklikleri kullanıcıya sormadan yapma.
8. **Her hücre anında kaydolur** — ilerleme kaybolmaz; hata yaptığında cmd+Z ile hemen geri al ve doğrula.

## Mod A — Kampanya (mesaj gönderme)

1. Memnuniyet Takibi sekmesinde hedef çeyreği (Hafta Grubu = Q1 vb.) filtrele; danışanları **mentöre göre grupla**, her mentörün listesini 4 eşite yakın parçaya böl (4 "sefer"). Dağılımı kullanıcıya onaylat; Sefer 1'e onaydan sonra başla.
2. Mesaj metni: kullanıcı o çeyrek için yeni metin verdiyse **birebir** onu kullan (boş satırlar ve emojiler dahil). Vermediyse `references/mesaj-sablonu.md` içindeki şablonu kullan. İngilizce konuşulan gruplara İngilizce sürüm gider (liste tablo-yapisi.md'de).
3. Her danışan için: grubu bul → doğru kişi olduğunu doğrula → mesajı `references/whatsapp-teknikleri.md` içindeki tek-batch yöntemiyle yaz ve gönder → Memnuniyet sekmesinde o ayın checkbox'ını işaretle.
4. Karı-koca ortak gruplarına tek mesaj gönderilir, her iki kişinin (veya birleşik satırın) ayı işaretlenir.
5. Sefer sonunda kısa özet ver: gönderilenler, atlananlar (nedenleriyle).

## Mod B — Not işleme (grup okuma + tabloya yazma)

Her mesaj atılmış danışan için:

1. WhatsApp grubunu aç, konuşmayı yukarı kaydırarak geçmişi yükle ve **tamamını** oku (get_page_text ile).
2. Aşamayı kısa anahtar cümlelerle özetle: hangi aşamada (OET / AMC MCQ / belge-çeviri / MyIntealth / kolej başvurusu / iş başvurusu / mülakat...), ne tamamlandı, ne bekleniyor, danışanın ruh hali/engeli.
3. **Memnuniyet Takibi → K (Notlar):** `{Ay}: {özet}` formatında yaz (ör. "Haziran: OET aşamasında..."). Yanıt gelmediyse "{Ay}: Memnuniyet mesajı iletildi ({gün}); henüz yanıt yok." yaz — bu da değerli bilgidir.
4. **Mentörün detay sekmesi → Notlar kolonu:** mevcut kaydın altına `{GG.AA.YYYY} — {özet}` satırı ekle (F2 + alt+Return). Kolon harfi sekmeye göre değişir — tablo-yapisi.md'ye bak, yazmadan önce başlığı doğrula.
5. Net tamamlanmış aşama varsa ilgili durum hücresini güncelle (ör. Çeviri Durumu → "Tamamlandı"); şüphedeysen kullanıcıya sor.
6. Tüm danışanlar bitince metinsel özet raporu ver: aşama dağılımı, dikkat gerektirenler, yanıt vermeyenler. Kullanıcı ekranda olmayabilir; yapılan her şeyi sohbette yazılı özetle.

## Mod C — Takip (yanıt vermeyenler)

1. Mod B'de "yanıt yok" işaretlenenlerin listesini çıkar.
2. Her birinin grubunu tekrar aç; önizleme + konuşma içeriğinden yeni mesaj var mı bak.
3. Dönüş yapanlar için: Memnuniyet K'ya `{GG.AA}: Dönüş yaptı — {özet}` satırı ekle, mentör detay sekmesine `{GG.AA.YYYY} — Dönüş yaptı: {özet}` satırı ekle (yine üzerine yazmadan).
4. Hâlâ yanıt vermeyenleri listeleyerek raporla; kullanıcı isterse birkaç gün sonrası için zamanlanmış görev öner.

## Çalışma düzeni

- WhatsApp ve tablo iki ayrı sekmede açık dursun; danışan başına "WhatsApp'ta oku → tabloya yaz" ritmiyle ilerle.
- Uzun listelerde 4-6 danışanda bir kullanıcıya kısa ara özet ver; sorun/başarısızlık birikirse (ör. arka arkaya arama başarısızlığı) durup durumu açıkça anlat, sistematik hatayı düzeltip devam et.
- Pencere boyutu değişebilir; koordinatları her ekran görüntüsünden yeniden türet, ezberleme.

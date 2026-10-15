---
name: webinar-lead
description: Use when webinar poll leads need to go into the CRM — after an AUSCAMP, UKCAMP or DENTCAMP webinar, when the user says "webinar leadlerini gir", "anket leadlerini CRM'e aktar", "bu haftanın leadlerini çek", "lead aktarımı yap", or asks about missing leads from a past webinar. Runs the ~/camp-lead-crm tool.
---

# Webinar anket leadleri → Quickesta CRM

Araç: `~/camp-lead-crm` (Python + CDP + Quickesta GraphQL). Kullanıcı bunu **her webinar
sonrası** çalıştırıyor. Detaylı teknik anlatım ve tuzaklar: `~/camp-lead-crm/PLAYBOOK.md`
— karar vermen gereken bir şey çıkarsa önce oraya bak.

## Akış

```bash
cd ~/camp-lead-crm
./bin/chrome-start.sh                        # otomasyon Chrome'u (zaten açıksa atlar)
./bin/lead doctor --brand <marka>            # WhatsApp bağlı mı, CRM oturumu var mı
./bin/lead webinar --brand <marka>           # anketi bul → oyları çıkar → CRM planı (dry-run)
./bin/lead push --brand <marka> --date <tarih> --yes    # SADECE kullanıcı onaylayınca
./bin/lead verify --brand <marka> --date <tarih>
```

`webinar` komutu tarihten (boşsa en son Pazar) grupları kendi bulur, konuyu grup
başlığından çıkarır, tabloyu üretir ve CRM planını dry-run olarak gösterir. Doğru CRM'e
geçişi de kendi yapar. Grup id'si vermeye gerek yok.

## Kurallar

1. **Onaysız yazma yok.** `webinar` çıktısındaki planı kullanıcıya sun (kaç yeni kayıt, kaç
   atlanacak, kimler girilmeyecek), onayını al, sonra `push --yes`.
2. **Sayıları doğru anlat.** Anket balonundaki sayılar *işaretleme*, kişi değil. Bir kişi
   birden fazla seçenek işaretleyebilir, iki grupta da oy verebilir. Raporda hep üç
   satırı ayır: işaretleme / oy veren kayıt / tekil kişi.
3. **Uyarı varsa yazma.** "oy sayısı okumalar arasında değişiyor" uyarısı gelirse oylar
   hâlâ senkronlanıyor demektir; biraz bekle ve `webinar` komutunu tekrar çalıştır.
4. **Ekip üyeleri lead değil** (`team_names`: Genel Koordinatör, Satış temsilcisi 1). Yeni bir ekip
   üyesi oy verirse kullanıcıya sor, onaylarsa config'e ekle.
5. **Silme/birleştirme yok.** Mükerrer kayıt çıkarsa karar kullanıcının; sen sadece raporla.
6. ⚠ işaretli satırlar (önceki turda girilmiş ama kaydı silinmiş) kullanıcıya ayrıca söylenir.
7. Telefonu çözülemeyen oy verenler CRM'e yazılmaz; raporda "TELEFON YOK" olarak geçer.
   Numara ancak kişiden istenerek alınabilir.

## Markalar

Atama kaynağı her zaman `config/brands.yml`'dir, bu tablo değil.

| Marka | CRM | Atanan personel |
|---|---|---|
| auscamp | AUSCAMP CRM | **Satış temsilcisi 1 / Satış temsilcisi 2 yarı yarıya** (21.09.2026 kullanıcı kararı, `split_assignees`) |
| ukcamp | UKCAMP CRM | Satış temsilcisi 3 |
| dentcamp | DENTCAMP CRM (07.09.2026'da açıldı) | ankette işaretlenen ülkeye göre: Satış temsilcisi 4 / Satış temsilcisi 3 / Satış temsilcisi 1 |

## Kritik ön koşul

Anket oyları cihaz anahtarıyla şifreli: otomasyon Chrome profili
(`~/.camp-lead-chrome`) WhatsApp'a **anket gönderilmeden önce** bağlı olmalı. Bağlantı
koparsa o haftanın oyları kalıcı olarak okunamaz. Bu yüzden webinardan önce
`./bin/lead doctor` ile bağlantıyı teyit et.

#!/usr/bin/env python3
"""DENTCAMP: ABD (üç yol: Advanced Standing · Uzmanlık/ADEA PASS · AEGD/GPR).

Kaynak metinler:
  · BROŞÜR VE TANITIM/usa/Amerika_Dis_Hekimligi_Brosur.docx  (1. Yol)
  · Yol2_Uzmanlik_ADEA_PASS.docx                              (2. Yol)
  · Yol3_AEGD_GPR.docx                                        (3. Yol)

Yol 2 ve 3 belgeleri "danışman rehberi" olarak yazılmıştı (öğrenciye sordur,
kontrol listesi vb.). Katalog danışana gittiği için metin danışan diline ve
AUSCAMP Specialist Pathway kataloğunun kurumsal register'ına çevrildi.
"""
from build import H1, BAR, P, SUB, UL, DL, BOX, CTA, STATS
from content._common import (intro, mentorler, placeholders,
                             whatsapp_and_mentorship, PHONES)   # noqa: F401

ULKE = "ABD"

COVER = {
    # Kapak alt bandındaki üç künye — hepsi katalogda zaten geçen bilgiler.
    "kunye": [
        ('YOL', 'Üç ayrı yol'),
        ('SINAV', 'INBDE + ADEX'),
        ('HEDEF', 'Eyalet lisansı'),
    ],
    "pill": "Amerika’da",
    "title": "Diş Hekimliği\nKariyeri",
    "tag": "| US LICENSURE",   # diğer üç kapak da resmî süreç adı kullanıyor
    "sub": "(Diş hekimliği öğrencileri ve\ndiş hekimleri için süreç rehberi)",
}

INTRO = intro(ULKE)
MENTORLER_BOLUM = mentorler(ULKE)
MENTOR_YERI = 0        # kadro ORTAK İLK ADIMLAR'ın hemen başında.
                       # 2 Eylül 2026'da yeniden ölçüldü (dil yeterliliği hizmet
                       # bölümü çıktıktan sonra): 0 -> 16 sayfa, zayıf sayfa YOK;
                       # 1 -> 17 sayfa ve s.11 %32; 2 -> 17 sayfa ve s.4 %24;
                       # 11 -> 17 sayfa ve s.11 %32. Eski ölçümde (bölüm hâlâ
                       # dururken) 1 en iyiydi, 0 ise s.3'ü %15'te bırakıyordu.
MENTORS = placeholders(4, ULKE)

# --- Mentör (gerçek) --------------------------------------------------------
# Kaynak: ~/Downloads/Mentör Biyografi ve fotoğraflar/USA/
MENTOR_TAM = [dict(
    foto="m_ayse_nil_kocak.png",
    ad="Ayşe Nil Koçak, DDS",
    meta="DİŞ HEKİMİ & MENTÖR · NEW YORK, ABD",
    bio=[
        "2021 yılında Yakın Doğu Üniversitesi Diş Hekimliği Fakültesi’nden mezun oldum. "
        "Mezuniyetimin ardından Amerika Birleşik Devletleri’ne taşınarak dental asistan "
        "olarak ortodonti, ağız ve çene cerrahisi ve genel diş hekimliği alanlarında "
        "klinik deneyim kazandım; Amerikan diş hekimliği sistemini yakından tanıdım.",
        "**INBDE** sınavını geçtikten sonra kariyerimi ABD’de sürdürmeye karar verdim. "
        "Hâlen Manhattan’da klinik dental asistan olarak görev yapıyorum ve bu başvuru "
        "döneminde okullara başvurmuş durumdayım.",
        "Uluslararası diş hekimlerinin Amerika’daki kariyer yolculuğunu desteklemeye önem "
        "veriyorum; bu amaçla **Doctors Beyond Borders** adlı bir podcast başlattım. "
        "Mentörlükte INBDE hazırlığı, dental asistan olarak iş bulma, adaptasyon, klinik "
        "deneyim ve ABD’de kariyer planlaması konularında deneyimlerimi paylaşıyorum.",
    ],
)]


BODY = [
    # -- üç yolun haritası ---------------------------------------------------
    [
        H1("ABD’DE ÜÇ FARKLI YOL", "(Diş Hekimliği Öğrencileri · Diş Hekimleri)"),
        P("ABD’de yurt dışı diplomasının doğrudan “tanınması” (denklik) diye bir yol "
          "yoktur. Bunun yerine, hedefe ve profile göre **üç farklı rota** izlenir. Üçünün "
          "de **ilk dört adımı ortaktır;** ayrım beşinci adımda başlar."),
        BOX("**Hangi yol size uygun?** Sadece genel diş hekimi olarak çalışmak istiyorsanız "
            "asıl yol **1. Yol**’dur. Türkiye’de zaten bir uzmanlığınız varsa ya da ABD’de "
            "belirli bir dalda uzmanlaşmak istiyorsanız **2. Yol** mantıklıdır. Belirli bir "
            "eyalete yerleşmeye hazırsanız ve hızlı bir genel lisans istiyorsanız **3. Yol** "
            "değerlendirilebilir, ancak en riskli yol budur."),
        BAR("YOLLARIN KARŞILAŞTIRMASI"),
        DL([
            ("1. Yol: Advanced Standing (CAAPID)",
             "CODA akreditasyonlu bir fakültede 2–3 yıllık program; sonunda ABD diploması "
             "(DDS/DMD) alınır. En geniş kabul gören ve her eyalette geçerli yoldur. "
             "Öğrenim ücreti sürecin en büyük kalemidir."),
            ("2. Yol: Uzmanlık Asistanlığı (ADEA PASS)",
             "Yeni bir DDS/DMD alınmaz; mevcut diplomayla doğrudan bir uzmanlık programına "
             "başvurulur. Asistanlıklar genellikle maaşlıdır. Ancak uzmanlık, çoğu eyalette "
             "genel lisans hakkı vermez."),
            ("3. Yol: AEGD / GPR Asistanlığı",
             "1–2 yıllık genel diş hekimliği asistanlığı. En kısa ve en ucuz görünen yoldur, "
             "ama yalnızca yaklaşık 16 eyalet kabul eder ve lisans genelde o eyalete bağlı "
             "kalır."),
        ]),
        BOX("**Üçünde de değişmeyen tek şart INBDE’dir.** Tüm eyalet lisans otoriteleri bu "
            "sınavı ister; alternatif rotalar bile INBDE’yi sürecin parçası olarak kabul eder."),
    ],
    # -- ortak adımlar -------------------------------------------------------
    [
        H1("ORTAK İLK ADIMLAR", "(Her Üç Yol İçin)"),
        P("Türkiye’de 5 yıllık Diş Hekimliği Fakültesi’ni bitirmiş bir hekim için ilk dört "
          "adım, seçilen yoldan bağımsız olarak aynıdır. Yola özgü kısım bu adımlardan sonra "
          "başlar."),
        BAR("GÜNCEL BİLGİLER (2026)"),
        UL([
            "**Ocak 2026’dan** itibaren TOEFL iBT, eski 0–120 ölçeği yerine **1–6 bant "
            "ölçeği** kullanıyor; programların baraj puanları buna göre güncelleniyor.",
            "**CDCA-WREB-CITA ile ADEX 2026’da birleşti;** klinik lisans sınavı tek çatı "
            "altında yürütülüyor.",
            "**1 Ağustos 2026’dan** itibaren periodontal bölüm ADEX sınavının **zorunlu "
            "parçası** oldu.",
        ]),
        BAR("1. DENTPIN NUMARASI"),
        P("Sürecin ilk somut adımı. Tüm sınav ve başvurular için gereken **kişisel diş "
          "hekimliği kimlik numarasıdır.** ADA’nın sitesinden **ücretsiz** ve anında alınır. "
          "Daha önce DAT / NBDE / INBDE için alınmışsa mevcuttur."),
        BAR("2. DİPLOMA DEĞERLENDİRMESİ (ECE / WES)"),
        P("Bu adım **erken başlatılmalıdır;** hem INBDE’ye girmek hem de programlara "
          "başvurmak için gereklidir. Türkiye’deki diploma, transkript ve ilgili belgeler "
          "değerlendirme kuruluşuna gönderilir."),
        UL([
            "**Rapor türü: Course-by-Course** (ders ders) rapor alınmalıdır; General rapor "
            "yetersiz kalır.",
            "Hedeflenen programların **ECE mi WES mi** istediği önceden kontrol edilmelidir.",
            "**Süre:** belge hazırlığıyla birlikte birkaç hafta; başvuru sonrası genelde 1–3 "
            "hafta içinde yanıt gelir.",
        ]),
    ],
    [
        BAR("3. İNGİLİZCE YETERLİLİĞİ (TOEFL)"),
        P("Ana dili İngilizce olmayan Türkiye mezunları için zorunludur; programların büyük "
          "kısmı **TOEFL** ister (bazıları IELTS de kabul eder). Puan barajı programdan "
          "programa değişir."),
        BOX("**2026 değişikliği:** 21 Ocak 2026’dan itibaren TOEFL iBT, eski 0–120 ölçeği "
            "yerine **1–6 bant ölçeği** kullanıyor. Programların baraj puanları da bu yeni "
            "ölçeğe göre güncelleniyor; birçok fakülte **eski ölçekte 100+ puana denk** bir "
            "seviye bekler. Skorlar genellikle **2 yıl** geçerlidir."),
        BAR("4. INBDE: ULUSAL BOARD SINAVI"),
        P("Sürecin **tartışılmaz eşiğidir.** INBDE, JCNDE tarafından yürütülen ve eski NBDE "
          "Part I–II’nin yerini alan **tek ve bütünleşik** ulusal sınavdır; temel bilimler ile "
          "klinik konuları bir arada ölçer. Tüm eyalet lisans otoriteleri bu sınavı şart koşar."),
        UL([
            "**Uygunluk:** Türkiye’de diplomasını ve varsa zorunlu stajını tamamlamış hekim "
            "başvurabilir.",
            "**Format:** iki günlük, bilgisayarlı sınav; **pass/fail** olarak puanlanır.",
            "**Nerede:** yalnızca ABD ve Kanada’daki **Prometric** merkezlerinde; Türkiye’den "
            "girilemez.",
            "**Hak:** ilk beş denemede ya da ilk denemeden sonraki beş yılda geçilmelidir; "
            "sonrasında yılda bir kez girilebilir.",
        ]),
    ],
    # -- 1. yol --------------------------------------------------------------
    [
        H1("1. YOL: ADVANCED STANDING", "(CAAPID · DDS / DMD)"),
        P("Bu yolda aday, **CODA akreditasyonlu** bir ABD diş hekimliği fakültesinde Advanced "
          "Standing programını tamamlayıp bir **ABD diploması (DDS/DMD)** alır. Sürecin nihai "
          "hedefi bu diploma ve bir eyaletten alınan **çalışma lisansıdır (state license).**"),
        P("Üç yol arasında **en geniş kabul göreni** budur: alınan diploma her eyalette "
          "geçerlidir ve lisans yolunda ek bir eyalet kısıtı getirmez."),
        BAR("CAAPID BAŞVURUSU"),
        P("Başvuru **ADEA CAAPID** üzerinden yapılır: diploma değerlendirmesi, referans "
          "mektupları, INBDE ve TOEFL sonuçları, kişisel niyet mektubu (personal statement) ve "
          "fakülteye özel ek belgeler bu portal üzerinden iletilir."),
        P("Programlar **rekabetçidir.** Birçok fakülte, seçtiği adayları uygulamalı bir beceri "
          "sınavına (**bench test**) ve **mülakata** çağırır; bazı programlar video mülakat "
          "(ör. Kira Talent) da kullanır."),
        SUB("Başvuru ücretleri (2026–27):"),
        UL([
            "**ADEA CAAPID:** ilk program için **264 USD**, her ek program için **115 USD.**",
            "Ayrıca **fakülteye özel ek başvuru ücretleri** ve bench test ücretleri olabilir.",
        ]),
    ],
    [
        BAR("PROGRAM VE DİPLOMA"),
        P("Kabul alan aday, CODA akreditasyonlu fakültede genellikle **2–3 yıl** süren "
          "programa başlar. Program çoğu zaman yoğun bir hazırlık/oryantasyon dönemiyle "
          "açılır; ardından aday, dört yıllık DDS/DMD müfredatının **ileri sınıflarına "
          "entegre** olur."),
        P("Programların **kontenjanları sınırlıdır** ve öğrenim ücretleri fakülteden fakülteye "
          "önemli ölçüde değişir; bu, sürecin planlanmasında dikkate alınması gereken **en "
          "büyük maliyet kalemidir.**"),
        STATS([("2–3 yıl", "Program süresi"), ("264 USD", "CAAPID ilk başvuru"),
               ("DDS / DMD", "Alınan ABD diploması")]),
        BAR("VİZE VE KABUL KOŞULLARI"),
        P("Bazı programlar ABD vatandaşlarını veya daimi ikamet sahiplerini tercih eder ya da "
          "şart koşar; buna karşılık birçok fakülte uluslararası adayları kabul eder ve **F-1 "
          "öğrenci vizesi sponsorluğu** sunar. Doğru fakülte seçimi bu nedenle önemlidir."),
    ],
    # -- 2. yol --------------------------------------------------------------
    [
        H1("2. YOL: UZMANLIK REZİDANSLIĞI", "(ADEA PASS)"),
        P("Bu yolda aday ABD’de yeni bir DDS/DMD diploması almaya çalışmaz. Bunun yerine, "
          "**mevcut diplomasıyla doğrudan bir uzmanlık (postdoctoral / residency) programına** "
          "başvurur. Başvuru CAAPID’den değil, uzmanlık başvurularının merkezî portalı olan "
          "**ADEA PASS** üzerinden yapılır."),
        BOX("**İki farklı “PASS” karıştırılmamalı. ADEA PASS:** uzmanlık başvurularının "
            "yapıldığı merkezî portal: bu bölümün konusu budur. **UMN / Penn “PASS”:** bazı "
            "üniversitelerin Advanced Standing programına verdiği okula özel isim; o, 1. Yol’a "
            "aittir ve uzmanlık değildir."),
        BAR("TANINAN UZMANLIK DALLARI"),
        P("ABD’de ADA tarafından tanınan uzmanlık dalları sınırlı ve nettir:"),
        UL([
            "**Endodontics** (Endodonti) · **Orthodontics & Dentofacial Orthopedics** "
            "(Ortodonti) · **Periodontics** (Periodontoloji)",
            "**Prosthodontics** (Protez) · **Pediatric Dentistry** (Pedodonti) · **Oral & "
            "Maxillofacial Surgery** (Ağız, Diş ve Çene Cerrahisi)",
            "**Oral & Maxillofacial Pathology** (Patoloji) · **Oral & Maxillofacial "
            "Radiology** (Radyoloji) · **Dental Public Health** (Toplum Ağız Diş Sağlığı)",
        ]),
    ],
    [
        BAR("BAŞVURU, MÜLAKAT VE MATCH"),
        P("İlk dört ortak adım tamamlandığında aday doğrudan uzmanlık programlarına "
          "başvurabilir. **ADEA PASS Program Search Engine**, hangi programın uluslararası "
          "aday kabul ettiğini ve uygunluk şartlarını listeler; uluslararası başvuru kabul "
          "eden programların tek bir toplu listesi yoktur."),
        P("Bazı dallar ayrıca **Dental Match** sistemine tabidir. Match, adayları programlara "
          "yerleştiren **ayrı ve bağımsız** bir süreçtir; Match kullanan bir dala başvuran "
          "aday hem PASS’te başvuru yapar hem de natmatch.com üzerinden Match’e kaydolur."),
        UL([
            "**Faz I:** Ortodonti, Periodontoloji, Protez, Anestezi (ayrıca AEGD ve GPR).",
            "**Faz II:** Çene Cerrahisi (OMS), Pedodonti.",
            "Programların büyük kısmı **INBDE’nin geçilmiş olmasını** bekler; rekabetin büyük "
            "bölümü bu sınavı vermiş olarak başvurur.",
        ]),
        P("Kabul alındığında aday, seçtiği dalda ileri eğitim görür. Süre dala göre değişir: "
          "**genellikle 2–4 yıl;** cerrahi gibi dallar daha uzundur."),
    ],
    [
        BAR("UZMANLIK VE LİSANS İLİŞKİSİ"),
        P("Bu, uzmanlık yolunun **en kritik ayrımıdır.** Akredite bir okuldan DDS/DMD derecesi "
          "yoksa, yalnızca bir ileri düzey diş eğitimi programını tamamlamak **eyaletlerin "
          "çoğunda genel diş hekimliği lisansı için eğitim şartını karşılamaz.**"),
        P("Buna karşılık **bazı eyaletler** tamamlanmış bir uzmanlık asistanlığını genel "
          "lisans yolunda kabul eder. En somut örnek **Texas**’tır: Texas Dental Board, en az "
          "iki yıllık, CODA akreditasyonlu bir uzmanlık programını tamamlamış olmayı tanır. Bu "
          "durumda **uzmanlık → klinik sınav → genel lisans** zinciri mümkündür."),
        BOX("**Texas AEGD/GPR’yi bu amaçla kabul etmez.** Texas’ın kabul ettiği yalnızca "
            "tanınmış uzmanlık dallarıdır. Bu, 2. Yol ile 3. Yol arasındaki en önemli farktır."),
        BAR("MALİYET AVANTAJI"),
        P("Uzmanlık asistanlıkları **genellikle maaşlı pozisyonlardır** ve bazı programlarda "
          "öğrenim ücreti alınmaz. Bu, 1. Yol’un yüz binlerce dolarlık öğrenim ücretinden "
          "temel bir farktır: bu yolda aday öğrenirken kazanabilir. Ancak bu program bazında "
          "değişir; her programın kendi ücret ve maaş yapısı doğrulanmalıdır."),
        P("Başvuru aşaması: **ADEA PASS** ilk program **199 USD**, her ek program **92 USD** "
          "(2026–27). Buna ECE (~199 USD), TOEFL (~185–475 USD) ve INBDE (~1.325–1.525 USD) "
          "eklenir."),
    ],
    # -- 3. yol --------------------------------------------------------------
    [
        H1("3. YOL: AEGD / GPR REZİDANSLIĞI", "(Eyalet Bazlı Lisans)"),
        P("Bazı eyaletlerin lisans yönetmelikleri **DDS/DMD derecesi şart koşmaz;** yalnızca "
          "CODA akreditasyonlu bir programın tamamlanmasını yeterli sayar. **AEGD** (Advanced "
          "Education in General Dentistry) ve **GPR** (General Practice Residency), genel diş "
          "hekimliğinde **1–2 yıllık** ileri eğitim programlarıdır ve tam bu boşluğa oturur."),
        BOX("**Bu yol “ucuz kestirme” değildir: en riskli yoldur.** İlk bakışta en hızlı ve "
            "en ucuz görünür, ama her şey **eyalet seçimine** bağlıdır: yalnızca belirli "
            "eyaletler bu yolu tanır, bazı eyaletler AEGD’yi özellikle reddeder ve alınan "
            "lisans genelde o eyalete bağlı kalır. Yanlış eyaleti seçen aday, bitirdiği "
            "asistanlığı lisansa hiç çeviremeyebilir."),
        BAR("AEGD İLE GPR ARASINDAKİ FARK"),
        DL([
            ("AEGD: Advanced Education in General Dentistry",
             "Genel diş hekimliği becerilerini ileri düzeyde geliştiren program. Klinik diş "
             "hekimliği pratiğine odaklanır; genelde diş fakültesi / dental okul ortamında "
             "yürütülür."),
            ("GPR: General Practice Residency",
             "Genel diş hekimliği asistanlığı. Hastane ortamında yürütülür; tıbbi açıdan "
             "karmaşık hastalar ve acil bakım dâhil daha geniş bir yelpazeyi kapsar."),
        ]),
        P("Hangi program seçilirse seçilsin **CODA akreditasyonu pazarlık edilemez bir "
          "gerekliliktir.** CODA onaylı olmayan bir programı bitirmek bu yolda hiçbir işe "
          "yaramaz."),
    ],
    [
        BAR("HANGİ EYALETLER BU YOLU KABUL EDİYOR?"),
        P("Bu yolun kalbi eyalet seçimindedir. Derlemelere göre yabancı eğitimli diş hekimleri "
          "için AEGD/GPR yolunu kabul eden **yaklaşık 16 eyalet** vardır:"),
        UL([
            "**Batı / Kuzeybatı:** Alaska, Oregon, Washington",
            "**Orta Batı:** Illinois, Iowa, Minnesota, Ohio",
            "**Güney:** Arkansas, Kentucky, Louisiana, Mississippi, North Carolina, Virginia, "
            "West Virginia",
            "**Kuzeydoğu:** Connecticut, Vermont",
        ]),
        P("**Connecticut** somut bir örnektir: CODA onaylı **en az 12 aylık** bir GPR veya "
          "AEGD programının tamamlanması esasına dayalı lisans verir. Yani bir yıllık bir "
          "asistanlık, doğru eyalette lisans yolunu açabilir."),
        BOX("**Liste sabit değildir.** Kurallar değişir ve ayrıntıda farklılaşır; tam şartlar "
            "her zaman ilgili eyalet diş kurulundan **yazılı olarak** teyit edilmelidir."),
    ],
    [
        BAR("KAPALI OLAN EYALETLER"),
        P("“Asistanlık bitiren her yerde lisans alır” düşüncesi yanlıştır. Her eyalet "
          "eğitimin nasıl olması gerektiğini kendi belirler; bazı eyaletler “AEGD olmalı” "
          "derken bazıları **“AEGD olamaz”** der."),
        UL([
            "**Texas:** GPR ve AEGD programlarını bölgesel klinik sınav yerine geçer olarak "
            "tanımaz. Texas’ta bu yol genel lisans için **kapalıdır.**",
            "**New York:** AEGD/GPR yolunu genel lisansın yerine kabul etmez; advanced "
            "standing CODA DDS/DMD gereklidir.",
        ]),
        BAR("TÜRK DİPLOMASINA ÖZEL: 5 YIL / 6 YIL"),
        P("Türkiye’de diş hekimliği eğitimi **5 yıldır.** Bazı eyaletler ise toplam **6 yıllık** "
          "eğitim ister; bu fark başvuruyu doğrudan etkileyebilir. **New York** örneğinde, "
          "advanced standing programından önce 1 yıl pre-professional + 5 yıl professional "
          "olmak üzere 6 yıllık eğitim aranır."),
        P("Bu durumda ya lisans döneminden ek yıl belgelenmeli ya da **6 yıl şartı olmayan bir "
          "eyalet** hedeflenmelidir. Hedef eyaletin yalnızca “AEGD/GPR kabul ediyor mu” "
          "değil, **“kaç yıllık eğitim istiyor”** sorusu da baştan araştırılmalıdır."),
    ],
    # -- ortak son adım ------------------------------------------------------
    [
        H1("KLİNİK SINAV VE EYALET LİSANSI", "(Her Üç Yolun Ortak Sonu)"),
        P("Hangi yol izlenirse izlensin, lisans için bir **klinik yeterlilik sınavı** gerekir. "
          "En yaygın kabul gören sınav **ADEX**’tir: manken (**CompeDont**) üzerinde uygulamalı "
          "el-beceri bölümleri ile bilgisayar tabanlı **DLOSCE** bölümünden oluşur."),
        P("**ADEX’e yalnızca CODA / CDAC akreditasyonlu bir programdan mezun olanlar "
          "girebilir.** Bu, 2. ve 3. Yol’da (ABD diploması alınmadığı için) doğrudan kritik "
          "bir kapıdır; hedef eyaletin hangi sınavı kabul ettiği baştan araştırılmalıdır."),
        P("ADEX dışında **CRDTS ve SRTA** gibi kurulların sınavları da bazı eyaletlerde kabul "
          "edilir. Hangi sınavın ve türün kabul edildiği **eyalete göre değişir.** "
          "CDCA-WREB-CITA ile ADEX 2026’da birleşmiştir; 1 Ağustos 2026’dan itibaren "
          "periodontal bölüm ADEX sınavının **zorunlu parçası** olmuştur."),
        BAR("EYALET LİSANSI (STATE LICENSURE)"),
        P("Son adım, çalışılmak istenen eyaletin diş hekimliği kuruluna lisans başvurusudur. "
          "ABD’de **tek bir ulusal lisans olmadığı için** başvuru her eyalete ayrı yapılır. "
          "Çoğu eyalet ayrıca o eyalete özel bir **hukuk/etik (jurisprudence) sınavı** ister; "
          "bazı eyaletler (ör. New York) klinik sınav yerine ya da ek olarak **PGY-1 "
          "residency** tamamlanmasını şart koşar."),
        BOX("ABD’de lisans işlemleri **eyaletlere göre** yürütülür; kabul edilen sınavlar, "
            "belgeler, ücretler ve koşullar eyaletten eyalete farklılık gösterir. Kesin bilgi "
            "için hedeflenen eyaletin diş hekimliği kurulu esas alınmalıdır."),
    ],
    # -- hizmetler -----------------------------------------------------------
    [
        H1("HİZMETLERİMİZ", "(ABD: ÜÇ YOL)"),
        P("DENTCAMP, ABD sürecini; ABD sağlık ve eğitim sistemine uygun şekilde **planlı, "
          "sürdürülebilir ve kontrollü bir geçiş süreci** olarak ele alır. Sunulan destek, "
          "sürecin her aşamasında doğru adımı doğru sırayla atmayı sağlayacak **mentörlük ve "
          "yönlendirme** üzerine kuruludur."),
        P("ABD’de **yol seçimi ve eyalet stratejisi**, sonucu diğer ülkelerden çok daha fazla "
          "etkiler; bu nedenle süreç yol seçimiyle başlar."),
        BAR("1. PROFİL ANALİZİ & YOL SEÇİMİ"),
        P("Mentörler tarafından yapılan **iki online görüşme** sonrasında; adayın mevcut "
          "eğitim durumu, Türkiye’deki uzmanlığı (varsa), klinik deneyimi, vize/ikamet durumu "
          "ve hedefleri doğrultusunda **üç yoldan hangisinin uygun olduğu** belirlenir."),
        P("Bu aşamada TOEFL ve INBDE’nin ne zaman tamamlanacağı, hangi programlara hangi "
          "sırayla başvurulacağı ve, eyalet bazlı yollarda, **hangi eyaletin hedefleneceği** "
          "net bir yol haritası üzerinden planlanır."),
    ],
    # DİL YETERLİLİĞİ HİZMET BÖLÜMÜ YOK (2 Eylül 2026, kullanıcı): DENTCAMP ABD
    # sürecinde dil eğitimi/desteği sağlamıyor. Dil ŞARTI değişmedi, mevzuat
    # bölümündeki "3. İNGİLİZCE YETERLİLİĞİ (TOEFL)" aynen duruyor; kalkan yalnız
    # HİZMETLERİMİZ altındaki eğitim bloğu. Bölümler yeniden numaralandı.
    [
        BAR("2. INBDE MENTÖRLÜĞÜ"),
        P("Ulusal board sınavı INBDE için mentörlük desteği sunulur. **Sınavın yapısı, çalışma "
          "stratejisi, kaynak seçimi ve zaman planlaması** konularında; ABD sürecini bilen "
          "mentörler adaya birebir yönlendirme sağlar. Sınav yalnızca ABD ve Kanada’da "
          "yapıldığı için **seyahat planlaması** da sürece dâhil edilir."),
        BAR("3. BAŞVURU DOSYASI YÖNETİMİ (CAAPID / ADEA PASS)"),
        P("Seçilen yola göre **CAAPID** ya da **ADEA PASS** başvurusu hazırlanır. Denklik "
          "değerlendirmesi (ECE/WES), referans mektupları, kişisel niyet mektubu ve programa "
          "özel belgeler; ABD kurumlarının beklentilerine uygun şekilde düzenlenir. **Program "
          "filtreleme** (uluslararası aday kabulü, vize sponsorluğu), **başvuru sıralaması, "
          "bench test ve mülakat hazırlığı** ile, gerekiyorsa, **Match kaydı** planlanır."),
        BAR("4. EYALET STRATEJİSİ & LİSANS YÖNLENDİRMESİ"),
        P("Eyalet bazlı yollarda (2. ve 3. Yol) **hedef eyaletin kuralları baştan araştırılır:** "
          "AEGD mi GPR mi kabul ediliyor, kaç aylık program isteniyor, eğitim yılı şartı var mı, "
          "hangi klinik sınav aranıyor. Adayın hedef eyalet diş kurulundan **yazılı teyit** "
          "alması konusunda yönlendirilir. Klinik sınav (ADEX + DLOSCE), jurisprudence sınavı "
          "ve lisans başvurusu adımlarında da destek sağlanır."),
    ],
    whatsapp_and_mentorship(ULKE, [
        "Konaklama ve ev kiralama",
        "Sağlık sigortası ve ulaşım",
        "Banka hesabı ve resmî işlemler",
        "Yaşam düzeni ve şehir adaptasyonu",
    ]),
    # -- kavramlar -----------------------------------------------------------
    [
        H1("KAVRAMLAR & TERİMLER", "(ABD)"),
        P("ABD’de diş hekimliği sürecinde sıkça karşılaşılan bazı kavramlar ilk etapta kafa "
          "karıştırıcı olabilir. Aşağıda üç yol kapsamında en çok karşılaşılan temel terimler "
          "sade şekilde açıklanmıştır."),
        DL([
            ("DENTPIN",
             "Kişisel diş hekimliği kimlik numarasıdır. Tüm sınav ve başvurular için ilk "
             "alınması gereken numaradır; ADA sitesinden ücretsiz alınır."),
            ("CODA (Commission on Dental Accreditation)",
             "ABD’de diş hekimliği programlarını akredite eden kurumdur. Hangi yol izlenirse "
             "izlensin, girilecek programın CODA akreditasyonlu olması zorunludur."),
            ("INBDE (Integrated National Board Dental Examination)",
             "ABD ulusal diş hekimliği board sınavıdır; JCNDE tarafından yürütülür. Eski NBDE "
             "Part I–II’nin yerini almıştır. Üç yolda da zorunludur."),
            ("ECE / WES",
             "Yurt dışı diploma ve transkriptleri ders-ders değerlendiren kuruluşlardır. "
             "Course-by-Course rapor gerekir; General rapor yetersizdir."),
            ("Advanced Standing Program",
             "Yurt dışında eğitim almış adayların, CODA akreditasyonlu bir ABD fakültesinde "
             "2–3 yılda ABD diploması (DDS/DMD) almasını sağlayan programdır. 1. Yol."),
            ("ADEA CAAPID",
             "Advanced Standing programlarına başvurunun yapıldığı merkezî portaldır."),
            ("ADEA PASS",
             "Postdoctoral Application Support Service: uzmanlık ve asistanlık "
             "başvurularının yapıldığı merkezî portal. Bir program değil, bir başvuru "
             "sistemidir. 2. ve 3. Yol’da kullanılır."),
            ("Dental Match",
             "Asistanlık eşleştirme sistemidir (natmatch.com). PASS’ten ayrı ve bağımsız "
             "çalışır; bazı uzmanlık dalları buna tabidir."),
            ("AEGD / GPR",
             "Genel diş hekimliğinde 1–2 yıllık mezuniyet sonrası eğitim programlarıdır. AEGD "
             "okul/klinik odaklı, GPR hastane odaklıdır. 3. Yol’un temelidir."),
            ("Bench Test",
             "Bazı fakültelerin, seçtiği adayları çağırdığı uygulamalı el-beceri sınavıdır; "
             "genellikle mülakatla birlikte yapılır."),
            ("DDS / DMD",
             "İkisi de aynı değerde ABD diş hekimliği diplomasıdır; yalnızca isimleri "
             "farklıdır ve lisans açısından eşdeğerdir."),
            ("ADEX / DLOSCE",
             "En yaygın kabul gören klinik lisans sınavı ADEX’tir; manken (CompeDont) üzerinde "
             "uygulamalı bölümler ile bilgisayar tabanlı DLOSCE’den oluşur."),
            ("State License (Eyalet Lisansı)",
             "ABD’de tek bir ulusal lisans yoktur; her eyaletin kendi kurulu ve kuralları "
             "vardır. Başvuru her eyalete ayrı yapılır."),
            ("Jurisprudence Sınavı",
             "Çoğu eyaletin istediği, o eyalete özel hukuk ve etik sınavıdır."),
        ]),
    ],
    # -- SSS -----------------------------------------------------------------
    [
        H1("SIK SORULAN SORULAR", "(ABD)"),
        DL([
            ("Hangi yol bana uygun?",
             "Sadece genel diş hekimi olarak çalışmak istiyorsanız 1. Yol (Advanced Standing). "
             "Türkiye’de uzmanlığınız varsa ya da ABD’de bir dalda uzmanlaşmak istiyorsanız 2. "
             "Yol. Belirli bir eyalete yerleşmeye hazırsanız ve hızlı genel lisans "
             "istiyorsanız 3. Yol değerlendirilebilir. Bu seçim mentörünüzle birlikte "
             "yapılır."),
            ("Bu süreç ne kadar sürer?",
             "Yola göre değişir. Advanced Standing programları 2–3 yıl, uzmanlık 2–4 yıl, "
             "AEGD/GPR 1–2 yıldır; buna hazırlık, başvuru ve sonrasında klinik sınav/lisans "
             "adımları eklenir."),
            ("DENTCAMP’ten ne kadar süre faydalanabilirim?",
             "Sürece hâkimiz ve bir yıl sınırı koymuyoruz. Hedefiniz olan ABD’de diş "
             "hekimliğine başlayana kadar, süreç kesintisi olmadan yanınızda oluruz."),
            ("Diplomam ABD’de otomatik olarak tanınır mı?",
             "Hayır. ABD’de yurt dışı diplomanın doğrudan tanınması diye bir yol yoktur; üç "
             "rotadan biri izlenir."),
            ("INBDE’ye Türkiye’den girebilir miyim?",
             "Hayır. INBDE yalnızca ABD ve Kanada’daki Prometric merkezlerinde yapılır. "
             "Seyahat planlaması sürecin parçasıdır."),
            ("Uzmanlık bitirince otomatik genel lisans alır mıyım?",
             "Hayır, çoğu eyalette almazsınız. Akredite bir okuldan DDS/DMD yoksa, tek başına "
             "uzmanlık programı genel lisans için eğitim şartını karşılamaz. Texas gibi bazı "
             "eyaletler uzmanlığı kabul eder; hedef eyaletin kuralı baştan araştırılmalıdır."),
            ("AEGD/GPR yolu neden riskli?",
             "Çünkü her şey eyalet seçimine bağlıdır. Yalnızca yaklaşık 16 eyalet bu yolu "
             "tanır, Texas ve New York gibi büyük pazarlar genel lisans için kapatmıştır ve "
             "alınan lisans genelde o eyalete bağlı kalır. Yanlış eyalette bitirilen "
             "asistanlık lisansa dönüşmeyebilir."),
            ("AEGD ile GPR arasındaki fark nedir?",
             "AEGD daha çok okul/klinik odaklı, GPR daha çok hastane/tıbbi odaklıdır. Lisans "
             "açısından çoğu eyalet ikisini de kabul eder, ama hangi eyaletin hangisini kabul "
             "ettiği değişir: bazı eyaletler AEGD’yi özellikle reddeder."),
        ]),
        # SSS 942pt: tek sayfaya sığmıyor. Dengeli bölünme için alt başlık.
        BAR("EĞİTİM, MALİYET VE LİSANS"),
        DL([
            ("Türkiye’deki 5 yıllık eğitimim sorun olur mu?",
             "Çoğu eyalette olmaz. Ancak bazı eyaletler toplam 6 yıllık eğitim ister (ör. New "
             "York). Bu durumda ya ek yıl belgelenmeli ya da 6 yıl şartı olmayan bir eyalet "
             "hedeflenmelidir."),
            ("Hangi yol daha ucuz?",
             "Uzmanlık ve AEGD/GPR asistanlıkları genellikle maaşlıdır ve çoğunda öğrenim "
             "ücreti alınmaz; Advanced Standing’in öğrenim ücreti ise sürecin en büyük "
             "kalemidir. Ancak ucuz olan yol, ancak doğru eyalette anlam kazanır."),
            ("Öğrenciyim, mezuniyetime daha var, erken mi başladım?",
             "Hayır. Öğrenciyken sürece başlamak, özellikle TOEFL ve INBDE hazırlığı açısından "
             "büyük avantaj sağlar. Resmî başvurular mezuniyet ve diploma sonrası yapılır."),
            ("Süreç ne kadar maliyetli?",
             "Yola göre değişir. Ortak kalemler: ECE ~199 USD, TOEFL ~185–475 USD, INBDE "
             "~1.325–1.525 USD. Başvuru: CAAPID ilk program 264 USD + her ek program 115 "
             "USD; ADEA PASS ilk program 199 USD + her ek program 92 USD. En büyük kalem "
             "Advanced Standing öğrenim ücretidir ve fakülteden fakülteye önemli ölçüde "
             "değişir; uzmanlık ve AEGD/GPR asistanlıkları ise genellikle maaşlıdır. "
             "Kişiye özel bütçe planı mentörünüzle birlikte çıkarılır."),
            ("Sınavları geçmek iş garantisi verir mi?",
             "Hayır. INBDE’yi geçmek ve lisans almak ABD’de yasal olarak çalışabilmenizi "
             "sağlar; otomatik bir iş garantisi vermez. Klinik ve program başvuruları ayrı "
             "bir süreçtir ve DENTCAMP bu adımda da yönlendirme sağlar."),
            ("Hangi denklik değerlendirme kuruluşu geçerli?",
             "En çok kabul edilen kuruluşlar ECE ve WES’tir. Hangisinin kabul edildiği "
             "başvurulan programa göre değişir; değerlendirmeyi yaptırmadan önce hedef "
             "programın kuralı kontrol edilmelidir."),
            ("ABD’de tek bir ulusal lisans var mı?",
             "Hayır. Her eyaletin kendi kurulu ve kuralları vardır; lisans başvurusu her "
             "eyalete ayrı yapılır. Eyaletler arası geçiş giderek yaygınlaşsa da otomatik "
             "değildir."),
        ]),
    ],
]

# Üç yol için üç ayrı şema. İlk üç adım her üçünde de aynı — ayrım 4. adımda
# başlıyor; okuyucu ortak gövdeyi ve nerede ayrıldığını yan yana görüyor.
_ORTAK = [
    (1, "DENTPIN &amp;<br>Diploma Değerlendirmesi", "ECE / WES: Course-by-Course",
     "Erken başlatılmalı", "ic_belge.png"),
    (2, "İngilizce Yeterliliği", "TOEFL iBT: 1–6 ölçeği",
     "Skorlar 2 yıl geçerli", "ic_dil.png"),
    (3, "INBDE", "Ulusal board sınavı: pass/fail",
     "Yalnızca ABD/Kanada · üç yolda da şart", "ic_sinav.png"),
]

ROADMAPS = [
    ("1. YOL: ADVANCED STANDING", "CODA Fakültesinde ABD Diploması", _ORTAK + [
        (4, "CAAPID Başvurusu", "Referans + niyet mektubu",
         "Bench test ve mülakat", "ic_mentor.png"),
        (5, "Advanced Standing<br>Programı", "CODA fakültesi · 2–3 yıl",
         "ABD diploması (DDS / DMD)", "ic_muhur.png"),
        (6, "Klinik Sınav &amp;<br>Eyalet Lisansı", "ADEX + jurisprudence",
         "Her eyalette geçerli diploma", "ic_lisans.png"),
    ]),
    ("2. YOL: UZMANLIK REZİDANSLIĞI", "ADEA PASS ile Uzmanlık Programı", _ORTAK + [
        (4, "ADEA PASS Başvurusu", "Merkezî uzmanlık portalı",
         "Match dallarında ayrıca natmatch", "ic_mentor.png"),
        (5, "Uzmanlık Eğitimi", "Dala göre 2–4 yıl",
         "Genellikle maaşlı pozisyon", "ic_takvim.png"),
        (6, "Eyalet Lisansı", "Uzmanlığı kabul eden eyalet",
         "Uzmanlık = genel lisans DEĞİL", "ic_lisans.png"),
    ]),
    ("3. YOL: AEGD / GPR", "Eyalet Bazlı Asistanlık Yolu", _ORTAK + [
        (4, "ÖNCE Eyalet Stratejisi", "~16 eyalet bu yolu tanır",
         "Texas ve New York kapalı", "ic_ucak.png"),
        (5, "AEGD / GPR<br>Asistanlığı", "CODA akreditasyonlu · 1–2 yıl",
         "Genellikle maaşlı, öğrenim ücretsiz", "ic_butce.png"),
        (6, "Klinik Sınav &amp;<br>Eyalet Lisansı", "ADEX + jurisprudence",
         "Lisans o eyalete bağlı kalır", "ic_lisans.png"),
    ]),
]

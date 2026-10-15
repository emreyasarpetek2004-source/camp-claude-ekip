#!/usr/bin/env python3
"""DENTCAMP: İngiltere (GDC Registration Pathway).

Kaynak metin: BROŞÜR VE TANITIM/uk/Ingiltere_Dis_Hekimligi_Brosur.docx
Dil, AUSCAMP Specialist Pathway kataloğunun kurumsal register'ına çevrildi.
"""
from build import H1, BAR, P, SUB, UL, DL, BOX, STATS
from content._common import (intro, mentorler, placeholders,
                             whatsapp_and_mentorship, PHONES)   # noqa: F401

ULKE = "İngiltere"

COVER = {
    # Kapak alt bandındaki üç künye — hepsi katalogda zaten geçen bilgiler.
    "kunye": [
        ('YOL', 'ORE veya LDS'),
        ('ŞART', '1.600 klinik saat'),
        ('HEDEF', 'GDC kaydı'),
    ],
    "pill": "İngiltere’de",
    "title": "Diş Hekimliği\nKariyeri",
    "tag": "| GDC REGISTRATION",
    "sub": "(Diş hekimliği öğrencileri ve\ndiş hekimleri için süreç rehberi)",
}

INTRO = intro(ULKE)
MENTORLER_BOLUM = mentorler(ULKE)
MENTOR_YERI = 0        # kadro bu BODY bölümünden sonra: GDC REGISTRATION PATHWAY
MENTORS = placeholders(4, ULKE)

# --- Mentör ------------------------------------------------------------------
# İngiltere mentörü henüz belirlenmedi. Boş "?" kartı basmak yerine hiç kart
# basılmıyor; sayfa mentör ağının nasıl işlediğini anlatarak devam ediyor.
MENTOR_TAM = []


BODY = [
    [
        H1("GDC REGISTRATION PATHWAY", "(Diş Hekimliği Öğrencileri · Diş Hekimleri)"),
        P("GDC Registration Pathway, İngiltere’de diş hekimliği kariyerine adım atmak "
          "isteyenler için izlenen ana yoldur. Bu yol; **İngilizce yeterliliği, diploma "
          "tanınma durumunun tespiti, uygun sınav yolunun (ORE veya LDS) seçimi, başvuru ve "
          "belge yönetimi, sınavların geçilmesi ve GDC kaydı** adımlarının belirli bir sıra ve "
          "sistematik yapı içinde ilerlemesiyle tanımlanır."),
        P("Sürecin nihai hedefi, **GDC siciline kayıt olmak** ve İngiltere’de **gözetimsiz "
          "(bağımsız) çalışma yetkisi** kazanmaktır."),
        BOX("**Önemli:** İngiltere’de yurt dışı diplomanızın doğrudan tanınması (denklik) diye "
            "bir yol yoktur. Standart yol; **General Dental Council (GDC) siciline kayıt "
            "olmaktır.** Bunun için AB/EEA dışı adayların çoğu **ORE ya da LDS** sınavını "
            "geçmek zorundadır."),
        BAR("GÜNCEL BİLGİLER (2026)"),
        UL([
            "**6 Mayıs 2026’da** GDC, ORE’yi yeni sağlayıcı **UCL Consultants (UCLC)** ile "
            "yürütmeye başladı; ilk sınavlar Ağustos 2026’dan itibaren yapılıyor.",
            "**2026/27 ORE ücretleri** güncellendi: başvuru £115, Part 1 £485, Part 2 £6.967 "
            "(ORE ücretlerine artık KDV uygulanıyor).",
            "**LDS**, Safe Practitioner Framework’e göre yeniden yapılandırıldı; “unseen "
            "case“ bölümünün yerini Haziran 2026’dan itibaren **Structured Clinical "
            "Reasoning (SCR)** aldı.",
            "Hem ORE hem LDS’de **kapasite artırılıyor**; yine de talep yüksek ve slotlar "
            "açıldıktan kısa süre sonra doluyor.",
        ]),
    ],
    [
        BAR("1. İNGİLİZCE YETERLİLİĞİ (IELTS / OET)"),
        P("Adayın İngiltere’de klinik ve akademik ortamda İngilizceyi yeterli düzeyde "
          "kullanabildiğini kanıtlaması gerekir. GDC bunu genellikle **IELTS Academic** ya da "
          "**OET** ile belgeler. İstenen puan, geçerlilik süresi ve kabul edilen sınav türü "
          "GDC kurallarına göre değerlendirilir."),
        SUB("İngilizce seviyesi:"),
        UL([
            "**IELTS Academic**: genellikle genel **7.0** ve her bölümden (dinleme, okuma, "
            "yazma, konuşma) en az **6.5.**",
            "**OET**: dört bölümden **B notu** (alternatif olarak kabul edilir).",
            "Sertifika genellikle **son 2 yıl** içinde alınmış olmalıdır; güncel GDC kuralları "
            "esas alınır.",
        ]),
    ],
    [
        BAR("2. DİPLOMA TANINMA DURUMU & YOL SEÇİMİ"),
        P("Öncelikle diplomanın İngiltere’de doğrudan tanınıp tanınmadığı belirlenir. AB/EEA "
          "diplomaları belirli koşullarda **2028’e kadar** hızlı tanınabilir; AB dışı "
          "diplomaların çoğu doğrudan tanınmaz ve bir yeterlilik sınavı gerektirir."),
        P("Bu durumda iki ana yol vardır: **ORE veya LDS.** İkisi de GDC kaydı için **eşdeğer** "
          "kabul edilir; seçim, sınav takvimine, kapasiteye ve adayın güçlü olduğu sınav "
          "biçimine göre yapılır."),
    ],
    [
        BAR("3. BAŞVURU & BELGE YÖNETİMİ"),
        P("Diploma ve transkript, İngilizce yeterlilik belgesi, kimlik, referanslar ve "
          "**Certificate of Good Standing** gibi belgeler hazırlanır. AB dışı adaylardan "
          "ayrıca bir **ECCTIS / UK ENIC (NARIC)** denklik belgesi istenebilir."),
        SUB("Klinik deneyim & belgeler:"),
        UL([
            "**1.600 klinik saat**: hasta koltuğunda bizzat hasta tedavisi (ORE ve LDS için).",
            "**Certificate of Good Standing**: genellikle son 3 ay içinde düzenlenmiş olmalı.",
            "AB dışı adaylar için **ECCTIS / UK ENIC** denklik belgesi (NARIC statement) "
            "gerekebilir.",
        ]),
    ],
    [
        BAR("4. ORE: OVERSEAS REGISTRATION EXAMINATION"),
        P("ORE, GDC tarafından yürütülen **iki bölümlü** sınavdır. **Part 1**, klinik bilimler, "
          "insan hastalıkları, klinik diş hekimliği, hukuk, etik ve güvenlik konularını ölçen "
          "bilgisayar tabanlı yazılı bir sınavdır. **Part 2** ise manken üzerinde uygulamalı "
          "operatif testler, teşhis ve tedavi planlaması, tıbbi aciller ve OSCE tarzı "
          "istasyonlardan oluşan uygulamalı klinik sınavdır."),
        P("Her bölüm için **en fazla 4 deneme hakkı** vardır ve **Part 2, ilk Part 1 "
          "denemesinden itibaren 5 yıl içinde** geçilmelidir."),
        SUB("ORE ücretleri (2026/27):"),
        STATS([("£115", "Başvuru işlem ücreti"), ("£485", "Part 1: yazılı"),
               ("£6.967", "Part 2: uygulamalı")]),
        P("ORE ücretlerine artık **KDV uygulanmaktadır.** Rezervasyon **MyGDC** üzerinden "
          "yapılır; slotlar açıldıktan kısa süre sonra dolabilir."),
    ],
    [
        BAR("5. LDS: LICENCE IN DENTAL SURGERY (ALTERNATİF)"),
        P("LDS, **RCS England** tarafından verilen ve ORE’ye alternatif olan sınavdır; GDC "
          "kaydı için **eşdeğer** kabul edilir. 2026 itibarıyla **üç bölümlü** bir yapıya "
          "sahiptir ve **Safe Practitioner Framework**’e göre yürütülür."),
        P("Part 2’deki “unseen case” bölümünün yerini **Haziran 2026’dan itibaren Structured "
          "Clinical Reasoning (SCR)** almıştır. RCS England, 2026’da **1.000 Part 1 "
          "kontenjanı**, 2027’de ise yılda **2.000 kontenjan** sunmayı planlamaktadır."),
    ],
    [
        BAR("6. GDC KAYDI (REGISTRATION)"),
        P("Sınav(lar) başarıyla tamamlandıktan sonra son adım **GDC siciline kayıttır.** Kayıt "
          "için kimlik doğrulaması, iyi hâl (good standing) kontrolleri, **mesleki sorumluluk "
          "sigortası (indemnity)** ve kayıt ücretlerinin ödenmesi gerekir."),
        P("Başvuru onaylandığında isminiz GDC sicilinde yer alır ve İngiltere’de **gözetimsiz "
          "olarak diş hekimliği yapabilirsiniz.**"),
        BOX("İngiltere’de kayıt işlemleri ve sınav kuralları **GDC** ve **RCS England** "
            "tarafından belirlenir; kabul edilen sınavlar, belgeler, ücretler ve bazı koşullar "
            "zamanla değişebilir. Kesin bilgi için bu kurumların güncel duyuruları esas "
            "alınmalıdır."),
    ],
    [
        H1("HİZMETLERİMİZ", "(GDC REGISTRATION PATHWAY)"),
        P("DENTCAMP, GDC Registration Pathway sürecini; İngiltere sağlık ve eğitim sistemine "
          "uygun şekilde **planlı, sürdürülebilir ve kontrollü bir geçiş süreci** olarak ele "
          "alır. Sunulan destek, sürecin her aşamasında doğru adımı doğru sırayla atmayı "
          "sağlayacak **mentörlük ve yönlendirme** üzerine kuruludur."),
        P("Bu süreçte **yol seçimi (ORE / LDS), slot planlaması ve belge yönetimi** sonucu "
          "doğrudan etkileyen unsurlardır."),
        BAR("1. PROFİL ANALİZİ & YOL PLANI"),
        P("Mentörler tarafından yapılan **iki online görüşme** sonrasında; adayın mevcut eğitim "
          "durumu, klinik deneyimi, vize/ikamet durumu ve hedefleri doğrultusunda izlenecek "
          "adımlar belirlenir. İngilizce sınavının ne zaman tamamlanacağı, **ORE mi yoksa LDS "
          "yolunun mu** seçileceği ve tüm sürecin nasıl ilerleyeceği net bir yol haritası "
          "üzerinden planlanır."),
    ],
    # DİL YETERLİLİĞİ HİZMET BÖLÜMÜ YOK (2 Eylül 2026, kullanıcı): DENTCAMP İngiltere
    # sürecinde dil eğitimi/desteği sağlamıyor. Dil ŞARTI değişmedi, mevzuat
    # bölümündeki "1. İNGİLİZCE YETERLİLİĞİ (IELTS / OET)" aynen duruyor; kalkan
    # yalnız HİZMETLERİMİZ altındaki eğitim bloğu. Bölümler yeniden numaralandı.
    [
        BAR("2. ORE / LDS SINAV MENTÖRLÜĞÜ"),
        P("Seçilen yola göre ORE ya da LDS için mentörlük desteği sunulur. **Sınavın yapısı, "
          "çalışma stratejisi, kaynak seçimi, Part 1 / Part 2 (ve LDS’de üç bölüm) planlaması "
          "ile manken ve OSCE hazırlığı** konusunda; İngiltere sürecini bilen mentörler adaya "
          "birebir yönlendirme sağlar."),
        BAR("3. BAŞVURU & BELGE DOSYASI YÖNETİMİ"),
        P("Diploma, transkript, İngilizce belgesi, referanslar, Certificate of Good Standing ve "
          "gerektiğinde ECCTIS / UK ENIC denklik belgesi; GDC ve RCS England beklentilerine "
          "uygun şekilde hazırlanır. **1.600 klinik saat belgelemesi, MyGDC üzerinden slot "
          "rezervasyonu ve başvuru sıralaması** sürecin fiili işleyişine uygun planlanır."),
        BAR("4. GDC KAYDI & SONRAKİ ADIM YÖNLENDİRMESİ"),
        P("Sınav sonrası GDC siciline kayıt, mesleki sorumluluk sigortası (indemnity) ve "
          "İngiltere’de iş/başvuru adımları konusunda yönlendirme sağlanır. **NHS ve özel "
          "klinik seçenekleri** ile kariyer adımları konusunda adaya deneyime dayalı tavsiyeler "
          "verilir."),
    ],
    whatsapp_and_mentorship(ULKE, [
        "Konaklama ve ev kiralama",
        "Sağlık sistemi (NHS) ve ulaşım",
        "Banka hesabı ve resmî işlemler",
        "Yaşam düzeni ve şehir adaptasyonu",
    ]),
    [
        H1("KAVRAMLAR & TERİMLER", "(GDC REGISTRATION PATHWAY)"),
        P("İngiltere’de diş hekimliği sürecinde sıkça karşılaşılan bazı kavramlar ilk etapta "
          "kafa karıştırıcı olabilir. Aşağıda en çok karşılaşılan temel terimler sade şekilde "
          "açıklanmıştır."),
        DL([
            ("GDC (General Dental Council)",
             "İngiltere’de tüm diş hekimlerini ve diş sağlığı personelini denetleyen resmî "
             "düzenleyici kurumdur. Çalışmak için isminizin GDC siciline kayıtlı olması yasal "
             "bir zorunluluktur."),
            ("GDC Register (Sicil)",
             "İngiltere’de hasta tedavi etme yetkisine sahip diş hekimlerinin resmî "
             "listesidir. Bu sicile kayıtlı olduktan sonra gözetimsiz çalışabilirsiniz."),
            ("Denklik / Tanınma (Recognition)",
             "İngiltere’de yurt dışı diplomanın doğrudan tanınması sınırlıdır. AB/EEA "
             "diplomaları belirli koşullarda 2028’e kadar hızlı tanınabilir; AB dışı "
             "diplomaların çoğu ORE veya LDS sınavı gerektirir."),
            ("ORE (Overseas Registration Exam)",
             "AB/EEA dışında eğitim almış ve diploması doğrudan tanınmayan diş hekimleri için "
             "GDC tarafından yürütülen sınavdır. İki bölümden oluşur ve en yaygın kullanılan "
             "yoldur."),
            ("LDS (Licence in Dental Surgery)",
             "RCS England tarafından verilen, ORE’ye alternatif bir sınavdır. GDC kaydı için "
             "ORE ile eşdeğer kabul edilir; 2026 itibarıyla üç bölümlüdür."),
            ("RCS England",
             "Royal College of Surgeons of England: LDS sınavını düzenleyen kurumdur."),
            ("UCL Consultants (UCLC)",
             "2026’dan itibaren ORE sınavını GDC adına düzenleyen yeni sağlayıcıdır. Yeni "
             "sözleşmeyle sınav kapasitesi ve öngörülebilirliği artırılmıştır."),
            ("MyGDC",
             "ORE başvuru ve sınav yeri (slot) rezervasyonlarının 2026’dan itibaren yapıldığı "
             "çevrimiçi GDC hesabıdır. Rezervasyonlar belirli tarihlerde açılır ve hızla dolar."),
            ("Certificate of Good Standing",
             "Mesleki kaydınızın geçerli ve kısıtlamasız olduğunu gösteren belgedir; "
             "genellikle son 3 ay içinde düzenlenmiş olması istenir."),
            ("ECCTIS / UK ENIC",
             "Yurt dışı diplomaların İngiltere eğitim sistemindeki karşılığını belirleyen "
             "değerlendirme kuruluşudur. AB dışı adaylardan istenebilir."),
            ("Safe Practitioner Framework",
             "GDC’nin yeni mezun bir diş hekiminden beklediği yetkinlikleri tanımlayan "
             "çerçevedir. LDS 2026 itibarıyla bu çerçeveye göre yeniden yapılandırılmıştır."),
            ("Provisional Registration (Geçici Kayıt)",
             "Süreci hızlandırmak için gündeme gelen, ORE/LDS öncesi gözetim altında "
             "çalışmaya imkân tanıyabilecek kayıt türüdür. Kuralları GDC tarafından "
             "şekillendirilmektedir ve durum değişkendir."),
            ("1.600 Klinik Saat",
             "Hem ORE hem LDS başvurusu için istenen, hasta koltuğunda bizzat hasta tedavi "
             "edildiğini gösteren asgari klinik deneyimdir."),
            ("OSCE (Objective Structured Clinical Examination)",
             "ORE Part 2’nin bir parçasıdır. Birden çok istasyondan oluşur; her istasyonda "
             "belirli bir klinik beceri ya da iletişim durumu değerlendirilir."),
            ("Indemnity (Mesleki Sorumluluk Sigortası)",
             "GDC kaydı için zorunlu olan mesleki sorumluluk teminatıdır. Kayıt "
             "tamamlanmadan önce düzenlenmiş olmalıdır."),
        ]),
    ],
    [
        H1("SIK SORULAN SORULAR", "(GDC REGISTRATION PATHWAY)"),
        DL([
            ("Bu süreç ne kadar sürer?",
             "Süre; adayın İngilizce hazırlığına, seçtiği yola (ORE / LDS), sınav takvimine ve "
             "slot bulabilme durumuna bağlı olarak değişir. Talep yüksek olduğu için sınav "
             "slotları önemli bir zaman kalemidir. Planlı ilerleyen ve belgelerini erken "
             "hazırlayan adaylar için süreç yönetilebilir ve öngörülebilirdir."),
            ("DENTCAMP’ten ne kadar süre faydalanabilirim?",
             "Sürece hâkimiz ve bir yıl sınırı koymuyoruz. Hedefiniz olan İngiltere’de diş "
             "hekimliğine başlayana kadar, süreç kesintisi olmadan yanınızda oluruz."),
            ("Diplomam İngiltere’de otomatik olarak tanınır mı?",
             "Genellikle hayır. AB/EEA diplomaları belirli koşullarda 2028’e kadar hızlı "
             "tanınabilir; ancak AB dışı diplomaların çoğu doğrudan tanınmaz. Bu adayların GDC "
             "kaydı için ORE veya LDS sınavını geçmesi gerekir."),
            ("ORE ile LDS arasındaki fark nedir?",
             "İkisi de GDC kaydı için eşdeğer kabul edilir. ORE, GDC tarafından yürütülür ve "
             "iki bölümlüdür. LDS ise RCS England tarafından verilir ve 2026 itibarıyla üç "
             "bölümlüdür. Seçim; sınav takvimine, kapasiteye ve adayın güçlü olduğu sınav "
             "biçimine göre yapılır."),
            ("Öğrenciyim, mezuniyetime daha var, erken mi başladım?",
             "Hayır. Öğrenciyken sürece başlamak, özellikle İngilizce (IELTS/OET) hazırlığı ve "
             "klinik saat planlaması açısından büyük avantaj sağlar. Resmî başvurular "
             "mezuniyet ve diploma sonrası yapılır."),

        ]),
        # SSS 969pt: tek sayfaya sığmıyor. Ortadan dengeli bölünsün diye alt başlık;
        # yoksa ikinci sayfa %35 dolulukta kalıyor.
        BAR("SINAVLAR, ÜCRETLER VE BELGELER"),
        DL([
            ("ORE için kaç saat klinik deneyim gerekiyor?",
             "Hem ORE hem LDS başvurusu için, hasta koltuğunda bizzat hasta tedavi edildiğini "
             "gösteren en az 1.600 saatlik klinik deneyimin belgelenmesi gerekir. Bu nedenle "
             "klinik saatlerin erkenden ve düzgün şekilde kayıt altına alınması önemlidir."),
            ("Hangi İngilizce sınavı ve puanı gerekiyor?",
             "Genellikle IELTS Academic veya OET kabul edilir. IELTS’te çoğunlukla genel 7.0 "
             "ve her bölümden en az 6.5; OET’te ise dört bölümden B notu beklenir. Sertifika "
             "genellikle 2 yıl geçerlidir."),
            ("ORE ücretleri ne kadar?",
             "2026/27 için başvuru işlem ücreti £115, Part 1 £485 ve Part 2 £6.967’dir; ORE "
             "ücretlerine artık KDV uygulanmaktadır. Buna hazırlık kaynakları, İngilizce sınav "
             "ücreti ve gerekliyse ECCTIS/UK ENIC değerlendirmesi eklenir. Kişiye özel bütçe "
             "planı mentörünüzle birlikte çıkarılır."),
            ("ORE slotu bulmak neden zor?",
             "Talep, mevcut kapasitenin üzerindedir; bu nedenle slotlar açıldıktan kısa süre "
             "sonra dolabilir. 2026’dan itibaren rezervasyonlar MyGDC üzerinden yapılır. "
             "Belgelerinizin hazır olması ve rezervasyon tarihinde hızlı hareket etmek büyük "
             "önem taşır."),
            ("ORE ya da LDS’yi geçmek iş garantisi verir mi?",
             "Hayır. Sınavı geçmek ve GDC’ye kaydolmak, İngiltere’de yasal olarak "
             "çalışabilmenizi sağlar; ancak otomatik bir iş garantisi vermez. NHS ve özel "
             "klinik başvuruları ayrı bir süreçtir ve DENTCAMP bu adımda da yönlendirme sağlar."),
            ("Mezun olduğum üniversite önemli mi?",
             "Üniversitenin adı tek başına belirleyici değildir. Asıl önemli olan; "
             "diplomanızın GDC beklentilerini karşılaması, İngilizce ve klinik saat şartlarını "
             "sağlamanız ile başvuru dosyanızın doğru yönetilmesidir."),
            ("LDS’de ne değişti?",
             "LDS, Safe Practitioner Framework’e göre yeniden yapılandırıldı ve üç bölümlü "
             "bir yapıya kavuştu. Part 2’deki “unseen case” bölümünün yerini Haziran "
             "2026’dan itibaren Structured Clinical Reasoning (SCR) aldı. Ayrıca RCS England "
             "kontenjanları artırıyor: 2026’da 1.000, 2027’de yılda 2.000 Part 1 yeri."),
            ("Sınav öncesi çalışmaya başlayabilir miyim?",
             "Süreci hızlandırmak için gündeme gelen geçici (provisional) kayıt, ORE/LDS "
             "öncesi gözetim altında çalışmaya imkân tanıyabilir. Ancak kuralları GDC "
             "tarafından şekillendirilmektedir ve durum değişkendir; başvurudan önce güncel "
             "GDC duyuruları kontrol edilmelidir."),
            ("Belgelerimin / puanlarımın geçerlilik süresi var mı?",
             "Evet, olabilir. IELTS/OET sonuçları çoğunlukla 2 yıl, Certificate of Good "
             "Standing ise genellikle 3 ay geçerlidir. Ayrıca ORE Part 2, ilk Part 1 "
             "denemesinden itibaren 5 yıl içinde geçilmelidir."),
        ]),
    ],
]

ROADMAP_TITLE = "GDC REGISTRATION ROAD MAP"
ROADMAP_SUB = "İngiltere’de Diş Hekimliği Süreci"

ROADMAP = [
    (1, "İngilizce Yeterliliği", "IELTS 7.0 (her bölüm ≥ 6.5) / OET B",
     "Klinik ve akademik İngilizce", "ic_dil.png"),
    (2, "Tanınma Durumu &amp;<br>Yol Seçimi", "ORE / LDS kararı",
     "AB dışı adaylar için sınav yolu", "ic_muhur.png"),
    (3, "Başvuru &amp; Belgeler", "1.600 klinik saat + Good Standing",
     "ECCTIS / UK ENIC · referanslar", "ic_belge.png"),
    (4, "ORE", "Part 1 (yazılı) + Part 2 (uygulamalı)",
     "GDC tarafından yürütülür", "ic_sinav.png"),
    (5, "LDS (Alternatif)", "RCS England · üç bölüm",
     "Safe Practitioner Framework", "ic_dis.png"),
    (6, "GDC Kaydı", "Registration + indemnity",
     "Bağımsız çalışma yetkisi", "ic_lisans.png"),
]

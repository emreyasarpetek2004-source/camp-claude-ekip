#!/usr/bin/env python3
"""DENTCAMP: Toplu katalog (Almanya · Avustralya · İngiltere · ABD).

Dört ülke kataloğunun ORTAK özeti: 10 sayfa. Her ülke tek sayfa alır; süreç
şeması, tam sayfa road map yerine sayfa içi MINIMAP olarak basılır.

Olgular ülke kataloglarından alındı, yeniden araştırılmadı: burada geçen her
rakam ve her sınav adı content/deu.py, aus.py, uk.py, usa.py içinde de var.
Detay isteyen okuyucu ilgili ülke kataloğuna yönlendirilir.

Kullanım: python3 build_optimal.py toplu
"""
from build import H1, BAR, P, SUB, UL, DL, BOX, STATS, CARDS3, KARSI, MINIMAP
from content._common import mentorler_toplu, PHONES   # noqa: F401

ULKE = "Toplu"

COVER = {
    # Künye dört ülkeyi ve her birinin hedefini veriyor: okuyucu kapakta
    # kataloğun kapsamını görsün.
    "kunye": [
        ('ALMANYA', 'Approbation'),
        ('AVUSTRALYA', 'AHPRA kaydı'),
        ('İNGİLTERE', 'GDC kaydı'),
        ('ABD', 'Eyalet lisansı'),
    ],
    "pill": "Yurt Dışında",
    "title": "Diş Hekimliği\nKariyeri",
    "tag": "| 4 ÜLKE",
    "sub": "(Dört ülkenin denklik, lisans ve\nsüreç rehberi)",
    # 2 Eylül 2026 (kullanıcı): kapakta bayrak şeridi YOK. Kapak fotoğrafı dört
    # bayrağı kendi içinde taşıyor, şeritle birlikte kapakta iki kez geçiyordu.
    "bayrak": False,
}

MENTORLER_BOLUM = mentorler_toplu()
MENTOR_YERI = 4        # kadro ABD sayfasından sonra, HİZMETLERİMİZ'den önce

INTRO = [
    H1("DENTCAMP NEDİR?"),
    P("DENTCAMP, yurt dışında kariyerlerini sürdürmek isteyen diş hekimleri için "
      "nitelikli çözümler sunan, **diş hekimliği alanına özel bir eğitim ve "
      "danışmanlık kurumudur.**"),
    CARDS3([
        ("Ne yapıyoruz",
         "Almanya, Avustralya, İngiltere ve ABD olmak üzere **dört ülkede** diş "
         "hekimlerinin denklik ve lisans süreçlerini baştan sona yönetiriz."),
        ("Nasıl yürütüyoruz",
         "Sınav süreçlerinden belge yönetimine, dil yeterliliğinden hedef ülkedeki "
         "yeni hayatınıza uzanan **her aşamayı doğru sırayla** yürütürüz."),
        ("Kimlerle",
         "Dört ülkede aktif çalışan **deneyimli diş hekimi mentörler** ve "
         "Türkiye’de süreci koordine eden yönetim ekibi."),
    ]),
    BAR("BU KATALOG NE İŞE YARAR"),
    P("Bu katalog, dört ülkenin sürecini **aynı ölçekte** yan yana koyar. Amaç, ülke "
      "kararını vermeden önce sorulması gereken soruları netleştirmektir: hangi dil "
      "şartı sizi ne kadar geciktirir, hangi sınav sizin güçlü olduğunuz alandadır, "
      "hangi ülkede diploma yeniden okunur, hangisinde okunmaz."),
    SUB("Dört ülkenin tamamında değişmeyen üç kural:"),
    UL([
        "**Yurt dışı diplomanız hiçbir ülkede otomatik olarak tanınmaz.** Her ülkede "
        "belge değerlendirmesi ve sınav basamağı vardır.",
        "**Dil yeterliliği sürecin önünde durur.** Sertifika tamamlanmadan başvuru ve "
        "sınav takvimi ilerlemez.",
        "**Sıra önemlidir.** Yanlış sırayla atılan adım, geçerlilik süresi dolan belge "
        "ve tekrar ödenen sınav ücreti anlamına gelir.",
    ]),
    BAR("KİMLER BAŞVURUYOR"),
    P("Danışan profili tek tip değildir ve sürecin başlangıç noktası profile göre "
      "değişir:"),
    UL([
        "**Diş hekimliği öğrencileri:** mezuniyet öncesinde dil ve belge hazırlığına "
        "başlayanlar. Zaman avantajı en yüksek gruptur.",
        "**Yeni mezunlar:** klinik deneyim şartı olan ülkelerde (İngiltere) süreci buna "
        "göre kurgulaması gereken grup.",
        "**Aktif çalışan hekimler:** mevcut işini sürdürürken ilerleyen, bu nedenle sınav "
        "takvimi ve dil programı iş temposuna göre planlanan grup.",
        "**Uzmanlığı olan hekimler:** ABD’de uzmanlık rezidanslığı rotası, diğer üç ülkede "
        "genel lisans süreci gündeme gelir.",
    ]),
    BOX("**Ülke kararı bu katalogla verilmez, daraltılır.** Karar; mevcut eğitim "
        "durumunuz, klinik deneyiminiz, dil seviyeniz, bütçeniz ve hedef takviminiz "
        "birlikte değerlendirilerek çıkarılır. Bu değerlendirme mentörlerle yapılan "
        "görüşmelerin konusudur."),
]

BODY = [
    # -- 1. karşılaştırma ----------------------------------------------------
    [
        H1("DÖRT ÜLKE, DÖRT YOL", "(Almanya · Avustralya · İngiltere · ABD)"),
        P("Dört ülkenin de hedefi aynıdır: **o ülkede bağımsız çalışma yetkisi.** "
          "Ayrım, o yetkiye hangi kapıdan gidildiğindedir. Almanya ve İngiltere devlet "
          "ya da konsey eliyle yürütülen bir denklik sınavı ister; Avustralya konsey "
          "sınavı ile birlikte pratik sınav ister; ABD’de ise tek bir rota yoktur. Bu "
          "ayrım yalnız sınav biçimini değil; süreyi, maliyeti ve nerede yaşanacağını da "
          "belirler."),
        KARSI(
            ["Ülke", "Dil şartı", "Ana sınav / yol", "Belirleyici şart", "Hedef"],
            [
                ["Almanya", "Almanca B2 + mesleki Almanca (FSP)",
                 "Kenntnisprüfung: yazılı, sözlü ve pratik",
                 "Süreç eyalet (Land) bazlıdır; eyalet seçimi takvimi belirler",
                 "Approbation"],
                ["Avustralya", "IELTS / OET / PTE / TOEFL",
                 "ADC yazılı sınavı + ADC pratik sınavı",
                 "Pratik sınav yalnızca Melbourne’da yapılır",
                 "AHPRA kaydı"],
                ["İngiltere", "IELTS Academic 7.0 ya da OET B",
                 "ORE (Part 1 + Part 2) ya da alternatif olarak LDS",
                 "1.600 saat klinik deneyim belgelenmelidir",
                 "GDC kaydı"],
                ["ABD", "TOEFL (bazı programlarda IELTS)",
                 "INBDE + seçilen rotanın kendi basamakları",
                 "Üç ayrı rota vardır; lisans eyalet bazlıdır",
                 "Eyalet lisansı"],
            ]),
        SUB("Tabloyu okurken:"),
        UL([
            "**Dil sütunu takvimin başlangıcıdır.** Almanya’da sıfırdan B2 ve FSP’ye "
            "uzanan yol, diğer üç ülkenin İngilizce şartından belirgin şekilde uzundur.",
            "**Sınav sütunu maliyeti belirler.** İngiltere’de ORE Part 2 tek kalemde "
            "£6.967’dir; Almanya’da Kenntnisprüfung ~1.300 €’dur.",
            "**Belirleyici şart sütunu eleyicidir.** Avustralya’da pratik sınav için "
            "Melbourne seyahati, ABD’de rota seçimi, İngiltere’de 1.600 klinik saat: "
            "üçü de plan yapılmadan atlanamaz.",
            "**Hedef sütunu bitiş çizgisidir, başlangıç değil.** Approbation, AHPRA kaydı, "
            "GDC kaydı ve eyalet lisansı; dördü de o ülkede bağımsız çalışma yetkisi verir.",
            "**Tablo tek başına karar vermez.** Aynı yol, farklı iki hekim için farklı süre "
            "ve farklı maliyet anlamına gelir: dil seviyesi, klinik deneyim ve bütçe "
            "sıralamayı değiştirir.",
            "**Dil sütunu ile sınav sütunu birlikte okunur.** Almanya’da dil uzun ama "
            "sınav ücreti düşüktür; İngiltere’de dil kısa ama sınav ücreti dört ülkenin "
            "en yükseğidir. Toplam yük, iki sütunun toplamıdır.",
        ]),
        BOX("**Diploma yeniden okunur mu?** Almanya, Avustralya ve İngiltere’de "
            "**hayır:** denklik sınavı geçilir. ABD’de en yaygın rota olan Advanced "
            "Standing **evet** der: CODA akreditasyonlu bir fakültede 2–3 yıl okunur ve "
            "ABD diploması alınır."),
    ],

    # -- 2. Almanya ----------------------------------------------------------
    [
        H1("ALMANYA", "(Approbation Pathway)"),
        P("Almanya’da hedef **Approbation’dır:** süresiz ve tam yetkili çalışma "
          "lisansı. Yol; genel Almanca yeterliliği, mesleki Almanca sınavı (FSP), "
          "denklik başvurusu ve devlet komisyonu önünde verilen Kenntnisprüfung "
          "sırasıyla ilerler. Başvuru federal değil **eyalet (Land) bazlıdır;** "
          "eyalet seçimi hem takvimi hem istenen belgeleri etkiler."),
        MINIMAP([
            ("Almanca B2", "telc · Goethe · ÖSD"),
            ("Fachsprachprüfung", "Mesleki Almanca, C1"),
            ("Denklik Başvurusu", "Landesprüfungsamt"),
            ("Kenntnisprüfung", "Yazılı · sözlü · pratik"),
            ("Approbation", "Süresiz tam lisans"),
        ]),
        SUB("Sürecin belirleyici noktaları:"),
        UL([
            "**Dil, sürecin en çok eleyen aşamasıdır.** B2 sertifikası olmadan denklik "
            "dosyası ilerlemez; FSP ise hasta görüşmesi, hekim iletişimi ve tıbbi belge "
            "yazımı üzerinden ölçülür.",
            "**Kenntnisprüfung üç bölümlüdür** ve her bölüm için sınırlı sınav hakkı "
            "vardır; hazırlık kursları ayrı bir bütçe kalemidir.",
            "**Belgeler apostilli ve yeminli tercümeli** olmalıdır; tercüme ve apostil "
            "kalemi tek başına 500 – 1.500 € tutar.",
        ]),
        SUB("Sık karışan kavramlar:"),
        DL([
            ("Berufserlaubnis", "Belirli bir eyalete ve çoğu zaman belirli bir işverene "
             "bağlı, en fazla 2 yıllık **geçici** çalışma iznidir. Approbation süreci "
             "sürerken fiilen çalışıp Kenntnisprüfung’a hazırlanmak için ara adım olarak "
             "kullanılabilir."),
            ("Defizitbescheid", "Yetkili makamın, eğitimde esasa ilişkin fark tespit "
             "ettiğinde gönderdiği eksiklik yazısıdır. Kenntnisprüfung’a girilmesi "
             "gerektiği anlamına gelir."),
            ("Landesprüfungsamt", "Denklik ve Approbation başvurularının yürütüldüğü, "
             "**eyalet düzeyindeki** yetkili resmî makamdır."),
        ]),
        STATS([("12–24 ay", "Uçtan uca tipik süre"),
               ("~1.300 €", "Kenntnisprüfung ücreti"),
               ("3 hak", "Bölüm başına sınav hakkı")]),
        BOX("Almanya’da yaşayan ve şartları sağlayan adaylar, Kenntnisprüfung hazırlık "
            "kursları için İş Ajansı’ndan (**Agentur für Arbeit**) **Bildungsgutschein** "
            "ile %100’e varan finansman alabilir."),
    ],

    # -- 3. Avustralya -------------------------------------------------------
    [
        H1("AVUSTRALYA", "(ADC Pathway)"),
        P("Avustralya’da hedef **AHPRA kaydıdır** (general registration). Yol, "
          "Australian Dental Council’in üç aşamalı değerlendirmesi üzerine kuruludur: "
          "belge değerlendirmesi, yazılı sınav ve pratik sınav. Diploma otomatik olarak "
          "tanınmaz; buna karşılık **yeniden diş fakültesi okunmaz.**"),
        MINIMAP([
            ("Belge Değerlendirmesi", "ADC Connect"),
            ("Yazılı Sınav", "2 gün · 280 soru"),
            ("Pratik Sınav", "OSCE · Melbourne"),
            ("İngilizce Yeterliliği", "IELTS · OET · PTE"),
            ("AHPRA Kaydı", "General registration"),
        ]),
        SUB("Sürecin belirleyici noktaları:"),
        UL([
            "**Belge değerlendirmesi 7 yıl geçerlidir;** süreç bu tarihe göre "
            "planlanabilir ve erken başlatmak sonraki adımlarda esneklik sağlar.",
            "**Pratik sınav yalnızca Melbourne’da yapılır.** Seyahat, konaklama ve "
            "ekipman lojistiği sınav hazırlığının parçasıdır.",
            "**İngilizce sonuçları AHPRA’ya doğru sırayla iletilmelidir;** good "
            "standing belgesi ve sabıka kaydı da aynı dosyada istenir.",
            "**Yazılı sınav Pearson VUE merkezlerinde yapılır** ve iki güne yayılır; bilim "
            "bilgisi ile klinik muhakemeyi birlikte ölçer, bu nedenle hazırlık yalnız "
            "ezbere dayanamaz.",
        ]),
        SUB("Sık karışan kavramlar:"),
        DL([
            ("Initial Assessment", "ADC sürecinin ilk adımıdır. Bir sınav değil, belge "
             "doğrulamasıdır; başarılı sonuç **7 yıl geçerlidir.**"),
            ("Good Standing", "Kendi ülkenizdeki düzenleyici kurumdan alınan, mesleki "
             "kaydınızın geçerli ve kısıtlamasız olduğunu gösteren belgedir; doğrudan "
             "ilgili kurumdan gönderilir."),
            ("General Registration", "Avustralya’da diş hekimi olarak serbestçe çalışmaya "
             "izin veren kayıt türüdür. Her iki ADC sınavı geçildikten sonra alınır."),
        ]),
        STATS([("12–24 ay", "Uçtan uca tipik süre"),
               ("2 gün", "Yazılı sınav süresi"),
               ("280", "Senaryo bazlı soru")]),
        BOX("**Göç boyutu ayrıca planlanır.** Kalıcı yerleşim hedefi olan adaylarda "
            "skills assessment süreci, ADC takvimiyle birlikte kurgulanır."),
    ],

    # -- 4. İngiltere --------------------------------------------------------
    [
        H1("İNGİLTERE", "(GDC Registration Pathway)"),
        P("İngiltere’de hedef **GDC siciline kayıttır;** kayıt, gözetimsiz çalışma "
          "yetkisi anlamına gelir. AB/EEA dışı adayların çoğu için iki eşdeğer sınav "
          "yolu vardır: **ORE ve LDS.** Seçim; sınav takvimine, kapasiteye ve adayın "
          "güçlü olduğu sınav biçimine göre yapılır."),
        MINIMAP([
            ("İngilizce Yeterliliği", "IELTS 7.0 · OET B"),
            ("Yol Seçimi", "ORE ya da LDS"),
            ("Başvuru & Belgeler", "1.600 klinik saat"),
            ("Sınav", "ORE Part 1 + Part 2"),
            ("GDC Kaydı", "Bağımsız çalışma yetkisi"),
        ]),
        SUB("Sürecin belirleyici noktaları:"),
        UL([
            "**1.600 saat klinik deneyim** belgelenmelidir: hasta koltuğunda bizzat "
            "yürütülen tedavi. Bu şart hem ORE hem LDS için geçerlidir.",
            "**Slotlar dolabilir.** Rezervasyon MyGDC üzerinden yapılır; kapasite "
            "artırılsa da talep yüksektir, sınav takvimi önden planlanmalıdır.",
            "**Certificate of Good Standing** genellikle son 3 ay içinde düzenlenmiş "
            "olmalıdır; belgelerin geçerlilik penceresi dosyanın sırasını belirler.",
            "**ORE ve LDS eşdeğerdir.** Biri diğerinden üstün sayılmaz; seçim, sınav "
            "takvimine ve adayın hangi sınav biçiminde daha güçlü olduğuna göre yapılır.",
            "**Kayıt öncesinde indemnity düzenlenmiş olmalıdır;** sicile kayıt bu teminat "
            "olmadan tamamlanmaz.",
        ]),
        SUB("Sık karışan kavramlar:"),
        DL([
            ("ECCTIS / UK ENIC", "Yurt dışı diplomaların İngiltere eğitim sistemindeki "
             "karşılığını belirleyen değerlendirme kuruluşudur. AB dışı adaylardan "
             "istenebilir."),
            ("Indemnity", "GDC kaydı için zorunlu olan **mesleki sorumluluk teminatıdır.** "
             "Kayıt tamamlanmadan önce düzenlenmiş olmalıdır."),
            ("Safe Practitioner Framework", "LDS sınavının yeniden yapılandırıldığı "
             "çerçevedir; sınavın hangi yetkinlikleri hangi ağırlıkla ölçtüğünü belirler."),
        ]),
        STATS([("£485", "ORE Part 1 ücreti"),
               ("£6.967", "ORE Part 2 ücreti"),
               ("1.600 saat", "Klinik deneyim şartı")]),
        BOX("**ORE ücretlerine artık KDV uygulanır** ve 2026/27 ücretleri "
            "güncellenmiştir. Sınav, 6 Mayıs 2026’dan itibaren yeni sağlayıcı **UCL "
            "Consultants (UCLC)** ile yürütülür."),
    ],

    # -- 5. ABD --------------------------------------------------------------
    [
        H1("AMERİKA BİRLEŞİK DEVLETLERİ", "(US Licensure)"),
        P("ABD’de tek bir rota yoktur ve lisans federal değil **eyalet bazlıdır.** Buna "
          "karşılık ilk üç adım her rotada aynıdır: DENTPIN numarası ve diploma "
          "değerlendirmesi, TOEFL ve **INBDE.** Ayrım dördüncü adımda başlar."),
        MINIMAP([
            ("DENTPIN & Denklik", "ECE / WES değerlendirmesi"),
            ("TOEFL", "1–6 bant ölçeği"),
            ("INBDE", "Ulusal board sınavı"),
            ("Rota Seçimi", "Üç yoldan biri"),
            ("Eyalet Lisansı", "ADEX + jurisprudence"),
        ]),
        SUB("Dördüncü adımdaki üç rota:"),
        UL([
            "**Advanced Standing (CAAPID):** CODA akreditasyonlu fakültede 2–3 yıl, "
            "sonunda ABD diploması. Her eyalette geçerlidir; öğrenim ücreti en büyük "
            "bütçe kalemidir.",
            "**Uzmanlık rezidanslığı (ADEA PASS):** mevcut diplomayla uzmanlık "
            "programı, dala göre 2–4 yıl ve genellikle maaşlı. Ancak uzmanlık, çoğu "
            "eyalette genel lisans anlamına gelmez.",
            "**AEGD / GPR:** 1–2 yıllık genel asistanlık. En kısa ve en ucuz görünen "
            "yoldur; buna karşılık yaklaşık 16 eyalet kabul eder ve lisans genelde o "
            "eyalete bağlı kalır.",
            "**Rota seçimi eyalet stratejisiyle birlikte yapılır.** Özellikle AEGD / GPR "
            "yolunda önce hangi eyalette çalışılacağı belirlenir, program seçimi ondan "
            "sonra gelir.",
        ]),
        SUB("Sık karışan kavramlar:"),
        DL([
            ("DENTPIN", "Kişisel diş hekimliği kimlik numarasıdır. Tüm sınav ve başvurular "
             "için **ilk** alınması gereken numaradır; ADA sitesinden ücretsiz alınır."),
            ("CODA", "ABD’de diş hekimliği programlarını akredite eden kurumdur. Hangi rota "
             "izlenirse izlensin, girilecek programın **CODA akreditasyonlu** olması "
             "zorunludur."),
            ("ADEX / DLOSCE", "En yaygın kabul gören klinik lisans sınavı ADEX’tir; manken "
             "(CompeDont) üzerinde uygulamalı bölümler ile bilgisayar tabanlı DLOSCE’den "
             "oluşur."),
        ]),
        STATS([("2–3 yıl", "Advanced Standing süresi"),
               ("1–2 yıl", "AEGD / GPR süresi"),
               ("~16", "AEGD / GPR’yi tanıyan eyalet")]),
        BOX("**Üçünde de değişmeyen tek şart INBDE’dir.** Tüm eyalet lisans otoriteleri "
            "bu sınavı ister; alternatif rotalar bile INBDE’yi sürecin parçası olarak "
            "kabul eder."),
    ],

    # -- 6. hizmetler --------------------------------------------------------
    [
        H1("HİZMETLERİMİZ", "(Dört Ülkede Ortak)"),
        P("DENTCAMP, hangi ülkeyle ilerlenirse ilerlensin süreci **planlı, "
          "sürdürülebilir ve kontrollü bir geçiş** olarak ele alır. Sunulan destek, her "
          "aşamada doğru adımı doğru sırayla atmayı sağlayacak mentörlük ve yönlendirme "
          "üzerine kuruludur."),
        BAR("1. PROFİL ANALİZİ & YOL PLANI"),
        P("Mentörler tarafından yapılan **iki online görüşme** sonrasında; mevcut eğitim "
          "durumu, klinik deneyim, dil seviyesi, vize/ikamet durumu ve hedefler "
          "doğrultusunda izlenecek adımlar belirlenir. **Ülke kararı da bu aşamada "
          "netleşir.** Hangi sınavın ne zaman tamamlanacağı net bir yol haritasına bağlanır."),
        # 2 Eylül 2026 (kullanıcı): dil eğitimi YALNIZ Avustralya (MEDCAMP) ve Almanya
        # (MEDCAMP DEUTSCH) paketlerinde var. İngiltere ve ABD sürecinde DENTCAMP
        # dil desteği sağlamıyor; dil ŞARTI ise dört ülkede de duruyor ve karşılaştırma
        # tablosunda basılıyor.
        BAR("2. DİL EĞİTİMİ (AVUSTRALYA VE ALMANYA PAKETLERİNDE)"),
        P("Avustralya paketinde OET hazırlığı **MEDCAMP** bünyesinde yürütülür: seviye "
          "tespiti, kişiye özel çalışma programı ve sınav formatına birebir pratik. "
          "Almanya’da dil Almanca olduğu için eğitim, **ÖSD sınav merkezi akreditasyonuna "
          "sahip MEDCAMP DEUTSCH** bünyesinde A1’den B2’ye ve **FSP hazırlığına** kadar "
          "tek pakette verilir. İngiltere ve ABD paketlerinde dil eğitimi yer almaz; bu "
          "iki süreçte sınavın **hangi aşamada tamamlanacağı** yol haritasına bağlanır."),
        BAR("3. SINAV MENTÖRLÜĞÜ"),
        P("Hedef ülkenin sınavına özel mentörlük sağlanır: **sınavın yapısı, soru tipine "
          "yaklaşım, çalışma stratejisi, kaynak seçimi ve zaman planlaması.** Pratik sınavı "
          "olan ülkelerde istasyon ve maket çalışmasının yanı sıra sınav dönemi lojistiği "
          "de planlamaya dâhil edilir."),
        BAR("4. BELGE YÖNETİMİ & BAŞVURU"),
        P("Diploma değerlendirmesi, transkript, good standing belgesi, sabıka kaydı ve dil "
          "sonuçlarının **hangi kuruma hangi sırayla iletileceği** yönetilir. Belgelerin "
          "geçerlilik pencereleri takip edilir; süresi dolan belge nedeniyle tekrar ödenen "
          "ücret ve kaybedilen sınav dönemi bu şekilde önlenir."),
        BAR("5. KİŞİYE ÖZEL WHATSAPP GRUBU"),
        P("Sorulara en hızlı ve etkili cevabı verebilmek amacıyla her danışan için **kişiye "
          "özel bir grup** kurulur. Grupta biri primer, diğerleri sekonder olmak üzere "
          "**birden fazla mentör** bulunur. Tüm sınav, başvuru, belge ve süreç adımları bu "
          "grup üzerinden bireysel olarak yürütülür."),
        BAR("6. A’DAN Z’YE MENTÖRLÜK DESTEĞİ"),
        P("Süreç boyunca adaylara, **hedef ülkede bu yolu bizzat tamamlamış diş hekimi "
          "mentörler** eşlik eder. Mentörlük yalnızca mesleki adımlarla sınırlı değildir; "
          "yerleşme sürecinde günlük yaşam da kapsanır:"),
        UL([
            "Konaklama ve ev kiralama",
            "Sağlık sigortası ve ulaşım",
            "Banka hesabı ve resmî işlemler",
            "Yaşam düzeni ve şehir adaptasyonu",
        ]),
    ],
]

# Kapanış sayfası: ülke kataloglarındaki tam sayfa road map'in yerini alır
# (her ülkenin şeması kendi sayfasında MINIMAP olarak duruyor).
CLOSING = {
    "title": "BİR SONRAKİ ADIM",
    "sub": "Ülke Kararından Yol Planına",
    "lead": "Bu katalog dört ülkeyi aynı ölçekte gösterir. Sıradaki iş, bu dört yoldan "
            "**hangisinin sizin profilinize oturduğunu** belirlemek ve o yolu takvime "
            "bağlamaktır.",
    "steps": [
        ("Profil Analizi",
         "Eğitim durumunuz, klinik deneyiminiz, dil seviyeniz ve hedef takviminiz "
         "mentörlerle birlikte değerlendirilir."),
        ("Ülke Kararı",
         "Dört yol; süre, maliyet, sınav biçimi ve yerleşme koşulları üzerinden "
         "karşılaştırılır. Karar, tahminle değil **ölçüyle** verilir."),
        ("Kişiye Özel Yol Planı",
         "Seçilen ülkenin adımları sıraya konur: hangi belge ne zaman, hangi sınav "
         "hangi dönemde. Süreç bu plan üzerinden yürütülür."),
    ],
    "next": "Yol planınız, **mevcut durumunuz ve hedef takviminiz** üzerinden hazırlanır.",
}

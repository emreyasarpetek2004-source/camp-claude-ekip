#!/usr/bin/env python3
"""DENTCAMP: Avustralya (ADC Pathway).

Kaynak metin: BROŞÜR VE TANITIM/avustralya/Avustralya_Dis_Hekimligi_Brosur.docx
Dil, AUSCAMP Specialist Pathway kataloğunun kurumsal register'ına çevrildi.
**kalın** işaretlemesi otomatik <b>'ye dönüşür; sayfalama ölçümle yapıldığı için
metin uzayıp kısaldığında sayfa sonlarını elle ayarlamaya gerek yok.
"""
from build import H1, BAR, P, SUB, UL, DL, BOX, STATS
from content._common import (intro, mentorler, placeholders, dil_yeterliligi,
                             whatsapp_and_mentorship, PHONES)   # noqa: F401

ULKE = "Avustralya"

COVER = {
    # Kapak alt bandındaki üç künye — hepsi katalogda zaten geçen bilgiler.
    "kunye": [
        ('SÜRE', '12–24 ay'),
        ('SINAVLAR', 'Yazılı + Pratik'),
        ('HEDEF', 'AHPRA kaydı'),
    ],
    "pill": "Avustralya’da",
    "title": "Diş Hekimliği\nKariyeri",
    "tag": "| ADC PATHWAY",
    "sub": "(Diş hekimliği öğrencileri ve\ndiş hekimleri için süreç rehberi)",
}

INTRO = intro(ULKE)
MENTORLER_BOLUM = mentorler(ULKE)
MENTOR_YERI = 0        # kadro bu BODY bölümünden sonra: ADC PATHWAY

# Anita Gözübüyük anlaşması tamamlandı (DENTCAMP Mentör Tablosu, 23.07.2026);
# fotoğrafı AUSCAMP kataloğundan geliyor. Kalan kartlar anlaşmalar bitince doldurulur.
MENTORS = [
    ("m_anita_gozubuyuk.png", "Dt. Msc. Anita Gözübüyük",
     ["Diş Hekimi & Mentör", "Melbourne, VIC", ""]),
] + placeholders(3, ULKE)

# --- Mentör (gerçek) --------------------------------------------------------
# Biyografi henüz alınmadı; kart yalnız doğrulanmış bilgiyle basılıyor.
MENTOR_TAM = [dict(
    foto="m_anita_gozubuyuk.png",
    ad="Dt. MSc. Anita Gözübüyük",
    meta="DİŞ HEKİMİ & MENTÖR · MELBOURNE, AVUSTRALYA",
    bio=[],
)]

BODY = [
    # -- yol tanımı ----------------------------------------------------------
    [
        H1("ADC PATHWAY", "(Diş Hekimliği Öğrencileri · Diş Hekimleri)"),
        P("ADC Pathway, Avustralya’da diş hekimliği kariyerine adım atmak isteyenler için "
          "izlenen ana yoldur. Bu yol; **belge değerlendirmesi, yazılı sınav, pratik sınav, "
          "İngilizce yeterliliği ve AHPRA kaydı** adımlarının belirli bir sıra ve sistematik "
          "yapı içinde ilerlemesiyle tanımlanır."),
        P("Sürecin nihai hedefi, olumlu bir ADC sonucu ve AHPRA’dan alınan **çalışma kaydıdır "
          "(general registration).**"),
        BOX("**Önemli:** Avustralya’da yurt dışı diplomanız otomatik olarak tanınmaz; ancak "
            "ABD’den farklı olarak **yeniden diş fakültesi okumanız gerekmez.** Standart yol; "
            "Australian Dental Council (ADC) değerlendirme sürecini: belge, yazılı ve pratik "
            "sınav: tamamlayıp AHPRA’dan çalışma kaydı almaktır."),
        BAR("GÜNCEL BİLGİLER (2026)"),
        UL([
            "AHPRA’nın İngilizce puan gereksinimleri **23 Nisan 2026’da** değişmiştir; OET "
            "harf notundan sayısal sisteme geçmiş, PTE’de konuşma eşiği yükselmiştir.",
            "**Kasım 2025’ten** itibaren ADC, göç (skills assessment) belgelerini sürecin "
            "başında değil, **sınavlar geçildikten sonra** istemektedir.",
            "Pratik sınav **yalnızca Melbourne’da** yapılır; seyahat ve konaklama baştan "
            "planlanmalıdır.",
        ]),
    ],
    # -- adımlar -------------------------------------------------------------
    [
        BAR("1. BELGE DEĞERLENDİRMESİ (INITIAL ASSESSMENT)"),
        P("Sürecin ilk adımı, **ADC Connect** üzerinden yapılan belge değerlendirmesidir. "
          "Diploma, transkript, mesleki kayıt belgesi ve kimlik belgeleri sunulur; ADC, "
          "niteliklerin **en az 4 yıllık tam zamanlı diş hekimliği eğitimi** ölçütünü "
          "karşılayıp karşılamadığını ve adayın yazılı sınava girmeye uygun olup olmadığını "
          "değerlendirir. Başarılı sonuç **7 yıl geçerlidir.**"),
        SUB("Uygunluk (eligibility):"),
        UL([
            "Tanınan bir üniversiteden **en az 4 yıllık, tam zamanlı** diş hekimliği diploması.",
            "Eğitim alınan ülkede **tam ve kısıtlanmamış** mesleki kayıt.",
            "İngilizce dışı belgeler için **resmî çeviri** gereklidir.",
        ]),
    ],
    [
        BAR("2. YAZILI SINAV (WRITTEN EXAMINATION)"),
        P("Initial assessment onayı geçerliyken ADC Connect üzerinden yazılı sınava "
          "başvurulur. Sınav **yılda iki kez** (genellikle Mart ve Eylül) düzenlenir ve "
          "**Pearson VUE** merkezlerinde girilir. İki gün süren, senaryo bazlı çoktan seçmeli "
          "bir sınavdır; ezberden çok **güvenli klinik karar vermeye** odaklanır. Sonuçlar "
          "yaklaşık altı hafta sonra açıklanır."),
        SUB("Yazılı sınav: özet:"),
        UL([
            "**Format:** 2 gün, 280 senaryo bazlı soru, 4 bölüm (bölüm başına 70 soru).",
            "**İçerik:** diş hekimliği bilimi, Avustralya pratiğine uygun klinik muhakeme, "
            "yasal ve etik çerçeve.",
            "**Geçme oranları** son yıllarda %25 civarına kadar düşmüştür; ciddi bir hazırlık "
            "gerekir.",
        ]),
        STATS([("2 gün", "Sınav süresi"), ("280", "Senaryo bazlı soru"),
               ("~%25", "Son yıllardaki geçme oranı")]),
    ],
    [
        BAR("3. PRATİK SINAV (PRACTICAL EXAMINATION)"),
        P("Yazılı sınavı geçen adaylar pratik sınava başvurabilir. Bu **iki günlük, "
          "simülasyon tabanlı** sınav yalnızca **Melbourne’daki ADC merkezinde** yapılır. "
          "OSCE istasyonlarında hasta yönetimi, klinik muayene ve diş prosedürleri "
          "değerlendirilir; ayrıca **maket (manikin) üzerinde** kavite hazırlığı, restorasyon "
          "ve scaling gibi teknik görevler uygulanır."),
        P("Pratik sınav, **yazılı sınavın geçerlilik süresi içinde** tamamlanmalıdır. Bu "
          "nedenle aşamaların geriye doğru planlanması kritik önem taşır."),
    ],
    [
        BAR("4. İNGİLİZCE YETERLİLİĞİ"),
        P("AHPRA kaydı için İngilizce yeterliliğinin kanıtlanması gerekir. Kabul edilen "
          "testler **IELTS Academic, OET, PTE Academic, TOEFL iBT ve Cambridge C1/C2’dir.** "
          "Skorlar test kurumundan doğrudan AHPRA’ya iletilir."),
        P("**23 Nisan 2026’dan** itibaren minimum puanlar güncellenmiştir; gerekli yeterlilik "
          "düzeyi aynı kalmış, yalnızca puan karşılıkları yeniden ayarlanmıştır. Aynı "
          "sağlayıcıdan **12 ay içinde** alınmış en fazla iki oturumun skorları "
          "birleştirilebilir."),
    ],
    [
        BAR("5. AHPRA / DENTAL BOARD KAYDI"),
        P("Her iki sınav geçildikten sonra AHPRA portalından **genel kayıt (general "
          "registration)** başvurusu yapılır. İyi hâl / kayıt durumu belgesi düzenleyici "
          "kurumdan doğrudan gönderilir; yurt dışında altı aydan fazla yaşayanlar için "
          "**uluslararası sabıka kaydı** kontrolü gerekir. İngilizce yeterlilik kanıtı sunulur "
          "ve gerekirse **mesleki güncellik (recency of practice)** standardı karşılanır."),
        P("Kayıt onaylandığında Avustralya’da **yasal olarak diş hekimliği yapılabilir.**"),
        BOX("Avustralya’da **kayıt ve göç iki ayrı hedeftir:** çalışmak için AHPRA kaydı, göç "
            "için ayrıca skills assessment gerekir. Kesin ücretler, tarihler ve şartlar için "
            "adc.org.au, ahpra.gov.au ve dentalboard.gov.au esas alınmalıdır."),
    ],
    # -- hizmetler -----------------------------------------------------------
    [
        H1("HİZMETLERİMİZ", "(ADC PATHWAY)"),
        P("DENTCAMP, ADC Pathway sürecini; Avustralya sağlık ve eğitim sistemine uygun şekilde "
          "**planlı, sürdürülebilir ve kontrollü bir geçiş süreci** olarak ele alır. Sunulan "
          "destek, sürecin her aşamasında doğru adımı doğru sırayla atmayı sağlayacak "
          "**mentörlük ve yönlendirme** üzerine kuruludur."),
        P("ADC Pathway **sınav odaklı** bir süreçtir; bu nedenle hazırlık kalitesi, doğru "
          "zamanlama ve belge yönetimi sonucu doğrudan etkiler."),
        BAR("1. PROFİL ANALİZİ & YOL PLANI"),
        P("Mentörler tarafından yapılan **iki online görüşme** sonrasında; adayın mevcut "
          "eğitim durumu, klinik deneyimi, vize/ikamet durumu ve hedefleri doğrultusunda "
          "izlenecek adımlar belirlenir. İngilizce ve ADC sınavlarının ne zaman "
          "tamamlanacağı, hangi adımın hangi sırayla atılacağı **net bir yol haritası** "
          "üzerinden planlanır."),
    ],
    dil_yeterliligi("OET"),
    [
        BAR("3. ADC YAZILI SINAV MENTÖRLÜĞÜ"),
        P("Yazılı sınav için mentörlük desteği sunulur. **Sınavın yapısı, senaryo bazlı "
          "sorulara yaklaşım, çalışma stratejisi, kaynak seçimi ve zaman planlaması** "
          "konularında; Avustralya sürecini bilen mentörler adaya birebir yönlendirme sağlar."),
        BAR("4. ADC PRATİK SINAV HAZIRLIĞI"),
        P("Melbourne’da yapılan pratik sınav için hazırlık yönlendirmesi yapılır. **OSCE "
          "istasyonları, maket üzerinde teknik görevler, gerekli ekipman ve sınav dönemi "
          "lojistiği** (seyahat, konaklama) konusunda sürecin fiili işleyişine uygun planlama "
          "desteği verilir."),
        BAR("5. BELGE YÖNETİMİ & AHPRA KAYDI"),
        P("Initial assessment belgeleri, good standing / iyi hâl belgesi, sabıka kaydı ve "
          "İngilizce sonuçlarının **AHPRA’ya doğru sırayla iletilmesi** konusunda yönlendirme "
          "sağlanır. Göç (skills assessment) hedefi olan adaylar için sürecin bu boyutu da "
          "planlamaya dâhil edilir."),
    ],
    whatsapp_and_mentorship(ULKE, [
        "Konaklama ve ev kiralama",
        "Sağlık sigortası ve ulaşım",
        "Banka hesabı ve resmî işlemler",
        "Yaşam düzeni ve şehir adaptasyonu",
    ]),
    # -- kavramlar -----------------------------------------------------------
    [
        H1("KAVRAMLAR & TERİMLER", "(ADC PATHWAY)"),
        P("Avustralya’da diş hekimliği sürecinde sıkça karşılaşılan bazı kavramlar ilk etapta "
          "kafa karıştırıcı olabilir. Aşağıda ADC Pathway kapsamında en çok karşılaşılan temel "
          "terimler sade şekilde açıklanmıştır."),
        DL([
            ("ADC (Australian Dental Council)",
             "Yurt dışında eğitim almış diş hekimlerinin bilgi ve becerilerini değerlendiren "
             "merkezî kurumdur. Belge değerlendirmesi, yazılı sınav ve pratik sınav bu kurum "
             "tarafından yürütülür. Tüm başvurular ADC Connect portalı üzerinden yapılır."),
            ("AHPRA (Australian Health Practitioner Regulation Agency)",
             "Avustralya’da 16 sağlık mesleğinin ulusal kaydını yürüten kurumdur. Diş "
             "hekimleri, AHPRA aracılığıyla ve Dental Board of Australia adına kaydedilir."),
            ("Dental Board of Australia",
             "AHPRA çatısı altında diş mesleğine özel standartları (İngilizce yeterliliği, "
             "sabıka kaydı, kimlik) belirleyen ve kayıt kararlarını veren kuruldur."),
            ("Initial Assessment (İlk Değerlendirme)",
             "ADC sürecinin ilk adımıdır. Bir sınav değil, belge doğrulamasıdır; başarılı "
             "sonuç 7 yıl geçerlidir."),
            ("Written Examination (Yazılı Sınav)",
             "Pearson VUE merkezlerinde girilen, iki gün süren, senaryo bazlı çoktan seçmeli "
             "sınavdır. Diş hekimliği bilimi ve Avustralya pratiğine uygun klinik muhakeme "
             "ölçülür."),
            ("Practical Examination (Pratik Sınav)",
             "Sürecin son ve en zorlu aşamasıdır. Yalnızca Melbourne’daki ADC merkezinde "
             "yapılır; OSCE istasyonları ve maket üzerinde teknik görevlerden oluşur."),
            ("OSCE (Objective Structured Clinical Examination)",
             "Pratik sınavın bir parçasıdır. Her istasyonda hasta yönetimi, klinik muayene ve "
             "diş prosedürleri gibi belirli bir klinik beceri değerlendirilir."),
            ("Pearson VUE",
             "ADC yazılı sınavının fiilen girildiği uluslararası test merkezi ağıdır. Yazılı "
             "sınav için Avustralya’ya gitmek gerekmez; Türkiye dâhil pek çok ülkede girilir."),
            ("İngilizce Yeterliliği (IELTS / OET / PTE)",
             "AHPRA kaydı için istenen İngilizce yeterlilik kanıtıdır. IELTS Academic, OET, "
             "PTE Academic, TOEFL iBT ve Cambridge C1/C2 kabul edilir; 23 Nisan 2026’dan "
             "itibaren minimum puanlar güncellenmiştir."),
            ("Good Standing (İyi Hâl Belgesi)",
             "Kendi ülkenizdeki düzenleyici kurumdan alınan, mesleki kaydınızın geçerli ve "
             "kısıtlamasız olduğunu gösteren belgedir; doğrudan ilgili kurumdan gönderilir."),
            ("Skills Assessment (Beceri Değerlendirmesi)",
             "Yalnızca göç/oturum hedefi olanlar için gereken göçmenlik amaçlı "
             "değerlendirmedir. ADC bunu ana süreç tamamlandıktan sonra ek ücret almadan sunar."),
            ("General Registration (Genel Kayıt)",
             "Avustralya’da diş hekimi olarak serbestçe çalışmaya izin veren kayıt türüdür. "
             "Her iki ADC sınavı geçildikten ve kayıt şartları karşılandıktan sonra alınır."),
        ]),
    ],
    # -- SSS -----------------------------------------------------------------
    [
        H1("SIK SORULAN SORULAR", "(ADC PATHWAY)"),
        DL([
            ("Bu süreç ne kadar sürer?",
             "Süre; adayın İngilizce ve ADC yazılı sınav hazırlığına, sınav takvimine "
             "(Mart/Eylül) ve pratik sınav planlamasına bağlı olarak değişir. Uçtan uca "
             "genellikle 12–24 aydır. Planlı ilerleyen adaylar için süreç yönetilebilir ve "
             "öngörülebilirdir."),
            ("DENTCAMP’ten ne kadar süre faydalanabilirim?",
             "Sürece hâkimiz ve bir yıl sınırı koymuyoruz. Hedefiniz olan Avustralya’da diş "
             "hekimliğine başlayana kadar, süreç kesintisi olmadan yanınızda oluruz."),
            ("Diplomam Avustralya’da otomatik olarak tanınır mı?",
             "Hayır. Diplomanız doğrudan tanınmaz; ancak ABD’den farklı olarak yeniden fakülte "
             "okumanız da gerekmez. Standart yol ADC sürecini tamamlayıp AHPRA’dan çalışma "
             "kaydı almaktır."),
            ("Öğrenciyim, mezuniyetime daha var, erken mi başladım?",
             "Hayır. Öğrenciyken sürece başlamak, özellikle İngilizce hazırlığı açısından "
             "avantaj sağlar. Resmî ADC başvuruları mezuniyet ve tam kayıt sonrası yapılır; "
             "ancak erken başlamak tüm süreci belirgin şekilde hızlandırır."),
            ("Avustralya’ya göç etmem şart mı, yoksa sadece çalışabilir miyim?",
             "İkisi farklı hedeftir. Çalışmak için AHPRA kaydı yeterlidir; göç/oturum "
             "isteniyorsa ayrıca skills assessment gerekir. Hedefi baştan netleştirmek "
             "önemlidir."),
            ("ADC sürecini atlayıp doğrudan AHPRA’ya başvurabilir miyim?",
             "Yalnızca belirli ülkelerin mezunları (Yeni Zelanda’da kayıtlı hekimler ile "
             "İngiltere, İrlanda ve belirli Kanada mezunları) ADC sınavlarını atlayabilir. "
             "Türkiye dâhil diğer tüm ülkeler için ADC süreci zorunludur."),
            ("Yazılı sınava Türkiye’den girebilir miyim?",
             "Evet. Yazılı sınav dünya genelindeki Pearson VUE merkezlerinde yapılır; Türkiye "
             "dâhil pek çok ülkede girilebilir. Yalnızca pratik sınav için Melbourne’a "
             "gitmeniz gerekir."),
            ("Sınavların geçme oranı nedir?",
             "Son yıllarda yazılı + pratik geçme oranları %25 civarına kadar düşmüştür. Ciddi "
             "ve yapılandırılmış bir hazırlık başarı şansını belirgin şekilde artırır."),
            ("Sınav sonuçlarının geçerlilik süresi var mı?",
             "Evet. Initial assessment 7 yıl geçerlidir; yazılı sınav geçerliliği ise "
             "sınırlıdır (resmî sayfada 3 yıl). Pratik sınavı bu süre içinde geçemezseniz "
             "yazılı sonucunuz geçersiz olur."),
            ("Süreç ne kadar maliyetli?",
             "Resmî ADC ve AHPRA ücretleri (3 sınav + kayıt + bir İngilizce testi) yaklaşık "
             "8.400–9.000 AUD’dir. Buna hazırlık, ekipman, belge ve Melbourne seyahati "
             "eklenir. Tek seferde geçme senaryosunda toplam genellikle 12.000–18.000 AUD "
             "bandındadır; kişiye özel bütçe planı mentörünüzle birlikte çıkarılır."),
            ("Çalışma deneyimim yoksa başvurabilir miyim?",
             "Evet. Çalışma deneyimi zorunlu değildir; temel şart tanınan bir üniversiteden "
             "alınmış 4 yıllık tam zamanlı diploma ve kısıtlanmamış mesleki kayıttır. Ancak "
             "klinik deneyim, özellikle pratik sınav hazırlığında avantaj sağlar."),
            ("ADC sınavlarını geçmek iş garantisi verir mi?",
             "Hayır. Sınavları geçmek ve AHPRA’ya kaydolmak Avustralya’da yasal olarak "
             "çalışabilmenizi sağlar; otomatik bir iş garantisi vermez. İş başvuruları ayrı "
             "bir süreçtir ve DENTCAMP bu adımda da yönlendirme sağlar."),
            ("Kayıt sonrası uzmanlaşabilir miyim?",
             "Evet. AHPRA’da genel diş hekimi olarak kaydolduktan sonra, Avustralya’da mevcut "
             "bir uzmanlık alanında specialist registration yoluna başvurulabilir. Şartlar ve "
             "süreler alana göre değişir."),
        ]),
    ],
]

ROADMAP_TITLE = "ADC PATHWAY ROAD MAP"
ROADMAP_SUB = "Avustralya’da Diş Hekimliği Süreci"

ROADMAP = [
    (1, "Belge Değerlendirmesi", "ADC Connect üzerinden başvuru",
     "Diploma değerlendirmesi · 7 yıl geçerli", "ic_belge.png"),
    (2, "Yazılı Sınav", "Pearson VUE · 2 gün · 280 soru",
     "Bilim + klinik muhakeme", "ic_sinav.png"),
    (3, "Pratik Sınav", "Yalnızca Melbourne · 2 gün",
     "OSCE + maket üzerinde teknik görevler", "ic_dis.png"),
    (4, "İngilizce Yeterliliği", "IELTS / OET / PTE / TOEFL",
     "23 Nisan 2026 sonrası güncel puanlar", "ic_dil.png"),
    (5, "AHPRA / Dental Board<br>Kaydı", "General Registration",
     "Good standing · sabıka · İngilizce", "ic_lisans.png"),
]

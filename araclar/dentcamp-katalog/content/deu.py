#!/usr/bin/env python3
"""DENTCAMP: Almanya (Approbation Pathway).

Kaynak metin: BROŞÜR VE TANITIM/deu/broşür metin taslak,.docx
             + BROŞÜR VE TANITIM/deu/Almanya_Dis_Hekimligi_Denklik_Yol_Haritasi.docx
Dil, AUSCAMP Specialist Pathway kataloğunun kurumsal register'ına çevrildi.

DİKKAT (kullanıcıya); iki kaynak yasa tarihinde ÇELİŞİYOR:
  · "broşür metin taslak"  -> 26 Mart 2026 kabul, 1 KASIM 2026 yürürlük
  · "Yol Haritası"         -> 1 TEMMUZ 2026'dan itibaren geçerli
Aşağıda broşür taslağındaki tarih (1 Kasım 2026) kullanıldı. Doğrusu hangisiyse
tek satırda düzeltilir, metin GUNCEL listesinde.

NOT (kullanıcıya), Almanya'da dil şartı Almanca (B2 + FSP) olduğu için MEDCAMP
(OET / medikal İngilizce) bu katalogda yer almıyor. MEDCAMP Almanca da veriyorsa
content/_common.py'deki medcamp() bloğu buraya da eklenebilir.
"""
from build import H1, BAR, P, SUB, UL, DL, BOX, STATS
from content._common import (intro, mentorler, placeholders, medcamp_deutsch,
                             whatsapp_and_mentorship, PHONES)   # noqa: F401

ULKE = "Almanya"

COVER = {
    # Kapak alt bandındaki üç künye — hepsi katalogda zaten geçen bilgiler.
    "kunye": [
        ('SÜRE', '12–24 ay'),
        ('SINAVLAR', 'FSP + Kenntnisprüfung'),
        ('HEDEF', 'Approbation'),
    ],
    "pill": "Almanya’da",
    "title": "Diş Hekimliği\nKariyeri",
    "tag": "| APPROBATION",
    "sub": "(Diş hekimliği öğrencileri ve\ndiş hekimleri için süreç rehberi)",
}

INTRO = intro(ULKE)
MENTORLER_BOLUM = mentorler(ULKE)
MENTOR_YERI = 0        # kadro bu BODY bölümünden sonra: APPROBATION PATHWAY
MENTORS = placeholders(4, ULKE)

# --- Mentör (gerçek) --------------------------------------------------------
# Kaynak: ~/Downloads/Mentör Biyografi ve fotoğraflar/DEU/
# Biyografi mentörün kendi kaleminden; yalnız kısaltıldı ve marka adı çıkarıldı
# (özgün metinde DEUCAMP geçiyordu, bu katalog DENTCAMP'in).
MENTOR_TAM = [dict(
    foto="m_beste_su_ulu.png",
    ad="Dt. Beste Su Ulu",
    meta="DİŞ HEKİMİ & MENTÖR · SCHLESWIG-HOLSTEIN, ALMANYA",
    bio=[
        "2022 yılında Marmara Üniversitesi Diş Hekimliği Fakültesi’nden mezun olduktan "
        "sonra aynı yıl Almanya’ya gelerek ağız, çene ve yüz cerrahisi (MKG) bölümünde "
        "staj yaptım. Bu süreç hem mesleki hem kişisel açıdan çok verimli geçti ve uzun "
        "zamandır aklımda olan Almanya’da kariyer yapma fikrini güçlendirdi.",
        "Türkiye’ye döndükten sonra vize işlemlerimi başlatıp iş aramaya başladım. 2023’te "
        "Almanya’ya yerleşerek Schleswig-Holstein eyaletinde **Kenntnisprüfung** sürecime "
        "başladım. Şu anda sürecin son aşaması olan pratik sınav için randevu bekliyorum; "
        "aynı zamanda **Berufserlaubnis** ile aktif olarak diş hekimliği yapıyorum.",
        "Almanya’ya gelmek isteyen meslektaşlarıma kendi deneyimlerimi ve bu süreçte "
        "edindiğim tecrübeleri aktararak yol göstermeyi çok isterim.",
    ],
)]


BODY = [
    [
        H1("APPROBATION PATHWAY", "(Diş Hekimliği Öğrencileri · Diş Hekimleri)"),
        P("Almanya’da diş hekimliği **düzenlenmiş bir meslektir (reglementierter Beruf).** "
          "Diploma sahibi olmak tek başına yeterli değildir; hasta tedavi edebilmek, sigorta "
          "sistemiyle çalışabilmek ve muayenehane açabilmek için **Approbation** (tam ve "
          "süresiz mesleki lisans) almak zorunludur."),
        P("Bu yol; **dil yeterliliği, denklik başvurusu, bilgi sınavı (Kenntnisprüfung) ve "
          "lisans** adımlarının belirli bir sıra ve sistematik yapı içinde ilerlemesiyle "
          "tanımlanır. Sürecin nihai hedefi, Almanya’da süresiz ve tam yetkili çalışma lisansı "
          "olan **Approbation**’dır."),
        BOX("**İki temel statü vardır. Approbation:** tam, süresiz, ülke genelinde geçerli "
            "lisans; bağımsız çalışma ve muayenehane açma hakkı verir. **Berufserlaubnis "
            "(§13 ZHG):** en fazla 2 yıl geçerli geçici çalışma izni; genelde bir eyaletle "
            "sınırlıdır ve gözetim altında çalışmayı gerektirir. Sınav hazırlığı döneminde "
            "çalışıp deneyim edinmek için kullanılır."),
        BAR("GÜNCEL BİLGİLER (2026)"),
        UL([
            "**26 Mart 2026’da kabul edilen yeni yasayla**, AB dışı diş hekimleri için "
            "**Kenntnisprüfung standart yol** hâline gelmiştir. Belge üzerinden denklik "
            "(Gleichwertigkeitsprüfung) artık yalnızca isteğe bağlı bir seçenektir. Yasa "
            "**1 Kasım 2026** itibarıyla yürürlüğe girmektedir.",
            "**1 Mayıs 2026’dan** itibaren AB dışı mezunlar, Approbation verilmeden önce "
            "sertifikalı kurslarla **radyasyondan korunma (Strahlenschutz)** belgesi sunmak "
            "zorundadır.",
            "**Sınav hakkı sınırlıdır:** ZApprO §118’e göre Kenntnisprüfung’un her bölümü "
            "ayrı ayrı ikişer kez tekrarlanabilir (bölüm başına toplam 3 hak). Hakkı tükenen "
            "aday **Almanya genelinde** bir daha Approbation alamaz.",
            "**Geçiş dönemi:** **1 Kasım 2026’dan önce** başvurusu yapılmış dosyalar, "
            "yetkili makam **31 Aralık 2026’ya kadar** karar verirse eski usulle "
            "sonuçlanabilir. Devam eden dosyalar için hukuki danışmanlık önerilir.",
        ]),
    ],
    [
        BAR("1. ALMANCA DİL YETERLİLİĞİ (B2’DEN FSP’YE)"),
        P("Adayın, klinik ortamda hasta ile **güvenli ve yeterli iletişim** kurabileceğini "
          "kanıtlaması gerekir. Bu iki aşamalıdır: önce **genel B2 seviyesi**, ardından "
          "tıbbi/mesleki Almanca sınavı olan **Fachsprachprüfung (FSP).**"),
        P("FSP, genel dil bilgisinden farklı olarak **hasta görüşmesi (Anamnese), "
          "hekim iletişimi (Arzt-Arzt-Gespräch) ve tıbbi belge yazımı** gibi klinik "
          "iletişim becerilerini ölçer. FSP başarısı, denklik ve lisans sürecinin **ön "
          "koşuludur.**"),
        SUB("Gerekli seviye:"),
        UL([
            "**Genel Almanca:** B2 (telc, Goethe veya ÖSD sertifikasıyla belgelenir).",
            "**Mesleki Almanca:** FSP (Fachsprachprüfung); C1 düzeyinde değerlendirilir.",
            "**B1 seviyesi yeterli değildir.** Bazı eyaletler harici bir mesleki C1 "
            "sertifikasını (ör. telc Deutsch C1 Medizin) FSP’ye eşdeğer kabul edebilir; bu "
            "her eyalette geçerli değildir.",
        ]),
    ],
    [
        BAR("2. DENKLİK BAŞVURUSU (ANERKENNUNG)"),
        P("Diploma ve belgeler, çalışılmak istenen eyaletin yetkili makamına (ilgili "
          "**Landesprüfungsamt / Approbationsbehörde / Zahnärztekammer**) sunulur. Yeni yasayla "
          "birlikte AB dışı diş hekimleri için süreç doğrudan **Kenntnisprüfung’a** "
          "yönlendirilmektedir."),
        P("Makam dosyayı inceler; eğitimde “esasa ilişkin fark” görürse adaya bir "
          "**Defizitbescheid** (eksiklik yazısı) gönderir: bu, Kenntnisprüfung’a girilmesi "
          "gerektiği anlamına gelir. Bu aşamada belgelerin eksiksiz, çevirilerin onaylı ve "
          "dosyanın eyalet beklentilerine uygun olması **kritiktir.**"),
        SUB("Sık istenen belgeler:"),
        UL([
            "**Diploma ve transkript**: apostilli + yeminli tercümeli (ders "
            "içerikleri/saatleri dâhil).",
            "**Mesleki belge (Good Standing)**: Sağlık Bakanlığı’ndan hekimlik/iyi hâl belgesi.",
            "**Dil sertifikaları**: genel Almanca (B2) + FSP sonucu.",
            "**Adli sicil kaydı**: “yurt dışında kullanım” seçeneğiyle; genelde 3 aydan "
            "eski olmamalı.",
            "**Sağlık raporu, CV, çalışma referansları** ve yetkili makamın başvuru formu.",
        ]),
        P("Tüm resmî belgeler için **apostil** (kaymakamlık/valilik) ve Almanya’da tanınan "
          "**yeminli tercüman** çevirisi gerekir."),
    ],
    [
        BAR("3. KENNTNISPRÜFUNG (KP)"),
        P("Kenntnisprüfung, Alman diş hekimliği **devlet sınavının içeriğine dayanan**, Almanca "
          "yapılan bir bilgi sınavıdır. Bir üniversitenin diş hekimliği fakültesinde, devlet "
          "sınav komisyonu önünde yapılır. **ZApprO §§104–118**’e göre üç bölümden oluşur ve "
          "bölümler **sırayla** geçilir:"),
        UL([
            "**Yazılı (schriftlich)**: verilen bir vakaya göre en az iki tedavi planı yazıp "
            "gerekçelendirme (~45 dk).",
            "**Sözlü (mündlich)**: komisyonla mesleki mülakat; yazılı tedavi planı da "
            "tartışmaya dâhil edilebilir (60–90 dk).",
            "**Pratik (praktisch)**: simüle muayenehane ortamında fantom baş üzerinde "
            "uygulama: kron preparasyonu, ölçü, dolgu, kanal tedavisi, cerrahi alet seçimi "
            "(~5 saat, güne yayılmış).",
        ]),
        P("Sınav; **protez (Prothetik), ortodonti (Kieferorthopädie), ağız–çene cerrahisi "
          "(Oralchirurgie / MKG) ve Zahnerhaltung grubu** (endodonti, çocuk diş hekimliği, "
          "periodontoloji) alanlarını kapsar. Ayrıca **acil tıp, klinik farmakoloji, hijyen ve "
          "mesleki hukuk** soruları da sorulur. Not verilmez; komisyon **“denk bilgi düzeyi "
          "mevcut / mevcut değil“** şeklinde değerlendirir."),
        P("Sınav genelde **yılda iki kez** (örn. Mart ve Eylül) yapılır; kayıttan sonra 1–6 ay "
          "içinde başlar. Yaklaşık maliyet **~1.300 €**’dur."),
    ],
    [
        BAR("4. EYALET (BUNDESLAND) SEÇİMİ"),
        P("Diş hekimliği denkliği **eyalet bazında** yürütülür. Doğru eyalet seçimi süreci "
          "aylarca kısaltabilir. Değerlendirilmesi gereken kriterler:"),
        UL([
            "**İşlem/bekleme süresi**: çok başvuru alan eyaletlerde beklemeler uzayabilir.",
            "**Sınav takvimi ve kontenjan**: KP’nin yılda kaç kez yapıldığı ve sıra bekleme "
            "durumu.",
            "**Değerlendirme yaklaşımı**: bazı eyaletler müfredat analizinde daha katıdır.",
            "**Hazırlık kursu imkânı**: KP hazırlık kurslarının ve fantom laboratuvarlarının "
            "yoğunluğu.",
            "**İş ve referans ağı**: bölgedeki klinik yoğunluğu ve Berufserlaubnis ile "
            "çalışma imkânı.",
        ]),
        BOX("Eyaletlere ilişkin genel eğilimler zamanla değişir. Nihai kararı vermeden önce "
            "hedef eyaletin yetkili makamının **güncel işlem süresi ve sınav takvimi** teyit "
            "edilmelidir. 2027’ye kadar KP formatlarının ülke genelinde standartlaştırılması "
            "planlanmaktadır."),
    ],
    [
        BAR("5. STRAHLENSCHUTZ VE APPROBATION’IN VERİLMESİ"),
        P("**Strahlenschutz** (radyasyondan korunma) belgesi, 1 Mayıs 2026’dan itibaren AB "
          "dışı mezunlar için Approbation öncesi şarttır. Ayrıca **adli sicil, sağlık raporu "
          "ve mesleki uygunluk (Zuverlässigkeit)** koşulları da sağlanmalıdır."),
        P("Tüm şartlar tamamlanınca **Approbation belgesi** verilir. Artık "
          "“Zahnarzt/Zahnärztin” unvanıyla **bağımsız çalışılabilir**, sigorta sistemine "
          "kayıt olunabilir ve muayenehane açılabilir."),
        P("Süreç boyunca beklemek yerine, ara adım olarak **Berufserlaubnis** alınarak "
          "Almanya’da fiilen çalışıp KP’ye hazırlanmak da mümkündür."),
    ],
    [
        BAR("6. SÜRE VE MALİYET"),
        P("Toplam süre genellikle **12–24 aydır.** Belgelerin eksiksizliğine, eyaletin "
          "yoğunluğuna, dil seviyesine ve sınav takvimine göre değişir. Dili Türkiye’de "
          "bitirip belge hazırlığını ve başvuruyu paralel yürütmek **en çok zaman kazandıran "
          "stratejidir.**"),
        SUB("Yaklaşık maliyet kalemleri:"),
        UL([
            "Yeminli tercüme + apostil: **500 – 1.500 €**",
            "Approbation başvuru / dosya inceleme: **200 – 600 €**",
            "FSP ve/veya Kenntnisprüfung ücreti: **500 – 1.500 €** (KP ~1.300 €)",
            "Dil kursları (yoğunluğa göre): **2.000 – 6.000 €**",
            "KP hazırlık kursu (opsiyonel): **3.000 – 8.000 €**",
        ]),
        STATS([("12–24 ay", "Uçtan uca tipik süre"),
               ("~1.300 €", "Kenntnisprüfung ücreti"),
               ("3 hak", "Bölüm başına sınav hakkı")]),
        BOX("Almanya’da yaşayan ve şartları sağlayan adaylar, KP hazırlık kursları için İş "
            "Ajansı’ndan (**Agentur für Arbeit**) **Bildungsgutschein** ile %100’e varan "
            "finansman alabilir. Koşullar için ilgili Jobcenter’a danışılmalıdır."),
    ],
    [
        H1("HİZMETLERİMİZ", "(APPROBATION PATHWAY)"),
        P("DENTCAMP, Approbation sürecini; Alman sağlık sistemine uygun şekilde **planlı, "
          "sürdürülebilir ve kontrollü bir geçiş süreci** olarak ele alır. Sunulan destek, "
          "sürecin her aşamasında doğru adımı doğru sırayla atmayı sağlayacak **mentörlük ve "
          "yönlendirme** üzerine kuruludur."),
        P("Bu süreçte **dil, eyalet seçimi ve dosya yönetimi** sonucu doğrudan etkileyen "
          "unsurlardır."),
        BAR("1. PROFİL ANALİZİ & YOL PLANI"),
        P("Mentörler tarafından yapılan **iki online görüşme** sonrasında; adayın mevcut eğitim "
          "durumu, klinik deneyimi ve hedefleri doğrultusunda izlenecek adımlar belirlenir. "
          "**Hangi dil seviyesine ne zaman ulaşılacağı, hangi eyalete başvurulacağı ve denklik "
          "başvurusunun hangi aşamada yapılacağı** net bir yol haritası üzerinden planlanır."),
    ] + medcamp_deutsch(),
    [
        BAR("3. KENNTNISPRÜFUNG (KP) MENTÖRLÜĞÜ"),
        P("Alman diş hekimliği bilgi sınavı **Kenntnisprüfung** için mentörlük desteği "
          "sunulur. Almanya’da aktif çalışan diş hekimi mentörler; **sınavın yazılı, sözlü ve "
          "pratik bölümlerine yaklaşım, sık karşılaşılan konular ve Alman klinik perspektifi** "
          "konusunda deneyime dayalı tavsiyeler verir. Amaç, adayın sınava **doğru stratejiyle "
          "ve Alman sağlık sisteminin bakış açısıyla** hazırlanmasıdır."),
        BAR("4. BELGE, DOSYA & BAŞVURU YÖNETİMİ"),
        P("Gerekli belgelerin, Alman kurumlarının (**Landesprüfungsamt, Zahnärztekammer**) "
          "beklentilerine uygun şekilde hazırlanması konusunda yönlendirme sağlanır. **Belge "
          "listesi, apostil ve yeminli tercüme adımları, başvuru sıralaması ve dosya akışı** "
          "sürecin fiili işleyişine uygun şekilde planlanır."),
    ],
    whatsapp_and_mentorship(ULKE, [
        "Ev kiralama ve Anmeldung (adres kaydı)",
        "Sağlık sigortası ve ulaşım",
        "Banka hesabı ve resmî işlemler",
        "Yaşam düzeni ve şehir adaptasyonu",
    ]),
    [
        H1("KAVRAMLAR & TERİMLER", "(APPROBATION PATHWAY)"),
        P("Almanya’da diş hekimliği sürecinde sıkça karşılaşılan bazı kavramlar ilk etapta kafa "
          "karıştırıcı olabilir. Aşağıda en çok karşılaşılan temel terimler sade şekilde "
          "açıklanmıştır."),
        DL([
            ("Approbation",
             "Almanya’da süresiz ve tüm ülkede geçerli, tam yetkili diş hekimliği çalışma "
             "lisansıdır. Sürecin nihai hedefidir."),
            ("Berufserlaubnis (Geçici Çalışma İzni)",
             "Belirli bir eyalete ve çoğu zaman belirli bir işverene bağlı, en fazla 2 yıllık "
             "geçici çalışma iznidir. Approbation süreci devam ederken fiilen çalışıp KP’ye "
             "hazırlanmak için ara adım olarak kullanılabilir."),
            ("Anerkennung (Denklik)",
             "Yurt dışında alınmış diplomanın Almanya’da tanınması sürecinin genel adıdır. "
             "Otomatik tanınma değil, Alman standartlarının karşılanması anlamına gelir."),
            ("Gleichwertigkeitsprüfung",
             "Diplomanın Alman diş hekimliği eğitimiyle “denk” olup olmadığının belgeler "
             "üzerinden değerlendirilmesidir. Yeni yasayla AB dışı adaylar için artık yalnızca "
             "isteğe bağlı bir seçenektir."),
            ("Kenntnisprüfung (KP)",
             "Alman diş hekimliği devlet sınavının içeriğine dayanan, Almanca yapılan bilgi "
             "sınavıdır. Yazılı, sözlü ve pratik olmak üzere üç bölümden oluşur."),
            ("Fachsprachprüfung (FSP)",
             "Tıbbi/mesleki Almanca sınavıdır, C1 düzeyine göre değerlendirilir. Hasta "
             "görüşmesi, hekim iletişimi ve tıbbi belge yazımı gibi klinik iletişim "
             "becerilerini ölçer. Approbation için başarılması zorunludur."),
            ("Defizitbescheid",
             "Yetkili makamın, eğitimde esasa ilişkin fark tespit ettiğinde gönderdiği "
             "eksiklik yazısıdır. Kenntnisprüfung’a girilmesi gerektiği anlamına gelir."),
            ("ÖSD / telc / Goethe",
             "Almanca genel dil seviyesini belgeleyen resmî sınavlardır. Hangi sertifikanın "
             "geçerli olduğu eyalete göre değişebilir."),
            ("Strahlenschutz",
             "Radyasyondan korunma sertifikasıdır. 1 Mayıs 2026’dan itibaren AB dışı mezunlar "
             "için Approbation öncesi zorunludur."),
            ("ZApprO (Zahnärztliche Approbationsordnung)",
             "Diş hekimliği ruhsat yönetmeliğidir. Kenntnisprüfung’un içeriğini, bölümlerini "
             "ve deneme haklarını (§§104–118) düzenler."),
            ("ZHG (Zahnheilkundegesetz)",
             "Almanya’da diş hekimliği mesleğinin icrasını düzenleyen temel yasadır."),
            ("Landesprüfungsamt / Approbationsbehörde",
             "Denklik ve Approbation başvurularının yürütüldüğü, eyalet düzeyindeki yetkili "
             "resmî makamdır."),
            ("Zahnärztekammer",
             "Eyalet düzeyindeki diş hekimleri meslek odasıdır. Bazı eyaletlerde KP veya FSP "
             "bu oda bünyesinde yürütülür."),
            ("Anmeldung",
             "Almanya’da ikamet adresinin resmî olarak kaydedilmesidir. Banka hesabı, sağlık "
             "sigortası ve birçok resmî işlem için ön koşuldur."),
        ]),
    ],
    [
        H1("SIK SORULAN SORULAR", "(APPROBATION PATHWAY)"),
        DL([
            ("Bu süreç ne kadar sürer?",
             "Toplam süre genellikle 12–24 aydır. Belgelerin eksiksizliğine, eyaletin "
             "yoğunluğuna, dil seviyesine ve sınav takvimine göre değişir. Planlı ilerleyen "
             "adaylar için süreç yönetilebilir ve öngörülebilirdir."),
            ("DENTCAMP’ten ne kadar süre faydalanabilirim?",
             "Sürece hâkimiz ve bir yıl sınırı koymuyoruz. Hedefiniz olan Almanya’da diş "
             "hekimliğine başlayana kadar, süreç kesintisi olmadan yanınızda oluruz."),
            ("Diplomam Almanya’da otomatik olarak tanınır mı?",
             "Hayır. Almanya’da diş hekimliği düzenlenmiş bir meslektir; diploma tek başına "
             "yeterli değildir. Yeni yasayla AB dışı mezunlar için standart yol "
             "Kenntnisprüfung’dur."),
            ("Belge üzerinden denklik (Gleichwertigkeitsprüfung) hâlâ mümkün mü?",
             "26 Mart 2026 tarihli yasayla AB dışı adaylar için bu yol düzenli yol olmaktan "
             "çıkmış, yalnızca isteğe bağlı bir seçenek olarak kalmıştır. Yasa 1 Kasım 2026 "
             "itibarıyla yürürlüğe girmektedir."),
            ("Kaç kez sınava girebilirim?",
             "ZApprO §118’e göre Kenntnisprüfung’un her bölümü ayrı ayrı ikişer kez "
             "tekrarlanabilir (bölüm başına toplam 3 hak). Başarıyla geçilen bölümlerin "
             "tekrarlanmasına gerek yoktur. Hakkı tükenen aday Almanya genelinde bir daha "
             "Approbation alamaz."),
            ("Hangi Almanca seviyesi gerekiyor?",
             "İki düzeyde Almanca gerekir: genel Almanca en az B2 (başvuru ve FSP’ye kayıt ön "
             "koşulu) ve mesleki Almanca C1 (FSP ile kanıtlanır). B1 seviyesi yeterli "
             "değildir."),
            ("Approbation olmadan çalışabilir miyim?",
             "Approbation olmadan bağımsız çalışmak yasaktır. Ancak Berufserlaubnis (en fazla "
             "2 yıllık geçici izin) ile gözetim altında çalışıp bu sırada KP’ye hazırlanmak "
             "mümkündür."),
            ("Hangi eyaleti seçmeliyim?",
             "Denklik eyalet bazında yürütülür ve doğru seçim süreci aylarca kısaltabilir. "
             "İşlem süresi, sınav takvimi ve kontenjan, değerlendirme yaklaşımı, hazırlık "
             "kursu imkânı ve iş ağı birlikte değerlendirilir. Bu analiz mentörünüzle "
             "birlikte yapılır."),
            ("Öğrenciyim, mezuniyetime daha var, erken mi başladım?",
             "Hayır. Öğrenciyken sürece başlamak, özellikle Almanca hazırlığı açısından büyük "
             "avantaj sağlar. Resmî başvurular mezuniyet ve diploma sonrası yapılır; ancak "
             "erken başlamak tüm süreci belirgin şekilde hızlandırır."),
            ("Süreç ne kadar maliyetli?",
             "Tercüme ve apostil 500–1.500 €, başvuru/dosya inceleme 200–600 €, FSP ve/veya "
             "Kenntnisprüfung 500–1.500 € (KP ~1.300 €), dil kursları 2.000–6.000 € ve "
             "opsiyonel KP hazırlık kursu 3.000–8.000 € bandındadır. Kişiye özel bütçe planı "
             "mentörünüzle birlikte çıkarılır."),
            ("Hazırlık kursu için destek alabilir miyim?",
             "Almanya’da yaşayan ve şartları sağlayan adaylar, KP hazırlık kursları için "
             "Agentur für Arbeit’ten Bildungsgutschein ile %100’e varan finansman alabilir. "
             "Koşullar için ilgili Jobcenter’a danışılmalıdır."),
            ("Approbation almak iş garantisi verir mi?",
             "Hayır. Approbation, Almanya’da yasal olarak bağımsız çalışabilmenizi sağlar; "
             "otomatik bir iş garantisi vermez. İş başvuruları ayrı bir süreçtir ve DENTCAMP "
             "bu adımda da yönlendirme sağlar. Süreç devam ederken Berufserlaubnis ile "
             "çalışmak da mümkündür."),
            ("Belgelerimin apostilli olması şart mı?",
             "Evet. Tüm resmî belgeler için apostil (kaymakamlık/valilik) ve Almanya’da "
             "tanınan yeminli tercüman çevirisi gerekir. Eksik veya onaysız belge süreci "
             "geciktirir."),
        ]),
    ],
]

ROADMAP_TITLE = "APPROBATION ROAD MAP"
ROADMAP_SUB = "Almanya’da Diş Hekimliği Süreci"

ROADMAP = [
    (1, "Almanca Dil<br>Yeterliliği", "Genel Almanca B2",
     "telc / Goethe / ÖSD sertifikası", "ic_dil.png"),
    (2, "Fachsprachprüfung", "Mesleki Almanca: C1",
     "Anamnese · hekim iletişimi · belge", "ic_mentor.png"),
    (3, "Denklik Başvurusu", "Landesprüfungsamt’a dosya",
     "Apostilli belgeler · eyalet seçimi", "ic_belge.png"),
    (4, "Kenntnisprüfung", "Yazılı, sözlü ve pratik",
     "Devlet sınav komisyonu önünde", "ic_sinav.png"),
    (5, "Approbation", "Süresiz tam lisans",
     "Strahlenschutz + bağımsız çalışma", "ic_lisans.png"),
]

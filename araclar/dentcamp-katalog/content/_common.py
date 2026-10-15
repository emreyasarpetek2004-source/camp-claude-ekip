#!/usr/bin/env python3
"""Dört ülkenin ortak kullandığı metin blokları.

Ülkeye göre değişmeyen ne varsa burada durur; ülke dosyaları bunu içeri alır.
Dil, AUSCAMP Specialist Pathway kataloğunun kurumsal register'ına göre yazıldı:
üçüncü tekil ("yürütür", "sağlanır"), broşürlerdeki birinci çoğul ("yürütürüz")
kullanılmıyor.
"""
import theme as _T
from build import MGRID, MCTA, CARDS3, H1, BAR, P, SUB, UL, CTA

# DENTCAMP satış hattı 19 Ağustos 2026'da değişti; etiket de "CAMP Hattı" değil,
# katalog DENTCAMP'in.
PHONES = [("DENTCAMP Hattı:", "+90 552 000 78 38")]

# Ülke adlarının son ünlüsü ekin kalın/ince olmasını belirliyor. Sabit "'da/'daki/'ya"
# yazılınca "ABD'daki", "İngiltere'ya" gibi hatalar çıkıyordu — kaynak broşürler doğru
# yazmıştı, hata derleyicideydi.
_SUF = {
    "Almanya":    ("da", "daki", "ya"),
    "Avustralya": ("da", "daki", "ya"),
    "ABD":        ("de", "deki", "ye"),
    "İngiltere":  ("de", "deki", "ye"),
}


def loc(c):
    """Almanya'da / ABD'de"""
    return f"{c}’{_SUF[c][0]}"


def locd(c):
    """Almanya'daki / ABD'deki"""
    return f"{c}’{_SUF[c][1]}"


def dat(c):
    """Almanya'ya / ABD'ye"""
    return f"{c}’{_SUF[c][2]}"


# Toplu mentör listesi — biyografi YOK, yalnız yuvarlak fotoğraf ve künye.
# Dört broşürde de KADRONUN TAMAMI basılır; değişen tek şey sıra.
# Şehir/eyalet bilgisi mentörlerin kendi biyografilerinden alındı; biyografisinde
# şehir geçmeyen iki kayıtta (Gizem Subaşı, Damla Engin Arpacı) yalnız ülke yazıyor.
# İsim kalıbı: unvan sonda ise (DDS/BDS) başta "Dt." YOK, yoksa "Dt." var. Aksi
# halde aynı satırda "Dt. R. Damla Engin Arpacı, BDS" ile "Ayşe Nil Koçak, DDS"
# yan yana düşüyor; üstelik en uzun pill komşusuna 4,8pt kalıyordu.
# Fotoğraflar tools/prep_mentor_kesim.py ile üretilir (arka planı silinmiş kesim).
MENTORLER = [
    dict(foto="kart_beste_su_ulu.jpg", ulke="deu", ad="Dt. Beste Su Ulu",
         alt=["Diş Hekimi & Mentör", "Schleswig-Holstein, Almanya"]),
    dict(foto="kart_enes_yildiz.jpg", ulke="deu", ad="Dt. Enes Yıldız",
         alt=["Diş Hekimi & Mentör", "Hennef, Almanya"]),
    dict(foto="kart_ilke_aydin_demirel.jpg", ulke="deu", ad="İlke Aydın Demirel, DDS",
         alt=["Diş Hekimi & Mentör", "Bavyera, Almanya"]),
    dict(foto="kart_gizem_subasi.jpg", ulke="deu", ad="Dt. Gizem Subaşı",
         alt=["Diş Hekimi & Mentör", "Almanya"]),
    dict(foto="kart_merve_olcay_duman.jpg", ulke="deu", ad="Dt. Merve Olcay Duman",
         alt=["Diş Hekimi & Mentör", "Hamburg, Almanya"]),
    dict(foto="kart_gulce_ugurlu.jpg", ulke="deu", ad="Dt. Gülçe Uğurlu",
         alt=["Diş Hekimi & Mentör", "Schleswig-Holstein, Almanya"]),
    dict(foto="kart_ayse_nil_kocak.jpg", ulke="usa", ad="Ayşe Nil Koçak, DDS",
         alt=["Diş Hekimi & Mentör", "New York, ABD"]),
    dict(foto="kart_mustafa_kemal_atay.jpg", ulke="usa", ad="Dt. Mustafa Kemal Atay",
         alt=["Diş Hekimi & Mentör", "Boston, ABD"]),
    dict(foto="kart_buse_yazici.jpg", ulke="usa", ad="Dt. Buse Yazıcı",
         alt=["Diş Hekimi & Mentör", "Boston, ABD"]),
    dict(foto="kart_damla_engin_arpaci.jpg", ulke="uk", ad="R. Damla Engin Arpacı, BDS",
         alt=["Diş Hekimi & Mentör", "İngiltere"]),
    dict(foto="kart_anita_gozubuyuk.jpg", ulke="aus", ad="Dt. MSc. Anita Gözübüyük",
         alt=["Diş Hekimi & Mentör", "Melbourne, Avustralya"]),
    # ulke=None: hedef ülke kadrosunda değil, sıralamada en sona gidiyor.
    # bayrak="tur": rozet yine de basılıyor, Türkiye'den koordine ediyor.
    dict(foto="kart_semanur_terzi.jpg", ulke=None, bayrak="tur",
         ad="Dt. Semanur Terzi", alt=["Genel Koordinatör", "İstanbul"]),
]

# Broşürün ülkesi listede başa geçtikten sonra kalanların sırası.
MENTOR_SIRA = ["deu", "usa", "uk", "aus"]


def ulke_key(country):
    """"Almanya" -> "deu" """
    return {c.name: c.key for c in _T.COUNTRIES.values()}[country]


def mentor_sirasi(country):
    """Broşürün ülkesinin mentörleri başta; ülkesi olmayan kayıt (koordinatör) sonda.

    Okuyucu ilk satırda kendi hedef ülkesindeki kadroyu, sonraki satırlarda ağın
    tamamını görüyor. 12 kart = tam 3 satır, hangi broşür olursa olsun boş hücre
    kalmıyor."""
    key = ulke_key(country)
    sira = [key] + [k for k in MENTOR_SIRA if k != key]
    return ([m for k in sira for m in MENTORLER if m["ulke"] == k]
            + [m for m in MENTORLER if m["ulke"] is None])


def mentorler(country):
    """MENTÖRLERİMİZ bölümü: kendi sayfasında, kadronun tamamı + iletişim şeridi.

    Şerit sonradan eklendi: 12 yuvarlak portre, eski 4:5 kartlardan kısa olduğu
    için sayfanın altında 143,7pt (yüksekliğin %17'si) boş kalıyordu. Şerit hem
    o boşluğu kapatıyor hem de kataloğun en çok bakılan sayfasına site ve CAMP
    hattını koyuyor; daha önce bu sayfada hiç iletişim bilgisi yoktu.

    Eskiden BAR ile sayfa 2'nin alt yarısında üç kişiydi ve grid'in dördüncü hücresi
    boş kalıyordu. Kadro 12 kişiye çıkınca bölüm H1 ile kendi sayfasına alındı;
    H1 pack() içinde yeni sayfa açtığı için ek bir düzenleme gerekmiyor."""
    # İngiltere ve Avustralya'da hedef ülkenin tek mentörü var; çoğul cümle o iki
    # broşürde tek kartın üstünde duruyordu.
    n = sum(1 for m in MENTORLER if m["ulke"] == ulke_key(country))
    sira = (f"Listede önce **{country} kadrosu**, ardından diğer ülkelerdeki "
            f"mentörler yer alır." if n > 1 else
            f"Listede önce **{loc(country)} görev yapan mentör**, ardından diğer "
            f"ülkelerdeki kadro yer alır.")
    return [
        H1("MENTÖRLERİMİZ"),
        P("DENTCAMP mentör ağı, hedef ülkede aktif olarak çalışan ve bu süreci **bizzat "
          "tamamlamış** diş hekimlerinden oluşur. Her mentör; denklik ve başvuru "
          "sürecinden sınav hazırlığına, işe yerleşmeden sistem adaptasyonuna kadar "
          "**gerçek saha deneyimini** paylaşır."),
        P(sira),
        MGRID(mentor_sirasi(country)),
        MCTA(),
    ]


def mentorler_toplu():
    """MENTÖRLERİMİZ bölümünün toplu katalog sürümü.

    `mentorler(country)` kadroyu hedef ülkeye göre sıralar ve "önce <ülke>
    kadrosu" cümlesini kurar. Toplu katalogda hedef ülke yok: kadro dört ülkeye
    göre gruplanmış hâlde, MENTOR_SIRA sırasıyla basılır."""
    # Sıra, kataloğun ülke sırasıyla aynı (MENTOR_SIRA değil): okuyucu ülke
    # sayfalarını Almanya → Avustralya → İngiltere → ABD sırasıyla okuyor,
    # kadro da aynı sırada görünmeli. Ülkesi olmayan kayıt (koordinatör) sona.
    duzen = ["deu", "aus", "uk", "usa"]
    sira = sorted(MENTORLER, key=lambda m: (duzen.index(m["ulke"])
                                            if m["ulke"] in duzen else 99))
    return [
        H1("MENTÖRLERİMİZ"),
        P("DENTCAMP mentör ağı, hedef ülkede aktif olarak çalışan ve bu süreci **bizzat "
          "tamamlamış** diş hekimlerinden oluşur. Her mentör; denklik ve başvuru "
          "sürecinden sınav hazırlığına, işe yerleşmeden sistem adaptasyonuna kadar "
          "**gerçek saha deneyimini** paylaşır."),
        P("Kadro **dört ülkeye** dağılmıştır. Hangi ülkeyle ilerlenirse ilerlensin, süreci "
          "o ülkede bizzat tamamlamış bir mentör eşlik eder; ülke kararı henüz "
          "verilmemişse karşılaştırma da bu kadronun deneyimi üzerinden yapılır."),
        MGRID(sira),
        MCTA(),
    ]


def intro(country):
    """DENTCAMP nedir?: giriş cümlesi + üç kart.

    Mentör bölümü eskiden buraya ekliydi. Kadro 12 kişiye çıkıp bölüm kendi
    sayfasını isteyince (610pt) sayfa 2'de yalnız bu 185pt'lik giriş kalıyordu;
    artık mentörler MENTORLER_BOLUM olarak ülke dosyasından geçiyor ve
    Catalog.body_pages() onu yol haritası özetinden sonraya yerleştiriyor.

    Eskiden üç paragraf düz akıyordu ve sayfanın yarısı boş kalıyordu; aynı bilgi
    kart olarak hem daha hızlı okunuyor hem sayfayı dolduruyor."""
    return [
        H1("DENTCAMP NEDİR?"),
        P("DENTCAMP, yurt dışında kariyerlerini sürdürmek isteyen diş hekimleri için "
          "nitelikli çözümler sunan, **diş hekimliği alanına özel bir eğitim ve "
          "danışmanlık kurumudur.**"),
        CARDS3([
            ("Ne yapıyoruz",
             "Almanya, Avustralya, ABD ve İngiltere olmak üzere **dört ülkede** diş "
             "hekimlerinin denklik ve lisans süreçlerini baştan sona yönetiriz."),
            ("Nasıl yürütüyoruz",
             f"Sınav süreçlerinden belge yönetimine, dil yeterliliğinden {locd(country)} "
             f"yeni hayatınıza uzanan **her aşamayı doğru sırayla** yürütürüz."),
            # Eskiden "{loc(country).capitalize()} aktif çalışan" yazıyordu:
            # ABD kataloğunda "Abd'de" basılıyordu ve tek mentörlü ülkelerde çoğul
            # iddia oluyordu. Ağın tamamına atıf ikisini de çözüyor.
            ("Kimlerle",
             "Dört ülkede aktif çalışan **deneyimli diş hekimi mentörler** ve "
             "Türkiye’de süreci koordine eden yönetim ekibi."),
        ]),
    ]


# Fotoğrafı/ismi henüz belli olmayan mentör kartı.
# Anlaşmalar tamamlanınca ("dosya.png", "Ad Soyad", [...]) satırlarıyla değiştirilir.
def placeholders(n, country):
    return [("", "Mentör", ["Diş Hekimi & Mentör", country, ""])] * n


# Sınavın ne olduğu ülkeye göre değişiyor: OET tıbbi İngilizce, IELTS ve TOEFL
# akademik. Eskiden üçü için de "sağlık profesyonellerine özel tıbbi İngilizce
# sınavı" yazıyordu.
_DIL_TANIM = {
    "OET": "Sağlık profesyonellerine özel tıbbi İngilizce sınavı olan **OET**",
    "IELTS": "GDC’nin kabul ettiği akademik İngilizce sınavı **IELTS Academic**",
    "TOEFL": "Programların istediği akademik İngilizce sınavı **TOEFL**",
}


def dil_yeterliligi(exam="OET", num="2. ", marka="MEDCAMP"):
    """İngilizce dil yeterliliği hizmeti.

    AUSCAMP Specialist Pathway kataloğundaki "DİL YETERLİLİĞİ SÜRECİ (OET) X MEDCAMP"
    bölümünün diş hekimliğine uyarlanmış hâli. Broşür taslaklarında bu bölüm tek
    paragraftı; katalogda hizmetin kapsamı açıkça anlatılıyor.

    ABD kataloğunda bu blok ayrıca yazılıydı ve kaynakta olmayan iki vaat içeriyordu
    ("online canlı ders", ayrıca "mentörümüzün" birinci çoğul iyelik). Üç katalog da
    aynı bloğu kullanınca hizmet anlatımı tek yerden yürüyor.

    2 Eylül 2026 (kullanıcı): **bu bölüm yalnız AVUSTRALYA kataloğunda basılıyor.**
    DENTCAMP İngiltere ve ABD sürecinde dil eğitimi/desteği sağlamıyor, o iki
    katalogdan bölüm tamamen çıkarıldı (dil ŞARTI değişmedi: mevzuat bölümlerindeki
    IELTS/OET ve TOEFL maddeleri aynen duruyor). Almanya'nın karşılığı
    medcamp_deutsch(). Fonksiyon adı bu turda medcamp() -> dil_yeterliligi() oldu.

    `marka=None` markayı basmadan aynı bölümü üretir; şu an hiçbir katalog
    kullanmıyor, ara adımda İngiltere ve ABD için yazılmıştı.
    """
    baslik = (f"{num}DİL YETERLİLİĞİ SÜRECİ ({exam}) X {marka}" if marka
              else f"{num}DİL YETERLİLİĞİ SÜRECİ ({exam})")
    kurum = f"**{marka}** bünyesinde, adayın" if marka else "Adayın"
    return [
        BAR(baslik),
        P(f"{_DIL_TANIM[exam]} için süreç, adayın mevcut seviyesinin belirlenmesiyle "
          f"başlar. {kurum} seviyesine ve hedef takvimine uygun "
          f"bir çalışma programı oluşturulur."),
        SUB("Eğitim süreci:"),
        UL([
            "**Seviye tespiti** ile başlangıç noktası belirlenir.",
            "Uzman mentör rehberliğinde **kişiye özel çalışma programı** hazırlanır.",
            f"**Speaking, Writing, Reading, Listening** becerileri {exam} formatına uygun "
            f"şekilde çalışılır.",
            f"**İnteraktif testler ve deneme sınavları** sayesinde adaylar {exam} formatına "
            f"birebir pratik yapma imkânı bulur.",
            "İhtiyaca göre **birebir mentörlük** desteği sağlanır.",
        ]),
        P("Amaç; yalnızca sınavı geçmek değil, **klinik ortamda güvenli ve etkili iletişim "
          "kurabilecek dil yeterliliğini** kazandırmaktır."),
    ]


def medcamp_deutsch():
    """Almanca dil eğitimi hizmeti: MEDCAMP DEUTSCH (A1–B2 + FSP).

    2 Eylül 2026: hizmetin adı ALMANGO iken MEDCAMP DEUTSCH oldu (kullanıcı).
    Fonksiyon adı da almango() -> medcamp_deutsch() olarak değişti.

    MEDCAMP bloğunun Almanya karşılığı. FSP eğitimi de pakete dâhil olduğu için
    ayrı bir "FSP mentörlüğü" maddesi tutulmuyor: aksi hâlde aynı şey iki kez
    anlatılmış oluyordu.

    Almanya kataloğunda bu blok (o zamanki adıyla ALMANGO) İKİ KEZ anlatılıyordu: bir kez burada, bir kez de
    APPROBATION PATHWAY bölümünün içinde (deu.py, 08.08.2026 sesli anlatımından).
    Örtüşen vaatler (online canlı ders, portal erişimi, konuşma dersi, seviye
    tespiti, yapay zekâ) iki blokta ayrı ayrı sayılıyordu; üstelik ikincisi mevzuat
    bölümünün ortasında duruyordu. İki blok burada birleştirildi, hizmet anlatımı
    yalnız HİZMETLERİMİZ'de kaldı.

    Sesli anlatımda "emin değiliz" denen iki madde (yazma metinlerinin yapay zekâ ve
    hoca tarafından değerlendirilmesi, konuşmanın yapay zekâ ile analiz edilmesi)
    BİLİNÇLİ OLARAK YAZILMIYOR: kesinleşmemiş özellik basılı satış belgesine girmez.
    Bu iki iddia birleştirme öncesinde satır içi blokta basılıyordu.
    """
    return [
        BAR("2. ALMANCA DİL EĞİTİMİ (A1–B2 + FSP) X MEDCAMP DEUTSCH"),
        P("Almanya sürecinin **en kritik ve en çok elenen aşaması dildir;** dil "
          "yeterliliği olmadan Approbation süreci ilerlemez. Bu nedenle süreç, "
          "adayın mevcut seviyesinin belirlenmesiyle başlar. **ÖSD sınav merkezi "
          "akreditasyonuna sahip MEDCAMP DEUTSCH** bünyesinde **A1’den B2’ye** kadar tüm "
          "seviyeler ve **mesleki Almanca sınavı FSP hazırlığı** tek pakette "
          "yürütülür."),
        SUB("Eğitim süreci:"),
        UL([
            "**Seviye tespiti** ile başlangıç noktası belirlenir: sıfırdan "
            "başlayanlar dâhil.",
            "**A1 → A2 → B1 → B2** basamakları hedef takvime göre sıralanır ve "
            "**kişiye özel çalışma programı** hazırlanır.",
            "Her kurun kendi **Aufgabe** (alıştırma) seti vardır; platformda ayrıca "
            "**sınırsız ek Aufgabe** bulunur: yazma, boşluk doldurma ve dinleme.",
            "Sistem yapılan alıştırmayı değerlendirip **anında geri bildirim** verir; "
            "hatanın hangi konuda yoğunlaştığını (ör. Akkusativ) tespit eder ve o "
            "konuya yönlendirir.",
            "**Online canlı dersler** ve **kayıtlı dersler** birlikte sunulur; "
            "kaçırılan ya da tekrar edilmek istenen konulara istenildiği zaman "
            "dönülebilir. **Ders portalı** üzerinden materyallere, kayıtlara ve "
            "alıştırmalara erişilir.",
            "**Speaking Club** ve **birebir ders** ayrı olarak yürütülür: konuşma, "
            "sınavın ve klinik ortamın en çok zorlayan tarafı; randevu hocaların "
            "takvimi üzerinden alınır.",
            "**Kelime kartları ve tekrar egzersizleriyle** düzenli pekiştirme yapılır.",
            "**Yapay zekâ destekli uygulama** ile aday ders dışında da pratik "
            "yapar; çalışma verisi düzenli olarak analiz edilir ve eksik kalan "
            "konular takip edilir.",
            "**telc / Goethe / ÖSD** sınavlarına yönelik hazırlık ve **deneme "
            "sınavları** yapılır; MEDCAMP DEUTSCH bir **ÖSD sınav merkezi** olduğu için "
            "adaylar sınava hazırlandıkları yerde girebilir.",
            "**FSP (Fachsprachprüfung) eğitimi pakete dâhildir:** hasta görüşmesi "
            "(Anamnese), hekim iletişimi (Arzt-Arzt-Gespräch) ve tıbbi belge "
            "yazımı ayrı ayrı çalışılır.",
        ]),
        P("Amaç; yalnızca sertifika almak değil, **klinik ortamda hastayla ve "
          "hekimlerle güvenle iletişim kurabilecek** dil yeterliliğini "
          "kazandırmaktır."),
    ]


def whatsapp_and_mentorship(country, life_items):
    """Her broşürde ortak olan iki hizmet bloğu: katalog diline çevrilmiş hâli."""
    return [
        BAR("KİŞİYE ÖZEL WHATSAPP GRUBU"),
        P("Sorulara en hızlı ve etkili cevabı verebilmek amacıyla her danışan için "
          "**kişiye özel bir grup** kurulur. Grupta biri primer, diğerleri sekonder olmak "
          "üzere **birden fazla mentör** bulunur. Tüm sınav, başvuru, belge ve süreç "
          "adımları bu grup üzerinden bireysel olarak yürütülür."),
        BAR("A’DAN Z’YE MENTÖRLÜK DESTEĞİ"),
        P(f"Süreç boyunca adaylara, **{loc(country)} bu yolu bizzat tamamlamış diş hekimi "
          f"mentörler** eşlik eder. Bu destek, teorik yönlendirmelerden ziyade **gerçek saha "
          f"deneyimine dayalı** bir rehberlik sunar. Amaç, adayın süreci yalnız başına değil; "
          f"**{country} sistemini içeriden bilen hekimlerin deneyimiyle** güvenli ve bilinçli "
          f"şekilde ilerletmesidir."),
        P(f"Mentörlük yalnızca mesleki adımlarla sınırlı değildir. Adaylar, {dat(country)} "
          f"yerleşme sürecinde günlük yaşamla ilgili konularda da yönlendirilir:"),
        UL(life_items),
        P(f"Bu sayede adaylar, mesleki olduğu kadar **sosyal anlamda da daha hızlı ve "
          f"güvenli bir adaptasyon** süreci yaşar."),
        # "ilk görüşme ücretsizdir" çıkarıldı: bu broşür ilk görüşmeyi zaten
        # yapmış kişilere gönderiliyor.
    ]

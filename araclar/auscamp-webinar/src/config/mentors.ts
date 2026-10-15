// AUSCAMP mentor & instructor team — names, roles, photos and bios sourced
// from auscamp.com.tr (/egitmen/*). Photos live under /public/speakers/.
export interface Mentor {
  name: string;
  role: string;
  photo?: string;
  /** object-position for the circular crop so the face stays centered. */
  objectPosition?: string;
  bio?: string;
}

export const mentors: Mentor[] = [
  {
    name: "Dr. Fidan Şenova",
    role: "Co-Founder & Mentör",
    photo: "/speakers/fidan-senova.jpg",
    objectPosition: "50% 28%",
    bio: "Çukurova Üniversitesi Tıp Fakültesi 2019 mezunu. Tıp eğitimi boyunca IFMSA, TurkMSIC, UNHCR ve UNFPA ile pek çok ulusal ve uluslararası halk sağlığı çalışmasında bulundu. 15 yılı aşkın süredir Türkçe-İngilizce medikal çevirmenlik yapıyor. 2021'den beri Melbourne'da yaşıyor, 2023'ten beri tıp eğitimi alanında uluslararası kapasitede çalışıyor. AUSCAMP'in kurucularından ve mentörlerinden biri.",
  },
  {
    name: "Doç. Dr. İbrahim Ethem Cakcak",
    role: "Genel Cerrah & Mentör",
    photo: "/speakers/ethem-face.jpg",
    objectPosition: "50% 50%",
    bio: "2005'te İstanbul Üniversitesi Cerrahpaşa İngilizce Tıp'tan mezun oldu; 2006-2012 arasında aynı fakültede Genel Cerrahi uzmanlığını tamamladı. 2016'da Trakya Üniversitesi'nde akademik hayata başladı, 2023'te doçent oldu; 2022'de EBSQ ile FEBS-C unvanını kazandı. RACS tarafından 'Substantially Comparable' değerlendirildi ve Şubat 2025'ten beri NSW'de Wollongong Devlet Hastanesi ve Üniversitesi'nde Upper GI Fellow olarak çalışıyor. Cerrahi branşların uzmanlık denkliğinde destek sağlıyor.",
  },
  {
    name: "Uzm. Dr. Duygu Batu",
    role: "Dahiliye Uzmanı & Mentör",
    photo: "/speakers/duygu-batu.jpg",
    objectPosition: "50% 30%",
    bio: "2009 Marmara Üniversitesi İngilizce Tıp mezunu; 2010-2015 arasında İstanbul Üniversitesi Çapa'da İç Hastalıkları uzmanlığını tamamladı. 2015'te diyabetik nefropati araştırması için Avustralya'ya geldi. Standard ve Specialist Pathway üzerinden 2021'de FRACP unvanını aldı. 2021'den beri karavanıyla Avustralya'yı gezerken farklı eyaletlerde dahiliye uzmanı olarak görev yapıyor. Dahili branşların denklik sürecinde danışman.",
  },
  {
    name: "Doç. Dr. Tolga Karacan",
    role: "Kadın Hast. ve Doğum Uzmanı & Mentör",
    photo: "/speakers/tolga-karacan.jpg",
    objectPosition: "50% 25%",
    bio: "2002-2008 İstanbul Üniversitesi Cerrahpaşa Tıp mezunu; 2008-2013 Bağcılar EAH'de Kadın Hastalıkları ve Doğum uzmanlığını aldı. 2019'da doçent oldu. 2023'te RANZCOG tarafından 'Partial Comparable' değerlendirildi; 2024'ten beri Canberra Hospital'da Senior Registrar olarak görev yapıyor. Kadın doğum alanında Avustralya uzmanlık denkliği süreçlerinde destek sağlıyor.",
  },
  {
    name: "Dr. Gizem Pehlivan",
    role: "Mentör & Eğitmen",
    photo: "/speakers/gizem-pehlivan.jpg",
    objectPosition: "50% 30%",
    bio: "2019 Çanakkale On Sekiz Mart Üniversitesi Tıp mezunu. Öğrencilik yıllarında Avustralya'da doktorluğa karar verdi ve 2022'de iş bularak taşındı. Tıp eğitimi ve sağlık hakkına erişimde eşitlik üzerine çalışmalar yapıyor. 2025'ten beri AUSCAMP ile denklik sürecinde mentör olarak destek sağlıyor.",
  },
  {
    name: "Dr. Onur Uysal",
    role: "Mentör & Eğitmen",
    photo: "/speakers/onur-uysal.jpg",
    objectPosition: "50% 18%",
    bio: "2014 Gazi Üniversitesi Tıp mezunu. Mezuniyet sonrası Türkiye'nin çeşitli yerlerinde acil serviste pratisyen hekim olarak görev yaptı. 2023'ten beri Queensland'da acil serviste önce RMO, ardından PHO pozisyonunda çalışıyor. AUSCAMP aracılığıyla Avustralya'ya göç etmek isteyen doktorlara danışmanlık sunuyor.",
  },
  {
    name: "Dr. Çağlar Aktuna",
    role: "Mentör & Eğitmen",
    photo: "/speakers/caglar-aktuna.jpg",
    objectPosition: "50% 28%",
    bio: "1995 doğumlu; lise mezuniyetine dek Kıbrıs'ta yaşadı. 2013-2019 arasında Çukurova Üniversitesi Tıp Fakültesi'ni tamamladı. 2019'da Kıbrıs'ta Dr. Burhan Nalbantoğlu Devlet Hastanesi'nde göreve başladı ve 2022 sonuna dek çeşitli hastanelerde hizmet verdi. 2022'de Working Holiday Visa ile Melbourne'a gitti, 2 yıl yaşadı. 2025'ten beri AUSCAMP'te danışmanlık süreçlerinde destek sağlıyor.",
  },
  {
    name: "Dr. İlayda Ertürk",
    role: "Mentör",
    photo: "/speakers/ilayda-erturk.jpg",
    objectPosition: "50% 22%",
    bio: "2024 Marmara Üniversitesi İngilizce Tıp mezunu. DHY sürecini beklerken Yeni Zelanda'ya geldi ve denklik sınavlarını başarıyla tamamladı. Şu anda Genel Cerrahi departmanında PGY-1 olarak RMO pozisyonunda çalışıyor. Bu süreçte edindiği deneyimleri AUSCAMP mentörlüğü kapsamında paylaşıyor.",
  },
  {
    name: "Dt. Anita Gözübüyük",
    role: "Diş Hekimi & Mentör",
    photo: "/speakers/anita-face.jpg",
    objectPosition: "50% 50%",
    bio: "2010'da Varşova Tıp Üniversitesi'nden diş hekimliği diplomasını aldı. Türkiye'de Marmara Üniversitesi'nde Pediatrik Diş Hekimliği yüksek lisansını tamamladı. Ailesiyle Avustralya'ya yerleştikten sonra Avustralya Diş Hekimliği Konseyi ile denklik sürecini yürüttü ve 2025'te Avustralya'da diş hekimliği ruhsatını elde etti. Diş hekimliği denklik süreçlerinde meslektaşlarına destek oluyor.",
  },
  {
    name: "Dr. Burak Şenocak",
    role: "Genel Koordinatör",
    photo: "/speakers/burak-senocak.jpg",
    objectPosition: "50% 8%",
    bio: "İstanbul Tıp Fakültesi'nden üç farklı alanda (Bilimsel, Sanat, Sosyal Farkındalık) dekanlık ödülü alarak mezun oldu. Tıp eğitimi sırasında TurkMSIC'te akran eğitmenliği (2018-21) ve Ulusal Direktörlük (2020-21) pozisyonlarında bulundu. 2024'ten beri AUSCAMP'te genel koordinatör olarak süreçlere destek sağlıyor.",
  },
  {
    name: "Dr. Başak Karazağ",
    role: "Danışan Koordinatörü",
    photo: "/speakers/basak-karazag.jpg",
    objectPosition: "50% 35%",
    bio: "Bahçeşehir Üniversitesi Tıp Fakültesi mezunu. Tıp eğitimi sırasında EMSA'da (Avrupa Tıp Öğrencileri Birliği) başkanlık dahil çeşitli pozisyonlarda aktif rol aldı ve Türkiye Girişimcilik Vakfı 2021 fellow'larından biri oldu. 2024'ten beri AUSCAMP'te danışman olarak süreçlere destek sağlıyor.",
  },
];

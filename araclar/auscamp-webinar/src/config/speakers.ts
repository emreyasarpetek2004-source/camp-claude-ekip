// Speaker profiles + photos, kept separate from webinars.ts so that data file
// stays pristine. Keyed by webinar slug (a webinar can have >1 speaker).
//
// Photos live under /public/speakers/. Missing photo -> SpeakerAvatar falls
// back to initials automatically. `objectPosition` fine-tunes the crop for
// non-headshot photos (e.g. full-body shots).
//
// NOTE: bios are intentionally short and tied to each speaker's given title +
// the webinar topic. Zenginleştirmek için gerçek özgeçmiş bilgileriyle güncelle.
export interface SpeakerProfile {
  name: string;
  title?: string;
  photo?: string;
  objectPosition?: string;
  bio?: string;
}

export const webinarSpeakers: Record<string, SpeakerProfile[]> = {
  "cv-is-basvurulari-4-eki": [
    {
      name: "Doç. Dr. İbrahim Ethem Cakcak",
      title: "Genel Cerrahi Uzmanı, FEBS-C · Mentör",
      photo: "/speakers/ethem.jpg",
      objectPosition: "50% 15%",
      bio: "2005'te İstanbul Üniversitesi Cerrahpaşa İngilizce Tıp'tan mezun oldu; 2006-2012 arasında aynı fakültede Genel Cerrahi uzmanlığını tamamladı. 2016'da Trakya Üniversitesi'nde akademik hayata başladı, 2023'te doçent oldu; 2022'de EBSQ ile FEBS-C unvanını kazandı. RACS tarafından 'Substantially Comparable' değerlendirildi ve Şubat 2025'ten beri NSW'de Wollongong Devlet Hastanesi ve Üniversitesi'nde Upper GI Fellow olarak çalışıyor. Bu oturumda Avustralya sistemine uygun bir CV'nin nasıl hazırlandığını, iş ilanlarının nerede çıktığını ve başvurunun adım adım nasıl yürüdüğünü kendi deneyiminden aktarır.",
    },
  ],
  "uzmanlik-denkligi-basvuru-belgeleri-11-eki": [
    {
      name: "Dr. Fidan Şenova",
      title: "AUSCAMP Co-Founder & Mentör",
      photo: "/speakers/fidan.jpg",
      objectPosition: "50% 28%",
      bio: "Çukurova Üniversitesi Tıp Fakültesi 2019 mezunu. Tıp eğitimi boyunca IFMSA, TurkMSIC, UNHCR ve UNFPA ile pek çok ulusal ve uluslararası halk sağlığı çalışmasında bulundu. 15 yılı aşkın süredir Türkçe-İngilizce medikal çevirmenlik yapıyor. 2021'den beri Melbourne'da yaşıyor, 2023'ten beri tıp eğitimi alanında uluslararası kapasitede çalışıyor. Bu oturumda uzmanlık denkliği başvurusu için hangi belgelerin gerektiğini, nasıl hazırlanıp onaylatıldığını ve dosyada en sık yapılan hataları anlatır.",
    },
  ],
  "radyoloji-konu-anlatimi-18-eki": [
    {
      name: "Dr. Gizem Pehlivan",
      title: "AUSCAMP Mentörü & Eğitmeni",
      photo: "/speakers/gizem-pehlivan.jpg",
      objectPosition: "50% 30%",
      bio: "2019 Çanakkale On Sekiz Mart Üniversitesi Tıp mezunu. Öğrencilik yıllarında Avustralya'da doktorluğa karar verdi ve 2022'de iş bularak taşındı. Tıp eğitimi ve sağlık hakkına erişimde eşitlik üzerine çalışmalar yapıyor. 2025'ten beri AUSCAMP ile denklik sürecinde mentör olarak destek sağlıyor. Bu oturumda AMC sınavına yönelik radyoloji konularını sistematik biçimde anlatır.",
    },
  ],
  "mcq-soru-cozumu-25-eki": [
    {
      name: "Dr. Gizem Pehlivan",
      title: "AUSCAMP Mentörü & Eğitmeni",
      photo: "/speakers/gizem-pehlivan.jpg",
      objectPosition: "50% 30%",
      bio: "2019 Çanakkale On Sekiz Mart Üniversitesi Tıp mezunu. Öğrencilik yıllarında Avustralya'da doktorluğa karar verdi ve 2022'de iş bularak taşındı. Tıp eğitimi ve sağlık hakkına erişimde eşitlik üzerine çalışmalar yapıyor. 2025'ten beri AUSCAMP ile denklik sürecinde mentör olarak destek sağlıyor. Bu oturumda AMC CAT MCQ tarzı soruları canlı çözer, soru kökünü okuma ve çeldiricileri ayıklama mantığını adım adım gösterir.",
    },
  ],
};

// Primary photo for a webinar card avatar (first speaker's photo, if any).
export function primaryPhoto(slug: string): string | undefined {
  return webinarSpeakers[slug]?.[0]?.photo;
}

export function primaryObjectPosition(slug: string): string | undefined {
  return webinarSpeakers[slug]?.[0]?.objectPosition;
}

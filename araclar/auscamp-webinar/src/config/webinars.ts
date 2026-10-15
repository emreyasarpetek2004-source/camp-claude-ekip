export const communityUrl =
  "https://chat.whatsapp.com/<DAVET_KODU>?mode=gi_t";

// openToAll: true  -> herkese açık & ücretsiz (sarı etiket + "ücretsiz" dili)
// openToAll: false -> yalnız AUSCAMP danışanlarına özel (sarı etiket gösterilmez)
export const webinars = [
 { slug: "cv-is-basvurulari-4-eki", date: "2026-10-04", time: "13.00",
   title: "Avustralya'da Doktorluk: CV ve İş Başvuruları",
   audience: "Tüm Hekimlere Açık",
   openToAll: true,
   speaker: "Doç. Dr. İbrahim Ethem Cakcak",
   whatsappUrl: "https://chat.whatsapp.com/<DAVET_KODU>?mode=gi_t" },
 { slug: "uzmanlik-denkligi-basvuru-belgeleri-11-eki", date: "2026-10-11", time: "13.00",
   title: "Avustralya'da Uzmanlık Denkliği: Başvuru Belgeleri",
   audience: "Tüm Hekimlere Açık",
   openToAll: true,
   speaker: "Dr. Fidan Şenova",
   whatsappUrl: "https://chat.whatsapp.com/<DAVET_KODU>?mode=gi_t" },
 { slug: "radyoloji-konu-anlatimi-18-eki", date: "2026-10-18", time: "13.00",
   title: "Radyoloji Konu Anlatımı",
   audience: "AUSCAMP Danışanlarına Özel",
   openToAll: false,
   speaker: "Dr. Gizem Pehlivan",
   whatsappUrl: communityUrl },
 { slug: "mcq-soru-cozumu-25-eki", date: "2026-10-25", time: "13.00",
   title: "MCQ Soru Çözümü",
   audience: "AUSCAMP Danışanlarına Özel",
   openToAll: false,
   speaker: "Dr. Gizem Pehlivan",
   whatsappUrl: communityUrl }
];

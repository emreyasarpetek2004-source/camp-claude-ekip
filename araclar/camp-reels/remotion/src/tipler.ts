// sahne_NN.json ve klip.json şemaları (Python tarafı bunları yazar, yönetmen agent'ı sahneyi üretir)

export type Kelime = {w: string; b: number; e: number; nokta?: boolean};

export type Klip = {
  no: number;
  marka: string;
  duzen: 'paylasim' | 'konusmaci' | 'slayt' | 'gorsel';
  sure: number;
  kelimeler: Kelime[];
  hoca?: {ad: string; unvan?: string; etiket?: string};
  webinar?: string;
};

// her eklemede isteğe bağlı konu emojisi: emoji (karakter) + emoji_dosya (Twemoji SVG, sahne.py çözer)
export type EkOrtak = {emoji?: string; emoji_dosya?: string};
export type Ekleme = EkOrtak & (
  | {tip: 'stat'; bas: number; bit: number; deger: string; etiket: string; alt?: string}
  | {tip: 'adimlar'; bas: number; bit: number; baslik?: string; maddeler: string[]}
  | {tip: 'karsilastirma'; bas: number; bit: number; sol: {baslik: string; metin: string}; sag: {baslik: string; metin: string}}
  | {tip: 'rozet'; bas: number; bit: number; metin: string; ikon?: 'ok' | 'carpi' | 'unlem' | 'saat' | 'para'}
  | {tip: 'gorsel'; bas: number; bit: number; dosya: string; aciklama?: string; kunye?: string}
  | {tip: 'slayt_zoom'; bas: number; bit: number; bolge: [number, number, number, number]});

export type Sahne = {
  soru_karti: {metin: string; etiket?: string; bas: number; bit: number};
  vurgu: number[]; // kelime indeksleri
  gizle?: number[]; // altyazıda gösterilmeyen kelimeler (sürçme)
  eklemeler: Ekleme[];
  zoom: {bas: number; bit: number; olcek: number}[];
  sfx: {t: number; ses: string; seviye?: number}[];
  kapanis?: {sure: number; baslik?: string};
  tepe?: {dosya: string; bas: number; bit: number; kunye?: string}[]; // düzen 'gorsel': üst panel görsel akışı
};

export type Marka = {
  ad: string;
  zemin: {ust: string; alt: string; vurgu: string};
  altyazi: {renk: string; kontur: string};
  v2: {vurgu: string; vurgu2: string; acik: string; koyu: string; logo?: string; kapanis_alt?: string;
    kapanis?: {baslik?: string; alt?: string; iletisim?: string[]};
    tema?: 'koyu' | 'acik'; zemin_acik?: {ust: string; alt: string; leke: string}; metin?: string; ust_logo?: boolean; logo_golge?: boolean; vurgu_ustu?: string};
};

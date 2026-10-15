import React from 'react';
import {AbsoluteFill, Audio, Img, OffthreadVideo, Sequence, interpolate, spring, staticFile, useCurrentFrame,
  useVideoConfig, Easing} from 'remotion';
import {Klip, Sahne, Marka} from './tipler';
import {Altyazi} from './bilesen/Altyazi';
import {SoruKarti} from './bilesen/SoruKarti';
import {EklemeKatmani} from './bilesen/Ekleme';
import {HocaEtiketi} from './bilesen/HocaEtiketi';
import {Kapanis} from './bilesen/Kapanis';
import {fontYukle} from './bilesen/font';
import {TepeAkis} from './bilesen/TepeAkis';

export const FPS = 30;
export type ReelsProps = {klip: Klip; sahne: Sahne; marka: Marka};

// 1080x1920 yerleşim (@camp2uk webinar kesiti, analiz/RAPOR.md)
export const SLAYT = {x: 0, y: 225, w: 1080, h: 608};  // üstte logo için 22 px aşağı (kullanıcı, 8 Eki 2026)
export const KONUS = {x: 40, y: 1045, w: 1000, h: 563};
export const KONUS_TAM = {x: 40, y: 250, w: 1000, h: 1130};
export const ALTYAZI_Y = 939;
export const ALTYAZI_Y_TAM = 1500;

export const kapanisSure = (p: ReelsProps) => p.sahne?.kapanis?.sure ?? 2.0;
export const toplamSure = (p: ReelsProps) => (p.klip?.sure ?? 10) + kapanisSure(p);

const Zemin: React.FC<{marka: Marka}> = ({marka}) => {
  const f = useCurrentFrame();
  const x = 30 + 12 * Math.sin(f / 90);
  const y = 45 + 8 * Math.cos(f / 110);
  if (marka.v2.tema === 'acik' && marka.v2.zemin_acik) {
    // kırık beyaz zemin (kullanıcı, 8 Eki 2026): sıcak beyaz gradyan + çok hafif mint lekeler
    const z = marka.v2.zemin_acik;
    return (
      <AbsoluteFill style={{background: `linear-gradient(180deg, ${z.ust} 0%, ${z.alt} 100%)`}}>
        <AbsoluteFill style={{background: `radial-gradient(circle at ${x}% ${y}%, ${z.leke}cc 0%, transparent 42%)`}} />
        <AbsoluteFill style={{background: `radial-gradient(circle at ${100 - x}% ${90 - y / 3}%, ${z.leke}99 0%, transparent 38%)`}} />
        <AbsoluteFill style={{opacity: 0.035, backgroundImage:
          'repeating-linear-gradient(45deg, #000 0px, #000 1px, transparent 1px, transparent 7px)'}} />
      </AbsoluteFill>
    );
  }
  return (
    <AbsoluteFill style={{background: `linear-gradient(180deg, ${marka.zemin.ust} 0%, ${marka.zemin.alt} 100%)`}}>
      <AbsoluteFill style={{background: `radial-gradient(circle at ${x}% ${y}%, ${marka.zemin.vurgu}aa 0%, transparent 45%)`}} />
      <AbsoluteFill style={{background: `radial-gradient(circle at ${100 - x}% ${100 - y / 2}%, ${marka.v2.vurgu}22 0%, transparent 40%)`}} />
      <AbsoluteFill style={{opacity: 0.06, backgroundImage:
        'repeating-linear-gradient(45deg, #fff 0px, #fff 1px, transparent 1px, transparent 6px)'}} />
    </AbsoluteFill>
  );
};

// üst logo: slaytın üstünde ortada (kullanıcı: "üstte DENTCAMP logosu olsun")
const UstLogo: React.FC<{marka: Marka}> = ({marka}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const g = spring({frame: f - 2, fps, config: {damping: 16, stiffness: 140}});
  if (!marka.v2.ust_logo || !marka.v2.logo) return null;
  return <Img src={staticFile('marka/' + marka.v2.logo)} style={{position: 'absolute', left: 540 - 190, top: 118, width: 380,
    opacity: g, transform: `translateY(${(1 - g) * -20}px)`,
    // AUSCAMP sarısı beyaz zeminde soluk kalıyor: ince koyu yeşil gölge (10 Eki 2026)
    filter: marka.v2.logo_golge ? `drop-shadow(0 0 1.5px ${marka.v2.koyu}) drop-shadow(0 3px 6px rgba(0,0,0,0.18))` : undefined}} />;
};

const panelGiris = (f: number, fps: number, gecikme: number) =>
  spring({frame: f - gecikme, fps, config: {damping: 18, stiffness: 120}});

export const Reels: React.FC<ReelsProps> = (p) => {
  const {klip, sahne, marka} = p;
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  fontYukle();
  const t = f / fps;
  const sonKare = Math.round(klip.sure * fps);
  const paylasim = klip.duzen !== 'konusmaci';
  const konus = paylasim ? KONUS : KONUS_TAM;

  // konuşmacı punch-in: sahne.zoom anlarında spring
  let olcek = 1;
  for (const z of sahne.zoom || []) {
    const g = spring({frame: f - z.bas * fps, fps, config: {damping: 20, stiffness: 140}});
    const c = spring({frame: f - z.bit * fps, fps, config: {damping: 20, stiffness: 140}});
    olcek = Math.max(olcek, 1 + (z.olcek - 1) * (g - c));
  }
  const girS = panelGiris(f, fps, 0);
  const girK = panelGiris(f, fps, 4);

  // slayt_zoom = spot ışığı: bölge dışı kararır, bölgeye turkuaz çerçeve; yakınlaşma en çok 1,08 (metin kesilmesin)
  let spot: null | {g: number; b: [number, number, number, number]} = null;
  for (const e of sahne.eklemeler || []) {
    if (e.tip !== 'slayt_zoom') continue;
    const g = interpolate(t, [e.bas, e.bas + 0.45, e.bit - 0.4, e.bit], [0, 1, 1, 0],
      {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.inOut(Easing.cubic)});
    if (g > 0) spot = {g, b: e.bolge};
  }
  const sz = spot ? {s: 1 + 0.08 * spot.g, ox: ((spot.b[0] + spot.b[2]) / 2) * 100, oy: ((spot.b[1] + spot.b[3]) / 2) * 100} : {s: 1, ox: 50, oy: 50};

  return (
    <AbsoluteFill style={{fontFamily: 'PoppinsX'}}>
      <Zemin marka={marka} />
      <Sequence durationInFrames={sonKare}><UstLogo marka={marka} /></Sequence>
      <Sequence durationInFrames={sonKare}>
        {paylasim && (
          <div style={{position: 'absolute', left: SLAYT.x, top: SLAYT.y, width: SLAYT.w, height: SLAYT.h, overflow: 'hidden',
            transform: `translateY(${(1 - girS) * -40}px)`, opacity: girS,
            boxShadow: '0 18px 50px rgba(0,0,0,0.45)'}}>
            <div style={{width: '100%', height: '100%', transform: `scale(${sz.s})`, transformOrigin: `${sz.ox}% ${sz.oy}%`}}>
              {klip.duzen === 'gorsel'
                ? <TepeAkis tepe={sahne.tepe || []} marka={marka} />
                : <OffthreadVideo src={staticFile(`klip_${String(klip.no).padStart(2, '0')}/slayt.mp4`)} muted
                    style={{width: '100%', height: '100%'}} />}
              {spot && (() => {
                const [x0, y0, x1, y1] = spot.b;
                const pad = 0.015;
                const L = Math.max(0, x0 - pad) * 100, T = Math.max(0, y0 - pad) * 100;
                const R = Math.min(1, x1 + pad) * 100, B = Math.min(1, y1 + pad) * 100;
                return <>
                  <div style={{position: 'absolute', inset: 0, background: `rgba(0,0,0,${0.55 * spot.g})`,
                    clipPath: `polygon(0% 0%, 0% 100%, ${L}% 100%, ${L}% ${T}%, ${R}% ${T}%, ${R}% ${B}%, ${L}% ${B}%, ${L}% 100%, 100% 100%, 100% 0%)`}} />
                  <div style={{position: 'absolute', left: `${L}%`, top: `${T}%`, width: `${R - L}%`, height: `${B - T}%`,
                    border: `6px solid ${marka.v2.vurgu}`, borderRadius: 14, opacity: spot.g,
                    boxShadow: `0 0 30px ${marka.v2.vurgu}88`}} />
                </>;
              })()}
            </div>
          </div>
        )}
        {klip.duzen !== 'slayt' && (
          <div style={{position: 'absolute', left: konus.x, top: konus.y, width: konus.w, height: konus.h,
            borderRadius: 34, overflow: 'hidden', border: `5px solid ${marka.v2.vurgu}`,
            boxShadow: `0 20px 60px rgba(0,0,0,0.5), 0 0 0 10px ${marka.v2.vurgu}22`,
            transform: `translateY(${(1 - girK) * 60}px)`, opacity: girK}}>
            <OffthreadVideo src={staticFile(`klip_${String(klip.no).padStart(2, '0')}/konusmaci.mp4`)} muted
              style={{width: '100%', height: '100%', objectFit: 'cover', transform: `scale(${olcek})`}} />
          </div>
        )}
        <EklemeKatmani sahne={sahne} marka={marka} alan={paylasim ? SLAYT : {x: 70, y: 860, w: 940, h: 500}} />
        {klip.hoca && <HocaEtiketi hoca={klip.hoca} marka={marka} alan={konus} />}
        <Altyazi kelimeler={klip.kelimeler.filter((_, i) => !(sahne.gizle || []).includes(i))} vurgu={(sahne.vurgu || []).map((i) => i - (sahne.gizle || []).filter((g) => g < i).length)} marka={marka}
          y={paylasim ? ALTYAZI_Y : ALTYAZI_Y_TAM} />
        <SoruKarti kart={sahne.soru_karti} marka={marka} alan={paylasim ? SLAYT : {x: 60, y: 300, w: 960, h: 560}} />
      </Sequence>
      <Sequence from={sonKare - 6}>
        <Kapanis klip={klip} marka={marka} sure={kapanisSure(p)} baslik={sahne.kapanis?.baslik} />
      </Sequence>
      <Audio src={staticFile(`klip_${String(klip.no).padStart(2, '0')}/ses.wav`)} />
      {(sahne.sfx || []).map((s, i) => (
        <Sequence key={i} from={Math.max(0, Math.round(s.t * fps))}>
          <Audio src={staticFile(`sfx/${s.ses}.wav`)} volume={s.seviye ?? 0.35} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};

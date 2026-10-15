import React, {useMemo} from 'react';
import {interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {Kelime, Marka} from '../tipler';

// Kelime kelime vurgulu altyazı: sayfa = en çok 2 satır (~24 karakter/satır, en çok 6 kelime).
// Sayfa cümle sonunda, 0,5 sn üstü duraklamada ya da doluluğunda biter. Aktif kelime marka renginde ve büyür.
const MAX_KAR = 20;   // 66 px Poppins ExtraBold, 980 px genişlikte satır başına ~22-24 karakter
const MAX_KELIME = 5;

type Sayfa = {i0: number; i1: number; b: number; e: number};

const sayfala = (k: Kelime[]): Sayfa[] => {
  const s: Sayfa[] = [];
  let cur: number[] = [];
  let kar = 0;
  k.forEach((w, i) => {
    cur.push(i);
    kar += w.w.length + 1;
    const son = i === k.length - 1;
    const ara = !son && k[i + 1].b - w.e > 0.5;
    // 2 satır bütçesi (~2 x 20 karakter): sonraki kelime sığmıyorsa sayfa burada biter
    if (son || w.nokta || ara || cur.length >= MAX_KELIME || kar + (k[i + 1]?.w.length ?? 0) + 1 > MAX_KAR * 2) {
      s.push({i0: cur[0], i1: cur[cur.length - 1], b: k[cur[0]].b, e: k[cur[cur.length - 1]].e});
      cur = [];
      kar = 0;
    }
  });
  // tek kelimelik sayfa yalnız kalmaz
  const out: Sayfa[] = [];
  for (const p of s) {
    const o = out[out.length - 1];
    if (o && p.i1 === p.i0 && p.b - o.e < 0.6 && o.i1 - o.i0 < MAX_KELIME) { o.i1 = p.i1; o.e = p.e; } else out.push({...p});
  }
  // ekranda kalma: sonraki sayfa 0,6 sn içinde başlıyorsa boşluk bırakma
  out.forEach((p, i) => { const n = out[i + 1]; if (n && n.b - p.e < 0.6) p.e = n.b; else p.e = p.e + 0.25; });
  return out;
};

export const Altyazi: React.FC<{kelimeler: Kelime[]; vurgu: number[]; marka: Marka; y: number}> = ({kelimeler, vurgu, marka, y}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = f / fps;
  const sayfalar = useMemo(() => sayfala(kelimeler), [kelimeler]);
  const v = useMemo(() => new Set(vurgu), [vurgu]);
  const p = sayfalar.find((s) => t >= s.b - 0.05 && t < s.e);
  if (!p) return null;
  const giris = spring({frame: f - Math.round(p.b * fps), fps, config: {damping: 18, stiffness: 320}, durationInFrames: 5});
  const kelime = [];
  let uzunluk = 0, enUzun = 0;
  for (let i = p.i0; i <= p.i1; i++) { uzunluk += kelimeler[i].w.length + 1; enUzun = Math.max(enUzun, kelimeler[i].w.length); }
  for (let i = p.i0; i <= p.i1; i++) {
    const w = kelimeler[i];
    // aktif: kelime başlangıcından bir sonraki kelimenin başlangıcına kadar (iki kelime aynı anda hap olmaz)
    const sonraki = kelimeler[i + 1];
    const aktif = t >= w.b - 0.03 && t < (sonraki ? Math.min(Math.max(w.e, w.b + 0.18), sonraki.b - 0.03) : Math.max(w.e, w.b + 0.18));
    const gecti = t >= w.e;
    const pop = spring({frame: f - Math.round(w.b * fps), fps, config: {damping: 12, stiffness: 260}, durationInFrames: 8});
    const vurgulu = v.has(i);
    // aktif kelime: marka renginde hap içinde koyu yazı; vurgu kelimesi (rakam/terim): marka renginde yazı
    const acik = marka.v2.tema === 'acik';
    const renk = aktif ? (marka.v2.vurgu_ustu || marka.v2.koyu) : vurgulu ? marka.v2.vurgu2 : (acik ? (marka.v2.metin || '#111') : '#ffffff');
    const olcek = aktif ? 1 + 0.05 * pop : 1;
    kelime.push(
      <span key={i} style={{display: 'inline-block', margin: '4px 6px', padding: '0 10px', borderRadius: 16, color: renk,
        background: aktif ? marka.v2.vurgu : 'transparent',
        transform: `scale(${olcek}) translateY(${aktif ? -3 * pop : 0}px)`,
        opacity: gecti || aktif ? 1 : 0.9,
        textShadow: aktif || acik ? 'none' : '0 4px 0 rgba(0,0,0,0.55), 0 0 18px rgba(0,0,0,0.55)',
        WebkitTextStroke: aktif || acik ? '0px' : '2.5px #000', paintOrder: 'stroke fill',
        boxShadow: aktif ? '0 8px 24px rgba(0,0,0,0.35)' : 'none'}}>
        {w.w}
      </span>,
    );
  }
  return (
    <div style={{position: 'absolute', left: 50, right: 50, top: y, transform: `translateY(-50%) scale(${interpolate(giris, [0, 1], [0.95, 1])})`,
      opacity: interpolate(giris, [0, 1], [0.6, 1]), textAlign: 'center', fontSize: (uzunluk > 36 || enUzun > 15) ? 56 : 64, fontWeight: 800, lineHeight: 1.18, letterSpacing: -0.5}}>
      {kelime}
    </div>
  );
};

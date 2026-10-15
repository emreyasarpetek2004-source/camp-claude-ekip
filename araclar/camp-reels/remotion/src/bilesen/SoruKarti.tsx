import React from 'react';
import {interpolate, spring, useCurrentFrame, useVideoConfig, Easing} from 'remotion';
import {Marka} from '../tipler';

type Alan = {x: number; y: number; w: number; h: number};

// Giriş soru kartı (pop-up): elastik açılış, arkada ışık patlaması + yayılan halkalar,
// köşeye zıplayan "?" balonu, sorunun can alıcı kısmı vurgulu. Metinde *yıldızlı* kısım vurgulanır;
// yıldız yoksa son 3 kelime vurgulanır. "HOCA CEVAPLIYOR" hapı kullanıcı kararıyla kaldırıldı (8 Eki 2026).
export const SoruKarti: React.FC<{kart: {metin: string; etiket?: string; bas: number; bit: number}; marka: Marka; alan: Alan}> =
  ({kart, marka, alan}) => {
    const f = useCurrentFrame();
    const {fps} = useVideoConfig();
    if (!kart || !kart.metin) return null;
    const b = Math.round(kart.bas * fps), e = Math.round(kart.bit * fps);
    if (f < b || f > e + 12) return null;
    const yerel = f - b;

    // 1. evre (0-0,55 sn): dev "?" ekranın ortasına çarpar. 2. evre: küçülüp kartın köşesine uçar, kart açılır.
    const KART = 14;  // kart açılış karesi
    const dev = spring({frame: yerel, fps, config: {damping: 8, stiffness: 200, mass: 0.9}});
    const uc = interpolate(yerel, [KART - 2, KART + 8], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.inOut(Easing.cubic)});
    // elastik pop: 0,55 -> ~1,06 -> 1
    const pop = spring({frame: yerel - KART, fps, config: {damping: 9, stiffness: 170, mass: 0.8}});
    const cik = interpolate(f, [e - 2, e + 10], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.in(Easing.back(1.6))});
    const olcek = interpolate(pop, [0, 1], [0.55, 1]) * interpolate(cik, [0, 1], [1, 0.7]);
    // 1,2 sn'de hafif nabız: dikkat tazelenir
    const nabiz = 1 + 0.025 * Math.sin(Math.max(0, Math.min(1, (yerel - 36) / 10)) * Math.PI);

    // metin: *vurgu* işareti ya da son 3 kelime
    const yildizli = /\*(.+?)\*/.exec(kart.metin);
    const temiz = kart.metin.replace(/\*/g, '');
    const kelimeler = temiz.split(' ');
    let vurguBas = Math.max(0, kelimeler.length - 3);
    if (yildizli) vurguBas = kart.metin.slice(0, yildizli.index).replace(/\*/g, '').split(' ').filter(Boolean).length;
    const vurguSon = yildizli ? vurguBas + yildizli[1].split(' ').length - 1 : kelimeler.length - 1;

    // ışık patlaması ve halkalar
    const isik = interpolate(yerel, [0, 6, 30], [0, 1, 0.55], {extrapolateRight: 'clamp'});
    const halka = (gec: number) => {
      const k = interpolate(yerel - gec, [0, 22], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic)});
      return {s: 0.4 + 1.3 * k, o: (1 - k) * (yerel >= gec ? 0.9 : 0)};
    };
    const h1 = halka(1), h2 = halka(7), h3 = halka(KART);

    // "?" balonu: gecikmeli zıplama + sallanma
    const salla = Math.sin(yerel / 4) * 6 * Math.exp(-Math.max(0, yerel - KART) / 25);

    const cx = alan.x + alan.w / 2, cy = alan.y + alan.h / 2;
    return (
      <>
        {/* arka plan: slaytı karart */}
        <div style={{position: 'absolute', left: alan.x, top: alan.y, width: alan.w, height: alan.h,
          background: `rgba(0,0,0,${0.55 * (1 - cik)})`}} />
        {/* ışık patlaması */}
        <div style={{position: 'absolute', left: cx - 700, top: cy - 700, width: 1400, height: 1400, borderRadius: '50%',
          background: `radial-gradient(circle, ${marka.v2.vurgu}88 0%, ${marka.v2.vurgu}22 30%, transparent 60%)`,
          opacity: isik * (1 - cik), transform: `scale(${0.6 + 0.4 * pop})`, pointerEvents: 'none'}} />
        {[h1, h2, h3].map((h, i) => (
          <div key={i} style={{position: 'absolute', left: cx - 420, top: cy - 420, width: 840, height: 840, borderRadius: '50%',
            border: `8px solid ${marka.v2.vurgu}`, opacity: h.o * (1 - cik), transform: `scale(${h.s})`}} />
        ))}
        {/* kart */}
        <div style={{position: 'absolute', left: alan.x + 40, top: alan.y + 50, width: alan.w - 80, height: alan.h - 100,
          transform: `translateY(${-cik * 140}px) scale(${olcek * nabiz}) rotate(${(1 - pop) * -4}deg)`,
          opacity: Math.min(1, pop * 1.4) * (1 - cik), borderRadius: 40,
          background: `linear-gradient(150deg, ${marka.v2.koyu} 0%, ${marka.zemin.alt} 100%)`,
          boxShadow: `0 30px 80px rgba(0,0,0,0.6), 0 0 0 6px ${marka.v2.vurgu}, 0 0 60px ${marka.v2.vurgu}66`,
          display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '0 70px'}}>
          <div style={{color: '#fff', fontWeight: 800, fontSize: temiz.length > 50 ? 60 : temiz.length > 40 ? 66 : 74,
            lineHeight: 1.14, textAlign: 'center', letterSpacing: -1}}>
            {kelimeler.map((w, i) => {
              const k = spring({frame: yerel - KART - 4 - i * 2, fps, config: {damping: 12, stiffness: 220}});
              const vurgulu = i >= vurguBas && i <= vurguSon;
              return <span key={i} style={{display: 'inline-block', margin: '0 9px', opacity: k,
                transform: `translateY(${(1 - k) * 34}px) scale(${0.8 + 0.2 * k})`,
                color: vurgulu ? marka.v2.vurgu : '#fff',
                textShadow: vurgulu ? `0 0 28px ${marka.v2.vurgu}aa` : '0 4px 0 rgba(0,0,0,0.35)'}}>{w}</span>;
            })}
          </div>
        </div>
        {/* dev "?": ortada çarpar (2,4x -> 1), sonra köşedeki balona dönüşür */}
        {(() => {
          const kose = {x: alan.x + alan.w - 115, y: alan.y + 65};
          const orta = {x: cx, y: cy};
          const x = orta.x + (kose.x - orta.x) * uc, y = orta.y + (kose.y - orta.y) * uc;
          const boyut = interpolate(uc, [0, 1], [420, 150]);
          const sc = interpolate(dev, [0, 1], [2.4, 1]) * (1 - cik);
          const rad = interpolate(uc, [0, 1], [50, 50]);
          return <div style={{position: 'absolute', left: x - boyut / 2, top: y - boyut / 2, width: boyut, height: boyut,
            borderRadius: uc > 0.5 ? '50% 50% 50% 12%' : `${rad}%`, background: marka.v2.vurgu, color: marka.v2.vurgu_ustu || marka.v2.koyu,
            display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: boyut * 0.72, fontWeight: 800, lineHeight: 1,
            opacity: Math.min(1, dev * 2) * (1 - cik),
            transform: `scale(${sc}) rotate(${salla + (1 - dev) * -25}deg)`,
            boxShadow: `0 20px 60px rgba(0,0,0,0.5), 0 0 0 ${interpolate(uc, [0, 1], [26, 10])}px ${marka.v2.vurgu}33, 0 0 80px ${marka.v2.vurgu}88`}}>?</div>;
        })()}
      </>
    );
  };

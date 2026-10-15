import React from 'react';
import {spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {Marka} from '../tipler';

// Hoca etiketi (kullanıcı, 8 Eki 2026, son hali): boyut DEĞİŞMEZ, büyüyüp küçülmez.
// Konuşmacı panelinin sol alt kenarında (biraz dışarı taşar), reels boyunca kalır.
// Üst şerit (ad, marka rengi) SOLDAN, alt şerit (unvan, koyu) SAĞDAN kayarak gelir.
export const HocaEtiketi: React.FC<{hoca: {ad: string; unvan?: string; etiket?: string}; marka: Marka;
  alan: {x: number; y: number; w: number; h: number}}> = ({hoca, marka, alan}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const ust = spring({frame: f - 12, fps, config: {damping: 15, stiffness: 150}});
  const alt = spring({frame: f - 20, fps, config: {damping: 15, stiffness: 150}});
  const metin = hoca.etiket || (hoca.unvan ? `${hoca.ad} (${hoca.unvan})` : hoca.ad);
  const i = metin.indexOf('(');
  const ad = i > 0 ? metin.slice(0, i).trimEnd() : metin;
  const ek = i > 0 ? metin.slice(i) : '';
  return (
    <div style={{position: 'absolute', left: alan.x - 6, top: alan.y + alan.h + 30, transform: 'translateY(-100%)',
      display: 'flex', flexDirection: 'column', alignItems: 'flex-start', filter: 'drop-shadow(0 10px 22px rgba(0,0,0,0.35))'}}>
      <div style={{background: marka.v2.vurgu, color: marka.v2.vurgu_ustu || marka.v2.koyu, fontWeight: 800, fontSize: 31, padding: '7px 20px',
        borderRadius: '12px 12px 12px 0', whiteSpace: 'nowrap', opacity: ust,
        transform: `translateX(${(1 - ust) * -700}px)`}}>{ad}</div>
      {ek && <div style={{background: 'rgba(0,0,0,0.82)', color: '#fff', fontWeight: 600, fontSize: 23, padding: '5px 18px',
        borderRadius: '0 0 10px 10px', whiteSpace: 'nowrap', opacity: alt,
        transform: `translateX(${(1 - alt) * 900}px)`}}>{ek}</div>}
    </div>
  );
};

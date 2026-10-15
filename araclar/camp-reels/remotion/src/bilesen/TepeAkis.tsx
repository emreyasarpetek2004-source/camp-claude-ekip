import React from 'react';
import {AbsoluteFill, Img, interpolate, staticFile, useCurrentFrame, useVideoConfig, Easing} from 'remotion';
import {Marka} from '../tipler';

// Düzen "gorsel" (yalnız konuşmacı olan kesit): üst panelde slayt yerine görsel akışı.
// Her görsel Ken Burns (yavaş yakınlaşma + yön değiştiren kaydırma), geçişte 0,5 sn kayarak çapraz geçiş.
export const TepeAkis: React.FC<{tepe: {dosya: string; bas: number; bit: number; kunye?: string}[]; marka: Marka}> = ({tepe, marka}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = f / fps;
  const G = 0.5;
  return (
    <AbsoluteFill style={{background: marka.v2.koyu}}>
      {tepe.map((x, i) => {
        if (t < x.bas - 0.05 || t > x.bit + G) return null;
        const gir = i === 0 ? 1 : interpolate(t, [x.bas, x.bas + G], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic)});
        const k = interpolate(t, [x.bas, x.bit + G], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
        const yon = i % 2 === 0 ? 1 : -1;
        return (
          <AbsoluteFill key={i} style={{opacity: gir, transform: `translateX(${(1 - gir) * 120 * yon}px)`}}>
            <Img src={staticFile(x.dosya)} style={{width: '100%', height: '100%', objectFit: 'cover',
              transform: `scale(${1.05 + 0.1 * k}) translateX(${yon * (k - 0.5) * 30}px)`}} />
            <AbsoluteFill style={{background: 'linear-gradient(180deg, rgba(0,0,0,0) 55%, rgba(0,0,0,0.35) 100%)'}} />
            {x.kunye && <div style={{position: 'absolute', right: 14, bottom: 8, color: '#fff', fontSize: 16, opacity: 0.7}}>{x.kunye}</div>}
          </AbsoluteFill>
        );
      })}
    </AbsoluteFill>
  );
};

import React from 'react';
import {Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig, Easing} from 'remotion';
import {Ekleme, Marka, Sahne} from '../tipler';

type Alan = {x: number; y: number; w: number; h: number};

const Ikon: React.FC<{tip?: string; renk: string; boyut?: number}> = ({tip = 'ok', renk, boyut = 92}) => {
  const p: Record<string, React.ReactNode> = {
    ok: <path d="M20 52 L42 72 L80 30" />,
    carpi: <><path d="M28 28 L72 72" /><path d="M72 28 L28 72" /></>,
    unlem: <><path d="M50 22 L50 60" /><circle cx="50" cy="78" r="3" /></>,
    saat: <><circle cx="50" cy="50" r="32" /><path d="M50 30 L50 52 L64 60" /></>,
    para: <><circle cx="50" cy="50" r="32" /><path d="M58 36 C40 30 38 48 50 50 C62 52 60 70 42 64" /><path d="M50 26 L50 74" /></>,
  };
  return (
    <svg width={boyut} height={boyut} viewBox="0 0 100 100" fill="none" stroke={renk} strokeWidth={9} strokeLinecap="round" strokeLinejoin="round">
      {p[tip] || p.ok}
    </svg>
  );
};

// konu emojisi: zıplayarak gelir, hafif sallanır (Twemoji SVG)
const Emoji: React.FC<{dosya?: string; boyut: number; k: number; f: number}> = ({dosya, boyut, k, f}) =>
  dosya ? <Img src={staticFile(dosya)} style={{width: boyut, height: boyut,
    transform: `scale(${k}) rotate(${Math.sin(f / 6) * 5 * k}deg)`, filter: 'drop-shadow(0 10px 18px rgba(0,0,0,0.45))'}} /> : null;

// "%50", "4", "£485", "60 iş günü" -> sayı kısmı sayılarak artar
const SayanDeger: React.FC<{deger: string; ilerleme: number}> = ({deger, ilerleme}) => {
  const m = deger.match(/^(\D*)(\d+(?:[.,]\d+)?)(.*)$/);
  if (!m) return <>{deger}</>;
  const hedef = parseFloat(m[2].replace(',', '.'));
  // küçük sayı ve aralıkta ("2 yıl", "25-30") ara değer yanıltıcı: yalnız 100+ tek sayılar sayar
  if (hedef < 100 || /^\s*[-–]\s*\d/.test(m[3])) return <>{deger}</>;
  const ondalik = m[2].includes(',') || m[2].includes('.');
  const v = hedef * ilerleme;
  const metin = ondalik ? v.toFixed(1).replace('.', ',') : Math.round(v).toLocaleString('tr-TR');
  return <>{m[1]}{metin}{m[3]}</>;
};

const Kart: React.FC<{e: Ekleme; marka: Marka; alan: Alan}> = ({e, marka, alan}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const b = Math.round(e.bas * fps), son = Math.round(e.bit * fps);
  const gir = spring({frame: f - b, fps, config: {damping: 15, stiffness: 170}});
  const cik = interpolate(f, [son - 8, son], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.in(Easing.cubic)});
  const v = gir * (1 - cik);
  const ic = (gecikme: number) => spring({frame: f - b - gecikme, fps, config: {damping: 14, stiffness: 190}});
  const kutu: React.CSSProperties = {position: 'absolute', left: alan.x, top: alan.y, width: alan.w, height: alan.h,
    transform: `translateX(${(1 - gir) * 140 + cik * -140}px) scale(${interpolate(v, [0, 1], [0.94, 1])})`, opacity: v,
    overflow: 'hidden', boxShadow: '0 22px 60px rgba(0,0,0,0.5)',
    background: `linear-gradient(150deg, ${marka.v2.koyu} 0%, ${marka.zemin.alt} 100%)`,
    display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', color: '#fff'};
  const cizgi = <div style={{position: 'absolute', left: 0, top: 0, height: 10, width: `${100 * ic(4)}%`, background: marka.v2.vurgu}} />;

  if (e.tip === 'stat') {
    const say = interpolate(f - b, [4, 26], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic)});
    return (
      <div style={kutu}>{cizgi}
        {e.emoji_dosya && <div style={{marginBottom: 6}}><Emoji dosya={e.emoji_dosya} boyut={110} k={ic(0)} f={f} /></div>}
        <div style={{fontSize: e.deger.length > 7 ? 130 : e.deger.length > 5 ? 165 : 210, fontWeight: 800, whiteSpace: 'nowrap', color: marka.v2.vurgu, lineHeight: 1, letterSpacing: -6,
          transform: `scale(${0.7 + 0.3 * ic(2)})`, textShadow: '0 10px 40px rgba(0,0,0,0.4)'}}>
          <SayanDeger deger={e.deger} ilerleme={say} />
        </div>
        <div style={{fontSize: 54, fontWeight: 800, marginTop: 18, opacity: ic(8), textAlign: 'center', padding: '0 60px'}}>{e.etiket}</div>
        {e.alt && <div style={{fontSize: 34, fontWeight: 500, marginTop: 12, opacity: 0.85 * ic(12), color: marka.v2.acik}}>{e.alt}</div>}
      </div>
    );
  }
  if (e.tip === 'adimlar') {
    return (
      <div style={{...kutu, alignItems: 'stretch', padding: '0 80px'}}>{cizgi}
        {e.baslik && <div style={{display: 'flex', alignItems: 'center', gap: 20, fontSize: 46, fontWeight: 800, marginBottom: 26,
          color: marka.v2.vurgu, opacity: ic(2)}}><Emoji dosya={e.emoji_dosya} boyut={72} k={ic(0)} f={f} />{e.baslik}</div>}
        {e.maddeler.map((m, i) => {
          const k = ic(6 + i * 9);
          return (
            <div key={i} style={{display: 'flex', alignItems: 'center', margin: '12px 0', opacity: k, transform: `translateX(${(1 - k) * 60}px)`}}>
              <div style={{width: 74, height: 74, borderRadius: 40, background: marka.v2.vurgu, color: marka.v2.vurgu_ustu || marka.v2.koyu, fontSize: 40,
                fontWeight: 800, display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0}}>{i + 1}</div>
              <div style={{fontSize: 44, fontWeight: 700, marginLeft: 28, lineHeight: 1.15}}>{m}</div>
            </div>
          );
        })}
      </div>
    );
  }
  if (e.tip === 'karsilastirma') {
    const yan = (s: {baslik: string; metin: string}, k: number, vurgu: boolean) => (
      <div style={{flex: 1, margin: '0 16px', padding: '36px 26px', borderRadius: 28, opacity: k, transform: `translateY(${(1 - k) * 40}px)`,
        background: vurgu ? marka.v2.vurgu : 'rgba(255,255,255,0.08)', color: vurgu ? (marka.v2.vurgu_ustu || marka.v2.koyu) : '#fff', textAlign: 'center',
        border: vurgu ? 'none' : '3px solid rgba(255,255,255,0.25)'}}>
        <div style={{fontSize: 44, fontWeight: 800}}>{s.baslik}</div>
        <div style={{fontSize: 36, fontWeight: 600, marginTop: 16, lineHeight: 1.2}}>{s.metin}</div>
      </div>
    );
    return (
      <div style={{...kutu, flexDirection: 'row', padding: '0 40px'}}>{cizgi}
        {yan(e.sol, ic(3), false)}
        <div style={{fontSize: 46, fontWeight: 800, color: marka.v2.vurgu, opacity: ic(8)}}>VS</div>
        {yan(e.sag, ic(12), true)}
      </div>
    );
  }
  if (e.tip === 'rozet') {
    const k = ic(2);
    return (
      <div style={kutu}>{cizgi}
        {e.emoji_dosya ? (
          <div style={{position: 'relative', width: 200, height: 200, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
            <div style={{position: 'absolute', inset: 10, borderRadius: 100, background: `${marka.v2.vurgu}2e`,
              boxShadow: `0 0 0 14px ${marka.v2.vurgu}18`, transform: `scale(${k})`}} />
            <Emoji dosya={e.emoji_dosya} boyut={150} k={k} f={f} />
          </div>
        ) : (
        <div style={{width: 170, height: 170, borderRadius: 100, background: marka.v2.vurgu, display: 'flex', alignItems: 'center',
          justifyContent: 'center', transform: `scale(${k}) rotate(${(1 - k) * -40}deg)`, boxShadow: `0 0 0 16px ${marka.v2.vurgu}33`}}>
          <Ikon tip={e.ikon} renk={marka.v2.vurgu_ustu || marka.v2.koyu} />
        </div>)}
        <div style={{fontSize: 64, fontWeight: 800, marginTop: 40, textAlign: 'center', padding: '0 70px', lineHeight: 1.12, opacity: ic(7),
          transform: `translateY(${(1 - ic(7)) * 30}px)`}}>{e.metin}</div>
      </div>
    );
  }
  if (e.tip === 'gorsel') {
    const kb = interpolate(f - b, [0, son - b], [1.0, 1.1], {extrapolateRight: 'clamp'});
    return (
      <div style={{...kutu, background: '#000'}}>
        <Img src={staticFile(e.dosya)} style={{width: '100%', height: '100%', objectFit: 'cover', transform: `scale(${kb})`}} />
        <div style={{position: 'absolute', inset: 0, boxShadow: `inset 0 0 0 6px ${marka.v2.vurgu}`}} />
        {e.aciklama && (
          <div style={{position: 'absolute', left: 30, bottom: 30, background: 'rgba(0,0,0,0.72)', color: '#fff', fontWeight: 700,
            fontSize: 36, padding: '10px 22px', borderRadius: 14, opacity: ic(8), transform: `translateY(${(1 - ic(8)) * 20}px)`}}>
            {e.aciklama}
          </div>
        )}
        {e.kunye && <div style={{position: 'absolute', right: 14, bottom: 8, color: '#fff', fontSize: 16, opacity: 0.7}}>{e.kunye}</div>}
      </div>
    );
  }
  return null;
};

export const EklemeKatmani: React.FC<{sahne: Sahne; marka: Marka; alan: Alan}> = ({sahne, marka, alan}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = f / fps;
  return (
    <>
      {(sahne.eklemeler || []).filter((e) => e.tip !== 'slayt_zoom' && t >= e.bas - 0.05 && t <= e.bit + 0.05)
        .map((e, i) => <Kart key={i} e={e} marka={marka} alan={alan} />)}
    </>
  );
};

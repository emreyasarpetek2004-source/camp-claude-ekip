import React from 'react';
import {AbsoluteFill, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {Klip, Marka} from '../tipler';

// Son 2 sn: marka kartı (logo + hoca + webinar). CTA metni yok, caption'da.
export const Kapanis: React.FC<{klip: Klip; marka: Marka; sure: number; baslik?: string}> = ({klip, marka, baslik}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const g = interpolate(f, [0, 8], [0, 1], {extrapolateRight: 'clamp'});
  const logo = spring({frame: f - 4, fps, config: {damping: 12, stiffness: 160}});
  const yazi = spring({frame: f - 12, fps, config: {damping: 16, stiffness: 140}});
  return (
    <AbsoluteFill style={{opacity: g, background: marka.v2.tema === 'acik' && marka.v2.zemin_acik
        ? `radial-gradient(circle at 50% 40%, ${marka.v2.zemin_acik.leke} 0%, ${marka.v2.zemin_acik.ust} 55%, ${marka.v2.zemin_acik.alt} 100%)`
        : `radial-gradient(circle at 50% 42%, ${marka.zemin.vurgu} 0%, ${marka.zemin.alt} 70%)`,
      alignItems: 'center', justifyContent: 'center', flexDirection: 'column'}}>
      {marka.v2.logo ? (
        <div style={{transform: `scale(${logo})`, background: marka.v2.tema === 'acik' ? 'transparent' : '#fff', borderRadius: 36,
          padding: '38px 56px', boxShadow: marka.v2.tema === 'acik' ? 'none' : '0 24px 70px rgba(0,0,0,0.45)'}}>
          <Img src={staticFile('marka/' + marka.v2.logo)} style={{width: 620}} />
        </div>
      ) : (
        <div style={{transform: `scale(${logo})`, color: '#fff', fontWeight: 800, fontSize: 120}}>{marka.ad}</div>
      )}
      <div style={{marginTop: 80, opacity: yazi, transform: `translateY(${(1 - yazi) * 30}px)`, textAlign: 'center', padding: '0 70px'}}>
        <div style={{color: marka.v2.tema === 'acik' ? (marka.v2.metin || '#111') : '#fff', fontWeight: 800, fontSize: 58, lineHeight: 1.18, letterSpacing: -0.5}}>
          {marka.v2.kapanis?.baslik || baslik || klip.webinar}</div>
        {marka.v2.kapanis?.alt && (() => {
          // DM çağrısı: zıplayarak açılan buton + sürekli nabız + yayılan halkalar (kullanıcı: "animasyon koy, popupla vurgula")
          const p = spring({frame: f - 14, fps, config: {damping: 8, stiffness: 190, mass: 0.8}});
          const nabiz = 1 + 0.045 * Math.sin(Math.max(0, f - 24) / 4.2);
          const halka = (gec: number) => { const k = ((Math.max(0, f - 20 - gec)) % 24) / 24; return {s: 1 + 0.5 * k, o: f >= 20 + gec ? 0.7 * (1 - k) : 0}; };
          return <div style={{position: 'relative', display: 'inline-block', marginTop: 40}}>
            {[halka(0), halka(12)].map((h, i) => <div key={i} style={{position: 'absolute', inset: 0, borderRadius: 60,
              border: `5px solid ${marka.v2.vurgu}`, opacity: h.o, transform: `scale(${h.s})`}} />)}
            <div style={{display: 'flex', alignItems: 'center', gap: 18, background: marka.v2.vurgu, color: marka.v2.vurgu_ustu || marka.v2.koyu,
              fontWeight: 800, fontSize: 42, padding: '18px 38px', borderRadius: 60, whiteSpace: 'nowrap',
              transform: `scale(${p * nabiz}) rotate(${(1 - p) * -8}deg)`, opacity: Math.min(1, p * 1.5),
              boxShadow: `0 18px 44px rgba(0,0,0,0.45), 0 0 50px ${marka.v2.vurgu}aa`}}>
              <svg width="46" height="46" viewBox="0 0 24 24" fill="none" stroke={marka.v2.vurgu_ustu || marka.v2.koyu} strokeWidth="2.4" strokeLinejoin="round">
                <path d="M22 2 11 13" /><path d="M22 2 15 22l-4-9-9-4 20-7z" /></svg>
              {marka.v2.kapanis.alt}
            </div>
          </div>;
        })()}
        {marka.v2.kapanis?.iletisim && <div style={{display: 'flex', justifyContent: 'center', gap: 46, marginTop: 40,
          color: marka.v2.tema === 'acik' ? (marka.v2.metin || '#111') : marka.v2.acik, fontWeight: 600, fontSize: 36, opacity: interpolate(f, [16, 26], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})}}>
          {marka.v2.kapanis.iletisim.map((x, i) => {
            // emoji headless Chrome'da renksiz/küçük çıkıyor: baştaki 🌐/📲 marka renginde SVG ikona çevrilir
            const web = x.startsWith('🌐'), tel = x.startsWith('📲');
            const metin = x.replace(/^(🌐|📲)\s*/u, '');
            return <span key={i} style={{whiteSpace: 'nowrap', display: 'inline-flex', alignItems: 'center', gap: 14}}>
              {web && <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke={marka.v2.tema === 'acik' ? marka.v2.vurgu2 : marka.v2.vurgu} strokeWidth="2">
                <circle cx="12" cy="12" r="10" /><path d="M2 12h20M12 2c3 3.2 3 16.8 0 20M12 2c-3 3.2-3 16.8 0 20" /></svg>}
              {tel && <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke={marka.v2.tema === 'acik' ? marka.v2.vurgu2 : marka.v2.vurgu} strokeWidth="2" strokeLinecap="round">
                <rect x="6" y="2" width="12" height="20" rx="2.5" /><path d="M10.5 18.5h3" /></svg>}
              {metin}</span>;
          })}
        </div>}
      </div>
    </AbsoluteFill>
  );
};

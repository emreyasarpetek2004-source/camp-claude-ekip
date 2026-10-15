import {continueRender, delayRender, staticFile} from 'remotion';

let yuklendi = false;
// Poppins ExtraBold/Bold/SemiBold yerel dosyadan (render_pub/marka/). Ağ yok, sürüm sabit.
export const fontYukle = () => {
  if (yuklendi || typeof document === 'undefined') return;
  yuklendi = true;
  const h = delayRender('font');
  const agirliklar: [string, string][] = [['800', 'Poppins-ExtraBold.ttf'], ['700', 'Poppins-Bold.ttf'], ['600', 'Poppins-SemiBold.ttf'], ['500', 'Poppins-Medium.ttf']];
  Promise.all(agirliklar.map(([w, d]) => {
    const ff = new FontFace('PoppinsX', `url(${staticFile('marka/' + d)})`, {weight: w});
    return ff.load().then((x) => (document as any).fonts.add(x));
  })).then(() => continueRender(h)).catch((e) => { console.error(e); continueRender(h); });
};

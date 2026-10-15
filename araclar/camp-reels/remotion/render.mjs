// Kullanım: node render.mjs <proje_dizini> <no> [--taslak]
// render_pub/ = Remotion public dizini (yalnız gereken dosyalar; edit/ içindeki 150 MB ses.wav kopyalanmasın)
import {bundle} from '@remotion/bundler';
import {renderMedia, selectComposition} from '@remotion/renderer';
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';

const [proje, noStr, ...bayrak] = process.argv.slice(2);
const taslak = bayrak.includes('--taslak');
const no = String(noStr).padStart(2, '0');
const KOK = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const edit = path.join(proje, 'edit');
const meta = JSON.parse(fs.readFileSync(path.join(proje, 'proje.json')));
const marka = JSON.parse(fs.readFileSync(path.join(KOK, 'brands', meta.marka + '.json')));
const klip = JSON.parse(fs.readFileSync(path.join(edit, `klip_${no}`, 'klip.json')));
const sahne = JSON.parse(fs.readFileSync(path.join(edit, `sahne_${no}.json`)));

const pub = path.join(edit, 'render_pub');
fs.mkdirSync(pub, {recursive: true});
const bag = (hedef, ad) => { const p = path.join(pub, ad); try { fs.rmSync(p, {recursive: true, force: true}); } catch {} fs.symlinkSync(hedef, p); };
bag(path.join(edit, `klip_${no}`), `klip_${no}`);
bag(path.join(KOK, 'sfx'), 'sfx');
if (fs.existsSync(path.join(KOK, 'emoji'))) bag(path.join(KOK, 'emoji'), 'emoji');
if (fs.existsSync(path.join(edit, 'assets'))) bag(path.join(edit, 'assets'), 'assets');
const md = path.join(pub, 'marka');
fs.mkdirSync(md, {recursive: true});
for (const f of ['Poppins-ExtraBold.ttf', 'Poppins-Bold.ttf', 'Poppins-SemiBold.ttf', 'Poppins-Medium.ttf'])
  fs.copyFileSync(path.join(os.homedir(), 'Library/Fonts', f), path.join(md, f));
if (marka.v2?.logo) fs.copyFileSync(path.join(KOK, 'brands', 'logo', meta.marka + '.png'), path.join(md, marka.v2.logo));

const serveUrl = await bundle({entryPoint: path.join(KOK, 'remotion/src/index.ts'), publicDir: pub});
const inputProps = {klip, sahne, marka};
const comp = await selectComposition({serveUrl, id: 'Reels', inputProps});
const out = path.join(proje, 'out', `reels_${no}.mp4`);
fs.mkdirSync(path.dirname(out), {recursive: true});
let son = -1;
await renderMedia({
  composition: comp, serveUrl, codec: 'h264', outputLocation: out, inputProps,
  crf: taslak ? 26 : 17, x264Preset: taslak ? 'veryfast' : 'medium', pixelFormat: 'yuv420p',
  audioCodec: 'aac', audioBitrate: '192k', concurrency: Math.max(2, os.cpus().length - 2),
  onProgress: ({progress}) => { const p = Math.floor(progress * 10); if (p !== son) { son = p; process.stdout.write(`${p * 10}% `); } },
});
console.log('\n' + out);
// geçici webpack paketi her basımda ~26 MB bırakıyor; 58 basımda disk doldu (9 Eki 2026): sil
try { fs.rmSync(serveUrl, {recursive: true, force: true}); } catch {}

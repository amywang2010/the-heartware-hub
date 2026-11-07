/**
 * RENDER.MJS -- turns stage.html into the photography the site uses.
 *
 *   node studio/render.mjs stills      five stills at 2000 px
 *   node studio/render.mjs video       a 6 s turntable, 1280x720, h264
 *
 * Headless Chrome has no GPU here, so WebGL runs on SwiftShader. That is slow
 * but deterministic, which is what a repeatable asset pipeline wants.
 */

import { chromium } from 'playwright';
import path from 'node:path';
import fs from 'node:fs';
import { spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');
const OUT = path.join(ROOT, 'assets', 'img');
const FRAMES = path.join(ROOT, '.studio-frames');
const PORT = 8231;

const FFMPEG =
  process.env.FFMPEG ||
  'C:/Users/Okapi/eigenpulse-cuff/viz/bin/ffmpeg-9.0.2-essentials_build/bin/ffmpeg.exe';

const STILLS = [
  { view: 'hero', w: 2000, h: 2400 },
  { view: 'macro', w: 2200, h: 1650 },
  { view: 'installed', w: 2000, h: 1600 },
  { view: 'explode', w: 2200, h: 1650, explode: 1 },
  { view: 'back', w: 1800, h: 1800 }
];

function serve() {
  const p = spawn('python', ['-m', 'http.server', String(PORT)], {
    cwd: ROOT,
    stdio: 'ignore',
    windowsHide: true
  });
  return p;
}

const wait = (ms) => new Promise((r) => setTimeout(r, ms));

async function shoot(page, url, file, timeout = 180000) {
  const errs = [];
  page.on('pageerror', (e) => errs.push(e.message));
  await page.goto(url, { waitUntil: 'load' });
  await page.waitForFunction('window.__ready === true', { timeout });
  await wait(600);
  await page.screenshot({ path: file, timeout });
  if (errs.length) console.log('  errors:', errs);
  return errs;
}

async function stills(browser, only) {
  for (const s of STILLS) {
    if (only && only !== s.view) continue;
    const page = await browser.newPage({ viewport: { width: s.w, height: s.h } });
    const q = new URLSearchParams({ view: s.view, w: s.w, h: s.h, explode: s.explode || 0 });
    const file = path.join(OUT, `product-${s.view}.png`);
    await shoot(page, `http://localhost:${PORT}/studio/stage.html?${q}`, file);
    q.set('depth', '1');
    await shoot(page, `http://localhost:${PORT}/studio/stage.html?${q}`,
      path.join(OUT, `product-${s.view}.depth.png`), 120000);
    console.log('still', path.basename(file), s.w + 'x' + s.h);
    await page.close();
  }
}

async function video(browser) {
  fs.rmSync(FRAMES, { recursive: true, force: true });
  fs.mkdirSync(FRAMES, { recursive: true });
  const W = 1280, H = 720, N = 150;
  const page = await browser.newPage({ viewport: { width: W, height: H } });
  await shoot(page, `http://localhost:${PORT}/studio/stage.html?view=hero&w=${W}&h=${H}`, path.join(FRAMES, 'seed.png'));
  for (let i = 0; i < N; i++) {
    await page.evaluate((t) => window.__shoot(t), i / N);
    await page.screenshot({ path: path.join(FRAMES, `f${String(i).padStart(4, '0')}.png`) });
    if (i % 25 === 0) console.log('  frame', i);
  }
  await page.close();

  const mp4 = path.join(OUT, 'product-loop.mp4');
  const args = [
    '-y', '-framerate', '25', '-i', path.join(FRAMES, 'f%04d.png'),
    '-vf', 'scale=1280:-2:flags=lanczos',
    '-c:v', 'libx264', '-profile:v', 'high', '-crf', '24', '-pix_fmt', 'yuv420p',
    '-movflags', '+faststart', '-an', mp4
  ];
  const r = spawn(FFMPEG, args, { stdio: 'inherit' });
  await new Promise((res, rej) => r.on('close', (c) => (c === 0 ? res() : rej(new Error('ffmpeg ' + c)))));
  console.log('video', mp4, (fs.statSync(mp4).size / 1048576).toFixed(2) + ' MB');
}

async function main() {
  fs.mkdirSync(OUT, { recursive: true });
  const srv = serve();
  await wait(1200);
  const browser = await chromium.launch({
    args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader']
  });
  const what = process.argv[2] || 'stills';
  try {
    if (what === 'stills' || what === 'all') await stills(browser, process.argv[3]);
    if (what === 'video' || what === 'all') await video(browser);
  } finally {
    await browser.close();
    srv.kill();
  }
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});

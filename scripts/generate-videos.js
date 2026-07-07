#!/usr/bin/env node
/**
 * Coremagna — Kingham listing videoları (Kie.ai / Kling 2.5 Turbo Pro)
 *
 * Kullanım (repo kökünden):
 *   node scripts/generate-videos.js            # planı göster + onay iste
 *   node scripts/generate-videos.js --yes      # onaysız üret (kredi yakar)
 *   node scripts/generate-videos.js --only 01-exterior,03-kitchen
 *
 * Akış: images/raw/kling-kingham/*.jpg → kie file upload → createTask →
 *       poll recordInfo → images/raw/kling-kingham/out/<slug>.mp4
 *
 * Model: kling/v25-turbo-image-to-video-pro — 5 sn, 1080p, ~$0.21/video
 * Girdi görselleri 9:16 kırpık; Kling i2v çıktıyı görüntü oranında üretir.
 *
 * Not: generate-images.js'teki gibi tüm HTTP çağrıları curl üzerinden
 * (TLS-intercept proxy Node fetch'i asılı bırakıyor).
 */
'use strict';
const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');
const readline = require('readline');

const REPO = path.dirname(__dirname);
const SRC_DIR = path.join(REPO, 'images', 'raw', 'kling-kingham');
const OUT_DIR = path.join(SRC_DIR, 'out');
const API_BASE = 'https://api.kie.ai/api/v1/jobs';
const UPLOAD_URL = 'https://kieai.redpandaai.co/api/file-stream-upload';
const MODEL = 'kling/v2-5-turbo-image-to-video-pro';
const EST_USD_PER_VIDEO = 0.21;

const POLL_INTERVAL_MS = 15000;
const POLL_TIMEOUT_MS = 12 * 60 * 1000;

const NEGATIVE =
  'people, person, hands, face, pets, text, captions, watermark, logo, ' +
  'warped walls, bending lines, distorted furniture, morphing objects, ' +
  'static shot, frozen frame, no movement, still photo, ' +
  'changing room layout, extra rooms, cartoon, painting, low quality';

/*
 * v2 (2026-07-07): "sakin gimbal" yaklaşımı terk edildi. Referans analizi
 * (Rendy promosu + kullanıcının kendi killer_reel.mp4'ü) gösterdi ki bu tarz
 * videolarda etkileyicilik yavaş/temiz kamera hareketinden DEĞİL, hızlı
 * FPV-drone tarzı uçuştan ve motion blur'un kusurları gizlemesinden geliyor.
 * Yavaş+temiz istemek Kling'i "güvenli" oynayıp neredeyse dururken görmeye
 * itiyor. Bu yüzden prompt'lar artık FPV enerjisini hedefliyor: hızlı ileri
 * hareket, kapı/koridordan içeri "uçma" hissi, belirgin motion blur.
 * cfg_scale hepsinde 0.8 — görsele daha az sıkı bağlı kal, harekete izin ver.
 */
const SCENES = [
  {
    slug: '01-exterior',
    file: '01-exterior-front.jpg',
    cfgScale: 0.8,
    prompt:
      'FPV drone real estate video, fast energetic forward flight, strong cinematic motion ' +
      'blur on the edges of frame, this is a fast dynamic shot not a slow calm one. The ' +
      'drone accelerates forward straight toward the front door of the honey-coloured ' +
      'Cotswold stone cottage, rushing past the low stone garden wall and the topiary ' +
      'shrubs which blur past quickly in the foreground, while the cottage grows larger in ' +
      'frame. Warm morning sunlight, sun flare. Photorealistic, high energy real estate ' +
      'reel style, continuous accelerating motion from first frame to last frame.',
  },
  {
    slug: '02-fireplace',
    file: '02-living-fireplace.jpg',
    cfgScale: 0.75,
    prompt:
      'Fast energetic real estate reel shot, strong cinematic motion blur, continuous ' +
      'forward camera rush toward a black cast-iron wood-burning stove set in a white ' +
      'fireplace alcove. Warm orange flames roar and flicker vividly behind the glass door ' +
      'of the stove, casting a strong warm glow that pulses onto the surrounding white ' +
      'plaster and stacked firewood. Photorealistic, high energy real estate reel style, ' +
      'continuous accelerating motion from first frame to last frame.',
  },
  {
    slug: '02b-living',
    file: '02b-living-wide.jpg',
    cfgScale: 0.8,
    prompt:
      'FPV real estate video, fast energetic forward flight through a bright cottage living ' +
      'room straight toward the lit wood-burning stove, strong cinematic motion blur on the ' +
      'linen sofa and coffee table as they rush past in the foreground. The fire glows and ' +
      'flickers vividly inside the stove. Photorealistic, high energy real estate reel ' +
      'style, continuous accelerating motion from first frame to last frame.',
  },
  {
    slug: '03-kitchen',
    file: '03-kitchen.jpg',
    cfgScale: 0.8,
    prompt:
      'FPV real estate video, fast energetic forward flight through a bright cream cottage ' +
      'kitchen straight through the open glazed garden door out into the garden, strong ' +
      'cinematic motion blur as the worktop and open oak shelves rush past in the ' +
      'foreground. Green garden foliage grows larger ahead as the camera bursts through the ' +
      'doorway into daylight. Photorealistic, high energy real estate reel style, ' +
      'continuous accelerating motion from first frame to last frame.',
  },
  {
    slug: '04-bedroom',
    file: '04-bedroom.jpg',
    cfgScale: 0.8,
    prompt:
      'FPV real estate video, fast energetic forward flight low across the bed toward the ' +
      'window, strong cinematic motion blur on the linen pillows and throw as they rush ' +
      'past in the foreground below the camera, rustic oak ceiling beam blurring past ' +
      'overhead. Soft daylight flares as the camera approaches the window. Photorealistic, ' +
      'high energy real estate reel style, continuous accelerating motion from first frame ' +
      'to last frame.',
  },
  {
    slug: '05-dining',
    file: '05-dining.jpg',
    cfgScale: 0.8,
    prompt:
      'FPV real estate video, fast energetic forward flight over the dining table toward the ' +
      'painted staircase, strong cinematic motion blur on the chairs and pendant lamp as ' +
      'they rush past in the foreground, the staircase and window seat growing larger ahead. ' +
      'Photorealistic, high energy real estate reel style, continuous accelerating motion ' +
      'from first frame to last frame.',
  },
  {
    slug: '06-bathroom',
    file: '06-bathroom.jpg',
    cfgScale: 0.8,
    prompt:
      'FPV real estate video, fast energetic forward flight toward the bathtub and bright ' +
      'window, strong cinematic motion blur on the oak vanity and round brass mirror as ' +
      'they rush past in the foreground. Bright daylight flares near the window. ' +
      'Photorealistic, high energy real estate reel style, continuous accelerating motion ' +
      'from first frame to last frame.',
  },
];

// ---------- yardımcılar (generate-images.js ile aynı kalıp) ----------
function fail(msg) { console.error('HATA: ' + msg); process.exit(1); }

function loadEnv() {
  const envPath = path.join(REPO, '.env');
  if (fs.existsSync(envPath)) {
    for (const line of fs.readFileSync(envPath, 'utf8').split(/\r?\n/)) {
      const m = line.match(/^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*?)\s*$/);
      if (m && !(m[1] in process.env)) process.env[m[1]] = m[2].replace(/^["']|["']$/g, '');
    }
  }
  if (!process.env.KIE_API_KEY) fail('KIE_API_KEY bulunamadı (.env).');
  return process.env.KIE_API_KEY;
}

function curl(args, label, maxTime) {
  const r = spawnSync('curl', ['-sS', '--max-time', String(maxTime || 120), ...args], { encoding: 'utf8' });
  if (r.status !== 0) throw new Error(`${label}: curl çıkış kodu ${r.status} — ${(r.stderr || '').trim().slice(0, 300)}`);
  return r.stdout;
}

function apiJson(method, url, apiKey, body, label) {
  const args = ['-X', method, url,
    '-H', `Authorization: Bearer ${apiKey}`,
    '-H', 'Content-Type: application/json'];
  if (body) args.push('-d', JSON.stringify(body));
  const out = curl(args, label);
  let json;
  try { json = JSON.parse(out); }
  catch { throw new Error(`${label}: JSON çözülemedi — ${out.slice(0, 300)}`); }
  if (json.code !== 200) throw new Error(`${label}: API kodu ${json.code} — ${json.msg || ''}`);
  return json;
}

const sleep = (ms) => new Promise((res) => setTimeout(res, ms));

function askConfirm(question) {
  return new Promise((res) => {
    const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
    rl.question(question, (a) => { rl.close(); res(/^[ye]/i.test(a.trim())); });
  });
}

// ---------- adımlar ----------
function uploadImage(apiKey, filePath, label) {
  const out = curl([
    '-X', 'POST', UPLOAD_URL,
    '-H', `Authorization: Bearer ${apiKey}`,
    '-F', `file=@${filePath}`,
    '-F', 'uploadPath=kingham',
  ], label, 180);
  let json;
  try { json = JSON.parse(out); }
  catch { throw new Error(`${label}: upload JSON çözülemedi — ${out.slice(0, 300)}`); }
  const d = json.data || json;
  const url = d.downloadUrl || d.fileUrl || d.url || d.file_url;
  if (!url) throw new Error(`${label}: upload cevabında URL yok — ${out.slice(0, 300)}`);
  return url;
}

function createTask(apiKey, scene, imageUrl) {
  const json = apiJson('POST', `${API_BASE}/createTask`, apiKey, {
    model: MODEL,
    input: {
      prompt: scene.prompt,
      image_url: imageUrl,
      duration: '5',
      negative_prompt: NEGATIVE,
      cfg_scale: scene.cfgScale || 0.5,
    },
  }, `createTask ${scene.slug}`);
  const taskId = json.data && (json.data.taskId || json.data.task_id);
  if (!taskId) throw new Error(`createTask ${scene.slug}: taskId yok`);
  return taskId;
}

async function pollTask(apiKey, scene, taskId) {
  const start = Date.now();
  for (;;) {
    if (Date.now() - start > POLL_TIMEOUT_MS) throw new Error(`${scene.slug}: zaman aşımı (${taskId})`);
    await sleep(POLL_INTERVAL_MS);
    let json;
    try {
      json = apiJson('GET', `${API_BASE}/recordInfo?taskId=${taskId}`, apiKey, null, `recordInfo ${scene.slug}`);
    } catch (e) { console.log(`  ${scene.slug}: poll hatası, tekrar denenecek — ${e.message}`); continue; }
    const d = json.data || {};
    const state = d.state || d.status;
    if (state === 'success') {
      let result = d.resultJson;
      if (typeof result === 'string') { try { result = JSON.parse(result); } catch { result = {}; } }
      const urls = (result && (result.resultUrls || result.result_urls || result.videoUrls)) || [];
      if (!urls.length) throw new Error(`${scene.slug}: success ama video URL yok`);
      return { url: urls[0], credits: d.creditsConsumed || d.credits || null };
    }
    if (state === 'fail' || state === 'failed') {
      throw new Error(`${scene.slug}: üretim başarısız — ${d.failMsg || d.failCode || 'sebep yok'}`);
    }
    process.stdout.write(`  ${scene.slug}: ${state || '...'} (${Math.round((Date.now() - start) / 1000)}sn)\r`);
  }
}

function download(url, dest, label) {
  curl(['-L', '-o', dest, url], label, 300);
  const size = fs.existsSync(dest) ? fs.statSync(dest).size : 0;
  if (size < 100 * 1024) throw new Error(`${label}: indirilen dosya şüpheli küçük (${size}B)`);
  return size;
}

// ---------- main ----------
(async () => {
  const apiKey = loadEnv();
  const args = process.argv.slice(2);
  const yes = args.includes('--yes');
  const onlyIdx = args.indexOf('--only');
  let scenes = SCENES;
  if (onlyIdx !== -1 && args[onlyIdx + 1]) {
    const want = args[onlyIdx + 1].split(',').map((s) => s.trim());
    scenes = SCENES.filter((s) => want.some((w) => s.slug.startsWith(w)));
    if (!scenes.length) fail('--only ile eşleşen sahne yok');
  }

  for (const s of scenes) {
    if (!fs.existsSync(path.join(SRC_DIR, s.file))) fail(`Kaynak yok: ${s.file}`);
  }

  console.log(`Model : ${MODEL}`);
  console.log(`Süre  : 5 sn / video, 9:16, 1080p`);
  console.log(`Plan  : ${scenes.length} video → tahmini ~$${(scenes.length * EST_USD_PER_VIDEO).toFixed(2)}`);
  scenes.forEach((s) => console.log(`  - ${s.slug}  (${s.file})`));

  if (!yes) {
    const ok = await askConfirm('Kredi harcanacak. Devam? (y/e): ');
    if (!ok) { console.log('İptal.'); process.exit(0); }
  }

  fs.mkdirSync(OUT_DIR, { recursive: true });

  // 1) yükle + task aç (seri: upload büyük, rate limit rahat)
  const running = [];
  for (const s of scenes) {
    process.stdout.write(`Yükleniyor: ${s.file} ... `);
    const imageUrl = uploadImage(apiKey, path.join(SRC_DIR, s.file), `upload ${s.slug}`);
    console.log('ok');
    const taskId = createTask(apiKey, s, imageUrl);
    console.log(`Task açıldı: ${s.slug} → ${taskId}`);
    running.push({ scene: s, taskId });
    await sleep(1500);
  }

  // 2) hepsini paralel bekle
  const results = await Promise.allSettled(
    running.map(async ({ scene, taskId }) => {
      const r = await pollTask(apiKey, scene, taskId);
      const dest = path.join(OUT_DIR, `${scene.slug}.mp4`);
      const size = download(r.url, dest, `download ${scene.slug}`);
      console.log(`\nTAMAM: ${scene.slug}.mp4 (${(size / 1024 / 1024).toFixed(1)}MB)` +
        (r.credits ? ` — ${r.credits} kredi` : ''));
      return scene.slug;
    })
  );

  console.log('\n===== SONUÇ =====');
  let okCount = 0;
  results.forEach((r, i) => {
    if (r.status === 'fulfilled') { okCount++; console.log(`  OK   ${r.value}`); }
    else console.log(`  FAIL ${running[i].scene.slug} — ${r.reason.message}`);
  });
  console.log(`${okCount}/${results.length} video üretildi → ${OUT_DIR}`);
  process.exit(okCount === results.length ? 0 : 1);
})().catch((e) => fail(e.message));

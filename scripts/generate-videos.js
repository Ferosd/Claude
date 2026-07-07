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
  'flickering light, camera shake, fast motion, added objects, ' +
  'changing room layout, cartoon, painting, low quality';

const SCENES = [
  {
    slug: '01-exterior',
    file: '01-exterior-front.jpg',
    prompt:
      'Cinematic real estate listing video. The camera glides slowly forward toward the ' +
      'front door of a honey-coloured Cotswold stone cottage, a smooth stabilised gimbal ' +
      'push-in at slow walking pace. Gentle parallax between the low stone garden wall in ' +
      'the foreground and the cottage facade. The climbing plant on the wall and the grass ' +
      'tremble softly in a light breeze, clouds drift almost imperceptibly. Warm morning ' +
      'sunlight with soft shadows. Photorealistic, natural colour, the architecture stays ' +
      'perfectly rigid, window frames and the roofline remain dead straight.',
  },
  {
    slug: '02-fireplace',
    file: '02-living-fireplace.jpg',
    prompt:
      'Cinematic interior real estate video. Slow steady push-in toward a black cast-iron ' +
      'wood-burning stove set in a white fireplace alcove under an oak beam mantel. Warm ' +
      'orange flames flicker naturally behind the glass door of the stove, casting a subtle ' +
      'warm glow onto the surrounding white plaster and the stacked firewood. Everything ' +
      'else in the room stays completely still. Soft natural daylight mixing with firelight. ' +
      'Photorealistic, fixed smooth camera path, no objects move, appear or disappear.',
  },
  {
    slug: '02b-living',
    file: '02b-living-wide.jpg',
    prompt:
      'Cinematic interior real estate video. Slow smooth dolly forward through a bright ' +
      'cottage living room toward the lit wood-burning stove, gentle parallax past the ' +
      'linen sofa, the oak shelves and the coffee table. The fire glows and flickers softly ' +
      'inside the stove; everything else remains perfectly still. Soft diffused daylight ' +
      'from the window, calm high-end staging. Photorealistic, furniture and walls stay ' +
      'rigid and unchanged, straight lines remain straight.',
  },
  {
    slug: '03-kitchen',
    file: '03-kitchen.jpg',
    prompt:
      'Cinematic interior real estate video. Slow steady dolly forward through a bright ' +
      'cream cottage kitchen toward the open glazed garden door, gentle parallax past the ' +
      'worktop, the sink and the open oak shelves. Through the doorway, green garden ' +
      'foliage sways softly in the breeze and sunlight shifts gently on the stone step. ' +
      'The interior stays completely still. Soft natural daylight. Photorealistic, cabinet ' +
      'fronts and ceiling beams remain perfectly rigid, no new objects appear.',
  },
  {
    slug: '04-bedroom',
    file: '04-bedroom.jpg',
    prompt:
      'Cinematic interior real estate video. Very slow gentle push-in toward a neatly made ' +
      'bed layered with natural linen pillows and a soft throw, beneath a rustic oak ' +
      'ceiling beam. The light from the window breathes almost imperceptibly, as if a thin ' +
      'curtain moved outside the frame. Calm, serene, high-end staging. Soft daylight. ' +
      'Photorealistic, bedding keeps its exact folds, furniture and walls stay perfectly ' +
      'still, no morphing.',
  },
  {
    slug: '05-dining',
    file: '05-dining.jpg',
    prompt:
      'Cinematic interior real estate video. Slow push-in toward a rustic oak dining table ' +
      'with upholstered chairs, gentle parallax gradually revealing the painted staircase ' +
      'and the window seat beyond. The pendant lamp light stays constant; the leaves of the ' +
      'small plant on the table tremble very slightly. Soft natural daylight. Photorealistic, ' +
      'architecture and furniture remain rigid and unchanged, straight lines stay straight.',
  },
  {
    slug: '06-bathroom',
    file: '06-bathroom.jpg',
    prompt:
      'Cinematic interior real estate video. Slow steady push-in toward the bathtub beneath ' +
      'a bright window, gentle parallax past the oak vanity and the round brass mirror. The ' +
      'green stems in the vase sway very slightly; everything else is completely still. ' +
      'Bright soft daylight, clean spa-like calm. Photorealistic, tile lines and wall ' +
      'panelling remain dead straight, no objects appear or change.',
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
      cfg_scale: 0.5,
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

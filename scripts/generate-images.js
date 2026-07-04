#!/usr/bin/env node
/**
 * Coremagna — Nano Banana 2 görsel üretim otomasyonu (Kie.ai API)
 *
 * Kullanım (repo kökünden):
 *   node scripts/generate-images.js            # planı göster + onay iste
 *   node scripts/generate-images.js --yes      # onaysız üret (kredi yakar)
 *   node scripts/generate-images.js --only salon-chair,estate-keys
 *
 * Gereksinim: .env dosyasında KIE_API_KEY=...  (kie.ai dashboard'dan)
 * Prompt kaynağı: nano-banana-prompt-kiti.md (kök) yoksa docs/image-prompts.md
 * Çıktı: images/raw/<slug>-v1.jpg, <slug>-v2.jpg ...
 *
 * Not: Bu makinedeki TLS-intercept proxy Node'un kendi fetch'ini dış sitelere
 * asılı bırakıyor; o yüzden tüm HTTP çağrıları curl üzerinden yapılıyor.
 */
'use strict';
const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');
const readline = require('readline');

const REPO = path.dirname(__dirname);
const RAW_DIR = path.join(REPO, 'images', 'raw');
const API_BASE = 'https://api.kie.ai/api/v1/jobs';
const MODEL = 'nano-banana-2';
const EST_USD_PER_IMAGE = 0.04; // kie.ai fiyat sayfasındaki "from $0.04" — gerçek maliyet creditsConsumed'dan raporlanır

const CREATE_DELAY_MS = 1500;   // limit 20 istek/10sn — bunun çok altında kalıyoruz
const POLL_INTERVAL_MS = 5000;
const POLL_TIMEOUT_MS = 5 * 60 * 1000;
const MAX_RETRIES = 2;          // başarısız varyant başına ek deneme

// Kullanıcının güncellenmiş ortak sanat yönetmenliği bloğu (MD'deki ESKİ blok kullanılmaz)
const SHARED_BLOCK =
  'Editorial commercial photograph, shot on a real camera. Moody low-key lighting, ' +
  'deep charcoal and near-black environment (#060a0e tones), a single teal accent light ' +
  '(#00D4AA) used as rim light or practical glow, cinematic 35mm film look, shallow depth ' +
  'of field, subtle film grain, high dynamic range. Documentary realism: candid unstaged ' +
  'feel, natural imperfections like faint dust, smudges and fingerprints on surfaces, ' +
  'slight wear on furniture edges, uneven ambient light, true-to-life colour response, ' +
  'no CGI look, no 3D render, no illustration, not overly polished. No visible human ' +
  'faces, no readable text or brand logos anywhere in frame, no watermark.';

// Ekran içeren sahneler — prompt sonuna ek cümle
const SCREEN_SLUGS = new Set(['law-night', 'estate-keys', 'salon-phone']);
// Kalabalık sahneler — 3 varyant (artefakt riski), diğerleri 2
const TRIPLE_SLUGS = new Set(['estate-window', 'restaurant-host']);

// ---------- yardımcılar ----------
function fail(msg) { console.error('HATA: ' + msg); process.exit(1); }

function loadEnv() {
  const envPath = path.join(REPO, '.env');
  if (fs.existsSync(envPath)) {
    for (const line of fs.readFileSync(envPath, 'utf8').split(/\r?\n/)) {
      const m = line.match(/^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*?)\s*$/);
      if (m && !(m[1] in process.env)) process.env[m[1]] = m[2].replace(/^["']|["']$/g, '');
    }
  }
  if (!process.env.KIE_API_KEY) {
    fail('KIE_API_KEY bulunamadı. Repo köküne .env dosyası oluşturup içine yaz:\n  KIE_API_KEY=senin-anahtarın');
  }
  return process.env.KIE_API_KEY;
}

function curl(args, label) {
  const r = spawnSync('curl', ['-sS', '--max-time', '120', ...args], { encoding: 'utf8' });
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

// ---------- prompt kiti parse ----------
function findPromptKit() {
  for (const p of [path.join(REPO, 'nano-banana-prompt-kiti.md'), path.join(REPO, 'docs', 'image-prompts.md')]) {
    if (fs.existsSync(p)) return p;
  }
  fail('Prompt kiti bulunamadı (nano-banana-prompt-kiti.md veya docs/image-prompts.md).');
}

function parsePrompts(mdPath) {
  const md = fs.readFileSync(mdPath, 'utf8');
  const jobs = [];
  // Bölümler: "## N. slug — başlık" ... blockquote satırları prompt'un kendisi
  const sections = md.split(/^## /m).slice(1);
  for (const sec of sections) {
    const head = sec.match(/^(\d+)\.\s+([a-z0-9-]+)/);
    if (!head) continue;
    const slug = head[2];
    const quoteLines = sec.split(/\r?\n/).filter((l) => l.startsWith('>'));
    if (!quoteLines.length) continue;
    let prompt = quoteLines.map((l) => l.replace(/^>\s?/, '')).join(' ').replace(/\s+/g, ' ').trim();
    prompt += ' ' + SHARED_BLOCK;
    if (SCREEN_SLUGS.has(slug)) prompt += ' Screen content abstract and unreadable.';
    jobs.push({ num: +head[1], slug, prompt, variants: TRIPLE_SLUGS.has(slug) ? 3 : 2 });
  }
  return jobs;
}

function alreadyProduced(slug) {
  if (!fs.existsSync(RAW_DIR)) return false;
  return fs.readdirSync(RAW_DIR).some((f) => {
    const base = f.toLowerCase();
    return base === `${slug}.jpg` || base === `${slug}.png` || base === `${slug}.jpeg` ||
           base.startsWith(`${slug}-v`);
  });
}

// ---------- üretim ----------
async function generateOne(apiKey, slug, variant, prompt) {
  const created = apiJson('POST', `${API_BASE}/createTask`, apiKey, {
    model: MODEL,
    input: { prompt, aspect_ratio: '3:2', resolution: '2K', output_format: 'jpg' },
  }, `${slug}-v${variant} createTask`);
  const taskId = created.data && created.data.taskId;
  if (!taskId) throw new Error(`${slug}-v${variant}: taskId dönmedi`);

  const deadline = Date.now() + POLL_TIMEOUT_MS;
  while (true) {
    await sleep(POLL_INTERVAL_MS);
    if (Date.now() > deadline) throw new Error(`${slug}-v${variant}: ${POLL_TIMEOUT_MS / 60000} dk içinde bitmedi (taskId ${taskId})`);
    const info = apiJson('GET', `${API_BASE}/recordInfo?taskId=${encodeURIComponent(taskId)}`, apiKey, null, `${slug}-v${variant} recordInfo`);
    const d = info.data || {};
    if (d.state === 'success') {
      let urls = [];
      try { urls = JSON.parse(d.resultJson || '{}').resultUrls || []; } catch {}
      if (!urls.length) throw new Error(`${slug}-v${variant}: success ama resultUrls boş`);
      const dest = path.join(RAW_DIR, `${slug}-v${variant}.jpg`);
      curl(['-L', '-o', dest, urls[0]], `${slug}-v${variant} indirme`);
      const kb = Math.round(fs.statSync(dest).size / 1024);
      if (kb < 5) throw new Error(`${slug}-v${variant}: indirilen dosya şüpheli küçük (${kb} KB)`);
      return { dest, credits: d.creditsConsumed };
    }
    if (d.state === 'fail') throw new Error(`${slug}-v${variant}: üretim başarısız — ${d.failCode || ''} ${d.failMsg || ''}`);
    // waiting / queuing / generating → beklemeye devam
  }
}

async function main() {
  const argv = process.argv.slice(2);
  const yes = argv.includes('--yes');
  const onlyArg = argv.find((a) => a.startsWith('--only'));
  const only = onlyArg ? (onlyArg.split('=')[1] || argv[argv.indexOf(onlyArg) + 1] || '').split(',').filter(Boolean) : null;

  fs.mkdirSync(RAW_DIR, { recursive: true });

  const kitPath = findPromptKit();
  let jobs = parsePrompts(kitPath);
  if (only) jobs = jobs.filter((j) => only.includes(j.slug));

  const skipped = jobs.filter((j) => alreadyProduced(j.slug));
  jobs = jobs.filter((j) => !alreadyProduced(j.slug));

  const totalRequests = jobs.reduce((n, j) => n + j.variants, 0);
  console.log(`Prompt kiti: ${path.relative(REPO, kitPath)}`);
  if (skipped.length) console.log(`Atlanıyor (images/raw'da zaten var): ${skipped.map((j) => j.slug).join(', ')}`);
  console.log('\nÜretim planı:');
  for (const j of jobs) console.log(`  ${String(j.num).padStart(2)}. ${j.slug}  × ${j.variants} varyant`);
  console.log(`\nToplam istek: ${totalRequests}  |  Tahmini maliyet: ~$${(totalRequests * EST_USD_PER_IMAGE).toFixed(2)} (2K, "from $0.04"/görsel — kesin tutar creditsConsumed'dan raporlanır)`);

  if (!totalRequests) { console.log('Üretilecek görsel yok.'); return; }
  if (!yes) {
    if (!process.stdin.isTTY) { console.log('\nOnay için --yes ile çalıştır (kredi yakmadan durdu).'); return; }
    if (!(await askConfirm('\nDevam edilsin mi? (y/n) '))) { console.log('İptal edildi.'); return; }
  }
  const apiKey = loadEnv(); // plan onaylandıktan sonra, kredi yakmadan hemen önce

  const ok = [], failed = [], retried = [];
  let creditsTotal = 0;
  for (const j of jobs) {
    for (let v = 1; v <= j.variants; v++) {
      let done = false;
      for (let attempt = 0; attempt <= MAX_RETRIES && !done; attempt++) {
        if (attempt) { retried.push(`${j.slug}-v${v} (deneme ${attempt + 1})`); console.log(`  ↻ ${j.slug}-v${v}: tekrar deneniyor (${attempt}/${MAX_RETRIES})`); }
        try {
          const r = await generateOne(apiKey, j.slug, v, j.prompt);
          if (typeof r.credits === 'number') creditsTotal += r.credits;
          console.log(`  ✓ ${j.slug}-v${v} → ${path.relative(REPO, r.dest)}${r.credits ? `  (${r.credits} kredi)` : ''}`);
          ok.push(`${j.slug}-v${v}`);
          done = true;
        } catch (e) {
          console.log(`  ✗ ${j.slug}-v${v}: ${e.message}`);
          if (attempt === MAX_RETRIES) failed.push(`${j.slug}-v${v}`);
        }
      }
      await sleep(CREATE_DELAY_MS);
    }
  }

  console.log('\n──────── ÖZET ────────');
  console.log(`Başarılı: ${ok.length}/${totalRequests}${ok.length ? ' — ' + ok.join(', ') : ''}`);
  console.log(`Başarısız: ${failed.length}${failed.length ? ' — ' + failed.join(', ') : ''}`);
  console.log(`Retry yiyen: ${retried.length ? retried.join(', ') : 'yok'}`);
  if (creditsTotal) console.log(`Toplam harcanan kredi: ${creditsTotal}`);
  console.log('Bittiğinde Claude\'a "görseller hazır" de — webp dönüşümü ve sayfa yerleşimi oradan devam eder.');
}

main().catch((e) => fail(e.stack || e.message));

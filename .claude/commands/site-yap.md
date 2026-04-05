CLAUDE.md dosyasını oku ve tüm kurallara uy — istisnasız.

$ARGUMENTS

## Görevin

Coremagna ajans websitesini tek bir index.html olarak oluştur.
Inline CSS ve JS, framework yok, lorem ipsum yok.

---

## 1 — Başlamadan Önce

CLAUDE.md içindeki tüm skill kurallarını oku:
- Frontend-design kuralları
- Senior-frontend kuralları  
- Proje kuralları

Estetik yön: Koyu + sinematik + premium tech
Referans: forai.studio, clay.com
Font: Syne 800 (başlık) + DM Sans 300/400/500 (gövde)
Renk: #060a0e arka plan, #00D4AA teal aksan
Layout: Asimetrik, grid-breaking, bol negatif alan

---

## 2 — Hero Bölümü (Sinematik Video Banner)

Video dosyaları aynı klasörde:
- video1.mp4 → Web Design sahnesi
- video2.mp4 → RAG Chatbot sahnesi
- video3.mp4 → Automation sahnesi

Cross-fade geçiş sistemi:
- Mouse wheel scroll → sahne değişimi (aşağı=ileri, yukarı=geri)
- Mevcut video: opacity 1→0, scale 1.0→1.04, blur 0→6px (900ms)
- Yeni video: opacity 0→1, scale 1.04→1.0, blur 6px→0 (900ms)
- Ken Burns: her aktif video scale(1.0)→scale(1.06), 6s linear
- Metin geçişi: opacity+translateY fade out/in, spring easing
- 6 saniyede otomatik geçiş, mouseenter durur, mouseleave devam
- Debounce: 1100ms
- Touch swipe desteği (50px minimum)

Layout:
- Sol üst: "Coremagna" logo (Syne, "magna" #00D4AA)
- Sağ üst: slide sayacı (01 / 03)
- Sol alt: SERVICE I/II/III etiketi + büyük başlık + açıklama
- Sağ alt: dikey tıklanabilir timeline
- Alt: teal progress bar (2px)
- İlk 3sn: scroll hint animasyonu

Slide içerikleri:
Slide 1: SERVICE I | "Web Design & Development"
  "Modern, fast websites built to convert. From zero to live in 3 days."

Slide 2: SERVICE II | "RAG Chatbot & AI Integration"
  "An AI trained on your data — answers questions, qualifies leads, 24/7."

Slide 3: SERVICE III | "Automation & Workflows"
  "Eliminate manual work. Lead collection, emails, CRM — all automated."

---

## 3 — Tüm Sayfa Bölümleri

### Nav
Sticky, scroll'da backdrop-filter:blur(20px)
Sol: Coremagna logo | Orta: Services · Work · About · FAQ
Sağ: "Book a Call" (#00D4AA solid buton)
Mobil: hamburger menü

### Social Proof Bar
3 rakam: "50+ Projects" · "3 Continents" · "100% Retention"
Altında 5 adet placeholder client logo (gri kutu)

### Services (3 Kart)
Koyu yüzey (#0d1317), hover'da teal border (1px #00D4AA):

Kart 1 — Web Design & Development
"Your website, live in 3 days."
Mobile-first · SEO optimized · Conversion focused · CMS included
Starting from €499 | "Learn More →"

Kart 2 — RAG Chatbot & AI Integration
"An AI that knows your business inside out."
Trained on your data · 24/7 availability · Multilingual · Lead qualification
Starting from €299/month | "Learn More →"

Kart 3 — Automation & Workflows
"Stop doing manually what machines can do."
CRM integration · Email automation · Lead collection · Custom workflows
Starting from €199/month | "Learn More →"

### How It Works
4 adım, aralarında teal connector çizgi:
1. Free Audit — "We analyze your digital presence and find the gaps."
2. Strategy — "A tailored roadmap. No templates, no generic plans."
3. Build — "Fast execution. Most projects ship within 1 week."
4. Grow — "Ongoing support and optimization as you scale."

### Case Studies (3 Kart)
Case 1: München Restaurant Group
F&B · No online presence → +340% reservations in 60 days
Solution: Web Design + AI Chatbot

Case 2: Austin E-commerce
Retail · Manual support → 80% tickets automated
Solution: RAG Chatbot Integration

Case 3: Berlin Marketing Agency
Services · Slow leads → 3x faster response time
Solution: Automation & CRM Workflows

### Testimonials (3 Kart)
Teal tırnak işareti, koyu yüzey:

"Coremagna delivered our website in 4 days. The chatbot paid for itself in month one."
— Marco Berger, CEO @ Berger Consulting, Germany ★★★★★

"Finally an agency that speaks business, not tech jargon. Results were immediate."
— Sarah Mitchell, Founder @ Mitchell Retail Co., USA ★★★★★

"The automation saves us 15 hours a week. Best investment we've made."
— Lukas Hoffmann, Managing Director @ Hoffmann GmbH, Austria ★★★★★

### About
Başlık: "Built to deliver, not to impress."
"Coremagna is a remote-first digital agency helping SMBs in the US and Europe
compete with enterprise-level digital infrastructure. We move fast, communicate
clearly, and deliver results — not excuses."
3 değer: ⚡ Speed · 🔍 Transparency · 📈 ROI

### FAQ (Accordion, smooth animasyon)
1. Do I need technical knowledge? → No. We handle everything end-to-end.
2. How long does a project take? → Website: 3–7 days. Chatbot: 1–3 days. Automation: 1–2 weeks.
3. What does a RAG chatbot actually do? → It reads your documents and data, then answers customer questions 24/7 as if it were your best employee.
4. Do you offer ongoing support? → Yes. All plans include 30-day support. Monthly retainers available.
5. Is there a long-term contract? → No. Project-based or monthly. Cancel anytime.
6. Do you work with US-based clients? → Yes. US, Germany, Austria, Switzerland, and UK.
7. What if I already have a website? → Free audit. If it underperforms, we upgrade it.
8. How do I get started? → Book a free 30-minute strategy call. No commitment required.

### CTA Section
Başlık: "Ready to build something that works?"
Alt: "Book a free 30-minute strategy call. We'll audit your setup and show you exactly what's possible."
Buton: "Book a Free Call →" → href="https://calendly.com"
Koyu atmosferik arka plan + teal radial glow efekti

### Footer
Sol: Coremagna logo + tagline
Orta: Services (Web Design · RAG Chatbot · Automation) | Company (About · Work · FAQ)
Sağ: "Book a Call" + LinkedIn SVG ikonu
Alt: © 2025 Coremagna. All rights reserved.

---

## 4 — Teknik Gereksinimler

- Tek dosya: index.html, inline style ve script
- Scroll reveal: IntersectionObserver, staggered animation-delay
- Sayfa girişi: orchestrated entrance (nav → hero → içerik sırayla)
- Noise texture arka plan (SVG inline, opacity 0.035)
- Radial gradient mesh arka plan
- Favicon: inline SVG "C" harfi, #00D4AA
- title: "Coremagna — Digital Agency"
- description: "Web design, AI chatbots and automation for US and European businesses."
- Open Graph tags
- Video: autoplay muted loop playsinline
- transition-all YASAK
- Aktif olmayan slide videoları pause() — aktif olunca currentTime=0, play()

---

## 5 — Bitince

Tarayıcıda aç: start index.html

Screenshot al. Kontrol et:
1. Video cross-fade geçişi yumuşak mı?
2. Otomatik geçiş 6sn'de çalışıyor mu?
3. Mouse wheel scroll ile sahne değişiyor mu?
4. Scroll reveal animasyonlar geliyor mu?
5. Mobilde hero düzgün görünüyor mu?
6. "Bu site forai.studio ile rekabet edebilir mi?"

Hayırsa güçlendir. En az 2 screenshot turu yap.

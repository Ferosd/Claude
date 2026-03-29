# Coremagna — Claude Code Ana Kurallar

Bu dosya okunmadan tek satır kod yazılmaz. Her bölüm için geçerlidir.

---

## FRONTEND-DESIGN SKILL — Her Zaman Uygula

Frontend kodu yazmadan önce, her bölüm için, istisnasız bu kuralları uygula.

### Tasarım Düşüncesi
Kod yazmadan ÖNCE cesur bir estetik yön seç:
- **Amaç:** Bu arayüz hangi sorunu çözüyor? Kim kullanacak?
- **Ton:** Bir uç seç ve tam uygula
- **Farklılaşma:** Bu siteyi UNUTULMAZ yapan ne?

Coremagna için yön: **Koyu + sinematik + premium tech**
İlham: forai.studio, clay.com, writer.com — koyu temalar, bold tipografi, ürün UI gösterimleri.

### Tipografi
Display + body için ASLA aynı font:
- **Display:** Syne, Bricolage Grotesque, Cabinet Grotesk, Archivo Black, Fraunces
- **Body:** DM Sans, Manrope, Plus Jakarta Sans, Figtree
- Coremagna için: **Syne 800** (başlık) + **DM Sans 300/400/500** (gövde)
- Büyük başlıklarda: `letter-spacing: -0.03em`, `line-height: 0.95`
- Gövde: `line-height: 1.7`
- Google Fonts, `font-display: swap`

### Renkler
```css
--bg: #060a0e;
--surface: #0d1317;
--surface2: #111920;
--accent: #00D4AA;
--accent-dim: rgba(0, 212, 170, 0.12);
--text: #F0F4F3;
--muted: #6B8A8A;
--border: rgba(0, 212, 170, 0.1);
--border2: rgba(255,255,255,0.06);
--shadow-color: 0, 212, 170;
--space-xs: 4px; --space-sm: 8px; --space-md: 16px;
--space-lg: 24px; --space-xl: 48px; --space-2xl: 80px; --space-3xl: 120px;
```

### Shadows — Katmanlı, Renk Tonlu
Düz `shadow-md` YASAK:
```css
box-shadow:
  0 1px 2px rgba(var(--shadow-color), 0.04),
  0 4px 8px rgba(var(--shadow-color), 0.06),
  0 16px 32px rgba(var(--shadow-color), 0.08);
```

### Animasyonlar
- Sadece `transform`, `opacity`, `filter` animate et
- `transition-all` → YASAK, spesifik property yaz
- Spring easing: `cubic-bezier(0.34, 1.56, 0.64, 1)`
- Smooth easing: `cubic-bezier(0.4, 0, 0.2, 1)`
- IntersectionObserver ile scroll reveal, staggered `animation-delay`
- Sayfa girişinde orchestrated entrance — her bölüm sırayla gelsin

### Interactive States — İstisnasız
Her tıklanabilir elementte 3 state:
- **Hover:** transform + color shift (sadece opacity değil)
- **Focus-visible:** belirgin outline, erişilebilirlik
- **Active:** scale(0.97) veya renk değişimi

### Arka Plan — Atmosfer Zorunlu
Düz renk tembelliktir:
```css
/* Noise texture */
background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.035'/%3E%3C/svg%3E");

/* Radial gradient mesh */
background-image:
  radial-gradient(ellipse at 20% 50%, rgba(0,212,170,0.06) 0%, transparent 60%),
  radial-gradient(ellipse at 80% 20%, rgba(0,180,150,0.04) 0%, transparent 50%);
```

### Derinlik Sistemi
- **Base:** `--bg` (#060a0e) — ana arka plan
- **Elevated:** `--surface` (#0d1317) — kartlar, paneller
- **Floating:** `--surface2` (#111920) — modal, tooltip

### Görseller
```css
.img-container::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, rgba(0,0,0,0.7), transparent);
}
```

---

## SENIOR-FRONTEND SKILL — Her Zaman Uygula

### Semantic HTML
```html
<header> <nav> <main> <section> <article> <footer>
<!-- Her section'da anlamlı id -->
<section id="services"> <section id="about"> <section id="faq">
```

### Performance
- `loading="lazy"` tüm img için (hero hariç)
- `font-display: swap` Google Fonts
- `defer` tüm script tag'leri
- Video: `autoplay muted loop playsinline`
- Unsplash: `?w=800&q=80` formatı

### Accessibility
- Her img'de anlamlı `alt` metni
- `focus-visible` outline — `outline: none` tek başına YASAK
- `aria-label` tıklanabilir elementlerde
- WCAG AA kontrast minimum

### Responsive — Mobile-First
```
375px → default (mobile)
768px → tablet  (@media min-width: 768px)
1024px → desktop (@media min-width: 1024px)
1440px → wide   (@media min-width: 1440px)
```

### Scroll Reveal
```css
.reveal {
  opacity: 0;
  transform: translateY(24px);
  transition: opacity 0.6s cubic-bezier(0.4,0,0.2,1),
              transform 0.6s cubic-bezier(0.4,0,0.2,1);
}
.reveal.visible { opacity: 1; transform: none; }
```
```javascript
const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry, i) => {
    if (entry.isIntersecting) {
      entry.target.style.animationDelay = i * 0.1 + 's';
      entry.target.classList.add('visible');
    }
  });
}, { threshold: 0.1 });
document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
```

### Animasyon Kuralları
- Sadece `transform`, `opacity`, `filter` animate et
- `requestAnimationFrame` progress bar ve sürekli animasyonlar için
- `@media (prefers-reduced-motion: reduce)` ile animasyonları kapat

---

## PROJE KURALLARI — Coremagna

### Ajans Kimliği
Şu hizmetleri sunan ajans:
1. **Web Design & Development** — KOBİ'ler için modern, hızlı, dönüşüm odaklı siteler
2. **RAG Chatbot & AI Integration** — İşletmenin kendi verisini kullanan 7/24 AI asistanlar
3. **Automation & Workflows** — İş akışı otomasyonu, lead toplama, email kampanyası

**Hedef kitle:** ABD ve Avrupa KOBİ'leri. Teknik bilgisi olmayan işletme sahipleri.
**Ton:** Profesyonel, sonuç odaklı, jargonsuz. "Biz işi hallederiz, sen işine bak."
**Dil:** İngilizce (birincil). `<html lang="en">`

### Teknik
- **Tek dosya:** `index.html` — inline `<style>` ve `<script>`
- **Framework yok:** Saf HTML, CSS, JavaScript. Tailwind, Bootstrap, React YASAK.
- **Favicon:** Inline SVG "C" harfi, #00D4AA renk
- **İkonlar:** Inline SVG — Font Awesome YASAK
- **Meta:** `<title>`, `<meta description>`, Open Graph tags

### İçerik Kuralları
- Lorem ipsum YASAK — gerçekçi, ikna edici, ROI odaklı yaz
- CTA'lar net: "Book a Free Call", "Get a Free Audit", "See How It Works"
- Rakamlar kullan: "3 days to launch", "24/7 AI support", "80% automated"
- Testimonial'larda gerçekçi Avrupa/ABD işletme isimleri
- "We help businesses grow with AI" tarzı boş tagline YASAK — somut ol

### Sayfa Bölümleri
1. **Navigation** — Sticky, backdrop blur. Logo sol, linkler orta, "Book a Call" sağ. Hamburger mobilde.
2. **Hero** — Sinematik video banner (gru.space tarzı). video1/2/3.mp4. Scroll geçiş.
3. **Social Proof** — 3 rakam + client logo strip
4. **Services** — 3 kart: Web Design / RAG Chatbot / Automation. Fiyat aralığı dahil.
5. **How It Works** — 4 adım: Audit → Strategy → Build → Grow
6. **Case Studies** — 3 proje, somut metrikler
7. **Testimonials** — 3 müşteri yorumu, yıldız rating
8. **About** — Kısa hikaye + 3 değer
9. **FAQ** — Accordion, smooth animasyon, 8 soru
10. **CTA Section** — "Ready to build something that works?" + Calendly butonu
11. **Footer** — Logo, linkler, sosyal medya SVG, copyright

### Screenshot Workflow
- Puppeteer ile screenshot al
- PNG'yi Read tool ile oku ve analiz et
- Karşılaştırırken spesifik ol: "başlık 32px ama 48px olmalı"
- En az 2 karşılaştırma turu yap

### Kalite Kontrol — Her Bölüm Sonrası Sor
1. "Bu site forai.studio ile rekabet edebilir mi?" → Hayırsa yeniden yap
2. "Hero başlığı somut ve güçlü mü?" → "We do AI" değil, sonuç anlat
3. "Hizmetler ROI anlatıyor mu?" → Özellik değil, sonuç
4. "`transition-all` var mı?" → Kaldır
5. "Arka plan düz mı?" → Noise + gradient ekle
6. "Hover state sıkıcı mı?" → Transform + color ekle
7. "Shadow flat mı?" → Katmanlı yap
8. "Başka AI sitesine benziyor mu?" → Farklılaştır

---

## AI SLOP YASAK — Mutlak Kurallar

### Yasak Liste
- **Fontlar:** Inter, Roboto, Arial, system-ui → YASAK
- **Renkler:** Mor→mavi gradient, indigo-500, blue-600 birincil → YASAK
- **Layout:** 3 eşit simetrik kart, her şey ortalanmış → YASAK
- **Kod:** `transition-all` → YASAK
- **Shadow:** Düz `shadow-md` → YASAK
- **Arka plan:** Düz renk → YASAK
- **İçerik:** Boş tagline, lorem ipsum → YASAK

### Hard Rules — İstisnasız
- `transition-all` → YASAK
- Generic font (Inter, Roboto, Arial) → YASAK
- Mor/mavi AI gradient → YASAK
- Lorem ipsum → YASAK
- Düz arka plan → YASAK
- Screenshot kontrolü → ZORUNLU (en az 2 tur)
- Aynı font combo'yu tekrarlama → YASAK

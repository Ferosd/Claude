# Coremagna Agency Site

## Project Overview

AI automation agency targeting law firms, dental clinics, real estate agencies, mortgage brokers in UK, Australia, international markets.

**Founder:** Ferit Patefe (ferit1@coremagna.com)  
**Location:** Antalya, Turkey  
**Hosting:** Vercel (auto-deploy from GitHub repo Ferosd/Claude)  
**Booking:** https://calendar.app.google/XDGM8XJ9zEdqugKr9

## Tech Stack (LOCKED)

- HTML/CSS/JS only, no frameworks, no build step
- Fonts: Cabinet Grotesk (headings, 800), DM Sans (body), JetBrains Mono (numbers)
- Icons: Phosphor Icons inline SVG only. No emojis, no Lucide, no Font Awesome
- Animation: GSAP + ScrollTrigger via CDN
- Analytics: GA4 (G-7MDPMWZ158)

## CSS Variables (Define on every page)

```css
:root {
  --bg: #060a0e;
  --surface: #0d1117;
  --surface-2: #111920;
  --text: #F0F4F3;
  --text-secondary: #c0ccd8;
  --text-muted: #8a9ba8;
  --text-fine: #5a6b78;
  --border: #1a2530;
  --border-hover: rgba(0,212,170,0.4);
  --accent: #00D4AA;
  --accent-dim: rgba(0,212,170,0.12);
  --red: #e85d4a;
  --yellow: #f5c14a;
}

[data-theme="light"] {
  --bg: #fafbfc;
  --surface: #ffffff;
  --surface-2: #f4f6f8;
  --text: #0a1014;
  --text-secondary: #2a3340;
  --text-muted: #5a6b78;
  --text-fine: #8a9ba8;
  --border: #e1e5ea;
  --border-hover: rgba(0,184,148,0.5);
  --accent: #00B894;
  --accent-dim: rgba(0,184,148,0.10);
  --red: #d14a37;
  --yellow: #d49a2a;
}
```

Always use var(--*), never hardcode hex values.

## Design Rules

- Container: max-width 1280px, padding 0 32px (20px mobile)
- Asymmetric layouts (55/45 or 60/40), never centered hero
- Transitions: cubic-bezier(0.16, 1, 0.3, 1), animate only transform + opacity
- No transition-all, no neon glows, no 3 equal cards horizontally
- No Inter, no Plus Jakarta Sans, no purple/blue AI gradients

## Headings

- H1: clamp(2.4rem, 5vw, 3.5rem) max 56px desktop / 36px mobile, max-width 720px
- H2: clamp(1.8rem, 3.5vw, 2.5rem) max 40px desktop / 28px mobile, max-width 680px
- H3: 22px desktop / 18px mobile
- line-height: 1.05, letter-spacing: -0.02em, font-weight: 800
- Include: overflow-wrap: break-word; max-width: 100%; hyphens: none

## Heading Punctuation (CRITICAL)

REMOVE from all headings: periods (.) commas (,) colons (:) semicolons (;) em dashes and en dashes  
KEEP: question marks (?) apostrophes (') hyphens in compound words (after-hours, follow-up)

## Number Sizing

- Stat numbers (78%, $64K): clamp(2.5rem, 5vw, 4rem) max 64px
- Counter numbers: clamp(2.2rem, 4.5vw, 3.5rem) max 56px
- Pricing fees: clamp(2rem, 3.5vw, 2.5rem) max 40px
- Never use static large font sizes or font-size above 4rem

## Mobile Requirements

Breakpoints: 480px, 768px, 1024px, 1280px

At <768px: single column layouts, section padding 64px, container padding 20px, all tap targets min 44x44px, bottom padding 24px for iOS Safari

## Banned Copy

Never use: leverage, seamless, elevate, unleash, next-gen, cutting-edge, robust, synergy, harness, unlock potential, John Doe, Acme Corp, Lorem ipsum

## Pricing (LOCKED)

- Starter: $697 setup, $197/month
- Growth: $997 setup, $297/month (most popular, teal border + lift)
- Scale: $1,497 setup, $497/month
- API costs at cost, no markup

## Navigation Order

Industries > Work > About > Blog > FAQ > Contact > [Theme Toggle] > [Book a Call]

Services dropdown removed. Legacy service pages kept for SEO only.

## Site Structure

```
index.html, about.html, industries.html
industries/ (8 sub-pages: law-firms-*, real-estate-*)
blog/ (index.html, posts.json, 14 posts)
Legacy: web-design.html, rag-chatbot.html, automation.html, ai-voice-agent.html, ad-automation.html
```

## Sub-Page Framework (4 Questions)

1. Will it make money? (ROI calculator + revenue loss)
2. Will it be efficient? (Without/With comparison)
3. Will it beat competitors? (Speed-to-lead data)
4. Does it reduce risk? (6 guarantee cards)

Plus: How It Works (5 steps), Mockups, Before/After, Pricing, Final CTA

## Code Rules

- Absolute paths in nav (/industries.html)
- Semantic HTML tags
- All CTAs link to booking calendar
- Cards wrapped in <a> tags
- prefers-reduced-motion disables GSAP
- aria-hidden on decorative SVGs, aria-label on icon buttons

# Coremagna Agency Site — CLAUDE.md

## Project Overview

Coremagna is an AI automation agency targeting law firms, dental clinics, 
real estate agencies, and mortgage brokers in the UK, Australia, and 
international markets. This is the agency website at coremagna.com.

**Founder:** Ferit Patefe (ferit1@coremagna.com)
**Location:** Antalya, Turkey
**Target markets:** UK, Australia, Antalya/Turkey, US

## Tech Stack (LOCKED — DO NOT DEVIATE)

- **HTML/CSS/JS only** — no React, no frameworks, no build step
- **Hosting:** Vercel (auto-deploy from GitHub repo Ferosd/Claude)
- **Fonts:** Cabinet Grotesk (headings, weight 800), DM Sans (body), 
  JetBrains Mono (numbers/code)
- **Icons:** Phosphor Icons inline SVG only. NEVER use emojis. 
  NEVER use Lucide. NEVER use Font Awesome.
- **Animation library:** GSAP + ScrollTrigger via CDN
- **Analytics:** GA4 (ID: G-7MDPMWZ158)
- **Contact email:** ferit1@coremagna.com
- **Booking calendar:** https://calendar.app.google/XDGM8XJ9zEdqugKr9

## Color Palette & CSS Variables (CRITICAL)

NEVER hardcode color hex values in CSS. ALWAYS use var(--*) for all 
backgrounds, text, borders. This is required for light/dark mode support.

Define these variables on every page:

```css
:root {
  /* DARK MODE (default) */
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

**Rules:**
- The accent is slightly darker in light mode (#00B894 vs #00D4AA) for 
  contrast on white surfaces
- Body must use: `background: var(--bg); color: var(--text);`
- All cards must use: `background: var(--surface); border: 1px solid var(--border);`
- Red and yellow accents are used ONLY for negative comparisons / warnings

## Light/Dark Mode (REQUIRED on every page)

Every page must include a theme toggle button in the top-right of the nav 
bar (before the "Book a Call" button).

**HTML (in nav, right side):**
```html
<button class="theme-toggle" aria-label="Toggle light or dark theme" id="themeToggle">
  <svg class="sun-icon" width="18" height="18" viewBox="0 0 24 24" 
       fill="none" stroke="currentColor" stroke-width="1.5">
    <circle cx="12" cy="12" r="4"/>
    <path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/>
  </svg>
  <svg class="moon-icon" width="18" height="18" viewBox="0 0 24 24" 
       fill="none" stroke="currentColor" stroke-width="1.5" style="display:none">
    <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
  </svg>
</button>
```

**CSS:**
```css
.theme-toggle {
  width: 38px; height: 38px;
  background: transparent;
  border: 1px solid var(--border);
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  cursor: pointer;
  color: var(--text-muted);
  transition: border-color 0.3s cubic-bezier(0.16,1,0.3,1),
              color 0.3s cubic-bezier(0.16,1,0.3,1);
}
.theme-toggle:hover {
  border-color: var(--accent);
  color: var(--accent);
}
[data-theme="light"] .sun-icon { display: none; }
[data-theme="light"] .moon-icon { display: block; }
```

**JS (place at end of <body>):**
```javascript
(function() {
  const toggle = document.getElementById('themeToggle');
  const stored = localStorage.getItem('theme');
  const prefersLight = window.matchMedia('(prefers-color-scheme: light)').matches;
  if (stored === 'light' || (!stored && prefersLight)) {
    document.documentElement.setAttribute('data-theme', 'light');
  }
  toggle?.addEventListener('click', () => {
    const current = document.documentElement.getAttribute('data-theme');
    if (current === 'light') {
      document.documentElement.removeAttribute('data-theme');
      localStorage.setItem('theme', 'dark');
    } else {
      document.documentElement.setAttribute('data-theme', 'light');
      localStorage.setItem('theme', 'light');
    }
  });
})();
```

The toggle goes in EVERY HTML page. Same position, same logic.

## Design Rules (TASTE-SKILL APPLIED)

- DESIGN_VARIANCE: 8 — asymmetric layouts, NEVER centered hero, 
  prefer 55/45 or 60/40 splits over 50/50
- MOTION_INTENSITY: 6 — cubic-bezier(0.16, 1, 0.3, 1) transitions, 
  GSAP ScrollTrigger for scroll reveals, animate ONLY transform + opacity
- VISUAL_DENSITY: 4 — normal app spacing, use border lines and negative 
  space over excessive cards
- NO transition-all anywhere
- NO neon/outer glows — use inset borders and subtle tinted shadows
- NO 3 equal cards horizontally — use asymmetric grids
- NO Inter font, NO Plus Jakarta Sans, NO purple/blue AI gradients
- Container: max-width 1280px, padding 0 32px (24px mobile)

## Heading Style Rules

- H1: clamp(2.4rem, 5vw, 3.5rem) — max 56px desktop / 36px mobile, max-width 720px
- H2: clamp(1.8rem, 3.5vw, 2.5rem) — max 40px desktop / 28px mobile, max-width 680px
- H3: 22px desktop / 18px mobile
- line-height: 1.05 (NEVER tighter than 1.0, NEVER looser than 1.15)
- letter-spacing: -0.02em (NOT -0.03em — too tight)
- font-weight: 800 (Cabinet Grotesk only)
- Always include: `overflow-wrap: break-word; max-width: 100%; hyphens: none;`

## Punctuation in Headings (CRITICAL — APPLIED EVERYWHERE)

REMOVE these from all H1, H2, H3, H4 text:
  ✗ Commas (,)
  ✗ Periods (.)
  ✗ Em dashes (—)
  ✗ En dashes (–)
  ✗ Colons (:)
  ✗ Semicolons (;)

KEEP these:
  ✓ Question marks (?)
  ✓ Apostrophes (')
  ✓ Hyphens in compound words (after-hours, follow-up, 5-step)
  ✓ Numeric range dashes ($15,000–$50,000) — only inside data values

CORRECT:
  ✓ "What is one missed lead actually costing you?"
  ✓ "Stop Losing Cases Before They Walk In The Door"
  ✓ "Every Lead Perfectly Organised Automatically"

WRONG:
  ✗ "Stop losing cases, before they walk in."
  ✗ "Simple Pricing. Predictable ROI."
  ✗ "Built on Results, Not Retainers"

## Number Sizing (LIMITS — DO NOT EXCEED)

Big numbers tend to render too large. Apply these clamp() limits:

- Hero H1: clamp(2.4rem, 5vw, 3.5rem) — max 56px
- Section H2: clamp(1.8rem, 3.5vw, 2.5rem) — max 40px
- Big stat numbers (78%, $64K): clamp(2.5rem, 5vw, 4rem) — max 64px
- Counter numbers in stat banners: clamp(2.2rem, 4.5vw, 3.5rem) — max 56px
- Pricing setup fee ($697, $997): clamp(2rem, 3.5vw, 2.5rem) — max 40px
- Bento card big numbers: clamp(1.6rem, 3vw, 2.4rem) — max ~38px

NEVER use static large font sizes (font-size: 80px, font-size: 96px, etc.)
NEVER use font-size above 4rem on any heading or stat number.

## Mobile-First Requirements

Every page MUST work flawlessly at 375px viewport (iPhone SE width).

Required breakpoints:
- 480px: small phones
- 768px: tablets
- 1024px: laptops  
- 1280px: desktops

Mobile rules (apply at <768px):
- All asymmetric grid layouts collapse to single column
- Pricing cards stack vertically, "Most Popular" card NOT elevated 
  (no translateY)
- Hero text alignment can stay left-aligned, but visuals stack below
- Section vertical padding 64px (not 100px+)
- Container horizontal padding 20px (not 32px)
- Font sizes scale via clamp() — see Number Sizing
- Tables → wrap in horizontal scroll container, never break layout
- All interactive elements (buttons, cards, toggles) → minimum 44×44px tap target
- Bottom nav padding 24px to clear iOS Safari toolbar

## Copy Guidelines (BANNED PHRASES)

NEVER use these AI-cliché words:
- "leverage", "seamless", "elevate", "unleash", "next-gen", 
  "cutting-edge", "robust", "synergy", "harness", "unlock potential"

NEVER use generic data:
- "John Doe", "Acme Corp", "Lorem ipsum", "$99.99", "50%", 
  predictable phone numbers like "+1 555 123 4567"

USE realistic data: 
- "Marcus Whitfield", "Sterling Fintech Solutions", 
  "+44 7700 900123", organic numbers like "47.2%", "€8,400"

## Pricing (LOCKED — DO NOT CHANGE WITHOUT APPROVAL)

All service pages use these three tiers:

**STARTER**
- Setup: $697 one-time
- Monthly: $197/month

**GROWTH** (most popular, always elevated visually with teal border + lift)
- Setup: $997 one-time
- Monthly: $297/month

**SCALE**
- Setup: $1,497 one-time  
- Monthly: $497/month

API costs billed at cost — no markup.
Always include the line: "One captured case pays for 12 months of the system."

## Site Structure
/
├── index.html                          # Home (Three.js cube grid hero)
├── about.html                          # About page
├── industries.html                     # Industries hub (DONE)
├── industries/
│   ├── law-firms-enquiry.html          # CRM Lead Automation (DONE)
│   ├── law-firms-after-hours.html      # AI Chatbot (DONE)
│   ├── law-firms-intake.html           # Manual Case Intake (PLACEHOLDER)
│   ├── law-firms-followup.html         # No Follow-Up (PLACEHOLDER)
│   ├── real-estate-viewings.html       # PLACEHOLDER
│   ├── real-estate-leads.html          # PLACEHOLDER
│   ├── real-estate-vendors.html        # PLACEHOLDER
│   └── real-estate-noshow.html         # PLACEHOLDER
├── blog/
│   ├── index.html                      # Blog hub
│   ├── posts.json                      # Dynamic data
│   └── [14 blog posts].html
├── web-design.html                     # Legacy service page (kept for SEO)
├── rag-chatbot.html                    # Legacy service page
├── automation.html                     # Legacy service page
├── ai-voice-agent.html                 # Legacy service page
├── ad-automation.html                  # Legacy service page
└── skills/                             # Claude Code skill folders
    ├── taste-skill/                    # Primary frontend design rules
    ├── brutalist-skill/
    ├── minimalist-skill/
    ├── soft-skill/
    ├── stitch-skill/
    ├── output-skill/
    └── redesign-skill/

## Navigation Order (LATEST — Services REMOVED)

Industries → Work → About → Blog → FAQ → Contact → [Theme Toggle] → [Book a Call]

The Services dropdown is REMOVED from the nav. Industries replaces it. 
The legacy service pages (web-design, rag-chatbot, etc.) still exist for 
SEO but are no longer in the nav. They may be linked from industries 
sub-pages where relevant.

The "Industries" link must use absolute path: /industries.html

## Industries Page Structure

industries.html has 2 categories:
1. **Law Firms** — 4 problem-cards: Slow Enquiry Response, After-Hours 
   Lead Loss, Manual Case Intake, No Follow-Up System
2. **Real Estate** — 4 problem-cards: Missed Viewing Requests, Slow 
   Lead Response, Manual Vendor Updates, No-Show Viewings

Each card MUST be wrapped in an <a> tag making the entire card clickable.

## Sub-Page Structure (Service Pages)

Each industry sub-page follows this 4-question framework:

1. **Will it make money?** — ROI calculator + revenue loss stats
2. **Will it be efficient?** — Without/With Coremagna comparison + 
   hours saved × billable rate
3. **Will it beat competitors?** — Speed-to-lead chart + conversion data
4. **Does it reduce risk?** — 6 guarantee cards (14-day refund, 
   30-day support, your data stays yours, 7 days to live, dedicated 
   onboarding, direct account manager access)

Plus: How It Works (5 steps), Real System mockups, Before/After table, 
Pricing (3 tiers), Final CTA.

## Recent Work Completed

- ✅ industries.html built with 2 categories, 8 sub-cards, asymmetric layout
- ✅ 8 placeholder sub-pages created
- ✅ Nav updated across all 22+ HTML files
- ✅ industries/law-firms-enquiry.html — CRM Lead Automation full sales page
- ✅ industries/law-firms-after-hours.html — AI Chatbot full sales page 
     with live Harlow & Partners chat mockup
- ✅ Pricing values standardised to $697 / $997 / $1,497
- ✅ Banned fonts removed (Inter, Plus Jakarta Sans)
- ✅ Container width unified at 1280px
- ✅ CLAUDE.md migrated to English
- ✅ node_modules and old screenshot files cleaned up

## Pending Work (Priority Order)

1. industries/law-firms-intake.html — Manual Case Intake content
2. industries/law-firms-followup.html — No Follow-Up content
3. industries/real-estate-*.html — 4 sub-pages content
4. Light/dark mode toggle applied to ALL existing pages
5. Demos page (showcase the automation demos)
6. Built by Us style page
7. About page optimization
8. Contact page optimization
9. Home page redesign (requires planning discussion)
10. Mobile compatibility audit
11. SEO: sitemap.xml + robots.txt + Search Console submit
12. Final bug audit + fix pass

## Code Conventions

- File paths: use absolute paths in nav (/industries.html, not 
  ../industries.html or ./industries.html)
- HTML structure: semantic tags (header, nav, main, section, article, footer)
- All CTAs link to: https://calendar.app.google/XDGM8XJ9zEdqugKr9
- All interactive cards must be <a> tags wrapping the full content, 
  not just title links
- prefers-reduced-motion media query must disable all GSAP animations
- aria-hidden="true" on decorative SVG icons
- aria-label on icon-only buttons (incl. theme-toggle)
- NEVER hardcode color hex — always use var(--*) so light/dark works

## File Cleanup Rules

The project must NOT contain:
- node_modules/ (no build process used — add to .gitignore)
- Old screenshot files in root: ss_*, qa_*, final_*, v2_* prefixed PNGs
- Backup files: *.bak, *.old, *_backup.html
- package.json / package-lock.json (no Node build needed)

.gitignore must include:
node_modules/
.DS_Store
*.log
*.bak
.env
.env.local

## Files in /skills/ Folder

These are Claude Code skill folders — reference them when generating 
new pages or sections:
- **taste-skill** — primary frontend design rules (DESIGN_VARIANCE, 
  MOTION_INTENSITY, VISUAL_DENSITY) — read this BEFORE building any page
- brutalist-skill, minimalist-skill, soft-skill — alternate aesthetics
- stitch-skill, output-skill — specialized output rules
- redesign-skill — page redesign guidelines

When user requests a new page or section, read taste-skill/SKILL.md 
first to apply correct design rules.

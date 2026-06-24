# TPO Group — Design System

A working design system for **TPO Group**, a cybersecurity consulting firm.

> _"TPO Group leads in mission-critical, high-stakes cybersecurity consulting through strategic experience and technical prowess."_

The three pillars **Technology · Policy · Operations** give the firm its name and structure every piece of communication.

---

## 1. Company & Product Context

**Who they are.** TPO Group is a boutique cybersecurity consulting firm serving critical infrastructure, government agencies, and large enterprises. Locations: Boston, New York, Washington, Seattle, Austin, San Francisco, London.

**What they sell.** Advisory services, not software. Engagements are sold as named service lines:

- **Resilience Growth Strategy** — bespoke, 360-degree security strategy
- **vCISO** — fractional executive partnership
- **Incident Response** — adversary containment and eradication
- **Policy Navigation** — global policy roadmaps for industry/government
- **Cloud Security Architecture Services** — complex migrations
- **Digital Supply Chain Risk Management** — interconnected-ecosystem security
- **Executive Education** — uplift for security teams
- **SOC Enhancement** — tools, intel, and AI integration
- **Insider Threat Management** — program design and investigations

**Audience.** CISOs, GCs, Heads of Risk, government program owners. Buyers who are themselves technical, want to see depth and gravitas, and will not tolerate hype, gradient-of-the-week, or marketing fluff.

**Tone.** Quiet authority. Formal but not stiff. Government / national-security adjacency.

**Surfaces represented in this system.**
- Marketing website (`tpo.group`, built on Wix) — _the only public surface today_
- Logo system (provided directly by the user)

There is no app, no docs site, no admin panel. This design system therefore ships **one UI kit** (the marketing website) plus brand foundations, slide samples, and primitives suitable for proposal decks, RFP responses, and one-pagers.

---

## 2. Sources Consulted

- `https://www.tpo.group/` — home
- `https://www.tpo.group/services` — service catalog
- User-supplied logo files (see `uploads/` → copied into `assets/logos/`):
  - `tpo_group_logo.jpg` / `.png` — primary logotype
  - `tpo_group_logo_fordarkbackground.png` — primary + bars motif, dark-bg lockup
  - `tpo_group_logo_withtagline.png` — primary + "TECHNOLOGY · POLICY · OPERATIONS" lockup

No codebase, Figma, or design-token export was shared; the system below is derived from the live website + logo artwork.

---

## 3. Content Fundamentals

**Voice.** Authoritative, plainspoken, security-professional. Reads like a senior consultant briefing a board, not a SaaS landing page.

**Person.** Third-person institutional ("TPO Group leads…", "Our custom solutions…") and first-person plural ("we tune existing tools…"). Never second-person hype ("You'll love…"). Customers are referred to as **clients**.

**Casing.**
- Section labels and the three pillars are **ALL CAPS** with letter-spacing (`TECHNOLOGY`, `POLICY`, `OPERATIONS`).
- Headlines use **Sentence case** with a period when they are full statements ("TPO Group leads in mission critical high-stakes cybersecurity consulting…").
- Service titles use **Title Case** ("Resilience Growth Strategy", "Cloud Security Architecture Services").
- The brand name is always written **TPO.group** in marks, **TPO Group** in running prose.

**Vocabulary signals.** _operational continuity_, _security posture_, _governance_, _framework/standards mapping_, _containment and eradication_, _attack vectors_, _business continuity and disaster recovery_, _mission critical_, _high-stakes_. Use plural Latinate nouns; avoid contractions in formal copy; allow them in conversational sales copy.

**Things never to do.**
- ❌ No emoji. Anywhere.
- ❌ No exclamation marks.
- ❌ No internet/slang voice ("Let's dive in", "Game-changer", "Supercharge").
- ❌ No second-person sales hype ("Get yours today").
- ❌ No fear-mongering. The brand sells **competence**, not panic.

**Examples (from the live site).**
- Hero, headline: _"TPO Group leads in mission critical high-stakes cybersecurity consulting through strategic experience and technical prowess."_
- Hero, subhead: _"Our custom solutions and incident response targeted training ensure operational continuity and security amid evolving cyber threats."_
- Pillar copy (POLICY): _"360-degree security strategy creation spanning program design, policy development, governance structure, framework/standards mapping, and metrics that deliver a singular goal: assuring clients' operational efficiency and business growth."_

Sentences run long. They stack qualifiers. They commit. Don't sand that down.

---

## 4. Visual Foundations

### 4.1 Palette
Two greens carry the brand:

| Token | Hex | Used for |
|---|---|---|
| `--tpo-forest-800` | `#06371F` | "TPO" letterforms; primary headings; dark hero backgrounds |
| `--tpo-emerald-600` | `#0E8E54` | ".group" letterforms; accent links; positive states |

A **bars-motif spectrum** in `--tpo-bar-1 … --tpo-bar-9` runs deep green → emerald → teal → steel blue. Used **only** when the literal vertical-bars artwork appears — never as a section background gradient.

Neutrals are warm-cool **graphite** (`--tpo-ink-*`) against `--tpo-paper` white and a barely-warm `--tpo-cream` off-white. No pure black: text bottoms out at `#0B0F0D`.

### 4.2 Typography

A deliberate **serif + sans pairing**: editorial gravitas in display, technical neutrality in body. The TPO wordmark itself stays geometric sans (it's the logo art) — the serif/sans contrast lives between **logo** and **content**, which is the classic editorial move and reads "policy paper / whitepaper," not "SaaS landing."

- **Display & headings → Newsreader** (Production Type, Google Fonts).
  Transitional editorial serif with optical-size axis. Used at weight `600` for most headlines; pulled up to weight `500 italic` for emphasis runs (mission-critical, Safer Future). Variable `opsz` axis is set per role — `opsz 60–72` for the hero, `opsz 32–48` for H2/H3.
- **Body, UI, all caps labels → Hanken Grotesk** (Hanken Design Co., Google Fonts).
  Humanist grotesque with Söhne-family DNA. Body at `400 / 16-18px`, UI at `600`, the three **PILLAR** labels at `800` + caps + `+0.08em` tracking.
- **Mono → JetBrains Mono.** Reserved for code, IPs/CVEs/hashes, and the contact phone number.
- **Italics:** allowed in Newsreader (editorial emphasis on one short phrase per headline). Never in Hanken.
- **No underlines** outside link hover.
- **Tracking:** display `-0.02em`, body `0`, eyebrow/caps `+0.12em`, pillar `+0.08em`.

### 4.3 Backgrounds
- **Default:** flat `--tpo-paper` white.
- **Section variety:** `--tpo-ink-50` (cool warm gray) or `--tpo-emerald-50` (faintest mint). Never a CSS gradient as section fill.
- **Hero option A — white:** big sans-serif type, no imagery, single emerald accent rule.
- **Hero option B — dark forest:** `--bg-dark` (`#042B1B`) with light type and the bars motif at low opacity bottom-right.
- **Imagery:** dim, atmospheric. Server-room blacks, network-cable greens, satellite/topographic monochrome. **Cool, never warm. Never grainy. Never illustrated.** Treated images sit at ~70% brightness with a `--tpo-forest-900` multiply at 40% so type stays legible.

### 4.4 The Bars Motif
The only ornamental device in the system. Twelve vertical rounded-cap rules of varying heights, recoloring along the green→teal→blue spectrum. Used:
- as a quiet footer ornament behind the address line,
- in slide masters as a left-edge title band,
- never as a 50%+ canvas fill, never animated as a "loading" bar, never as a chart axis.

### 4.5 Spacing & Layout
4-pt baseline grid. The system rounds to `8 / 16 / 24 / 48 / 96` for section rhythm. Max content width 1280px; long-form copy column 720px. Fixed elements: header (sticky, 80px tall, white with bottom border on scroll); footer is static.

### 4.6 Radii
Corners are mostly **square** (`--radius-0`). Buttons and inputs use a 2-4px hairline radius. **No 12px+ pill cards**, **no fully rounded "soft" containers**. The single exception: `--radius-pill` for status chips and the small "Send" form pill.

### 4.7 Borders
1-px hairlines at `rgba(11,15,13,0.10)` for separating sections; `0.18` for cards. On dark: `rgba(255,255,255,0.14)`. Borders are preferred over shadows for separation.

### 4.8 Shadows / Elevation
Used sparingly. `--shadow-sm` for hovered cards, `--shadow-md` for menus, `--shadow-lg` for modal-class surfaces. Never on the hero. Never colored shadows except the deep-green `--shadow-xl` reserved for the rare image lift on a marketing module.

### 4.9 Cards
Default = white surface with `--border-2` hairline, square corners, **no shadow at rest**. On hover: `--shadow-sm` and a 1-px shift of the left border to `--tpo-emerald-600`. That is the only "ornamental" hover state in the system.

### 4.10 Animation
- **Durations:** 120ms (fast micro-feedback), 200ms (default), 320ms (pageful transitions).
- **Easing:** `cubic-bezier(0.2,0.6,0.2,1)` standard; `cubic-bezier(0.16,1,0.3,1)` for emphasis (entrances).
- **Style:** fade + 4-8px translate. **No bounces, springs, scale > 1.04, or marketing parallax.** The brand is calm.

### 4.11 Hover / Press States
- **Link / nav:** color shifts `--tpo-ink-900` → `--tpo-emerald-600`. Underline appears with a 200ms reveal from left.
- **Button primary:** background `--tpo-forest-800` → `--tpo-emerald-600` on hover; press = darken to `--tpo-forest-900`. No scale.
- **Button secondary (outline):** border + label adopt emerald on hover; background stays white.
- **Card:** see § 4.9.
- **Press:** color darken only. **Never** shrink-scale a button.

### 4.12 Transparency & Blur
Rarely. The only sanctioned blur is the sticky header switching to `backdrop-filter: blur(12px); background: rgba(255,255,255,0.78)` once the page is scrolled. Imagery uses opacity, not blur.

### 4.13 Iconography
See § ICONOGRAPHY below.

---

## 5. Iconography

The live tpo.group site uses a small, line-style icon set (sized ~36-48px) above each service tile. None of the source SVGs were shareable to us; we substitute **Lucide** (CDN, MIT licensed, 1.5-px stroke, rounded line caps) as the closest visual match — same hairline stroke weight, square-ish geometry, professional feel. **⚠️ This is a substitution. See § Caveats.**

**Rules.**
- **System:** Lucide line icons, stroke `1.5`, line caps `round`, line joins `round`.
- **Sizing:** 20px in dense UI, 24px standard, 36-44px featured (e.g., above a service tile).
- **Color:** inherits `currentColor` — typically `--tpo-forest-800` on light, `--fg-on-dark` on dark, `--tpo-emerald-600` for accent/active.
- **No fills.** No duotone. No emoji. No Unicode glyphs as iconography.
- **No invented icons.** If Lucide doesn't have it, fall back to a labeled chip.

CDN:
```html
<script src="https://unpkg.com/lucide@latest/dist/umd/lucide.min.js"></script>
<i data-lucide="shield-check"></i>
```

---

## 6. Index — what's in this folder

```
README.md                    ← you are here
SKILL.md                     ← cross-compat invocation card for Claude Code
colors_and_type.css          ← CSS custom properties + semantic type classes

fonts/                       ← self-hosted .woff2 files (latin subset)
  fonts.css                    Newsreader · Hanken Grotesk · JetBrains Mono
  *.woff2

assets/
  logos/
    tpo-logo.png             ← primary logotype, light bg
    tpo-logo.jpg
    tpo-logo-dark-bg.png     ← logotype + bars, dark bg
    tpo-logo-tagline.png     ← logotype + "TECHNOLOGY.POLICY.OPERATIONS"

preview/                     ← design-system tab cards (registered as assets)

ui_kits/
  website/
    README.md                ← what's covered, what isn't
    index.html               ← interactive recreation of tpo.group
    Header.jsx, Hero.jsx, Pillars.jsx, Services.jsx, Contact.jsx,
    Footer.jsx, Bars.jsx, Button.jsx, etc.

slides/                      ← (none — no decks were provided)
```

---

## 7. Caveats — please review

1. **Typefaces are locked in.** We chose a deliberate pairing — **Newsreader** (serif display, Production Type) + **Hanken Grotesk** (sans body, Hanken Design Co.) — that gives the brand editorial / policy-paper authority. Both are self-hosted under `fonts/` (latin subset, `.woff2`, SIL OFL — see `fonts/fonts.css`). No CDN, no Google Fonts call at runtime. To swap in a licensed brand serif later, replace the `.woff2` files in `fonts/` and update `--font-display` / `--font-sans` in `colors_and_type.css`.
2. **Icons are a substitution.** Service-tile icons on the live site are bespoke (or Wix-stock); we ship the system pinned to **Lucide**. **Action:** if there's a master icon SVG kit, drop it into `assets/icons/` and we'll repoint.
3. **No imagery shipped.** The brand currently uses a single hero background (`tpo_group_background.jpg` per Wix's CDN). We avoided redistributing it; the UI kit uses the bars motif and dark-green flats instead. **Action:** if you have approved hero photography, drop one or two into `assets/imagery/`.
4. **No app surface.** This system covers marketing + collateral only. If TPO Group ever builds a client portal, dashboard, or report viewer, that's a second UI kit on top of these foundations.

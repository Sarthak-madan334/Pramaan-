# 08. Design System: Cosmic Glass

## Where this direction comes from

The reference is the user-provided short launch video and the [GPT-6 Astra launch page](https://openai.com/index/gpt-6-astra/). Its useful qualities are scale, restraint, pacing and the move from atmosphere into concrete examples. Reading frames from the video, the look is:

- a **near-black navy void** with soft blue nebula clouds and a faint dot grid
- a **cloud of tiny white star particles** that gathers into the shape of the title
- **large, light-weight, tightly set grotesque type**: line one white, line two in a pale periwinkle gradient, ending in a full stop
- **small monospace eyebrow labels** in capitals with wide tracking ("INTRODUCING", "A SPACE FOR POSSIBILITY")
- **dark glass panels**: deep navy fill, hairline light-blue border, large radius, a faint top-edge glow
- a **prompt box** that types text, with a small model selector underneath
- **speed-line streaks** radiating outward as the camera "zooms"
- a **3D-tilted glass card** showing a mini page, with a light **pill button** and a tiny orbit-and-star icon
- slow, confident motion; no bouncing, no clutter

Pramaan takes the **mood and craft level**, not the identity. See [What we do not copy](#what-we-do-not-copy).

## Pramaan's twist: the Nakshatra idea

*Nakshatra* (नक्षत्र) are the star groups of Indian astronomy. Pramaan's visual story:

> **Every claim on your resume is a star. Proof makes it brighter. Your profile is the constellation.**

- Unproven claims are dim, small stars. As evidence is added they brighten and gain a ring.
- Proof levels map to brightness and shape: Listed (faint dot), Used (small star), Demonstrated (bright star), Quantified (bright star with a **warm saffron core**).
- The saffron core is the single warm accent in the whole palette: it means "proven". That keeps the UI calm and gives it an Indian signature without costume.
- The hero animation shows noisy stars (a weak bullet) condensing into a clean constellation (a verified bullet).

## Design principles

1. **Cinematic but quiet.** One strong idea per screen; lots of dark space.
2. **Readable always.** Atmosphere never sits under body text at full strength.
3. **Mobile first, cheap-phone safe.** Every effect has a lighter fallback ([performance tiers](#performance-tiers)).
4. **Accessible by default.** Motion, transparency and contrast preferences are honoured.
5. **Meaningful, not decorative.** Stars represent claims; motion explains the product.
6. **Original.** Inspired by the mood only.

## Colour tokens

```css
:root {
  /* Void */
  --void-0: #03060f;          /* deepest background */
  --void-1: #060c1c;          /* page background */
  --void-2: #0a1428;          /* panel fill base */
  --nebula-1: #0f2a55;        /* soft cloud */
  --nebula-2: #1b3f7a;        /* brighter cloud, used sparingly */

  /* Text */
  --ink-1: #f2f5fc;           /* primary */
  --ink-2: #aab6d3;           /* secondary */
  --ink-3: #7f8caa;           /* tertiary: large text or non-essential only */
  --accent-1: #b9ccf5;        /* periwinkle highlight */
  --accent-2: #86a6ea;        /* periwinkle deeper */

  /* Meaning */
  --proof-0: #6b7794;         /* Listed */
  --proof-1: #e0b04a;         /* Used */
  --proof-2: #9db8f5;         /* Demonstrated */
  --proof-3: #ffb454;         /* Quantified: saffron core, the only warm accent */
  --ok: #55d6b8;
  --risk: #ff7f8f;
  --warn: #ffd166;

  /* Glass */
  --glass-fill: rgba(10, 20, 40, 0.62);
  --glass-fill-strong: rgba(10, 20, 40, 0.82);
  --glass-border: rgba(160, 190, 255, 0.18);
  --glass-edge-glow: rgba(190, 215, 255, 0.35);   /* top edge highlight */
  --glass-shadow: 0 24px 60px rgba(0, 0, 0, 0.5);
  --glass-blur: 14px;

  /* Shape and space */
  --radius-sm: 10px; --radius-md: 16px; --radius-lg: 22px; --radius-pill: 999px;
  --space-1: 4px; --space-2: 8px; --space-3: 12px; --space-4: 16px;
  --space-5: 24px; --space-6: 32px; --space-7: 48px; --space-8: 72px; --space-9: 112px;
}
```

**Themes.** Dark "void" is the primary theme and the brand. A light theme exists for the dashboard only (paper-white background, navy ink, same proof colours adjusted for contrast); the landing page ships dark only. Verify every text/background pair on the **rendered** background, including brightest particle behind text.

## Background layers (back to front)

1. **Void:** flat `--void-1` with a vertical gradient to `--void-0`.
2. **Nebula:** two to three large radial gradients in `--nebula-1/2` at low opacity, slightly offset. Pre-render as one optimised image (AVIF/WebP) or CSS gradients; never as live blurred elements.
3. **Dot grid:** a very faint repeating dot pattern (CSS background), opacity under 6 percent.
4. **Stars (static):** a pre-rendered sprite layer or CSS radial dots, slow parallax on desktop only.
5. **Particles (animated, hero only):** canvas layer, see [Hero sequence](#hero-sequence).
6. **Scrim:** a soft gradient behind text blocks to guarantee contrast.

## Typography

| Role | Direction | Notes |
|---|---|---|
| Display | Clean grotesque, **light to regular weight**, tight tracking (about -0.03em), very large | Matches the launch look; avoid bold headlines |
| Body / UI | Same family or a neutral sans | 16px base, line-height about 1.6 |
| Eyebrow / labels | **Monospace, uppercase, wide tracking** (about 0.14em), 11 to 12px | The "INTRODUCING"-style labels |
| Devanagari | Noto Sans Devanagari or similar | For Hindi and Hinglish; same weights where possible |

Use open-licence fonts (self-hosted, subset, `font-display: swap`). Do not use or imitate a proprietary brand font.

**Headline pattern:** two lines. Line one `--ink-1`; line two filled with a periwinkle gradient (`--accent-1` to `--accent-2`) via `background-clip: text`, ending in a full stop. Example: "Har line ka" / "pramaan."

```css
.display { font-weight: 400; letter-spacing: -0.03em; line-height: 1.02;
           font-size: clamp(2.6rem, 8vw, 6.5rem); }
.display .accent {
  background: linear-gradient(180deg, var(--accent-1), var(--accent-2));
  -webkit-background-clip: text; background-clip: text; color: transparent;
}
.eyebrow { font-family: var(--font-mono); text-transform: uppercase;
           letter-spacing: 0.14em; font-size: 0.72rem; color: var(--accent-2); }
```

## Glass panel

```css
.glass {
  position: relative;
  background: var(--glass-fill);
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-lg);
  box-shadow: var(--glass-shadow);
  -webkit-backdrop-filter: blur(var(--glass-blur)) saturate(120%);
  backdrop-filter: blur(var(--glass-blur)) saturate(120%);
}
.glass::before {            /* faint top-edge glow */
  content: ""; position: absolute; inset: 0 0 auto 0; height: 1px;
  background: linear-gradient(90deg, transparent, var(--glass-edge-glow), transparent);
}
@supports not ((backdrop-filter: blur(1px)) or (-webkit-backdrop-filter: blur(1px))) {
  .glass { background: var(--glass-fill-strong); }
}
@media (prefers-reduced-transparency: reduce) {
  .glass { background: var(--void-2); backdrop-filter: none; -webkit-backdrop-filter: none; }
}
```

Panels are **dark and fairly opaque** (as in the reference), which also protects text contrast and reduces blur cost.

## Core components

- **Prompt box:** a wide glass panel with a typing line, a small "+" and a model-style selector row beneath (for Pramaan: "+ attach resume" and "Fact Ledger on"). Used in the hero demo and later as the Evidence Intake input.
- **Pill button:** primary is a light pill (`#e6ebf8` background, dark text), generous padding, subtle inner highlight; secondary is a glass pill with light text.
- **Tilted card:** a glass card with `perspective` and a slight `rotateY/rotateX` to show a mini page or screen; used once or twice per page, never stacked.
- **Orbit icon:** tiny SVG of a star with an elliptical ring; used as brand mark accompaniment and loader.
- **Proof badge:** star glyph + text label + colour for each level (never colour alone).
- **Claim chip:** a rounded tag with a leading star, used in the Fact Ledger ("you said it", "from your repo", "needs your input").
- **Eyebrow label, tabs, accordion, toast, sheet, skeleton, diff view, stepper, dropzone, progress** as in the minimal set, restyled with the tokens above.

## Layout and responsiveness

- Mobile-first CSS; breakpoints 480, 768, 1024, 1280.
- Hero copy is **left-aligned and first in the reading order**. On desktop, the visual may sit beside or partly below it; on mobile, the compact visual follows the message. The opening needs ample negative space, but the headline, explanation and action must remain readable without animation.
- Container max-width about 1200px; generous vertical rhythm (`--space-8` to `--space-9` between sections).
- Respect safe-area insets; no horizontal scroll; tap targets at least 44px.
- Headline scales with `clamp()`; test at 320px and with large system fonts.

## Motion

| Element | Behaviour | Duration |
|---|---|---|
| Hero particle gather | Particles drift into a small constellation around the title; the actual title remains HTML text and is visible immediately | ~3 s |
| Prompt typing | Characters appear at human pace with a blinking caret | 2 to 4 s |
| Speed lines | Short radial streaks during the "zoom" beat | ~0.8 s |
| Card tilt | Glass card eases into perspective | ~0.9 s |
| Section reveal | Fade and 12px rise on enter | 250 to 400 ms |
| Star brighten | Scale and glow when proof level rises | 400 ms |

Rules: ease-out curves; animate **transform and opacity only**; never animate blur; no scroll-jacking (native scrolling always); everything stops or simplifies under `prefers-reduced-motion`.

## Hero sequence

A roughly 8 to 12 second scripted sequence plays **once**, then settles into a static state. It uses a quiet build-up and reveal while telling Pramaan's own story:

1. **Opening:** the headline, subhead and action are present in the DOM from first paint; nebula and a few stars gently build around them.
2. **Question:** a weak illustrative bullet appears in a **prompt box**. Two focused questions ask what the student personally built and what evidence they have.
3. **Proof:** answers appear as source-tagged Fact Ledger chips. A rewritten bullet uses **only** those shown facts. If the example has no supplied metric, its highest possible level is Demonstrated; no saffron Quantified core appears.
4. **Settle:** a small constellation and proof badge reinforce the result. The final state remains readable, with skip, pause and replay controls as appropriate. The CTA is available throughout.

The example is **illustrative and labelled as such** ("Illustrative example. Not a real user."). It is built with real HTML/CSS and a small state machine, so text is crisp, selectable and accessible, not a pre-rendered video. Its facts, output and proof badge must agree exactly.

## Performance tiers

Effects are chosen by capability and preference at load:

| Tier | Who | What they get |
|---|---|---|
| A: Full | Capable desktop/laptop, no reduced-motion | WebGL or canvas particles (about 2 to 4K), speed lines, parallax, tilt card |
| B: Lite | Typical phones | Canvas 2D particles (about 400 to 800), no speed lines, shorter sequence |
| C: Static | Low-end devices, Save-Data, reduced motion, battery saver, WebGL failure | Pre-rendered poster of nebula and stars (AVIF/WebP), fade-only reveals, final hero state shown immediately |

Rules:

1. Load the particle code **after** first paint (dynamic import); LCP is the headline text, not the canvas.
2. Cap device pixel ratio (about 1.5 on mobile, 2 on desktop); cap particle count by tier.
3. **Pause** animation when the tab is hidden or the canvas is off-screen (IntersectionObserver, `visibilitychange`).
4. Prefer a tiny custom WebGL points shader or Canvas 2D over large 3D libraries. Particle chunk budget: about 50 KB gzipped or less; first-load JS about 150 KB gzipped or less ([09](09-LANDING-PAGE.md)).
5. At most two overlapping `backdrop-filter` layers; blur 10 to 14px; never animate blur.
6. Auto-downgrade tier if measured frame time stays above about 24 ms for a second.
7. Test on an older mid-range Android phone on throttled 4G; this is the real target device.
8. Offer a quiet "Reduce motion" toggle in the footer that sets Tier C.

## Accessibility

- Contrast: 4.5:1 body, 3:1 large text and UI boundaries, checked against the brightest background pixel behind the element.
- Decorative canvases are `aria-hidden`; the demo has a **text alternative** and a "skip animation" control.
- Keyboard: skip link, visible focus rings (periwinkle, 2px), no keyboard traps in the demo.
- Do not flash; no strobe effects; speed lines never exceed three streaks per 100 ms.
- `prefers-reduced-motion` and `prefers-reduced-transparency` supported.
- Proof levels always use icon + text + colour.
- Pause/stop control for any animation lasting over 5 seconds, as required for accessibility.

## Copy voice

Short, confident, specific. Lines like "Every number checked against what you told us." Light Hinglish touches (the tagline) are welcome; core UI stays in clear English with a Hinglish toggle later. No hype, no guarantees.

## What we do not copy

- No logos, wordmarks, product names ("GPT", "Astra", "Codex") or copy from the reference.
- No screenshots, video frames or assets from it; the uploaded video is **reference only** and must not be redistributed or embedded.
- No imitation of a proprietary typeface.
- No wording that suggests affiliation with any other company.
- No benchmark-style charts, claims of model superiority or invented customer proof to fill space.
- Layout and animation are redesigned around Pramaan's own story (claims as stars), not recreated frame by frame. Use the reference's editorial pacing, not its section order.

## Implementation notes

- Next.js + TypeScript + Tailwind with the tokens as CSS variables; Radix primitives for accessible widgets.
- Hero demo: a small state machine (steps, timers, skip) rendering real DOM; particles in a separate lazily loaded module with a clean `destroy()`.
- Build a **component gallery** page with light/dark, tiers A/B/C and reduced-motion states.
- Visual regression tests for key components; a Lighthouse CI budget for performance and accessibility.

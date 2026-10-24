# 09. Landing Page (Phase 1)

## Goals

1. Explain Pramaan in under 30 seconds, through a short, cinematic, **honest** demo.
2. Feel as polished as a modern AI launch page, while staying fast on a mid-range phone over 4G.
3. Build trust: no invented claims, visible privacy promise, no dark patterns.
4. Collect waitlist signups and learn what students want.

Visual language comes from [08](08-DESIGN-SYSTEM.md): dark void, star particles, nebula, glass panels, monospace eyebrows, two-line gradient headline. Story: **every claim is a star; proof makes it shine.** The requested reference is the [GPT-6 Astra launch page](https://openai.com/index/gpt-6-astra/) and its short launch video. Use its sense of scale, pacing and editorial confidence as inspiration, while making every visual, line of copy and interaction original to Pramaan.

## Reference translation: the feeling, not the page

The reference feels like an event: an almost empty opening screen, a large headline, carefully timed motion, then a long-form story that alternates between quiet explanation and vivid demonstrations. Pramaan should borrow that **rhythm**. It should not reproduce the reference's layout section by section, brand marks, footage, typography, wording, benchmark charts, or product imagery.

| Reference quality | Pramaan interpretation |
|---|---|
| Cinematic opening and generous negative space | A near-black opening with one oversized idea: **Har line ka pramaan.** A small constellation forms from scattered claims. |
| Product capability shown rather than merely claimed | A selectable, labelled example follows one vague resume bullet through questions, ledger facts and a supported rewrite. |
| Alternating editorial text and visual evidence | Large statement sections alternate with intimate, readable product scenes. Avoid a wall of identical feature cards. |
| Data or examples that substantiate claims | Show *how* evidence levels and validator checks work. Do not invent users, metrics, model results or testimonials. |
| Long-form launch narrative | Keep the story focused enough for a student on a phone: problem → proof → decision → trust → next step. |

The uploaded video is a visual reference only. Do not ship it, trace its frames, or use assets extracted from it. The constellation, resume claim, Fact Ledger and saffron proof star give this page its own identity.

## Audience

CS/IT students and freshers in India, usually on a phone, anxious, sceptical of "AI resume" tools and used to being upsold.

## Page map (scroll story)

| # | Section | What it shows | Visual |
|---|---|---|---|
| 1 | Header | Orbit-star wordmark; How it works, Product, Our promise, FAQ; one early-access action | Minimal and nearly transparent over the opening; a solid dark state after scroll. Mobile navigation works without relying on a custom gesture. |
| 2 | **Opening / hero** | Eyebrow "PRAMAAN · EARLY ACCESS"; headline "Har line ka / pramaan." and a plain-English explanation; one clear action | The headline owns the first view. Stars gather in the surrounding space. A small proof motif or demo teaser may overlap the lower edge, but must not compete with the headline. |
| 3 | **One claim, examined** | An illustrative weak bullet, the questions it invites, facts supplied by the user, and a grounded rewrite | The signature visual sequence. Real selectable text, source tags and a visible "illustrative example" label. On mobile it becomes a vertical story, not a shrunken desktop card. |
| 4 | The problem and method | Why generic rewrites, unexplained scores and blind applications fail; the three beats **Show → Prove → Decide** | Editorial type and one concrete visual per beat. Alternate spacious text blocks with demonstrations instead of repeating three-card rows. |
| 5 | Constellation | Claims as stars, brightness as proof depth; a selected claim reveals what is known and what is missing | Original interactive proof map with an equally complete text/list view. Use saffron only for genuinely quantified, user-supplied facts. |
| 6 | Product scenes | Fact Ledger, Project Truth Check, Apply-or-Skip, tailored resume; Fire Drill clearly marked later | Each scene answers one user question and includes a realistic example or source trace. Do not use empty decorative dashboard screenshots. |
| 7 | Trust and limits | Validator path, user approval, privacy controls and honest limits | The quietest section: large clear statements, a small source-to-claim diagram, no performance hype. |
| 8 | FAQ and final action | Short answers, then a decisive closing line and waitlist action | One closing constellation moment; footer carries legal, privacy, contact and motion controls once those destinations exist. |

### Layout rhythm

1. **Opening:** near-black, almost empty, full-bleed atmosphere; headline and action visible without waiting for motion.
2. **Demonstration:** more structured glass surfaces appear only when showing an actual product mechanism.
3. **Explanation:** alternate wide headline sections with narrower reading columns; vary scale and alignment while preserving a clear reading order.
4. **Closing:** return to negative space and the orbit-star mark. The final action is unmistakable.

At desktop widths, the hero may place the proof visual beside or partially below the left-aligned headline. At phone widths, keep the headline first in reading order and place a compact visual after it. Do not force the visual above the message if that pushes the value proposition below the first screen. Keep section heights content-led rather than fixing every act to `100vh`.

## Hero sequence (plays once, ~8–12 s, skippable)

Matches [08](08-DESIGN-SYSTEM.md#hero-sequence).

1. **Gather:** a sparse field of claims resolves into a small constellation around the already-readable headline. The motion adds meaning; it does not reveal essential copy.
2. **Question:** a weak example bullet appears, followed by two focused questions. Its problem is apparent even if the sequence is paused.
3. **Evidence:** example answers enter the Fact Ledger with their source labels. Rewrite the bullet using only those displayed facts. If no measured result was supplied, **do not show a Quantified badge, saffron core, or invented number**.
4. **Settle:** the example remains visible in its final state; the page action stays available throughout, rather than arriving only at the end.

Behaviour rules:

- Always shows a **"Skip demo"** control; skipping jumps to the settled state. Provide pause/replay if movement continues longer than five seconds.
- If the user scrolls early, the sequence jumps to the settled state (no scroll-jacking).
- Reduced motion, low-end, Save-Data or battery saver: show the settled state immediately (Tier C).
- A caption under the demo: **"Illustrative example. Not a real user."** Never show invented testimonials, user counts or results. The visible Fact Ledger must contain every fact used by the rewrite.
- The whole demo has a plain-text equivalent for screen readers and for no-JS visitors.

## Copy

### Hero
- Eyebrow: `PRAMAAN · EARLY ACCESS`
- Headline: **Har line ka** / **pramaan.**
- Subhead: "An AI career copilot for Indian students. It never invents facts, tells you which jobs are worth your time, and prepares you for the questions your resume invites."
- Button once signup is live: "Join the waitlist". Under it: "Free to join. No spam. Unsubscribe anytime."
- Before the secure waitlist and confirmation email are working, use a non-collecting status such as "Waitlist opening soon". Do not render a form that only simulates success or saves addresses locally.

### Alternative headlines to test
- "Your resume, with proof behind every line."
- "Stop guessing. Start proving."
- "Every claim, a star. Every star, proven."

### Section copy direction
- Problem: honest and specific ("AI rewrites that sound like everyone else", "A score with no explanation", "Hundreds of applications, almost no replies").
- Promises: plain statements, not slogans ("We check every number against what you told us").
- Tone: confident, warm, no hype. Light Hinglish in small doses (tagline, a few labels); optional Hinglish toggle later.
- Social proof only when real. Until then, the promises section does the trust work.
- Do not mention or compare to any other company's product on the page.
- When a feature is still planned, write "we're building" or "planned" instead of presenting it as an available service. A mock product scene must carry a visible "Concept preview" or "Illustrative example" label.

### FAQ
1. Will it write my resume for me? (It builds from facts you give it and shows every change.)
2. Does it make things up? (Every number and tool is checked against what you told us.)
3. Is it free? (Core fixes are free; paid options, if any, will never hide fixes.)
4. What happens to my resume? (Redaction, encryption, deletion; link to notice.)
5. Can it guarantee interviews or beat an ATS? (No tool can; we show what is real.)
6. Which roles does it support? (Starting with software, data and ML freshers.)
7. Do you train on my resume? (Only with explicit opt-in.)
8. Is there a Hindi/Hinglish option? (Planned.)

## Waitlist form

**Release condition:** expose the signup form and "Join the waitlist" CTA only after the server-side handler, confirmation email, unsubscribe path, privacy notice and anti-abuse controls below work end to end. Until then, the page is a product preview with no email collection. This avoids collecting personal data through an unfinished flow.

Fields: **email** (required); optional: college year, target role, "what frustrates you most about resumes?" (short text).

Security and anti-abuse:

- Client and server validation; normalise email; strict length limits.
- **Double opt-in** with a signed, expiring confirmation link.
- Rate limits per IP and per email; honeypot field plus a privacy-friendly bot challenge.
- JSON-only endpoint with strict CORS (or CSRF protection if cookies are used).
- Identical response whether or not the email already exists.
- Store only what is needed; no uploads on the landing page.
- Consent text beside the button; unsubscribe link in every email, honoured immediately.
- Escape all free text everywhere it is shown (including admin views).

## Technical approach

- **Next.js** static generation, TypeScript, Tailwind with design tokens; Radix primitives for menu, tabs, accordion, dialog.
- **Progressive enhancement:** all content and the form work without JavaScript; the demo and particles enhance.
- **Hero demo:** small state machine (steps, timers, skip), real DOM text, CSS transforms.
- **Particles:** separate lazily loaded module (custom WebGL points or Canvas 2D), capability tiers A/B/C, pause off-screen, auto-downgrade on low frame rate.
- **Constellation section:** SVG or canvas with an accessible list alternative.
- **Images:** nebula and stars pre-rendered (AVIF/WebP); mini-screens built from HTML/CSS or SVG; no heavy video. If a looping video poster is used for Tier C, keep it under about 1 MB (WebM plus MP4), muted, no autoplay on Save-Data.
- **Fonts:** self-hosted, subset; display, body, mono, Devanagari.
- **Analytics:** none, or cookieless and self-hosted; no third-party trackers or chat widgets.
- **Waitlist handler:** small serverless/API route, separate from the future app's auth surface.

## Performance targets (mid-range phone, throttled 4G)

| Metric | Target |
|---|---|
| Largest Contentful Paint | under 2.5 s (the headline text, not the canvas) |
| Interaction to Next Paint | under 200 ms |
| Cumulative Layout Shift | under 0.1 |
| First-load JavaScript | about 150 KB gzipped or less (particles load afterwards, about 50 KB or less) |
| Total page weight (first view) | about 1 MB or less excluding deferred particle module |
| Lighthouse (mobile) | Performance, Accessibility, Best Practices, SEO all at or above 90 |
| Frame rate (hero, Tier B) | steady 30 fps or better; auto-downgrade otherwise |

## Accessibility

- Contrast verified against the brightest background pixel behind each text block; text sits on a scrim.
- Skip link, visible focus, full keyboard use; the demo is skippable and pausable.
- Decorative canvases `aria-hidden`; meaningful visuals have text alternatives.
- No flashing; respects `prefers-reduced-motion` and `prefers-reduced-transparency`.
- Works at 320px, 200 percent zoom and large system fonts.
- The headline and primary action are present before JavaScript and remain visible at every animation stage; animation must not be the only way to learn the product story.

## SEO and sharing

- Title, description, canonical, Open Graph and Twitter cards with a clean preview image (the nebula and a single constellation, no third-party assets).
- Semantic headings, sitemap, robots, simple organisation structured data.
- Target searches: resume review for freshers, ATS-friendly resume India, resume for CS freshers.
- `lang` attributes for Hindi snippets.

## Security headers

- `Strict-Transport-Security` with long max-age.
- `Content-Security-Policy`: own origin for scripts, styles, fonts, images; explicit nonce/hash for any inline script; no remote shaders or third-party scripts; if a web worker is used for particles, allow it explicitly (`worker-src 'self'`).
- `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`, `Permissions-Policy` disabling unused features, `frame-ancestors 'none'`.
- Subresource integrity for any third-party script (avoid them).
- Pinned, audited dependencies; automated vulnerability alerts.

## Legal and trust pages

- Plain-language privacy notice, terms with a no-guarantee statement, contact and grievance contact ([12](12-PRIVACY-AND-COMPLIANCE.md)), `security.txt`.
- Cookie banner only if non-essential cookies exist; prefer none.
- Footer line: "Pramaan is independent and not affiliated with any AI lab or employer."

## Build plan inside Phase 1

| Step | Work | Output |
|---|---|---|
| 1A | Wireframes (mobile first) and copy | Approved page map and text |
| 1B | Design tokens, component gallery, background layers | Cosmic-glass base |
| 1C | Static page with all sections, no animation | Complete accessible page |
| 1D | Hero demo state machine and particle module with tiers | Motion layer |
| 1E | Waitlist, double opt-in, emails, anti-abuse | Working signups |
| 1F | Performance and accessibility pass on real devices | Passing budgets |
| 1G | Launch: headers, monitoring, share in student communities | Live site |

Ship **1C before 1D**: a good static page is the product; the animation is an enhancement.

## Success criteria

- Budgets above met on a real low-to-mid Android phone.
- At least 100 waitlist signups or 20 completed student interviews (set the number before launch).
- Time on page and scroll to FAQ show that the demo is understood; if not, simplify the demo.

## Launch checklist

- [ ] Name, domain and trademark checks done
- [ ] Contrast, keyboard and reduced-motion checks pass; screen-reader smoke test
- [ ] Tiers A, B and C tested; auto-downgrade verified
- [ ] Tested on an older Android phone on throttled 4G
- [ ] Security headers verified; dependency audit clean
- [ ] Double opt-in and unsubscribe tested end to end
- [ ] Privacy notice, terms and grievance contact published
- [ ] No third-party assets or copied content from any reference
- [ ] Every example rewrite uses only its visible ledger facts; proof badges match the actual evidence level
- [ ] Planned features, concept previews and live functionality are clearly distinguished in page copy
- [ ] 404 and error pages designed in the same style
- [ ] Uptime monitoring and rollback plan in place

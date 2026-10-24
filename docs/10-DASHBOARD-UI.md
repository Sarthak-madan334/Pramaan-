# 10. Dashboard UI (Phase 3)

The dashboard is where students do the work. It shares the **cosmic-glass** identity of the landing page ([08](08-DESIGN-SYSTEM.md)) but is **calmer and more functional**: the same void, glass panels and star language, with far less motion and more opaque surfaces so long work sessions stay readable and fast. Backend and auth are built first (Phase 3A) so these screens run on real data.

## Principles

1. **One clear next step** on every screen.
2. **Show the evidence.** Every finding links to the resume line or ledger fact behind it.
3. **Calm by default.** Static star field, no particle animation, motion only to explain change.
4. **Mobile equals desktop in capability.** Nothing important is desktop-only.
5. **Never hide fixes.** If an issue is shown, so is the fix.
6. **Honest tone.** "Not yet proven", never "bad" or "weak".

## Visual rules for the app

- Background: `--void-1` with a **static** faint nebula and dot grid (CSS/image); no canvas particles in the app.
- Surfaces: mostly **opaque dark panels** (`--glass-fill-strong`); true blur only on the top bar, bottom tab bar and sheets.
- Accent: periwinkle for actions and focus; saffron only for "Quantified/proven" moments.
- The **constellation** is the signature visual, used as an optional view, not the only one.
- Light theme available for long reading sessions; proof colours re-tuned for contrast.
- Respect reduced-motion and reduced-transparency; a "Calm mode" in Settings removes all non-essential effects.

## Information architecture

| Area | Purpose |
|---|---|
| Home | Next best action, recent activity, profile strength overview (constellation preview) |
| Resume | Upload, versions, X-Ray, Defensibility map |
| Evidence | Evidence Intake and the Fact Ledger |
| Projects | GitHub connection, Project Truth Check, upgrade paths |
| Jobs | Paste/save JDs, Apply-or-Skip verdicts, tailored versions |
| Practice | Interview Fire Drill (Phase 5) |
| Tracker | Applications and outcomes (Phase 5) |
| Settings | Profile, privacy, export/delete, sessions, calm mode, notifications |

### Navigation

- **Mobile:** glass bottom tab bar with four items (Home, Resume, Jobs, More) and one contextual primary action; sheets for secondary actions; safe-area aware.
- **Desktop:** left sidebar (glass) with the orbit-star mark, content area, optional right detail panel.
- Back button or breadcrumb on every nested screen.

## Core screens

### 1. Onboarding and upload
- Short welcome in the prompt-box style: target role and college year.
- Drag-and-drop or tap to upload PDF/DOCX; clear limits; a note that files are scanned and deleted per the retention setting ([11](11-SECURITY.md), [12](12-PRIVACY-AND-COMPLIANCE.md)).
- Progress: uploading, scanning, parsing, done, with plain-language messages.
- Failure states explain what happened and what to try.

### 2. Resume X-Ray
- Original preview beside "what a machine reads"; pass/warn/fail checklist with guidance for each item.
- Note that this is not a simulation of any specific company's ATS.

### 3. Defensibility map
- **Two views, switchable:**
  - **List/text view (default, fully accessible):** resume text with claims highlighted by level.
  - **Constellation view:** each claim a star; brightness and shape show level; saffron core for Quantified; risky claims pulse gently once (not continuously).
- Filter: risky only. Tap a claim or star → side sheet with why this level, what would raise it, "Add evidence" and "Move to Familiar with".

### 4. Evidence Intake
- Prompt-box style input, one question at a time; optional quick-answer chips.
- The **Fact Ledger** builds on the side (desktop) or in a collapsible sheet (mobile) with tags: *you said it*, *from your repo*, *needs your input*.
- Draft bullets show "facts used"; accept, edit or reject; undo available.
- Autosave; resume where you left off.

### 5. Projects
- Connect GitHub (read-only), choose repos.
- Project card: signals found, originality notes, three upgrade steps with hour estimates, "Add to my plan".
- Supportive language only.

### 6. Jobs and triage
- Paste a JD; see extracted requirements.
- Verdict card: **Apply / Stretch / Skip** with reasons and the fastest way to close the main gap; override at any time.
- Actions: create tailored version, save, dismiss. Compare 2 to 3 JDs as stacked cards on mobile.

### 7. Tailored version and diff
- Inline or side-by-side diff; every change expands to the facts behind it.
- Voice-check suggestions as dismissible chips.
- Export DOCX; blocked with a clear list of remaining placeholders if any.

### 8. Settings and privacy
- Export my data; delete everything (confirmation and clear consequences).
- Research-use consent (off by default); retention selector; active sessions and sign-out; connected accounts; email preferences; **Calm mode**.
- Plain-language explanation beside every control.

## States every screen must handle

Loading (skeletons), empty (explain and offer the next step), error (what happened, what to do, retry), slow or offline, partial results, long-running jobs (progress, leave and return).

## Interaction details

- Undo for accept/reject; autosave with a quiet "saved" indicator.
- Confirm destructive actions; make them recoverable where possible.
- Toasts for success; inline messages for errors next to the thing that failed.
- Optional desktop keyboard shortcuts, discoverable.
- Star "brighten" animation (about 400 ms) when a claim's level rises; this is the only celebratory motion.

## Content patterns

- Supportive and specific: "You listed Kubernetes but no project uses it. Add one, or move it to Familiar with."
- Show reasons and sources, not just conclusions.
- Numbers always have units and a source (your answer, your repo).
- Hinglish toggle later; the structure and strings are built for localisation from day one.

## Accessibility and mobile specifics

- Full keyboard and screen-reader support; focus is managed when sheets open and close.
- Constellation view has a complete list equivalent; diffs and highlights have non-colour indicators.
- Large tap targets; primary actions within thumb reach; safe-area aware.
- No hover-only interactions.
- Data-light: no video, lazy-loaded heavy views, works on slow connections.

## Frontend architecture

- Next.js (App Router) + TypeScript; server components for static parts, client components for interactive flows.
- Typed data layer with caching and revalidation; schemas shared with the API ([13](13-API-AND-DATA-MODEL.md)).
- Auth by secure cookie sessions ([11](11-SECURITY.md)); no long-lived tokens in `localStorage`.
- Long jobs via polling or server-sent events with backoff.
- Error boundary per route; error reporting **scrubs resume content**.
- Constellation rendered with SVG (small sets) or canvas (large sets), lazily loaded.
- Tests: component tests, end-to-end first-session flow, accessibility checks and visual regression in CI, performance budget checks.

## Telemetry (privacy-first)

Event analytics without resume or JD content; user can opt out; no third-party ad or tracking pixels.

## Definition of done per screen

- Works at 320px and 1280px, dark and light, calm mode on and off.
- Keyboard and screen-reader pass.
- Loading, empty and error states implemented.
- No resume content in logs or error reports.
- Reviewed against the security checklist in [11](11-SECURITY.md).

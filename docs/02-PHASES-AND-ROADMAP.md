# 02. Phases and Roadmap

Order requested by the project owner: **landing page first, model training second, dashboard UI third.** This plan keeps that order and splits each into sub-phases. One honest adjustment: the dashboard cannot work without an API and authentication, so Phase 3 starts with the backend. Timelines are estimates for a small team (1 to 3 people); adjust after Phase 1.

```
Phase 0  Foundations            week 0-1
Phase 1  Landing page           weeks 1-4    (cinematic hero adds about one week)
Phase 2  Model training         weeks 3-15   (data work starts during Phase 1)
Phase 3  Backend + dashboard    weeks 13-23  (backend starts once a model checkpoint exists)
Phase 4  Beta + hardening       weeks 23-29
Phase 5  Launch + growth        week 29+
```

Phases 1 and 2 overlap on purpose: data collection and labelling are slow and do not need the landing page.

---

## Phase 0: Foundations (week 0 to 1)

**Goal:** remove avoidable risk before writing product code.

- Name decision, trademark/domain/handle checks ([01](01-VISION-AND-PRODUCT.md)).
- Create the monorepo, branch protection, CI, linting, pre-commit secret scanning.
- Set up design tokens and the component gallery skeleton ([08](08-DESIGN-SYSTEM.md)) and the security baseline ([11](11-SECURITY.md)).
- Decide hosting accounts, billing alerts and a budget cap.
- Draft the privacy notice outline ([12](12-PRIVACY-AND-COMPLIANCE.md)).
- Record that the reference video and page are **inspiration only**: no assets, logos or copy are reused ([08](08-DESIGN-SYSTEM.md#what-we-do-not-copy)).

**Exit criteria:** repo builds in CI; secret scanning passes; name decision recorded.

---

## Phase 1: Landing page (weeks 1 to 4)

**Goal:** a fast, cinematic yet honest public site that explains the idea through a short demo and collects waitlist signups to validate demand. Visual direction: **cosmic glass** (void, star particles, nebula, dark glass panels, two-line gradient headline). Spec in [09](09-LANDING-PAGE.md), design in [08](08-DESIGN-SYSTEM.md).

| Sub-phase | Work | Output |
|---|---|---|
| 1A Wireframes and copy | Mobile-first page map, copy, FAQ, promises | Approved content |
| 1B Design base | Tokens, nebula/star layers, glass panel, type scale, component gallery | Cosmic-glass foundation |
| 1C Static build | All sections, responsive, accessible, **no animation yet** | A complete good page |
| 1D Motion layer | Hero demo state machine, particle module with tiers A/B/C, constellation section | Cinematic enhancement |
| 1E Waitlist | Form, double opt-in, emails, anti-abuse, unsubscribe | Working signups |
| 1F Device pass | Performance, accessibility, reduced-motion, real low-end Android on 4G | Passing budgets |
| 1G Launch | Security headers, monitoring, share in student communities | Live site |

Rule: **ship 1C before 1D.** A strong static page is the product; animation is an enhancement that must degrade gracefully.

**Exit criteria:**
- Lighthouse Performance, Accessibility, Best Practices and SEO at or above 90 on mobile.
- First-load JavaScript at or below about 150 KB gzipped; particle module loads after first paint.
- Tier C (static) experience verified on a low-end device.
- Security headers pass an automated check.
- At least 100 waitlist signups or 20 completed student interviews (set the target before launch).

---

## Phase 2: Model training (weeks 3 to 15)

**Goal:** an own fine-tuned model plus small supporting models and a validator that together beat a strong prompted baseline on faithfulness and usefulness. Details in [05](05-DATASETS.md), [06](06-MODEL-TRAINING.md), [07](07-EVALUATION-AND-QUALITY.md).

| Sub-phase | Work | Output |
|---|---|---|
| 2A Data and gold set | Collect and licence-check Hugging Face datasets; build synthetic pipeline; hand-label 300 to 500 resumes | Clean datasets, labelling guide, gold set v1 |
| 2B Rules engine and validator | Parser, X-Ray rules, Fact Ledger schema, validator (before any generation) | Deterministic engine with tests |
| 2C Small models | Extraction/NER, proof-depth classifier, JD requirement extractor, embeddings | Models on CPU, benchmarked |
| 2D Main model SFT | QLoRA fine-tune of a 7B to 8B class base model on ledger-grounded tasks | Checkpoint v0.1 |
| 2E Faithfulness tuning | Rejection sampling and preference tuning using the validator to penalise invented facts | Checkpoint v0.2 |
| 2F Evaluation | Compare with prompted baseline and Groq fallback on the gold set | Report and go/no-go |
| 2G Compress and serve | Quantise, load test, build the inference service | Serving image and latency numbers |

**Exit criteria (go/no-go gate):**
- Faithfulness: zero facts outside the ledger after validation on the held-out set.
- Fine-tuned model matches or beats the prompted baseline on task quality, or equals it at clearly lower cost/latency.
- Latency target met on the chosen serving hardware.
- Model card and data card written.

If the gate fails, ship the prompted-baseline path (Groq or another hosted model under the same validator) and keep iterating. Do not block the product on the model.

---

## Phase 3: Backend, auth and dashboard UI (weeks 13 to 23)

**Goal:** a working private-beta product. Specs in [10](10-DASHBOARD-UI.md), [13](13-API-AND-DATA-MODEL.md). The app uses the same cosmic-glass identity as the landing page but in a **calm, static, more opaque** form.

| Sub-phase | Work |
|---|---|
| 3A Backend core | FastAPI, PostgreSQL, authentication, ownership checks, file upload pipeline, job queue |
| 3B Engine integration | Parser, X-Ray, claim classifier, ledger, validator, model service wired in |
| 3C Dashboard v1 | Upload, X-Ray, Defensibility map (list + constellation views), Evidence Intake, Apply-or-Skip, DOCX export |
| 3D Integrations | GitHub Project Truth Check, tailored builder with diff |
| 3E Account and privacy | Data export, delete-everything, consent controls, retention jobs, Calm mode |

**Exit criteria:**
- A new user completes the first-session flow in about 15 minutes.
- All controls in [11](11-SECURITY.md) tagged "Beta" are implemented and tested.
- Every generated export passes the validator with zero placeholders.

---

## Phase 4: Beta and hardening (weeks 23 to 29)

- Invite 30 to 100 students; interview at least 20 of them.
- Independent security review or penetration test of auth, upload and model endpoints.
- Privacy review with a qualified lawyer before opening signups.
- Performance and cost tuning (cache, queue limits, model batching).
- Fix top usability issues; publish the first benchmark report.

**Exit criteria:** no open high/critical security findings; privacy sign-off; positive signal that users act on suggestions.

---

## Phase 5: Launch and growth (week 29 onward)

- Public launch, student community outreach, college placement-cell pilots.
- Interview Fire Drill (text, then voice; Hinglish).
- Outcome Tracker with opt-in anonymised data contribution.
- PDF export; roles beyond software; regional-language phrasing support.
- Pricing experiments only after the free core is trusted.

---

## Dependencies and risks between phases

| Dependency | Risk | Mitigation |
|---|---|---|
| Phase 1 cinematic hero | Heavy effects slow cheap phones | Tiers A/B/C, static fallback, performance budgets, device testing |
| Phase 1 design reference | Looking like a copy of another brand | Original "claims as stars" story; no assets or copy reused |
| Phase 2 needs GPU compute | Cost or access limits | Budget early; rent GPUs per run; train small models on CPU |
| Phase 2 needs data | Public data is small and PII-sensitive | Synthetic pipeline plus consented samples ([05](05-DATASETS.md)) |
| Phase 3 needs a model | Model gate fails | Fallback to prompted baseline under the same validator |
| Phase 4 needs real users | Low signups | Use the Phase 1 waitlist and student communities |

# Pramaan (प्रमाण)

**Har line ka pramaan.** *Proof for every line of your resume.*

Pramaan is an evidence-first career copilot for Indian students and freshers. It helps you **prove every claim on your resume, decide which jobs are worth applying to, and prepare for the questions your own resume invites.** It is powered by our own fine-tuned language model, with a strict validator that stops it from inventing facts.


---

## Why this exists

Most resume tools polish the *document*. Freshers' real problems are different: scores that feel like upsell bait, AI rewrites that sound generic or invent numbers, tutorial-clone projects, skills lists that become interview traps, and hundreds of applications sent to roles that were never realistic. Pramaan is built on one idea:

> A resume is only as strong as the proof behind each line.

## What it does *(planned)*

- **Resume X-Ray:** see what a machine actually reads from your file.
- **Evidence Intake:** the model asks questions and builds bullets only from your answers.
- **Fact Ledger + Validator:** every fact is tagged with its source; nothing is invented.
- **Defensibility Score:** each claim rated Listed, Used, Demonstrated or Quantified.
- **Project Truth Check:** GitHub-based verification and upgrade paths for projects.
- **Apply-or-Skip triage:** honest verdicts on whether a job is worth your time.
- **Tailored resume builder** with a diff of every change, exported to DOCX/PDF.
- **Interview Fire Drill** and **Outcome Tracker** (later phases).

## Build phases at a glance

| Phase | Name | Outcome |
|---|---|---|
| 0 | Foundations | Repo, design tokens, security baseline, name checks |
| 1 | **Landing page** | Public site, secure waitlist, validates demand |
| 2 | **Model training** | Own fine-tuned model + small models + validator, evaluated on a gold set |
| 3 | **Backend, auth and dashboard UI** | Working product for private beta |
| 4 | Beta and hardening | Security review, privacy review, real-user feedback |
| 5 | Launch and growth | Interview Fire Drill, outcome tracker, institution pilots |

Full detail: [02-PHASES-AND-ROADMAP](docs/02-PHASES-AND-ROADMAP.md).

## Documentation index

| # | Document | What it covers |
|---|---|---|
| 01 | [Vision and Product](docs/01-VISION-AND-PRODUCT.md) | Problem, users, principles, name |
| 02 | [Phases and Roadmap](docs/02-PHASES-AND-ROADMAP.md) | Every phase, sub-phase, exit criteria |
| 03 | [Features Spec](docs/03-FEATURES-SPEC.md) | What each feature does and how it behaves |
| 04 | [Architecture](docs/04-ARCHITECTURE.md) | Components, model split, data flow |
| 05 | [Datasets](docs/05-DATASETS.md) | Hugging Face datasets, gaps, data pipeline, licensing |
| 06 | [Model Training](docs/06-MODEL-TRAINING.md) | Base models, fine-tuning plan, hardware, serving |
| 07 | [Evaluation and Quality](docs/07-EVALUATION-AND-QUALITY.md) | Gold set, metrics, release gates |
| 08 | [Design System](docs/08-DESIGN-SYSTEM.md) | Minimal glassmorphism, tokens, accessibility, mobile |
| 09 | [Landing Page](docs/09-LANDING-PAGE.md) | Phase 1 spec |
| 10 | [Dashboard UI](docs/10-DASHBOARD-UI.md) | Phase 3 screens and flows |
| 11 | [Security](docs/11-SECURITY.md) | Threat model and controls |
| 12 | [Privacy and Compliance](docs/12-PRIVACY-AND-COMPLIANCE.md) | Data handling, consent, DPDP considerations |
| 13 | [API and Data Model](docs/13-API-AND-DATA-MODEL.md) | Endpoints, schemas, Fact Ledger |
| 14 | [Deployment and Ops](docs/14-DEPLOYMENT-AND-OPS%20%281%29.md) | Infra, CI/CD, monitoring, costs |

## Tech stack (proposed)

- **Frontend:** Next.js (TypeScript), Tailwind CSS, Radix UI primitives; minimal glassmorphism design; mobile-first.
- **Backend:** Python, FastAPI, Pydantic, PostgreSQL, S3-compatible storage.
- **ML:** PyTorch, Hugging Face Transformers, PEFT/TRL (QLoRA fine-tuning), a 7B to 8B class open-weight base model, small encoder models for extraction, Groq for minor language tasks only.
- **Serving:** GPU inference service for the main model (vLLM or similar); CPU for small models and the rules engine.
- **Infra:** Docker, GitHub Actions, AWS.

## Security and privacy in one paragraph

Resumes are personal data, so security is a product feature, not an afterthought: strong authentication, strict ownership checks, sandboxed file parsing, treating all resume and job text as untrusted input to the model (prompt-injection defences), PII redaction before any external call, encryption in transit and at rest, short retention with one-click deletion, and no resume content in logs. See [11-SECURITY](docs/11-SECURITY.md) and [12-PRIVACY-AND-COMPLIANCE](docs/12-PRIVACY-AND-COMPLIANCE.md).

## Proposed repository layout

```
pramaan/
├── apps/
│   ├── web/              # Next.js: landing + dashboard
│   └── api/              # FastAPI
├── engine/               # parsing, x-ray, claims, ledger, validator, triage, github, export
├── ml/
│   ├── data/             # data prep scripts (no raw PII committed)
│   ├── train/            # SFT / DPO / encoder training configs
│   ├── eval/             # gold set loaders, metrics, regression tests
│   └── serve/            # inference service
├── docs/                 # these documents
├── infra/                # Docker, IaC, CI
└── README.md
```

## Getting started *(planned)*

The scaffold is not committed yet. When it is, local setup will be:

```bash
git clone https://github.com/<your-username>/pramaan.git
cd pramaan
cp .env.example .env     # fill in values; never commit .env
docker compose up --build
```

## Contributing

Early help that matters most: consented or synthetic resume/JD samples, claim-level labelling, parser edge cases, and security/privacy reviews. See [07-EVALUATION-AND-QUALITY](docs/07-EVALUATION-AND-QUALITY.md) for how contributions are validated.

## License

The GitHub repository includes an MIT licence for its contents. Model weights and datasets may have separate licences; check the terms of every base model and dataset before using or distributing them.

## Disclaimer

Pramaan is a decision-support tool. No resume tool can guarantee interviews, ATS outcomes or job offers. Triage verdicts are guidance and you can always override them.

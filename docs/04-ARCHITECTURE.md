# 04. Architecture

## System overview

```
Browser (Next.js, mobile-first)
   │  HTTPS only
   ▼
CDN / WAF ──► Web app (static landing + dashboard)
   │
   ▼
API gateway (FastAPI)  ── auth, rate limits, ownership checks
   ├── Upload service ──► quarantine bucket ──► scanner ──► sandboxed parser
   ├── Engine (deterministic Python): X-Ray rules, claims, Fact Ledger, validator, triage
   ├── Small models (CPU): extraction, proof-depth classifier, JD extractor, embeddings
   ├── Model service (GPU): own fine-tuned LLM  ◄── request queue
   ├── GitHub service: read-only repo analysis (allowlisted hosts)
   ├── Groq adapter: minor language tasks only, PII-redacted input
   └── Storage: PostgreSQL + object store (encrypted), Redis (queue/cache)
```

## Design principles

1. **Deterministic first.** Rules and classifiers do everything they can before any generative model is called.
2. **Generation is always validated.** No model output reaches the user without the validator.
3. **Untrusted input everywhere.** Resume text, JD text, repo contents and file metadata are untrusted ([11](11-SECURITY.md)).
4. **Isolation.** Parsing and model serving run as separate, least-privilege services.
5. **Graceful degradation.** If the own model is down, fall back to Groq under the same validator; if Groq is down, deterministic features still work.

## Who does what

| Task | Handled by | Why |
|---|---|---|
| File parsing, layout checks, rules | Deterministic Python | Fast, reproducible, free |
| Section and entity extraction | Own small encoder model | Cheap, accurate, CPU-friendly |
| Proof-depth classification | Own classifier | Core logic; must be consistent |
| Skill / JD semantic matching | Small embedding model | CPU-friendly, cacheable |
| Evidence questions, bullet drafting, interview questions, answer grading | **Own fine-tuned LLM (7B to 8B class)** | Core product behaviour |
| Tone polish, shortening, plain-language explanations, Hinglish phrasing help | **Groq (minor tasks only)** | Low stakes, cheap, replaceable |
| Fallback when own model is unavailable | Groq with same validator | Resilience |

Groq never sees raw PII: names, phone numbers, emails and addresses are replaced with tokens before the call and restored locally.

## Validator (the key component)

After any generation step:

1. Extract numbers, units, tool/technology names, organisations and dates from the output.
2. Compare each against the Fact Ledger entries for that claim.
3. Anything not present is **rejected** or turned into a `placeholder` the user must fill.
4. If rejection rate is high, re-run with stricter constraints; after N failures return a safe template instead of unverified text.

This turns "we never invent facts" into an enforced property, independent of which model produced the text.

## Model service

- Separate container with its own network policy; no direct internet egress.
- Inputs are structured (task type + ledger facts + resume excerpt), outputs are schema-constrained JSON.
- Request queue with per-user concurrency limits and timeouts.
- Prompt templates keep untrusted text inside clearly delimited data sections and never grant the model tools with side effects ([11](11-SECURITY.md)).
- Versioned: every response records `model_version` and `prompt_version`.
- Serving options: GPU with vLLM-style batching for the main model; quantised small variant for CPU fallback (slower).

## Data flow: first session

1. User uploads resume → quarantine storage → size/type checks → malware scan → sandboxed parsing.
2. Engine builds the structured resume and runs X-Ray and claim classification.
3. Dashboard shows the Defensibility map.
4. For weak claims, the model service asks questions; answers are stored as ledger facts.
5. Drafted bullets pass the validator; the user accepts or edits.
6. JD pasted → extraction → triage verdict with reasons.
7. Tailored version built; DOCX exported from the validated structure (not from free-form model text).

## Background jobs

Upload scanning, parsing, GitHub analysis, model calls and exports run as queued jobs so the UI stays responsive and abusive load cannot block other users.

## Caching

- Cache by content hash for parse results and embeddings (per user, never shared across users).
- Cache JD extraction results by JD hash plus engine version.
- Never cache across users in a way that could leak content.

## Observability

- Structured logs with **no resume or JD content**; log request IDs, user IDs (hashed), timings, versions.
- Metrics: queue depth, model latency, validator rejection rate, error rates.
- Alerts on rejection-rate spikes (signals a model regression).

## Scaling path

1. **Beta:** one app server, Postgres, Redis, one GPU instance for the model service.
2. **Growth:** separate worker pool, autoscaled model replicas, read replicas.
3. **Later:** regional deployment in India for latency and data-residency options.

## Technology choices (proposed)

| Layer | Choice | Notes |
|---|---|---|
| Frontend | Next.js + TypeScript + Tailwind + Radix | See [08](08-DESIGN-SYSTEM.md) |
| API | FastAPI + Pydantic | Typed schemas end to end |
| DB | PostgreSQL | Row-level ownership; encrypted at rest |
| Queue/cache | Redis | Short TTLs |
| Object store | S3-compatible | Separate quarantine and clean buckets |
| ML | PyTorch, Transformers, PEFT, TRL | See [06](06-MODEL-TRAINING.md) |
| Serving | vLLM-style server (GPU) | Quantised model |
| CI/CD | GitHub Actions | See [14](14-DEPLOYMENT-AND-OPS%20%281%29.md) |

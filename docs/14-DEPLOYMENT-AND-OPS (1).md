# 14. Deployment and Operations

## Environments

| Environment | Purpose | Data |
|---|---|---|
| Local | Development | Synthetic data only |
| CI | Automated tests | Synthetic data only |
| Staging | Pre-release checks, load and security tests | Synthetic data only |
| Production | Real users | Real data, strictest controls |

Rule: **no production data in any other environment.** Separate accounts/projects and separate credentials per environment.

## Phase-by-phase hosting

### Phase 1: Landing page
- Static export or edge-rendered Next.js behind a CDN (any reputable static host or object storage plus CDN).
- A small serverless function or API route for the waitlist form, with rate limiting and bot protection ([09](09-LANDING-PAGE.md)).
- Custom domain, HTTPS, HSTS, security headers.
- Email delivery through a transactional provider with SPF, DKIM and DMARC configured.

### Phase 2: Model training
- Training happens on rented or credited GPU instances per run; shut down when finished.
- Data and checkpoints stored in private, encrypted object storage; gold set in a separate restricted bucket.
- Reproducible runs: container image, pinned dependencies, config files in the repo, experiment tracking.
- Budget caps and alerts before starting any run ([06](06-MODEL-TRAINING.md)).

### Phase 3: Private beta
- **App tier:** containers for web and API on a managed container service or a small VM group.
- **Database:** managed PostgreSQL with encryption, automated backups, point-in-time recovery.
- **Cache/queue:** Redis (managed).
- **Object storage:** separate quarantine and clean buckets, private, server-side encryption.
- **Model service:** one GPU instance (on-demand or reserved depending on credits and usage) in a private subnet, no public IP, no outbound internet by default, reachable only from the API.
- **Parsing workers:** isolated containers, no network egress.
- **Edge:** CDN and WAF in front of web and API.

Note: a CPU-only instance is fine for the web app, rules engine and small models; a 7B to 8B generative model needs a GPU for acceptable latency. If credits or budget do not allow an always-on GPU, options include scheduled/on-demand GPU, a smaller distilled model for simple tasks, or the prompted fallback under the same validator.

### Phase 4 and 5: Growth
- Autoscaling worker pool, model replicas behind a queue, read replicas for the database.
- Optional India-region deployment for latency and trust; check data-transfer implications ([12](12-PRIVACY-AND-COMPLIANCE.md)).

## Network layout (beta)

```
Internet → CDN/WAF → Load balancer → Web/API (private subnets)
                                      ├─ DB (private)
                                      ├─ Redis (private)
                                      ├─ Object storage (private endpoints)
                                      ├─ Parsing workers (no egress)
                                      └─ Model service (no public IP, no egress)
Outbound allowlist (API only): github.com / api.github.com, email provider, Groq (redacted payloads)
```

## CI/CD

- **GitHub Actions** pipelines:
  1. Lint, type-check, unit tests
  2. Dependency and secret scanning, SAST, container image scan
  3. Build images, generate SBOM
  4. Integration tests (including authorisation matrix, upload abuse cases, injection suite)
  5. ML checks: engine regression suite and validator tests on every PR; full gold-set evaluation on model/prompt changes ([07](07-EVALUATION-AND-QUALITY.md))
  6. Deploy to staging automatically; production after approval
- Protected `main`; required reviews; no direct pushes.
- Database migrations run as a separate, reviewed step with rollback plans.
- Immutable, versioned images; deploy by digest.
- Feature flags for risky features (for example turning the own model on or off per task).

## Configuration and secrets

- Configuration via environment variables; **secrets only in a secret manager**.
- `.env.example` documents variables without values; `.env` is git-ignored.
- Rotate keys on a schedule and after any suspected exposure.
- Different credentials per environment and per service (least privilege).

Expected variables (names may change):

| Variable | Purpose |
|---|---|
| `DATABASE_URL` | PostgreSQL connection |
| `REDIS_URL` | Cache/queue |
| `SESSION_SECRET` | Session signing |
| `OAUTH_GOOGLE_CLIENT_ID/SECRET` | Sign-in |
| `GITHUB_APP_ID/PRIVATE_KEY` | GitHub integration |
| `GROQ_API_KEY` | Minor language tasks (optional) |
| `MODEL_ENDPOINT` | Internal URL of the model service |
| `MODEL_VERSION`, `PROMPT_VERSION` | Pin versions |
| `RETENTION_HOURS` | Upload retention |
| `STORAGE_BUCKET_QUARANTINE/CLEAN` | Object storage |

## Observability

- **Logs:** structured, content-free, request IDs; centralised with limited retention.
- **Metrics:** latency (p50/p95), error rates, queue depth, model tokens/sec, validator rejection rate, GPU utilisation, cost per active user.
- **Tracing:** request traces across API, queue and model service (no payloads).
- **Alerts:** auth anomalies, rejection-rate spikes, queue backlog, failed backups, certificate expiry, unusual spend.
- **Uptime checks** for landing page, API health and a synthetic end-to-end test.

## Backups and recovery

- Automated daily database backups plus point-in-time recovery; encrypted.
- Object storage versioning for model artifacts and datasets (not for user uploads beyond retention).
- Restore drills quarterly; document RTO/RPO targets (for beta, accept something modest and write it down).
- Backup expiry aligned with the deletion policy ([12](12-PRIVACY-AND-COMPLIANCE.md)).

## Cost management

| Cost driver | Control |
|---|---|
| GPU inference | Batching, quantisation, caching, scheduled scaling, per-user quotas |
| GPU training | Experiment budget, small trial runs first, shut down idle instances |
| Storage | Short retention, lifecycle rules |
| Third-party APIs | Groq for minor tasks only, caching, rate limits |
| Egress/CDN | Optimised assets, caching |

Set billing alerts and hard budget caps from day one. Track cost per active user monthly. Cloud credits expire; plan the post-credit budget before relying on them.

## Operational runbooks (write before beta)

- Deploy and rollback
- Model rollback (switch to previous version or to the prompted fallback)
- Elevated validator rejection rate
- Queue backlog / model unavailable
- Suspected data exposure or credential leak
- User deletion request handling
- Restore from backup

## Release process

1. Merge to `main` after review and green CI.
2. Auto-deploy to staging; run smoke and end-to-end tests.
3. For model/prompt changes: run the full evaluation and compare to the previous version; require approval if any metric regresses.
4. Canary release to a small share of users or invite-only group.
5. Monitor key metrics for a defined window; roll back on regression.
6. Record release notes including engine, scorer, model and prompt versions.

## Disaster and abuse scenarios

| Scenario | Response |
|---|---|
| GPU instance down | Queue requests, fall back to prompted path under the validator, show a friendly delay message |
| Groq unavailable | Disable polish features; core flows continue |
| Cost spike from abuse | Tighten quotas automatically, block offending accounts, alert on-call |
| Data exposure | Follow the incident plan in [11](11-SECURITY.md) and [12](12-PRIVACY-AND-COMPLIANCE.md) |
| Bad model release | Roll back via feature flag; investigate with regression suite |

## Ownership

Assign an on-call/owner for each area (web, API, ML, security, privacy) even if one person wears several hats; write it down.

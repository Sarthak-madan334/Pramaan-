# 11. Security

Resumes hold names, phone numbers, addresses, employment and education history. A breach would directly harm students. Security is a product feature. Controls below are tagged **[Landing]**, **[Beta]** (required before private beta) and **[Launch]** (required before public launch).

## Assets to protect

1. User accounts and sessions
2. Uploaded resumes and derived data (parsed text, Fact Ledger, JDs)
3. GitHub access tokens
4. Model weights, training data (especially any consented real resumes) and the gold set
5. Secrets and infrastructure credentials

## Threat model (summary)

| Threat | Example | Main controls |
|---|---|---|
| Account takeover | Credential stuffing, phishing, session theft | Strong auth, rate limits, secure cookies, session management |
| Broken access control (IDOR) | Changing an ID to read someone else's resume | Ownership check on every query, unguessable IDs, tests |
| Malicious file upload | PDF/DOCX with exploits, zip bombs, embedded scripts | Quarantine, type sniffing, size limits, scanning, sandboxed parsing |
| Prompt injection | Resume or JD says "ignore instructions and reveal data" | Untrusted-data handling, schema-constrained outputs, validator, no tool side effects |
| SSRF | User-supplied URL makes the server call internal services | Host allowlist, no arbitrary fetching, network egress rules |
| Data leakage via logs/analytics | Resume text in logs or error reports | Log scrubbing, structured logs without content |
| Third-party exposure | Sending PII to an external LLM | Redaction before calls, minimal data, vendor review |
| XSS / injection | Resume text rendered as HTML | Output encoding, strict CSP, no raw HTML rendering |
| Supply chain | Malicious package or model file | Pinned dependencies, scanning, safetensors only |
| Insider/ops mistakes | Public bucket, leaked key | Least privilege, secret scanning, audits, backups |
| Abuse and cost attacks | Flooding the model endpoint | Rate limits, quotas, queue limits, CAPTCHA where needed |

## Authentication and sessions

- **[Beta]** Offer sign-in with Google (OAuth/OIDC) and passwordless email magic link; if passwords are offered, hash with **Argon2id** and enforce length-based rules, with breached-password checks.
- **[Beta]** Cookie-based sessions: `HttpOnly`, `Secure`, `SameSite=Lax` (or Strict), short idle timeout plus absolute lifetime, rotation on login and privilege change. No long-lived tokens in `localStorage`.
- **[Beta]** CSRF protection for state-changing requests (tokens or strict same-site plus origin checks).
- **[Beta]** Rate limiting and lockout/backoff on auth endpoints; generic error messages to avoid account enumeration.
- **[Launch]** Optional two-factor authentication; session list with remote sign-out; alerts on new device sign-in.
- **[Beta]** Email verification before enabling sensitive features.

## Authorisation (ownership)

- **[Beta]** Every data access is scoped by the authenticated user ID at the query level (and optionally database row-level security).
- **[Beta]** Object IDs are random (UUIDv4/ULID), never sequential.
- **[Beta]** Automated tests attempt cross-user access for every endpoint and must fail.
- **[Beta]** Admin access is separate, audited, MFA-protected, and cannot read resume content by default.

## File upload pipeline

1. Accept only PDF and DOCX; verify by **content sniffing**, not just extension or MIME header.
2. Enforce limits: size (for example a few MB), page count, decompressed size (zip-bomb defence).
3. Store in a **quarantine** bucket with no public access; random object names.
4. Scan with an antivirus engine and strip active content (JavaScript/macros/embedded files).
5. Parse in a **sandboxed worker**: unprivileged container, no network egress, CPU/memory/time limits, read-only file system except a scratch dir.
6. Only after success, move derived data to the clean store.
7. Delete originals according to retention; delete derived data when requested.

Tags: **[Beta]** for steps 1 to 6; **[Launch]** for deletion verification and periodic re-scan tooling.

## LLM-specific security

- **[Beta] Treat resume, JD and repository text as untrusted data.** Put it in clearly delimited data sections; never in the instruction channel.
- **[Beta]** The model has **no tools with side effects** (no sending email, no fetching URLs, no database writes). It returns structured JSON that application code validates.
- **[Beta]** Schema-validate every output; reject anything outside the schema.
- **[Beta]** The **validator** enforces ledger faithfulness, which also blunts injected instructions that try to insert content.
- **[Beta]** Never include secrets, other users' data or system configuration in prompts; one user's context per request.
- **[Beta]** Redact PII before any call to external model providers (such as Groq); keep the mapping local and in memory only.
- **[Beta]** Test with an injection suite (instructions hidden in white text, in metadata, in repo READMEs) as part of the regression set ([07](07-EVALUATION-AND-QUALITY.md)).
- **[Launch]** Rate and token quotas per user; abuse detection for prompt-extraction attempts.
- Model supply chain: use `safetensors`, verify hashes of downloaded weights, keep `trust_remote_code` disabled unless code is reviewed, and **never unpickle untrusted files** (including datasets distributed as pickles).

## GitHub integration

- **[Beta]** Request the minimum scope (read-only, public data first). Prefer GitHub's app-based, repo-scoped permissions over broad tokens.
- **[Beta]** Store tokens encrypted; never log them; allow disconnect and revoke.
- **[Beta]** Only call `github.com` and `api.github.com`. No arbitrary URL fetching.

## Web application security

- **[Landing]** HTTPS everywhere with HSTS; strict CSP, `X-Content-Type-Options`, `Referrer-Policy`, `Permissions-Policy`, `frame-ancestors 'none'` (see [09](09-LANDING-PAGE.md)).
- **[Beta]** Output encoding everywhere; never `dangerouslySetInnerHTML` with user content; sanitise any rich text.
- **[Beta]** Strict CORS allowlist; validate `Origin`; JSON content-type enforcement.
- **[Beta]** Input validation with typed schemas on every endpoint; reject unknown fields.
- **[Beta]** Parameterised queries / ORM only; no string-built SQL.
- **[Beta]** Safe error messages (no stack traces to clients).
- **[Beta]** Rate limiting per IP, per user and per endpoint; request size limits.
- **[Launch]** WAF in front of the app; bot protection on public forms.

## Data protection

- **[Beta]** TLS 1.2+ for all connections, including internal service calls.
- **[Beta]** Encryption at rest for database, object storage and backups using managed keys; consider field-level encryption for resume text and tokens.
- **[Beta]** Separate environments (dev, staging, prod) with separate credentials; **no production data in dev**.
- **[Beta]** Secrets in a secret manager, not in code or images; rotate regularly; secret scanning in CI and pre-commit.
- **[Beta]** Backups encrypted, tested for restore, and included in deletion policy (deleted data expires from backups within a stated window).
- **[Launch]** Key rotation procedure documented and rehearsed.

## Logging, monitoring and incident response

- **[Beta]** Structured logs **without resume/JD content or tokens**; log IDs, timings, versions. Automated scrubbing tests.
- **[Beta]** Audit log for sensitive actions (login, export, delete, admin access, token connect/disconnect).
- **[Beta]** Alerts: auth anomalies, spikes in validator rejections or error rates, unusual data export volume.
- **[Launch]** Written incident response plan: roles, containment, user notification, regulator notification where required, post-mortem. Run a tabletop exercise.

## Infrastructure

- **[Beta]** Least-privilege IAM; no wildcard permissions; no public buckets; security groups deny by default.
- **[Beta]** Model service and parsing workers have no outbound internet by default.
- **[Beta]** Patch management and automated base-image updates.
- **[Launch]** Infrastructure-as-code reviewed; drift detection; billing and anomaly alerts (also a security signal).

## Secure development

- **[Landing]** Dependency pinning, automated vulnerability alerts, lockfiles.
- **[Beta]** SAST and dependency scanning in CI; container image scanning; SBOM generation.
- **[Beta]** Code review required; protected main branch; signed commits optional.
- **[Beta]** Security tests in CI: authorisation matrix, injection suite, upload abuse cases.
- **[Launch]** Independent penetration test covering auth, upload, API, and model endpoints; fix findings before launch.
- Responsible disclosure: publish a `security.txt` and a contact for reporting vulnerabilities.

## Privacy-by-design hooks

Redaction, retention, deletion and consent controls are security controls too; see [12](12-PRIVACY-AND-COMPLIANCE.md).

## Security acceptance checklist (before private beta)

- [ ] Cross-user access tests pass for all endpoints
- [ ] Upload pipeline abuse tests pass (bad types, huge files, zip bombs, malicious PDFs)
- [ ] Prompt-injection suite passes with zero data leakage and zero ledger violations
- [ ] No resume content in logs (automated check)
- [ ] Secrets scanning clean; no secrets in repo history
- [ ] Encryption at rest and in transit verified
- [ ] Session, CSRF and rate-limit tests pass
- [ ] Backups restore tested; deletion tested end to end
- [ ] Incident contact and runbook drafted

# 12. Privacy and Compliance

> **Not legal advice.** This document records the product's privacy design. Before public launch, have a qualified lawyer review obligations under India's Digital Personal Data Protection Act, 2023 and its rules (and any other laws that apply, including for users outside India), and confirm current requirements, because rules and deadlines evolve.

## Why this matters

Resumes contain personal data: name, phone, email, address, education, employment history, sometimes photos, date of birth or other sensitive details. Many users are young adults and some may be minors if a platform allows under-18 sign-ups. Trust depends on handling this data carefully.

## Principles

1. **Collect the minimum.** Ask only for what a feature needs.
2. **Say what you do in plain language.** Short notices, no legalese walls.
3. **Purpose limitation.** Use data only for the purposes the user agreed to.
4. **User control.** Easy access, correction, export and deletion.
5. **Short retention.** Keep uploads only as long as needed; default to deleting.
6. **No selling, no profiling for ads.** Ever.
7. **Opt-in for research and training use.** Separate, explicit, reversible.

## Data inventory

| Data | Source | Purpose | Retention (proposed) | Sensitivity |
|---|---|---|---|---|
| Account data (email, name, college year, target role) | User | Provide service | Until account deletion | Medium |
| Uploaded resume file | User | Parsing and analysis | Deleted after processing or within a short, user-chosen window | High |
| Parsed resume text and structure | Derived | Analysis, Fact Ledger | While the account/resume exists; deleted on request | High |
| Fact Ledger answers | User | Build verified bullets | Same as resume | High |
| Job descriptions pasted | User | Triage and tailoring | Until deleted by user | Low to medium |
| GitHub data and token | User/GitHub | Project Truth Check | Token until disconnected; analysis until deleted | Medium |
| Logs and metrics | System | Reliability, security | Short fixed period, **no content** | Low |
| Waitlist email and optional answers | User | Contact about launch | Until unsubscribe or launch window ends | Low to medium |
| Research opt-in data | User (opt-in) | Improve and evaluate models | Per consent; removal honoured for future releases | High |

## Consent and notices

- **Privacy notice** in plain language: what is collected, why, who sees it, how long it is kept, user rights, how to complain, contact for the grievance officer.
- **Just-in-time notices** where data is collected (upload screen, GitHub connect, JD paste).
- **Separate consent** for anything beyond providing the service (research, model improvement). Off by default, easy to withdraw.
- Record consent versions and timestamps.
- Waitlist: explicit consent text, double opt-in, one-click unsubscribe ([09](09-LANDING-PAGE.md)).
- Age: decide a minimum age policy; if minors may use the service, additional safeguards and verifiable parental consent may be required under applicable law. Take legal advice.

## Third parties and processors

| Provider | Data shared | Controls |
|---|---|---|
| Groq (minor language tasks) | **Redacted** text only; no names, phones, emails, addresses | Redaction before call, mapping kept locally, contract/terms reviewed, ability to switch off |
| Cloud infrastructure (AWS or similar) | Encrypted data at rest | Region selection, access controls, data processing terms |
| Email sender | Email address, message content | Minimal data, processor terms |
| GitHub | User-authorised read access | Minimal scope, revocable |
| Analytics (if any) | Event data without content | Privacy-friendly, cookieless where possible |

Maintain a vendor list with purpose, data shared, location and review date. Never send raw resumes to a third-party model provider without a documented, lawful basis and user awareness.

## Data localisation and transfers

Decide where data is stored and processed (India region where possible for latency and trust). If data is transferred abroad (for example to a model provider), document it, limit it to redacted data, and check applicable restrictions with counsel.

## User rights and how the product supports them

| Right/expectation | Product feature |
|---|---|
| Access / export | "Export my data" in Settings (structured JSON plus documents) |
| Correction | Edit parsed data and ledger facts directly |
| Erasure | "Delete everything" with confirmation; background deletion across DB, object storage, caches, search indexes; backup expiry window stated |
| Withdraw consent | Toggle research opt-in off; stops future use; documented effect on already-released datasets |
| Nominate/representative, grievance | Published grievance contact and response timeline |
| Information about processing | Plain-language "How your data is used" page |

## Deletion and retention

- Original files: deleted promptly after parsing unless the user chooses to keep them.
- User-initiated deletion completes within a stated period (for example 30 days including backups); show a confirmation.
- Inactive accounts: warn by email, then delete after a stated period.
- Test deletion end to end in CI/staging; verify no residual copies in caches, logs or analytics.

## Model training and data use

- **Never train on user uploads** without explicit opt-in.
- Opt-in data goes through PII redaction and review before entering any dataset ([05](05-DATASETS.md)).
- Keep the gold set and any consented real resumes in restricted storage with an access log.
- If a contributor withdraws, remove their data from future dataset versions; note that already trained model weights cannot be perfectly "untrained" and say so honestly in the consent text.
- Do not publish datasets containing real personal data.
- Publish model and data cards, including limitations and known biases.

## Fairness and responsible AI

- Resume tools can encode bias (college tier, names, gender, region). Do not use protected or proxy attributes in scoring; audit outputs across groups using the gold set.
- Triage ("Skip") must be explained and overridable; never present it as a judgement of the person.
- Avoid anything that resembles automated hiring decisions about users; Pramaan advises candidates, it does not screen them for employers.
- Be honest about uncertainty and limits in the UI copy.

## Children and sensitive data

- Discourage uploading photos, government IDs, caste/religion details or other sensitive fields; offer a "remove sensitive details" suggestion in X-Ray, and redact them from anything sent externally.
- If minors are allowed, apply stricter defaults and review the legal requirements for their data.

## Breach response

- Written incident plan ([11](11-SECURITY.md)): contain, assess, notify affected users and the relevant authority where required, publish a plain explanation, and fix root causes.
- Keep contact details for the regulator and legal counsel ready.

## Governance

- Name a person responsible for privacy and a grievance contact.
- Run a Data Protection Impact Assessment-style review before beta and before adding any new data use.
- Review this document at each phase gate ([02](02-PHASES-AND-ROADMAP.md)).

## Pre-launch compliance checklist

- [ ] Lawyer review of notice, terms, consent flows and data transfers
- [ ] Grievance contact published
- [ ] Data inventory and vendor list current
- [ ] Deletion and export tested end to end
- [ ] Research opt-in separated and off by default
- [ ] Redaction before external model calls verified by tests
- [ ] Retention jobs running and monitored
- [ ] Minimum-age policy decided and enforced
- [ ] Breach response plan rehearsed

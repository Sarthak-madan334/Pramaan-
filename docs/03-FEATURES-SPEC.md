# 03. Features Spec

Each feature lists purpose, behaviour, inputs/outputs, and the phase it ships in. Phase numbers refer to [02](02-PHASES-AND-ROADMAP.md).

## Cross-cutting rules

- **Free fixes:** every issue shown comes with how to fix it, at no charge.
- **Explain everything:** each finding links to the exact resume line or fact behind it.
- **No invented facts:** generated text may use only facts in the Fact Ledger.
- **Reproducible:** each result records the engine and model versions that produced it.
- **User stays in control:** every suggestion can be accepted, edited or rejected; verdicts can be overridden.

---

## F1. Resume X-Ray (Phase 3C)

**Purpose:** show what a machine actually reads and flag real parsing problems.

- **Input:** PDF or DOCX (size and page limits apply, see [11](11-SECURITY.md)).
- **Output:** parsed view (sections, dates, contact fields, skills, bullets) beside the original; a pass/warn/fail checklist.
- **Checks:** reading order issues (tables, multi-column), text in images, missing or unusual headings, missing dates, unreadable fonts, contact info placement, page length.
- **Parser agreement:** run more than one open-source parser and highlight where they disagree.
- **Honesty:** states plainly that it does not simulate any specific company's ATS.

## F2. Defensibility Score (Phase 3C)

**Purpose:** rate how well each claim is backed by proof.

| Level | Meaning | Example |
|---|---|---|
| 0 Listed | Named, no context | "Python" in a skills list |
| 1 Used | Appears in a project or role | "Built a scraper in Python" |
| 2 Demonstrated | Specific problem and approach | "Used async Python to scrape 40 sites with retry logic" |
| 3 Quantified | Measured outcome | "Cut scrape time from 3 hours to 25 minutes" |

- **Output:** per-claim level, list of **risky claims** (prominent on the resume but weakly evidenced), and a recommendation per risky claim (reframe, move to "Familiar with", or add evidence).
- **Rule:** the score is a set of parts (see F8), never a single mystery number.

## F3. Evidence Intake and Fact Ledger (Phase 3C)

**Purpose:** build strong bullets only from facts the user supplied.

1. The system picks the weakest or riskiest claims.
2. The model asks 3 to 6 targeted questions per claim (problem, users, hardest part, what was measured, what was personal work versus tutorial).
3. Answers become structured facts in the **Fact Ledger**, each tagged:
   - `user_stated`: the user typed it
   - `repo_derived`: from GitHub analysis
   - `placeholder`: a number or detail the model needs but does not have
4. The model drafts bullets using only ledger facts.
5. The **validator** checks every number, tool and named entity in the draft against the ledger.
6. Export is blocked while any `placeholder` remains.

## F4. Project Truth Check (Phase 3D)

**Purpose:** verify project claims against the repository and suggest upgrades.

- **Input:** GitHub username or repo URL (public repos first; read-only access; only `github.com` / `api.github.com` are fetched).
- **Signals:** commit history and cadence, languages, structure, tests, CI, README quality, deployment link status, similarity to well-known tutorial repositories, match between resume claims and code (for example "uses Redis" and no Redis present).
- **Output:** never "your project is weak". Instead an **upgrade path**: up to three concrete extensions with hour estimates (add auth, tests for the core module, deploy, rate limiting, design notes).
- **User override:** the user can explain a finding; the explanation is stored, not ignored.

## F5. Apply-or-Skip triage (Phase 3C)

**Purpose:** reduce wasted applications.

- **Input:** pasted JD text or file; user's proven profile (not just listed skills).
- **Extracted:** must-haves, nice-to-haves, years of experience, seniority signals.
- **Verdicts:**
  - **Apply:** strong match
  - **Stretch:** worth applying if a named gap is closed; the fastest way to close it is shown
  - **Skip:** a hard requirement is unmet
- **Always shown:** reasons for the verdict. Always overridable.
- **Weekly summary (later):** which role types the user is competitive for.

## F6. Tailored resume builder with diff (Phase 3D)

**Purpose:** create a per-JD version by selecting and reordering proven content.

- Side-by-side diff of every change.
- Each rewritten bullet lists the facts it uses.
- **Voice check:** flags overused AI or fresher boilerplate and suggests specific, personal alternatives using the user's own words.
- **Export:** DOCX first (single-column, ATS-safe); PDF in Phase 5.

## F7. Interview Fire Drill (Phase 5)

- Questions from the user's own weakest and strongest claims plus gaps against the target JD.
- Technical, behavioural and follow-up chains.
- Text practice first, voice later; English and Hinglish.
- Answers graded against the user's resume and code; defensibility levels update.

## F8. Scores (decomposed)

No single master number. Three independent reports:

1. **Parse integrity:** pass/warn/fail checklist.
2. **Evidence strength:** share of claims at level 2 or higher, weighted by position on the page, minus a penalty for risky claims.
3. **JD relevance:** required skills covered at level 1 or higher count fully; listed-only skills count partially; nice-to-haves count less; synonyms handled by the semantic matcher.

Weights are published and versioned (for example `scorer v0.3`). A change in score always lists the lines that caused it. Scores are never lowered to encourage upgrades.

## F9. Outcome Tracker (Phase 5)

- Log each application and outcome (interview, rejected, no response).
- Private analytics on which resume version or role type gets callbacks.
- Optional, opt-in anonymised contribution to calibrate scoring.

## F10. Account and privacy controls (Phase 3E)

- Export all my data; delete everything; manage consent for research use.
- Retention setting for uploads; visible deletion confirmation.
- Session list with remote sign-out.

---

## Non-goals

Auto-apply bots, recruiter-side screening, simulating a specific employer's ATS, or guaranteeing any outcome.

# 07. Evaluation and Quality

Trust is the product. This document defines how quality is measured, what blocks a release, and what is published.

## Principles

1. **Evaluate before you build.** The gold set exists before the first training run.
2. **Held-out means held-out.** Gold data is never trained on, never used to tune prompts without a separate dev split.
3. **Baselines are mandatory.** Every report compares against a strong prompted baseline.
4. **Failures are permanent tests.** Any bug found becomes a regression case forever.
5. **Publish honestly.** Include weaknesses.

## Evaluation sets

| Set | Purpose | Contents |
|---|---|---|
| Gold (test) | Final reporting | 300 to 500 consented real-structure resumes, human-labelled; no synthetic items |
| Dev | Tuning prompts, thresholds | Separate split, may include synthetic |
| Adversarial | Stress tests | Messy layouts, tricky claims, injection attempts, missing-number traps |
| Regression | Known failures | Cases other tools got wrong, plus every bug we find |

### Regression cases to include from day one

- A clean, well-formatted resume that a parser reports as unreadable.
- Side projects wrongly turned into jobs.
- Metrics that appear in output but not in the input.
- Skills inferred from nothing.
- Multi-column and table layouts.
- Resumes with text only inside images.
- Resumes containing instructions aimed at the AI.

## Metrics

### Parsing and extraction
- Section detection precision/recall.
- Field accuracy (dates, institutions, titles).
- Reading-order accuracy on tricky layouts.
- Parser disagreement rate, and whether disagreement predicts real problems.

### Claims and scoring
- Proof-depth classifier: per-level precision/recall and agreement with human labels (report inter-annotator agreement on the double-labelled subset as the ceiling).
- Risky-claim detection: precision (are flagged claims really risky?) and recall.
- Score stability: same input, same version, same output (must be exact for rules).

### Generation (main LLM)
- **Faithfulness (critical):** share of generated bullets with zero facts outside the ledger. Report raw (before validator) and final (after validator).
- **Placeholder behaviour:** when a needed number is missing, does the model produce a placeholder or ask, rather than invent?
- **Specificity:** share of bullets containing concrete, ledger-backed details; boilerplate-phrase rate.
- **Voice:** reviewer ratings on "sounds like a real person" using blind comparison against baseline.
- **Question quality (Evidence Intake):** are questions targeted, non-leading and answerable?

### Triage
- Agreement of Apply/Stretch/Skip with experienced human reviewers.
- Reason quality: does each verdict cite the right requirement?
- Calibration: do "Skip" verdicts correspond to hard requirements, not preference?

### Interview Fire Drill (Phase 5)
- Relevance and difficulty of questions, grader agreement with human graders.

### Systems
- Latency (p50/p95), validator rejection rate, queue time, error rate.
- Cost per active user per month.

## Human evaluation

- Blind side-by-side comparisons: Pramaan output versus the prompted baseline versus an unedited generic AI rewrite.
- Raters include at least a few recruiters or experienced engineers and several fresher users.
- Use a written rubric; record rater agreement.

## Release gates

| Gate | Requirement |
|---|---|
| Model go/no-go (Phase 2) | See [06](06-MODEL-TRAINING.md) section 8 |
| Beta release | Zero ledger violations in exported resumes in the test suite; parsing regression suite green; security controls required for beta in place ([11](11-SECURITY.md)) |
| Public launch | No open high/critical security findings; privacy sign-off; benchmark report published |
| Any model change | Full gold-set evaluation plus regression suite before deploy |

## Monitoring in production

- Track validator rejection rate per model version; alert on spikes.
- Sample outputs weekly for human review (only from users who opted in to quality review).
- User feedback buttons on every suggestion (useful / wrong / unsafe), with reasons.
- Drift checks: new resume styles, new JD patterns.

## Outcome measurement (honest, slow)

- Survey and (opt-in) tracker data on interviews and callbacks.
- Compare users who followed suggestions with a reasonable baseline, with clear caveats: self-selection, market conditions and many other factors affect outcomes. Report limitations.
- Never claim causation without a proper design.

## Benchmark publication

Publish a living benchmark page and repository folder with:
- dataset descriptions (synthetic or anonymised only),
- scripts to reproduce metrics,
- results per release, including failures,
- scorer and model versions.

## Contribution quality

Contributed data or labels must include provenance and consent, follow the labelling guide, and pass automated checks (schema, PII scan) before review.

# 01. Vision and Product

## One-line pitch

Pramaan is an evidence-first career copilot for Indian students and freshers: **prove every line of your resume, know which jobs are worth applying to, and prepare for the questions your resume invites.**

## The name

**Pramaan (प्रमाण)** means proof or evidence. It captures the product thesis and works as a tagline: **"Har line ka pramaan."**

| Alternative | Meaning | Note |
|---|---|---|
| Kasauti (कसौटी) | Touchstone that tests gold | Strong metaphor, common word |
| Saakshya (साक्ष्य) | Evidence, testimony | Close to the thesis, harder to spell |
| Sanad (सनद) | Certificate, proof | Short, overlaps other brands |
| Hunar (हुनर) | Skill, talent | Warm, extremely common |

**Before committing:** check IP India's trademark database, domains (.in, .ai, .com), social handles and app stores, and consult a trademark lawyer. A light web check found no resume product called Pramaan, but that is not proof none exists, and the word is used in other Indian contexts.

## The problem

Research across Reddit discussions, reviews and independent tests shows recurring frustrations:

1. **Scores feel like upsell bait.** Many free checkers show a number and lock the fixes.
2. **Nobody trusts the number.** People doubt that an ATS score predicts interviews; the "most resumes are auto-rejected" claim is a debunked marketing line.
3. **Tools are sometimes wrong.** One comparison saw a clean resume reported as unparsed, invented metrics, and side projects turned into jobs.
4. **AI rewriting makes resumes generic or false.** Output tends to be symmetrical, buzzword-heavy and sometimes inflated beyond what the candidate can defend.
5. **Freshers apply blindly.** Hundreds of applications, few callbacks, often to roles asking for experience they lack.
6. **Projects look like tutorial clones.** Reviewers want originality, readable code, a clear README and a deployed link.
7. **Skills lists are interview traps.** Anything on the resume can become a question.

**Core insight:** competitors optimise the *document*. The candidate's real problem is that the document is not backed by provable substance, and nobody helps them decide where applying is worth the effort.

## Target users

**Primary (v1):** final-year and recent-graduate CS/IT students and freshers in India targeting software, data and ML roles. Often Tier 2/3 colleges, limited or no internship, high anxiety, low willingness to pay.

Why start here:
- Project-driven resumes make GitHub verification possible.
- Pain is acute and visible in public communities.
- Competitors price for Western professionals, leaving room for a free, honest tool.

**Later:** non-tech freshers, career switchers, experienced professionals, college placement cells as institutional customers.

## Product principles

1. **Evidence over adjectives.** Every suggestion points to a line in the resume or a user-provided fact.
2. **Never fabricate.** The product cannot add a number, tool or achievement the user did not supply. A validator enforces this.
3. **Fixes are free.** Users always see what is wrong and how to fix it.
4. **No mystery score.** Scores are decomposed, versioned, reproducible and explained.
5. **Say "don't apply" when true.** The product is allowed to advise skipping a role.
6. **Private by default.** Resumes are personal data. Redact before any external call, delete on schedule.
7. **Honest about limits.** No guarantee of interviews or ATS results, ever.

## Competitive position

Many tools already offer ATS checks, keyword matching and AI bullet rewriting. The defensible difference is the *combination*:

| Area | Typical tools | Pramaan |
|---|---|---|
| Score | Single number, often gated | Decomposed, free, reproducible |
| Rewriting | Generates text, may invent facts | Built from a Fact Ledger, validated |
| Skills | Keyword counts | Proof depth per claim, risky-claim warnings |
| Projects | Ignored | GitHub verification and upgrade paths |
| JD matching | Keyword overlap | Realism triage including "Skip" |
| Interview prep | Generic banks | Questions from your own weakest claims |
| Context | Western defaults | India-first: freshers, Hinglish, campus flow |
| Model | Generic API | Own fine-tuned model, constrained and validated |

## Business model (hypotheses to test)

- **Free:** full analysis and every fix suggestion for one active resume; limited tailored exports per month.
- **Plus (student pricing):** more tailored exports, Fire Drill sessions, outcome analytics.
- **Institutions:** licences for college training and placement cells (cohort dashboards, anonymised insights).
- **Never:** selling user data, hiding fixes behind paywalls, ad-based scoring.

Validate pricing with at least 30 student interviews before building billing.

## Success metrics

- **Product:** time to first insight under 3 minutes; Evidence Intake completion rate; exports with zero placeholders.
- **Quality:** faithfulness (no invented facts) in exported resumes; parse accuracy; agreement with human reviewers.
- **Outcome (slow, honest):** users reporting interviews within 60 days versus their prior rate; fewer applications sent to "Skip" roles.

## Out of scope for v1

- Auto-applying to jobs
- Claiming to simulate any specific company's ATS
- Job board or recruiter-side tooling
- Non-English resumes beyond Hinglish phrasing help

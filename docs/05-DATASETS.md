# 05. Datasets

## The honest summary

Public Hugging Face resume and job-description datasets are **small** (typically thousands of rows), mostly English, mostly not Indian-fresher specific, and some contain real people's data of unclear consent. They are useful as seeds and for evaluating small extraction models. They are **not enough** to fine-tune a 7B to 8B model on the tasks Pramaan needs (evidence questions, ledger-grounded bullets, claim grading, triage reasons). Most of your training data will have to be **synthetic, generated and filtered by you**, plus a small hand-labelled gold set.

Always re-check each dataset's card, licence and provenance yourself before use; cards change and some are incomplete.

## Candidate Hugging Face datasets (found during research; verify before use)

| Dataset | What it is | Notes |
|---|---|---|
| `datasetmaster/resumes` | Merged real and synthetic resumes in normalised JSON (personal info, projects, technologies, impact) | Card lists MIT licence, English, 1K to 10K rows. Real portion was collected from "various CV submissions"; **consent and PII status unclear**, so treat as sensitive and check before training or redistributing |
| `ttxy/resume_ner` | Token-classification (NER) dataset for resumes | Tagged as BSD, 1K to 10K rows; suited to small extraction models |
| `jacob-hugging-face/job-descriptions` | Job descriptions | Used in public resume-matching projects; check licence and fields |
| Synthetic JD NER (`gmay29/ner_model_final` model card) | Model trained on ~20K synthetic internship/job description samples (SKILL, DISCIPLINE, COURSE, ROLE) | A model, not a dataset; shows the synthetic approach and its limit: its card says it is not designed for candidate resumes |

Outside Hugging Face, a commonly used Kaggle resume dataset exists; check its licence and provenance before use. If any dataset ships as pickle files, **do not unpickle untrusted files** ([11](11-SECURITY.md)); convert from a safe environment or use formats like JSON/Parquet.

## What you need that does not exist publicly

| Need | Why public data does not cover it | Plan |
|---|---|---|
| Indian fresher resumes (projects-heavy, Tier 2/3 colleges, campus style) | Public sets skew Western and experienced | Consented collection from students; synthetic generation seeded by real structure |
| Claim proof-depth labels (0 to 3) | No such labelling exists | Hand-label the gold set; use it to train and evaluate the classifier |
| Evidence-Intake dialogues (question → answer → ledger facts → bullet) | Does not exist | Generate synthetically from structured profiles, then filter |
| Ledger-grounded rewriting with refusals ("this number is not in the ledger") | Does not exist | Generate positives and adversarial negatives programmatically |
| Triage reasons (Apply / Stretch / Skip) | Does not exist | Rule-derived labels from JD requirements vs profile, reviewed by humans |
| Hinglish phrasing | Rare | Small curated set plus synthetic data; review by native speakers |
| Interview questions tied to resume claims | Generic banks only | Generate from claims; filter for specificity |

## Data pipeline

```
sources → licence + PII check → normalise to common JSON schema → de-duplicate
        → split (train / val / test, by person, never by row) → versioned release
```

1. **Licence check:** record licence, source and date per dataset in a manifest. Exclude anything with unclear rights for commercial use.
2. **PII handling:** detect and replace names, phones, emails, addresses and profile URLs with consistent fake values. Keep an unredacted copy only if consent allows, with restricted access.
3. **Normalise:** one schema for resumes and JDs (see [13](13-API-AND-DATA-MODEL.md)).
4. **De-duplicate:** near-duplicate resumes and JDs removed to avoid train/test leakage.
5. **Split by person/source**, not by row; the gold set is **never** trained on.
6. **Version:** each release gets a tag and a data card.

## Synthetic data generation

Goal: lots of varied examples with **known ground truth**, because you create the facts first.

1. **Generate structured profiles first** (the "truth"): skills with real context, projects, outcomes, numbers.
2. **Render** them as resumes in varied styles, quality levels and layouts (including messy ones).
3. **Derive labels from the truth:** proof-depth levels, ledger facts, which numbers are real.
4. **Create tasks** from the same truth:
   - question generation for weak claims
   - bullet drafting using only ledger facts
   - adversarial cases where a tempting number is missing from the ledger (target behaviour: placeholder or refusal)
   - triage verdicts from rules
5. **Filter:** run the validator and heuristics; discard outputs that fail; sample and read some by hand.
6. **Diversity:** vary branch (CSE, IT, ECE), college tier, project types, quality, Hinglish.

Risks: synthetic data teaches the model the generator's style and mistakes. Mitigate with human review of samples, diversity controls, and a gold set that contains **no synthetic items**.

## Gold set

- Target: **300 to 500** resumes, with real structure and varied quality, from consenting contributors.
- Labels: sections, claims, proof-depth levels, true facts, risky claims, JD triage verdicts for a subset.
- Two annotators on at least 20 percent for agreement measurement; written labelling guide.
- Stored separately with restricted access; never used in training.

## Consent and ethics

- Contributors explicitly opt in, are told what the data is used for, and can withdraw (data removed from future releases).
- Never train on user uploads from the product without separate, explicit opt-in ([12](12-PRIVACY-AND-COMPLIANCE.md)).
- Do not publish raw resumes. If you publish datasets, publish only synthetic or fully anonymised, consented data.

## General-ability retention

When fine-tuning, mix in a small slice of a permissively licensed general instruction dataset (verify its licence) so the model keeps general language ability and follows instructions outside the narrow task.

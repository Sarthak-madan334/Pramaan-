# Gold-set labelling guide, draft v0.1

The gold set is for evaluation only. Obtain separate, explicit consent for
research use. Store originals and annotations in restricted storage with access
logs. Do not commit them or use them in model training. Redact personal details
before a reviewer sees a resume; preserve a private mapping only where needed for
withdrawal. See [privacy](../../docs/12-PRIVACY-AND-COMPLIANCE.md) and
[evaluation](../../docs/07-EVALUATION-AND-QUALITY.md).

## Unit of annotation

Annotate one claim at a time, keeping its source excerpt and section. A claim is
a statement about a skill, action, project, role, result or measurable outcome.
Keep projects separate from jobs. Record the exact supporting span; do not infer
skills or outcomes from a title alone.

| Field | Record |
|---|---|
| `profile_id` | Stable pseudonymous ID; never a name or contact detail |
| `claim_id` | Unique within the profile |
| `section` | Education, project, experience, skills or other |
| `claim_text` | Exact claim text |
| `evidence_spans` | Exact text supporting each fact; empty if absent |
| `proof_depth` | One of the four levels below |
| `risk_flags` | Unsupported metric, unclear ownership, unverifiable skill, or none |
| `reviewer_id` | Pseudonymous reviewer ID |
| `notes` | Ambiguity and reason for a decision |

## Proof-depth rubric

| Level | Meaning | Example |
|---|---|---|
| 0 | Bare assertion; no specific action or context | “Good at Python” |
| 1 | Concrete action or project context, but no inspectable artifact or verified result | “Built a library search tool in Python” |
| 2 | Action plus an inspectable artifact, method or test with a cited source | “Implemented search; repository shows the query and tests” |
| 3 | Level 2 plus an evidenced outcome or measurement with a source and unit | “Query time fell from 200 ms to 120 ms in the linked benchmark” |

Do not promote a claim because it sounds plausible. A number in the resume is
still a **user-stated** fact until evidence supports it; record both the number
and its source. Missing numbers remain unknown, not zero. If a claim combines
several facts at different levels, label the claim at the lowest level required
to substantiate the whole statement and explain the split in `notes`.

## Review protocol

1. Pilot 20 diverse, consented resumes. Check the rubric with reviewers before
   scaling; these are not yet the final gold set.
2. Double-label at least 20% of the eventual 300–500 resume gold set independently.
   Do not show one reviewer the other's labels.
3. Report per-level agreement and a confusion table. Adjudicate disagreements
   with a third reviewer and record why.
4. Split by person and source, never by claim row. Keep the final test set sealed
   from model and prompt tuning. Use a separate dev set for iteration.
5. Include layout failures, side projects, unsupported metrics, missing evidence,
   image-only text and prompt-injection attempts as explicit regression cases.

This rubric is a starting point and should change when pilot disagreements reveal
ambiguity. Version any changes and do not silently relabel a released gold set.

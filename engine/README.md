# Phase 2B: Fact Ledger baseline

`grounded_bullet.py` is a deliberately limited deterministic baseline. It
requires a claim ID, evidence-referenced ledger facts and a plan selecting the
facts. It renders a fixed bullet and accepts only an exact match. Missing facts,
placeholders, foreign-claim facts and unsupported prose are rejected.

Run its tests from the repository root:

```bash
python -m unittest discover -s engine/tests -v
```

This does **not** parse resumes, establish that a cited evidence reference is
authentic, or validate arbitrary model prose. Those are separate Phase 2B tasks.
Until they exist, no free-form model output should be considered validated or
export-safe. The small test phrases are code fixtures, not a training dataset.

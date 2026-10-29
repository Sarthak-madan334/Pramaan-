# Phase 2A: real-data intake

Pramaan will train on real data that the project is permitted to use. There is
no synthetic generator or synthetic training data in this setup.

Before importing a dataset, record its source link, version, licence and any
permission terms. Check whether it contains personal information, what consent
covers, and whether the data may be used for training and evaluation. Keep raw
resumes in restricted storage, not in Git. The local `ml/data/private/` and
`ml/eval/gold/` paths are ignored by Git, but an ignore rule alone is not a
security control; use encrypted storage and access controls for real resumes.

The dataset-specific steps are:

1. Inspect the source's card, files and permitted uses.
2. Define normalization and PII handling for its actual format.
3. Split by person and source, rather than by row, to prevent leakage.
4. Hand-label a separate gold set using [the draft guide](LABELING-GUIDE.md).
5. Establish the prompted baseline and evaluator before fine-tuning.

Do not mix the gold set into train or dev. Do not load untrusted pickle files or
run dataset-provided scripts without review. See the project [dataset plan](../../docs/05-DATASETS.md)
and [security plan](../../docs/11-SECURITY.md).

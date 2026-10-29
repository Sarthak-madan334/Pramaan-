# Hugging Face source review — 2026-10-29

This is a preliminary review of the three sources proposed for Phase 2. It does
not independently establish that a dataset is safe or permitted to train on.
The project owner wants real data only and has stated that permission is
available. Record a full immutable Hugging Face revision for every run; `main`
is not a reproducible version.

| Source | What is available | Possible Pramaan use | Decision now |
|---|---|---|---|
| [`d4rk3r/resumes-raw-pdf`](https://huggingface.co/datasets/d4rk3r/resumes-raw-pdf) | 1,940 PDFs, with `pdf` and `label` fields; the card contains only an MIT tag and no provenance or consent description | Parser and layout testing after rights and PII review; it has no claim-level or grounded-writing targets | **Hold** |
| [`AzharAli05/Resume-Screening-Dataset`](https://huggingface.co/datasets/AzharAli05/Resume-Screening-Dataset) | 10,174 CSV rows with `Role`, `Resume`, `Decision`, `Reason_for_decision`, and `Job_Description`; card contains only an MIT tag | Potential triage research, but previewed resumes use sample-style names/contact details and some decision reasons appear disconnected from the JD | **Exclude from real-only training unless the author documents real provenance and label creation** |
| [`md-zain/resume-parser-dataset`](https://huggingface.co/datasets/md-zain/resume-parser-dataset) | 14,635 records with resume text and structured parsing targets; train/validation/test splits; source PDFs, extracted text and annotations | Best task match for **structured resume extraction**. It does not supply Pramaan's evidence questions or grounded bullet labels | **Selected for the first local extraction experiment under the owner's permission assurance; source-specific terms and real-data provenance remain to be verified** |

The `md-zain` [dataset card](https://huggingface.co/datasets/md-zain/resume-parser-dataset/blob/main/README.md)
says the corpus combines three upstream datasets, contains personal information,
and has **no blanket licence** for all sources. The preview contains names,
addresses, emails and phone numbers. Its stated purpose is research and
experimentation, and the card says it is not a ranking dataset. Treat its
provided split as provisional until duplicate people and overlap with other
sources are checked.

One upstream source, [`opensporks/resumes`](https://huggingface.co/datasets/opensporks/resumes),
states that its 2,400+ resume examples were scraped from LiveCareer. Another,
[`Mehyaar/Annotated_NER_PDF_Resumes`](https://huggingface.co/datasets/Mehyaar/Annotated_NER_PDF_Resumes),
describes 5,029 CV texts with IT-skill annotations. These descriptions do not
establish consent for Pramaan's commercial model training or prove all rows are
real applicants. The third upstream source is a Kaggle PDF collection whose
terms still need direct review.

The AzharAli05 preview looks generated, but the card does not say how the
records were created. That is an inference from the preview, not a verified
provenance finding. Because the owner requires real data, keep it excluded
unless the source author can clarify this point.

## Approval gates for any source

1. Record the full source revision, uploader, upstream origin, licence text and
   explicit permission for the intended training use. A Hub licence tag alone
   is insufficient evidence of consent from people named in resumes.
2. Review and redact personal information before creating any local training
   copy; keep raw files in restricted storage, outside Git and public model
   artifacts. Check withdrawal requirements where applicable.
3. Inspect a limited sample for real-versus-generated origin, label correctness,
   language, occupation and layout. Do not treat author-provided labels as
   ground truth without a manual audit.
4. De-duplicate by person/document across **all** approved sources before
   splitting. Reserve a separate, human-reviewed gold set. Do not train on it.
5. Map each approved source to one task: PDFs for parser tests, extraction pairs
   for parser training, and separately human-labelled claim/evidence pairs for
   Pramaan's grounded writing. Raw resumes do not provide SFT targets by
   themselves.

For the first local experiment, the pinned `md-zain` train and validation files
were downloaded and PII-reduced under the ignored `ml/data/private/` directory.
The test split was not downloaded. A local extraction-model experiment was
completed on the Intel XPU; its data, checkpoints and run outputs remain outside
Git. No resume data or model artifacts were added to this repository.

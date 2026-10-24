# 06. Model Training

This is Phase 2. The goal is a model of **meaningful size (7B to 8B class)** that does Pramaan's core generative tasks faithfully, plus small models for extraction and classification. Everything here is a plan; hyperparameters are starting points to be tuned against the evaluation set ([07](07-EVALUATION-AND-QUALITY.md)).

## 1. What gets trained

| Model | Task | Size class | Runs on |
|---|---|---|---|
| Extractor | Section, entity and claim extraction (token classification) | Small encoder (~100M to 400M) | CPU |
| Proof-depth classifier | Claim level 0 to 3 | Small encoder | CPU |
| JD extractor | Must-have / nice-to-have, years, seniority | Small encoder | CPU |
| Embeddings | Skill and JD semantic match | Small embedding model (use or lightly tune an existing one) | CPU |
| **Main LLM** | Evidence questions, ledger-grounded bullets, interview questions, answer grading, triage reasons | **7B to 8B class** (optionally a 12B to 14B variant later) | GPU |

## 2. Choosing the base model for the main LLM

Research (mid-2026 comparisons) points to a 7B to 14B dense model with 4-bit QLoRA as the practical sweet spot for specialist fine-tuning. Candidate bases to evaluate side by side:

| Candidate | Size | Licence (verify on the model card) | Why consider |
|---|---|---|---|
| Qwen3-8B | 8B | Apache 2.0 | Strong all-round and multilingual, large fine-tuning ecosystem |
| Ministral 8B (Mistral 3 family) | 8B | Apache 2.0 | Clean licence, strong instruction following |
| Gemma 4 (12B) | 12B | Apache 2.0 reported | Larger, strong quality; needs more memory |
| Llama 3.x 8B | 8B | Llama community licence (gated, usage terms) | Largest fine-tuning ecosystem; check licence terms |

**Recommendation:** run a short bake-off. Fine-tune each of two or three candidates on a small subset (a few thousand examples), evaluate on the gold set, then commit to one. Decide using faithfulness, Hinglish handling, latency after quantisation, and licence clarity, not benchmark headlines alone. Licence and model details change quickly; confirm on the model card on the day you decide.

**Why not bigger?** Larger models (30B and up) are costlier to train and serve and unnecessary when the task is narrow and a validator enforces faithfulness. Start at 7B to 8B; move up only if evaluation shows a clear gap.

## 3. Training stages for the main LLM

### Stage A: Supervised fine-tuning (SFT) with QLoRA

- **Data:** synthetic, ledger-grounded tasks from [05](05-DATASETS.md), plus a small slice of general instruction data.
- **Task formats:** every example has structured input (task, ledger facts, resume excerpt) and structured output (JSON).
- **Starting hyperparameters** (tune!): LoRA rank 16 to 64, alpha about 2x rank, dropout 0.05, target all attention and MLP projections; learning rate 1e-4 to 2e-4 with cosine schedule and warmup; 2 to 3 epochs; context length 2048 to 4096; effective batch via gradient accumulation; bf16 where supported.
- **Tooling:** Hugging Face Transformers, PEFT, TRL, bitsandbytes (4-bit); optional accelerators such as Unsloth or Axolotl if they support the chosen model.
- **Checkpointing:** save adapters often; log training and validation loss; hold out the validation set by person.

### Stage B: Faithfulness tuning

The main failure to eliminate is invented facts. Two complementary methods:

1. **Rejection sampling:** generate several candidates per prompt, keep those the validator accepts, fine-tune again on the accepted ones.
2. **Preference tuning (DPO-style):** pairs of (validator-accepted, validator-rejected) outputs for the same prompt, including adversarial prompts where a tempting number is missing. Target behaviour is to emit a `placeholder` or ask a question instead of inventing.

Track the validator rejection rate per checkpoint; it should fall steadily.

### Stage C: Behaviour checks

- Refusal and placeholder behaviour on adversarial cases.
- Prompt-injection resistance: resumes containing instructions like "ignore previous instructions" must not change behaviour ([11](11-SECURITY.md)).
- Hinglish prompts and outputs.
- Tone: specific, human, non-boilerplate (voice check metrics).

## 4. Training the small models

- Start from a pretrained encoder (for example a DeBERTa-class or multilingual model), fine-tune for token or sequence classification on the gold and synthetic data.
- These train on a single modest GPU or even CPU for small data; iterate quickly.
- Evaluate with per-label precision/recall, not accuracy alone.

## 5. Hardware and cost planning

| Item | Guidance |
|---|---|
| QLoRA on 7B to 8B | Fits on a single GPU in the ~24 GB class with 4-bit weights and gradient checkpointing; larger context or 12B+ needs more memory |
| Free/low-cost options | Notebook platforms (Colab, Kaggle) are fine for small-model work and short experiments, but session limits make long 8B runs risky |
| Rented GPUs | Per-hour cloud GPUs are the realistic path for full runs; budget for several experiment runs, not one |
| Inference | A 7B to 8B model at 4-bit needs on the order of 5 GB of weights; fast serving still wants a GPU |

Plan for **many small experiments** (data variants, hyperparameters, base-model bake-off) before one long final run. Write a budget and cap it before starting.

## 6. Experiment discipline

- Track every run: data version, code commit, base model, hyperparameters, seeds, metrics (use any experiment tracker).
- Never evaluate on training data; the gold set is untouched until final reports.
- Change one thing at a time when debugging.
- Keep the prompted-baseline score beside every report so progress is meaningful.

## 7. Compression and serving

1. **Merge** LoRA adapters into the base (or serve adapters separately).
2. **Quantise** (4-bit or 8-bit, using a method supported by the serving stack); re-run the full evaluation on the quantised model, because quantisation can change behaviour.
3. **Serve** behind the model service ([04](04-ARCHITECTURE.md)): GPU with batching for production; a smaller quantised variant on CPU as fallback.
4. **Load test:** measure time-to-first-token and total latency for realistic prompts; set queue and timeout limits.
5. **Optional distillation:** later, distil into a smaller 1B to 4B model to run cheaply on CPU for simple tasks.

Prefer the **safetensors** format for weights. Do not load pickled checkpoints from untrusted sources and keep `trust_remote_code` off unless you have reviewed the code.

## 8. Go/no-go gate

Ship the own model for a task only if on the held-out gold set it:

- produces zero ledger violations after the validator (and a low raw rejection rate),
- matches or beats the prompted baseline on task quality, or equals it at clearly lower cost/latency,
- meets latency targets on the chosen hardware,
- passes the injection and refusal checks.

Otherwise keep the prompted baseline for that task (Groq or another hosted model under the same validator) and keep iterating. The product must not depend on a model that has not passed this gate.

## 9. Model and data documentation

Publish for each release: a **model card** (intended use, limits, training data summary, evaluation results, known failures) and a **data card** (sources, licences, PII handling, splits). Record the base model's licence obligations and attribution requirements.

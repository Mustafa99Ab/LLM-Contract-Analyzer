# LLM-Based Vulnerability Detection for Solana Smart Contracts: Fine-Tuning and RAG

> **Author:** Mustafa Abuzaraiba
>
> **Supervisors:** Prof. Christian Esposito , Dr. Biagio Boi
>
> **University:** University of Salerno — Academic Year 2025/2026

## Abstract

This repository contains the source code, datasets, and evaluation pipeline developed for the IEEE BCCA 2025 paper. The project proposes a hybrid framework (**Fine-Tuning + RAG**) for automated vulnerability detection in smart contracts written in **Rust** (Solana).

The approach replicates and adapts the methodology proposed by Tortora (2025) for Algorand/PyTeal, applying it to the Solana/Rust ecosystem. Three LLMs are evaluated — **LLaMA 3.1-8B-Instruct**, **Qwen2.5-Coder-32B-Instruct**, and **Qwen3-32B** — each adapted via *QLoRA* and *Chain-of-Thought* training, combined with a *Retrieval-Augmented Generation (RAG)* pipeline for dynamic vulnerability context injection.

The framework is evaluated across 4 configurations per model to measure the impact of Fine-Tuning and RAG on detection performance (Precision, Recall, F1-Score, Accuracy).

## System Architecture

The system consists of three main phases:

1. **Fine-Tuning:** Domain adaptation using QLoRA to learn Solana/Rust vulnerability patterns and Chain-of-Thought reasoning (`<think>...</think>`).
2. **RAG Pipeline:** Retrieval of similar vulnerable contracts from a vector knowledge base to provide few-shot examples and reduce hallucinations.
3. **Inference & Evaluation:** Contract audit, structured output parsing, and automated metric computation (Precision, Recall, F1, Accuracy).

## Model Comparison Matrix

The three models form a comparison matrix that isolates key effects:

|  | Small (8B) | Large (32B) |
|---|-----------|-------------|
| **General-purpose** | LLaMA 3.1-8B | Qwen3-32B |
| **Code-specialized** | — | Qwen2.5-Coder-32B |

1. **Size effect:** LLaMA 8B vs Qwen3 32B (both general-purpose)
2. **Code specialization effect:** Qwen3 32B vs Qwen2.5-Coder 32B (same size, different pre-training)
3. **Cross-platform comparison:** Tortora (2025) used Qwen3-32B for Algorand — enabling direct Algorand vs Solana comparison

## Vulnerability Taxonomy

Based on the OWASP Top 10 mapping by Boi & Esposito (2025):

| Code | Vulnerability | Solana/Rust Manifestation |
|------|--------------|--------------------------|
| V1   | Missing Key Check        | Missing signer/owner verification |
| V4   | Type Confusion           | Missing account type/discriminator validation |
| V5   | CPI Reentrancy           | State update after cross-program invocation |
| V6   | Unchecked External Calls | CPI results silently discarded (`let _ =`) |
| V8   | Integer Overflow         | Unchecked arithmetic (`+` instead of `checked_add`) |
| V9   | Bump Seed                | `create_program_address` without canonical bump |
| V10  | Denial of Service        | Missing re-initialization guards, stale data |

## Repository Structure

```
├── data/
│   ├── training/                        # CoT training dataset
│   │   ├── dataset_think_format.jsonl   # 226 training samples (Prompt + CoT + Verdict)
│   │   └── validation_dataset.jsonl     # 22 validation samples
│   ├── test_set/                        # 59 test contracts (code only, no labels)
│   │   └── solana_01.json ... solana_59.json
│   ├── knowledge_base/                  # RAG reference data
│   │   ├── vulnerability_info.json      # 7 vulnerability profiles
│   │   └── rag_contracts.jsonl          # Indexed vulnerable contracts
│   └── dataset_construction/            # Original dataset (285 samples, 15 contracts)
│       ├── dataset_batch1/ ... dataset_batch11/
│       └── final DS/
│           └── dataset_final.json       # Merged dataset (285 samples)
│
├── notebooks/
│   ├── llama-3.1-8b/
│   │   ├── solana_finetuning.ipynb      # QLoRA fine-tuning on Kaggle T4
│   │   └── solana_evaluation.ipynb      # 4-configuration evaluation
│   ├── qwen2.5-coder-32b/
│   │   ├── qwen-finetuning.ipynb        # QLoRA fine-tuning on RTX A6000
│   │   └── qwen-evaluation.ipynb        # 4-configuration evaluation
│   └── qwen3-32b/
│       ├── qwen3-finetuning.ipynb       # QLoRA fine-tuning on RTX A6000
│       └── qwen3-evaluation.ipynb       # 4-configuration evaluation
│
├── src/
│   ├── rag/
│   │   ├── generate_embeddings.py       # Encode KB contracts into vectors
│   │   └── rag.py                       # Similarity search + dynamic checklist
│   ├── finetuning/
│   │   ├── train_qlora.py               # Main training script (Kaggle T4)
│   │   └── custom_chat_template.jinja   # Chat template with <think>/<final> tags
│   └── evaluation/
│       ├── run_benchmark_no_rag.py      # Benchmark without RAG
│       ├── run_benchmark_rag.py         # Benchmark with RAG
│       ├── metrics.py                   # Precision, Recall, F1 computation
│       └── utils/                       # Prompts, parser, logging
│
├── results/
│   ├── llama-3.1-8b/                    # Results for LLaMA 3.1-8B
│   ├── qwen2.5-coder-32b/              # Results for Qwen2.5-Coder-32B
│   └── qwen3-32b/                      # Results for Qwen3-32B
│
└── requirements.txt
```

## Dataset

- **285 samples** across 15 real Solana SPL contracts
- **7 vulnerability types** (V1, V4, V5, V6, V8, V9, V10)
- **Balanced**: ~50/50 SAFE/VULNERABLE per category
- **Source**: Real deployed SPL contracts from solana-labs GitHub
- **Methodology**: Extract secure code as SAFE, systematically remove security checks to create VULNERABLE variants
- **Training split**: 226 train / 22 validation / 59 test

## Models and Training

All three models share identical QLoRA hyperparameters for fair comparison:

| Parameter | Value |
|-----------|-------|
| Quantization | 4-bit (NF4) via QLoRA |
| LoRA Rank (r) | 64 |
| LoRA Alpha | 128 |
| Target Modules | All linear layers (Attention + MLP) |
| Epochs | 3 |
| Learning Rate | 5e-5 (cosine decay) |
| Effective Batch Size | 8 (1 per device × 8 accumulation) |
| Max Sequence Length | 2048 tokens |
| Framework | Unsloth + trl |

| Model | Type | Parameters | Hardware | Training Time | Final Train Loss | Final Val Loss |
|-------|------|-----------|----------|--------------|-----------------|----------------|
| LLaMA 3.1-8B-Instruct | General-purpose | 8B | Kaggle T4 (16GB) | ~37 min | 0.472 | — |
| Qwen2.5-Coder-32B-Instruct | Code-specialized | 32B | RTX A6000 (48GB) | 29.9 min | 0.173 | 0.170 |
| Qwen3-32B | General-purpose | 32B | RTX A6000 (48GB) | 29.9 min | 0.165 | 0.157 |

### Evaluation Timing

| Configuration | LLaMA 3.1-8B | Qwen2.5-Coder-32B | Qwen3-32B |
|--------------|-------------|-------------------|-----------|
| Base (no RAG) | ~25 min | 49.9 min | 19.4 min |
| Base + RAG | ~55 min | 51.2 min | 51.6 min |
| FT (no RAG) | ~12 min | 21.0 min | 8.1 min |
| FT + RAG | ~35 min | 51.5 min | 28.0 min |

> LLaMA 3.1-8B was evaluated on a Kaggle T4 GPU (16GB VRAM). Qwen models were evaluated on an NVIDIA RTX A6000 (48GB VRAM).


### Evaluation Timing

| Configuration | LLaMA 3.1-8B | Qwen2.5-Coder-32B | Qwen3-32B |
|--------------|-------------|-------------------|-----------|
| Base (no RAG) + Base + RAG | 191.6 min | 101.1 min | 71.0 min |
| FT (no RAG) + FT + RAG | 49.8 min | 72.5 min | 36.1 min |
| **Total** | **241.4 min** | **173.6 min** | **107.1 min** |

> LLaMA 3.1-8B was evaluated on a Kaggle T4 GPU (16GB VRAM). Qwen models were evaluated on an NVIDIA RTX A6000 (48GB VRAM). LLaMA timings are reported as combined pairs because both configurations within each pair were executed in a single notebook cell.

## Evaluation Configurations

Each model is evaluated across 4 configurations on 59 unseen Solana contracts:

| # | Configuration | Description |
|---|--------------|-------------|
| 1 | Base (no RAG) | Baseline: unmodified model, direct prompting |
| 2 | Base + RAG    | Base model with retrieval-augmented context |
| 3 | FT (no RAG)   | Fine-tuned model, direct prompting |
| 4 | FT + RAG      | Fine-tuned model with RAG context |

## Results

### Per-Model Results

| Configuration | LLaMA 3.1-8B F1 | Qwen2.5-Coder-32B F1 | Qwen3-32B F1 |
|--------------|-----------------|----------------------|--------------|
| Base (no RAG) | 0.085 | 0.291 | 0.237 |
| Base + RAG | 0.193 | 0.336 | 0.167 |
| **FT (no RAG)** | **0.327** | **0.514** | **0.291** |
| FT + RAG | 0.319 | 0.272 | 0.279 |

### Cross-Model Comparison (Best Config: FT no RAG)

| Metric | LLaMA 3.1-8B | Qwen2.5-Coder-32B | Qwen3-32B |
|--------|-------------|-------------------|-----------|
| Accuracy  | 0.507 | 0.471 | 0.451 |
| Precision | 0.346 | 0.422 | 0.308 |
| Recall    | 0.310 | 0.655 | 0.276 |
| **F1-Score** | **0.327** | **0.514** | **0.291** |

### Key Findings

1. **Fine-tuning is essential for all models.** F1 improves by +285% (LLaMA), +77% (Qwen2.5-Coder), and +23% (Qwen3).

2. **Code specialization matters more than model size.** Qwen2.5-Coder-32B outperforms Qwen3-32B at the same parameter count (F1: 0.514 vs 0.291), confirming that code-specific pre-training provides a stronger foundation.

3. **RAG helps base models but hurts fine-tuned models.** Consistent across all three models — fine-tuned models have already internalized vulnerability patterns.

4. **Model size alone does not guarantee better results.** LLaMA 3.1-8B (8B) outperforms Qwen3-32B (32B) on F1 (0.327 vs 0.291), suggesting that fine-tuning effectiveness varies by architecture.

5. **Qwen2.5-Coder achieves the highest recall.** After fine-tuning, its recall reaches 0.655 — more than double any other model — meaning it catches far more real vulnerabilities.

Full per-model results, charts, and detailed per-contract predictions are available in `results/`.

## Trained Models

| Base Model | Fine-Tuned Adapter |
|-----------|-------------------|
| LLaMA 3.1-8B-Instruct | [Mustafa99Hafed/LLaMA-3.1-8B-Solana-Audit](https://huggingface.co/Mustafa99Hafed/LLaMA-3.1-8B-Solana-Audit) |
| Qwen2.5-Coder-32B-Instruct | Saved locally on server |
| Qwen3-32B | Saved locally on server |

### Loading the LLaMA adapter

```python
from unsloth import FastLanguageModel

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="Mustafa99Hafed/LLaMA-3.1-8B-Solana-Audit",
    max_seq_length=2048,
    load_in_4bit=True,
)
```

## References

- Boi, B. & Esposito, C. (2025). *Prompt Engineering vs. Fine-Tuning for LLM-Based Vulnerability Detection in Solana and Algorand Smart Contracts*. IEEE BCCA 2025.
- Tortora, N. (2025). *LLM-Based Vulnerability Detection for Smart Contracts: Fine-Tuning and RAG*. Master's Thesis, University of Salerno. [GitHub](https://github.com/NickTor99/llm_based_vulnerability_detection_algorand)

## License

This project is part of academic research at the University of Salerno.

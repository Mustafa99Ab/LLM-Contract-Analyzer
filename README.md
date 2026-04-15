# LLM-Based Vulnerability Detection for Solana Smart Contracts: Fine-Tuning and RAG

> **IEEE BCCA 2025 Paper**
>
> **Author:** Mustafa Hafed
>
> **Supervisors:** Prof. Biagio Boi, Prof. Christian Esposito
>
> **University:** University of Salerno — Academic Year 2025/2026

## Abstract

This repository contains the source code, datasets, and evaluation pipeline developed for the IEEE BCCA 2025 paper. The project proposes a hybrid framework (**Fine-Tuning + RAG**) for automated vulnerability detection in smart contracts written in **Rust** (Solana).

The approach replicates and adapts the methodology proposed by Tortora (2025) for Algorand/PyTeal, applying it to the Solana/Rust ecosystem. The system uses **LLaMA 3.1-8B-Instruct** adapted via *QLoRA* and *Chain-of-Thought* training, combined with a *Retrieval-Augmented Generation (RAG)* pipeline for dynamic vulnerability context injection.

The framework is evaluated across 6 configurations to measure the impact of Fine-Tuning and RAG on detection performance (Precision, Recall, F1-Score).

## System Architecture

The system consists of three main phases:

1. **Fine-Tuning:** Domain adaptation of LLaMA 3.1-8B using QLoRA to learn Solana/Rust vulnerability patterns and Chain-of-Thought reasoning (`<think>...</think>`).
2. **RAG Pipeline:** Retrieval of similar vulnerable contracts from a vector knowledge base to provide few-shot examples and reduce hallucinations.
3. **Inference & Evaluation:** Contract audit, structured output parsing, and automated metric computation (Precision, Recall, F1).

## Vulnerability Taxonomy

Based on the OWASP Top 10 mapping by Boi & Esposito (2025):

| Code | Vulnerability | Solana/Rust Manifestation |
|------|--------------|--------------------------|
| V1 | Missing Key Check | Missing signer/owner verification |
| V4 | Type Confusion | Missing account type/discriminator validation |
| V5 | CPI Reentrancy | State update after cross-program invocation |
| V6 | Unchecked External Calls | CPI results silently discarded (`let _ =`) |
| V8 | Integer Overflow | Unchecked arithmetic (`+` instead of `checked_add`) |
| V9 | Bump Seed | `create_program_address` without canonical bump |
| V10 | Denial of Service | Missing re-initialization guards, stale data |

## Repository Structure

```
├── data/
│   ├── training/                        # CoT training dataset
│   │   ├── dataset_think_format.jsonl   # 226 training samples (Prompt + CoT + Verdict)
│   │   └── validation_dataset.jsonl     # 22 validation samples
│   ├── test_set/                        # 59 test contracts (code only, no labels)
│   │   └── solana_01.json ... solana_59.json
│   └── knowledge_base/                  # RAG reference data
│       ├── vulnerability_info.json      # 7 vulnerability profiles
│       └── rag_contracts.jsonl          # 37 indexed vulnerable contracts
│
├── src/
│   ├── rag/                             # RAG pipeline modules
│   │   ├── generate_embeddings.py       # Encode KB contracts into vectors
│   │   └── rag.py                       # Similarity search + dynamic checklist
│   ├── finetuning/                      # QLoRA training scripts
│   │   ├── train_qlora.py              # Main training script (Kaggle T4)
│   │   └── custom_chat_template.jinja   # Chat template with <think>/<final> tags
│   └── evaluation/                      # Testing and metrics
│       ├── run_benchmark_no_rag.py      # Benchmark without RAG
│       ├── run_benchmark_rag.py         # Benchmark with RAG
│       ├── metrics.py                   # Precision, Recall, F1 computation
│       └── utils/                       # Prompts, parser, logging
│
├── dataset_construction/                # Original dataset (285 samples, 15 contracts)
│   └── ...                              # Batch files, raw contracts, documentation
│
├── results/                             # Evaluation outputs (populated after testing)
│
└── requirements.txt
```

## Dataset

- **285 samples** across 15 real Solana SPL contracts
- **7 vulnerability types** (V1, V4, V5, V6, V8, V9, V10)
- **Balanced**: ~50/50 SAFE/VULNERABLE per category
- **Source**: Real deployed SPL contracts from solana-labs GitHub
- **Methodology**: Extract secure code as SAFE, systematically remove security checks to create VULNERABLE variants

## Model and Training

| Parameter | Value |
|-----------|-------|
| Base Model | LLaMA 3.1-8B-Instruct |
| Quantization | 4-bit (NF4) via QLoRA |
| LoRA Rank (r) | 64 |
| LoRA Alpha | 128 |
| Target Modules | All linear layers (Attention + MLP) |
| Epochs | 3 |
| Learning Rate | 5e-5 (cosine decay) |
| Effective Batch Size | 8 (1 per device x 8 accumulation) |
| Max Sequence Length | 2048 tokens |
| Framework | Unsloth + trl |
| Hardware | Kaggle T4 GPU (16GB VRAM) |

## Evaluation Configurations

| # | Configuration | Description |
|---|--------------|-------------|
| 1 | LLaMA-Base (no RAG) | Baseline: unmodified model, direct prompting |
| 2 | LLaMA-Base + RAG | Base model with retrieval-augmented context |
| 3 | LLaMA-FT (no RAG) | Fine-tuned model, direct prompting |
| 4 | LLaMA-FT + RAG | Fine-tuned model with RAG (best expected) |

## References

- Boi, B. & Esposito, C. (2025). *Prompt Engineering vs. Fine-Tuning for LLM-Based Vulnerability Detection in Solana and Algorand Smart Contracts*. IEEE BCCA 2025.
- Tortora, N. (2025). *LLM-Based Vulnerability Detection for Smart Contracts: Fine-Tuning and RAG*. Master's Thesis, University of Salerno. [GitHub](https://github.com/NickTor99/llm_based_vulnerability_detection_algorand)

## License

This project is part of academic research at the University of Salerno.

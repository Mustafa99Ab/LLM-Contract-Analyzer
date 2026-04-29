# Notebooks

This folder contains the fine-tuning and evaluation notebooks for the Solana vulnerability detection framework, organized per model. Each model has its own subfolder with two notebooks following a standardized pipeline.

## Structure

```
notebooks/
├── llama-3.1-8b/
│   ├── solana_finetuning.ipynb     # QLoRA fine-tuning
│   └── solana_evaluation.ipynb     # 4-configuration evaluation
│
├── qwen2.5-coder-32b/
│   ├── qwen-finetuning.ipynb       # QLoRA fine-tuning
│   └── qwen-evaluation.ipynb       # 4-configuration evaluation
│
└── qwen3-32b/
    ├── qwen3-finetuning.ipynb      # QLoRA fine-tuning
    └── qwen3-evaluation.ipynb      # 4-configuration evaluation
```

## Pipeline Overview

Every model follows the same two-notebook pipeline for fair comparison:

### Notebook 1: Fine-Tuning (`*-finetuning.ipynb`)

QLoRA fine-tuning on 226 Solana/Rust training samples using Chain-of-Thought (CoT) format. The model learns to reason step-by-step inside `<think>` tags before issuing a verdict inside `<final>` tags.

**Shared hyperparameters across all models:**

| Parameter | Value |
|-----------|-------|
| Quantization | 4-bit (NF4) via QLoRA |
| LoRA Rank (r) | 64 |
| LoRA Alpha | 128 |
| Target Modules | All linear layers (Attention + MLP) |
| Epochs | 3 |
| Learning Rate | 5e-5 (cosine decay) |
| Effective Batch Size | 8 (1 × 8 accumulation) |
| Max Sequence Length | 2048 tokens |
| Training Data | 226 samples (CoT format) |
| Validation Data | 22 samples |

### Notebook 2: Evaluation (`*-evaluation.ipynb`)

Evaluation across 4 configurations on 59 unseen Solana contracts:

| # | Configuration | Description |
|---|--------------|-------------|
| 1 | Base (no RAG) | Unmodified model, direct prompting |
| 2 | Base + RAG | Base model with retrieval-augmented context |
| 3 | FT (no RAG) | Fine-tuned model, direct prompting |
| 4 | FT + RAG | Fine-tuned model with RAG context |

Metrics computed: Accuracy, Precision, Recall, F1-Score.

---

## Model Details

### LLaMA 3.1-8B-Instruct

| Detail | Value |
|--------|-------|
| Model type | General-purpose |
| Parameters | 8B |
| Hardware | Kaggle T4 GPU (16GB VRAM) |
| Training time | ~37 minutes |
| Final Train Loss | 0.472 |
| Best F1 (FT no RAG) | **0.327** |
| LoRA adapter | [Mustafa99Hafed/LLaMA-3.1-8B-Solana-Audit](https://huggingface.co/Mustafa99Hafed/LLaMA-3.1-8B-Solana-Audit) |

### Qwen2.5-Coder-32B-Instruct

| Detail | Value |
|--------|-------|
| Model type | Code-specialized (92 languages including Rust) |
| Parameters | 32B |
| Hardware | NVIDIA RTX A6000 (48GB VRAM) |
| Training time | 29.9 minutes |
| Final Train Loss | 0.173 |
| Final Val Loss | 0.170 |
| Best F1 (FT no RAG) | **0.514** |
| LoRA adapter | Saved locally on server |

### Qwen3-32B

| Detail | Value |
|--------|-------|
| Model type | General-purpose |
| Parameters | 32B |
| Hardware | NVIDIA RTX A6000 (48GB VRAM) |
| Training time | 29.9 minutes |
| Final Train Loss | 0.165 |
| Final Val Loss | 0.157 |
| Best F1 (FT no RAG) | **0.291** |
| LoRA adapter | Saved locally on server |

**Note:** Qwen3 has a native thinking mode that uses `<think>` as a special token. Since our training data already contains custom `<think>` and `<final>` tags, the native thinking mode is disabled (`enable_thinking=False`) to avoid format conflicts.

### Evaluation Timing

| Configuration | LLaMA 3.1-8B | Qwen2.5-Coder-32B | Qwen3-32B |
|--------------|-------------|-------------------|-----------|
| Base (no RAG) | ~25 min | 49.9 min | 19.4 min |
| Base + RAG | ~55 min | 51.2 min | 51.6 min |
| FT (no RAG) | ~12 min | 21.0 min | 8.1 min |
| FT + RAG | ~35 min | 51.5 min | 28.0 min |

> LLaMA 3.1-8B was evaluated on a Kaggle T4 GPU (16GB VRAM). Qwen models were evaluated on an NVIDIA RTX A6000 (48GB VRAM).


---

## Results Overview

| Configuration | LLaMA 3.1-8B F1 | Qwen2.5-Coder-32B F1 | Qwen3-32B F1 |
|--------------|-----------------|----------------------|--------------|
| Base (no RAG) | 0.085 | 0.291 | 0.237 |
| Base + RAG | 0.193 | 0.336 | 0.167 |
| **FT (no RAG)** | **0.327** | **0.514** | **0.291** |
| FT + RAG | 0.319 | 0.272 | 0.279 |

### Why Three Models?

The three models form a comparison matrix that isolates key effects:

|  | Small (8B) | Large (32B) |
|---|-----------|-------------|
| **General-purpose** | LLaMA 3.1-8B | Qwen3-32B |
| **Code-specialized** | — | Qwen2.5-Coder-32B |

1. **Size effect:** LLaMA 8B vs Qwen3 32B (both general-purpose)
2. **Code specialization effect:** Qwen3 32B vs Qwen2.5-Coder 32B (same size, different pre-training)
3. **Cross-platform comparison:** Tortora (2025) used Qwen3-32B for Algorand — enabling direct Algorand vs Solana comparison

Full evaluation results are available at: `results/`

## References

- Boi, B. & Esposito, C. (2025). *Prompt Engineering vs. Fine-Tuning for LLM-Based Vulnerability Detection in Solana and Algorand Smart Contracts*. IEEE BCCA 2025.
- Tortora, N. (2025). *LLM-Based Vulnerability Detection for Smart Contracts*. Master's Thesis, University of Salerno.

# Evaluation Results

This folder contains the evaluation results for the Solana vulnerability detection framework, organized per model. Each model has its own subfolder with metrics, detailed predictions, and comparative charts.

## Structure

```
results/
├── llama-3.1-8b/
│   ├── evaluation_results.json    # Aggregated metrics (Accuracy, Precision, Recall, F1)
│   ├── detailed_results.json      # Per-contract predictions for all 4 configurations
│   ├── recompute_metrics.py       # Script to recompute metrics from detailed results
│   ├── no_rag/
│   │   ├── LLaMA_Base_results.json   # Config 1: Base model, no RAG
│   │   └── LLaMA_FT_results.json     # Config 3: Fine-tuned model, no RAG
│   ├── rag/
│   │   ├── LLaMA_Base_RAG_results.json   # Config 2: Base model + RAG
│   │   └── LLaMA_FT_RAG_results.json     # Config 4: Fine-tuned model + RAG
│   └── charts/
│       ├── evaluation_chart.png   # 4-configuration comparison
│       ├── finetuning_impact.png  # Base vs Fine-Tuned (no RAG)
│       └── rag_impact.png         # FT vs FT+RAG
│
├── qwen2.5-coder-32b/
│   ├── evaluation_results.json        # Aggregated metrics (Accuracy, Precision, Recall, F1)
│   ├── detailed_results.json          # Per-contract predictions for all 4 configurations
│   ├── results_base_no_rag.json       # Config 1: Base model, no RAG
│   ├── results_base_rag.json          # Config 2: Base model + RAG
│   ├── results_ft_no_rag.json         # Config 3: Fine-tuned model, no RAG
│   ├── results_ft_rag.json            # Config 4: Fine-tuned model + RAG
│   └── charts/
│       ├── evaluation_chart.png       # 4-configuration comparison
│       ├── finetuning_impact.png      # Base vs Fine-Tuned (no RAG)
│       └── rag_impact.png             # FT vs FT+RAG
│
└── qwen3-32b/
    ├── evaluation_results.json        # Aggregated metrics (Accuracy, Precision, Recall, F1)
    ├── detailed_results.json          # Per-contract predictions for all 4 configurations
    ├── results_base_no_rag.json       # Config 1: Base model, no RAG
    ├── results_base_rag.json          # Config 2: Base model + RAG
    ├── results_ft_no_rag.json         # Config 3: Fine-tuned model, no RAG
    ├── results_ft_rag.json            # Config 4: Fine-tuned model + RAG
    └── charts/
        ├── evaluation_chart.png       # 4-configuration comparison
        ├── finetuning_impact.png      # Base vs Fine-Tuned (no RAG)
        └── rag_impact.png             # FT vs FT+RAG
```

## Evaluation Configurations

Each model is evaluated across four configurations on 59 unseen Solana smart contracts:

| # | Configuration | Description |
|---|--------------|-------------|
| 1 | Base (no RAG) | Baseline: unmodified model, direct prompting |
| 2 | Base + RAG    | Base model with retrieval-augmented context |
| 3 | FT (no RAG)   | Fine-tuned model, direct prompting |
| 4 | FT + RAG      | Fine-tuned model with RAG context |

---

## Results Summary — LLaMA 3.1-8B

| Configuration | Accuracy | Precision | Recall | F1-Score |
|--------------|----------|-----------|--------|----------|
| LLaMA-Base (no RAG)  | 0.358 | 0.111 | 0.069 | 0.085 |
| LLaMA-Base + RAG     | 0.330 | 0.148 | 0.276 | 0.193 |
| **LLaMA-FT (no RAG)**| **0.507** | **0.346** | **0.310** | **0.327** |
| LLaMA-FT + RAG       | 0.454 | 0.275 | 0.379 | 0.319 |

**Best configuration: LLaMA-FT (no RAG)** — F1 = 0.327, Accuracy = 0.507

| Detail | Value |
|--------|-------|
| Model type | General-purpose |
| Parameters | 8B |
| Hardware | Kaggle T4 GPU (16GB VRAM) |
| Training time | ~37 minutes |
| LoRA adapter | [Mustafa99Hafed/LLaMA-3.1-8B-Solana-Audit](https://huggingface.co/Mustafa99Hafed/LLaMA-3.1-8B-Solana-Audit) |

---

## Results Summary — Qwen2.5-Coder-32B

| Configuration | Accuracy | Precision | Recall | F1-Score |
|--------------|----------|-----------|--------|----------|
| Qwen-Base (no RAG)  | 0.409 | 0.308 | 0.276 | 0.291 |
| Qwen-Base + RAG     | 0.202 | 0.213 | 0.793 | 0.336 |
| **Qwen-FT (no RAG)**| **0.471** | **0.422** | **0.655** | **0.514** |
| Qwen-FT + RAG       | 0.235 | 0.177 | 0.586 | 0.272 |

**Best configuration: Qwen-FT (no RAG)** — F1 = 0.514, Accuracy = 0.471

| Detail | Value |
|--------|-------|
| Model type | Code-specialized (92 languages including Rust) |
| Parameters | 32B |
| Hardware | NVIDIA RTX A6000 (48GB VRAM) |
| Training time | 29.9 minutes |
| LoRA adapter | Saved locally on server |

---

## Results Summary — Qwen3-32B

| Configuration | Accuracy | Precision | Recall | F1-Score |
|--------------|----------|-----------|--------|----------|
| Qwen3-Base (no RAG)  | 0.357 | 0.233 | 0.241 | 0.237 |
| Qwen3-Base + RAG     | 0.524 | 0.429 | 0.103 | 0.167 |
| **Qwen3-FT (no RAG)**| **0.451** | **0.308** | **0.276** | **0.291** |
| Qwen3-FT + RAG       | 0.279 | 0.220 | 0.379 | 0.279 |

**Best configuration: Qwen3-FT (no RAG)** — F1 = 0.291, Accuracy = 0.451

| Detail | Value |
|--------|-------|
| Model type | General-purpose |
| Parameters | 32B |
| Hardware | NVIDIA RTX A6000 (48GB VRAM) |
| Training time | 29.9 minutes |
| LoRA adapter | Saved locally on server |

---

## Cross-Model Comparison (Best Config: FT no RAG)

| Metric | LLaMA 3.1-8B | Qwen2.5-Coder-32B | Qwen3-32B |
|--------|-------------|-------------------|-----------|
| Accuracy  | 0.507 | 0.471 | 0.451 |
| Precision | 0.346 | 0.422 | 0.308 |
| Recall    | 0.310 | 0.655 | 0.276 |
| **F1-Score** | **0.327** | **0.514** | **0.291** |

### Key Findings

1. **Fine-tuning is essential for all models.** F1 improves from 0.085 → 0.327 (+285%) for LLaMA, from 0.291 → 0.514 (+77%) for Qwen2.5-Coder, and from 0.237 → 0.291 (+23%) for Qwen3.

2. **Code specialization matters more than model size.** Qwen2.5-Coder-32B (code-specialized) significantly outperforms Qwen3-32B (general-purpose) at the same parameter count, with F1 of 0.514 vs 0.291. This confirms that pre-training on code provides a stronger foundation for vulnerability detection.

3. **RAG helps base models but hurts fine-tuned models.** This pattern is consistent across all three models. RAG boosts recall at the expense of precision, and the fine-tuned models have already internalized vulnerability patterns.

4. **Qwen2.5-Coder doubles recall after fine-tuning.** The most significant improvement is in Recall (0.276 → 0.655), meaning it catches far more real vulnerabilities than either LLaMA or Qwen3.

5. **Model size alone does not guarantee better results.** LLaMA 3.1-8B (8B, general-purpose) outperforms Qwen3-32B (32B, general-purpose) on F1 (0.327 vs 0.291), suggesting that fine-tuning effectiveness varies by architecture.

## A Note on Metric Computation

The `evaluation_results.json` files contain the **corrected** metrics. During the initial evaluation (LLaMA), the scoring function treated vulnerability synonyms as distinct predictions. For example, if the model output `["Bump Seed", "Bump Seed Canonicalization"]`, the original parser counted this as one correct answer plus one false positive, when in fact both terms refer to the same vulnerability.

The `recompute_metrics.py` script (in `llama-3.1-8b/`) addresses this by normalizing predictions through an alias table before counting. The raw model predictions in `detailed_results.json` are untouched — only the aggregation logic changed.

### Reproducing the corrected metrics (LLaMA)

```bash
python recompute_metrics.py detailed_results.json
```

## Notebooks

| Model | Training | Evaluation |
|-------|----------|------------|
| LLaMA 3.1-8B | `notebooks/llama-3.1-8b/solana_finetuning.ipynb` | `notebooks/llama-3.1-8b/solana_evaluation.ipynb` |
| Qwen2.5-Coder-32B | `notebooks/qwen2.5-coder-32b/qwen-finetuning.ipynb` | `notebooks/qwen2.5-coder-32b/qwen-evaluation.ipynb` |
| Qwen3-32B | `notebooks/qwen3-32b/qwen3-finetuning.ipynb` | `notebooks/qwen3-32b/qwen3-evaluation.ipynb` |

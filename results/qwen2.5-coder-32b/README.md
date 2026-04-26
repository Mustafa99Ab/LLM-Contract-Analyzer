# Qwen2.5-Coder-32B — Evaluation Results

Evaluation results for **Qwen2.5-Coder-32B-Instruct** on 59 unseen Solana smart contracts across 4 configurations.

## Results Summary

| Configuration | Accuracy | Precision | Recall | F1-Score | TP | FP | TN | FN |
|--------------|----------|-----------|--------|----------|----|----|----|----|
| Qwen-Base (no RAG) | 0.409 | 0.308 | 0.276 | 0.291 | 8 | 18 | 19 | 21 |
| Qwen-Base + RAG | 0.202 | 0.213 | 0.793 | 0.336 | 23 | 85 | 0 | 6 |
| **Qwen-FT (no RAG)** | **0.471** | **0.422** | **0.655** | **0.514** | **19** | **26** | **13** | **10** |
| Qwen-FT + RAG | 0.235 | 0.177 | 0.586 | 0.272 | 17 | 79 | 11 | 12 |

## Key Findings

1. **Fine-tuning improves F1 by 77%** (0.291 → 0.514), confirming domain adaptation is essential even for code-specialized models.
2. **RAG boosts base model recall dramatically** (0.276 → 0.793) but at the cost of precision (0.308 → 0.213), producing many false positives.
3. **RAG hurts the fine-tuned model** (F1: 0.514 → 0.272) — the FT model already internalized vulnerability patterns, and RAG introduces noise.
4. **Best configuration: Qwen-FT without RAG** (F1 = 0.514, Accuracy = 0.471).

## Comparison with LLaMA 3.1-8B (Phase 1)

| Configuration | LLaMA 3.1-8B | Qwen2.5-Coder-32B | Improvement |
|--------------|-------------|-------------------|-------------|
| Base (no RAG) F1 | 0.085 | 0.291 | +242% |
| Base + RAG F1 | 0.193 | 0.336 | +74% |
| **FT (no RAG) F1** | **0.327** | **0.514** | **+57%** |
| FT + RAG F1 | 0.319 | 0.272 | -15% |

The code-specialized Qwen2.5-Coder-32B outperforms the general-purpose LLaMA 3.1-8B in 3 out of 4 configurations, with the most significant gains in the fine-tuned configuration (+57% F1).

## Files

| File | Description |
|------|-------------|
| `evaluation_results.json` | Aggregated metrics for all 4 configurations |
| `detailed_results.json` | Per-contract predictions and model responses |
| `results_base_no_rag.json` | Config 1: Base model, no RAG |
| `results_base_rag.json` | Config 2: Base model + RAG |
| `results_ft_no_rag.json` | Config 3: Fine-tuned, no RAG |
| `results_ft_rag.json` | Config 4: Fine-tuned + RAG |
| `charts/evaluation_chart.png` | All 4 configurations comparison chart |
| `charts/finetuning_impact.png` | Base vs Fine-tuned comparison |
| `charts/rag_impact.png` | FT vs FT+RAG comparison |

## Hardware

- **GPU:** NVIDIA RTX A6000 (48GB VRAM)
- **Total evaluation time:** ~174 minutes (Config 1: 50 min, Config 2: 51 min, Config 3: 21 min, Config 4: 52 min)

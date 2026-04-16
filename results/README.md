# Evaluation Results

This folder contains the evaluation results for the Solana vulnerability detection framework, organized per base model. Each model has its own subfolder with metrics, detailed predictions, and comparative charts.

## Structure

```
results/
└── llama-3.1-8b/
    ├── evaluation_results.json    # Aggregated metrics (Accuracy, Precision, Recall, F1)
    ├── detailed_results.json      # Per-contract predictions for all 4 configurations
    ├── recompute_metrics.py       # Script to recompute metrics from detailed results
    └── charts/
        ├── evaluation_chart.png   # 4-configuration comparison
        ├── finetuning_impact.png  # Base vs Fine-Tuned (no RAG)
        └── rag_impact.png         # FT vs FT+RAG
```

## Evaluation Configurations

Following Tortora (2025), the model is evaluated across four configurations on 59 unseen Solana smart contracts:

| # | Configuration | Description |
|---|--------------|-------------|
| 1 | LLaMA-Base (no RAG) | Baseline: unmodified model, direct prompting |
| 2 | LLaMA-Base + RAG | Base model with retrieval-augmented context |
| 3 | LLaMA-FT (no RAG) | Fine-tuned model, direct prompting |
| 4 | LLaMA-FT + RAG | Fine-tuned model with RAG context |

## Results Summary (LLaMA 3.1-8B)

| Configuration | Accuracy | Precision | Recall | F1-Score |
|--------------|----------|-----------|--------|----------|
| LLaMA-Base (no RAG) | 0.358 | 0.111 | 0.069 | 0.085 |
| LLaMA-Base + RAG | 0.330 | 0.148 | 0.276 | 0.193 |
| **LLaMA-FT (no RAG)** | **0.507** | **0.346** | **0.310** | **0.327** |
| LLaMA-FT + RAG | 0.454 | 0.275 | 0.379 | 0.319 |

### Key observations

1. **Fine-tuning significantly improves performance.** The F1-score nearly quadruples (0.085 to 0.327) from Base to FT without RAG, confirming that domain adaptation is essential for Solana/Rust code analysis.

2. **RAG provides the largest gain on the base model.** On the unmodified LLaMA, RAG improves F1 from 0.085 to 0.193 (more than 2x). This suggests that the base model benefits heavily from injected vulnerability context.

3. **RAG does not improve the fine-tuned model.** F1 drops slightly from 0.327 to 0.319 when RAG is added. One hypothesis: the fine-tuned model has already internalized the vulnerability patterns, making additional context less useful and occasionally misleading.

4. **The best configuration is LLaMA-FT without RAG** at F1=0.327, Accuracy=0.507.

### Comparison with Tortora (2025)

| Metric | Tortora (Qwen3-32B FT+RAG, PyTeal) | Ours (LLaMA-8B FT, Rust) |
|--------|-------------------------------------|--------------------------|
| F1-Score | 0.90 | 0.33 |
| Base model | 32B | 8B (4x smaller) |
| Training samples | ~500 | 226 |

The absolute difference is expected given the smaller model capacity and fewer training samples. However, the **relative improvement from fine-tuning** is consistent: both studies observe that domain adaptation substantially improves detection performance on non-EVM smart contract languages.

## A Note on Metric Computation

The `evaluation_results.json` file in this folder contains the **corrected** metrics. During the initial evaluation, the scoring function treated vulnerability synonyms as distinct predictions. For example, if the model output `["Bump Seed", "Bump Seed Canonicalization"]`, the original parser counted this as one correct answer plus one false positive, when in fact both terms refer to the same vulnerability.

The `recompute_metrics.py` script in this folder addresses this by normalizing predictions through an alias table before counting. The raw model predictions in `detailed_results.json` are untouched - only the aggregation logic changed.

### Reproducing the corrected metrics

To verify the results yourself:

```bash
python recompute_metrics.py detailed_results.json
```

This reads the raw predictions and produces the same numbers shown in `evaluation_results.json` in under one second, without requiring any GPU or model inference.

### Why this approach

The alternative would be to re-run the entire evaluation on Kaggle (approximately 6 hours on a T4 GPU). Since the model outputs themselves are deterministic and already saved, re-running would produce identical predictions. Recomputing the metrics directly from the saved predictions is both faster and equivalent.

### For transparency

The original (uncorrected) `evaluation_notebook.py` cell is preserved in the notebook history. The corrected version is documented inline so reviewers can see both the original issue and the fix.

## Training Notebook

The notebook used to train the model is available at:
`notebooks/llama-3.1-8b/solana_finetuning.ipynb`

The evaluation notebook is at:
`notebooks/llama-3.1-8b/solana_evaluation.ipynb`

Both include all cells, hyperparameters, and data paths needed for full reproducibility.

## Model Hosting

The fine-tuned LoRA adapter is hosted on Hugging Face Hub:
https://huggingface.co/Mustafa99Hafed/LLaMA-3.1-8B-Solana-Audit

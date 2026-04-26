# Qwen2.5-Coder-32B — Notebooks

Fine-tuning and evaluation notebooks for **Qwen2.5-Coder-32B-Instruct** on the Solana vulnerability detection task.

## Hardware

| Component | Specification |
|-----------|---------------|
| GPU | NVIDIA RTX A6000 (48GB VRAM) |
| CUDA | 12.6 |
| Python | 3.10.19 |
| PyTorch | 2.10.0+cu126 |
| Framework | Unsloth + trl 0.24.0 |

## Notebooks

### `qwen-finetuning.ipynb`

QLoRA fine-tuning of Qwen2.5-Coder-32B-Instruct for Solana/Rust vulnerability detection using Chain-of-Thought (CoT) training.

| Parameter | Value |
|-----------|-------|
| Base Model | Qwen2.5-Coder-32B-Instruct |
| Quantization | 4-bit (NF4) via QLoRA |
| LoRA Rank (r) | 64 |
| LoRA Alpha | 128 |
| Target Modules | All linear layers (Attention + MLP) |
| Epochs | 3 |
| Learning Rate | 5e-5 (cosine decay) |
| Effective Batch Size | 8 (1 × 8 accumulation) |
| Max Sequence Length | 2048 tokens |
| Training Duration | 29.9 minutes (87 steps) |
| Final Train Loss | 0.173 |
| Final Val Loss | 0.170 |
| Adapter Size | 2059 MB |

### `qwen-evaluation.ipynb`

Evaluation across 4 configurations on 59 unseen Solana contracts, measuring Accuracy, Precision, Recall, and F1-Score.

| Configuration | Accuracy | Precision | Recall | F1-Score |
|--------------|----------|-----------|--------|----------|
| Qwen-Base (no RAG) | 0.409 | 0.308 | 0.276 | 0.291 |
| Qwen-Base + RAG | 0.202 | 0.213 | 0.793 | 0.336 |
| **Qwen-FT (no RAG)** | **0.471** | **0.422** | **0.655** | **0.514** |
| Qwen-FT + RAG | 0.235 | 0.177 | 0.586 | 0.272 |

**Best configuration: Qwen-FT (no RAG)** — F1 = 0.514

## Why Qwen2.5-Coder-32B?

- Code-specialized model trained on 5.5 trillion tokens across 92 programming languages (including Rust)
- 32B parameters (4× larger than LLaMA 3.1-8B used in Phase 1)
- Provides two comparison axes: model size (8B vs 32B) and specialization (general-purpose vs code-specialized)

## References

- Boi, B. & Esposito, C. (2025). *Prompt Engineering vs. Fine-Tuning for LLM-Based Vulnerability Detection in Solana and Algorand Smart Contracts*. IEEE BCCA 2025.
- Tortora, N. (2025). *LLM-Based Vulnerability Detection for Smart Contracts*. Master's Thesis, University of Salerno.

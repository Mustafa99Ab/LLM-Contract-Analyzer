# Source Code

This folder contains the full project source code organized into three modules.

## `rag/`
- `generate_embeddings.py` — Encodes the knowledge base contracts into vector representations and saves them to disk. Run this once before evaluation to prepare the RAG index.
- `rag.py` — At inference time, searches the index for contracts similar to the input and builds a dynamic vulnerability checklist that is injected into the model prompt.

## `finetuning/`
- `train_qlora.py` — Main training script. Loads the CoT dataset, configures QLoRA (r=64, alpha=128), and fine-tunes LLaMA 3.1-8B-Instruct using Unsloth on a Kaggle T4 GPU.
- `custom_chat_template.jinja` — Defines the chat template used during training so the model learns to produce structured output with `<think>` and `<final>` tags.

## `evaluation/`
- `run_benchmark_no_rag.py` — Runs the evaluation pipeline on the 59 test contracts without RAG context (Configurations 1 and 3).
- `run_benchmark_rag.py` — Runs the evaluation pipeline with RAG-augmented prompts (Configurations 2 and 4).
- `metrics.py` — Computes Accuracy, Precision, Recall, and F1-Score from the model predictions.
- `utils/` — Shared utilities: prompt templates, output parser, API client, and test logging.

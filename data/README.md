# Data

This folder contains all data used in the project, organized into four subfolders.

## Structure

### `training/`
Contains the Chain-of-Thought (CoT) formatted dataset used to fine-tune LLaMA 3.1-8B:
- `dataset_think_format.jsonl` — 226 training samples. Each sample contains a Solana/Rust contract, a structured reasoning trace inside `<think>` tags, and a vulnerability verdict inside `<final>` tags.
- `validation_dataset.jsonl` — 22 samples held out during training to monitor overfitting.

### `test_set/`
Contains 59 unseen Solana smart contracts (`solana_01.json` to `solana_59.json`) used for evaluation. Each file contains only the contract code and the ground-truth vulnerability label — the model never sees these during training.

### `knowledge_base/`
Contains the RAG reference data used during inference:
- `vulnerability_info.json` — Profiles for all 7 vulnerability types (description, attack scenario, security checks, mitigation).
- `rag_contracts.jsonl` — Indexed vulnerable contracts used for similarity search to build dynamic checklists at inference time.

### `dataset_construction/`
Contains the raw SPL contracts and batch files used to build the full dataset of 285 samples across 15 real deployed contracts. Each batch subfolder includes the source contracts and a README documenting the extraction methodology. The final merged dataset is in `final DS/dataset_final.json`.

# Confusion Matrix & Binary Re-evaluation — Analysis Results

This folder contains the supplementary analysis requested by the supervisors (Prof. Esposito and Dr. Boi) during the May 2026 review meeting. The analysis was performed entirely on the per-sample predictions already logged in the three evaluation notebooks — **no new model inference was executed**.

Two deliverables were produced for each of the 12 experiments (3 models × 4 configurations):

1. A **9 × 9 confusion matrix** (rows = true label, columns = predicted label).
2. A **binary re-evaluation** (VULNERABLE vs NOT_VULNERABLE) testing the supervisors' hypothesis that the models detect vulnerabilities reliably but confuse the specific class.

---

## Folder Structure

```
confusion_matrix_binary_analysis/
├── README.md                   ← this file
├── REPORT.md                   ← main analytical report (start here)
├── LLaMA/                      ← LLaMA-3.1-8B-Instruct results
│   ├── cm_LLaMA-Base_no_RAG.png
│   ├── cm_LLaMA-Base_plus_RAG.png
│   ├── cm_LLaMA-FT_no_RAG.png
│   ├── cm_LLaMA-FT_plus_RAG.png
│   ├── comparison.json
│   └── confusion_matrices.json
├── Qwen2.5/                    ← Qwen2.5-Coder-32B-Instruct results
│   ├── cm_Qwen-Base_no_RAG.png
│   ├── cm_Qwen-Base_plus_RAG.png
│   ├── cm_Qwen-FT_no_RAG.png
│   ├── cm_Qwen-FT_plus_RAG.png
│   └── qwen25_comparison.json
└── Qwen3/                      ← Qwen3-32B results
    ├── cm_Qwen3-Base_no_RAG.png
    ├── cm_Qwen3-Base_plus_RAG.png
    ├── cm_Qwen3-FT_no_RAG.png
    ├── cm_Qwen3-FT_plus_RAG.png
    └── qwen3_comparison.json
```

---

## Contents

### `REPORT.md`
Full analytical write-up: methodology, unified comparison table covering all 12 experiments, key confusion-matrix findings with embedded figures, hypothesis discussion, and limitations. **Start here.**

### `LLaMA/`
Four 9×9 confusion matrices (PNG) corresponding to the four configurations:
- **Base (no RAG)**, **Base + RAG**, **Fine-tuned (no RAG)**, **Fine-tuned + RAG**

Plus two JSON files:
- `confusion_matrices.json` — raw 9×9 matrix counts for all four configurations
- `comparison.json` — binary re-evaluation: Accuracy, Precision, Recall, F1, and TP/FP/TN/FN counts per configuration

### `Qwen2.5/`
Same four-config PNG structure. `qwen25_comparison.json` holds the binary metrics.

### `Qwen3/`
Same structure. **Note:** Qwen3-FT + RAG completed only 54 of 59 test samples in the original notebook run — contracts #19, 20, 37, 38 and 57 failed during inference (likely OOM or timeout) and are not present in the logged predictions. The matrix and binary metrics for that configuration are computed over 54 samples; this is flagged in `REPORT.md`.

---

## Confusion-Matrix Class Codes

All twelve confusion matrices use the following 9-class axis labels:

| Code | Class |
|------|-------|
| V1   | Missing Key Check |
| V4   | Type Confusion / Input Validation |
| V5   | CPI Reentrancy |
| V6   | Unchecked External Calls |
| V8   | Integer Overflow |
| V9   | Bump Seed Canonicalization |
| V10  | Denial of Service |
| NV   | Not Vulnerable |
| UNP  | Unparseable (model failed to emit a recognizable verdict) |

The **UNP** column was added because the original parser sometimes returned an empty list when the model produced no recognizable answer; counting these explicitly avoids inflating the "Not Vulnerable" cells with cases where the model simply stayed silent.

A perfect classifier would have all counts on the diagonal.

---

## How to Read the Outputs

1. Open `REPORT.md` in any markdown viewer that supports relative image paths (VS Code, Obsidian, GitHub web view).
2. The four selected confusion matrices referenced in the report render automatically from the sub-folders.
3. The remaining eight matrices are available in their respective model folders for cases where additional figures are needed.
4. The `*_comparison.json` and `confusion_matrices.json` files are machine-readable; they are the source of truth for the tables in `REPORT.md` and can be re-used to produce alternative visualizations.

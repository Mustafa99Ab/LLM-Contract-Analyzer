# Experiment 1: Zero-Shot Prompt Engineering

## Overview

This experiment evaluates the capability of LLaMA-3.1-8B-Instruct to detect vulnerabilities in Solana smart contracts **without any fine-tuning**, using only role-based prompting.

---

## Methodology

### What is Zero-Shot?

Zero-Shot learning means the model performs a task without seeing any training examples. The model relies entirely on its pre-trained knowledge and the task description provided in the prompt.

### Approach

The model is given a **role-based prompt** that instructs it to act as a security analyzer:

```
System Prompt:
    You are a smart contract security analyzer.
    You analyze Solana smart contracts written in Rust and identify vulnerabilities.
    Classify the code as either VULNERABLE or SAFE.
    Respond with only one word: VULNERABLE or SAFE.

User Input:
    [Solana Smart Contract Code]

Model Output:
    VULNERABLE or SAFE
```

### Why No Training Parameters?

Since this is Zero-Shot, there are:
- ❌ No training epochs
- ❌ No learning rate
- ❌ No fine-tuning
- ✅ Only inference using pre-trained weights

---

## Model Configuration

| Parameter | Value |
|-----------|-------|
| Model | Llama-3.1-8B-Instruct |
| Parameters | 8 Billion |
| Quantization | 4-bit NF4 |
| Max Sequence Length | 2048 tokens |

---

## Dataset

### Structure

| Split | Samples | Percentage |
|-------|---------|------------|
| Train | 112 | 80% |
| Validation | 14 | 10% |
| Test | 14 | 10% |
| **Total** | **140** | 100% |

### Vulnerability Types (7 Categories)

Each category contains 20 samples (10 VULNERABLE + 10 SAFE):

1. **Bump Seed** - Insecure PDA derivation
2. **CPI (Cross-Program Invocation)** - Unsafe cross-program calls
3. **DoS (Denial of Service)** - Resource exhaustion vulnerabilities
4. **Integer Flow** - Overflow/underflow issues
5. **Missing Key Check** - Missing account validation
6. **Type Confusion** - Incorrect type handling
7. **Unchecked Calls** - Unvalidated external calls

### Label Distribution

- VULNERABLE: 70 samples (50%)
- SAFE: 70 samples (50%)

---

## Results

### Overall Performance

| Metric | Value |
|--------|-------|
| **Accuracy** | **71.43%** |
| Precision | 63.64% |
| Recall | 100% |
| F1-Score | 77.78% |

### Performance by Vulnerability Type

| Vulnerability | Accuracy | Precision | Recall | F1-Score |
|---------------|----------|-----------|--------|----------|
| Integer Flow | 100% | 100% | 100% | 100% |
| Missing Key Check | 100% | 100% | 100% | 100% |
| Type Confusion | 100% | 100% | 100% | 100% |
| Bump Seed | 50% | 50% | 100% | 67% |
| CPI | 50% | 50% | 100% | 67% |
| DoS | 50% | 50% | 100% | 67% |
| Unchecked Calls | 50% | 50% | 100% | 67% |

### Confusion Matrix

```
                    Predicted
                VULNERABLE    SAFE
Actual  VULNERABLE    7         0      → 100% Detection Rate
        SAFE          4         3      → 43% Specificity
```

| Metric | Count | Meaning |
|--------|-------|---------|
| TP (True Positive) | 7 | Correctly identified vulnerabilities |
| FN (False Negative) | 0 | Missed vulnerabilities |
| FP (False Positive) | 4 | Safe code marked as vulnerable |
| TN (True Negative) | 3 | Correctly identified safe code |

---

## Analysis

### Strengths

1. **Perfect Recall (100%)**: The model detected ALL vulnerabilities in the test set without missing any. This is critical for security applications where missing a vulnerability could be catastrophic.

2. **Strong Performance on Complex Vulnerabilities**: Achieved 100% accuracy on Integer Flow, Missing Key Check, and Type Confusion - these require understanding of code semantics.

3. **No Training Required**: Achieved 71.43% accuracy without any fine-tuning, demonstrating strong transfer learning capabilities.

### Weaknesses

1. **High False Positive Rate**: 4 out of 7 safe samples were incorrectly classified as vulnerable, indicating the model is overly cautious.

2. **Conservative Bias**: The model tends to classify ambiguous code as VULNERABLE, which increases recall but decreases precision.

3. **Inconsistent Performance**: Perfect accuracy on some vulnerability types (100%) but only 50% on others, suggesting the model's pre-trained knowledge varies by vulnerability category.

### Why These Results?

The model exhibits **conservative security behavior** - it prefers to flag potential issues rather than miss them. This is actually desirable in security contexts where:
- False Positives → Extra code review (acceptable)
- False Negatives → Undetected vulnerabilities (dangerous)

---

## Output Files

| File | Description |
|------|-------------|
| `results_zero_shot.csv` | Detailed predictions for each sample |
| `summary_zero_shot.json` | Complete metrics and configuration |
| `cm_zero_shot.png` | Confusion matrix visualization |

---

## How to Run

1. Upload the notebook to Kaggle
2. Enable GPU (Settings → Accelerator → GPU T4 x2)
3. Add HuggingFace token to Secrets (name: `HF_TOKEN`)
4. Upload dataset to `/kaggle/input/solana-dataset/`
5. Run all cells

---

## Requirements

```
torch
transformers
bitsandbytes
accelerate
scikit-learn
pandas
matplotlib
seaborn
```

---

## Citation

If you use this experiment, please cite:

```bibtex
@misc{solana_vuln_detection_2025,
  title={LLM-Based Vulnerability Detection in Solana Smart Contracts},
  author={[Your Name]},
  year={2025},
  note={Experiment 1: Zero-Shot Prompt Engineering}
}
```

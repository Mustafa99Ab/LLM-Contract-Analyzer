# Final Research Report
## A Comprehensive Analysis of Solana Smart Contracts Using the LLaMA 3 Large Language Model

---

# Research Information

| Item | Details |
|------|---------|
| **Title** | A Comparative Study of Large Language Models for Smart Contract Security Analysis |
| **Academic Context** | Master’s Thesis – University of Salerno |
| **Reference Paper** | Prompt Engineering vs. Fine-Tuning for LLM-Based Vulnerability Detection in Solana and Algorand Smart Contracts |
| **Model Used** | LLaMA-3.1-8B-Instruct |
| **Model in Reference Paper** | LLaMA-3-8B |

---

# 1. Dataset

## 1.1 General Statistics

| Item | Value |
|------|-------|
| **Total Samples** | 182 |
| **Training Samples** | 140 (77%) |
| **Validation Samples** | 21 (11.5%) |
| **Test Samples** | 21 (11.5%) |
| **Balance** | 91 VULNERABLE / 91 SAFE (50% / 50%) |

## 1.2 Vulnerability Type Distribution

| Vulnerability Type | OWASP Code | Number of Samples | VULN | SAFE |
|--------------------|------------|------------------|------|------|
| Missing Key Check (Access Control) | V1 | 26 | 13 | 13 |
| Integer Flow (Overflow/Underflow) | V4 | 26 | 13 | 13 |
| CPI (Cross-Program Invocation) | V5 | 26 | 13 | 13 |
| Unchecked Calls | V6 | 26 | 13 | 13 |
| Bump Seed (PDA Validation) | V8 | 26 | 13 | 13 |
| Type Confusion | V9 | 26 | 13 | 13 |
| DoS (Denial of Service) | V10 | 26 | 13 | 13 |
| **Total** | – | **182** | **91** | **91** |

## 1.3 Data Sources

| Source | Number of Samples | Lines of Code |
|--------|------------------|---------------|
| solana-program-library (stake-pool) | 45 | ~3,200 |
| anchor-escrow | 35 | ~1,500 |
| solana-developers/program-examples | 30 | ~2,100 |
| elmhamed/smart-contracts-vulns | 30 | ~1,600 |
| token-swap program | 42 | ~8,377 |
| **Total** | **182** | **~16,766** |

---

# 2. Experiments

## 2.1 Experiment 1: Zero-Shot Prompt Engineering

### Description
The base model (without training) is used with a simple prompt to classify code.

### Configuration

| Item | Value |
|------|-------|
| Model | LLaMA-3.1-8B-Instruct (Base) |
| Training | None |
| Examples | None |
| Quantization | 4-bit NF4 |

### Results

| Metric | Value |
|--------|-------|
| **Accuracy** | **38.10%** |
| Precision | 35.00% |
| Recall | 100.00% |
| F1-Score | 51.85% |

### Confusion Matrix

|  | Predicted VULN | Predicted SAFE |
|--|----------------|----------------|
| **Actual VULN** | 7 (TP) | 0 (FN) |
| **Actual SAFE** | 13 (FP) | 1 (TN) |

### Performance per Vulnerability Type

| Vulnerability Type | Accuracy |
|--------------------|----------|
| Bump Seed | 33.33% |
| CPI | 33.33% |
| DoS | 33.33% |
| Integer Flow | 66.67% |
| Missing Key Check | 33.33% |
| Type Confusion | 33.33% |
| Unchecked Calls | 33.33% |
| **Average** | **38.10%** |

### Analysis
- The model classifies **almost everything as VULNERABLE** (20 out of 21).
- Recall = 100% because no vulnerability is missed.
- However, FP = 13, indicating many false alarms.
- This is a conservative behavior expected from an untrained model.

---

## 2.2 Experiment 2: Few-Shot Prompt Engineering

### Description
The base model is used with a small number of examples in the prompt to guide classification.

### Configuration

| Item | Value |
|------|-------|
| Model | LLaMA-3.1-8B-Instruct (Base) |
| Training | None |
| Examples | 4 (2 VULNERABLE + 2 SAFE) |
| Quantization | 4-bit NF4 |

### Results

| Metric | Value |
|--------|-------|
| **Accuracy** | **61.90%** |
| Precision | 44.44% |
| Recall | 57.14% |
| F1-Score | 50.00% |

### Confusion Matrix

|  | Predicted VULN | Predicted SAFE |
|--|----------------|----------------|
| **Actual VULN** | 4 (TP) | 3 (FN) |
| **Actual SAFE** | 5 (FP) | 9 (TN) |

### Performance per Vulnerability Type

| Vulnerability Type | Accuracy |
|--------------------|----------|
| Bump Seed | 33.33% |
| CPI | 66.67% |
| DoS | 33.33% |
| Integer Flow | 33.33% |
| Missing Key Check | 66.67% |
| Type Confusion | 100.00% |
| Unchecked Calls | 100.00% |
| **Average** | **61.90%** |

### Analysis
- Significant improvement compared to Zero-Shot (+23.8%).
- The model becomes more balanced.
- True Negatives improved from 1 to 9, indicating better recognition of safe code.
- Type Confusion and Unchecked Calls achieved 100% accuracy.

---

## 2.3 Experiment 3: Fine-Tuning with QLoRA

### Description
The model is trained on the dataset using QLoRA (Quantized Low-Rank Adaptation).

### Configuration

| Item | Value |
|------|-------|
| Model | LLaMA-3.1-8B-Instruct |
| Training Method | QLoRA (4-bit) |
| Epochs | 3 |
| Learning Rate | 2e-4 |
| LoRA r | 64 |
| LoRA alpha | 16 |
| LoRA dropout | 0.1 |
| Batch Size | 2 |
| Gradient Accumulation | 4 |
| Effective Batch Size | 8 |

### Training Results

| Epoch | Training Loss | Validation Loss | Token Accuracy |
|-------|---------------|-----------------|----------------|
| 1 | 1.6252 | 0.8696 | 80.58% |
| 2 | 0.7450 | 0.7079 | 83.64% |
| 3 | 0.6382 | 0.6923 | 83.96% |

### Results

| Metric | Value |
|--------|-------|
| **Accuracy** | **66.67%** |
| Precision | 50.00% |
| Recall | 28.57% |
| F1-Score | 36.36% |

### Confusion Matrix

|  | Predicted VULN | Predicted SAFE |
|--|----------------|----------------|
| **Actual VULN** | 2 (TP) | 5 (FN) |
| **Actual SAFE** | 2 (FP) | 12 (TN) |

### Performance per Vulnerability Type

| Vulnerability Type | Accuracy |
|--------------------|----------|
| Bump Seed | 66.67% |
| CPI | 33.33% |
| DoS | 66.67% |
| Integer Flow | 33.33% |
| Missing Key Check | 100.00% |
| Type Confusion | 100.00% |
| Unchecked Calls | 66.67% |
| **Average** | **66.67%** |

### Analysis
- Highest accuracy so far among individual approaches.
- The model tends to classify code as SAFE (TN = 12).
- Recall is low (28.57%), meaning some vulnerabilities are missed.
- Missing Key Check and Type Confusion achieved 100% accuracy.

---

## 2.4 Experiment 4: Prompt Engineering + Fine-Tuning (PE + FT)

### Description
The fine-tuned model is used with an optimized role-based prompt (without few-shot examples).

### Configuration

| Item | Value |
|------|-------|
| Model | LLaMA-3.1-8B-Instruct (Fine-Tuned) |
| Training | QLoRA (from Experiment 3) |
| Examples | None |
| Prompt | Role-based optimized |

### Results

| Metric | Value |
|--------|-------|
| **Accuracy** | **71.43%** |
| Precision | 60.00% |
| Recall | 42.86% |
| F1-Score | 50.00% |

### Confusion Matrix

|  | Predicted VULN | Predicted SAFE |
|--|----------------|----------------|
| **Actual VULN** | 3 (TP) | 4 (FN) |
| **Actual SAFE** | 2 (FP) | 12 (TN) |

### Performance per Vulnerability Type

| Vulnerability Type | Accuracy |
|--------------------|----------|
| Bump Seed | 66.67% |
| CPI | 33.33% |
| DoS | 100.00% |
| Integer Flow | 33.33% |
| Missing Key Check | 100.00% |
| Type Confusion | 100.00% |
| Unchecked Calls | 66.67% |
| **Average** | **71.43%** |

### Analysis
- **Best overall result** among all experiments.
- Good balance between True Positives and True Negatives.
- Three vulnerability types achieved 100% accuracy.
- Recall improved compared to Fine-Tuning alone.

---

# 3. Results Summary

## 3.1 Overall Comparison

| Metric | Zero-Shot | Few-Shot | Fine-Tuning | **PE + FT** |
|--------|-----------|----------|-------------|-------------|
| **Accuracy** | 38.10% | 61.90% | 66.67% | **71.43%** |
| Precision | 35.00% | 44.44% | 50.00% | **60.00%** |
| Recall | **100.00%** | 57.14% | 28.57% | 42.86% |
| F1-Score | 51.85% | **50.00%** | 36.36% | **50.00%** |

---

# 4. Conclusions

> **Combining Prompt Engineering with Fine-Tuning (PE + FT) provides the best performance for detecting vulnerabilities in Solana smart contracts, achieving an accuracy of 71.43% and outperforming the reference paper by +10.43%.**

---

**Report Date:** December 15, 2025

**Tools Used:** Kaggle, HuggingFace, PyTorch


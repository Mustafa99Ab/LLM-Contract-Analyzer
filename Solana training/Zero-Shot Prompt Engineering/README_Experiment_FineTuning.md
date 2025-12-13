# Experiment 2: Fine-Tuning with QLoRA

## Overview

This experiment fine-tunes LLaMA-3.1-8B-Instruct on Solana smart contract vulnerability detection using **QLoRA** (Quantized Low-Rank Adaptation) combined with **SFTTrainer** for efficient and effective training.

---

## Methodology

### What is QLoRA?

QLoRA (Quantized Low-Rank Adaptation) is an efficient fine-tuning technique that:
1. **Quantizes** the base model to 4-bit precision (reduces memory)
2. **Adds small trainable adapters** (LoRA) to specific layers
3. **Trains only the adapters** while keeping base weights frozen

This allows fine-tuning large models (8B parameters) on consumer GPUs.

### Key Innovation: Completion-Only Training

We use `DataCollatorForCompletionOnlyLM` which computes loss **only on the model's response** (VULNERABLE/SAFE), not on the input prompt.

```
Standard Training:
    Loss = f(System Prompt + User Code + Response)  ← Learns everything
    Problem: Model may memorize patterns instead of learning

Our Approach:
    Loss = f(Response only)  ← Learns only classification
    Result: Model focuses on actual vulnerability detection
```

### Training Pipeline

```
Input: Solana Smart Contract Code
   ↓
[4-bit Quantized LLaMA-3.1-8B] + [LoRA Adapters]
   ↓
SFTTrainer with Completion-Only Loss
   ↓
Output: VULNERABLE or SAFE
```

---

## Model Configuration

| Parameter | Value |
|-----------|-------|
| Base Model | Llama-3.1-8B-Instruct |
| Parameters | 8 Billion |
| Quantization | 4-bit NF4 |
| Double Quantization | Enabled |

---

## LoRA Configuration

| Parameter | Value | Description |
|-----------|-------|-------------|
| Rank (r) | 64 | Dimension of low-rank matrices |
| Alpha | 16 | Scaling factor |
| Dropout | 0.1 | Regularization |
| Target Modules | q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj | Attention + MLP layers |

### Why These Values?

- **r=64**: Higher rank captures more task-specific patterns
- **alpha=16**: Standard scaling factor
- **dropout=0.1**: Prevents overfitting on small dataset
- **All attention + MLP layers**: Maximum adaptation capability

---

## Training Configuration

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Epochs | 3 | 1-3 recommended to prevent overfitting |
| Learning Rate | 2e-4 | Standard for QLoRA |
| Batch Size | 2 | GPU memory constraint |
| Gradient Accumulation | 4 | Effective batch = 8 |
| Max Sequence Length | 1024 | Sufficient for smart contracts |
| Warmup Ratio | 0.03 | Gradual learning rate increase |
| Optimizer | paged_adamw_32bit | Memory-efficient optimizer |
| LR Scheduler | Cosine | Smooth learning rate decay |

### Why 3 Epochs?

According to established best practices:
- Small datasets (140 samples) need fewer epochs
- More than 3 epochs increases overfitting risk
- Early stopping monitors validation loss

---

## Dataset

### Structure

| Split | Samples | Percentage | Purpose |
|-------|---------|------------|---------|
| Train | 112 | 80% | Model training |
| Validation | 14 | 10% | Hyperparameter tuning |
| Test | 14 | 10% | Final evaluation |
| **Total** | **140** | 100% | |

### Vulnerability Types (7 Categories)

Each category contains 20 samples (10 VULNERABLE + 10 SAFE):

1. **Bump Seed** - Insecure PDA derivation
2. **CPI (Cross-Program Invocation)** - Unsafe cross-program calls
3. **DoS (Denial of Service)** - Resource exhaustion vulnerabilities
4. **Integer Flow** - Overflow/underflow issues
5. **Missing Key Check** - Missing account validation
6. **Type Confusion** - Incorrect type handling
7. **Unchecked Calls** - Unvalidated external calls

### Stratified Sampling

Data split maintains class balance within each vulnerability type to ensure representative training and evaluation.

---

## Results

### Overall Performance

| Metric | Value |
|--------|-------|
| **Accuracy** | **85.71%** |
| Precision | 85.71% |
| Recall | 85.71% |
| F1-Score | 85.71% |

### Performance by Vulnerability Type

| Vulnerability | Accuracy | Precision | Recall | F1-Score |
|---------------|----------|-----------|--------|----------|
| Bump Seed | 100% | 100% | 100% | 100% |
| DoS | 100% | 100% | 100% | 100% |
| Missing Key Check | 100% | 100% | 100% | 100% |
| Type Confusion | 100% | 100% | 100% | 100% |
| Unchecked Calls | 100% | 100% | 100% | 100% |
| CPI | 50% | 50% | 100% | 67% |
| Integer Flow | 50% | 0% | 0% | 0% |

### Confusion Matrix

```
                    Predicted
                VULNERABLE    SAFE
Actual  VULNERABLE    6         1      → 85.7% Detection Rate
        SAFE          1         6      → 85.7% Specificity
```

| Metric | Count | Meaning |
|--------|-------|---------|
| TP (True Positive) | 6 | Correctly identified vulnerabilities |
| FN (False Negative) | 1 | Missed vulnerabilities |
| FP (False Positive) | 1 | Safe code marked as vulnerable |
| TN (True Negative) | 6 | Correctly identified safe code |

---

## Analysis

### Strengths

1. **High Overall Accuracy (85.71%)**: Significant improvement from baseline, demonstrating effective learning from the training data.

2. **Balanced Performance**: Equal precision and recall (85.71%) indicates the model is not biased toward either class.

3. **Perfect Detection on 5/7 Categories**: Achieved 100% accuracy on Bump Seed, DoS, Missing Key Check, Type Confusion, and Unchecked Calls.

4. **Reduced False Positives**: Only 1 false positive compared to 4 in Zero-Shot, making the model more practical for real-world use.

### Weaknesses

1. **Integer Flow Detection Failed**: 0% recall on Integer Flow suggests the model failed to learn patterns for this vulnerability type.

2. **CPI Partial Success**: 50% accuracy on CPI indicates room for improvement in cross-program invocation detection.

### Why These Results?

1. **Completion-Only Training**: By training only on the classification output, the model learned to focus on vulnerability patterns rather than memorizing prompt structures.

2. **QLoRA Efficiency**: 4-bit quantization with LoRA adapters allowed effective fine-tuning despite limited GPU resources.

3. **Integer Flow Difficulty**: This category may require more diverse training examples or longer code context to detect subtle overflow/underflow patterns.

4. **Small Test Set**: With only 2 samples per category in the test set, individual misclassifications have large impact on per-category metrics.

---

## Training Logs

| Epoch | Training Loss | Validation Loss |
|-------|---------------|-----------------|
| 1 | ~2.4 | ~1.5 |
| 2 | ~1.4 | ~1.4 |
| 3 | ~0.9 | ~1.4 |

The decreasing training loss with stable validation loss indicates proper learning without severe overfitting.

---

## Output Files

| File | Description |
|------|-------------|
| `results_fine_tuning.csv` | Detailed predictions for each sample |
| `summary_fine_tuning.json` | Complete metrics and configuration |
| `cm_fine_tuning.png` | Confusion matrix visualization |
| `solana-vuln-model/` | Fine-tuned LoRA adapter weights |

---

## How to Run

1. Upload the notebook to Kaggle
2. Enable GPU (Settings → Accelerator → GPU T4 x2)
3. Add HuggingFace token to Secrets (name: `HF_TOKEN`)
4. Upload dataset to `/kaggle/input/solana-dataset/`
5. Run all cells (~30 minutes training time)

---

## Requirements

```
torch
transformers
bitsandbytes
accelerate
peft==0.9.0
trl==0.12.0
datasets
scikit-learn
pandas
matplotlib
seaborn
```

---

## Using the Fine-Tuned Model

```python
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

# Load base model
base_model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.1-8B-Instruct")

# Load fine-tuned adapter
model = PeftModel.from_pretrained(base_model, "path/to/solana-vuln-model")

# Use for inference
```

---

## References

```bibtex
@article{dettmers2023qlora,
  title={QLoRA: Efficient Finetuning of Quantized LLMs},
  author={Dettmers, Tim and Pagnoni, Artidoro and Holtzman, Ari and Zettlemoyer, Luke},
  journal={arXiv preprint arXiv:2305.14314},
  year={2023}
}
```

---

## Citation

If you use this experiment, please cite:

```bibtex
@misc{solana_vuln_detection_2025,
  title={LLM-Based Vulnerability Detection in Solana Smart Contracts},
  author={[Your Name]},
  year={2025},
  note={Experiment 2: Fine-Tuning with QLoRA}
}
```

"""
Step 4: Fine-Tuning LLaMA 3.1-8B with QLoRA
Adapted from Nicola Tortora's train_qlora.py for Solana/Rust.

Run this on Kaggle with T4 GPU (16GB VRAM).
LLaMA 3.1-8B in 4-bit uses ~6GB VRAM, well within T4 limits.

Setup on Kaggle:
  !pip install unsloth
  !pip install --no-deps trl peft accelerate bitsandbytes
  # Upload dataset_think_format.jsonl and validation_dataset.jsonl
"""

from unsloth import FastLanguageModel
from trl import SFTConfig, SFTTrainer
from datasets import load_dataset
from unsloth.chat_templates import standardize_sharegpt, train_on_responses_only

# ============================================================
# CONFIGURATION
# ============================================================
max_seq_length = 2048
dtype = None

# LLaMA 3.1-8B instead of Nicola's Qwen3-32B (Kaggle T4 constraint)
model_name = "unsloth/Meta-Llama-3.1-8B-Instruct"
new_model_id = "LLaMA-3.1-8B-Solana-Audit"

# Data paths (adjust if needed on Kaggle)
TRAIN_DATA = "./data/training/dataset_think_format.jsonl"
VAL_DATA = "./data/training/validation_dataset.jsonl"

# ============================================================
# 1. LOAD MODEL (4-bit quantization)
# ============================================================
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name=model_name,
    dtype=dtype,
    max_seq_length=max_seq_length,
    load_in_4bit=True,
    full_finetuning=False,
)

# ============================================================
# 2. CONFIGURE LoRA ADAPTER
# Same parameters as Nicola: r=64, alpha=128, all linear layers
# ============================================================
model = FastLanguageModel.get_peft_model(
    model,
    r=64,
    target_modules=[
        "q_proj", "k_proj", "v_proj", "o_proj",
        "gate_proj", "up_proj", "down_proj",
    ],
    lora_alpha=128,
    lora_dropout=0,
    bias="none",
    use_gradient_checkpointing="unsloth",
    random_state=3407,
    use_rslora=False,
    loftq_config=None,
)

# ============================================================
# 3. LOAD CUSTOM CHAT TEMPLATE (adds <think> and <final> tags)
# ============================================================
with open("custom_chat_template.jinja", "r", encoding="utf-8") as f:
    loaded_template = f.read()

tokenizer.chat_template = loaded_template


def formatting_prompts_func(examples):
    """Apply chat template to convert messages into formatted text."""
    convos = examples["messages"]
    texts = [
        tokenizer.apply_chat_template(
            convo, tokenize=False, add_generation_prompt=False
        )
        for convo in convos
    ]
    return {"text": texts}


# ============================================================
# 4. LOAD AND PREPARE DATASETS
# ============================================================
dataset_train = load_dataset(
    "json", data_files=TRAIN_DATA, split="train"
).shuffle(seed=43)

dataset_eval = load_dataset(
    "json", data_files=VAL_DATA, split="train"
).shuffle(seed=43)

dataset_train = standardize_sharegpt(dataset_train)
dataset_train = dataset_train.map(formatting_prompts_func, batched=True)

dataset_eval = standardize_sharegpt(dataset_eval)
dataset_eval = dataset_eval.map(formatting_prompts_func, batched=True)

# ============================================================
# 5. TRAINING CONFIGURATION
# Same hyperparameters as Nicola's thesis (Section 4.4.2)
# ============================================================
sft_config = SFTConfig(
    # GPU efficiency
    per_device_train_batch_size=1,
    gradient_accumulation_steps=8,
    gradient_checkpointing=True,

    # Training duration
    num_train_epochs=3,
    max_seq_length=max_seq_length,
    warmup_ratio=0.05,
    lr_scheduler_type="cosine",

    # Optimization
    learning_rate=5e-5,
    weight_decay=0.02,
    optim="paged_adamw_8bit",
    max_grad_norm=1.0,

    # Evaluation and logging
    eval_strategy="steps",
    eval_steps=10,
    logging_steps=10,
    save_strategy="epoch",
    save_total_limit=3,

    # Reproducibility
    seed=3407,

    # Output
    output_dir=f"models/{new_model_id}",
    report_to="none",
)

# ============================================================
# 6. CREATE TRAINER
# ============================================================
trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=dataset_train,
    eval_dataset=dataset_eval,
    args=sft_config,
)

# Train only on assistant responses, not on system/user prompts
# Adapted markers for LLaMA 3.1 token format
training_kwargs = dict(
    instruction_part="<|start_header_id|>user<|end_header_id|>",
    response_part="<|eot_id|>user_end",
)

trainer = train_on_responses_only(
    trainer,
    **training_kwargs,
)

# ============================================================
# 7. TRAIN
# ============================================================
print(f"Starting training: {new_model_id}")
print(f"  Model: {model_name}")
print(f"  Train samples: {len(dataset_train)}")
print(f"  Val samples: {len(dataset_eval)}")
print(f"  Epochs: 3, Effective batch size: 8")
print(f"  LoRA: r=64, alpha=128")

trainer_stats = trainer.train()

# ============================================================
# 8. SAVE MODEL
# ============================================================
# Save LoRA adapter locally
model.save_pretrained(f"models/{new_model_id}")
tokenizer.save_pretrained(f"models/{new_model_id}")
print(f"Model saved to models/{new_model_id}")

# Optional: push to Hugging Face Hub
# model.push_to_hub("YOUR_USERNAME/LLaMA-3.1-8B-Solana-Audit")
# tokenizer.push_to_hub("YOUR_USERNAME/LLaMA-3.1-8B-Solana-Audit")

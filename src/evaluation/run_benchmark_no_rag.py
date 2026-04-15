"""
Step 5a: Benchmark WITHOUT RAG
Tests the model's intrinsic knowledge (no retrieval context).
Adapted from Nicola Tortora's run_benchmark_no_rag.py.

Configurations tested:
  - LLaMA-Base (no RAG)
  - LLaMA-FT (no RAG)

Run on Kaggle after fine-tuning.
"""

import json
import os
from utils.clients import get_client
from utils.test_logs import create_test_log_dir, create_log_file, write_log, write_log_summary
from utils.prompts import system_prompt_no_rag, user_prompt_no_rag
from utils.parser import parse_response

# === CONFIG ===
model_name = "LLaMA-3.1-8B-FT"

config_model = {
    "model_name": "models/LLaMA-3.1-8B-Solana-Audit",  # Fine-tuned adapter
    "type": "local",
}

# For base model testing, change to:
# config_model = {
#     "model_name": "unsloth/Meta-Llama-3.1-8B-Instruct",
#     "type": "local",
# }

client = get_client(config_model)

test_dir = "../../data/test_set"
test_logs_basedir = "../../results/test_logs/no_rag"

test_logs_dir = create_test_log_dir(test_logs_basedir, model_name)

for file in sorted(os.listdir(test_dir)):
    if not file.endswith(".json"):
        continue

    full_path = os.path.join(test_dir, file)

    with open(full_path, "r", encoding="utf-8") as f:
        content = json.load(f)
        code = content["smart_contract"]
        vulnerability = content["vulnerability"]

    log_file = create_log_file(test_logs_dir, file, vulnerability)
    write_log_summary(
        test_logs_dir,
        f"{'-' * 50}ANALYZING {file}-{vulnerability}{'-' * 50}",
    )

    messages = [
        {"role": "system", "content": system_prompt_no_rag},
        {"role": "user", "content": user_prompt_no_rag.format(code=code)},
    ]

    MAX_RETRY = 3
    retry = 0
    vulnerabilities = []

    while retry < MAX_RETRY:
        print(f"[{file}] Attempt {retry + 1}/{MAX_RETRY}...")
        response = client.generate(messages)

        success, vulnerabilities = parse_response(response)

        if success:
            break
        else:
            retry += 1

    write_log(log_file, response, type="Audit")
    write_log_summary(
        test_logs_dir,
        f"Vulnerabilities found in the audit: {vulnerabilities}",
    )

print(f"\nBenchmark complete. Logs saved to {test_logs_dir}")

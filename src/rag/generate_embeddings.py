"""
Step 3: Generate Embeddings for the RAG Knowledge Base
Adapted from Nicola Tortora's generate_embeddings.py for Solana/Rust.

This script:
  1. Loads the RAG contracts from knowledge_base/rag_contracts.jsonl
  2. Uses sentence-transformers (hkunlp/instructor-xl) to encode descriptions
  3. Saves embeddings + metadata to contract_embeddings.json

Run this on Kaggle (or any machine with GPU for faster encoding).

Usage:
  pip install sentence-transformers pandas tqdm
  python generate_embeddings.py
"""

import pandas as pd
from tqdm import tqdm
from sentence_transformers import SentenceTransformer
import numpy as np
import json

# === CONFIG ===
CONTRACT_PATH = "../../data/knowledge_base/rag_contracts.jsonl"
EMBEDDING_MODEL = "hkunlp/instructor-xl"
OUTPUT_JSON = "contract_embeddings.json"

# === 1. LOAD THE EMBEDDING MODEL ===
print(f"Loading embedding model: {EMBEDDING_MODEL}")
model = SentenceTransformer(EMBEDDING_MODEL)


def generate_embeddings():
    # === 2. LOAD RAG CONTRACTS ===
    contracts = []
    with open(CONTRACT_PATH, "r", encoding="utf-8") as f:
        for line in f.readlines():
            contract = json.loads(line)
            contracts.append({
                "id": contract["id"],
                "code": contract["smart_contract"],
                "vulnerability": contract["vulnerability"],
                "description": contract["description"],
                "vulnerable_part": contract["vulnerable_part"],
            })

    print(f"Found {len(contracts)} smart contracts in {CONTRACT_PATH}")

    # === 3. GENERATE EMBEDDINGS ===
    embeddings = []

    for c in tqdm(contracts, desc="Embedding contracts"):
        # Instruction prefix for INSTRUCTOR model (adapted for Solana)
        instruction = (
            "Represent the following functional description "
            "of a Solana smart contract, written in Rust:"
        )
        text_input = [instruction, c["description"]]
        emb = model.encode(text_input)
        embeddings.append(emb)

    embeddings = np.array(embeddings)

    # === 4. SAVE TO JSON ===
    df = pd.DataFrame({
        "id": [c["id"] for c in contracts],
        "vulnerability": [c["vulnerability"] for c in contracts],
        "code": [c["code"] for c in contracts],
        "description": [c["description"] for c in contracts],
        "vulnerable_part": [c["vulnerable_part"] for c in contracts],
        "embedding": [emb for emb in embeddings],
    })
    df.to_json(OUTPUT_JSON, index=False)
    print(f"Saved embeddings to {OUTPUT_JSON}")
    print(f"Total contracts embedded: {len(contracts)}")


generate_embeddings()

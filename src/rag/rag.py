"""
RAG Pipeline: Retrieval and Dynamic Prompt Construction
Adapted from Nicola Tortora's rag.py for Solana/Rust.

This module:
  1. Loads pre-computed embeddings from contract_embeddings.json
  2. Performs cosine similarity search against a query description
  3. Builds a prioritized vulnerability checklist for the audit prompt

Used by: run_benchmark_rag.py during evaluation (Step 5)
"""

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import json
import os

# === CONFIG ===
EMBEDDING_PATH = "./contract_embeddings.json"
EMBEDDING_MODEL = "hkunlp/instructor-xl"
VULN_INFO_PATH = os.path.join(
    os.path.dirname(__file__), "../../data/knowledge_base/vulnerability_info.json"
)

# === LOAD EMBEDDING FILE ===
df = pd.read_json(EMBEDDING_PATH)
df = df.to_dict()

# === LOAD EMBEDDING MODEL ===
print(f"Loading embedding model: {EMBEDDING_MODEL}")
model = SentenceTransformer(EMBEDDING_MODEL)


def search_similarity(query: str, find_duplicates: bool = False) -> list:
    """Search for the most similar contracts in the vector store.

    Args:
        query: Security-focused description of the target contract.
        find_duplicates: If False, returns at most one entry per vulnerability type.

    Returns:
        List of dicts sorted by similarity (descending), each with
        vulnerability, code, vulnerable_part, id, and similarity score.
    """
    num_of_emb = len(df["embedding"])
    instruction = (
        "Represent the following functional description "
        "of a Solana smart contract, written in Rust:"
    )
    query_emb = model.encode([instruction, query])

    embeddings = df["embedding"]

    k_vet = VetOfMax(n_of_max=num_of_emb)

    for index in range(num_of_emb):
        e = embeddings[index]
        e = np.array(e)
        e = e.reshape(1, -1)
        q = query_emb.reshape(1, -1)

        similarity = cosine_similarity(e, q)

        k_vet.insert_sorted_desc(
            {"index": index, "num": f"{similarity[0][0]:.4f}"}
        )

    entries = []
    for k in k_vet.vet_of_max:
        entry = get_contract_info(k["index"])
        entry["similarity"] = k["num"]
        flag = True

        if not find_duplicates:
            for i, e in enumerate(entries):
                if e["vulnerability"] == entry["vulnerability"]:
                    flag = False
                    if entry["similarity"] > e["similarity"]:
                        entries[i] = entry
                        break
                    else:
                        break

        if flag:
            entries.append(entry)

    return entries


def get_contract_info(index: int):
    """Retrieve contract metadata by index."""
    return {
        "vulnerability": df["vulnerability"][index],
        "code": df["code"][index],
        "vulnerable_part": df["vulnerable_part"][index],
        "id": df["id"][index],
    }


def map_vulnerability(name):
    """Map between internal keys and display names."""
    mapping = {
        "Missing Key Check": "missing_key_check",
        "Type Confusion": "type_confusion",
        "CPI Reentrancy": "cpi_reentrancy",
        "Unchecked External Calls": "unchecked_calls",
        "Integer Overflow": "integer_overflow",
        "Bump Seed": "bump_seed",
        "Denial of Service": "dos",
        "missing_key_check": "Missing Key Check",
        "type_confusion": "Type Confusion",
        "cpi_reentrancy": "CPI Reentrancy",
        "unchecked_calls": "Unchecked External Calls",
        "integer_overflow": "Integer Overflow",
        "bump_seed": "Bump Seed",
        "dos": "Denial of Service",
        "not_vulnerable": "Not Vulnerable",
    }
    return mapping.get(name, "Unknown")


def create_rag_checklist(
    rag_contracts: list, num_relevant: int = 3, with_few_shot: bool = True
) -> str:
    """Build a prioritized vulnerability checklist from RAG results.

    Args:
        rag_contracts: List of retrieved contracts sorted by similarity.
        num_relevant: Number of top results to include full details for.
        with_few_shot: If True, include vulnerable code snippets as examples.

    Returns:
        Formatted checklist string to inject into the audit prompt.
    """
    checklist = ""

    info_few_shot = """
    {num}. **{vulnerability}** ({score})
        - **Description:** {description}
        - **Preconditions:** {precondition}
        - **Security check to perform**: {check}
        - **Example Vulnerable Pattern:
          ```rust
    {vuln_part}
          ```
      """

    info_zero_shot = """
    {num}. **{vulnerability}** ({score})
        - **Description:** {description}
        - **Preconditions:** {precondition}
        - **Security check to perform**: {check}
      """

    if with_few_shot:
        info = info_few_shot
    else:
        info = info_zero_shot

    info_no_desc = """
    {num}. **{vulnerability}** ({score})
    """

    with open(VULN_INFO_PATH, "r", encoding="utf-8") as f:
        content = json.load(f)

    for i, c in enumerate(rag_contracts):
        vuln = rag_contracts[i]["vulnerability"]
        vuln_part = rag_contracts[i]["vulnerable_part"]
        score = rag_contracts[i]["similarity"]

        if vuln not in content:
            continue

        data = content[vuln]
        if i < num_relevant:
            checklist += info.format(
                num=i + 1,
                score=score,
                vulnerability=data["name"],
                description=data["description"],
                precondition=data["precondition"],
                check=data["security_check"],
                vuln_part=vuln_part.strip(),
            )
        else:
            checklist += info_no_desc.format(
                num=i + 1,
                score=score,
                vulnerability=data["name"],
            )
    return checklist


# === HELPER CLASS: Sorted Max-Heap ===

def initialize(n: int) -> list:
    return [None] * n


class VetOfMax:
    def __init__(self, n_of_max):
        self.n_of_max = n_of_max
        self.vet_of_max = initialize(n_of_max)

    def insert_sorted_desc(self, index_similarity: dict, verbose: bool = False):
        if verbose:
            print(f"insert_sorted_desc {index_similarity}")

        for i, m in enumerate(self.vet_of_max):
            num = index_similarity["num"]
            if m is None:
                self.vet_of_max[i] = index_similarity
                break
            if m["num"] < num:
                self.vet_of_max[i] = index_similarity
                index_similarity = m

        if verbose:
            print(self.vet_of_max)

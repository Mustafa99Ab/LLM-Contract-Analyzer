"""
Recompute evaluation metrics with corrected alias handling.

This script reads detailed_results.json (produced by the evaluation notebook)
and recomputes Accuracy, Precision, Recall, and F1-Score by properly handling
vulnerability synonyms.

The original parser counted synonyms separately:
  "Bump Seed" and "Bump Seed Canonicalization" were treated as 2 different predictions
  "Denial of Service" and "DoS" were treated as 2 different predictions

This script fixes that by grouping synonyms together.

Usage:
    python recompute_metrics.py detailed_results.json
"""

import json
import sys
from collections import defaultdict


# Vulnerability aliases - terms that refer to the same vulnerability
VULNERABILITY_ALIASES = {
    "Missing Key Check": [
        "missing key check",
        "access control",
    ],
    "Type Confusion": [
        "type confusion",
        "input validation",
    ],
    "CPI Reentrancy": [
        "cpi reentrancy",
        "cpi",
        "reentrancy",
    ],
    "Unchecked External Calls": [
        "unchecked external calls",
        "unchecked calls",
    ],
    "Integer Overflow": [
        "integer overflow",
        "integer underflow",
        "integer flow",
    ],
    "Bump Seed": [
        "bump seed",
        "bump seed canonicalization",
    ],
    "Denial of Service": [
        "denial of service",
        "dos",
    ],
    "Not Vulnerable": [
        "not vulnerable",
        "no security risk",
        "no vulnerabilities",
        "none detected",
    ],
}

# Map the lowercase test file keys to canonical names
GROUND_TRUTH_MAP = {
    "integer_flow": "Integer Overflow",
    "cpi": "CPI Reentrancy",
}


def normalize_predictions(predictions):
    """Map raw predictions to canonical vulnerability names.

    Synonyms are merged, so ["Bump Seed", "Bump Seed Canonicalization"]
    becomes {"Bump Seed"} rather than two separate predictions.
    """
    canonical_set = set()
    for pred in predictions:
        pred_lower = pred.lower().strip()
        for canonical, aliases in VULNERABILITY_ALIASES.items():
            if pred_lower in aliases:
                canonical_set.add(canonical)
                break
    return canonical_set


def compute_metrics(results):
    """Compute classification metrics from a list of test results."""
    tp = fp = tn = fn = 0
    per_vuln = defaultdict(lambda: {"tp": 0, "fp": 0, "tn": 0, "fn": 0})

    for r in results:
        truth = GROUND_TRUTH_MAP.get(r["truth"], r["truth"])
        predictions = normalize_predictions(r["predicted"])

        if not predictions:
            # Model produced no valid prediction
            if truth == "Not Vulnerable":
                tn += 1
                per_vuln[truth]["tn"] += 1
            else:
                fn += 1
                per_vuln[truth]["fn"] += 1
            continue

        if truth in predictions:
            # Truth was correctly identified
            if truth == "Not Vulnerable":
                tn += 1
                per_vuln[truth]["tn"] += 1
                extras = predictions - {"Not Vulnerable"}
                fp += len(extras)
                for e in extras:
                    per_vuln[e]["fp"] += 1
            else:
                tp += 1
                per_vuln[truth]["tp"] += 1
                extras = predictions - {truth, "Not Vulnerable"}
                fp += len(extras)
                for e in extras:
                    per_vuln[e]["fp"] += 1
        else:
            # Truth was missed
            if truth == "Not Vulnerable":
                extras = predictions - {"Not Vulnerable"}
                fp += len(extras)
                for e in extras:
                    per_vuln[e]["fp"] += 1
            else:
                fn += 1
                per_vuln[truth]["fn"] += 1
                wrong = predictions - {"Not Vulnerable"}
                fp += len(wrong)
                for e in wrong:
                    per_vuln[e]["fp"] += 1

    total = tp + fp + tn + fn
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = (
        2 * precision * recall / (precision + recall)
        if (precision + recall) > 0
        else 0
    )
    accuracy = (tp + tn) / total if total > 0 else 0

    return {
        "accuracy": round(accuracy, 4),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1_score": round(f1, 4),
        "confusion_matrix": {"tp": tp, "fp": fp, "tn": tn, "fn": fn},
        "per_vulnerability": dict(per_vuln),
    }


def main(input_path, output_path="evaluation_results_corrected.json"):
    with open(input_path, "r") as f:
        data = json.load(f)

    corrected = {}
    for config_name in ["base_no_rag", "base_rag", "ft_no_rag", "ft_rag"]:
        if config_name in data:
            corrected[config_name] = compute_metrics(data[config_name])

    # Print summary
    print("=" * 70)
    print("EVALUATION METRICS (with alias-aware parser)")
    print("=" * 70)
    for config_name, metrics in corrected.items():
        cm = metrics["confusion_matrix"]
        print(f"\n{config_name.upper().replace('_', ' '):20s}")
        print(f"  Accuracy:  {metrics['accuracy']:.4f}")
        print(f"  Precision: {metrics['precision']:.4f}")
        print(f"  Recall:    {metrics['recall']:.4f}")
        print(f"  F1-Score:  {metrics['f1_score']:.4f}")
        print(f"  TP={cm['tp']}, FP={cm['fp']}, TN={cm['tn']}, FN={cm['fn']}")

    with open(output_path, "w") as f:
        json.dump(corrected, f, indent=2)

    print(f"\nCorrected results saved to: {output_path}")


if __name__ == "__main__":
    input_path = sys.argv[1] if len(sys.argv) > 1 else "detailed_results.json"
    main(input_path)

"""
Step 5c: Calculate evaluation metrics from test logs.
Adapted from Nicola Tortora's metrics.py for Solana/Rust.

Computes: Accuracy, Precision, Recall, F1-Score
Both globally and per vulnerability type.
"""

import json
import os
import re

# Vulnerability key mapping for display
VULN_DISPLAY = {
    "missing_key_check": "Missing Key Check",
    "type_confusion": "Type Confusion",
    "cpi_reentrancy": "CPI Reentrancy",
    "unchecked_calls": "Unchecked External Calls",
    "integer_overflow": "Integer Overflow",
    "bump_seed": "Bump Seed",
    "dos": "Denial of Service",
    "not_vulnerable": "Not Vulnerable",
}


def parse_log(text: str) -> dict:
    """Parse a test log summary and compute metrics."""

    pattern = re.compile(
        r"-{50}ANALYZING solana_[0-9]{1,2}\.json-(.+?)-{50}",
        re.IGNORECASE,
    )

    split = re.split(pattern, text.strip())
    split = [s for s in split if s != ""]

    # Ground truth labels are at odd indices (captured by regex group)
    ground_truth_list = split[::2]
    # Results are at even indices (text between headers)
    results = split[1::2]

    # Initialize per-vulnerability metrics
    single_vuln_metrics = {}
    unique_vulns = set(
        VULN_DISPLAY.get(gt, gt) for gt in ground_truth_list
    )
    for v in unique_vulns:
        single_vuln_metrics[v] = {"tp": 0, "fp": 0, "tn": 0, "fn": 0}

    # Global confusion matrix
    global_metrics = {"tp": 0, "fp": 0, "tn": 0, "fn": 0}

    for i, r in enumerate(results):
        truth = VULN_DISPLAY.get(ground_truth_list[i], ground_truth_list[i])

        local_tp = 0
        local_fp = 0
        local_tn = 0
        local_fn = 0

        for line in r.split("\n"):
            if "Vulnerabilities found in the audit:" in line:
                try:
                    r1 = eval(
                        line.split("Vulnerabilities found in the audit: ")[1]
                    )
                except Exception:
                    r1 = []

                if len(r1) == 0:
                    r1.append("Unknown Vulnerability")

                for vuln in r1:
                    if vuln == truth and vuln != "Not Vulnerable":
                        local_tp += 1
                    if vuln != truth and vuln != "Not Vulnerable":
                        local_fp += 1

        if truth == "Not Vulnerable" and local_fp == 0:
            local_tn += 1
        if truth != "Not Vulnerable" and local_tp == 0:
            local_fn += 1

        # Update global totals
        global_metrics["tp"] += local_tp
        global_metrics["fp"] += local_fp
        global_metrics["tn"] += local_tn
        global_metrics["fn"] += local_fn

        print(
            f"{truth}{'-' * 40}\n"
            f"tp: {local_tp}, fn: {local_fn}, "
            f"fp: {local_fp}, tn: {local_tn}\n"
            f"{'-' * 50}"
        )

        # Update per-class totals
        if truth in single_vuln_metrics:
            single_vuln_metrics[truth]["tp"] += local_tp
            single_vuln_metrics[truth]["fp"] += local_fp
            single_vuln_metrics[truth]["tn"] += local_tn
            single_vuln_metrics[truth]["fn"] += local_fn

    # Compute derived metrics
    tp = global_metrics["tp"]
    fp = global_metrics["fp"]
    fn = global_metrics["fn"]
    tn = global_metrics["tn"]

    total = tp + fp + fn + tn

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = (
        2 * (precision * recall) / (precision + recall)
        if (precision + recall) > 0
        else 0
    )
    accuracy = (tp + tn) / total if total > 0 else 0

    print(f"\n{'=' * 50}")
    print(f"GLOBAL: tp={tp}, fn={fn}, fp={fp}, tn={tn}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1-Score:  {f1:.4f}")
    print(f"Accuracy:  {accuracy:.4f}")
    print(f"{'=' * 50}")

    return {
        "total_samples": len(ground_truth_list),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1_score": round(f1, 4),
        "accuracy": round(accuracy, 4),
        "confusion_matrix": global_metrics,
        "details_by_vulnerability": single_vuln_metrics,
    }


def save_results():
    """Compute metrics for all test logs and save as JSON."""

    test_logs_dir = os.path.join(
        os.path.dirname(__file__), "../../results/test_logs"
    )

    if not os.path.exists(test_logs_dir):
        print(f"No test logs found in {test_logs_dir}")
        return

    for mode in os.listdir(test_logs_dir):
        mode_dir = os.path.join(test_logs_dir, mode)
        if not os.path.isdir(mode_dir):
            continue

        for test in os.listdir(mode_dir):
            log_path = os.path.join(mode_dir, test, "log_summary.txt")

            if not os.path.exists(log_path):
                continue

            print(f"\nProcessing: {mode}/{test}")

            with open(log_path, "r", encoding="utf-8") as f:
                text = f.read()

            results = parse_log(text)

            output = {
                "model_name": test,
                "test_mode": mode,
                "results": results,
            }

            output_dir = os.path.join(
                os.path.dirname(__file__),
                f"../../results/{mode}",
            )
            os.makedirs(output_dir, exist_ok=True)

            output_path = os.path.join(output_dir, f"{test}_results.json")
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(output, f, indent=4)

            print(f"Results saved to: {output_path}")


if __name__ == "__main__":
    save_results()

"""
Utility for managing test log files during evaluation.
Adapted from Nicola Tortora's test_logs.py.
"""

import os
from datetime import datetime


def create_test_log_dir(basedir: str, model_name: str) -> str:
    """Create a timestamped directory for test logs."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_dir = os.path.join(basedir, f"{model_name}_{timestamp}")
    os.makedirs(log_dir, exist_ok=True)
    return log_dir


def create_log_file(log_dir: str, filename: str, vulnerability: str) -> str:
    """Create a log file for a single test case."""
    log_file = os.path.join(log_dir, f"{filename}_{vulnerability}.txt")
    return log_file


def write_log(log_file: str, content: str, type: str = ""):
    """Append content to a log file."""
    with open(log_file, "a", encoding="utf-8") as f:
        if type:
            f.write(f"\n{'=' * 40} {type} {'=' * 40}\n")
        f.write(content)
        f.write("\n")


def write_log_summary(log_dir: str, content: str):
    """Append to the summary log file."""
    summary_file = os.path.join(log_dir, "log_summary.txt")
    with open(summary_file, "a", encoding="utf-8") as f:
        f.write(content + "\n")

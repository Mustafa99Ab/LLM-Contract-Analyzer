"""
Parser for extracting vulnerability verdicts from model responses.
Adapted from Nicola Tortora's parser.py for Solana/Rust vulnerabilities.
"""

import re

# Solana/Rust vulnerability names (all recognized variants)
VULNERABILITIES = [
    "Missing Key Check",
    "Access Control",
    "Type Confusion",
    "Input Validation",
    "CPI Reentrancy",
    "Reentrancy",
    "Unchecked External Calls",
    "Unchecked Calls",
    "Integer Overflow",
    "Integer Underflow",
    "Integer Flow",
    "Bump Seed",
    "Bump Seed Canonicalization",
    "Denial of Service",
    "DoS",
    "Not Vulnerable",
    "No security risk",
    "No vulnerabilities",
    "None detected",
]


def parse_response(response: str) -> tuple:
    """Parse model response to extract vulnerability findings.

    Returns:
        (success, vulnerabilities): success is True if the <final> tag
        was found and at least one known vulnerability was recognized.
    """
    tag_pattern = re.compile(
        r"<final>\s*(.*?)\s*</final>", re.IGNORECASE | re.DOTALL
    )
    match = tag_pattern.search(response)

    if not match:
        return False, []

    content = match.group(1).strip().lower()

    found_vulns = []
    for v in VULNERABILITIES:
        if v.lower() in content:
            found_vulns.append(v)

    if len(found_vulns) > 0:
        return True, found_vulns
    else:
        return False, []

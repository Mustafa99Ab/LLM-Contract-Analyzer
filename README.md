# 🧠 LLM Contract Analyzer

A structured dataset and framework for analyzing smart contracts using Large Language Models (LLMs)

---

## 📌 Overview

**LLM Contract Analyzer** is an open-source project focused on organizing smart contract security samples for training, evaluating, and benchmarking LLMs.
The dataset is designed to help models detect logic bugs, security vulnerabilities, and misconfigurations across different blockchain platforms.

This repository currently includes:

* Organized JSON datasets
* **Two supported platforms**: **Solana** and **Algorand**
* Classification by vulnerability type
* Handcrafted custom samples
* Future support for additional platforms

---

## 🏛️ Academic Affiliation

This project is part of research conducted at:

**HABES Lab — Hardware Assisted and Blockchain Empowered Security Lab**
Computer Science Department
University of Salerno, Italy
[https://habes.cs.unisa.it](https://habes.cs.unisa.it)

---

## 📁 Repository Structure

```
```text
dataset/
├── algorand/
│   └── custom_samples/       # PyTeal samples tailored to OWASP categories
│       ├── algorand_v1_access_control.json
│       ├── algorand_v3_logic_errors.json
│       ├── algorand_v6_unchecked_calls.json
│       ├── algorand_v8_integer_overflow.json
│       └── algorand_v10_dos.json
├── solana/
│   └── custom_samples/       # Rust (Anchor) samples tailored to OWASP categories
│       ├── solana_v1_access_control.json
│       ├── solana_v2_oracle_manipulation.json
│       ├── solana_v3_logic_errors.json
│       ├── solana_v5_reentrancy.json
│       ├── solana_v6_unchecked_calls.json
│       └── ... (complete set v1-v10)
```

Each JSON file contains:

* **instruction** → The task for the LLM
* **input** → Smart contract code
* **output** → Vulnerability classification & explanation
* **meta_platform** → Blockchain platform
* **meta_vuln_type** → Vulnerability type

---

---
## Vulnerability Taxonomy 🗂️

The samples map traditional vulnerabilities to platform-specific implementations. Note that some vulnerabilities (like Reentrancy) manifest differently or are not applicable in Algorand due to its atomic execution model.

| ID | Vulnerability Category | Solana Context (Rust/Anchor) 🦀 | Algorand Context (PyTeal) 🐍 |
| :--- | :--- | :--- | :--- |
| **V1** | Access Control | Missing `Signer` checks, `Owner` validation gaps | Unchecked `Sender`, `RekeyTo` unauthorized logic |
| **V2** | Oracle Manipulation | Unverified `Pyth`/`Switchboard` feeds, Stale prices | N/A (Architecture dependent / Logic) |
| **V3** | Logic Errors | Business logic flaws, incorrect math assumptions | Logic flaws in state transitions |
| **V4** | Input Validation | Missing checks on account data/types | Missing size/type checks on transaction args |
| **V5** | Reentrancy | Cross-Program Invocation (CPI) state inconsistencies | N/A (Mitigated by Atomic Transfers) |
| **V6** | Unchecked Calls | Unverified CPI calls to malicious programs | Unchecked Inner Transactions or `RekeyTo` |
| **V7** | Flash Loan Attacks | Spot price manipulation in AMMs | N/A (Atomic groups mitigate typical exploits) |
| **V8** | Integer Issues | Integer Overflow/Underflow (wrapping) | Mathematical errors in TEAL logic |
| **V9** | Insecure Randomness | Predictable seeds (Clock/Slot) | N/A (VRF is standard) |
| **V10**| Denial of Service (DoS)| PDA collisions, Compute Budget exhaustion | Dynamic Fee abuse, Resource exhaustion |

---

---

## Methodology 🔬

1.  **🧩 Pattern Definition:** Vulnerability patterns were rigorously derived from auditing reports, platform documentation (Anchor Lang docs, Algorand Dev Portal), and academic literature on blockchain security.
2.  **🤖 Synthetic Generation:** Samples were generated to isolate specific security flaws (Negative Samples ❌) and paired with their secure counterparts (Positive Samples ✅).
3.  **✅ Verification:** A structural static analysis (Syntax Check) was performed to ensure code validity:
    * **🐍 PyTeal:** Verified against valid Python/PyTeal AST structure.
    * **🦀 Rust:** Verified for essential Anchor framework macros (e.g., `#[program]`, `Context`).

---


## 🎯 Project Goals

* Build a unified, high-quality dataset for LLM security analysis
* Enable academic and industry research on AI-assisted auditing
* Provide consistent benchmarks across blockchain platforms
* Expand the dataset with multi-platform support

---

## 🔧 Usage

You can load and use the dataset in:

* Google Colab
* Python scripts
* Jupyter / VS Code
* LLM training frameworks (TRL, Axolotl, DSPy…)

**Example (Python):**

```python
import json

with open("solana/solana_v3_logic_errors.json", "r") as f:
    samples = json.load(f)

print(samples[0])
```

---

## 📌 Supported Platforms

### ✅ Currently Available

* **Solana**
* **Algorand**

### 🔜 Coming Soon

* Ethereum
* Cosmos
* NEAR
* Aptos
* Additional chains…

---

## 🤝 Contributing

Researchers and developers are welcome to contribute by:

* Adding new smart contract samples
* Proposing new platforms
* Improving vulnerability labels
* Reporting dataset issues

Open a Pull Request or Issue anytime.

---

## 📜 License

This project is licensed under the **MIT License**.

---

## ⭐ Acknowledgements

Special thanks to the HABES Lab research group and the blockchain security community for supporting open-source datasets.

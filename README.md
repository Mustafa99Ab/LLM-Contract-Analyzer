
<img width="762" height="284" alt="Logo-HABES_SfondoTrasparente" src="https://github.com/user-attachments/assets/3a31c595-c60b-47d7-9967-3a7ef3004921" />

---

# 🧠 LLM Contract Analyzer

A structured dataset and framework for analyzing smart contracts using Large Language Models (LLMs)

---

## 📌 Overview

LLM Contract Analyzer is an open-source project focused on organizing smart contract security samples for training, evaluating, and benchmarking LLMs. The dataset is designed to help models detect logic bugs, security vulnerabilities, and misconfigurations across different blockchain platforms (Non-EVM).

This repository currently includes:
* ✅ Organized JSON datasets
* ✅ Two supported platforms: **Solana** and **Algorand**
* ✅ Classification by vulnerability type (OWASP Top 10)
* ✅ Handcrafted & Validated custom samples
* ✅ Verified external datasets

---

## 🏛️ Academic Affiliation
This project is part of research conducted at:
**HABES Lab — Hardware Assisted and Blockchain Empowered Security Lab**
*Department of Computer Science, University of Salerno, Italy*
[https://habes.cs.unisa.it](https://habes.cs.unisa.it)


---

## 📁 Repository Structure

```
```text
LLM-Contract-Analyzer/
├── algorand/
│   ├── custom_samples/       # Handcrafted PyTeal samples (OWASP tailored)
│   │   ├── algorand_v1_access_control.json
│   │   ├── algorand_v3_logic_errors.json
│   │   ├── algorand_v6_unchecked_calls.json
│   │   ├── algorand_v8_integer_overflow.json
│   │   └── algorand_v10_dos.json
│   │
│   └── external_datasets/    # Verified datasets collected from external sources
│       └── (e.g., audit_reports, benchmarks...)
│
├── solana/
│   ├── custom_samples/       # Handcrafted Rust/Anchor samples (OWASP tailored)
│   │   ├── solana_v1_access_control.json
│   │   ├── solana_v2_oracle_manipulation.json
│   │   ├── solana_v5_reentrancy.json
│   │   └── ...
│   │
│   └── external_datasets/    # Verified datasets collected from external sources
│       └── (e.g., audit_reports, benchmarks...)
│
└── README.md
```

Each JSON file contains:

* **instruction** → The task for the LLM
* **input** → Smart contract code
* **output** → Vulnerability classification & explanation
* **meta_platform** → Blockchain platform
* **meta_vuln_type** → Vulnerability type

---

---

## 📊 Vulnerability Taxonomy
The samples map traditional vulnerabilities to platform-specific implementations. Note that some vulnerabilities (like Reentrancy) manifest differently or are not applicable in Algorand due to its atomic execution model.

| ID | Vulnerability Category | Solana Context (Rust/Anchor) | Algorand Context (PyTeal) |
|----|------------------------|------------------------------|---------------------------|
| **V1** | Access Control | Missing `Signer` checks, Owner validation | Unchecked `Sender`, `RekeyTo` logic |
| **V2** | Price Oracle Manipulation | Unverified `Pyth` feeds, Stale prices | N/A (Architecture dependent) |
| **V3** | Logic Errors | Business logic flaws, incorrect math assumptions | Logic flaws in state transitions |
| **V4** | Input Validation | Account Type Confusion, Missing Data Checks | N/A (Strongly typed / Structural) |
| **V5** | Reentrancy | CPI state inconsistencies | N/A (Atomic Transfers mitigate this) |
| **V6** | Unchecked External Calls | Unverified CPI calls | Unchecked Inner Transactions |
| **V7** | Flash Loan Attacks | Spot price manipulation in AMMs | N/A (Atomic groups mitigate typical exploits) |
| **V8** | Integer Issues | Overflow/Underflow | Mathematical errors in TEAL |
| **V9** | Insecure Randomness | Predictable seeds (Clock/Slot) | N/A (VRF is standard) |
| **V10**| Denial of Service (DoS)| PDA collisions, Compute Budget | Dynamic Fee abuse |

---

---

## 🔬 Methodology

* Pattern Definition: Vulnerability patterns were rigorously derived from auditing reports and academic literature.
* Synthetic Generation: Samples were generated to isolate specific security flaws (Negative Samples) vs. secure code (Positive Samples).
* External Verification: Datasets collected from external sources are reviewed and verified before inclusion in the external_datasets directory.
* Static Analysis: A structural static analysis was performed to ensure code validity:
* PyTeal: Verified against valid Python AST.
* Rust: Verified for essential Anchor macros (#[program], Context).

---


## 🎯 Project Goals

* Build a unified, high-quality dataset for LLM security analysis
* Enable academic and industry research on AI-assisted auditing
* Provide consistent benchmarks across blockchain platforms
* Expand the dataset with multi-platform support

---

🔧 Usage
You can load the dataset in Python/Colab for training frameworks (TRL, Axolotl):

* Google Colab
* Python scripts
* Jupyter / VS Code
* LLM training frameworks (TRL, Axolotl, DSPy…)

**Example (Python):**

```python
import json

# Load Solana Logic Errors dataset
with open("solana/custom_samples/solana_v3_logic_errors.json", "r") as f:
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

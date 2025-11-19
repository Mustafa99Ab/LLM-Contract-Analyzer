<img width="762" height="284" alt="Logo-HABES_SfondoTrasparente" src="https://github.com/user-attachments/assets/3a31c595-c60b-47d7-9967-3a7ef3004921" />

---

# 🧠 LLM Contract Analyzer

A structured dataset and framework for analyzing smart contracts using Large Language Models (LLMs)

---

## 📌 Overview

**LLM Contract Analyzer** is an academic research project developed as part of a bachelor thesis focused on smart contract security and AI-assisted vulnerability detection.
The goal is to build a high-quality, structured dataset that helps LLMs detect logic bugs, security vulnerabilities, and misconfigurations across multiple non-EVM blockchain platforms.

This repository currently includes:

* Organized JSON datasets
* Two supported platforms: **Solana** and **Algorand**
* Samples categorized by OWASP-aligned vulnerability types
* Handcrafted and validated custom samples
* Verified external datasets (audits, benchmarks, reports)

The project will remain **open-source** to encourage collaboration from researchers, students, and developers.

---

## 🏛️ Academic Affiliation

This thesis project is conducted under the supervision of the:

**HABES Lab — Hardware Assisted and Blockchain Empowered Security Lab**
Department of Computer Science
University of Salerno, Italy
[https://habes.cs.unisa.it](https://habes.cs.unisa.it)

Although the author is not physically part of the laboratory, the project is supervised by the professor responsible for the HABES Lab.

---

## 📁 Repository Structure

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

* **instruction** → Task for the LLM
* **input** → Smart contract code
* **output** → Vulnerability classification & explanation
* **meta_platform** → Blockchain platform
* **meta_vuln_type** → Vulnerability type

---

## 📊 Vulnerability Taxonomy

The samples map traditional vulnerability classes to platform-specific implementations.
Some vulnerabilities (e.g., reentrancy) appear only in Solana due to Algorand’s atomic model.

| ID      | Vulnerability Category | Solana (Rust/Anchor)           | Algorand (PyTeal)               |
| ------- | ---------------------- | ------------------------------ | ------------------------------- |
| **V1**  | Access Control         | Missing `Signer`, owner checks | Unchecked `Sender`, Rekey logic |
| **V2**  | Oracle Manipulation    | Unverified Pyth feeds          | N/A                             |
| **V3**  | Logic Errors           | Incorrect business logic       | State transition flaws          |
| **V4**  | Input Validation       | Missing account/type checks    | Mostly structural (N/A)         |
| **V5**  | Reentrancy             | CPI inconsistencies            | N/A                             |
| **V6**  | Unchecked Calls        | Unverified CPI calls           | Unchecked inner transactions    |
| **V7**  | Flash Loans            | AMM price manipulation         | N/A                             |
| **V8**  | Integer Issues         | Overflow/Underflow             | Math errors in TEAL             |
| **V9**  | Insecure Randomness    | Predictable seeds              | N/A                             |
| **V10** | DoS                    | PDA collisions, compute budget | Dynamic fee abuse               |

---

## 🔬 Methodology

* **Pattern Definition**: Extracted from security audits and academic literature
* **Synthetic Samples**: Generated to isolate specific flaws
* **External Verification**: Third-party datasets reviewed before inclusion
* **Static Analysis**:

  * PyTeal → validated through Python AST
  * Rust/Anchor → validated for key macros and structure

---

## 🎯 Project Goals

* Provide a high-quality academic dataset for LLM security analysis
* Support thesis research and reproducible experiments
* Enable collaboration between students and researchers
* Expand vulnerability coverage and platform diversity

---

## 🔧 Usage Example

```python
import json

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

This repository is open for academic and community contributions.
You may contribute by:

* Adding new smart contract samples
* Proposing new platforms
* Improving vulnerability labels
* Reporting dataset issues

Open a Pull Request or Issue at any time.

---

## 🏅 Acknowledgements

This project is part of an undergraduate thesis supervised by the HABES Lab at the University of Salerno.
Special thanks to the supervising professor for guidance and academic support.

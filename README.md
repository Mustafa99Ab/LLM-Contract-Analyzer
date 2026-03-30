
---
<div align="center">

<img width="100%" src="https://github.com/user-attachments/assets/c4ef87e2-7935-4839-827a-3c3561b6b086" alt="University of Salerno Header" />

# 🧠 LLM Contract Analyzer

**A structured framework and dataset for detecting smart contract vulnerabilities using Large Language Models (LLMs).**

[![Status: Work in Progress](https://img.shields.io/badge/Status-Work_in_Progress-orange)](https://github.com/yourusername/LLM-Contract-Analyzer)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform: Solana](https://img.shields.io/badge/Platform-Solana-blueviolet)](https://solana.com/)
[![Platform: Algorand](https://img.shields.io/badge/Platform-Algorand-black)](https://algorand.com/)
[![Research: Thesis](https://img.shields.io/badge/Research-Master's_Thesis-blue)](https://habes.cs.unisa.it)

</div>

---

## 🚧 Project Status: Under Active Development

> **⚠️ Note:** This repository is currently in the **data preparation and validation phase**. The datasets provided here are subject to updates, refinement, and expansion. The final release will be aligned with the completion of the associated thesis.

---

## 📌 Overview

**LLM Contract Analyzer** is an academic research project developed as part of a Master's thesis focused on smart contract security and AI-assisted vulnerability detection.

The primary goal is to establish a high-quality, structured, and labeled dataset that enables Large Language Models (LLMs) to accurately detect logic bugs, security vulnerabilities, and configuration errors across **non-EVM** blockchain architectures (specifically Solana & Algorand).

---

## 📊 Vulnerability Taxonomy & Dataset Scope

The dataset aligns with **OWASP Smart Contract Top 10** standards but is adapted for platform-specific relevance. 

**Current Scope Limitation:**
Certain vulnerability types (V2, V3, V7) are currently **excluded** from the generated dataset as they primarily rely on external off-chain data (Oracles), complex business logic specific to a single DApp, or external DeFi protocol interactions (Flash Loans), which are difficult to capture in isolated static code snippets.

| ID | Vulnerability Category | Solana Status | Algorand Status | Description |
| :--- | :--- | :---: | :---: | :--- |
| **V1** | **Access Control** | ✅ **Included** | ✅ **Included** | Missing signer checks, owner validation errors. |
| **V2** | **Oracle Manipulation** | ❌ *Excluded* | ⚪ N/A | Requires external price feed context. |
| **V3** | **Logic Errors** | ❌ *Excluded* | ✅ **Included** | Generic business logic flaws. |
| **V4** | **Input Validation** | ✅ **Included** | ⚪ N/A | Missing constraints, account confusion. |
| **V5** | **Reentrancy** | ✅ **Included** | ⚪ N/A | CPI inconsistencies (Solana specific). |
| **V6** | **Unchecked Calls** | ✅ **Included** | ✅ **Included** | Unverified CPI calls / ignored return data. |
| **V7** | **Flash Loans** | ❌ *Excluded* | ⚪ N/A | Arbitrage/AMM manipulation (Out of scope). |
| **V8** | **Integer Issues** | ✅ **Included** | ✅ **Included** | Overflow/Underflow (Arithmetic errors). |
| **V9** | **Insecure Randomness** | ✅ **Included** | ⚪ N/A | Predictable seeds / slot hashes. |
| **V10** | **DoS** | ✅ **Included** | ✅ **Included** | PDA collisions, Compute Budget exhaustion. |

> **Legend:**
> * ✅ **Included:** High-quality samples are ready/in-progress.
> * ❌ **Excluded:** Out of scope for the current research phase.
> * ⚪ **N/A:** Not applicable to this blockchain's architecture.

---



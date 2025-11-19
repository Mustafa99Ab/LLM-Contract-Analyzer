
<img width="762" height="284" alt="Logo-HABES_SfondoTrasparente" src="https://github.com/user-attachments/assets/71c13451-6ec6-4768-b8e3-b9e2d317464b" />


🧠 LLM Contract Analyzer


A structured dataset and framework for analyzing smart contracts using Large Language Models (LLMs)


________________________________________
📌 Overview

LLM Contract Analyzer is an open-source project focused on organizing smart contract security samples for training, evaluating, and benchmarking LLMs.

The dataset is designed to help models detect logic bugs, security vulnerabilities, and misconfigurations across different blockchain platforms.


This repository currently includes:

•	Organized JSON datasets

•	Two supported platforms: Solana and Algorand

•	Classification by vulnerability type

•	Handcrafted custom samples

•	Future support for additional platforms

________________________________________


🏛️ Academic Affiliation

This project is part of research conducted at:

HABES Lab — Hardware Assisted and Blockchain Empowered Security Lab

Computer Science Department

University of Salerno, Italy

https://habes.cs.unisa.it

________________________________________

📁 Repository Structure

LLM-Contract-Analyzer/
│
├── algorand/
│   └── custom_samples/
│       ├── algorand_v1_access_control.json
│       ├── algorand_v10_dos.json
│       └── ...
│
├── solana/
│   └── custom_samples/
│       ├── solana_v1_access_control.json
│       ├── solana_v2_oracle_manipulation.json
│       └── ...Each JSON file contains:


•	instruction → The task for the LLM

•	input → Smart contract code

•	output → Vulnerability classification & explanation

•	meta_platform → Blockchain platform

•	meta_vuln_type → Vulnerability type

________________________________________


📊 Vulnerability Taxonomy

The samples map traditional vulnerabilities to platform-specific implementations:

ID	Vulnerability Category	Solana Context (Rust/Anchor)	Algorand Context (PyTeal)

V1	Access Control	Missing Signer checks, Owner validation	Unchecked Sender, RekeyTo logic

V2	Oracle Manipulation	Unverified Pyth feeds, Stale prices	N/A (Architecture dependent)

V5	Reentrancy	CPI state inconsistencies	N/A (Atomic Transfers mitigate this)

V6	Unchecked Calls	Unverified CPI calls	Unchecked Inner Transactions

V8	Integer Issues	Overflow/Underflow	Mathematical errors in TEAL

V10	Denial of Service	PDA collisions, Compute Budget	Dynamic Fee abuse

________________________________________
🎯 Project Goals
•	Build a unified, high-quality dataset for LLM security analysis
•	Enable academic and industry research on AI-assisted auditing
•	Provide consistent benchmarks across blockchain platforms
•	Expand the dataset with multi-platform support
________________________________________
🔧 Usage
You can load and use the dataset in:
•	Google Colab
•	Python scripts
•	Jupyter / VS Code
•	LLM training frameworks (TRL, Axolotl, DSPy…)
Example (Python):
import json

with open("solana/solana_v3_logic_errors.json", "r") as f:
    samples = json.load(f)

print(samples[0])
________________________________________
📌 Supported Platforms
✅ Currently Available
•	Solana
•	Algorand
🔜 Coming Soon
•	Ethereum
•	Cosmos
•	NEAR
•	Aptos
•	Additional chains…
________________________________________
🤝 Contributing
Researchers and developers are welcome to contribute by:
•	Adding new smart contract samples
•	Proposing new platforms
•	Improving vulnerability labels
•	Reporting dataset issues
Open a Pull Request or Issue anytime.
________________________________________
📜 License
This project is licensed under the MIT License.
________________________________________
⭐ Acknowledgements
Special thanks to the HABES Lab research group and the blockchain security community for supporting open-source datasets.


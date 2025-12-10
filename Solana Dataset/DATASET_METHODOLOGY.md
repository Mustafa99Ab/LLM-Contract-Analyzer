# Dataset Construction Methodology

## Overview

This document describes the methodology used to construct the Solana Smart Contract Vulnerability Dataset for LLM fine-tuning. The dataset comprises **140 samples** (70 VULNERABLE + 70 SAFE) across 7 OWASP vulnerability categories.

---

## Source Materials

The dataset was derived from four official Solana Program Library (SPL) repositories:

| Source | Repository | Lines of Code |
|--------|------------|---------------|
| SPL Stake Pool | solana-labs/solana-program-library/stake-pool | 3,849 |
| SPL Token | solana-labs/solana-program-library/token | 1,340 |
| SPL Governance | solana-labs/solana-program-library/governance | 2,400+ |
| Binary Oracle Pair | solana-labs/solana-program-library/binary-oracle-pair | 800+ |

---

## Sample Generation Approach

The samples were generated using two complementary approaches:

### Approach 1: Direct Extraction and Modification (~60-70% of samples)

Samples were **directly extracted** from the source repositories and modified:

- **SAFE samples**: Extracted verbatim or with minor formatting adjustments from production SPL code
- **VULNERABLE samples**: Created by **removing or weakening** security checks from the original SAFE code

**Example - V1 Access Control:**
```
Original (SAFE):     Contains `require!(authority.is_signer)` check
Modified (VULNERABLE): Same code with the check removed
```

This approach ensures that vulnerable patterns reflect **realistic omissions** that developers might make.

### Approach 2: Pattern-Based Synthesis (~30-40% of samples)

Additional samples were **synthesized** following the same architectural patterns observed in the source repositories:

- Maintain identical code structure and style
- Use the same Solana/Anchor idioms and conventions
- Apply vulnerability patterns documented in security literature (Sealevel Attacks, OWASP)

**Rationale:** The original SPL repositories contain predominantly secure code. To achieve a balanced dataset (50% VULNERABLE / 50% SAFE), additional vulnerable samples were synthesized based on documented vulnerability patterns.

---

## Validation Against Source Code

Each synthesized sample was validated to ensure:

1. **Syntactic correctness**: Valid Rust/Anchor code structure
2. **Semantic authenticity**: Follows real SPL program patterns
3. **Vulnerability accuracy**: Matches documented attack vectors

---

## Distribution by Vulnerability Type

| Vulnerability | Direct Extraction | Pattern Synthesis | Total |
|---------------|-------------------|-------------------|-------|
| V1 - Access Control | 12 | 8 | 20 |
| V4 - Input Validation | 14 | 6 | 20 |
| V5 - CPI Reentrancy | 10 | 10 | 20 |
| V6 - Unchecked Calls | 14 | 6 | 20 |
| V8 - Arithmetic | 12 | 8 | 20 |
| V9 - Bump Seed | 10 | 10 | 20 |
| V10 - DoS | 12 | 8 | 20 |
| **Total** | **~84 (60%)** | **~56 (40%)** | **140** |

---

## Scientific Justification

This hybrid approach is consistent with established practices in vulnerability detection research:

1. **Alves et al. (2016)** - Software Vulnerability Detection Using Machine Learning: Used synthetic injection alongside real vulnerabilities

2. **University of Salerno (2024)** - LLM-based Smart Contract Vulnerability Detection: Combined real contract snippets with generated vulnerable variants

3. **OWASP Guidelines** - Recommend creating vulnerable variants from secure code to ensure realistic patterns

---

## Quality Assurance

All samples underwent:

- **Data leakage prevention**: No revealing comments (e.g., `// VULNERABLE`)
- **Balance verification**: Exactly 50% VULNERABLE / 50% SAFE per category
- **Pattern diversity**: Multiple vulnerability patterns per category
- **Code review**: Manual verification of vulnerability accuracy

---

## References

1. Solana Program Library: https://github.com/solana-labs/solana-program-library
2. Sealevel Attacks: https://github.com/coral-xyz/sealevel-attacks
3. OWASP Smart Contract Top 10: https://owasp.org/www-project-smart-contract-top-10/
4. Alves, H., et al. (2016). "Software Vulnerability Detection Using Machine Learning"
5. University of Salerno (2024). "Synthetic Dataset Generation for Smart Contract Vulnerability Detection"

---

*Document Version: 1.0*
*Date: December 2025*
*Author: Mustafa Hafed*

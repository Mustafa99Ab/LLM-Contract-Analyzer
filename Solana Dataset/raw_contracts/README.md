# Raw Smart Contracts - Source Files

This folder contains the original Solana smart contract source code from which the vulnerability dataset was derived.

## Sources

### 1. SPL Stake Pool
- **Folder:** `spl_stake_pool/`
- **Source:** [github.com/solana-labs/solana-program-library/tree/master/stake-pool](https://github.com/solana-labs/solana-program-library/tree/master/stake-pool)
- **Lines:** 3,849
- **Patterns extracted:** MAX_VALIDATORS, pagination, bump seed validation, checked arithmetic

### 2. SPL Token
- **Folder:** `spl_token/`
- **Source:** [github.com/solana-labs/solana-program-library/tree/master/token](https://github.com/solana-labs/solana-program-library/tree/master/token)
- **Lines:** 1,340
- **Patterns extracted:** Owner validation, CPI patterns, authority checks

### 3. SPL Governance
- **Folder:** `spl_governance/`
- **Source:** [github.com/solana-labs/solana-program-library/tree/master/governance](https://github.com/solana-labs/solana-program-library/tree/master/governance)
- **Files:** 8 processor files
- **Patterns extracted:** Access control, signer validation, proposal execution

### 4. Binary Oracle Pair
- **Folder:** `binary_oracle_pair/`
- **Source:** [github.com/solana-labs/solana-program-library/tree/master/binary-oracle-pair](https://github.com/solana-labs/solana-program-library/tree/master/binary-oracle-pair)
- **Files:** processor.rs, state.rs, instruction.rs
- **Patterns extracted:** Bump seed vulnerabilities (user-provided bump)

## Vulnerability Mapping

| Source | V1 | V4 | V5 | V6 | V8 | V9 | V10 |
|--------|----|----|----|----|----|----|-----|
| SPL Stake Pool | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| SPL Token | ✓ | ✓ | - | ✓ | - | - | - |
| SPL Governance | ✓ | ✓ | - | - | ✓ | - | ✓ |
| Binary Oracle Pair | - | - | - | - | - | ✓ | - |

## License

These files are from the official Solana Program Library, licensed under Apache 2.0.

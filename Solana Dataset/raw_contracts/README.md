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

### 5. Token Swap (NEW)
- **Folder:** `token_swap/`
- **Source:** [github.com/solana-labs/solana-program-library/tree/master/token-swap](https://github.com/solana-labs/solana-program-library/tree/master/token-swap)
- **Lines:** 8,377
- **Files:** processor.rs (main), curve/, state.rs, instruction.rs
- **Patterns extracted:** 
  - Account ownership validation (unpack_token_account, unpack_mint)
  - PDA authority with stored bump seed
  - Checked arithmetic (saturating_sub, checked_mul, checked_div)
  - CPI with invoke_signed_wrapper
  - Slippage protection (minimum_amount_out)
  - Extension checks (MintCloseAuthority, TransferFeeConfig)
  - Type confusion prevention (StateWithExtensions unpacking)

## Vulnerability Mapping

| Source | V1 | V4 | V5 | V6 | V8 | V9 | V10 |
|--------|----|----|----|----|----|----|-----|
| SPL Stake Pool | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| SPL Token | ✓ | ✓ | - | ✓ | - | - | - |
| SPL Governance | ✓ | ✓ | - | - | ✓ | - | ✓ |
| Binary Oracle Pair | - | - | - | - | - | ✓ | - |
| **Token Swap** | **✓** | **✓** | **✓** | **✓** | **✓** | **✓** | **✓** |

### Vulnerability Legend
| Code | Vulnerability Type |
|------|-------------------|
| V1 | Missing Key Check (Access Control) |
| V4 | Type Confusion (Input Validation) |
| V5 | CPI Issues (Cross-Program Invocation) |
| V6 | Unchecked Calls |
| V8 | Integer Overflow/Underflow |
| V9 | Bump Seed Canonicalization |
| V10 | Denial of Service |

## Dataset Statistics

| Source | Lines of Code | Samples Generated |
|--------|---------------|-------------------|
| SPL Stake Pool | 3,849 | 40 |
| SPL Token | 1,340 | 30 |
| SPL Governance | 2,400+ | 30 |
| Binary Oracle Pair | 800+ | 40 |
| **Token Swap** | **8,377** | **42** |
| **Total** | **~16,766** | **182** |

## License

These files are from the official Solana Program Library, licensed under Apache 2.0.

---

*Last Updated: December 2024*

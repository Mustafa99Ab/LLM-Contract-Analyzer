# Raw Smart Contracts - Source Files

This folder contains the original Solana smart contract source code from which the vulnerability dataset was derived.

## Sources

### 1. SPL Stake Pool
- **File:** `SPL_Stake_Pool.txt`
- **Source:** [github.com/solana-program/stake-pool](https://github.com/solana-program/stake-pool/blob/main/program/src/processor.rs)
- **Lines:** 3,783
- **Samples:** 32
- **Patterns extracted:** MAX_VALIDATORS pagination, bump seed validation, checked arithmetic, stake delegation CPI, fee calculation

### 2. SPL Token
- **File:** `SPL_Token.txt`
- **Source:** [github.com/solana-program/token](https://github.com/solana-program/token/blob/main/program/src/processor.rs)
- **Lines:** 1,340
- **Samples:** 20
- **Patterns extracted:** Owner validation, authority checks, freeze/thaw, checked lamport transfers

### 3. Associated Token Account
- **File:** `Associated_Token_Account.txt`
- **Source:** [github.com/solana-program/associated-token-account](https://github.com/solana-program/associated-token-account/blob/main/program/src/processor.rs)
- **Lines:** 270
- **Samples:** 14
- **Patterns extracted:** PDA derivation, idempotent creation, nested account recovery

### 4. Binary Oracle Pair
- **File:** `Binary_Oracle_Pair.txt`
- **Source:** [github.com/solana-labs/solana-program-library/tree/master/binary-oracle-pair](https://github.com/solana-labs/solana-program-library/blob/master/binary-oracle-pair/program/src/processor.rs)
- **Lines:** 560
- **Samples:** 16
- **Patterns extracted:** User-provided bump seed (real V9 vulnerability), deposit/withdraw CPI ordering, decider authorization

### 5. Token Swap
- **File:** `Token_Swap.txt`
- **Source:** [github.com/solana-labs/solana-program-library/tree/master/token-swap](https://github.com/solana-labs/solana-program-library/blob/master/token-swap/program/src/processor.rs)
- **Lines:** 8,377
- **Samples:** 24
- **Patterns extracted:** Account ownership validation, PDA authority with stored bump, checked arithmetic, CPI with invoke_signed_wrapper, slippage protection, check_accounts pattern

### 6. Token Lending
- **File:** `Token_Lending.txt`
- **Source:** [github.com/solana-labs/solana-program-library/tree/master/token-lending](https://github.com/solana-labs/solana-program-library/blob/master/token-lending/program/src/processor.rs)
- **Lines:** 2,041
- **Samples:** 33
- **Patterns extracted:** Reserve staleness checks, oracle validation, flash loan repayment verification, obligation health checks, market owner authorization

### 7. Single Pool
- **File:** `Single_Pool.txt`
- **Source:** [github.com/solana-program/single-pool](https://github.com/solana-program/single-pool/blob/main/program/src/processor.rs)
- **Lines:** 1,812
- **Samples:** 29
- **Patterns extracted:** Generic PDA checker (check_pool_pda), 5-PDA initialization, vote account validation, stake split/merge/authorize CPI ordering, metadata update authorization

### 8. Token-2022
- **File:** `Token-2022.txt`
- **Source:** [github.com/solana-program/token-2022](https://github.com/solana-program/token-2022/blob/main/program/src/processor.rs)
- **Lines:** 10,167
- **Samples:** 16
- **Patterns extracted:** Extension-aware account initialization, transfer hooks, CPI guard, permanent delegate warnings, checked supply/amount arithmetic

### 9. Name Service
- **File:** `Name_Service.txt`
- **Source:** [github.com/solana-labs/solana-program-library/tree/master/name-service](https://github.com/solana-labs/solana-program-library/blob/master/name-service/program/src/processor.rs)
- **Lines:** 280
- **Samples:** 14
- **Patterns extracted:** get_seeds_and_key PDA derivation, parent name ownership chain, class-based authorization, realloc with rent handling, data zeroing on close

### 10. Binary Option
- **File:** `Binary_Option.txt`
- **Source:** [github.com/solana-labs/solana-program-library/tree/master/binary-option](https://github.com/solana-labs/solana-program-library/blob/master/binary-option/program/src/processor.rs)
- **Lines:** 744
- **Samples:** 15
- **Patterns extracted:** Unchecked n*price multiplication (real V8 vulnerability), burn-then-transfer CPI ordering, escrow PDA authority, settle/collect state machine

### 11. Stateless Asks
- **File:** `Stateless_Asks.txt`
- **Source:** [github.com/solana-labs/solana-program-library/tree/master/stateless-asks](https://github.com/solana-labs/solana-program-library/blob/master/stateless-asks/program/src/processor.rs)
- **Lines:** 399
- **Samples:** 9
- **Patterns extracted:** User-provided bump with create_program_address (real V9 vulnerability), delegation amount validation, atomic maker-taker swap, checked creator fee arithmetic

### 12. Governance
- **Files:** `process_execute_transaction.rs`, `process_cast_vote.rs`, `process_create_proposal.rs`, `process_create_realm.rs`, `process_deposit_governing_tokens.rs`, `process_withdraw_governing_tokens.rs`, `process_set_realm_authority.rs`
- **Source:** [github.com/solana-labs/solana-program-library/tree/master/governance/program/src/processor](https://github.com/solana-labs/solana-program-library/tree/master/governance/program/src/processor)
- **Lines:** ~600 (7 files)
- **Samples:** 35
- **Patterns extracted:** Dual PDA signing (governance + treasury), voter weight thresholds, proposal count limits, VoteAlreadyExists prevention, realm authority transfer, transfer-then-update CPI ordering

### 13. Token Upgrade
- **File:** `token-upgrade.rs`
- **Source:** [github.com/solana-labs/solana-program-library/tree/master/token-upgrade](https://github.com/solana-labs/solana-program-library/blob/master/token-upgrade/program/src/processor.rs)
- **Lines:** 170
- **Samples:** 8
- **Patterns extracted:** 5 check_owner calls, burn-then-transfer atomic exchange, decimals mismatch check, escrow balance validation, data borrow/drop before CPI

### 14. Record
- **File:** `record.rs`
- **Source:** [github.com/solana-program/record](https://github.com/solana-program/record/blob/main/program/src/processor.rs)
- **Lines:** 173
- **Samples:** 12
- **Patterns extracted:** check_authority (key match + signer), bytemuck typed deserialization, saturating_add for write bounds, checked_add for realloc size, re-initialization prevention

### 15. Feature Proposal
- **File:** `feature-proposal.rs`
- **Source:** [github.com/solana-program/feature-proposal](https://github.com/solana-program/feature-proposal/blob/main/program/src/processor.rs)
- **Lines:** 291
- **Samples:** 8
- **Patterns extracted:** 4 PDA derivations with verification, deadline + threshold acceptance criteria, graceful expiration handling, feature-id assignment via invoke_signed

---

## Vulnerability Mapping

| Source | V1 | V4 | V5 | V6 | V8 | V9 | V10 |
|--------|:--:|:--:|:--:|:--:|:--:|:--:|:---:|
| SPL Stake Pool | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| SPL Token | ✓ | ✓ | - | - | ✓ | - | ✓ |
| Associated Token Account | ✓ | ✓ | ✓ | ✓ | - | ✓ | - |
| Binary Oracle Pair | ✓ | ✓ | ✓ | - | - | ✓ | - |
| Token Swap | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Token Lending | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Single Pool | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Token-2022 | ✓ | ✓ | ✓ | - | ✓ | - | ✓ |
| Name Service | ✓ | ✓ | - | ✓ | ✓ | ✓ | ✓ |
| Binary Option | ✓ | ✓ | ✓ | - | ✓ | ✓ | ✓ |
| Stateless Asks | - | ✓ | ✓ | ✓ | ✓ | ✓ | - |
| Governance | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Token Upgrade | - | ✓ | ✓ | ✓ | - | ✓ | - |
| Record | ✓ | ✓ | - | ✓ | ✓ | - | ✓ |
| Feature Proposal | - | - | - | ✓ | - | ✓ | ✓ |

### Vulnerability Legend

| Code | Vulnerability Type |
|------|-------------------|
| V1 | Missing Key Check (Access Control) |
| V4 | Type Confusion (Input Validation) |
| V5 | CPI Reentrancy (Cross-Program Invocation) |
| V6 | Unchecked External Calls |
| V8 | Integer Overflow/Underflow |
| V9 | Bump Seed Canonicalization |
| V10 | Denial of Service |

---

## Real Vulnerabilities Discovered

During dataset construction, the following **real vulnerabilities** were identified in the source contracts:

| Contract | Vulnerability | Type | Description |
|----------|--------------|------|-------------|
| Stateless Asks | `bump_seed` from user input (L97) | V9 | `create_program_address` with user-provided bump instead of `find_program_address` |
| Binary Option | Unchecked `n * price` (L331, L339) | V8 | `n * sell_price` and `n * buy_price` without `checked_mul` |
| Binary Oracle Pair | `bump_seed` from user (L159) | V9 | User-provided bump stored and used for PDA derivation |
| Binary Oracle Pair | Inconsistent amounts (L372) | V4 | `token_amount` vs `pool_amount` inconsistency in deposit |

---

## Dataset Statistics

| Source | Lines of Code | Samples Generated |
|--------|:-------------:|:-----------------:|
| SPL Stake Pool | 3,783 | 32 |
| SPL Token | 1,340 | 20 |
| Associated Token Account | 270 | 14 |
| Binary Oracle Pair | 560 | 16 |
| Token Swap | 8,377 | 24 |
| Token Lending | 2,041 | 33 |
| Single Pool | 1,812 | 29 |
| Token-2022 | 10,167 | 16 |
| Name Service | 280 | 14 |
| Binary Option | 744 | 15 |
| Stateless Asks | 399 | 9 |
| Governance | ~600 | 35 |
| Token Upgrade | 170 | 8 |
| Record | 173 | 12 |
| Feature Proposal | 291 | 8 |
| **Total** | **~30,807** | **285** |

---

## License

These files are from the official Solana Program Library and Solana Program repositories, licensed under Apache 2.0.

---

*Last Updated: April 2026*
*Author: Mustafa Hafed*

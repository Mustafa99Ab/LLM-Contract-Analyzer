# Dataset Sources Documentation — Batch 2

## Contracts in This Batch

| # | Contract | Repository | File | Lines of Code |
|---|----------|------------|------|---------------|
| 3 | Associated Token Account | solana-program/associated-token-account | program/src/processor.rs | 270 |
| 4 | Binary Oracle Pair | solana-labs/solana-program-library/binary-oracle-pair | program/src/processor.rs | 594 |

**Repository URLs:**
- Associated Token Account: https://github.com/solana-program/associated-token-account/blob/main/program/src/processor.rs
- Binary Oracle Pair: https://github.com/solana-labs/solana-program-library/blob/master/binary-oracle-pair/program/src/processor.rs

---

## Extraction Methods

| Method | Description | Verification |
|--------|-------------|--------------|
| **direct extraction** | Code copied verbatim from source, may be simplified for length | Compare with source at specified lines |
| **extracted and simplified** | Core logic preserved, boilerplate removed for training clarity | Key validation patterns match source |
| **modified from source** | Security checks removed to create VULNERABLE variant | Diff against SAFE version shows exact removals |

---

## Contract 3: Associated Token Account

**Source:** `solana-program/associated-token-account/program/src/processor.rs` (270 lines)
**URL:** https://github.com/solana-program/associated-token-account/blob/main/program/src/processor.rs

### V9 — Bump Seed Canonicalization

#### Sample 1: process_create_associated_token_account — SAFE
- **Function:** `process_create_associated_token_account` (lines 69–149)
- **Extraction:** extracted and simplified — kept PDA derivation from lines 82–93
- **Security pattern:** `get_associated_token_address_and_bump_seed_internal()` uses `find_program_address()` internally. Address verified before use.

#### Sample 2: process_create_associated_token_account — VULNERABLE
- **Based on:** Same function, lines 69–149
- **Extraction:** modified from source
- **What was changed:** Replaced `get_associated_token_address_and_bump_seed_internal` (L82, uses find_program_address) with `create_program_address` accepting user-provided `bump_seed` parameter
- **Resulting vulnerability:** Multiple token accounts per wallet/mint pair with non-canonical bumps

#### Sample 3: process_recover_nested (triple PDA verification) — SAFE
- **Function:** `process_recover_nested` (lines 152–270)
- **Extraction:** extracted and simplified — kept triple PDA verification from lines 161–200
- **Security pattern:** Owner, nested, and destination addresses all derived via `find_program_address` and verified

### V1 — Access Control (Missing Key Check)

#### Sample 4: process_recover_nested (ownership chain) — SAFE
- **Function:** `process_recover_nested` (lines 152–270)
- **Extraction:** extracted and simplified — kept signer check (L203) and ownership chain (L208–243)
- **Security patterns:** wallet is_signer, owner mint ownership, owner ATA ownership, nested ATA ownership

#### Sample 5: process_recover_nested — VULNERABLE
- **Based on:** Same function, lines 152–270
- **Extraction:** modified from source
- **What was removed:** wallet is_signer check (L203–206), all ownership verification (L208–243), mint ownership check (L207)
- **Resulting vulnerability:** Anyone can recover nested tokens to arbitrary destination

### V6 — Unchecked External Calls

#### Sample 6: process_create CPI chain — SAFE
- **Function:** `process_create_associated_token_account` (lines 120–149)
- **Extraction:** extracted and simplified — kept CPI chain with `?` propagation
- **Security pattern:** All three CPIs (create_pda, init_immutable_owner, init_account3) use `?`

#### Sample 7: process_recover_nested transfer+close — SAFE
- **Function:** `process_recover_nested` (lines 248–270)
- **Extraction:** direct extraction of CPI portion
- **Security pattern:** Both transfer_checked and close_account use `?`

#### Sample 8: process_recover_nested — VULNERABLE
- **Based on:** Same function, lines 248–270
- **Extraction:** modified from source
- **What was changed:** Changed transfer invoke_signed from `?` to `let _ =` (error discarded)
- **Resulting vulnerability:** Close executes even if transfer fails — tokens lost permanently

### V5 — CPI Reentrancy

#### Sample 9: process_recover_nested transfer-then-close — SAFE
- **Function:** `process_recover_nested` (lines 226–270)
- **Extraction:** extracted and simplified — kept transfer-then-close ordering
- **Security pattern:** Transfer before close prevents use of closed account

#### Sample 10: process_recover_nested — VULNERABLE
- **Based on:** Same function, lines 248–270
- **Extraction:** modified from source
- **What was changed:** Reversed CPI order — close_account before transfer_checked
- **Resulting vulnerability:** Account destroyed before transfer, tokens lost

### V4 — Input Validation (Type Confusion)

#### Sample 11: CreateIdempotent validation — SAFE
- **Function:** `process_create_associated_token_account` (lines 94–115)
- **Extraction:** extracted and simplified — kept idempotent validation logic
- **Security patterns:** Owner match, mint match, system_program ownership check for uninitialized

---

## Contract 4: Binary Oracle Pair

**Source:** `solana-labs/solana-program-library/binary-oracle-pair/program/src/processor.rs` (594 lines)
**URL:** https://github.com/solana-labs/solana-program-library/blob/master/binary-oracle-pair/program/src/processor.rs

### V9 — Bump Seed Canonicalization

#### Sample 12: authority_id + process_init_pool — VULNERABLE (REAL VULNERABILITY)
- **Function:** `authority_id` (lines 29–36) + `process_init_pool` (lines 185–305)
- **Extraction:** direct extraction and simplified
- **This is a REAL vulnerability in the original code:** `bump_seed` comes from instruction data (line 190) and `authority_id` uses `create_program_address` (line 34) instead of `find_program_address`
- **Impact:** Non-canonical bumps can create phantom pool authorities

#### Sample 13: authority_id + process_init_pool — SAFE (fixed version)
- **Based on:** Same functions
- **Extraction:** modified from source
- **What was changed:** Replaced `create_program_address` with `find_program_address`, removed user-provided bump_seed parameter
- **Fix:** Bump is now derived canonically

### V6 — Unchecked External Calls

#### Sample 14: mint helper — VULNERABLE (REAL CODE SMELL)
- **Function:** `mint` (lines 94–126)
- **Extraction:** direct extraction
- **Real issue:** `.unwrap()` on instruction creation (line 117) instead of `?`

#### Sample 15: mint helper — SAFE (fixed version)
- **Based on:** Same function
- **Extraction:** modified from source
- **What was changed:** Replaced `.unwrap()` with `?`

#### Sample 16: transfer helper — VULNERABLE (REAL CODE SMELL)
- **Function:** `transfer` (lines 39–92)
- **Extraction:** direct extraction
- **Real issue:** Both code paths use `.unwrap()` (lines 64, 83)

### V5 — CPI Reentrancy

#### Sample 17: process_deposit transfer-then-mint — SAFE
- **Function:** `process_deposit` (lines 307–377)
- **Extraction:** direct extraction
- **Security pattern:** Deposit transfer executes before PASS/FAIL mint

#### Sample 18: process_deposit — VULNERABLE
- **Based on:** Same function
- **Extraction:** modified from source
- **What was changed:** Reversed CPI order — mint before transfer (original: transfer L344, mint L356)
- **Resulting vulnerability:** User gets tokens before depositing

#### Sample 19: process_withdraw burn-then-transfer — SAFE
- **Function:** `process_withdraw` (lines 379–520)
- **Extraction:** extracted from Decision::Pass branch (lines 421–444)
- **Security pattern:** PASS tokens burned before deposit returned

#### Sample 20: process_withdraw — VULNERABLE
- **Based on:** Same function
- **Extraction:** modified from source
- **What was changed:** Reversed — transfer before burn (original: burn L423, transfer L435)
- **Resulting vulnerability:** Recursive withdrawal drains pool

### V1 — Access Control (Missing Key Check)

#### Sample 21: process_decide — SAFE
- **Function:** `process_decide` (lines 522–560)
- **Extraction:** direct extraction
- **Security patterns:** decider key match (L536), is_signer (L540), already-decided check (L544), slot window (L548)

#### Sample 22: process_decide — VULNERABLE
- **Based on:** Same function
- **Extraction:** modified from source
- **What was removed:** Key check (L536–538), signer check (L540–542), slot validation (L548–551)
- **Resulting vulnerability:** Anyone can decide pool outcome

### V4 — Input Validation (Type Confusion)

#### Sample 23: process_withdraw (inconsistent amounts) — VULNERABLE (REAL BUG)
- **Function:** `process_withdraw` Undecided branch (lines 471–516)
- **Extraction:** direct extraction
- **This is a REAL bug:** `possible_withdraw_amount` (min of amount, pass, fail) used for PASS burn (L485) but raw `amount` used for FAIL burn (L498) and transfer (L509)

#### Sample 24: process_deposit validation — SAFE
- **Function:** `process_deposit` (lines 307–341)
- **Extraction:** extracted and simplified
- **Security patterns:** Zero amount rejection (L327), slot window check (L333), authority verification (L337)

---

## Verification Instructions

To verify any sample:

1. Open the source URL listed in the contract section above
2. Navigate to the function name and line numbers specified
3. For **SAFE** samples: confirm the security patterns listed are present in the original code
4. For **VULNERABLE** samples: confirm the "What was removed" items are present in the original but absent in the sample

---

## Batch 2 Statistics

| Metric | Value |
|--------|-------|
| Total samples | 24 |
| SAFE samples | 13 |
| VULNERABLE samples | 11 |
| Source contracts | 2 |
| Vulnerability types covered | V1, V4, V5, V6, V9 |

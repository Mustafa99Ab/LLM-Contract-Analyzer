# Dataset Sources Documentation — Batch 4

## Contracts in This Batch

| # | Contract | Repository | File | Lines of Code |
|---|----------|------------|------|---------------|
| 7 | Single Pool | solana-program/single-pool | program/src/processor.rs | 1,812 |
| 8 | Token-2022 | solana-program/token-2022 | program/src/processor.rs | 10,167 |

**Repository URLs:**
- Single Pool: https://github.com/solana-program/single-pool/blob/main/program/src/processor.rs
- Token-2022: https://github.com/solana-program/token-2022/blob/main/program/src/processor.rs

---

## Extraction Methods

| Method | Description | Verification |
|--------|-------------|--------------|
| **direct extraction** | Code copied verbatim from source, may be simplified for length | Compare with source at specified lines |
| **extracted and simplified** | Core logic preserved, boilerplate removed for training clarity | Key validation patterns match source |
| **modified from source** | Security checks removed to create VULNERABLE variant | Diff against SAFE version shows exact removals |

---

## Contract 7: Single Pool

**Source:** `solana-program/single-pool/program/src/processor.rs` (1,812 lines)
**URL:** https://github.com/solana-program/single-pool/blob/main/program/src/processor.rs

### V8 — Integer Overflow/Underflow

#### Sample 1: calculate_deposit_amount (checked_mul/div) — SAFE
- **Function:** `calculate_deposit_amount` (lines 44–59)
- **Extraction:** direct extraction
- **Security patterns:** u128 promotion, checked_mul, checked_div, u64::try_from, Option return

#### Sample 2: calculate_deposit_amount — VULNERABLE
- **Based on:** Same function, lines 44–59
- **What was changed:** Replaced u128 promotion with u64 arithmetic, replaced checked_mul/checked_div with unchecked * and /, removed u64::try_from, changed return to u64
- **Resulting vulnerability:** Silent overflow on large stake × supply products

#### Sample 3: calculate_withdraw_amount (checked arithmetic) — SAFE
- **Function:** `calculate_withdraw_amount` (lines 63–75)
- **Extraction:** direct extraction
- **Security patterns:** u128 checked_mul, denominator zero check, dust protection (returns 0 if numerator < denominator), u64::try_from

#### Sample 4: process_deposit_stake (checked_sub chain) — SAFE
- **Function:** `process_deposit_stake` (lines 931–1088)
- **Extraction:** extracted and simplified — kept checked_sub chains (L988–996, L1032–1042), zero deposit check (L1059–1061)

### V10 — Denial of Service

#### Sample 5: process_deposit_stake (zero/self-deposit checks) — SAFE
- **Function:** `process_deposit_stake` (lines 931–1088)
- **Extraction:** extracted and simplified — kept self-deposit prevention (L973–980), zero token check (L1059–1061)

#### Sample 6: process_withdraw_stake (size limits) — SAFE
- **Function:** `process_withdraw_stake` (lines 1091–1204)
- **Extraction:** extracted and simplified — kept withdrawal size validation (L1160–1167), self-stake prevention (L1135–1142), burn-then-split ordering

#### Sample 7: process_withdraw_stake — VULNERABLE
- **Based on:** Same function, lines 1091–1204
- **What was removed:** WithdrawalTooSmall check (L1160–1162), WithdrawalTooLarge check (L1165–1167), self-stake prevention (L1135–1142)
- **Resulting vulnerability:** Pool can be drained entirely, leaving it unusable

### V5 — CPI Reentrancy

#### Sample 8: process_deposit_stake (merge-then-mint) — SAFE
- **Function:** `process_deposit_stake` (lines 1001–1072)
- **Extraction:** extracted and simplified — kept merge-then-mint CPI ordering (merge L1013–1021, mint L1064–1072), post-merge sanity check (L1045–1047)

#### Sample 9: process_deposit_stake — VULNERABLE
- **Based on:** Same function
- **What was changed:** Reversed CPI order — token_mint_to before stake_merge, removed post-merge sanity check
- **Resulting vulnerability:** Tokens minted before stake consumed, enabling reentrancy drain

#### Sample 10: process_withdraw_stake (burn-then-split-then-authorize) — SAFE
- **Function:** `process_withdraw_stake` (lines 1170–1198)
- **Extraction:** extracted and simplified — kept burn-then-split-then-authorize ordering

### V6 — Unchecked External Calls

#### Sample 11: token_mint_to (? propagation) — SAFE
- **Function:** `token_mint_to` (lines 502–529)
- **Extraction:** direct extraction
- **Security pattern:** ? on instruction creation, invoke_signed returns Result

#### Sample 12: token_burn (? propagation) — SAFE
- **Function:** `token_burn` (lines 531–558)
- **Extraction:** direct extraction
- **Security pattern:** Same as token_mint_to

#### Sample 13: stake_split (.last().unwrap()) — VULNERABLE (REAL CODE SMELL)
- **Function:** `stake_split` (lines 390–413)
- **Extraction:** direct extraction
- **Real issue:** `.last().unwrap()` on instruction vector (L409) panics if vector is empty

### V9 — Bump Seed Canonicalization

#### Sample 14: check_pool_pda (generic PDA checker) — SAFE
- **Function:** `check_pool_pda` (lines 219–240)
- **Extraction:** direct extraction
- **Security pattern:** Uses find_program_address via pda_lookup_fn, derives and verifies canonical address, returns bump

#### Sample 15: process_initialize_pool (5 PDA checks) — SAFE
- **Function:** `process_initialize_pool` (lines 560–596)
- **Extraction:** extracted and simplified — kept all 5 PDA checks (pool, stake, mint, stake_authority, mint_authority) plus program checks

### V4 — Input Validation

#### Sample 16: check_vote_account (discriminator validation) — SAFE
- **Function:** `check_vote_account` (lines 243–258)
- **Extraction:** direct extraction
- **Security patterns:** Vote program ownership, discriminator parsing, legacy version rejection

### V1 — Access Control

#### Sample 17: process_update_pool_token_metadata (withdrawer auth) — SAFE
- **Function:** `process_update_pool_token_metadata` (lines 1288–1372)
- **Extraction:** extracted and simplified — kept vote account check, pool-vote link, withdrawer extraction and match, signer check

---

## Contract 8: Token-2022

**Source:** `solana-program/token-2022/program/src/processor.rs` (10,167 lines)
**URL:** https://github.com/solana-program/token-2022/blob/main/program/src/processor.rs

### V8 — Integer Overflow/Underflow

#### Sample 18: process_transfer (checked arithmetic) — SAFE
- **Function:** `process_transfer` (lines 329–600)
- **Extraction:** extracted and simplified — kept checked_sub for source (L535–538), checked_sub for fee (L539–541), checked_add for destination (L542–545), checked_add for withheld_amount (L548–550)

#### Sample 19: process_transfer — VULNERABLE
- **Based on:** Same function
- **What was changed:** Replaced checked_sub/checked_add with unchecked -/+, removed InsufficientFunds check (L362–364)
- **Resulting vulnerability:** Balance underflow/overflow, drain without sufficient tokens

#### Sample 20: process_mint_to (checked_add) — SAFE
- **Function:** `process_mint_to` (lines 1022–1113)
- **Extraction:** extracted and simplified — kept checked_add for amount (L1102–1105) and supply (L1107–1110), validate_owner, frozen/native/mint checks

#### Sample 21: process_burn (checked_sub) — SAFE
- **Function:** `process_burn` (lines 1115–1286)
- **Extraction:** extracted and simplified — kept InsufficientFunds (L1192–1194), checked_sub for amount (L1276–1279) and supply (L1280–1283)

### V10 — Denial of Service

#### Sample 22: process_close_account (non-zero balance check) — SAFE
- **Function:** `process_close_account` (lines 1288–1400)
- **Extraction:** extracted and simplified — kept self-close prevention (L1298–1300), non-zero balance check (L1309–1311), CPI guard, checked_add for lamports

### V5 — CPI Reentrancy

#### Sample 23: process_transfer (CPI guard + transfer hook flags) — SAFE
- **Function:** `process_transfer` (lines 329–600)
- **Extraction:** extracted and simplified — kept CPI guard check (L445–456), transfer hook flag mechanism (L575–593)

### V4 — Input Validation

#### Sample 24: _process_initialize_mint (comprehensive validation) — SAFE
- **Function:** `_process_initialize_mint` (lines 99–145)
- **Extraction:** direct extraction
- **Security patterns:** Program ownership, rent exemption, unpack_uninitialized, extension validation, frozen-without-freeze prevention

#### Sample 25: _process_initialize_mint — VULNERABLE
- **Based on:** Same function
- **What was removed:** check_program_account (L111), rent exemption (L119–121), extension size validation (L125–127), combination check (L128), frozen-without-freeze (L130–136)
- **Resulting vulnerability:** Cross-program initialization, invalid extensions, non-rent-exempt mints

#### Sample 26: _process_initialize_account (dual validation) — SAFE
- **Function:** `_process_initialize_account` (lines 168–253)
- **Extraction:** extracted and simplified — kept dual check_program_account, rent, mint validation, extension requirements, default state handling

### V1 — Access Control

#### Sample 27: process_transfer (three-way authority validation) — SAFE
- **Function:** `process_transfer` (lines 329–502)
- **Extraction:** extracted and simplified — kept validate_owner for permanent delegate (L458–464), delegate (L472–491), and owner (L494–500), CPI guard, frozen check

#### Sample 28: process_transfer — VULNERABLE
- **Based on:** Same function
- **What was removed:** All validate_owner calls (L458–500), frozen check (L358–360), check_program_account (L352–353), CPI guard (L445–456), mint mismatch check (L521–523)
- **Resulting vulnerability:** Anyone can transfer tokens from any account

---

## Verification Instructions

To verify any sample:

1. Open the source URL listed in the contract section above
2. Navigate to the function name and line numbers specified
3. For **SAFE** samples: confirm the security patterns listed are present in the original code
4. For **VULNERABLE** samples: confirm the "What was removed/changed" items are present in the original but absent in the sample

---

## Batch 4 Statistics

| Metric | Value |
|--------|-------|
| Total samples | 28 |
| SAFE samples | 21 |
| VULNERABLE samples | 7 |
| Source contracts | 2 |
| Vulnerability types covered | V1, V4, V5, V6, V8, V9, V10 |

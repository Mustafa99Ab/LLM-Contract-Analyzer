# Dataset Sources Documentation — Batch 1

## Contracts in This Batch

| # | Contract | Repository | File | Lines of Code |
|---|----------|------------|------|---------------|
| 1 | SPL Stake Pool | solana-program/stake-pool | program/src/processor.rs | 3,783 |
| 2 | SPL Token | solana-program/token | program/src/processor.rs | 1,347 |

**Repository URLs:**
- Stake Pool: https://github.com/solana-program/stake-pool/blob/main/program/src/processor.rs
- Token: https://github.com/solana-program/token/blob/main/program/src/processor.rs

---

## Extraction Methods

| Method | Description | Verification |
|--------|-------------|--------------|
| **direct extraction** | Code copied verbatim from source, may be simplified for length | Compare with source at specified lines |
| **extracted and simplified** | Core logic preserved, boilerplate removed for training clarity | Key validation patterns match source |
| **modified from source** | Security checks removed to create VULNERABLE variant | Diff against SAFE version shows exact removals |

---

## Contract 1: SPL Stake Pool

**Source:** `solana-program/stake-pool/program/src/processor.rs` (3,783 lines)
**URL:** https://github.com/solana-program/stake-pool/blob/main/program/src/processor.rs

### V1 — Access Control (Missing Key Check)

#### Sample 1: process_set_manager — SAFE
- **Function:** `process_set_manager` (lines 3446–3472)
- **Extraction:** direct extraction
- **Security patterns present:**
  - `check_account_owner(stake_pool_info, program_id)?` — verifies program ownership (line 3453)
  - `stake_pool.check_manager(manager_info)?` — validates current manager authorization (line 3460)
  - `new_manager_info.is_signer` — requires new manager signature (line 3461)
  - `stake_pool.check_manager_fee_info(new_manager_fee_info)?` — validates fee account (line 3466)

#### Sample 2: process_set_manager — VULNERABLE
- **Based on:** Same function, lines 3446–3472
- **Extraction:** modified from source
- **What was removed:**
  - Removed `check_account_owner` call (line 3453)
  - Removed `check_manager` call (line 3460)
  - Removed `is_signer` check (line 3461)
  - Removed `check_manager_fee_info` call (line 3466)
- **Resulting vulnerability:** Anyone can change the pool manager and redirect fees

#### Sample 3: process_set_staker — SAFE
- **Function:** `process_set_staker` (lines 3505–3525)
- **Extraction:** direct extraction
- **Security patterns present:**
  - `check_account_owner(stake_pool_info, program_id)?` — program ownership (line 3511)
  - Dual-authority check: `check_staker` OR `check_manager` (lines 3517–3521)

#### Sample 4: process_set_staker — VULNERABLE
- **Based on:** Same function, lines 3505–3525
- **Extraction:** modified from source
- **What was removed:**
  - Replaced dual-authority check with simple `is_signer` — any signer can change staker
  - Removed `check_account_owner` (line 3511)
- **Resulting vulnerability:** Any signer can take control of stake delegation

#### Sample 5: process_set_fee — SAFE
- **Function:** `process_set_fee` (lines 3476–3501)
- **Extraction:** direct extraction
- **Security patterns present:**
  - `check_account_owner(stake_pool_info, program_id)?` (line 3486)
  - `stake_pool.check_manager(manager_info)?` (line 3491)
  - `fee.can_only_change_next_epoch()` epoch timing check (line 3493)
  - `fee.check_too_high()?` bounds validation (line 3497)

#### Sample 6: process_set_fee — VULNERABLE
- **Based on:** Same function, lines 3476–3501
- **Extraction:** modified from source
- **What was removed:**
  - Removed `check_account_owner` (line 3486)
  - Removed `check_manager` (line 3491)
- **Resulting vulnerability:** Anyone can modify pool fees

---

### V4 — Input Validation (Type Confusion)

#### Sample 7: process_initialize (fee validation) — SAFE
- **Function:** `process_initialize` (lines 646–890)
- **Extraction:** extracted and simplified — kept validation logic from lines 728–798
- **Security patterns present:**
  - Fee bounds: `epoch_fee.numerator > epoch_fee.denominator` check (line 728)
  - Referral cap: `referral_fee > 100u8` (line 731)
  - Validator limits: `max_validators == 0` and `> MAX_VALIDATORS_IN_POOL` (lines 699, 707)
  - Rent-exemption: `rent.is_exempt()` (line 714)
  - Mint validation: `pool_mint.base.supply != 0` and `decimals` check (lines 771, 775)

#### Sample 8: process_initialize — VULNERABLE
- **Based on:** Same function, lines 646–890
- **Extraction:** modified from source
- **What was removed:**
  - Removed fee bounds check (lines 728–734)
  - Removed max_validators checks (lines 697–709)
  - Removed rent-exemption check (lines 714–725)
  - Removed mint supply and decimals validation (lines 768–798)
- **Resulting vulnerability:** Fees can exceed 100%, unlimited validators, unvalidated mint state

---

### V9 — Bump Seed Canonicalization

#### Sample 9: check_transient_stake_address — SAFE
- **Function:** `check_transient_stake_address` (lines 82–101)
- **Extraction:** direct extraction
- **Security pattern:** Uses `find_transient_stake_program_address()` which internally calls `find_program_address()` to derive canonical bump

#### Sample 10: check_ephemeral_stake_address — SAFE
- **Function:** `check_ephemeral_stake_address` (lines 104–118)
- **Extraction:** direct extraction
- **Security pattern:** Uses `find_ephemeral_stake_program_address()` → `find_program_address()` for canonical bump

#### Sample 11: process_initialize (withdraw authority) — SAFE
- **Function:** `process_initialize` (lines 756–765)
- **Extraction:** extracted and simplified — kept PDA derivation logic
- **Security pattern:** `find_withdraw_authority_program_address()` derives canonical bump, then address is verified and bump is stored

#### Sample 12: process_initialize — VULNERABLE
- **Based on:** Same function, lines 756–765
- **Extraction:** synthesized vulnerable variant
- **What was changed:** Accepts user-provided `bump_seed` via `InitArgs` struct and uses `create_program_address()` instead of `find_program_address()`
- **Resulting vulnerability:** Non-canonical bumps can create phantom PDAs

---

### V6 — Unchecked External Calls

#### Sample 13: token_mint_to — SAFE
- **Function:** `token_mint_to` (lines 586–609)
- **Extraction:** direct extraction
- **Security pattern:** `invoke_signed()` result is returned directly from the function — errors propagate to caller

#### Sample 14: stake_delegate — SAFE
- **Function:** `stake_delegate` (lines 331–363)
- **Extraction:** direct extraction
- **Security pattern:** `invoke_signed()` result returned directly — any delegation failure propagates

---

### V8 — Integer Overflow/Underflow

#### Sample 15: process_deposit_sol — SAFE
- **Function:** `process_deposit_sol` (lines 2651–2800)
- **Extraction:** extracted and simplified — kept arithmetic logic
- **Security patterns present:**
  - `checked_sub` for fee deduction (line ~2720)
  - `checked_add` for supply update (line 2632)
  - `checked_add` for lamports update (line 2638)
  - Minimum deposit check: `pool_tokens_user == 0` (line 2572)
  - Slippage protection via `minimum_pool_tokens_out` (line 2576)

#### Sample 16: process_deposit_sol — VULNERABLE
- **Based on:** Same function, lines 2651–2800
- **Extraction:** modified from source
- **What was removed:**
  - Replaced `checked_add` (lines 2632–2641) with unchecked `+=`
  - Removed slippage protection
  - Removed minimum deposit check
- **Resulting vulnerability:** Supply and lamport values can wrap around silently

---

### V10 — Denial of Service

#### Sample 17: process_update_validator_list_balance — SAFE
- **Function:** `process_update_validator_list_balance` (lines 1849–1898)
- **Extraction:** extracted and simplified — kept pagination pattern
- **Security patterns present:**
  - `start_index` parameter enables paginated processing across transactions
  - `EpochRewards::get()?.active` check prevents updates during reward distribution
  - Pairs validation: `checked_rem(2) != 0` ensures proper account pairs

#### Sample 18: process_add_validator_to_pool (capacity limits) — SAFE
- **Function:** `process_add_validator_to_pool` (lines 892–1037)
- **Extraction:** extracted and simplified — kept capacity limits from lines 946–957
- **Security patterns present:**
  - `header.max_validators == validator_list.len()` — pool-specific limit (line 946)
  - `validator_list.len() >= MAX_VALIDATORS_IN_POOL` — global hard cap (line 949)
  - Duplicate check via `find()` with `memcmp_pubkey` (lines 952–957)

#### Sample 19: process_add_validator_to_pool — VULNERABLE
- **Based on:** Same function, lines 892–1037
- **Extraction:** modified from source
- **What was removed:**
  - Removed capacity checks (lines 946–951)
  - Removed duplicate validator check (lines 952–957)
  - Removed staker authorization (line 931)
  - Removed epoch freshness check (lines 935–937)
- **Resulting vulnerability:** Unbounded validator list growth, duplicate entries possible

---

## Contract 2: SPL Token

**Source:** `solana-program/token/program/src/processor.rs` (1,347 lines)
**URL:** https://github.com/solana-program/token/blob/main/program/src/processor.rs

### V1 — Access Control (Missing Key Check)

#### Sample 20: process_transfer — SAFE
- **Function:** `process_transfer` (lines 227–341)
- **Extraction:** extracted and simplified — kept core validation logic
- **Security patterns present:**
  - `validate_owner()` for both owner and delegate paths (lines 273–300)
  - Frozen account check (line 249)
  - Mint mismatch check (line 255)
  - Delegate allowance tracking with `checked_sub` (line 287)

#### Sample 21: process_transfer — VULNERABLE
- **Based on:** Same function, lines 227–341
- **Extraction:** modified from source
- **What was removed:**
  - Removed `validate_owner` call (lines 273–300)
  - Removed frozen check (lines 249–251)
  - Removed mint mismatch check (lines 255–257)
- **Resulting vulnerability:** Anyone can transfer tokens from any account

#### Sample 22: process_set_authority — SAFE
- **Function:** `process_set_authority` (lines 422–518)
- **Extraction:** extracted and simplified — kept mint authority validation from lines 477–512
- **Security patterns present:**
  - `validate_owner()` before changing `mint_authority` (lines 486–491)
  - `validate_owner()` before changing `freeze_authority` (lines 500–505)
  - Fixed supply protection via `ok_or(TokenError::FixedSupply)` (line 484)

#### Sample 23: process_set_authority — VULNERABLE
- **Based on:** Same function, lines 422–518
- **Extraction:** modified from source
- **What was removed:**
  - Removed `validate_owner` for MintTokens (lines 486–491)
  - Removed `validate_owner` for FreezeAccount (lines 500–505)
  - Removed FixedSupply and MintCannotFreeze checks
- **Resulting vulnerability:** Anyone can take over mint authority

#### Sample 24: process_close_account — SAFE
- **Function:** `process_close_account` (lines 670–709)
- **Extraction:** extracted and simplified — removed incinerator special case
- **Security patterns present:**
  - Self-transfer check: `cmp_pubkeys(source, destination)` (line 677)
  - Balance check for non-native accounts (line 682)
  - `validate_owner()` against `close_authority` or `owner` (lines 686–695)
  - Checked arithmetic for lamport transfer (line 701)

#### Sample 25: process_close_account — VULNERABLE
- **Based on:** Same function, lines 670–709
- **Extraction:** modified from source
- **What was removed:**
  - Removed `validate_owner` call (lines 690–695)
  - Removed self-transfer check (lines 677–679)
- **Resulting vulnerability:** Anyone can close empty accounts and steal rent lamports

#### Sample 26: process_burn — SAFE
- **Function:** `process_burn` (lines 585–668)
- **Extraction:** extracted and simplified
- **Security patterns present:**
  - `validate_owner()` for both owner and delegate (lines 621–648)
  - Frozen check (line 601), funds check (line 607), mint check (line 610)
  - Delegate allowance with `checked_sub` (line 633)

#### Sample 27: process_burn — VULNERABLE
- **Based on:** Same function, lines 585–668
- **Extraction:** modified from source
- **What was removed:**
  - Removed `validate_owner` for both paths (lines 621–648)
  - Removed frozen check (line 601), mint check (line 610)
- **Resulting vulnerability:** Anyone can burn any user's tokens

---

### V4 — Input Validation (Type Confusion)

#### Sample 28: _process_initialize_multisig — SAFE
- **Function:** `_process_initialize_multisig` (lines 172–212)
- **Extraction:** direct extraction
- **Security patterns present:**
  - Re-initialization prevention: `multisig.is_initialized` (line 187)
  - Rent-exemption check (lines 191–193)
  - `is_valid_signer_index(multisig.n)` — validates signer count (lines 198–200)
  - `is_valid_signer_index(multisig.m)` — validates required signers (lines 201–203)

#### Sample 29: _process_initialize_multisig — VULNERABLE
- **Based on:** Same function, lines 172–212
- **Extraction:** modified from source
- **What was removed:**
  - Removed rent-exemption check (lines 191–193)
  - Removed `is_valid_signer_index` for n (lines 198–200)
  - Removed `is_valid_signer_index` for m (lines 201–203)
- **Resulting vulnerability:** m=0 allows zero-signature operations, m>n makes multisig unusable

#### Sample 30: process_transfer (full validation) — SAFE
- **Function:** `process_transfer` (lines 227–341)
- **Extraction:** extracted and simplified — focused on input validation patterns
- **Security patterns present:**
  - Frozen account check, balance check, mint consistency
  - Optional decimals matching for TransferChecked variant
  - Self-transfer handling with ownership verification
  - Checked arithmetic for amount operations

---

### V8 — Integer Overflow/Underflow

#### Sample 31: process_mint_to — SAFE
- **Function:** `process_mint_to` (lines 520–583)
- **Extraction:** extracted and simplified
- **Security patterns present:**
  - `checked_add(amount).ok_or(TokenError::Overflow)` for destination balance (line 566)
  - `checked_add(amount).ok_or(TokenError::Overflow)` for mint supply (line 571)
  - `validate_owner` for mint authority (lines 551–558)

#### Sample 32: process_mint_to — VULNERABLE
- **Based on:** Same function, lines 520–583
- **Extraction:** modified from source
- **What was removed:**
  - Replaced `checked_add` (lines 566–574) with unchecked `+=`
  - Removed frozen check (line 533), native check (line 537), mint check (line 540)
  - Removed `validate_owner` (lines 551–558)
- **Resulting vulnerability:** Unchecked overflow + no authority = unlimited minting

#### Sample 33: relocate_lamports — SAFE
- **Function:** Derived from `process_close_account` lamport transfer pattern (lines 700–706)
- **Extraction:** extracted lamport transfer pattern and generalized
- **Security patterns present:**
  - `checked_sub` with InsufficientFunds error for source
  - `checked_add` with ArithmeticOverflow error for destination

---

## Verification Instructions

To verify any sample:

1. Open the source URL listed in the contract section above
2. Navigate to the function name and line numbers specified
3. For **SAFE** samples: confirm the security patterns listed are present in the original code
4. For **VULNERABLE** samples: confirm the "What was removed" items are present in the original but absent in the sample

---

## Batch 1 Statistics

| Metric | Value |
|--------|-------|
| Total samples | 33 |
| SAFE samples | 20 |
| VULNERABLE samples | 13 |
| Source contracts | 2 |
| Vulnerability types covered | V1, V4, V6, V8, V9, V10 |
| Missing: V5 (CPI) | Covered in batch 2 and later |

# Dataset Sources Documentation — Batch 5

## Contracts in This Batch

| # | Contract | Repository | File | Lines of Code |
|---|----------|------------|------|---------------|
| 9 | Name Service | solana-labs/solana-program-library/name-service | program/src/processor.rs | 280 |
| 10 | Binary Option | solana-labs/solana-program-library/binary-option | program/src/processor.rs | 744 |
| 11 | Stateless Asks | solana-labs/solana-program-library/stateless-asks | program/src/processor.rs | 399 |

**Repository URLs:**
- Name Service: https://github.com/solana-labs/solana-program-library/blob/master/name-service/program/src/processor.rs
- Binary Option: https://github.com/solana-labs/solana-program-library/blob/master/binary-option/program/src/processor.rs
- Stateless Asks: https://github.com/solana-labs/solana-program-library/blob/master/stateless-asks/program/src/processor.rs

---

## Contract 9: Name Service

**Source:** `solana-labs/solana-program-library/name-service/program/src/processor.rs` (280 lines)
**URL:** https://github.com/solana-labs/solana-program-library/blob/master/name-service/program/src/processor.rs

### V9 — Bump Seed Canonicalization

#### Sample 1: process_create (get_seeds_and_key) — SAFE
- **Function:** `process_create` (lines 26–50)
- **Extraction:** extracted and simplified — kept get_seeds_and_key (uses find_program_address internally) and address verification (L51–54)

### V8 — Integer Overflow/Underflow

#### Sample 2: process_delete (saturating_add) — SAFE
- **Function:** `process_delete` (lines 197–230)
- **Extraction:** direct extraction — kept owner+signer check, data zeroing, saturating_add for lamports (L219)

### V1 — Access Control

#### Sample 3: process_transfer (owner+signer+class checks) — SAFE
- **Function:** `process_transfer` (lines 155–193)
- **Extraction:** direct extraction

#### Sample 4: process_transfer — VULNERABLE
- **Based on:** Same function
- **What was removed:** is_signer check (L175–178), owner match (L176), parent_owner logic (L162–172), class signer check (L179–185)
- **Resulting vulnerability:** Anyone can transfer any name

### V4 — Input Validation

#### Sample 5: process_create (comprehensive validation) — SAFE
- **Function:** `process_create` (lines 26–82)
- **Extraction:** extracted and simplified — kept PDA verification (L51–54), re-creation prevention (L55–61), class signer (L62–65), parent validation (L66–76), zero-owner (L77–80)

#### Sample 6: process_create — VULNERABLE
- **Based on:** Same function
- **What was removed:** PDA verification (L51–54), re-creation check (L55–61), class signer (L62–65), parent validation (L66–76), zero-owner (L77–80)
- **Resulting vulnerability:** Arbitrary account writes, name overwriting, domain hijacking

### V10 — Denial of Service

#### Sample 7: process_realloc (rent handling) — SAFE
- **Function:** `process_realloc` (lines 233–272)
- **Extraction:** direct extraction

#### Sample 8: process_realloc — VULNERABLE
- **Based on:** Same function
- **What was removed:** owner+signer check (L246–249), rent calculation and lamport adjustment (L251–267)
- **Resulting vulnerability:** Unauthorized resize, rent-exempt violation

#### Sample 9: process_delete (data zeroing) — SAFE
- **Function:** `process_delete` (lines 197–230)
- **Extraction:** direct extraction — data zeroing prevents ghost account reuse

### V6 — Unchecked External Calls

#### Sample 10: process_create CPI chain — SAFE
- **Function:** `process_create` (lines 84–108)
- **Extraction:** extracted and simplified — three-step CPI (transfer, allocate, assign) with ? propagation

---

## Contract 10: Binary Option

**Source:** `solana-labs/solana-program-library/binary-option/program/src/processor.rs` (744 lines)
**URL:** https://github.com/solana-labs/solana-program-library/blob/master/binary-option/program/src/processor.rs

### V9 — Bump Seed Canonicalization

#### Sample 11: process_trade (find_program_address) — SAFE
- **Function:** `process_trade` (lines 187–238)
- **Extraction:** extracted and simplified — kept find_program_address (L223–231), authority verification (L260)

#### Sample 12: process_initialize (find_program_address) — SAFE
- **Function:** `process_initialize_binary_option` (lines 65–185)
- **Extraction:** extracted and simplified — kept find_program_address (L130–138), authority transfers (L139–159)

### V8 — Integer Overflow/Underflow

#### Sample 13: process_trade (unchecked n * price) — VULNERABLE (REAL VULNERABILITY)
- **Function:** `process_trade` (lines 187–544)
- **Extraction:** extracted from Case 1 (L310–345)
- **Real issue:** `n * sell_price` (L331) and `n * buy_price` (L339) are unchecked u64 multiplications despite total_price being validated with checked_add

#### Sample 14: process_collect (checked_mul) — SAFE
- **Function:** `process_collect` (lines 626–744)
- **Extraction:** extracted and simplified — kept checked_mul (L725–727), settled check (L666–668), reward validation

### V1 — Access Control

#### Sample 15: process_settle (owner+signer) — SAFE
- **Function:** `process_settle` (lines 591–624)
- **Extraction:** direct extraction

#### Sample 16: process_settle — VULNERABLE
- **Based on:** Same function
- **What was removed:** signer check (L603–605), already-settled check (L606–608), owner match (L610), winning mint validation (L611–617)
- **Resulting vulnerability:** Anyone settles and chooses winner

### V4 — Input Validation

#### Sample 17: process_trade (price+account validation) — SAFE
- **Function:** `process_trade` (lines 187–293)
- **Extraction:** extracted and simplified — kept checked_add price validation (L241–246), settled check (L247–249), extensive key matching (L250–293)

### V5 — CPI Reentrancy

#### Sample 18: process_trade (burn-then-transfer) — SAFE
- **Function:** `process_trade` Case 1 (lines 310–345)
- **Extraction:** extracted and simplified — burns before escrow transfers

#### Sample 19: process_trade — VULNERABLE
- **Based on:** Same function
- **What was changed:** Reversed CPI order — escrow transfers before burns
- **Resulting vulnerability:** Reentrancy drain via unreduced positions

---

## Contract 11: Stateless Asks

**Source:** `solana-labs/solana-program-library/stateless-asks/program/src/processor.rs` (399 lines)
**URL:** https://github.com/solana-labs/solana-program-library/blob/master/stateless-asks/program/src/processor.rs

### V9 — Bump Seed Canonicalization

#### Sample 20: process_accept_offer (create_program_address) — VULNERABLE (REAL VULNERABILITY)
- **Function:** `process_accept_offer` (lines 91–229)
- **Extraction:** direct extraction and simplified
- **Real issue:** bump_seed from instruction data (L97) used with create_program_address (L198) instead of find_program_address

### V8 — Integer Overflow/Underflow

#### Sample 21: pay_creator_fees (checked arithmetic chain) — SAFE
- **Function:** `pay_creator_fees` (lines 276–399)
- **Extraction:** extracted and simplified — kept checked_mul (L295–297), checked_div (L298–299), checked_sub (L301–303), checked_add (L396–398)

### V4 — Input Validation

#### Sample 22: process_accept_offer (delegation validation) — SAFE
- **Function:** `process_accept_offer` (lines 182–212)
- **Extraction:** extracted and simplified — kept delegated_amount check (L195–197), delegate match (L202–204), ATA assertions (L211–212)

### V6 — Unchecked External Calls

#### Sample 23: process_accept_offer (dual transfer with ?) — SAFE
- **Function:** `process_accept_offer` (lines 213–268)
- **Extraction:** extracted and simplified — both CPI transfers with ? propagation

### V5 — CPI Reentrancy

#### Sample 24: process_accept_offer (atomic swap) — SAFE
- **Function:** `process_accept_offer` (lines 182–269)
- **Extraction:** extracted and simplified — delegation validation prevents partial-fill reentrancy

---

## Verification Instructions

To verify any sample:

1. Open the source URL listed in the contract section above
2. Navigate to the function name and line numbers specified
3. For **SAFE** samples: confirm the security patterns listed are present in the original code
4. For **VULNERABLE** samples: confirm the "What was removed/changed" items are present in the original but absent in the sample

---

## Batch 5 Statistics

| Metric | Value |
|--------|-------|
| Total samples | 24 |
| SAFE samples | 17 |
| VULNERABLE samples | 7 |
| Source contracts | 3 |
| Vulnerability types covered | V1, V4, V5, V6, V8, V9, V10 |

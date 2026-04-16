# Dataset Sources Documentation — Batch 3

## Contracts in This Batch

| # | Contract | Repository | File | Lines of Code |
|---|----------|------------|------|---------------|
| 5 | Token Swap | solana-labs/solana-program-library/token-swap | program/src/processor.rs | 8,376 |
| 6 | Token Lending | solana-labs/solana-program-library/token-lending | program/src/processor.rs | 2,041 |

**Repository URLs:**
- Token Swap: https://github.com/solana-labs/solana-program-library/blob/master/token-swap/program/src/processor.rs
- Token Lending: https://github.com/solana-labs/solana-program-library/blob/master/token-lending/program/src/processor.rs

---

## Extraction Methods

| Method | Description | Verification |
|--------|-------------|--------------|
| **direct extraction** | Code copied verbatim from source, may be simplified for length | Compare with source at specified lines |
| **extracted and simplified** | Core logic preserved, boilerplate removed for training clarity | Key validation patterns match source |
| **modified from source** | Security checks removed to create VULNERABLE variant | Diff against SAFE version shows exact removals |

---

## Contract 5: Token Swap

**Source:** `solana-labs/solana-program-library/token-swap/program/src/processor.rs` (8,376 lines)
**URL:** https://github.com/solana-labs/solana-program-library/blob/master/token-swap/program/src/processor.rs

### V8 — Integer Overflow/Underflow

#### Sample 1: process_swap (slippage + checked arithmetic) — SAFE
- **Function:** `process_swap` (lines 382–628)
- **Extraction:** extracted and simplified — kept to_u64() checks (L489,517), u128 promotion (L479–481), checked_sub (L585–587), slippage (L529–531)
- **Security patterns:** to_u64() validates u128→u64 conversion, u128 promotion for intermediate values, checked_sub for host_fee, slippage protection

#### Sample 2: process_swap — VULNERABLE
- **Based on:** Same function, lines 382–628
- **What was changed:** Replaced to_u64() with unsafe 'as u64' truncation (L489,517), removed minimum_amount_out slippage parameter (L529–531), replaced checked_sub with unchecked subtraction (L585)
- **Resulting vulnerability:** Silent u128→u64 truncation, no slippage protection, fee underflow

#### Sample 3: process_deposit_all_token_types (overflow protection) — SAFE
- **Function:** `process_deposit_all_token_types` (lines 630–742)
- **Extraction:** extracted and simplified — kept to_u64() (L692,699), u128 promotion (L684–688), slippage limits (L693–694,700–701), zero checks (L696–698,703–705)

#### Sample 4: process_deposit_all_token_types — VULNERABLE
- **Based on:** Same function, lines 630–742
- **What was changed:** Removed maximum_token_a/b_amount slippage parameters (L633–635), replaced to_u64() with 'as u64' (L692,699), removed zero checks (L696–698,703–705)

#### Sample 5: process_withdraw_all_token_types (checked_sub for fees) — SAFE
- **Function:** `process_withdraw_all_token_types` (lines 744–884)
- **Extraction:** extracted and simplified — kept checked_sub for fee (L804–806), u128 promotion, to_u64(), min() capping (L818,826), slippage (L819–821,827–829)

### V10 — Denial of Service

#### Sample 6: process_swap (zero trading check) — SAFE
- **Function:** `process_swap` (lines 476–533)
- **Extraction:** extracted and simplified — kept ZeroTradingTokens check (L485), transfer fee handling with ok_or (L462–464,523–525), slippage (L529–531)

#### Sample 7: process_swap — VULNERABLE
- **Based on:** Same function
- **What was changed:** Replaced .ok_or() with .unwrap() (L485), removed slippage, removed transfer fee handling (L459–468,518–528)
- **Resulting vulnerability:** Program panic on zero-liquidity pool, zero-output swaps drain pool

### V5 — CPI Reentrancy

#### Sample 8: process_swap transfer-in then transfer-out — SAFE
- **Function:** `process_swap` (lines 546–625)
- **Extraction:** extracted and simplified — kept transfer-in-then-out CPI ordering (source L546–556, destination L615–625)

#### Sample 9: process_swap — VULNERABLE
- **Based on:** Same function
- **What was changed:** Reversed CPI order — destination transfer before source transfer
- **Resulting vulnerability:** Pool drained via reentrancy before receiving user's input tokens

#### Sample 10: process_deposit transfer-in then mint — SAFE
- **Function:** `process_deposit_all_token_types` (lines 709–739)
- **Extraction:** extracted and simplified — kept transfer-A, transfer-B, then mint ordering

### V1 — Access Control

#### Sample 11: check_accounts comprehensive validation — SAFE
- **Function:** `check_accounts` (lines 194–244)
- **Extraction:** direct extraction
- **Security patterns:** Program ownership (L208), authority PDA (L211–214), token A/B matching (L216–221), pool mint (L222–224), user-pool separation (L228–236), fee account (L238–242)

### V9 — Bump Seed Canonicalization

#### Sample 12: process_initialize with find_program_address — SAFE
- **Function:** `process_initialize` (lines 246–380)
- **Extraction:** extracted and simplified — kept find_program_address (L269–270), authority verification (L271–273), bump stored (L367)

### V4 — Input Validation

#### Sample 13: process_initialize comprehensive input validation — SAFE
- **Function:** `process_initialize` (lines 274–351)
- **Extraction:** extracted and simplified — kept ownership (L293–298), repeated mint (L309–311), delegate/close checks (L315–326), supply/freeze (L328–333), fee/curve validation (L350–351)

#### Sample 14: process_initialize — VULNERABLE
- **Based on:** Same function
- **What was removed:** Token ownership checks (L293–298), repeated mint check (L309–311), delegate checks (L315–320), close_authority checks (L321–326), supply/freeze checks (L328–333), fee/curve validation (L350–351)
- **Resulting vulnerability:** Degenerate pools, delegated token drain, share inflation

### V6 — Unchecked External Calls

#### Sample 15: token_burn with ? propagation — SAFE
- **Function:** `token_burn` (lines 102–130)
- **Extraction:** direct extraction
- **Security pattern:** ? on instruction creation, invoke_signed_wrapper returns Result

---

## Contract 6: Token Lending

**Source:** `solana-labs/solana-program-library/token-lending/program/src/processor.rs` (2,041 lines)
**URL:** https://github.com/solana-labs/solana-program-library/blob/master/token-lending/program/src/processor.rs

### V8 — Integer Overflow/Underflow

#### Sample 16: process_refresh_obligation (checked_pow + Decimal) — SAFE
- **Function:** `process_refresh_obligation` (lines 660–781)
- **Extraction:** extracted and simplified — kept checked_pow (L703–705), try_mul/try_div/try_add Decimal arithmetic (L707–711,718–722)

#### Sample 17: process_refresh_obligation — VULNERABLE
- **Based on:** Same function
- **What was changed:** Replaced checked_pow with unchecked pow (L703–705), replaced Decimal arithmetic with unchecked u128 multiplication (L707–722), removed stale check (L694–700)
- **Resulting vulnerability:** Panic on large decimals, silent overflow in valuation

#### Sample 18: process_flash_loan (checked_add for balance) — SAFE
- **Function:** `process_flash_loan` (lines 1508–1685)
- **Extraction:** extracted and simplified — kept checked_add (L1590–1595), checked_sub (L1661–1663), post-loan balance verification (L1652–1657)

#### Sample 19: process_flash_loan — VULNERABLE
- **Based on:** Same function
- **What was changed:** Replaced checked_add with unchecked + (L1590–1595), replaced checked_sub with unchecked - (L1661–1663), removed u64::MAX handling (L1577–1581), removed zero check (L1514–1517)
- **Resulting vulnerability:** Balance overflow bypass, uncontrolled flash loan amounts

#### Sample 20: process_borrow_obligation_liquidity (fee checked_sub) — SAFE
- **Function:** `process_borrow_obligation_liquidity` (lines 1035–1210)
- **Extraction:** extracted and simplified — kept zero checks, remaining_borrow_value check, slippage, checked_sub (L1175–1177)

### V10 — Denial of Service

#### Sample 21: process_deposit_reserve_liquidity (stale check) — SAFE
- **Function:** `process_deposit_reserve_liquidity` (lines 414–514)
- **Extraction:** extracted and simplified — kept stale check (L471–474), zero check (L419–422), self-deposit prevention (L463–466), market-reserve link (L451–454)

#### Sample 22: process_deposit_reserve_liquidity — VULNERABLE
- **Based on:** Same function
- **What was removed:** Zero amount check (L419–422), stale check (L471–474), program ownership checks (L437–440,447–450), market-reserve link (L451–454), self-deposit prevention (L463–466)
- **Resulting vulnerability:** Outdated exchange rates, circular deposits, cross-market abuse

#### Sample 23: process_liquidate_obligation (health check) — SAFE
- **Function:** `process_liquidate_obligation` (lines 1316–1506)
- **Extraction:** extracted and simplified — kept health check (L1426–1429), stale check (L1416–1419), zero checks (L1420–1425), liquidation minimums (L1469–1476)

#### Sample 24: process_liquidate_obligation — VULNERABLE
- **Based on:** Same function
- **What was removed:** Health check (L1426–1429), stale checks (L1374–1377,L1416–1419), zero value checks (L1420–1425), liquidation minimums (L1469–1476), ownership checks
- **Resulting vulnerability:** Healthy obligations liquidated, stale price exploitation, dust griefing

### V5 — CPI Reentrancy

#### Sample 25: process_flash_loan (balance verification + self-call prevention) — SAFE
- **Function:** `process_flash_loan` (lines 1508–1685)
- **Extraction:** extracted and simplified — kept self-invocation prevention (L1530–1533), balance snapshot (L1589), post-CPI verification (L1652–1657), reserve re-read (L1646–1650)

#### Sample 26: process_flash_loan — VULNERABLE
- **Based on:** Same function
- **What was removed:** Self-invocation check (L1530–1533), balance snapshot (L1589), post-CPI balance verification (L1652–1657), reserve re-read and repay (L1646–1650)
- **Resulting vulnerability:** Self-recursive drain, unverified repayment, permanent reserve debt

### V1 — Access Control

#### Sample 27: process_set_lending_market_owner — SAFE
- **Function:** `process_set_lending_market_owner` (lines 152–180)
- **Extraction:** direct extraction
- **Security patterns:** Program ownership (L163–166), owner key match (L167–170), signer check (L171–174)

#### Sample 28: process_set_lending_market_owner — VULNERABLE
- **Based on:** Same function
- **What was removed:** Program ownership check (L163–166), owner key match (L167–170), signer check (L171–174)
- **Resulting vulnerability:** Anyone takes control of lending market

#### Sample 29: process_modify_reserve_config — SAFE
- **Function:** `process_modify_reserve_config` (lines 1688–1734)
- **Extraction:** direct extraction
- **Security patterns:** Dual program ownership, owner match, signer check, reserve-market link (L1724–1727)

### V9 — Bump Seed Canonicalization

#### Sample 30: process_init_lending_market with find_program_address — SAFE
- **Function:** `process_init_lending_market` (lines 121–150)
- **Extraction:** direct extraction
- **Security pattern:** find_program_address (L141) derives canonical bump at init, stored in market state

### V6 — Unchecked External Calls

#### Sample 31: spl_token_transfer + invoke_optionally_signed — SAFE
- **Function:** `spl_token_transfer` + `invoke_optionally_signed` (lines 1900–1938)
- **Extraction:** direct extraction
- **Security pattern:** ? on instruction creation, invoke_optionally_signed dispatches correctly, result mapped to domain error

---

## Verification Instructions

To verify any sample:

1. Open the source URL listed in the contract section above
2. Navigate to the function name and line numbers specified
3. For **SAFE** samples: confirm the security patterns listed are present in the original code
4. For **VULNERABLE** samples: confirm the "What was removed/changed" items are present in the original but absent in the sample

---

## Batch 3 Statistics

| Metric | Value |
|--------|-------|
| Total samples | 31 |
| SAFE samples | 20 |
| VULNERABLE samples | 11 |
| Source contracts | 2 |
| Vulnerability types covered | V1, V4, V5, V6, V8, V9, V10 |

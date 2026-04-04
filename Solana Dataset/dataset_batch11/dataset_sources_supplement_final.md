# Dataset Sources Documentation — Final Supplement

## Purpose

Final supplement to reach 20+ SAFE and 20+ VULNERABLE per vulnerability type. Adds 23 samples (6 SAFE + 17 VULNERABLE).

---

## V8 — Integer Overflow (11 VULNERABLE)

**Pattern:** Replaced `checked_add`/`checked_sub`/`checked_mul`/`saturating_add` with unchecked `+`/`-`/`*`.

| # | Contract | Function | Lines | What was changed |
|---|----------|----------|-------|------------------|
| 1 | SPL Token | process_close_account | 670–709 | checked_add → unchecked +, removed zero-balance check |
| 2 | Token Swap | process_withdraw_all_token_types | 742–874 | to_u64() → `as u64` truncation, checked_mul/div → unchecked, removed slippage |
| 3 | Token Lending | process_borrow_obligation_liquidity | 938–1074 | calculate_borrow checked → unchecked *÷-, checked Decimal add → unchecked + |
| 4 | Single Pool | calculate_withdraw_amount | 63–75 | u128 widening → u64 unchecked *, removed checked_div, removed try_from |
| 5 | Single Pool | process_deposit_stake | 931–1088 | calculate_deposit_amount (u128) → unchecked u64 */÷, removed zero check |
| 6 | Token-2022 | process_mint_to | 1022–1113 | checked_add supply/amount → unchecked +, removed authority/frozen checks |
| 7 | Token-2022 | process_burn | 1115–1286 | checked_sub amount/supply → unchecked -, removed authority/frozen/CPI guard |
| 8 | Stateless Asks | pay_creator_fees | 276–399 | checked_mul/div/sub/add → unchecked, removed metadata owner check |
| 9 | Name Service | process_delete | 197–230 | saturating_add → unchecked +, removed data zeroing |
| 10 | Governance | process_deposit_governing_tokens | 119–131 | checked_add → unchecked + |
| 11 | Governance | process_cast_vote | 107–140 | ALL checked_add → unchecked + for vote counts and weights |

## V10 — Denial of Service (3 SAFE + 3 VULNERABLE)

| # | Contract | Function | Label | Key points |
|---|----------|----------|-------|------------|
| 12 | Token Lending | process_refresh_reserve | SAFE | Ownership, rate update, interest accrual, oracle validation |
| 13 | Token Lending | process_refresh_reserve | VULN | Removed ownership, rate update, interest accrual, oracle validation |
| 14 | SPL Stake Pool | process_cleanup_removed_validator | SAFE | Status check, transient check, authority |
| 15 | SPL Stake Pool | process_cleanup_removed_validator | VULN | Removed all checks — active validators removable |
| 16 | SPL Token | process_initialize_mint | SAFE | Re-init prevention, rent exemption, supply=0 |
| 17 | SPL Token | process_initialize_mint | VULN | Removed re-init, rent check, supply reset |

## V1 — Access Control (1 VULNERABLE)

| # | Contract | Function | What was removed |
|---|----------|----------|------------------|
| 18 | SPL Token | process_freeze_account | freeze_authority validation, mint mismatch, frozen check |

## V5 — CPI Reentrancy (2 VULNERABLE)

| # | Contract | Function | What was changed |
|---|----------|----------|------------------|
| 19 | Token Lending | process_borrow_obligation_liquidity | Transfer BEFORE state update (originally after) |
| 20 | Token Swap | process_withdraw_all_token_types | Transfer A+B BEFORE burn (originally after) |

## V6 — Unchecked Calls (1 SAFE)

| # | Contract | Function | Security |
|---|----------|----------|----------|
| 21 | Record | Write | Direct data copy with bounds check, no external CPI |

## V9 — Bump Seed (2 SAFE)

| # | Contract | Function | Security |
|---|----------|----------|----------|
| 22 | Single Pool | check_pool_mint_address | find_program_address canonical PDA |
| 23 | Single Pool | check_pool_stake_authority_address | find_program_address canonical PDA |

---

## Final Statistics

| Metric | Value |
|--------|-------|
| Total samples | 23 |
| SAFE | 6 |
| VULNERABLE | 17 |
| Types covered | V1, V5, V6, V8, V9, V10 |

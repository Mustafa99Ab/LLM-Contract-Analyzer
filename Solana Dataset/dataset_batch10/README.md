# Dataset Sources Documentation — Supplement: V5 + V1

## Purpose

This supplement adds 22 samples (9 SAFE + 13 VULNERABLE) to balance V5 (CPI Reentrancy) and V1 (Access Control).

---

## V5 — CPI Reentrancy (16 samples: 7 SAFE + 9 VULNERABLE)

**Vulnerability pattern:** In each VULNERABLE sample, CPI ordering was reversed — external calls that release value (mint tokens, transfer funds, authorize stake) are moved BEFORE internal state updates that should prevent re-execution.

### VULNERABLE from existing SAFE pairs (6 samples)

#### Sample 1: process_deposit_all_token_types — VULNERABLE
- **Contract:** Token Swap | **Lines:** 631–740
- **SAFE pair:** Batch 3 | **What was changed:** Reversed CPI order — token_mint_to (originally L731–739) placed BEFORE token_transfer calls (originally L709–730); removed slippage checks (L693–704)
- **Resulting vulnerability:** Pool tokens minted before user deposits

#### Sample 2: process_withdraw_stake — VULNERABLE
- **Contract:** Single Pool | **Lines:** 1091–1204
- **SAFE pair:** Batch 4 | **What was changed:** Reversed CPI order — stake_authorize (originally L1191–1198) placed BEFORE token_burn (originally L1170–1178) and stake_split (originally L1181–1188)
- **Resulting vulnerability:** Stake authority transferred before LP tokens burned

#### Sample 3: process_transfer — VULNERABLE
- **Contract:** Token-2022 | **Lines:** 329–600
- **SAFE pair:** Batch 4 | **What was changed:** Moved balance updates (originally after all checks/hooks) BEFORE transfer hook CPI (L549–570); removed checked_sub/checked_add (L446–450)
- **Resulting vulnerability:** Balances updated before transfer hook — malicious hook can re-enter

#### Sample 4: process_accept_offer — VULNERABLE
- **Contract:** Stateless Asks | **Lines:** 213–268
- **SAFE pair:** Batch 5 | **What was changed:** Reversed CPI order — taker-to-maker transfer (originally L253–268) placed BEFORE maker-to-taker transfer (originally L213–229)
- **Resulting vulnerability:** Taker sends first, maker can revoke delegation

#### Sample 5: process_deposit_governing_tokens — VULNERABLE
- **Contract:** Governance | **Lines:** 34–132
- **SAFE pair:** Batch 6 | **What was changed:** Reversed order — record update (originally L119–131) placed BEFORE transfer_spl_tokens (originally L73–78)
- **Resulting vulnerability:** Voting power granted before tokens deposited

#### Sample 6: process_withdraw_governing_tokens — VULNERABLE
- **Contract:** Governance | **Lines:** 27–85
- **SAFE pair:** Batch 6 | **What was changed:** Reversed order — deposit zeroing (originally L83–84) placed BEFORE transfer_spl_tokens_signed (originally L73–81)
- **Resulting vulnerability:** Deposit record zeroed before tokens transferred

### New SAFE-VULNERABLE pairs (3 pairs + 4 additional SAFE)

#### Sample 7: process_deposit_reserve_liquidity — SAFE
- **Contract:** Token Lending | **Lines:** 414–514
- **Security:** Transfer-in FIRST (L472–478), THEN mint-out (L497–502); ownership check; self-deposit prevention

#### Sample 8: process_deposit_reserve_liquidity — VULNERABLE
- **What was changed:** Reversed — mint collateral FIRST, then transfer liquidity; removed ownership and self-deposit checks

#### Sample 9: process_update_stake_pool_balance — SAFE
- **Contract:** SPL Stake Pool | **Lines:** 2010–2140
- **Security:** State calculation BEFORE fee mint CPI; ownership/validity checks; serialize after all CPIs

#### Sample 10: process_update_stake_pool_balance — VULNERABLE
- **What was changed:** Fee minted BEFORE state update; removed validity checks; fee calculated on stale data

#### Sample 11: process_decide — SAFE
- **Contract:** Binary Oracle Pair | **Lines:** 522–560
- **Security:** State update (decision recorded) BEFORE burn CPI; authority+decider checks

#### Sample 12: process_decide — VULNERABLE
- **What was changed:** Burn CPI BEFORE decision recorded; removed authority and decider checks

#### Sample 13: process_borrow_obligation_liquidity — SAFE
- **Contract:** Token Lending | **Lines:** 938–1074
- **Security:** Reserve and obligation states updated BEFORE transfer CPI

#### Sample 14: process_liquidate_obligation — SAFE
- **Contract:** Token Lending | **Lines:** 1316–1506
- **Security:** Health check; repay-then-withdraw ordering

#### Sample 15: process_withdraw_all_token_types — SAFE
- **Contract:** Token Swap | **Lines:** 742–874
- **Security:** Burn pool tokens FIRST, then transfer A and B

#### Sample 16: process_decrease_validator_stake — SAFE
- **Contract:** SPL Stake Pool | **Lines:** 1373–1512
- **Security:** Split before deactivate; staker authorization; state update after CPIs

---

## V1 — Access Control (6 samples: 2 SAFE + 4 VULNERABLE)

### VULNERABLE from existing SAFE pairs (3 samples)

#### Sample 17: check_accounts — VULNERABLE
- **Contract:** Token Swap | **Lines:** 194–244
- **SAFE pair:** Batch 3 | **What was removed:** ALL 8 checks — program ownership (L208–210), authority PDA (L211–215), token_a/b match (L216–221), pool_mint (L222–224), token_program (L225–227), user-pool collision (L228–237), fee account (L238–242)

#### Sample 18: process_modify_reserve_config — VULNERABLE
- **Contract:** Token Lending | **Lines:** 1688–1734
- **SAFE pair:** Batch 3 | **What was removed:** config.validate (L1693), reserve ownership (L1700–1703), market ownership (L1706–1709), market owner key match (L1710–1713), signer check (L1714–1717), reserve-market link (L1724–1727)

#### Sample 19: process_update_pool_token_metadata — VULNERABLE
- **Contract:** Single Pool | **Lines:** 1288–1372
- **SAFE pair:** Batch 4 | **What was removed:** check_vote_account (L1303), check_pool_address (L1304), vote_account match (L1307–1309), authorized_withdrawer verification (L1324–1333), signer check (L1335–1338), metadata address check (L1318)

### New SAFE-VULNERABLE pair

#### Sample 20: process_set_preferred_validator — SAFE
- **Contract:** SPL Stake Pool | **Lines:** 3370–3444
- **Security:** ownership, validity, staker authorization, validator list match, validator existence check

#### Sample 21: process_set_preferred_validator — VULNERABLE
- **What was removed:** ownership (L3384), validity (L3388–3390), staker auth (L3392), validator list (L3393), existence check (L3403–3410)

#### Sample 22: process_freeze_account — SAFE
- **Contract:** SPL Token | **Lines:** 713–761
- **Security:** Already-frozen check, freeze_authority validation via validate_owner, mint mismatch check

---

## Supplement Statistics

| Metric | Value |
|--------|-------|
| Total samples | 22 |
| SAFE | 9 |
| VULNERABLE | 13 |
| V5 samples | 16 (7S + 9V) |
| V1 samples | 6 (2S + 4V) |
| Contracts referenced | 9 |

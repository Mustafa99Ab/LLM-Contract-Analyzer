# Dataset Sources Documentation — Supplement: V9 + V6 VULNERABLE

## Purpose

This supplement adds 30 VULNERABLE samples to balance the dataset. Each sample is the **broken version** of an existing SAFE sample from previous batches. The SAFE original already exists in batches 1–7; this file documents only the new VULNERABLE pairs.

---

## V9 — Bump Seed Canonicalization (16 VULNERABLE samples)

**Vulnerability pattern:** In each case, `find_program_address` (which derives the canonical bump) was replaced with `create_program_address` accepting a user-provided `bump_seed`. This allows non-canonical bumps to create phantom PDAs.

---

#### Sample 1: check_transient_stake_address — VULNERABLE
- **Contract:** SPL Stake Pool
- **URL:** https://github.com/solana-program/stake-pool/blob/main/program/src/processor.rs
- **Function:** `check_transient_stake_address` (lines 82–101)
- **SAFE pair:** Batch 1, Sample 9
- **What was changed:** Replaced `find_transient_stake_program_address` (L90, uses `find_program_address`) with `create_program_address` accepting user-provided `bump_seed` parameter
- **Resulting vulnerability:** Non-canonical bumps create phantom transient stake accounts

#### Sample 2: check_ephemeral_stake_address — VULNERABLE
- **Contract:** SPL Stake Pool
- **URL:** https://github.com/solana-program/stake-pool/blob/main/program/src/processor.rs
- **Function:** `check_ephemeral_stake_address` (lines 104–118)
- **SAFE pair:** Batch 1, Sample 10
- **What was changed:** Replaced `find_ephemeral_stake_program_address` (L111, uses `find_program_address`) with `create_program_address` accepting user-provided `bump_seed`
- **Resulting vulnerability:** Multiple ephemeral accounts for same seed with different non-canonical bumps

#### Sample 3: process_recover_nested — VULNERABLE
- **Contract:** Associated Token Account
- **URL:** https://github.com/solana-program/associated-token-account/blob/main/program/src/processor.rs
- **Function:** `process_recover_nested` (lines 152–270)
- **SAFE pair:** Batch 2, Sample 3
- **What was changed:** Replaced `get_associated_token_address_and_bump_seed_internal` (L161, uses `find_program_address`) with `create_program_address` accepting user bump; removed nested and destination PDA verification (L171–199)
- **Resulting vulnerability:** Only owner PDA checked, nested and destination skipped — tokens can be recovered to wrong destination

#### Sample 4: process_initialize — VULNERABLE
- **Contract:** Token Swap
- **URL:** https://github.com/solana-labs/solana-program-library/blob/master/token-swap/program/src/processor.rs
- **Function:** `process_initialize` (lines 246–380)
- **SAFE pair:** Batch 3, Sample 12
- **What was changed:** Replaced `find_program_address` (L269–270) with `create_program_address` accepting user-provided bump; non-canonical bump stored in state (L367)
- **Resulting vulnerability:** Multiple swap authorities possible for same pool, stored bump compromises all operations

#### Sample 5: process_init_lending_market — VULNERABLE
- **Contract:** Token Lending
- **URL:** https://github.com/solana-labs/solana-program-library/blob/master/token-lending/program/src/processor.rs
- **Function:** `process_init_lending_market` (lines 121–150)
- **SAFE pair:** Batch 3, Sample 13
- **What was changed:** Replaced `find_program_address` (L141) with user-provided `bump_seed` parameter; bump no longer derived canonically
- **Resulting vulnerability:** All subsequent authority verification can be bypassed with non-canonical bumps

#### Sample 6: check_pool_pda — VULNERABLE
- **Contract:** Single Pool
- **URL:** https://github.com/solana-program/single-pool/blob/main/program/src/processor.rs
- **Function:** `check_pool_pda` (lines 219–240)
- **SAFE pair:** Batch 4, Sample 14
- **What was changed:** Replaced `pda_lookup_fn` (L227, uses `find_program_address`) with `create_program_address` accepting user-provided bump; removed dynamic function dispatch
- **Resulting vulnerability:** Generic PDA checker compromised — affects ALL pool account derivations (stake, mint, authority)

#### Sample 7: process_initialize_pool — VULNERABLE
- **Contract:** Single Pool
- **URL:** https://github.com/solana-program/single-pool/blob/main/program/src/processor.rs
- **Function:** `process_initialize_pool` (lines 560–596)
- **SAFE pair:** Batch 4, Sample 15
- **What was changed:** Replaced 5 `check_pool_*_address` calls (L578–592, each uses `find_program_address`) with `create_program_address` accepting 5 user-provided bump parameters
- **Resulting vulnerability:** All 5 PDAs (pool, stake, mint, stake_authority, mint_authority) use non-canonical bumps — phantom pool infrastructure

#### Sample 8: process_trade — VULNERABLE
- **Contract:** Binary Option
- **URL:** https://github.com/solana-labs/solana-program-library/blob/master/binary-option/program/src/processor.rs
- **Function:** `process_trade` (lines 187–238)
- **SAFE pair:** Batch 5, Sample 11
- **What was changed:** Replaced `find_program_address` (L223–231) with `create_program_address` accepting user-provided `bump_seed` from instruction data
- **Resulting vulnerability:** Multiple valid authority keys for same mint pair

#### Sample 9: process_initialize_binary_option — VULNERABLE
- **Contract:** Binary Option
- **URL:** https://github.com/solana-labs/solana-program-library/blob/master/binary-option/program/src/processor.rs
- **Function:** `process_initialize_binary_option` (lines 65–185)
- **SAFE pair:** Batch 5, Sample 12
- **What was changed:** Replaced `find_program_address` (L130–138) with `create_program_address` accepting user-provided bump
- **Resulting vulnerability:** Escrow and mint authorities transferred to potentially non-canonical PDA

#### Sample 10: process_create — VULNERABLE
- **Contract:** Name Service
- **URL:** https://github.com/solana-labs/solana-program-library/blob/master/name-service/program/src/processor.rs
- **Function:** `process_create` (lines 26–50)
- **SAFE pair:** Batch 5, Sample 1
- **What was changed:** Replaced `get_seeds_and_key` (L43–48, uses `find_program_address` internally) with `create_program_address` accepting user-provided bump
- **Resulting vulnerability:** Multiple name accounts for same name/class/parent with different bumps

#### Sample 11: process_execute_transaction — VULNERABLE
- **Contract:** Governance
- **URL:** https://github.com/solana-labs/solana-program-library/blob/master/governance/program/src/processor/process_execute_transaction.rs
- **Function:** `process_execute_transaction` (lines 55–87)
- **SAFE pair:** Batch 6, Sample 13
- **What was changed:** Replaced `find_program_address` for governance PDA (L65–68) with user-provided bump; removed treasury `find_program_address` (L74–76)
- **Resulting vulnerability:** Unauthorized instruction execution with non-canonical governance PDA

#### Sample 12: process_create_realm — VULNERABLE
- **Contract:** Governance
- **URL:** https://github.com/solana-labs/solana-program-library/blob/master/governance/program/src/processor/process_create_realm.rs
- **Function:** `process_create_realm` (lines 32–155)
- **SAFE pair:** Batch 6, Sample 14
- **What was changed:** Replaced `create_and_serialize_account_signed` (L146–154, uses `find_program_address` internally) with `create_program_address` accepting user-provided realm_bump
- **Resulting vulnerability:** Multiple realms for same name; stored bump affects all governance operations

#### Sample 13: process_cast_vote — VULNERABLE
- **Contract:** Governance
- **URL:** https://github.com/solana-labs/solana-program-library/blob/master/governance/program/src/processor/process_cast_vote.rs
- **Function:** `process_cast_vote` (lines 170–192)
- **SAFE pair:** Batch 6, Sample 15
- **What was changed:** Replaced `create_and_serialize_account_signed` (L178–186, uses `find_program_address` internally) with `create_program_address` accepting user-provided vote_record_bump
- **Resulting vulnerability:** Voter can create multiple vote records per proposal with different bumps — vote multiple times

#### Sample 14: process_exchange — VULNERABLE
- **Contract:** Token Upgrade
- **URL:** https://github.com/solana-labs/solana-program-library/blob/master/token-upgrade/program/src/processor.rs
- **Function:** `process_exchange` (lines 102–117)
- **SAFE pair:** Batch 7, Sample 3
- **What was changed:** Replaced `get_token_upgrade_authority_address_and_bump_seed` (L103–104, uses `find_program_address`) with `create_program_address` accepting user-provided bump
- **Resulting vulnerability:** Multiple escrow authorities for same mint pair

#### Sample 15: process_propose — VULNERABLE
- **Contract:** Feature Proposal
- **URL:** https://github.com/solana-program/feature-proposal/blob/main/program/src/processor.rs
- **Function:** `process_propose` (lines 53–72)
- **SAFE pair:** Batch 7, Sample 19
- **What was changed:** Replaced `get_mint_address_with_seed` and `get_feature_id_address_with_seed` (L53–75, use `find_program_address`) with `create_program_address` accepting user bumps; removed distributor and acceptance PDA checks
- **Resulting vulnerability:** Phantom proposal infrastructure with only 2 of 4 PDAs verified

#### Sample 16: process_collect — VULNERABLE
- **Contract:** Binary Option
- **URL:** https://github.com/solana-labs/solana-program-library/blob/master/binary-option/program/src/processor.rs
- **Function:** `process_collect` (lines 626–744)
- **SAFE pair:** Batch 5, Sample 14
- **What was changed:** Replaced `find_program_address` (L649–657) with `create_program_address` accepting user-provided bump from instruction data
- **Resulting vulnerability:** Attacker can use non-canonical bump to sign as escrow authority and drain funds

---

## V6 — Unchecked External Calls (14 VULNERABLE samples)

**Vulnerability pattern:** In each case, `?` error propagation on CPI calls was replaced with `let _ =` (silently discarding errors) or `.unwrap()` (panicking instead of clean error). This means CPI failures are ignored and execution continues with incorrect state.

---

#### Sample 17: token_mint_to — VULNERABLE
- **Contract:** SPL Stake Pool
- **URL:** https://github.com/solana-program/stake-pool/blob/main/program/src/processor.rs
- **Function:** `token_mint_to` (lines 586–609)
- **SAFE pair:** Batch 1, Sample 13
- **What was changed:** Replaced `?` on instruction creation (L596) with `.unwrap()`; replaced `invoke_signed` result propagation with `let _ =`
- **Resulting vulnerability:** Mint failure silently ignored — pool state becomes inconsistent

#### Sample 18: stake_delegate — VULNERABLE
- **Contract:** SPL Stake Pool
- **URL:** https://github.com/solana-program/stake-pool/blob/main/program/src/processor.rs
- **Function:** `stake_delegate` (lines 331–363)
- **SAFE pair:** Batch 1, Sample 14
- **What was changed:** Replaced `invoke_signed` result (returned directly in original L351–362) with `let _ =`
- **Resulting vulnerability:** Delegation failure silently ignored — stake sits undelegated, losing rewards

#### Sample 19: process_create_associated_token_account — VULNERABLE
- **Contract:** Associated Token Account
- **URL:** https://github.com/solana-program/associated-token-account/blob/main/program/src/processor.rs
- **Function:** `process_create_associated_token_account` (lines 120–149)
- **SAFE pair:** Batch 2, Sample 6
- **What was changed:** Replaced `?` on `initialize_immutable_owner` invoke (L130–135) with `let _ =`; replaced `?` on `initialize_account3` invoke (L137–148) with `let _ =`
- **Resulting vulnerability:** Account created but initialization may fail — uninitialized account usable as drain target

#### Sample 20: token_burn — VULNERABLE
- **Contract:** Token Swap
- **URL:** https://github.com/solana-labs/solana-program-library/blob/master/token-swap/program/src/processor.rs
- **Function:** `token_burn` (lines 102–130)
- **SAFE pair:** Batch 3, Sample 15
- **What was changed:** Replaced `?` on instruction creation (L116–123) with `.unwrap()`; replaced `invoke_signed_wrapper` result with `let _ =`
- **Resulting vulnerability:** Burn error ignored — pool tokens not destroyed but withdrawal proceeds, inflating supply

#### Sample 21: spl_token_transfer — VULNERABLE
- **Contract:** Token Lending
- **URL:** https://github.com/solana-labs/solana-program-library/blob/master/token-lending/program/src/processor.rs
- **Function:** `spl_token_transfer + invoke_optionally_signed` (lines 1900–1938)
- **SAFE pair:** Batch 3, Sample 16
- **What was changed:** Replaced `result.map_err` (L1937) with `let _ =`
- **Resulting vulnerability:** In lending protocol: deposits not received but collateral minted, borrows recorded but funds not sent

#### Sample 22: token_mint_to — VULNERABLE
- **Contract:** Single Pool
- **URL:** https://github.com/solana-program/single-pool/blob/main/program/src/processor.rs
- **Function:** `token_mint_to` (lines 502–529)
- **SAFE pair:** Batch 4, Sample 11
- **What was changed:** Replaced `?` on instruction creation (L519–526) with `.unwrap()`; replaced `invoke_signed` result (L528) with `let _ =`
- **Resulting vulnerability:** Stake merged but LP tokens not minted — user loses stake without receiving pool tokens

#### Sample 23: token_burn — VULNERABLE
- **Contract:** Single Pool
- **URL:** https://github.com/solana-program/single-pool/blob/main/program/src/processor.rs
- **Function:** `token_burn` (lines 531–558)
- **SAFE pair:** Batch 4, Sample 12
- **What was changed:** Replaced `?` on instruction creation (L548–555) with `.unwrap()`; replaced `invoke_signed` result (L557) with `let _ =`
- **Resulting vulnerability:** Tokens not burned but stake split and transferred — user keeps pool tokens AND gets stake back

#### Sample 24: process_create — VULNERABLE
- **Contract:** Name Service
- **URL:** https://github.com/solana-labs/solana-program-library/blob/master/name-service/program/src/processor.rs
- **Function:** `process_create` (lines 84–108)
- **SAFE pair:** Batch 5, Sample 10
- **What was changed:** Replaced `?` on all three CPIs (transfer L89–93, allocate L95–101, assign L103–107) with `let _ =`
- **Resulting vulnerability:** Name record written to improperly initialized account

#### Sample 25: process_accept_offer — VULNERABLE
- **Contract:** Stateless Asks
- **URL:** https://github.com/solana-labs/solana-program-library/blob/master/stateless-asks/program/src/processor.rs
- **Function:** `process_accept_offer` (lines 213–268)
- **SAFE pair:** Batch 5, Sample 23
- **What was changed:** Replaced `?` on maker-to-taker `invoke_signed` (L213–229) with `let _ =`
- **Resulting vulnerability:** Taker sends tokens but maker's tokens don't transfer — taker loses without receiving

#### Sample 26: process_create_realm — VULNERABLE
- **Contract:** Governance
- **URL:** https://github.com/solana-labs/solana-program-library/blob/master/governance/program/src/processor/process_create_realm.rs
- **Function:** `process_create_realm` (lines 32–155)
- **SAFE pair:** Batch 6, Sample 3
- **What was changed:** Replaced `?` on token holding creation (L57–67) with `let _ =`; replaced `?` on realm config creation (L104–111) with `let _ =`
- **Resulting vulnerability:** Realm created without token holding or config — governance operations fail unpredictably

#### Sample 27: process_deposit_governing_tokens — VULNERABLE
- **Contract:** Governance
- **URL:** https://github.com/solana-labs/solana-program-library/blob/master/governance/program/src/processor/process_deposit_governing_tokens.rs
- **Function:** `process_deposit_governing_tokens` (lines 34–132)
- **SAFE pair:** Batch 6, Sample 4
- **What was changed:** Replaced `?` on `transfer_spl_tokens` (L73–78) with `let _ =`
- **Resulting vulnerability:** Deposit amount incremented without tokens actually transferred — free voting power

#### Sample 28: process_withdraw_governing_tokens — VULNERABLE
- **Contract:** Governance
- **URL:** https://github.com/solana-labs/solana-program-library/blob/master/governance/program/src/processor/process_withdraw_governing_tokens.rs
- **Function:** `process_withdraw_governing_tokens` (lines 27–85)
- **SAFE pair:** Batch 6, Sample 5
- **What was changed:** Replaced `?` on `transfer_spl_tokens_signed` (L73–81) with `let _ =`
- **Resulting vulnerability:** Deposit zeroed but tokens never transferred — user loses voting power without receiving tokens

#### Sample 29: process_propose — VULNERABLE
- **Contract:** Feature Proposal
- **URL:** https://github.com/solana-program/feature-proposal/blob/main/program/src/processor.rs
- **Function:** `process_propose` (lines 37–224)
- **SAFE pair:** Batch 7, Sample 17
- **What was changed:** Replaced `?` on mint creation `invoke_signed` (L116–125) with `let _ =`; replaced `?` on `initialize_mint` (L128–135) with `let _ =`; replaced `?` on `mint_to` (L208–217) with `let _ =`
- **Resulting vulnerability:** Proposal created but mint/tokens may not exist — entire proposal infrastructure inconsistent

#### Sample 30: process_tally — VULNERABLE
- **Contract:** Feature Proposal
- **URL:** https://github.com/solana-program/feature-proposal/blob/main/program/src/processor.rs
- **Function:** `process_tally` (lines 226–291)
- **SAFE pair:** Batch 7, Sample 18
- **What was changed:** Replaced `?` on `invoke_signed` for feature assignment (L273–277) with `let _ =`
- **Resulting vulnerability:** Proposal marked Accepted but feature never actually activated on-chain

---

## Verification Instructions

To verify any VULNERABLE sample:

1. Find the **SAFE pair** referenced above (in the specified batch)
2. Open the source URL and navigate to the function/lines
3. Confirm the original code has the protection (e.g., `find_program_address`, `?` propagation)
4. Confirm the VULNERABLE sample has that protection removed (e.g., `create_program_address`, `let _ =`)

---

## Supplement Statistics

| Metric | Value |
|--------|-------|
| Total samples | 30 |
| All VULNERABLE | Yes (100%) |
| V9 samples | 16 |
| V6 samples | 14 |
| Contracts referenced | 11 |

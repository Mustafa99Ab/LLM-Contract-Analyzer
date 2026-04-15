# Dataset Sources Documentation — Batch 6

## Contracts in This Batch

| # | Contract | Repository | Files Used | Total Lines |
|---|----------|------------|------------|-------------|
| 12 | Governance | solana-labs/solana-program-library/governance | 7 processor files | ~600 |

**Repository Base URL:** https://github.com/solana-labs/solana-program-library/blob/master/governance/program/src/processor

**Files Used:**
- process_execute_transaction.rs
- process_cast_vote.rs
- process_create_proposal.rs
- process_create_realm.rs
- process_deposit_governing_tokens.rs
- process_withdraw_governing_tokens.rs
- process_set_realm_authority.rs

---

## Contract 12: Governance

### V6 — Unchecked External Calls (5 samples)

#### Sample 1: process_execute_transaction (invoke_signed with ?) — SAFE
#### Sample 2: process_execute_transaction — VULNERABLE
- Removed assert_can_execute_transaction, replaced ? with let _ =, marks Success regardless

#### Sample 3: process_create_realm (three create calls with ?) — SAFE
#### Sample 4: process_deposit_governing_tokens (transfer/mint with ?) — SAFE
#### Sample 5: process_withdraw_governing_tokens (transfer_signed with ?) — SAFE

### V5 — CPI Reentrancy (4 samples)

#### Sample 6: process_execute_transaction (state check before CPI) — SAFE
#### Sample 7: process_execute_transaction — VULNERABLE
- Moved state updates before CPI loop, removed execution check

#### Sample 8: process_deposit_governing_tokens (transfer-then-update) — SAFE
#### Sample 9: process_withdraw_governing_tokens (transfer-then-zero) — SAFE

### V10 — Denial of Service (3 samples)

#### Sample 10: process_cast_vote (VoteAlreadyExists + timing) — SAFE
#### Sample 11: process_cast_vote — VULNERABLE
- Removed duplicate check, timing check, signer check, used unchecked arithmetic

#### Sample 12: process_create_proposal (existence + weight checks) — SAFE

### V9 — Bump Seed Canonicalization (3 samples)

#### Sample 13: process_execute_transaction (dual find_program_address) — SAFE
#### Sample 14: process_create_realm (PDA-based account creation) — SAFE
#### Sample 15: process_cast_vote (PDA vote record) — SAFE

### V4 — Input Validation (2 samples)

#### Sample 16: process_create_proposal (options + vote type validation) — SAFE
#### Sample 17: process_create_realm (config validation) — SAFE

### V1 — Access Control (2 samples)

#### Sample 18: process_set_realm_authority (authority + signer) — SAFE
#### Sample 19: process_set_realm_authority — VULNERABLE
- Removed authority check, signer check, governance validation

### V8 — Integer Overflow (3 samples)

#### Sample 20: process_deposit_governing_tokens (checked_add) — SAFE
#### Sample 21: process_cast_vote (checked_add for weights) — SAFE
#### Sample 22: process_execute_transaction (checked_add for count) — SAFE

---

## Batch 6 Statistics

| Metric | Value |
|--------|-------|
| Total samples | 22 |
| SAFE samples | 18 |
| VULNERABLE samples | 4 |
| Source contract | 1 (Governance, 7 files) |
| Vulnerability types covered | V1, V4, V5, V6, V8, V9, V10 |

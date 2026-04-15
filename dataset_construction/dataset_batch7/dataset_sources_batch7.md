# Dataset Sources Documentation — Batch 7

## Contracts in This Batch

| # | Contract | Repository | File | Lines of Code |
|---|----------|------------|------|---------------|
| 13 | Token Upgrade | solana-labs/solana-program-library/token-upgrade | program/src/processor.rs | 170 |
| 14 | Record | solana-program/record | program/src/processor.rs | 173 |
| 15 | Feature Proposal | solana-program/feature-proposal | program/src/processor.rs | 291 |

**Repository URLs:**
- Token Upgrade: https://github.com/solana-labs/solana-program-library/blob/master/token-upgrade/program/src/processor.rs
- Record: https://github.com/solana-program/record/blob/main/program/src/processor.rs
- Feature Proposal: https://github.com/solana-program/feature-proposal/blob/main/program/src/processor.rs

---

## Extraction Methods

| Method | Description | Verification |
|--------|-------------|--------------|
| **direct extraction** | Code copied verbatim from source, may be simplified for length | Compare with source at specified lines |
| **extracted and simplified** | Core logic preserved, boilerplate removed for training clarity | Key validation patterns match source |
| **modified from source** | Security checks removed to create VULNERABLE variant | Diff against SAFE version shows exact removals |

---

## Contract 13: Token Upgrade

**Source:** `solana-labs/solana-program-library/token-upgrade/program/src/processor.rs` (170 lines)
**URL:** https://github.com/solana-labs/solana-program-library/blob/master/token-upgrade/program/src/processor.rs

### V6 — Unchecked External Calls

#### Sample 1: process_exchange (burn + transfer with ?) — SAFE
- **Function:** `process_exchange` (lines 80–170)
- **Extraction:** extracted and simplified — kept 5 check_owner calls (L96–100), burn with ? (L143–151), transfer with ? (L153–162), data borrow/drop pattern (L108–140)
- **Security patterns present:**
  - `check_owner()` for all 5 accounts (original account, original mint, new escrow, new account, new mint)
  - `burn_original_tokens()` returns Result propagated with `?`
  - `transfer_new_tokens()` returns Result propagated with `?`
  - Data borrows dropped before CPIs to avoid double-borrow

#### Sample 2: process_exchange — VULNERABLE
- **Based on:** Same function, lines 80–170
- **Extraction:** modified from source
- **What was removed:**
  - Removed 5 check_owner calls (L96–100)
  - Replaced burn `?` with `let _ =` (L143–151) — error silently discarded
  - Removed escrow balance check (L128–134)
- **Resulting vulnerability:** Burn error silently discarded — user gets new tokens without burning originals. No ownership verification allows cross-program accounts.

### V9 — Bump Seed Canonicalization

#### Sample 3: process_exchange (PDA derivation) — SAFE
- **Function:** `process_exchange` (lines 102–117)
- **Extraction:** extracted and simplified — kept `get_token_upgrade_authority_address_and_bump_seed` (uses find_program_address internally, L103–104), authority verification (L112–117)
- **Security patterns present:**
  - `get_token_upgrade_authority_address_and_bump_seed()` uses `find_program_address` internally
  - Derived authority verified against provided account (L112–117)
  - Seeds include both original and new mint for uniqueness

### V4 — Input Validation (Type Confusion)

#### Sample 4: process_exchange (decimals + escrow validation) — SAFE
- **Function:** `process_exchange` (lines 108–140)
- **Extraction:** extracted and simplified — kept mint unpacking, escrow balance check (L128–134), decimals mismatch check (L135–141)
- **Security patterns present:**
  - Both mints unpacked and validated as actual Mint accounts via `StateWithExtensions::<Mint>::unpack`
  - Escrow balance checked: `new_escrow.base.amount < token_amount` returns InsufficientFunds
  - Decimals consistency enforced: `original_mint.base.decimals != new_mint.base.decimals` returns DecimalsMismatch

#### Sample 5: process_exchange — VULNERABLE
- **Based on:** Same function, lines 80–170
- **Extraction:** modified from source
- **What was removed:**
  - Removed check_owner calls (L96–100)
  - Removed escrow balance check (L128–134)
  - Removed decimals mismatch check (L135–141)
  - Removed new_mint unpacking
- **Resulting vulnerability:** Exchanging 6-decimal tokens for 9-decimal gives 1000x value. No escrow balance validation allows transfer failure or over-drain.

### V5 — CPI Reentrancy

#### Sample 6: process_exchange (burn-then-transfer) — SAFE
- **Function:** `process_exchange` (lines 108–170)
- **Extraction:** extracted and simplified — kept data borrow/drop pattern (L108–140), burn-then-transfer CPI ordering (burn L143–151, transfer L153–162)
- **Security pattern:** CEI pattern — data borrows dropped before CPIs, originals burned first, then new tokens transferred. During transfer CPI, originals already destroyed.

#### Sample 7: process_exchange — VULNERABLE
- **Based on:** Same function, lines 143–170
- **Extraction:** modified from source — reversed CPI order: transfer_new_tokens (originally L153) before burn_original_tokens (originally L143)
- **Resulting vulnerability:** New tokens transferred before originals burned. Attacker can re-enter during transfer and exchange same originals again.

---

## Contract 14: Record

**Source:** `solana-program/record/program/src/processor.rs` (173 lines)
**URL:** https://github.com/solana-program/record/blob/main/program/src/processor.rs

### V6 — Unchecked External Calls

#### Sample 8: CloseAccount (checked_add for lamports) — SAFE
- **Function:** `CloseAccount` handler (lines 112–133)
- **Extraction:** direct extraction
- **Security patterns present:**
  - `check_authority()` validates key match AND signer status
  - `is_initialized()` check prevents closing uninitialized accounts
  - `checked_add` for lamport transfer (L129–131) prevents overflow
  - Account lamports set to 0 after transfer

### V4 — Input Validation (Type Confusion)

#### Sample 9: Initialize (size + re-init checks) — SAFE
- **Function:** `Initialize` handler (lines 36–53)
- **Extraction:** direct extraction
- **Security patterns present:**
  - `raw_data.len() < RecordData::WRITABLE_START_INDEX` minimum size check (L42–44)
  - `is_initialized()` prevents re-initialization (L49–52)
  - `bytemuck::try_from_bytes_mut` validates data alignment and size

#### Sample 10: Write (bounds checking) — SAFE
- **Function:** `Write` handler (lines 55–84)
- **Extraction:** direct extraction
- **Security patterns present:**
  - Initialization check (L66–69)
  - `check_authority()` for authorization (L70)
  - `saturating_add` for offset calculation (L76–77) prevents overflow
  - Bounds check `end > data_info.data.borrow().len()` (L78–79) prevents buffer overflow

#### Sample 11: Write — VULNERABLE
- **Based on:** Same function, lines 55–84
- **Extraction:** modified from source
- **What was removed:**
  - Removed authority check
  - Removed initialization check (L66–69)
  - Replaced saturating_add with unchecked + (L76–77)
  - Removed bounds check (L78–79)
- **Resulting vulnerability:** Anyone can write to any record. Offset overflow causes out-of-bounds panic. Uninitialized accounts writable.

### V10 — Denial of Service

#### Sample 12: Reallocate (authority + size checks) — SAFE
- **Function:** `Reallocate` handler (lines 135–173)
- **Extraction:** direct extraction
- **Security patterns present:**
  - Authority and initialization checks
  - `checked_add` for size calculation (L156–159)
  - `usize::try_from` validates u64→usize conversion
  - No-op if already large enough (L162–164)
  - `data_info.resize()` enforces system max realloc limits

### V1 — Access Control (Missing Key Check)

#### Sample 13: SetAuthority (authority check) — SAFE
- **Function:** `SetAuthority` handler (lines 86–110)
- **Extraction:** direct extraction
- **Security patterns present:**
  - `check_authority()` validates: (1) authority key matches stored authority, (2) authority is a signer
  - `is_initialized()` prevents modifying uninitialized records
  - Only current authority can transfer control

#### Sample 14: SetAuthority — VULNERABLE
- **Based on:** Same function, lines 86–110
- **Extraction:** modified from source
- **What was removed:**
  - Removed `check_authority` call (L104)
  - Removed initialization check (L101–104)
  - Removed data size check (L93–95)
- **Resulting vulnerability:** Anyone can change authority of any record. No signer verification. Uninitialized accounts modifiable.

### V8 — Integer Overflow/Underflow

#### Sample 15: Write (saturating_add for bounds) — SAFE
- **Function:** `Write` handler (lines 55–84)
- **Extraction:** extracted and simplified — kept saturating_add for start (L76) and end (L77), bounds check (L78–79)
- **Security pattern:** `saturating_add` prevents overflow — if overflow would occur, value saturates to usize::MAX, always exceeding data_len, triggering AccountDataTooSmall error.

#### Sample 16: Reallocate (checked_add for size) — SAFE
- **Function:** `Reallocate` handler (lines 150–173)
- **Extraction:** extracted and simplified — kept usize::try_from validation, checked_add for size (L156–159)
- **Security pattern:** `usize::try_from` prevents u64→usize conversion issues. `checked_add` prevents size calculation overflow.

---

## Contract 15: Feature Proposal

**Source:** `solana-program/feature-proposal/program/src/processor.rs` (291 lines)
**URL:** https://github.com/solana-program/feature-proposal/blob/main/program/src/processor.rs

### V6 — Unchecked External Calls

#### Sample 17: Propose (invoke/invoke_signed chain with ?) — SAFE
- **Function:** `process_propose` (lines 37–224)
- **Extraction:** extracted and simplified — kept PDA verification (L56–72), full invoke/invoke_signed chain with ? propagation
- **Security patterns present:**
  - 4 PDA addresses derived and verified before any CPI
  - All CPIs (create_account, initialize_mint, mint_to) use `?`
  - Atomic — if any step fails, entire transaction reverts

#### Sample 18: Tally (invoke_signed with ?) — SAFE
- **Function:** `process_tally` (lines 226–291)
- **Extraction:** extracted and simplified — kept PDA re-derivation (L238–251), deadline check (L258–262), threshold check (L268–271), invoke_signed with ? (L273–277)
- **Security patterns present:**
  - PDA addresses re-derived and verified (not trusted from caller)
  - Deadline and threshold checked BEFORE any CPI
  - `invoke_signed` with `?` for feature assignment
  - State transitions only after successful CPI

### V9 — Bump Seed Canonicalization

#### Sample 19: Propose (4 PDA derivations with verification) — SAFE
- **Function:** `process_propose` (lines 53–72)
- **Extraction:** extracted and simplified — kept 4 PDA derivations: mint (L53–56), distributor (L58–62), acceptance (L64–68), feature_id (L70–75)
- **Security patterns present:**
  - All 4 use `get_*_address_with_seed` (which calls `find_program_address` internally)
  - Each derived address verified against provided account
  - Canonical bumps stored and used for signing

### V10 — Denial of Service

#### Sample 20: Tally (deadline + threshold checks) — SAFE
- **Function:** `process_tally` (lines 226–291)
- **Extraction:** extracted and simplified — kept Pending state match, deadline check (L258–262), threshold check (L268–271)
- **Security patterns present:**
  - State match: only `FeatureProposal::Pending` can be tallied
  - Expired proposals gracefully transition to `Expired` state (no error, clean transition)
  - Insufficient tokens return `Ok(())` — no-op, not error (prevents griefing)
  - Feature activation only after threshold met

#### Sample 21: Tally — VULNERABLE
- **Based on:** Same function, lines 226–291
- **Extraction:** modified from source
- **What was removed:**
  - Removed Pending state check (L233–235) — any state can be tallied
  - Removed deadline check (L258–262) — premature acceptance
  - Removed threshold check (L268–271) — zero-token acceptance
  - Removed PDA re-verification (L238–251) — fake accounts accepted
- **Resulting vulnerability:** Already-accepted or expired proposals can be re-tallied. No deadline allows premature feature activation. No threshold allows zero-token acceptance — feature activated without any consensus.

---

## Verification Instructions

To verify any sample:

1. Open the source URL listed in the contract section above
2. Navigate to the function name and line numbers specified
3. For **SAFE** samples: confirm the security patterns listed are present in the original code
4. For **VULNERABLE** samples: confirm the "What was removed" items are present in the original but absent in the sample

---

## Batch 7 Statistics

| Metric | Value |
|--------|-------|
| Total samples | 21 |
| SAFE samples | 15 |
| VULNERABLE samples | 6 |
| Source contracts | 3 |
| Vulnerability types covered | V1, V4, V5, V6, V8, V9, V10 |

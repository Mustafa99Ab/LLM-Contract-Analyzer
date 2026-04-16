# Dataset Sources Documentation — Supplement: V4 + V10

## Purpose

This supplement adds 27 samples (6 SAFE + 21 VULNERABLE) to balance V4 and V10 distributions. Each VULNERABLE sample is the broken version of an existing SAFE sample or a new SAFE-VULN pair.

---

## V4 — Input Validation / Type Confusion (15 samples: 3 SAFE + 12 VULNERABLE)

**Result: V4 now balanced at 20 SAFE : 20 VULNERABLE ✅**

### VULNERABLE from existing SAFE pairs (10 samples)

#### Sample 1: process_transfer — VULNERABLE
- **Contract:** SPL Token | **Lines:** 227–341
- **SAFE pair:** Batch 1 | **What was removed:** frozen check (L249–251), mint mismatch (L255–257), delegate tracking (L287)

#### Sample 2: process_create_associated_token_account — VULNERABLE
- **Contract:** ATA | **Lines:** 94–115
- **SAFE pair:** Batch 2 | **What was removed:** owner match in idempotent mode (L100–103), mint match (L104–106), system_program ownership (L108–110)

#### Sample 3: process_deposit — VULNERABLE
- **Contract:** Binary Oracle Pair | **Lines:** 307–377
- **SAFE pair:** Batch 2 | **What was removed:** zero amount check (L327–329), slot timing check (L333–335)

#### Sample 4: _process_initialize_account — VULNERABLE
- **Contract:** Token-2022 | **Lines:** 168–253
- **SAFE pair:** Batch 4 | **What was removed:** check_program_account (L177–178), rent exemption (L197–199), mint validation (L203–204), extensions check (L212–218), native mint overflow protection (L240–244)

#### Sample 5: check_vote_account — VULNERABLE
- **Contract:** Single Pool | **Lines:** 243–258
- **SAFE pair:** Batch 4 | **What was removed:** check_account_owner for vote program (L244), discriminator validation (L246–257)

#### Sample 6: process_trade — VULNERABLE
- **Contract:** Binary Option | **Lines:** 187–544
- **SAFE pair:** Batch 5 | **What was removed:** checked_add price validation (L241–246), settled check (L247–249), buyer≠seller (L251), token account ownership (L254–259), mint key matching (L262–293)

#### Sample 7: process_accept_offer — VULNERABLE
- **Contract:** Stateless Asks | **Lines:** 182–269
- **SAFE pair:** Batch 5 | **What was removed:** delegated_amount check (L195–197), delegate match (L202–204), ATA assertions (L211–212)

#### Sample 8: process_create_proposal — VULNERABLE
- **Contract:** Governance | **Lines:** 37–183
- **SAFE pair:** Batch 6 | **What was removed:** ProposalAlreadyExists (L62–63), governing_token_mint_can_vote (L79–83), voter weight check (L101–105), proposal options validation (L112), outstanding count (L108–110)

#### Sample 9: process_create_realm — VULNERABLE
- **Contract:** Governance | **Lines:** 32–155
- **SAFE pair:** Batch 6 | **What was removed:** RealmAlreadyExists (L52–54), config validation (L56), token config resolution (L98–107), RealmConfig creation (L104–111)

#### Sample 10: Initialize — VULNERABLE
- **Contract:** Record | **Lines:** 36–53
- **SAFE pair:** Batch 7 | **What was removed:** minimum data size check (L42–44), re-initialization check (L49–52)

### New SAFE-VULN pairs (2 VULNERABLE + 3 SAFE)

#### Sample 11: process_init_reserve — VULNERABLE
- **Contract:** Token Lending | **Lines:** 182–387
- **What was removed:** zero amount (L188–191), config.validate (L193), ownership checks (L217–220,L228–231), oracle validation (L245–284), authority PDA (L288–299)

#### Sample 12: process_swap — VULNERABLE
- **Contract:** Token Swap | **Lines:** 382–628
- **What was removed:** swap owner (L405–407), authority PDA (L410–414), account matching (L415–427), pool mint (L434–436), fee account (L437–439)

#### Sample 13: process_init_reserve — SAFE
- **Contract:** Token Lending | **Lines:** 182–387
- **Security:** zero amount, config.validate, ownership checks, oracle validation, authority PDA verification

#### Sample 14: process_swap — SAFE
- **Contract:** Token Swap | **Lines:** 382–442
- **Security:** ownership, authority PDA, account matching, same-account rejection, slippage protection

#### Sample 15: process_update_validator_list_balance — SAFE
- **Contract:** SPL Stake Pool | **Lines:** 1849–1898
- **Security:** ownership, state validity, validator list match, authority check, pairs validation

---

## V10 — Denial of Service (12 samples: 3 SAFE + 9 VULNERABLE)

### VULNERABLE from existing SAFE pairs (6 samples)

#### Sample 16: process_update_validator_list_balance — VULNERABLE
- **Contract:** SPL Stake Pool | **Lines:** 1849–1898
- **SAFE pair:** Sample 15 (above) | **What was removed:** is_valid (L1872–1874), check_validator_list (L1875), authority (L1876–1880), epoch rewards (L1885–1888), pairs validation (L1890–1898)

#### Sample 17: process_deposit_stake — VULNERABLE
- **Contract:** Single Pool | **Lines:** 931–1088
- **SAFE pair:** Batch 4 | **What was removed:** self-deposit prevention (L973–980), zero token check (L1059–1061), user stake authorization (L1002–1008)

#### Sample 18: process_close_account — VULNERABLE
- **Contract:** Token-2022 | **Lines:** 1288–1400
- **SAFE pair:** Batch 4 | **What was removed:** self-close (L1298–1300), non-zero balance (L1309–1311), validate_owner (L1316–1322), CPI guard (L1321–1325), checked_add for lamports

#### Sample 19: process_delete — VULNERABLE
- **Contract:** Name Service | **Lines:** 197–230
- **SAFE pair:** Batch 5 | **What was removed:** owner+signer check (L209–212), data zeroing (L215)

#### Sample 20: process_create_proposal — VULNERABLE
- **Contract:** Governance | **Lines:** 37–183
- **SAFE pair:** Batch 6 | **What was removed:** ProposalAlreadyExists (L62–63), voter weight (L101–105), outstanding count limit (L108–110), active count tracking (L164–166)

#### Sample 21: Reallocate — VULNERABLE
- **Contract:** Record | **Lines:** 135–173
- **SAFE pair:** Batch 7 | **What was removed:** authority check, initialization check (L148–153), checked_add → unchecked + (L156–159), usize::try_from (L157)

### New SAFE-VULN pairs (3 SAFE + 3 VULNERABLE)

#### Sample 22: process_redeem_reserve_collateral — SAFE
- **Contract:** Token Lending | **Lines:** 516–613
- **Security:** zero amount, ownership, stale check, self-collateral prevention

#### Sample 23: process_redeem_reserve_collateral — VULNERABLE
- **What was removed:** zero amount (L521–524), ownership (L539–542,L548–552), stale check (L573–576), self-collateral (L561–564)

#### Sample 24: process_repay_obligation_liquidity — SAFE
- **Contract:** Token Lending | **Lines:** 1212–1314
- **Security:** zero amount, ownership, dual stale checks, zero borrow check, minimum repay

#### Sample 25: process_repay_obligation_liquidity — VULNERABLE
- **What was removed:** zero amount (L1218–1221), ownership (L1234–1237,L1244–1247), stale checks (L1260–1263,L1274–1277), zero borrow (L1281–1284)

#### Sample 26: process_collect — SAFE
- **Contract:** Binary Option | **Lines:** 626–744
- **Security:** settled check, mint ownership, account ownership, escrow matching, winning side validation

#### Sample 27: process_collect — VULNERABLE
- **What was removed:** settled check (L666–668), mint ownership (L669–670), collector ownership (L671–673), winning side logic (L700–706)

---

## Supplement Statistics

| Metric | Value |
|--------|-------|
| Total samples | 27 |
| SAFE | 6 |
| VULNERABLE | 21 |
| V4 samples | 15 (3S + 12V) |
| V10 samples | 12 (3S + 9V) |
| Contracts referenced | 12 |

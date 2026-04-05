# Dataset Construction Methodology

## Solana Smart Contract Vulnerability Detection Dataset

---

## Overview

This document describes the methodology used to construct the **Solana Smart Contract Vulnerability Dataset** for LLM fine-tuning. The dataset comprises **285 samples** (145 SAFE + 140 VULNERABLE) across 7 vulnerability categories based on OWASP Smart Contract Top 10.

---

## Dataset Statistics

| Metric | Value |
|--------|-------|
| **Total Samples** | 285 |
| **SAFE** | 145 (51%) |
| **VULNERABLE** | 140 (49%) |
| **Vulnerability Types** | 7 |
| **Source Contracts** | 15 |
| **Total Source Code** | ~28,000+ lines of production Rust/Solana code |

---

## Source Repositories

The dataset was derived from **15 official Solana program repositories**:

| # | Source | Repository | Samples |
|---|--------|------------|---------|
| 1 | SPL Stake Pool | solana-program/stake-pool | 32 |
| 2 | SPL Token | solana-program/token | 20 |
| 3 | Associated Token Account | solana-program/associated-token-account | 14 |
| 4 | Binary Oracle Pair | solana-labs/solana-program-library/binary-oracle-pair | 16 |
| 5 | Token Swap | solana-labs/solana-program-library/token-swap | 24 |
| 6 | Token Lending | solana-labs/solana-program-library/token-lending | 33 |
| 7 | Single Pool | solana-program/single-pool | 29 |
| 8 | Token-2022 | solana-program/token-2022 | 16 |
| 9 | Name Service | solana-labs/solana-program-library/name-service | 14 |
| 10 | Binary Option | solana-labs/solana-program-library/binary-option | 15 |
| 11 | Stateless Asks | solana-labs/solana-program-library/stateless-asks | 9 |
| 12 | Governance | solana-labs/solana-program-library/governance | 35 |
| 13 | Token Upgrade | solana-labs/solana-program-library/token-upgrade | 8 |
| 14 | Record | solana-program/record | 12 |
| 15 | Feature Proposal | solana-program/feature-proposal | 8 |

---

## Vulnerability Categories

Based on OWASP Smart Contract Top 10 (2025):

| Code | Vulnerability Type | Description | SAFE | VULN | Total |
|------|-------------------|-------------|------|------|-------|
| V1 | Missing Key Check | Missing signer/owner verification | 20 | 20 | 40 |
| V4 | Input Validation (Type Confusion) | Improper account type validation | 20 | 20 | 40 |
| V5 | CPI Reentrancy | Unsafe Cross-Program Invocation ordering | 22 | 20 | 42 |
| V6 | Unchecked External Calls | Missing CPI return value checks | 20 | 20 | 40 |
| V8 | Integer Overflow/Underflow | Unchecked arithmetic operations | 23 | 20 | 43 |
| V9 | Bump Seed Canonicalization | PDA non-canonical derivation | 20 | 20 | 40 |
| V10 | Denial of Service (DoS) | Missing guards against resource abuse | 20 | 20 | 40 |
| | **Total** | | **145** | **140** | **285** |

---

## Sample Generation Methodology

### SAFE Samples: Direct Extraction from Production Code

SAFE samples were **directly extracted** from real, deployed Solana smart contracts on GitHub. These contracts have been audited, are actively used on mainnet, and represent genuine secure coding patterns.

**Process:**
1. Identify a function with clear security patterns (e.g., `validate_owner`, `checked_add`, `find_program_address`)
2. Extract the relevant code, simplifying boilerplate while preserving all security checks
3. Document the source: contract name, function name, line numbers, GitHub URL

### VULNERABLE Samples: Systematic Security Check Removal

VULNERABLE samples were created by **removing specific security checks** from the SAFE originals. Each removal is precisely documented.

**Process:**
1. Take an existing SAFE sample
2. Remove one or more specific security checks (documented by line number)
3. Verify the resulting code represents a realistic vulnerability
4. Document exactly what was removed and why it creates a vulnerability

### Key Principles

| Principle | Description |
|-----------|-------------|
| **Real Source Code** | All samples originate from real deployed contracts, not synthetic generation |
| **No Data Leakage** | No revealing comments like `// VULNERABLE` or `// SAFE` in code |
| **Documented Modifications** | Every VULNERABLE sample documents exactly which lines were removed |
| **Balanced Distribution** | 20 SAFE + 20 VULNERABLE per vulnerability type |
| **Source Traceability** | Each sample links to its GitHub source with function name and line numbers |

---

## Vulnerability Patterns: Before & After

### 1. Missing Key Check (V1)

**SAFE (Original — Token Swap `check_accounts` L194-244):**
```rust
fn check_accounts(token_swap: &dyn SwapState, program_id: &Pubkey,
    swap_account_info: &AccountInfo, authority_info: &AccountInfo,
    token_a_info: &AccountInfo, token_b_info: &AccountInfo,
) -> ProgramResult {
    if swap_account_info.owner != program_id {
        return Err(ProgramError::IncorrectProgramId);
    }
    if *authority_info.key != Self::authority_id(program_id, swap_account_info.key, token_swap.bump_seed())? {
        return Err(SwapError::InvalidProgramAddress.into());
    }
    if *token_a_info.key != *token_swap.token_a_account() {
        return Err(SwapError::IncorrectSwapAccount.into());
    }
    Ok(())
}
```

**VULNERABLE (Modified — removed all checks):**
```rust
fn check_accounts(token_swap: &dyn SwapState, program_id: &Pubkey,
    swap_account_info: &AccountInfo, authority_info: &AccountInfo,
    token_a_info: &AccountInfo, token_b_info: &AccountInfo,
) -> ProgramResult {
    Ok(())
}
```

**What was removed:** Program ownership (L208-210), authority PDA verification (L211-215), token account matching (L216-221), pool mint matching (L222-224).

---

### 2. Bump Seed Canonicalization (V9)

**SAFE (Original — Token Swap `process_initialize` L269-270):**
```rust
let (swap_authority, bump_seed) =
    Pubkey::find_program_address(&[&swap_info.key.to_bytes()], program_id);
if *authority_info.key != swap_authority {
    return Err(SwapError::InvalidProgramAddress.into());
}
```

**VULNERABLE (Modified — user-provided bump):**
```rust
let swap_authority = Pubkey::create_program_address(
    &[&swap_info.key.to_bytes(), &[bump_seed]], program_id)?;
if *authority_info.key != swap_authority {
    return Err(SwapError::InvalidProgramAddress.into());
}
```

**What was changed:** `find_program_address` (derives canonical bump) replaced with `create_program_address` (accepts user-provided bump). Multiple valid PDAs become possible.

---

### 3. Integer Overflow (V8)

**SAFE (Original — Token-2022 `process_mint_to` L1084-1087):**
```rust
mint.base.supply = u64::from(mint.base.supply)
    .checked_add(amount)
    .ok_or(TokenError::Overflow)?;
```

**VULNERABLE (Modified — unchecked arithmetic):**
```rust
mint.base.supply = u64::from(mint.base.supply) + amount;
```

**What was changed:** `checked_add` with error handling replaced with unchecked `+`. Supply can overflow to near-zero.

---

### 4. CPI Reentrancy (V5)

**SAFE (Original — Token Swap `process_withdraw_all` L822-854):**
```rust
// FIRST: Burn pool tokens (destroy LP position)
Self::token_burn(swap_info.key, pool_token_program_info.clone(),
    source_info.clone(), pool_mint_info.clone(), authority_info.clone(),
    token_swap.bump_seed(), pool_token_amount)?;

// THEN: Transfer tokens A and B out
Self::token_transfer(swap_info.key, /* ... */, token_a_amount)?;
Self::token_transfer(swap_info.key, /* ... */, token_b_amount)?;
```

**VULNERABLE (Modified — reversed CPI order):**
```rust
// WRONG: Transfer tokens out FIRST
Self::token_transfer(swap_info.key, /* ... */, token_a_amount)?;
Self::token_transfer(swap_info.key, /* ... */, token_b_amount)?;

// THEN burn — but user already has A and B
Self::token_burn(swap_info.key, pool_token_program_info.clone(),
    source_info.clone(), pool_mint_info.clone(), authority_info.clone(),
    token_swap.bump_seed(), pool_token_amount)?;
```

**What was changed:** Burn-then-transfer (CEI pattern) reversed to transfer-then-burn. During transfer CPI, pool tokens still exist for re-entry.

---

### 5. Denial of Service (V10)

**SAFE (Original — SPL Token `process_initialize_mint` L42-84):**
```rust
let mut mint = Mint::unpack_unchecked(&mint_info.data.borrow())?;
if mint.is_initialized {
    return Err(TokenError::AlreadyInUse.into());
}
if !Rent::from_account_info(rent)?.is_exempt(mint_info.lamports(), Mint::LEN) {
    return Err(TokenError::NotRentExempt.into());
}
mint.supply = 0;
```

**VULNERABLE (Modified — removed guards):**
```rust
let mut mint = Mint::unpack_unchecked(&mint_info.data.borrow())?;
mint.mint_authority = COption::Some(*mint_authority);
mint.is_initialized = true;
Mint::pack(mint, &mut mint_info.data.borrow_mut())?;
```

**What was removed:** Re-initialization check (L53-55), rent exemption check (L56-58), supply reset to 0.

---

### 6. Unchecked External Calls (V6)

**SAFE (Original — SPL Stake Pool `token_mint_to` L586-609):**
```rust
let ix = spl_token_2022::instruction::mint_to(
    token_program.key, mint.key, destination.key, authority.key, &[], amount)?;
invoke_signed(&ix, &[mint, destination, authority, token_program], signers)
```

**VULNERABLE (Modified — errors discarded):**
```rust
let ix = spl_token_2022::instruction::mint_to(
    token_program.key, mint.key, destination.key, authority.key, &[], amount).unwrap();
let _ = invoke_signed(&ix, &[mint, destination, authority, token_program], signers);
Ok(())
```

**What was changed:** `?` on instruction creation replaced with `.unwrap()` (panics). `invoke_signed` result replaced with `let _ =` (error silently discarded). Mint failure goes unnoticed.

---

### 7. Input Validation / Type Confusion (V4)

**SAFE (Original — Token-2022 `_process_initialize_account` L168-253):**
```rust
check_program_account(new_account_info.owner)?;
check_program_account(mint_info.owner)?;

let mut account = PodStateWithExtensionsMut::<PodAccount>::unpack_uninitialized(&mut account_data)?;
if !rent.is_exempt(new_account_info.lamports(), new_account_info_data_len) {
    return Err(TokenError::NotRentExempt.into());
}
let mint = PodStateWithExtensions::<PodMint>::unpack(&mint_data)
    .map_err(|_| Into::<ProgramError>::into(TokenError::InvalidMint))?;
```

**VULNERABLE (Modified — removed all validation):**
```rust
let mut account = PodStateWithExtensionsMut::<PodAccount>::unpack_uninitialized(&mut account_data)?;
account.base.mint = *mint_info.key;
account.base.owner = *owner;
account.base.state = AccountState::Initialized.into();
account.init_account_type()?;
```

**What was removed:** `check_program_account` for both accounts (L177-178), rent exemption (L197-199), mint validation via unpack (L203-204), required extensions check (L212-218), native mint overflow protection (L240-244).

---

## Source Verification

Each sample includes a `source_info` object:

```json
{
  "source_info": {
    "origin": "solana-labs/solana-program-library/token-swap",
    "file": "program/src/processor.rs",
    "url": "https://github.com/solana-labs/solana-program-library/blob/master/token-swap/program/src/processor.rs",
    "function": "check_accounts",
    "lines": "194-244",
    "extraction_method": "modified from source - removed ALL checks: program ownership (L208-210), authority PDA (L211-215), token_a match (L216-218)"
  }
}
```

**To verify any sample:**
1. Open the `url` in a browser
2. Navigate to the `function` at the specified `lines`
3. For SAFE: confirm the security patterns are present in the original
4. For VULNERABLE: confirm the `extraction_method` items are present in the original but absent in the sample

---

## Dataset Format

Each sample follows the LLaMA-3 instruction template:

```json
{
  "text": "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\nYou are a Solana smart contract security analyzer...<|eot_id|><|start_header_id|>user<|end_header_id|>\n\nCode:\n[RUST CODE]<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n[ANALYSIS]<|eot_id|>",
  "label": "SAFE",
  "vulnerability_type": "Missing Key Check",
  "owasp_code": "V1",
  "source_info": { ... }
}
```

---

## File Structure

| File | Description | Samples |
|------|-------------|---------|
| `dataset_batch1_stake_pool_token.json` | SPL Stake Pool + SPL Token | 33 |
| `dataset_batch2_ata_binary_oracle.json` | ATA + Binary Oracle Pair | 24 |
| `dataset_batch3_token_swap_lending.json` | Token Swap + Token Lending | 31 |
| `dataset_batch4_single_pool_token2022.json` | Single Pool + Token-2022 | 28 |
| `dataset_batch5_nameservice_binaryoption_statelessasks.json` | Name Service + Binary Option + Stateless Asks | 24 |
| `dataset_batch6_governance.json` | Governance (7 processor files) | 22 |
| `dataset_batch7_tokenupgrade_record_featureproposal.json` | Token Upgrade + Record + Feature Proposal | 21 |
| `dataset_supplement_v9_v6_vulnerable.json` | V9 + V6 balance supplement | 30 |
| `dataset_supplement_v4_v10.json` | V4 + V10 balance supplement | 27 |
| `dataset_supplement_v5_v1.json` | V5 + V1 balance supplement | 22 |
| `dataset_supplement_final.json` | Final balance supplement | 23 |
| `dataset_final_merged.json` | **All samples merged (use this for training)** | **285** |

Each batch JSON has a corresponding `dataset_sources_*.md` documentation file.

---

## References

1. **Solana Program Library**: https://github.com/solana-labs/solana-program-library
2. **Solana Program (migrated repos)**: https://github.com/solana-program
3. **OWASP Smart Contract Top 10 (2025)**: https://owasp.org/www-project-smart-contract-top-10/
4. **Sealevel Attacks**: https://github.com/coral-xyz/sealevel-attacks
5. Boi, B. & Esposito, C. (2025). *Prompt Engineering vs. Fine-Tuning for LLM-Based Vulnerability Detection in Solana and Algorand Smart Contracts*. IEEE BCCA 2025.

---

*Document Version: 3.0*
*Last Updated: April 2026*
*Author: Mustafa Hafed*
*Supervisor: Prof. Biagio Boi, University of Salerno*
*Dataset: dataset_final_merged.json (285 samples)*

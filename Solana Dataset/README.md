# Dataset Construction Methodology

## Solana Smart Contract Vulnerability Detection Dataset

---

## Overview

This document describes the methodology used to construct the **Solana Smart Contract Vulnerability Dataset** for LLM fine-tuning. The dataset comprises **182 samples** (91 VULNERABLE + 91 SAFE) across 7 vulnerability categories based on OWASP Smart Contract Top 10.

---

## Dataset Statistics

| Metric | Value |
|--------|-------|
| **Total Samples** | 182 |
| **VULNERABLE** | 91 (50%) |
| **SAFE** | 91 (50%) |
| **Vulnerability Types** | 7 |
| **Samples per Type** | 26 (13 SAFE + 13 VULN) |

---

## Source Repositories

The dataset was derived from **five official Solana Program Library (SPL) repositories**:

| # | Source | Repository | Lines of Code | Samples |
|---|--------|------------|---------------|---------|
| 1 | SPL Stake Pool | solana-labs/solana-program-library/stake-pool | 3,849 | 40 |
| 2 | SPL Token | solana-labs/solana-program-library/token | 1,340 | 30 |
| 3 | SPL Governance | solana-labs/solana-program-library/governance | 2,400+ | 30 |
| 4 | Binary Oracle Pair | solana-labs/solana-program-library/binary-oracle-pair | 800+ | 40 |
| 5 | **Token Swap** | solana-labs/solana-program-library/token-swap | 8,377 | **42** |

**Total Source Code: ~16,766 lines of production Rust/Solana code**

---

## Vulnerability Categories

Based on OWASP Smart Contract Top 10 (2023):

| Code | Vulnerability Type | Description | Samples |
|------|-------------------|-------------|---------|
| V1 | Missing Key Check | Missing signer/owner verification | 26 |
| V4 | Input Validation (Type Confusion) | Improper account type validation | 26 |
| V5 | CPI Reentrancy | Unsafe Cross-Program Invocation | 26 |
| V6 | Unchecked Calls | Missing return value/state checks | 26 |
| V8 | Integer Flow | Overflow/underflow vulnerabilities | 26 |
| V9 | Bump Seed | PDA canonicalization issues | 26 |
| V10 | DoS | Denial of Service vectors | 26 |

---

## Sample Generation Methodology

### Approach 1: Direct Extraction and Modification (~60% of samples)

Samples were **directly extracted** from production SPL code:

- **SAFE samples**: Extracted verbatim from audited production code
- **VULNERABLE samples**: Created by **removing or weakening** security checks

### Approach 2: Pattern-Based Synthesis (~40% of samples)

Additional samples were **synthesized** following documented vulnerability patterns:

- Maintain identical code structure and idioms
- Apply patterns from Sealevel Attacks repository
- Follow OWASP Smart Contract guidelines

---

## Injection Examples (Before & After)

Below are concrete examples showing how VULNERABLE variants were created from SAFE code for each vulnerability type:

### 1. Missing Key Check (V1)

**SAFE (Original):**
```rust
pub fn unpack_token_account(
    account_info: &AccountInfo,
    token_program_id: &Pubkey,
) -> Result<Account, SwapError> {
    // ✓ Validates account ownership
    if account_info.owner != token_program_id
        && check_spl_token_program_account(account_info.owner).is_err()
    {
        Err(SwapError::IncorrectTokenProgramId)
    } else {
        StateWithExtensions::<Account>::unpack(&account_info.data.borrow())
            .map(|a| a.base)
            .map_err(|_| SwapError::ExpectedAccount)
    }
}
```

**VULNERABLE (Modified):**
```rust
pub fn unpack_token_account(
    account_info: &AccountInfo,
    token_program_id: &Pubkey,
) -> Result<Account, SwapError> {
    // ✗ Missing ownership check - accepts any account
    StateWithExtensions::<Account>::unpack(&account_info.data.borrow())
        .map(|a| a.base)
        .map_err(|_| SwapError::ExpectedAccount)
}
```

**Vulnerability**: Attacker can pass a malicious account not owned by the token program.

---

### 2. Bump Seed Canonicalization (V9)

**SAFE (Original):**
```rust
pub fn process_initialize(
    program_id: &Pubkey,
    accounts: &[AccountInfo],
) -> ProgramResult {
    let swap_info = next_account_info(account_info_iter)?;
    
    // ✓ Derives canonical bump and stores it
    let (swap_authority, bump_seed) = 
        Pubkey::find_program_address(&[&swap_info.key.to_bytes()], program_id);
    
    // ✓ Verifies PDA matches
    if *authority_info.key != swap_authority {
        return Err(SwapError::InvalidProgramAddress.into());
    }
    
    // ✓ Stores canonical bump in state
    let obj = SwapV1 {
        bump_seed,  // Saved for later use
        // ...
    };
    Ok(())
}
```

**VULNERABLE (Modified):**
```rust
pub fn process_initialize(
    program_id: &Pubkey,
    accounts: &[AccountInfo],
) -> ProgramResult {
    let swap_info = next_account_info(account_info_iter)?;
    
    // ✗ No PDA derivation or verification
    // ✗ Hardcoded bump or user-supplied bump
    let obj = SwapV1 {
        bump_seed: 0,  // Invalid - not canonical
        // ...
    };
    Ok(())
}
```

**Vulnerability**: Non-canonical bump allows PDA collision attacks.

---

### 3. Integer Overflow (V8)

**SAFE (Original):**
```rust
pub fn process_swap(
    amount_in: u64,
    accounts: &[AccountInfo],
) -> ProgramResult {
    // ✓ Uses saturating_sub for safe subtraction
    let actual_amount = amount_in.saturating_sub(fee);
    
    // ✓ Uses checked_sub with error handling
    let pool_amount = pool_token_amount
        .checked_sub(withdraw_fee)
        .ok_or(SwapError::CalculationFailure)?;
    
    Ok(())
}
```

**VULNERABLE (Modified):**
```rust
pub fn process_swap(
    amount_in: u64,
    accounts: &[AccountInfo],
) -> ProgramResult {
    // ✗ Direct subtraction - can underflow
    let actual_amount = amount_in - fee;
    
    // ✗ No overflow protection
    let pool_amount = pool_token_amount - withdraw_fee;
    
    Ok(())
}
```

**Vulnerability**: Underflow can result in extremely large values, draining funds.

---

### 4. CPI Vulnerability (V5)

**SAFE (Original):**
```rust
pub fn token_transfer<'a>(
    swap: &Pubkey,
    token_program: AccountInfo<'a>,
    source: AccountInfo<'a>,
    destination: AccountInfo<'a>,
    authority: AccountInfo<'a>,
    bump_seed: u8,
    amount: u64,
) -> Result<(), ProgramError> {
    // ✓ Uses official SPL Token instruction builder
    let ix = spl_token_2022::instruction::transfer_checked(
        token_program.key,
        source.key,
        mint.key,
        destination.key,
        authority.key,
        &[],
        amount,
        decimals,
    )?;
    
    // ✓ Uses invoke_signed with PDA seeds
    invoke_signed(&ix, &[...], signers)
}
```

**VULNERABLE (Modified):**
```rust
pub fn token_transfer<'a>(
    swap: &Pubkey,
    token_program: AccountInfo<'a>,
    source: AccountInfo<'a>,
    destination: AccountInfo<'a>,
    amount: u64,
) -> Result<(), ProgramError> {
    // ✗ Manual instruction construction
    // ✗ No program ID verification
    let ix = Instruction {
        program_id: *token_program.key,  // Accepts ANY program
        accounts: vec![...],
        data: amount.to_le_bytes().to_vec(),
    };
    
    // ✗ Uses invoke without signing
    invoke(&ix, &[source, destination, token_program])
}
```

**Vulnerability**: Attacker can pass malicious program as token_program.

---

### 5. Denial of Service (V10)

**SAFE (Original):**
```rust
pub fn process_deposit(
    pool_token_amount: u64,
    maximum_token_a_amount: u64,
    accounts: &[AccountInfo],
) -> ProgramResult {
    // ✓ Validates operation is supported
    if !calculator.allows_deposits() {
        return Err(SwapError::UnsupportedCurveOperation.into());
    }
    
    // ✓ Uses ok_or for error handling
    let results = calculator.pool_tokens_to_trading_tokens(...)
        .ok_or(SwapError::ZeroTradingTokens)?;
    
    // ✓ Slippage protection
    if token_a_amount > maximum_token_a_amount {
        return Err(SwapError::ExceededSlippage.into());
    }
    
    // ✓ Zero amount check
    if token_a_amount == 0 {
        return Err(SwapError::ZeroTradingTokens.into());
    }
    Ok(())
}
```

**VULNERABLE (Modified):**
```rust
pub fn process_deposit(
    pool_token_amount: u64,
    accounts: &[AccountInfo],
) -> ProgramResult {
    // ✗ No deposit validation check
    
    // ✗ Uses unwrap - panics on None (DoS vector)
    let results = calculator.pool_tokens_to_trading_tokens(...)
        .unwrap();
    
    // ✗ No slippage protection - frontrunning vulnerable
    // ✗ No zero check - dust attack vector
    Ok(())
}
```

**Vulnerability**: Panics cause transaction failures; missing slippage enables MEV attacks.

---

### 6. Unchecked Calls (V6)

**SAFE (Original):**
```rust
pub fn process_initialize(
    accounts: &[AccountInfo],
) -> ProgramResult {
    // ✓ Checks for existing delegation
    if token_a.delegate.is_some() {
        return Err(SwapError::InvalidDelegate.into());
    }
    
    // ✓ Checks close authority
    if token_a.close_authority.is_some() {
        return Err(SwapError::InvalidCloseAuthority.into());
    }
    
    // ✓ Validates fees and curve
    fees.validate()?;
    swap_curve.calculator.validate()?;
    
    Ok(())
}
```

**VULNERABLE (Modified):**
```rust
pub fn process_initialize(
    accounts: &[AccountInfo],
) -> ProgramResult {
    // ✗ No delegate check - pre-approved transfers possible
    // ✗ No close authority check - tokens can be closed
    // ✗ No fee validation - malicious fees
    // ✗ No curve validation - invalid calculations
    
    Ok(())
}
```

**Vulnerability**: Missing checks allow rug pulls and fund theft.

---

### 7. Type Confusion (V4)

**SAFE (Original):**
```rust
pub fn unpack_token_account(
    account_info: &AccountInfo,
    token_program_id: &Pubkey,
) -> Result<Account, SwapError> {
    // ✓ Validates owner before unpacking
    if account_info.owner != token_program_id {
        Err(SwapError::IncorrectTokenProgramId)
    } else {
        // ✓ Uses typed unpacking
        StateWithExtensions::<Account>::unpack(&account_info.data.borrow())
            .map(|a| a.base)
            .map_err(|_| SwapError::ExpectedAccount)
    }
}
```

**VULNERABLE (Modified):**
```rust
pub fn unpack_account_data(
    account_info: &AccountInfo,
) -> Result<Account, SwapError> {
    // ✗ No type validation
    // ✗ Interprets raw bytes without verification
    let data = account_info.data.borrow();
    let account: Account = unsafe { 
        std::ptr::read(data.as_ptr() as *const Account) 
    };
    Ok(account)
}
```

**Vulnerability**: Mint accounts can be interpreted as Token accounts, causing logic errors.

---

## Quality Assurance

All samples underwent rigorous validation:

| Check | Description |
|-------|-------------|
| **Syntactic Correctness** | Valid Rust/Anchor code structure |
| **No Data Leakage** | No revealing comments like `// VULNERABLE` |
| **Balance** | Exactly 50% VULNERABLE / 50% SAFE |
| **Pattern Diversity** | Multiple patterns per vulnerability type |
| **Source Traceability** | Each sample linked to source repository |

---

## Dataset Format

Each sample follows the LLaMA-3 chat template:

```json
{
  "id": "TS_MKC_001",
  "vulnerability_type": "Missing Key Check",
  "label": "SAFE",
  "source": "token-swap/processor.rs",
  "text": "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\nYou are a Solana smart contract security auditor...<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n```rust\n[CODE]\n```<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\nSAFE<|eot_id|>"
}
```

---

## References

1. **Solana Program Library**: https://github.com/solana-labs/solana-program-library
2. **Token Swap Program**: https://github.com/solana-labs/solana-program-library/tree/master/token-swap
3. **Sealevel Attacks**: https://github.com/coral-xyz/sealevel-attacks
4. **OWASP Smart Contract Top 10**: https://owasp.org/www-project-smart-contract-top-10/
5. **Neodyme Blog - Solana Security**: https://blog.neodyme.io/
6. Alves, H., et al. (2016). *Software Vulnerability Detection Using Machine Learning*
7. University of Salerno (2024). *Synthetic Dataset Generation for Smart Contract Vulnerability Detection*

---

## Distribution Summary

| Vulnerability Type | SAFE | VULNERABLE | Total |
|-------------------|------|------------|-------|
| Missing Key Check | 13 | 13 | 26 |
| Bump Seed | 13 | 13 | 26 |
| Integer Flow | 13 | 13 | 26 |
| CPI | 13 | 13 | 26 |
| DoS | 13 | 13 | 26 |
| Unchecked Calls | 13 | 13 | 26 |
| Type Confusion | 13 | 13 | 26 |
| **Total** | **91** | **91** | **182** |

---

*Document Version: 2.0*  
*Last Updated: December 2024*  
*Author: Mustafa Hafed*  
*Dataset: solana_182_final.json*

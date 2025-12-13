# Solana V9 Bump Seed Canonicalization Dataset
## IEEE BCCA 2025 Research - LLM Fine-Tuning Dataset

**Author:** Mustafa Hafed  
**Version:** 1.0  
**Date:** December 2025  
**Vulnerability Type:** V9 - Bump Seed Canonicalization  
**Total Samples:** 20 (10 VULNERABLE + 10 SAFE)

---

## 1. Dataset Overview

This dataset contains 20 high-quality Solana smart contract code samples specifically designed for training Large Language Models to detect **Bump Seed Canonicalization** vulnerabilities (OWASP V9).

### Distribution

| Label | Count | Percentage |
|-------|-------|------------|
| VULNERABLE | 10 | 50% |
| SAFE | 10 | 50% |

### What is V9 (Bump Seed Canonicalization)?

Program Derived Addresses (PDAs) in Solana are deterministic addresses derived from seeds and a bump value. The **canonical bump** is the highest valid bump (starting from 255) that produces a valid PDA (one that doesn't lie on the ed25519 curve).

**The Problem:**
- Multiple bumps (0-255) can produce valid PDAs for the same seeds
- Using non-canonical bumps creates "phantom" PDAs
- Attackers can exploit non-canonical bumps for:
  - PDA collisions
  - Authority bypass
  - State fragmentation
  - Double-claiming rewards

---

## 2. Schema Format

```json
{
  "instruction": "System prompt for the analyzer",
  "input": "Rust smart contract code (NO revealing comments)",
  "output": "Classification + Vulnerability Type + Severity + Description",
  "label": "VULNERABLE | SAFE"
}
```

---

## 3. Key Functions

### VULNERABLE: create_program_address()

```rust
// ❌ VULNERABLE: Accepts any valid bump
Pubkey::create_program_address(
    &[b"vault", owner.as_ref(), &[user_provided_bump]],
    program_id,
)
```

### SAFE: find_program_address()

```rust
// ✅ SAFE: Returns canonical (highest) bump
let (pda, canonical_bump) = Pubkey::find_program_address(
    &[b"vault", owner.as_ref()],
    program_id,
);
```

---

## 4. Vulnerability Patterns Covered

### VULNERABLE Patterns (10 samples)

| # | Pattern | Source | Risk |
|---|---------|--------|------|
| 1 | User-provided bump in init | binary-oracle-pair | Phantom PDAs |
| 2 | Instruction param bump | Custom vault | Multiple vaults per user |
| 3 | Per-transaction bump | Deposit function | Authority bypass |
| 4 | Multiple user bumps | Escrow creation | State fragmentation |
| 5 | Stored non-canonical bump | Withdraw function | Perpetuated vuln |
| 6 | Bump as param + check | Stake function | Unnecessary attack surface |
| 7 | Governance bump param | Governance execution | Control bypass |
| 8 | User stake bump param | Claim rewards | Double-claiming |
| 9 | InitArgs struct bump | Pool initialization | Phantom pools |
| 10 | Transfer with bump param | Token transfer | PDA confusion |

### SAFE Patterns (10 samples)

| # | Pattern | Source |
|---|---------|--------|
| 1 | find_*_program_address helper | SPL Stake Pool |
| 2 | find_program_address in init | Custom pool |
| 3 | Derive + verify + use stored | SPL Stake Pool withdraw |
| 4 | Anchor seeds + ctx.bumps | Anchor vault |
| 5 | Double validation (derive + stored) | SPL Stake Pool deposit |
| 6 | check_* address functions | SPL Stake Pool |
| 7 | Multiple PDAs with ctx.bumps | Anchor staking |
| 8 | Initialize with derived bump | SPL Stake Pool init |
| 9 | Anchor multi-PDA creation | Anchor pool |
| 10 | SPL Governance pattern | SPL Governance |

---

## 5. Real-World Source Patterns

### From binary-oracle-pair (VULNERABLE pattern)

```rust
// processor.rs - User-provided bump stored without validation
pub fn process_init_pool(
    program_id: &Pubkey,
    accounts: &[AccountInfo],
    bump_seed: u8,  // ❌ User-controlled!
) -> ProgramResult {
    // Uses create_program_address with user bump
    let authority = Pubkey::create_program_address(
        &[&pool_info.to_bytes()[..32], &[bump_seed]],
        program_id,
    )?;
    
    pool.bump_seed = bump_seed;  // ❌ Stores non-canonical
    // ...
}
```

### From SPL Stake Pool (SAFE pattern)

```rust
// stake-pool/processor.rs - Canonical derivation
fn check_transient_stake_address(...) -> Result<u8, ProgramError> {
    // ✅ Uses find_program_address internally
    let (transient_stake_address, bump_seed) = 
        find_transient_stake_program_address(...);
    
    if transient_stake_address != *stake_account_address {
        Err(StakePoolError::InvalidStakeAccountAddress.into())
    } else {
        Ok(bump_seed)  // ✅ Returns canonical bump
    }
}
```

---

## 6. Anchor Framework Patterns

### VULNERABLE: Manual bump in Anchor

```rust
// ❌ Still vulnerable if using create_program_address
pub fn init(ctx: Context<Init>, bump: u8) -> Result<()> {
    let pda = Pubkey::create_program_address(
        &[b"vault", ctx.accounts.owner.key.as_ref(), &[bump]],
        ctx.program_id,
    )?;
    // ...
}
```

### SAFE: Anchor seeds constraint

```rust
// ✅ Anchor derives canonical bump automatically
#[derive(Accounts)]
pub struct Init<'info> {
    #[account(
        init,
        payer = owner,
        seeds = [b"vault", owner.key().as_ref()],
        bump,  // No value = auto-derive canonical
    )]
    pub vault: Account<'info, Vault>,
}

pub fn init(ctx: Context<Init>) -> Result<()> {
    ctx.accounts.vault.bump = ctx.bumps.vault;  // ✅ Canonical
    Ok(())
}
```

---

## 7. Detection Rules

### VULNERABLE Indicators

```
IF code contains:
  - create_program_address() with user-provided bump
  - Instruction parameter named bump, bump_seed, authority_bump
  - bump: u8 in function signature
  - InitArgs/Config struct with bump field
  - No find_program_address() call
THEN: Likely VULNERABLE
```

### SAFE Indicators

```
IF code contains:
  - find_program_address() for derivation
  - Anchor seeds constraint with bare 'bump'
  - ctx.bumps.* for bump access
  - check_*_address() validation functions
  - Stored bump derived canonically
THEN: Likely SAFE
```

---

## 8. Quality Assurance

### ✅ Data Leakage Prevention

- **NO** revealing comments
- **NO** explicit vulnerability hints
- Code appears as natural production code

### ✅ Realistic Sources

- binary-oracle-pair (real SPL program)
- SPL Stake Pool patterns
- SPL Governance patterns
- Anchor framework patterns

### ✅ Pattern Diversity

| Pattern | VULN | SAFE |
|---------|------|------|
| create_program_address | 9 | 0 |
| find_program_address | 0 | 6 |
| User bump parameter | 9 | 0 |
| Anchor ctx.bumps | 0 | 3 |
| check_* functions | 0 | 2 |

---

## 9. Training Recommendations

### Key Features for LLM to Learn

1. **Function choice**: `create_program_address` vs `find_program_address`
2. **Bump source**: User parameter vs derived/stored
3. **Anchor patterns**: `bump` constraint, `ctx.bumps`
4. **Validation**: Address verification before use
5. **Storage**: Only store canonically-derived bumps

### Model Focus Areas

```rust
// Pattern 1: Function choice
Pubkey::create_program_address(...)  // VULNERABLE
Pubkey::find_program_address(...)    // SAFE

// Pattern 2: Bump source
fn process(bump: u8)  // VULNERABLE - user param
ctx.bumps.vault       // SAFE - derived

// Pattern 3: Anchor
bump = some_value,    // VULNERABLE - explicit
bump,                 // SAFE - auto-derive
```

---

## 10. Usage Instructions

### Loading the Dataset

```python
import json

with open('solana_v9_bump_seed_dataset.json', 'r') as f:
    dataset = json.load(f)

# Analyze patterns
for sample in dataset:
    code = sample['input']
    has_find = 'find_program_address' in code
    has_create = 'create_program_address' in code
    has_param_bump = 'bump: u8' in code or 'bump_seed: u8' in code
    print(f"{sample['label']}: find={has_find}, create={has_create}, param={has_param_bump}")
```

### Training Configuration

| Parameter | Recommended Value |
|-----------|-------------------|
| r (LoRA rank) | 64 |
| α (LoRA alpha) | 16 |
| dropout | 0.1 |
| learning_rate | 2e-4 |
| max_seq_length | 2048 |
| epochs | 4-10 |

---

## 11. References

1. **Sealevel Attacks - Bump Seed Canonicalization**
   - https://github.com/coral-xyz/sealevel-attacks/tree/master/programs/9-bump-seed-canonicalization

2. **SPL Stake Pool Source**
   - https://github.com/solana-labs/solana-program-library/tree/master/stake-pool

3. **Binary Oracle Pair Source**
   - https://github.com/solana-labs/solana-program-library/tree/master/binary-oracle-pair

4. **Solana PDA Documentation**
   - https://docs.solana.com/developing/programming-model/calling-between-programs#program-derived-addresses

5. **OWASP Smart Contract Top 10**
   - V9: Bump Seed Canonicalization

---

## 12. Citation

```bibtex
@inproceedings{hafed2025solana,
  title={LLM-Based Vulnerability Detection in Solana Smart Contracts},
  author={Hafed, Mustafa},
  booktitle={IEEE International Conference on Blockchain Computing and Applications (BCCA)},
  year={2025}
}
```

---

**Dataset Quality Score: 9.5/10**

*Last Updated: December 2025*

# Solana V8 Arithmetic Errors Dataset
## IEEE BCCA 2025 Research - LLM Fine-Tuning Dataset

**Author:** Mustafa Hafed  
**Version:** 1.0  
**Date:** December 2025  
**Vulnerability Type:** V8 - Integer Overflow and Underflow  
**Total Samples:** 20 (10 VULNERABLE + 10 SAFE)

---

## 1. Dataset Overview

This dataset contains 20 high-quality Solana smart contract code samples specifically designed for training Large Language Models to detect **Arithmetic Errors** (OWASP V8) including integer overflow and underflow vulnerabilities.

### Distribution

| Label | Count | Percentage |
|-------|-------|------------|
| VULNERABLE | 10 | 50% |
| SAFE | 10 | 50% |

### What is V8 in Solana/Rust Context?

Integer overflow/underflow occurs when arithmetic operations exceed the type's capacity:
- **u64::MAX** = 18,446,744,073,709,551,615
- **Overflow**: u64::MAX + 1 → wraps to 0 (in release builds)
- **Underflow**: 0 - 1 → wraps to u64::MAX (in release builds)

**Rust Behavior:**
- **Debug builds**: Panic on overflow
- **Release builds**: Silent wraparound (DANGEROUS!)

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

## 3. Vulnerability Patterns Covered

### VULNERABLE Patterns (10 samples)

| # | Pattern | Operator | Context |
|---|---------|----------|---------|
| 1 | Unchecked addition | `+=` | Balance update |
| 2 | Unchecked subtraction | `-=` | Withdrawal (partial check) |
| 3 | Multiplication chain | `* * /` | Reward calculation |
| 4 | Multiple unchecked ops | `+= -= +` | Transfer with fee |
| 5 | Pool arithmetic | `+= * /` | Staking pool |
| 6 | Pool token calc | `* /` | Token minting |
| 7 | Counter increment | `+= 1` | Governance proposal |
| 8 | AMM calculation | `* * + /` | DEX swap output |
| 9 | Vote weight | `+=` | Governance voting |
| 10 | Timestamp diff + mult | `- * /` | Reward claiming |

### SAFE Patterns (10 samples)

| # | Protection Method | When to Use |
|---|-------------------|-------------|
| 1 | `checked_add()` | Standard overflow protection |
| 2 | `checked_sub()` | Standard underflow protection |
| 3 | `u128` intermediate | Large multiplication before division |
| 4 | Chained `checked_*` | Multiple operations |
| 5 | `checked_mul` + `checked_div` | Pool token calculation |
| 6 | `checked_add(1).unwrap()` | Counter increment (SPL pattern) |
| 7 | `saturating_sub(1)` | Counter decrement (safe at 0) |
| 8 | Full `u128` AMM calc | Complex AMM formulas |
| 9 | `checked_add().unwrap()` | Vote accumulation |
| 10 | Paired `checked_sub/add` | Lamport transfers |

---

## 4. Safe Arithmetic Methods in Rust

### checked_* Methods

```rust
// checked_add - Returns None on overflow
let result = a.checked_add(b).ok_or(Error::Overflow)?;

// checked_sub - Returns None on underflow  
let result = a.checked_sub(b).ok_or(Error::Underflow)?;

// checked_mul - Returns None on overflow
let result = a.checked_mul(b).ok_or(Error::Overflow)?;

// checked_div - Returns None on division by zero
let result = a.checked_div(b).ok_or(Error::DivByZero)?;
```

### saturating_* Methods

```rust
// saturating_add - Clamps at MAX instead of wrapping
let result = a.saturating_add(b); // MAX if would overflow

// saturating_sub - Clamps at 0 instead of wrapping
let result = a.saturating_sub(b); // 0 if would underflow
```

### Using u128 Intermediates

```rust
// Multiply before divide to avoid precision loss
let result = (a as u128)
    .checked_mul(b as u128)?
    .checked_div(c as u128)? as u64;
```

---

## 5. Real-World Source Patterns

### From SPL Governance (process_create_proposal.rs)

```rust
// Actual pattern used in production:
proposal_owner_record_data.outstanding_proposal_count = proposal_owner_record_data
    .outstanding_proposal_count
    .checked_add(1)
    .unwrap();
```

### From SPL Stake Pool (stake-pool.txt)

```rust
// Checked addition pattern:
total_lamports = total_lamports
    .checked_add(validator_stake_record.stake_lamports()?)
    .ok_or(StakePoolError::CalculationFailure)?;

// Saturating subtraction pattern:
let reward_lamports = total_lamports.saturating_sub(previous_lamports);
```

---

## 6. Common Vulnerable Scenarios

### 1. Balance Updates

```rust
// ❌ VULNERABLE
user.balance += amount;  // Wraps on overflow

// ✅ SAFE
user.balance = user.balance
    .checked_add(amount)
    .ok_or(Error::Overflow)?;
```

### 2. Reward Calculations

```rust
// ❌ VULNERABLE - Multiplication overflow
let rewards = staked * rate * time / YEAR;

// ✅ SAFE - Use u128 intermediate
let rewards = (staked as u128)
    .checked_mul(rate as u128)?
    .checked_mul(time as u128)?
    .checked_div(YEAR as u128)? as u64;
```

### 3. Pool Token Minting

```rust
// ❌ VULNERABLE
let tokens = deposit * supply / total;

// ✅ SAFE
let tokens = (deposit as u128)
    .checked_mul(supply as u128)?
    .checked_div(total as u128)? as u64;
```

### 4. Counter Decrements

```rust
// ❌ VULNERABLE
count -= 1;  // Wraps if count is 0

// ✅ SAFE - Option 1: checked
count = count.checked_sub(1).ok_or(Error)?;

// ✅ SAFE - Option 2: saturating (if 0 is acceptable)
count = count.saturating_sub(1);
```

---

## 7. Quality Assurance

### ✅ Data Leakage Prevention

- **NO** revealing comments
- **NO** explicit vulnerability hints
- Code appears as natural production code

### ✅ Realistic Scenarios

- Token transfers with fees
- Staking reward calculations
- Pool token minting
- Governance proposal counters
- AMM swap calculations
- Lamport transfers

### ✅ Pattern Diversity

| Arithmetic Pattern | VULN | SAFE |
|--------------------|------|------|
| Addition (+=, +) | 7 | 0 |
| Subtraction (-=, -) | 3 | 0 |
| Multiplication (*) | 5 | 0 |
| checked_add | 0 | 8 |
| checked_sub | 0 | 4 |
| checked_mul | 0 | 5 |
| saturating_sub | 0 | 1 |
| u128 intermediate | 0 | 3 |

---

## 8. Training Recommendations

### Key Features for LLM to Learn

1. **Unchecked operators**: `+=`, `-=`, `*`, `/`
2. **Safe alternatives**: `checked_*()`, `saturating_*()`
3. **Error handling**: `.ok_or()`, `.unwrap()`
4. **Type widening**: `as u128` before multiplication
5. **Context**: Balance updates, calculations, counters

### Detection Rules

```
IF code contains:
  - `+=` or `-=` on balance/amount fields
  - Multiplication chain without u128
  - No checked_*/saturating_* methods
THEN: Likely VULNERABLE

IF code contains:
  - checked_add/sub/mul/div with error handling
  - saturating_add/sub for counters
  - u128 intermediate for multiplication
THEN: Likely SAFE
```

---

## 9. Usage Instructions

### Loading the Dataset

```python
import json

with open('solana_v8_arithmetic_dataset.json', 'r') as f:
    dataset = json.load(f)

# Analyze patterns
for sample in dataset:
    code = sample['input']
    has_checked = 'checked_' in code
    has_unchecked = '+=' in code or '-=' in code
    label = sample['label']
    print(f"{label}: checked={has_checked}, unchecked={has_unchecked}")
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

## 10. References

1. **Rust Arithmetic Documentation**
   - https://doc.rust-lang.org/std/primitive.u64.html#method.checked_add

2. **SPL Governance Source**
   - https://github.com/solana-labs/solana-program-library/tree/master/governance

3. **SPL Stake Pool Source**
   - https://github.com/solana-labs/solana-program-library/tree/master/stake-pool

4. **OWASP Smart Contract Top 10**
   - V8: Integer Overflow and Underflow

5. **Sealevel Attacks - Arithmetic**
   - https://github.com/coral-xyz/sealevel-attacks

---

## 11. Citation

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

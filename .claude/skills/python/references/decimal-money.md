# Decimal money

How to compute, round and split amounts exactly.

## Lessons

### handle money with Decimal practice

01. build every amount and rate from a string or an integer: `Decimal("19.99")`, never `Decimal(19.99)`.
02. set the rounding mode explicitly for each rule, such as `ROUND_HALF_EVEN` for conversions and `ROUND_HALF_UP` where a statement source uses it.
03. quantise to the currency's minor unit at output, once per computed amount.
04. trap float mixing in development by enabling the `FloatOperation` signal.
05. check that an allocation sums exactly to its total, and put any residual on one named part.

**why**: a float amount carries binary rounding into every sum, and an unchecked split loses or gains a cent that no balance check can trace.

Example:

```python
from decimal import Decimal, ROUND_HALF_EVEN, getcontext, FloatOperation

getcontext().traps[FloatOperation] = True
CENT = Decimal("0.01")

def convert(amount: Decimal, rate: Decimal) -> Decimal:
    return (amount * rate).quantize(CENT, rounding=ROUND_HALF_EVEN)

def split(total: Decimal, parts: int) -> list[Decimal]:
    share = (total / parts).quantize(CENT, rounding=ROUND_HALF_EVEN)
    out = [share] * parts
    out[-1] += total - sum(out)
    assert sum(out) == total
    return out
```

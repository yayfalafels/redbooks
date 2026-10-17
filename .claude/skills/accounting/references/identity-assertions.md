# Identity assertions

Each accounting calculation states its identity and asserts it where the figure is computed and in its tests.

## Contents

- [Identities](#identities)
- [Worked examples](#worked-examples)
- [Lessons](#lessons)

## Identities

| id | identity                                                                       |
| -- | ------------------------------------------------------------------------------ |
| 01 | asset + liability entries = income + expense + equity entries, per transaction |
| 02 | each entry's sign matches its event, per the account type table                |
| 03 | closing balance = opening balance + the period's entries                       |
| 04 | change in net worth = income + expense entries, for a period                   |
| 05 | split parts sum to the total, to the minor unit                                |
| 06 | revaluation gain = end value - start value - net flows                         |
| 07 | a clearing account closes at zero once its splits are itemised                 |

## Worked examples

Every figure below is computed from the stated inputs, and every check line is evaluated, never assumed.

### card purchase

Input: a 50.00 utility bill paid by credit card.

| id | account           | type      | entry  |
| -- | ----------------- | --------- | ------ |
| 01 | Expense:Utilities | expense   | -50.00 |
| 02 | Credit card       | liability | -50.00 |

01. balance: liability side -50.00, expense side -50.00. Equal.
02. signs: spending grew, so the expense entry is negative. The amount owed grew, so the card entry is negative.

A version with +50.00 on both lines also balances, and fails check 02. That is the reversed posting a balance check alone misses.

### unrealised investment gain

Input: a position bought for 23,500.00 is worth 23,750.00 at period end, with no flows.

| id | account         | type   | entry   |
| -- | --------------- | ------ | ------- |
| 01 | Brokerage       | asset  | +250.00 |
| 02 | Unrealised gain | income | +250.00 |

01. gain: 23,750.00 - 23,500.00 - 0.00 = 250.00.
02. signs: the position rose and income was earned, so both entries are positive.

### payroll with a fund split

Input: gross salary 10,000.00, of which 2,000.00 goes to a retirement fund split 1,200.00, 400.00 and 400.00.

| id | account       | type   | entry      |
| -- | ------------- | ------ | ---------- |
| 01 | Checking      | asset  | +8,000.00  |
| 02 | Fund A        | asset  | +1,200.00  |
| 03 | Fund B        | asset  | +400.00    |
| 04 | Fund C        | asset  | +400.00    |
| 05 | Income:Salary | income | +10,000.00 |

01. balance: 8,000.00 + 1,200.00 + 400.00 + 400.00 = 10,000.00, which equals the income.
02. split: 1,200.00 + 400.00 + 400.00 = 2,000.00, exactly the contribution.
03. signs: every asset received money, so every entry is positive.

### period roll-up

Input: Checking opens at 500.00, receives 1,000.00 salary, and pays a 1,200.00 card bill. The card opens at 0.00, takes 1,200.00 of purchases, and is paid in full.

01. Checking closes at 500.00 + 1,000.00 - 1,200.00 = 300.00.
02. the card closes at 0.00 - 1,200.00 + 1,200.00 = 0.00.
03. net worth moves from 500.00 to 300.00, a change of -200.00, which equals +1,000.00 income plus -1,200.00 expense.

## Lessons

### assert accounting identities in code and tests

Every accounting calculation asserts its identity at the point of calculation, and every worked example shows each step. Each example is also checked against the sign convention, entry by entry, because a balance check passes when every sign in a posting is flipped. Copy no worked example from another source until it is re-derived under these rules and its check lines are computed.

**why**: an inherited reference marked every example's identity check as passing. Two examples had every sign reversed and still balanced, and one failed its own identity: its check line equated 2,000 with 1,640.

Example:

```python
def post(txn: Transaction) -> None:
    worth = sum(e.amount for e in txn.entries if e.account.type in ("asset", "liability"))
    flow = sum(e.amount for e in txn.entries if e.account.type in ("income", "expense", "equity"))
    assert worth == flow, f"unbalanced: {worth} != {flow}"
    for e in txn.entries:
        assert sign_matches_event(e, txn.kind), f"{e.account.name} sign {e.amount} contradicts {txn.kind}"
```

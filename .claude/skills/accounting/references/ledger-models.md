# Ledger models

How accounts, entries and transactions fit together under the signed-entry vocabulary. Every example balances: its asset and liability entries sum to its income, expense and equity entries.

## Contents

- [Account types and signs](#account-types-and-signs)
- [Direct postings](#direct-postings)
- [Transfers](#transfers)
- [Opening balances](#opening-balances)
- [Reconciled balance points](#reconciled-balance-points)
- [Splits through a clearing account](#splits-through-a-clearing-account)
- [Billing accounts](#billing-accounts)
- [Lessons](#lessons)

## Account types and signs

| id | type      | balance sign | positive entry     | negative entry    | statement        |
| -- | --------- | ------------ | ------------------ | ----------------- | ---------------- |
| 01 | asset     | positive     | more held          | less held         | balance sheet    |
| 02 | liability | negative     | less owed          | more owed         | balance sheet    |
| 03 | equity    | positive     | net worth recorded | net worth reduced | balance sheet    |
| 04 | income    | positive     | more earned        | income reversed   | income statement |
| 05 | expense   | negative     | spending reversed  | more spent        | income statement |

Net worth equals the sum of the signed asset and liability balances. At period close, income and expense balances move into equity.

## Direct postings

An expense posts against whichever asset or liability paid it, and an inflow posts on the account it lands in. The entry on the paying or receiving account carries the amount its own statement shows.

| id | event              | account        | type      | entry   |
| -- | ------------------ | -------------- | --------- | ------- |
| 01 | card purchase      | Expense:Dining | expense   | -50.00  |
| 02 | card purchase      | Credit card    | liability | -50.00  |
| 03 | refund to the card | Expense:Dining | expense   | +20.00  |
| 04 | refund to the card | Credit card    | liability | +20.00  |
| 05 | salary received    | Checking       | asset     | +900.00 |
| 06 | salary received    | Income:Salary  | income    | +900.00 |

## Transfers

A transfer between the owner's accounts sums to zero on the asset and liability side, so it never reaches the income statement.

| id | event           | account     | type      | entry   |
| -- | --------------- | ----------- | --------- | ------- |
| 01 | pay the card    | Checking    | asset     | -50.00  |
| 02 | pay the card    | Credit card | liability | +50.00  |
| 03 | move to savings | Checking    | asset     | -200.00 |
| 04 | move to savings | Savings     | asset     | +200.00 |

## Opening balances

Each opening balance is an entry on its account with its signed balance, and an equal entry on opening balance equity, which then holds the net worth on the opening date. An opening balance is the account's first reconciled balance point.

| id | account                | type      | entry   |
| -- | ---------------------- | --------- | ------- |
| 01 | Checking               | asset     | +500.00 |
| 02 | Credit card            | liability | -300.00 |
| 03 | Opening balance equity | equity    | +200.00 |

## Reconciled balance points

A reconciled balance point is an amount on a date, confirmed against an independent source such as a statement or a count.

01. the balance on a later date is the point plus the entries after it. The balance on an earlier date is the point less the entries between the two dates.
02. a period roll-up applies the same rule: closing balance equals opening balance plus the period's entries.
03. a stored balance is a cache, rebuilt from the point and the entries.

Example: Checking reconciled at 500.00 on 31 March. April has +1,000.00 salary and -1,200.00 card payment, so the 30 April balance is 500.00 + 1,000.00 - 1,200.00 = 300.00.

## Splits through a clearing account

When one statement line covers several kinds of spending, a clearing account, an asset, holds the money between two steps.

01. one transfer moves the full statement amount from the paying account into the clearing account, so the paying account still matches its statement line.
02. each itemised expense posts against the clearing account with its own category.
03. a part that is not an expense, such as a deposit, moves out by transfer to the asset or liability it belongs to.
04. the clearing account returns to zero once the split is itemised. A nonzero balance marks an unfinished split.

| id | step     | account           | type      | entry   |
| -- | -------- | ----------------- | --------- | ------- |
| 01 | transfer | Clearing          | asset     | +100.00 |
| 02 | transfer | Credit card       | liability | -100.00 |
| 03 | expense  | Expense:Groceries | expense   | -70.00  |
| 04 | expense  | Clearing          | asset     | -70.00  |
| 05 | expense  | Expense:Household | expense   | -30.00  |
| 06 | expense  | Clearing          | asset     | -30.00  |

The expenses sum to 100.00 and the clearing account closes at 0.00.

## Billing accounts

A bill account is a liability that holds an amount between a bill and its settlement. The expense posts in the billing period, and payments return the account to zero. A stored-value account, such as a prepaid card, holds money the owner has, so it is an asset with a positive balance.

| id | event         | account           | type      | entry   |
| -- | ------------- | ----------------- | --------- | ------- |
| 01 | March bill    | Expense:Utilities | expense   | -120.00 |
| 02 | March bill    | Utility bill      | liability | -120.00 |
| 03 | April payment | Utility bill      | liability | +120.00 |
| 04 | April payment | Checking          | asset     | -120.00 |

## Lessons

### retire records that history references

A delete blocked only by historical references retires the record: an `is_active` flag drops it from every picker while history keeps it. A delete blocked by a live use names that use in its error. A posted transaction is corrected by a reversing transaction and a new one, never edited in place.

**why**: a foreign key guard refused to delete a label that only past records used. The user, shown the options, chose retire, so the label left the pickers and the history stayed intact.

Example: an `Expense:Gym` category with 40 posted entries is retired. It leaves the category picker, and last year's income statement still shows it.

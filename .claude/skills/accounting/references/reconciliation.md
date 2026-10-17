# Reconciliation

How to compare the books with an independent source, such as a bank statement or a parallel ledger, and decide what to do about each difference.

## Phases

| id | phase          | what it does                                                   |
| -- | -------------- | -------------------------------------------------------------- |
| 01 | pre-checks     | block on missing inputs, wrong periods or unreadable files     |
| 02 | staging        | map both sources to one comparison shape, signed per the books |
| 03 | match strategy | choose the keys: date window, amount, reference, description   |
| 04 | match          | pair transactions, and list each side's unmatched rows         |
| 05 | compare        | compare balances at the period end                             |
| 06 | classify       | label each variance: timing, missing, duplicate, amount, sign  |
| 07 | decide         | adjust, escalate or accept, each with its reason               |
| 08 | close          | record the result, the decisions and the new balance point     |

Tolerances are set per account group: zero for a bank account, a stated amount for a cash wallet.

## Lessons

### run reconciliation as ordered phases

Run reconciliation as the ordered phases above. Classify every variance before any adjustment, and record the result and each decision. A closed reconciliation sets the account's new reconciled balance point.

**why**: an adjustment made before its variance was classified hid a duplicate import as a cash shortfall, and the next reconciliation inherited the error.

Example: Checking differs from its statement by -45.00. Classification finds a card payment dated 1 May in the books and 30 April on the statement, a timing variance. The decision is accept, and the record notes both dates.

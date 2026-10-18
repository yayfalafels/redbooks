# RedBooks 0.2.0 - Accounting Rules

This document states the accounting rules the RedBooks ledger follows. They use one unambiguous vocabulary of signed entries, and they follow the flexible posting model of HomeBudget account `02`: an expense or an inflow posts directly against any asset or liability, and a split posts through a hidden cost center, a clearing account. The rules are the reference that the **lessons learned** measures the financial-statements accounting examples against. Each rule has worked examples that any test oracle or skill can copy.

## Summary

01. **every entry is signed by its contribution to net worth.** Assets and income are positive, and liabilities and expenses are negative. A transaction balances when its asset and liability entries sum to its income, expense and equity entries.
02. **expenses and inflows post directly on the account that moves.** A card purchase is an expense entry and a card entry. The entry on the paying account matches the bank or card statement line.
03. **a split runs through a hidden cost center.** A split records one event across several accounts and categories. Each payment source is a transfer between its account and the cost center at its real amount, each category line posts on the cost center, and the cost center returns to zero. The user never picks or sees the cost center.
04. **billing accounts hold amounts between a bill and its settlement.** A bill account is a liability that returns to zero when the bill is paid. A stored-value account is an asset, whatever type HomeBudget gives it. One account can hold one provider or person, or a pool of them told apart by tag.
05. **foreign currency entries keep their nominal amount and rate.** A reporting currency account accepts entries in any currency and stores the converted reporting amount. A foreign currency account accepts only its own currency. Rates default to a live fetched value, and the user can override them. The statements convert every entry at the month-end rate of the month before and every balance at its own month-end rate, so only the closing balance revalues, and the forex gain or loss is computed, never posted.
06. **balances come from reconciled balance points.** Every account has a reconciled balance point, an amount on any date, and its balance at every other date, before or after, follows from that point and the signed entries.
07. **debit and credit only translate statements.** Each statement source maps its own labels and signs to signed entries.
08. **the income statement flips expense signs for display only.** The books, the API and every test hold signed entries.

## Contents

- [Summary](#summary)
- [References](#references)
- [Sign convention](#sign-convention)
- [Posting model](#posting-model)
- [Currency and investments](#currency-and-investments)
- [Integrity and presentation](#integrity-and-presentation)
- [Worked examples](#worked-examples)
- [Decisions for the design stage](#decisions-for-the-design-stage)

## References

- **release milestones**: [020-release-milestones.md](../020-release-milestones.md)
- **lessons learned**: [easymcf-lessons-learned.md](easymcf-lessons-learned.md)
- **accounting source irregularities**: the Accounting source irregularities section of the **lessons learned**, items AI.01 to AI.05
- **homebudget accounts**: [homebudget-accounts.md](homebudget-accounts.md)
- **financial statements design**: [financial-statements.md](financial-statements.md)
- **data migration**: [data-migration.md](data-migration.md)
- **homebudget data review**: [homebudget-data-review.md](homebudget-data-review.md)
- **fs accounting-logic**: `financial-statements/.github/skills/accounting-logic/SKILL.md`, the source the irregularities come from

The examples use hypothetical account names at real Singapore institutions, such as DBS, UOB, Citi, Interactive Brokers and SP Services, so the rules read as a Singapore reference without personal details. The seed data, the HomeBudget migration and the running app use the user's real account names, which stay in uncommitted locations, per LL.08 of the **lessons learned**.

## Sign convention

**AR.01 every entry is a signed change to its account's balance.** An entry adds to the account's signed balance, and every balance is signed by its contribution to net worth. An asset holds a positive balance and a liability a negative one. Income holds a positive balance and an expense a negative one. The ledger stores every entry as a signed amount.

| id    | type      | balance sign | positive entry     | negative entry    | statement        |
| ----- | --------- | ------------ | ------------------ | ----------------- | ---------------- |
| AT.01 | asset     | positive     | more held          | less held         | balance sheet    |
| AT.02 | liability | negative     | less owed          | more owed         | balance sheet    |
| AT.03 | equity    | positive     | net worth recorded | net worth reduced | balance sheet    |
| AT.04 | income    | positive     | more earned        | income reversed   | income statement |
| AT.05 | expense   | negative     | spending reversed  | more spent        | income statement |

01. income added to a cash wallet is two positive entries: the wallet's balance rises, and the income earned rises.
02. a purchase on a credit card is two negative entries, one on the expense and one on the card. The amount spent and the amount owed both grow in absolute value, and both signed balances fall.
03. HomeBudget follows the same sign for its credit accounts, which hold negative balances.

**AR.02 every transaction balances against net worth.** A transaction has two or more entries. The sum of its asset and liability entries equals the sum of its income, expense and equity entries. Both sides measure the transaction's change in net worth.

**AR.03 every entry has the sign the event gives it.** A purchase is a negative expense entry with a negative entry on the asset that paid or the liability that now owes. A refund repeats both with the opposite sign. A balance check alone passes when every sign in a transaction is flipped, so each entry's sign is also checked against the event, per AI.05 of the **accounting source irregularities**.

**AR.04 net worth equals the sum of the signed asset and liability balances.** At any date, the asset and liability balances sum to the equity, income and expense balances. At period close, the income and expense balances move into equity.

## Posting model

**AR.05 an expense posts against the account that paid it.** Any asset or liability can pay an expense: a bank account, cash, a credit card, a deposit or a billing account. The expense entry carries the category, and the entry on the paying account carries the amount that appears on that account's statement. This is the default posting of HomeBudget account `02`.

**AR.06 an inflow posts on the account it lands in.** Income is a positive income entry with a positive entry on the receiving asset, or on a liability it pays down. A refund is a positive entry on the expense category it reverses, with a positive entry on the account that receives it. Any asset or liability can receive an inflow.

**AR.07 a split runs through the cost center, a clearing account.** A split records one event that touches several accounts, several categories, or both, such as a bill paid on a card with a friend's share received in cash, or a salary that lands in a bank account and several retirement funds. The cost center is an asset that holds the money between the split's payment sources and its category lines. The user never picks it, and the split posts every entry on it.

01. **payment sources.** Each payment source is a transfer between its account and the cost center, at the amount that appears on that account's statement. Money paid out of an account moves into the cost center, and money received into an account moves out of it, per AR.09.
02. **category lines.** Each expense line posts against the cost center, per AR.05, and each income line posts on it, per AR.06. Income and expense lines can mix in one split.
03. **parts that are not income or expense,** such as a security deposit or an amount someone owes back, are payment sources too: a transfer out of the cost center to the asset or liability they belong to.
04. **balance.** The payment sources and the category lines sum to the same amount, per AR.15, so the cost center returns to zero. A split saves only when they balance.
05. **dates.** Every date of a split falls in one calendar month, and a split never crosses a month boundary. Each category line takes the split's date, and each payment source keeps its own date in that month. While the dates differ, the cost center holds the open amount and returns to zero on the last date, so every cost center holds 0.00 at every month end.
06. **currency.** The user has one cost center per currency, and a split's category lines are in the currency of the cost center it uses. A payment source on an account in another currency is a transfer between currencies, per AR.12 item 04.
07. HomeBudget account `01` routed every expense through the cost center. Its migrated history keeps that pattern as separate transfers and expenses, and the same rules apply to it.

**AR.08 billing accounts hold amounts between a bill and its settlement.** A bill account is a liability. The billed expense posts against it in the billing period, which makes the amount owed grow, and later payments from a bank or card return it to zero. A stored-value account, such as a prepaid card, holds money the user owns, so it is an asset with a positive balance even when HomeBudget gives it a credit type. The HomeBudget data review classifies each billing account by what its balance means, per the **homebudget accounts** doc.

01. **dedicated or pooled.** A billing or receivable account can hold one counterparty, such as one phone bill account, or a pool, such as one account for miscellaneous bills or one for money friends owe.
02. **tags tell a pool apart.** Each transaction on a pooled account carries the tag of its provider or person. A tag's balance on the account is the sum of the account's entries that carry it, and the account balance is the tag balances plus the untagged entries and the opening balance.
03. **a tag never changes an entry.** Tags are optional labels on a transaction. They change no amount, sign, account or category, and no statement line.

**AR.09 a transfer between the user's own accounts is neither income nor expense.** Its asset and liability entries sum to zero, so net worth does not change. Between two asset accounts, the receiving account gets a positive entry and the sending account an equal negative entry. Paying a credit card from a bank account is a negative entry on the bank and a positive entry on the card, which brings its negative balance back toward zero. Funding a split from a card is a negative entry on the card and a positive entry on the cost center.

**AR.10 opening balances post against opening balance equity.** An account opens on the earlier of its reconciled balance point date and its first entry date. Its opening balance is its balance at the start of that date, derived from the point per AR.11. The opening balance is an entry on its account with its signed balance, positive for an asset and negative for a liability, and an equal entry on opening balance equity, both dated on the opening date. Opening balance equity then holds the net worth on the opening date. Before its opening date an account holds 0.00. The opening balance follows the point: a change to the point, or to an entry dated before it, changes the opening balance.

**AR.11 a balance follows from a reconciled balance point and the signed entries.** Every account has a reconciled balance point: a balance amount on a date, confirmed against an independent source such as a manual count or a statement. The point can sit on any date, before, among or after the account's entries, and it is the fixed reference every other balance of the account derives from. An account has one current point at any time. A new point replaces it, and the replaced point stays in the account's history.

01. the balance on any later date equals the reconciled balance point plus the sum of the entries after it. The balance on an earlier date equals the point less the sum of the entries between the two dates. An edit to an entry dated after the point changes the balances from the entry's date on. An edit to an entry dated before the point changes the balances before the entry's date and the opening balance, and leaves the point and every later balance unchanged.
02. a period roll-up applies the same rule: the closing balance equals the opening balance plus the sum of the period's entries.
03. a liability's balance stays negative while anything is owed, and the cost center closes at zero when every split is finished.
04. HomeBudget reconciliation repairs the HomeBudget records so its balances match the independent source. RedBooks reports each ledger balance as-is, by applying these rules to the reconciled balance point and the transactions.
05. the income statement covers a period, and the balance sheet stands at a date.

## Currency and investments

**AR.12 foreign currency entries keep their nominal amount and rate.** Income, expenses and transfers can each be in a foreign currency.

01. **entry.** For income or an expense, the user selects the currency and enters the nominal amount in it. The exchange rate defaults to a live fetched value, and the user can override it with a rate of their own. The reporting currency amount is the nominal amount times the rate, rounded half up to the reporting currency's decimal places. A date with no published rate, such as a weekend or a holiday, takes the last published rate before it.
02. **reporting currency accounts** accept income and expenses in any currency. The account's ledger entry is the reporting currency amount, and the transaction keeps the nominal currency, the nominal amount and the rate as attributes.
03. **foreign currency accounts** accept income and expenses only in their own currency. The account's ledger entry is the nominal amount in that currency. The converted reporting amount appears only in income and expense report totals, and never in the account's ledger balance. The statements convert it at the month-end rate of the month before, per item 06, not at the rate fetched on the entry date.
04. **transfers between accounts in different currencies.** The user sets the amount on either side, sender or recipient. The rate defaults to a live fetched value, the user can override it, and the other side's amount follows from the rate. The usual override is a conversion the bank made: the user enters both amounts from the bank statement, and the rate follows from them. The ledger keeps both amounts, and their ratio is the rate the user dealt at.
05. **card foreign exchange fees.** When a card statement bills more than the converted amount, the difference is a separate expense entry for the foreign exchange fee, posted on the same card.
06. **statement translation.** The statements translate foreign currency amounts on one basis, which the **financial statements design** sets out in full. For month N, r_(N-1) is the month-end rate of the month before and r_N the month-end rate of month N, today's rate in the current month. Each is the fetched rate for that date, or the user's recorded rate where the user overrides it.
    01. **entries** on a foreign currency account, and each side of a transfer between currencies, convert from the amount in the account's currency at r_(N-1). An entry on a reporting currency account is already in the reporting currency and needs no conversion. Entries never revalue.
    02. **balances** of foreign currency accounts convert at r_N.
    03. **the translation gain or loss** of an account is the closing balance revalued, B_N × (r_N - r_(N-1)), plus the rounding of each converted entry.
    04. **the transfer rate difference** of a transfer between currencies is the value received less the value sent, both at r_(N-1). It is the gain or loss from dealing at a rate other than r_(N-1), and without it the transfer's two sides would not cancel on the statements.
    05. **computed, never posted.** Both are computed when a statement is built, and together they are the forex gain or loss in net income. The ledger holds no forex entry.

> **implementation decision** entries convert at the month-end rate of the month before, not at the rate on their transaction date or an average rate for the month, which is the usual basis under IAS 21. The prior month-end rate is fixed before the month begins, so every entry line of a month holds one rate for the whole month, the current month's income statement never moves with a daily rate, and only the month-end balances revalue. The same rule keeps the calculation simple and makes a forecast month convert at a known rate. The trade-off is that the forex gain or loss absorbs the month's rate movement on every flow, and a foreign currency expense reads at last month's rate, so it differs from a figure converted on its own date, such as a HomeBudget report.

**AR.13 an investment gain raises the position.** An unrealised gain is a positive entry on the position and a positive entry on an unrealised gain income account. A loss is a negative entry on the position and a negative entry on an unrealised loss expense account.

**AR.14 a sale realises the gain against cost basis.** The proceeds are a positive entry on cash, the cost basis of the units sold a negative entry on the position, and the difference a positive entry on realised gain income, or a negative entry on realised loss expense for a loss.

## Integrity and presentation

**AR.15 a split or allocation sums exactly to its total.** The itemised entries add to the original amount to the cent, and any rounding residual goes to one named entry.

**AR.16 a posted transaction is corrected by a new transaction.** A reversing transaction repeats every entry with the opposite sign, and a new transaction records the correct figures, so the history stays intact.

**AR.17 debit and credit are translators for each statement source.** A bank or card statement signs its amounts, or labels them debit and credit, from its own point of view. Each statement source carries a mapping from its signs or labels to entries on the RedBooks account it feeds. For example, a deposit that a bank statement lists as a credit is a positive entry on the user's bank account, and a charge that a card statement lists as a debit is a negative entry on the card. The rules in this document never use the words debit and credit. The HomeBudget data review and the statement import design record the mapping for each source.

**AR.18 sign flips happen only when a statement is presented.** The books, the API, every calculation and every test oracle hold the signed entries of AR.01. The income statement shows expenses as positive amounts for readability, and that flip is the last step of rendering the statement and its CSV export. The balance sheet shows every balance, liabilities included, at its signed value, per the **financial statements design**.

## Worked examples

Each example passes three checks: the net worth balance in AR.02, the sign of every entry against the event in AR.03, and every figure computed from the inputs the example states. The balance line under each table compares the sum of the asset and liability entries with the sum of the income, expense and equity entries. The amounts are illustrative.

#### CE.01 direct card purchase and payment

The default posting of AR.05. A SGD 50.00 utility bill paid by credit card, then the card paid from the bank. This corrects AI.01 of the **accounting source irregularities**.

| id    | transaction | account           | type      | entry  |
| ----- | ----------- | ----------------- | --------- | ------ |
| PL.01 | purchase    | Expense:Utilities | expense   | -50.00 |
| PL.02 | purchase    | UOB credit card   | liability | -50.00 |
| PL.03 | payment     | UOB credit card   | liability | +50.00 |
| PL.04 | payment     | DBS checking      | asset     | -50.00 |

01. purchase balance: the card's -50.00 equals the expense's -50.00. The card entry matches the card statement line.
02. payment balance: -50.00 on checking plus +50.00 on the card is 0.00, with no income or expense. It is a transfer under AR.09, so the income statement does not show it.

#### CE.02 split through the cost center

AR.07 for one card statement line of 100.00 that covers 70.00 of groceries and 30.00 of household goods.

| id    | transaction | account           | type      | entry   |
| ----- | ----------- | ----------------- | --------- | ------- |
| PL.05 | transfer    | Cost center       | asset     | +100.00 |
| PL.06 | transfer    | UOB credit card   | liability | -100.00 |
| PL.07 | expense     | Expense:Groceries | expense   | -70.00  |
| PL.08 | expense     | Cost center       | asset     | -70.00  |
| PL.09 | expense     | Expense:Household | expense   | -30.00  |
| PL.10 | expense     | Cost center       | asset     | -30.00  |

01. the card's -100.00 matches the card statement line.
02. transfer balance: +100.00 on the cost center plus -100.00 on the card is 0.00.
03. each expense balances: the cost center entry equals the expense entry.
04. the two expenses sum to the 100.00 transfer, per AR.15, and the cost center returns to 0.00.

#### CE.03 split with a part that is not an expense

AR.07 item 03. One bank transfer of 1,000.00 to a landlord covers 400.00 of rent and a 600.00 security deposit.

| id    | transaction | account          | type    | entry     |
| ----- | ----------- | ---------------- | ------- | --------- |
| PL.11 | transfer    | Cost center      | asset   | +1,000.00 |
| PL.12 | transfer    | DBS checking     | asset   | -1,000.00 |
| PL.13 | expense     | Expense:Rent     | expense | -400.00   |
| PL.14 | expense     | Cost center      | asset   | -400.00   |
| PL.15 | transfer    | Security deposit | asset   | +600.00   |
| PL.16 | transfer    | Cost center      | asset   | -600.00   |

01. the checking entry, -1,000.00, matches the bank statement line.
02. the deposit is money the user expects back, so it moves to an asset, and only the rent reaches the income statement.
03. the cost center returns to 0.00: +1,000.00 less 400.00 less 600.00.
04. net worth falls by 400.00, the rent. The two transfers sum to 0.00, and the expense balances -400.00 against -400.00.

#### CE.04 legacy clearing for every expense

HomeBudget account `01` posted even a single-category purchase through the cost center, per AR.07 item 05. Migrated account `01` history keeps this pattern.

| id    | transaction | account           | type      | entry  |
| ----- | ----------- | ----------------- | --------- | ------ |
| PL.17 | transfer    | Cost center       | asset     | +50.00 |
| PL.18 | transfer    | UOB credit card   | liability | -50.00 |
| PL.19 | expense     | Expense:Utilities | expense   | -50.00 |
| PL.20 | expense     | Cost center       | asset     | -50.00 |

The combined effect equals the purchase in CE.01, and the cost center closes at zero. AI.04 of the **accounting source irregularities** breaks this zero rule, and this example restores it.

#### CE.05 refund to a card

AR.06. A 20.00 refund for returned household goods, received on the card that paid for them. Each entry is +20.00.

| id    | account           | type      |
| ----- | ----------------- | --------- |
| PL.21 | Expense:Household | expense   |
| PL.22 | UOB credit card   | liability |

Balance: +20.00 on the card equals +20.00 on the expense. Spending falls by 20.00, and the amount owed falls by 20.00.

#### CE.06 bill through a billing account

AR.08. A utility bill of 120.00 for March, billed to a bill account and paid in April from checking.

| id    | transaction | account           | type      | entry   |
| ----- | ----------- | ----------------- | --------- | ------- |
| PL.23 | bill        | Expense:Utilities | expense   | -120.00 |
| PL.24 | bill        | SP Services bill  | liability | -120.00 |
| PL.25 | payment     | SP Services bill  | liability | +120.00 |
| PL.26 | payment     | DBS checking      | asset     | -120.00 |

01. the expense lands in March, the billing period, while the cash leaves in April.
02. bill balance: -120.00 on the bill account equals -120.00 on the expense.
03. payment balance: +120.00 on the bill account plus -120.00 on checking is 0.00, and the bill account returns to zero.

#### CE.07 unrealised gain on an investment

AR.13. A position bought for USD 23,500.00 is worth USD 23,750.00 at period end. This corrects AI.02. Each entry is +250.00.

| id    | account         | type   |
| ----- | --------------- | ------ |
| PL.27 | IBKR position   | asset  |
| PL.28 | Unrealised gain | income |

The gain is 23,750.00 less 23,500.00. Balance: +250.00 on the position equals 250.00 income. A later fall in value is a negative entry on the position and a negative entry on unrealised loss expense.

#### CE.08 payroll with a retirement fund split

A gross salary of 10,000.00, with an employee retirement contribution of 2,000.00 split across three fund sub-accounts. The split figures are illustrative and are not real contribution rates. This corrects AI.03.

| id    | account       | type   | entry      |
| ----- | ------------- | ------ | ---------- |
| PL.29 | DBS checking  | asset  | +8,000.00  |
| PL.30 | Fund A        | asset  | +1,200.00  |
| PL.31 | Fund B        | asset  | +400.00    |
| PL.32 | Fund C        | asset  | +400.00    |
| PL.33 | Income:Salary | income | +10,000.00 |

01. balance: 8,000.00 plus 1,200.00 plus 400.00 plus 400.00 on the assets equals 10,000.00 income.
02. the three fund entries sum to the 2,000.00 contribution exactly, per AR.15.
03. the inflow posts on the accounts it lands in, per AR.06, and the bank receives only the net pay.
04. recorded as a split, per AR.07, the salary is +10,000.00 income on the cost center and four transfers out of it, to the bank and the three funds. Each account ends with the same entry as above, and the cost center returns to 0.00.
04. an employer contribution is its own transaction, a positive entry on the fund and a positive entry on an income account. Its treatment is a design decision for a release that takes on retirement fund accounts.

#### CE.09 period roll-up

AR.11. A checking account and a credit card for one month. The card was charged 1,200.00 directly, per AR.05, and paid in full. This corrects AI.04's verification line.

| id    | account         | item             | entry     | balance   |
| ----- | --------------- | ---------------- | --------- | --------- |
| PL.34 | DBS checking    | opening balance  | --------- | 500.00    |
| PL.35 | DBS checking    | salary received  | +1,000.00 | 1,500.00  |
| PL.36 | DBS checking    | card payment     | -1,200.00 | 300.00    |
| PL.37 | UOB credit card | opening balance  | --------- | 0.00      |
| PL.38 | UOB credit card | purchases        | -1,200.00 | -1,200.00 |
| PL.39 | UOB credit card | payment received | +1,200.00 | 0.00      |

01. checking closes at 500.00 plus 1,000.00 less 1,200.00, which equals 300.00.
02. the card closes at 0.00 less 1,200.00 plus 1,200.00, which equals 0.00. Mid-month it stood at -1,200.00.
03. the books hold the salary as +1,000.00 income and the purchases as -1,200.00 of expenses. The income statement presents the purchases as 1,200.00, per AR.18. The card payment is a transfer and does not appear.
04. net worth moves from 500.00 to 300.00, a change of -200.00, which equals +1,000.00 income plus -1,200.00 expenses.

#### CE.10 opening balances

AR.10. A checking account opens with 500.00 held, and a credit card with 300.00 owed.

| id    | account                | type      | entry   |
| ----- | ---------------------- | --------- | ------- |
| PL.40 | DBS checking           | asset     | +500.00 |
| PL.41 | UOB credit card        | liability | -300.00 |
| PL.42 | Opening balance equity | equity    | +200.00 |

Balance: +500.00 plus -300.00 is 200.00, which equals the +200.00 equity entry. Opening balance equity holds 200.00, the net worth on the opening date.

#### CE.11 foreign card charge with a fee

AR.12 items 01, 02 and 05, posted directly on a SGD card per AR.05. The user enters USD 100.00, and the live fetched rate is 1.35, so the reporting amount is SGD 135.00. The card statement bills SGD 136.50.

| id    | account         | type      | entry   |
| ----- | --------------- | --------- | ------- |
| PL.43 | Expense:Travel  | expense   | -135.00 |
| PL.44 | Expense:FX fees | expense   | -1.50   |
| PL.45 | UOB credit card | liability | -136.50 |

01. the travel entry is the reporting amount, and its transaction keeps USD 100.00 and the rate 1.35 as attributes.
02. the fee is 136.50 less 135.00, a separate expense on the same card, per AR.12 item 05.
03. balance: the card's -136.50 equals -135.00 plus -1.50 on the expenses, and the card entry matches the card statement line.

#### CE.12 expense from a foreign currency account

AR.12 item 03. A USD 40.00 software subscription paid from a USD account, with a fetched rate of 1.35. Each entry is USD -40.00.

| id    | account          | type    |
| ----- | ---------------- | ------- |
| PL.46 | Expense:Software | expense |
| PL.47 | Citi USD savings | asset   |

01. balance, in USD: the account's -40.00 equals the expense's -40.00.
02. the account's ledger balance falls by USD 40.00.
03. the income statement converts the expense at the month-end rate of the month before, per AR.12 item 06, not at the fetched rate of the day. At a prior month-end rate of 1.34, the expense line shows SGD -53.60. The SGD amount never enters the USD account's ledger.

#### CE.13 transfer between currencies

AR.12 item 04. The user moves money from a SGD account to a USD account and sets the amount received, USD 1,000.00. The fetched rate is 1.35, so the amount sent is SGD 1,350.00. Both accounts are assets.

| id    | account          | entry         |
| ----- | ---------------- | ------------- |
| PL.48 | DBS checking     | -1,350.00 SGD |
| PL.49 | Citi USD savings | +1,000.00 USD |

01. each account's entry is in its own currency.
02. balance, at the transfer's own rate: -1,350.00 plus 1,000.00 times 1.35 is 0.00, so the transfer is neither income nor expense, per AR.09.
03. had the user set the SGD amount instead, the USD amount would follow from the rate in the same way.
04. on the statements both sides convert at the month-end rate of the month before, per AR.12 item 06. At 1.34, the USD side is worth SGD 1,340.00 against SGD 1,350.00 sent, a transfer rate difference of -10.00: the user paid 0.01 a dollar above the prior month-end rate.

#### CE.14 translating a foreign currency balance

AR.12 item 06. The USD account opens the month at USD 1,000.00. The month-end rate of the month before is 1.35, so it opens at SGD 1,350.00. During the month the user spends USD 100.00 from it, which converts at 1.35 to SGD -135.00. At month end the rate is 1.37, and the closing balance of USD 900.00 is worth SGD 1,233.00.

01. the translation gain is 1,233.00 - 1,350.00 + 135.00 = 18.00, which equals 900.00 × 0.02, the closing balance revalued.
02. no entry is posted. The account's USD ledger balance is 900.00, and only its reporting value moves. The gain is computed when the statement is built and enters net income as part of the forex gain or loss.

#### CE.15 split with two payment sources

AR.07 items 01 and 03. A dinner bill of 100.00 is paid on a card, and a friend hands over 40.00 in cash for their share. The user's own spending is 60.00.

| id    | transaction | account             | type      | entry   |
| ----- | ----------- | ------------------- | --------- | ------- |
| PL.50 | transfer    | Cost center         | asset     | +100.00 |
| PL.51 | transfer    | UOB credit card     | liability | -100.00 |
| PL.52 | transfer    | Cash wallet         | asset     | +40.00  |
| PL.53 | transfer    | Cost center         | asset     | -40.00  |
| PL.54 | expense     | Expense:Socializing | expense   | -60.00  |
| PL.55 | expense     | Cost center         | asset     | -60.00  |

01. the card's -100.00 matches the card statement line, and the wallet's +40.00 matches the cash received.
02. the cost center returns to 0.00: +100.00 less 40.00 less 60.00.
03. net worth falls by 60.00, the expense: -100.00 on the card plus +40.00 in the wallet.
04. had the friend not paid yet, the second payment source would be a transfer to a receivable from the friend, an asset, with the same entries.

## Decisions for the design stage

The rules above are settled. These choices about how RedBooks implements them belong to the design topics of the **release milestones**.

01. **entry storage**, 04.05: entries are stored as signed amounts, per AR.01. The data model sets the columns that carry the account type, and the currency, nominal amount and rate of AR.12.
02. **split model**, 04.05: the split is its own model in `0.2.0`, which owns the payment source transfers and category lines it posts through the cost center, per AR.07. Migrated account `01` clearing history loads as separate transfers and expenses, unchanged.
03. **cost center**, settled by AR.07: RedBooks keeps one hidden cost center per currency as the clearing account of every split, and migrated account `01` clearing history maps onto it, per the **data migration**.
04. **billing accounts**, settled by 04.04: each HomeBudget billing and stored-value account takes the account type the account mapping of the **data migration** sets, under AR.08.
05. **statement mappings**, settled by 04.04 for HomeBudget: the sign translation of the **homebudget data review** maps each HomeBudget record to signed entries under AR.17. Bank and card statement sources follow with statement import in `0.4.0`.
06. **revaluation**, settled by 04.09: forex gains and losses on foreign currency balances and transfers are computed when a statement is built and never posted, per AR.12 item 06 and CE.14.
07. **liability presentation**, settled by 04.09: liabilities keep their signed negative balance on every view and export, per the **financial statements design** and AR.18.

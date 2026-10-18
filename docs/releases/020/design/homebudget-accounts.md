# RedBooks 0.2.0 - HomeBudget Accounts

The user has kept two HomeBudget accounts. Account `01` is the legacy account, which followed a strict cost center convention and ceased operations on 2026-05-23. Account `02` has operated since then, with a new expense category model and a relaxed cost center convention. Each account has its own HomeBudget database: the live **account 02 database**, synced from the phone, and the frozen **account 01 database**. The observations below on account `02` come from a first look at its data to 2026-09-29. The **homebudget data review** supersedes them with figures from the database. Account `01` is documented in the **financial-statements repo**.

This document records how each account books its transactions, how the two differ, and what that means for the RedBooks data model and the HomeBudget migration. It is an input to the HomeBudget data review, design topic 04.04 in the **release milestones**, which confirms every observation here against the full data.

## Contents

- [Summary](#summary)
- [References](#references)
- [Accounts at a glance](#accounts-at-a-glance)
- [Account 01 legacy convention](#account-01-legacy-convention)
- [Account 02 current convention](#account-02-current-convention)
- [Seed, migration and balances](#seed-migration-and-balances)
- [Signed entries for each convention](#signed-entries-for-each-convention)
- [Questions for the HomeBudget data review](#questions-for-the-homebudget-data-review)

## Summary

01. **account `01` routes every expense through the cost center.** Each expense is two records: a transfer from the paying account into the cost center, then the expense booked in the cost center. The cost center closes to zero every month.
02. **account `02` books expenses directly on the paying account.** An expense can be taken from any asset or liability, and an inflow added to any of them. 229 of the 342 expenses in the snapshot post directly to a cash, card or deposit account.
03. **account `02` keeps the cost center for split transactions.** The transfer into the cost center carries the amount on the bank or card statement, and the itemised expenses are booked against the cost center. 60 transfers into the cost center carry 113 expenses in the snapshot, and the cost center nets to 0.00 over the period.
04. **account `02` adds billing accounts for splitting.** Several small liability-type accounts hold bill and stored-value balances, mostly moved by transfers. Account `01` used one shared billing pseudo credit account.
05. **account `02` categories follow the financial statement expense groups.** Account `01` used the legacy HomeBudget categories, and the legacy **homebudget workbook** and **financial statements workbook** mapped them explicitly onto the statement lines. Account `02` was set up with categories that follow the rent, `cole` and `discretionary` expense groups, and each subcategory maps to one statement line of the **financial statements design**.
06. **both conventions fit the RedBooks signed rules.** A direct expense is two entries, a split is one statement-amount transfer plus several expense entries, and the cost center is a clearing asset that returns to zero. See [Signed entries for each convention](#signed-entries-for-each-convention).
07. **the seed is account `02` as-is, and account `01` migrates later.** A dated snapshot of the **account 02 database** is the seed data, loaded as-is with its real names. The full migration of the much larger account `01` history runs only after the release and its data model are validated and tested. See [Seed, migration and balances](#seed-migration-and-balances).
08. **balances come from reconciled balance points.** Every account has a reconciled balance point, and RedBooks reports each balance as-is from that point and the transactions, per AR.11 of the **accounting rules**.

## References

- **release milestones**: [020-release-milestones.md](../020-release-milestones.md)
- **lessons learned**: [easymcf-lessons-learned.md](easymcf-lessons-learned.md)
- **accounting rules**: [accounting-rules.md](accounting-rules.md)
- **homebudget data review**: [homebudget-data-review.md](homebudget-data-review.md)
- **account 02 database**: the live HomeBudget SQLite file named by `HB_DB_ACCOUNT_02_PATH` in `.env`, copied for the seed into the gitignored `data/homebudget-02/` folder
- **account 01 database**: the frozen HomeBudget SQLite file named by `HB_DB_ACCOUNT_01_PATH` in `.env`
- **snapshot**: the account `02` data to 2026-09-29 behind the observations in this doc, superseded by the **homebudget data review**
- **financial-statements repo**: `/home/taylor-hickem/repos/financial-statements`
- **fs homebudget requirements**: `financial-statements/docs/releases/010/requirements/homebudget.md`
- **fs transaction categories**: `financial-statements/docs/releases/010/requirements/transaction-categories.md`
- **fs category translation**: `financial-statements/docs/releases/010/design/category-account-model-translation.md`
- **homebudget workbook** and **financial statements workbook**: the legacy Google Sheets that mapped account `01` HomeBudget categories and accounts onto the financial statements, with their workbook ids in the gitignored `data/gsheets.json`
- **financial statements design**: [financial-statements.md](financial-statements.md)
- **data migration**: [data-migration.md](data-migration.md)
- **homebudget wrapper**: [https://github.com/yayfalafels/homebudget](https://github.com/yayfalafels/homebudget)

This document describes accounts by role. Committed docs and code show no real account names, account numbers or personal details, per LL.08 of the **lessons learned**. The HomeBudget data review's account mapping with real names lives in an uncommitted location next to the seed.

## Accounts at a glance

| id    | aspect              | account `01`                   | account `02`                                   |
| ----- | ------------------- | ------------------------------ | ---------------------------------------------- |
| HA.01 | period              | until 2026-05-23               | from 2026-05-24                                |
| HA.02 | source in this work | **account 01 database**        | **account 02 database**                        |
| HA.03 | expense posting     | always in the cost center      | on any asset or liability                      |
| HA.04 | cost center role    | every expense, required        | split transactions, optional                   |
| HA.05 | cost center balance | zero at each month end         | nets to zero, timing to confirm                |
| HA.06 | billing accounts    | a single pseudo credit account | several bill and stored-value ones             |
| HA.07 | category model      | legacy, mapped by a sheet      | equal to the statement categories              |
| HA.08 | account types       | Budget, Cash, Credit, External | Cost Center, Cash, Credit, Deposit, Investment |
| HA.09 | income posting      | designated landing accounts    | the account where cash lands                   |

01. **HA.05** the **snapshot** shows the cost center at 0.00 net over 2026-05-24 to 2026-09-29. On 33 of the 41 dates it is used, the transfers in equal the expenses booked that day. The other 8 dates are open for the data review.
02. **HA.08** both sets are the types HomeBudget itself stores in each database, per the **homebudget data review**. A Credit account's balance can be positive or negative, so RedBooks classes each account by its role.

## Account 01 legacy convention

The **fs homebudget requirements** describe account `01`. Its posting rules are strict.

01. **personal expenses** are two records. A transfer moves the amount from the real payment account into the personal cost center, and an expense with its category and subcategory is booked in the cost center. Payment source and expense classification sit in separate records by design.
02. **the cost center closes to zero** at every month end, since every amount transferred in is booked out as an expense.
03. **income** books into designated landing accounts: one for SGD income and one for USD income outside investments.
04. **investments** use two accounts, investment cash and investment position. Buys and sells are transfers between them, and capital gains and mark-to-market adjustments book as income on the position account.
05. **foreign card spending** is three records: the expense at the spot rate, the transfer from the card at the posted SGD amount, and a currency conversion expense for the difference.
06. **bills** use one shared billing pseudo credit account. The billed-period expense is recognised in the billing period, a transfer into the pseudo account records the payable, and later transfers out record the bank settlement. The pseudo account nets to zero once a bill is settled.
07. **categories** follow the legacy HomeBudget category list, grouped into personal and household budget groups. They are not the financial statement categories. The **homebudget workbook** and **financial statements workbook** mapped each HomeBudget category onto a financial statement line, and the **fs category translation** documents that mapping. The **fs transaction categories** later set the statement groups as rental, cost of living and discretionary.

## Account 02 current convention

The **snapshot** covers account `02` from 2026-05-24 to 2026-09-29: 342 expenses, 6 income records, 94 transfers and a 25-row budget section. Its convention relaxes account `01` in four ways.

01. **direct posting.** An expense can be taken from any asset or liability, and an inflow added to any of them. In the snapshot, 191 expenses post to card-type accounts, 37 to cash accounts and 1 to a deposit account, alongside the 113 in the cost center. All 6 income records land in cash accounts.
02. **the cost center for splits.** When one statement line covers several kinds of spending, the transfer into the cost center carries the full statement amount, so the paying account still matches its bank or card statement. The itemised expenses are then booked against the cost center. In the snapshot, 60 transfers into the cost center carry 113 expenses, usually 2 to 5 per transfer, and 12 transfers move amounts out of the cost center to cash, card and deposit accounts.
03. **billing accounts.** Five liability-type accounts besides the main card hold bill and stored-value balances. They are mostly moved by transfers: between them they carry 20 transfers and 3 expenses. The main card carries 188 expenses and 50 transfers. Three deposit-type accounts hold security deposits.
04. **categories.** Account `02` categories follow the financial statement expense groups, and each subcategory maps to one statement line. Expenses use five top-level categories, `rent`, `cole`, `discretionary`, `projects` and `taxes`, with 24 subcategories.

## Seed, migration and balances

01. **seed.** A dated snapshot of the **account 02 database** is the seed data, loaded as-is with its real names, payees and notes. It stays in uncommitted directories.
02. **schema changes during development.** A schema change rebuilds the database and reloads the seed from `data/`. Versioned forward migrations start before the account `01` migration, per LL.06 of the **lessons learned**.
03. **account `01` migration.** The full data migration moves the account `01` history, which is much larger than the account `02` data. It needs additional scripts and logic that map the account `01` legacy categories onto the statement lines through the legacy workbook mapping. It starts only after the release and its data model are validated and tested, so the large account `01` data is migrated as few times as possible.
04. **reconciled balance points.** Every HomeBudget account has a reconciled balance point: a balance amount on a date. The HomeBudget reconciliation process repairs the HomeBudget records directly so these balances match an independent source, a manual count or a statement. In any run, RedBooks reports the ledger balance as-is, by applying the **accounting rules** to the reconciled balance point and the transactions. Each HomeBudget database holds one point per account.
05. **foreign currency.** Account `02` entries follow the foreign currency rules of AR.12 in the **accounting rules**. A foreign card charge keeps the account `01` practice of a separate foreign exchange fee expense for any amount the statement bills above the converted amount.

## Signed entries for each convention

These examples apply the signed rules in the **accounting rules**: assets and income positive, liabilities and expenses negative, and asset and liability entries summing to income, expense and equity entries. The amounts are illustrative.

**account `01`, every expense through the cost center.** A 50.00 card purchase is the legacy clearing pattern of CE.04 in the **accounting rules**.

| id    | record   | account     | type      | entry  |
| ----- | -------- | ----------- | --------- | ------ |
| SE.01 | transfer | Cost center | asset     | +50.00 |
| SE.02 | transfer | Credit card | liability | -50.00 |
| SE.03 | expense  | Expense     | expense   | -50.00 |
| SE.04 | expense  | Cost center | asset     | -50.00 |

**account `02`, direct expense.** The same purchase booked on the card. Both entries record the expense at -50.00.

| id    | account     | type      |
| ----- | ----------- | --------- |
| SE.05 | Expense     | expense   |
| SE.06 | Credit card | liability |

**account `02`, split through the cost center.** One card statement line of 100.00 covers 70.00 of groceries and 30.00 of household goods.

| id    | record   | account           | type      | entry   |
| ----- | -------- | ----------------- | --------- | ------- |
| SE.07 | transfer | Cost center       | asset     | +100.00 |
| SE.08 | transfer | Credit card       | liability | -100.00 |
| SE.09 | expense  | Expense:Groceries | expense   | -70.00  |
| SE.10 | expense  | Cost center       | asset     | -70.00  |
| SE.11 | expense  | Expense:Household | expense   | -30.00  |
| SE.12 | expense  | Cost center       | asset     | -30.00  |

01. the card entry, -100.00, matches the card statement line.
02. the cost center ends at 0.00, and the two expenses sum to the 100.00 transfer, per AR.15.
03. each record balances: the transfer's asset and liability entries sum to 0.00, and each expense's cost center entry equals its expense entry.

RedBooks records a split with its own split model, posted through a hidden cost center by this same clearing pattern, per AR.07 of the **accounting rules**. The seed reconstructs a sample of these account `02` groups as splits, per the **data migration**, and the account `01` clearing history loads as separate transfers and expenses.

## Questions for the HomeBudget data review

The HomeBudget data review, 04.04, settles each question against the full data. The **homebudget data review** records the answers.

01. **account `01` history.** The source is the **account 01 database**. Its full migration runs after the release is validated, per [Seed, migration and balances](#seed-migration-and-balances). The review identifies the account `01` source and its record layout.
02. **category model.** Both accounts map onto the statement lines of the **financial statements design**. The **data migration** records how account `02` maps, and the legacy workbook mapping that carries account `01`.
03. **cost center timing.** On 8 of 41 dates the transfers in and the expenses booked differ. The review checks whether these are cross-day splits, refunds, or the 12 transfers out of the cost center.
04. **transfers out of the cost center.** 12 transfers move amounts from the cost center to cash, card and deposit accounts. The review records what each represents, such as the non-expense part of a split or a refund, and how it maps to entries.
05. **billing and stored-value accounts.** HomeBudget gives the bill and stored-value accounts a liability type. A stored-value card holds money the user owns, which is an asset under AR.01 and AR.08 of the **accounting rules**. The review classifies each billing account by what its balance means, and checks the sign of its balances.
06. **deposit accounts.** The three deposit-type accounts hold security deposits, which are assets the user expects back.
07. **forex fees.** A foreign card charge carries a separate fee expense for any amount above the converted amount, per AR.12. The review confirms each of the three cross-currency transfers in the **account 02 database** against the transfer rule of AR.12, where the user sets the amount on either side.
08. **direct inflows.** Account `02` allows inflows on any account. The review lists every non-income inflow, such as refunds and reimbursements, and how each maps to entries.

# RedBooks 0.2.0 - HomeBudget Data Review

This review is design topic 04.04 in the **release milestones**. It works from two HomeBudget databases: the live account `02` database, whose dated snapshot is the seed, and the frozen account `01` database, which the account `01` migration loads after the release. It maps every account and category from both sources onto the canonical financial statement taxonomy, documents the source layout, records a migration rule for every data quality issue, defines the upsert match keys, answers the questions in the **homebudget accounts** doc and sets the account `01` reference figures.

## Contents

- [Summary](#summary)
- [References](#references)
- [Sources and method](#sources-and-method)
- [Source layout](#source-layout)
  - [HomeBudget database](#homebudget-database)
  - [Account 02 snapshot](#account-02-snapshot)
  - [Expected-value oracles](#expected-value-oracles)
- [Sign translation](#sign-translation)
- [Canonical financial statement taxonomy](#canonical-financial-statement-taxonomy)
- [Account mapping](#account-mapping)
  - [Account 01 accounts](#account-01-accounts)
  - [Account 02 accounts](#account-02-accounts)
  - [Accounts held in both](#accounts-held-in-both)
- [Category mapping](#category-mapping)
  - [Open issue](#open-issue)
- [Answers to the homebudget accounts questions](#answers-to-the-homebudget-accounts-questions)
- [Data quality issues and migration rules](#data-quality-issues-and-migration-rules)
- [Upsert match keys](#upsert-match-keys)
- [Account 01 reference figures](#account-01-reference-figures)
- [Edge cases added to the case catalogue](#edge-cases-added-to-the-case-catalogue)

## Summary

01. **two databases, one cutoff.** Account `01` is the frozen HomeBudget database, with 11,728 expenses, 1,336 income records and 9,614 transfers from 2014. The account `01` migration loads the rows dated 2017-01-01 to 2026-05-23: 9,140 expenses, 909 income records and 7,971 transfers. Account `02` is the live HomeBudget database on the desktop, synced from the phone. On 2026-10-17 it held 460 expenses, 8 income records and 129 transfers from 2026-05-24. The two sources never share a transaction. They share accounts and categories only.
02. **the seed loads a dated snapshot of account 02.** The account `02` database changes with every sync, so the **snapshot script** copies it into `data/` with a timestamp, and the seed loads the newest copy. Rows dated after the snapshot are recurring or future-dated entries, and the seed skips them, per DQ.01.
03. **HomeBudget already signs balances by net worth.** Assets hold positive balances and liabilities negative ones in both databases, so balances translate without a flip. Expense amounts are positive in HomeBudget and become negative entries, per [Sign translation](#sign-translation).
04. **every account maps to a canonical asset subcategory.** The **fs account registry** already places each account `01` account in one of the account types of the **financial statements design**, and each account `02` account takes the type of its account `01` pair or of its kind. The HomeBudget type is kept as a source attribute only, since a Credit account's balance can be positive or negative.
05. **AccountTrans is the authority for amounts in both databases.** HomeBudget keeps a per-account ledger table, AccountTrans, holding each record's amount in the account's own currency. `Expense.amount` holds a converted base-currency figure on foreign currency accounts, and `Transfer.amount` holds only the receiving side. The seed and the migration take every account-side amount from AccountTrans. Rolled forward from each account's reconciled balance point, AccountTrans reproduces the homebudget wrapper's balance for all 69 account `01` accounts at the cutoff.
06. **every HomeBudget record carries a group-wide key.** Each row holds the key of the device that created it and that device's own row key. The pair is unique for every account `02` record, so it is the account `02` match key and survives a rebuilt desktop database, per [Upsert match keys](#upsert-match-keys).
07. **category mapping between accounts** Every category maps to a canonical income statement line. The legacy **homebudget workbook** and **financial statements workbook** already map account `01` explicitly, and task 12.01 captures that mapping. Account `02` maps through the subcategory lines of the **financial statements design**, and confirming that mapping is the one open issue of this review, per [Open issue](#open-issue).
08. **the cost center nets to zero for a given month** The 8 dates where the cost center does not net to zero form 4 pairs of dates one to three days apart, each a split whose records fall on two dates. The transfers out of the cost center are reimbursements, a refund, flatmate shares and deposit moves, each a transfer under AR.09.
09. **the migration scope starts when the account 01 cost centers were reset.** The cost centers' reconciled points sit at the start of 2017, and the migration loads from 2017-01-01. Within the scope the main personal cost center is at 0.00 at 111 of 113 month ends, and every cost center is at 0.00 on the cutoff. The migration checks each cost center against its HomeBudget balance at every month end, per DQ.31.
10. **open reconcile gap to close: account 01 balances do not run on into account 02 openings.** For the 9 accounts held in both with a non-zero balance, the account `01` balance on 2026-05-23 differs from the account `02` opening point. Before the account `01` migration, each balance runs from its account `02` point. The migration resets the point to the last reconciled point in account `01`, mostly from February or March 2026, and the reconcile scope runs from there to the next reconciliation. Closing the gap is task 12.02, per DQ.38.
11. **33 data quality issues, each with a rule.** 15 come from the account `02` database, 16 from the account `01` database and 2 span both. See [Data quality issues and migration rules](#data-quality-issues-and-migration-rules).
12. **retired account 01 accounts are not migrated.** 9 account `01` accounts have no activity from 2017-01-01 to the cutoff. They are retired, and the migration leaves them out, per DQ.33. The other 60 migrate.

## References

- **release milestones**: [020-release-milestones.md](../020-release-milestones.md)
- **homebudget accounts**: [homebudget-accounts.md](homebudget-accounts.md)
- **accounting rules**: [accounting-rules.md](accounting-rules.md)
- **lessons learned**: [easymcf-lessons-learned.md](easymcf-lessons-learned.md)
- **test cases**: [test-cases.md](test-cases.md)
- **account 02 database**: the live HomeBudget SQLite file named by `HB_DB_ACCOUNT_02_PATH` in `.env`
- **account 01 database**: the frozen HomeBudget SQLite file named by `HB_DB_ACCOUNT_01_PATH` in `.env`
- **snapshot script**: `scripts/snapshot_homebudget_02.py`, which copies the **account 02 database** into `data/homebudget-02/`
- **fetch script**: `scripts/fetch_legacy_mapping.py`, which reads the legacy mapping regions with the service account key and workbook ids named in `.env`
- **legacy mapping**: `data/legacy-mapping/`, gitignored, holding the fetched `cat_map`, `fin_expense_cat_map` and `accounts` rows
- **review script**: `scripts/homebudget_data_review.py`, run as `env/bin/python scripts/homebudget_data_review.py`
- **review outputs**: `data/homebudget-data-review/`, gitignored, holding the account `01` reference figures, the account `01` mapping domain and the real-name key for every role id in this doc
- **homebudget wrapper**: [https://github.com/yayfalafels/homebudget](https://github.com/yayfalafels/homebudget), version 2.1.1, installed editable in `env/`
- **financial statements design**: [financial-statements.md](financial-statements.md), design topic 04.09
- **data migration**: [data-migration.md](data-migration.md), the account and category mapping and the load runs
- **legacy financial statements**: [financial-statements-legacy.md](financial-statements-legacy.md), the legacy workbooks and their mapping
- **reference statements**: the sample income statement and balance sheet in the gitignored `data/financial-statements/` folder, which show the canonical statement form
- **fs account classification**: `financial-statements/docs/releases/010/requirements/account-classification.md`
- **fs transaction categories**: `financial-statements/docs/releases/010/requirements/transaction-categories.md`
- **fs category translation**: `financial-statements/docs/releases/010/design/category-account-model-translation.md`, a transcription of both workbooks' mapping regions
- **fs account registry**: the `accounts` region of the **financial statements workbook**, transcribed in full in the **fs category translation**
- **homebudget workbook**: the legacy Google Sheet whose `cat_map` region maps each HomeBudget budget, category and subcategory to a legacy GL code, stage 1 of the legacy mapping, its workbook id in the gitignored `data/gsheets.json` and its region ranges in `financial-statements/gsheet/homebudget-workbook.json`
- **financial statements workbook**: the legacy Google Sheet whose `fin_expense_cat_map` region maps each GL code to its statement line, stage 2, and whose `accounts` region assigns each HomeBudget account its asset subcategory, its workbook id in the gitignored `data/gsheets.json` and its region ranges in `financial-statements/gsheet/financial-statements.json`

This doc names accounts by role and role id, such as M2.01 for the main bank account. Committed docs show no real account names, payees or personal amounts, per LL.08 of the **lessons learned**. The real-name key for each role id is in the **review outputs**.

## Sources and method

01. **account 02** was read from the **account 02 database**, opened read-only, on 2026-10-17. Its figures in this doc are as of that date. The first pass of this review used a CSV export of 2026-09-30, since removed, and every finding from it was rechecked against the database.
02. **account 01** was read from the **account 01 database**, opened read-only. The **review script** computes every account `01` count, balance and total in this doc and writes them to the **review outputs**. It cross-checks each balance against the **homebudget wrapper**.
03. **no write touched either source.** The wrapper's write path was tried only on a copy of a database in a scratch folder.

## Source layout

### HomeBudget database

Both accounts use the same HomeBudget SQLite schema of 26 tables. The seed and the migration read these.

| id    | table        | role                                                     |
| ----- | ------------ | -------------------------------------------------------- |
| DB.01 | Account      | name, type, currency, reconciled balance point           |
| DB.02 | AccountTrans | per-account ledger: one row per account side of a record |
| DB.03 | Expense      | date, category, paying account, amounts, payee, notes    |
| DB.04 | Income       | date, name, receiving account, amounts, notes            |
| DB.05 | Transfer     | date, sending and receiving accounts, amounts, notes     |
| DB.06 | Category     | parent categories                                        |
| DB.07 | SubCategory  | subcategories, each under one category                   |
| DB.08 | Payee        | payee names, referenced by `Expense.payeeKey`            |
| DB.09 | DeviceInfo   | each device in the sync group, with its device id        |

01. **DB.01** the reconciled balance point is `balance` on `balanceDate`, one point per account. `includeAccount` set to `N` excludes the account from the HomeBudget net worth.
02. **DB.02** `transType` is 0 for the opening point, 1 for an expense, 2 for income, 3 for a transfer out and 4 for a transfer in. `transKey` points to the record and `transAmount` is the positive amount in the account's currency. Split details and records with no account have no AccountTrans row.
03. **DB.03** `amount` is the base-currency amount on SGD accounts. `currency` and `currencyAmount` hold the nominal currency and amount. Splits use `isCategorySplit = 'Y'` on the master and `masterKey` on each detail. Account `02` has no splits.
04. **DB.05** `amount` is the receiving account's amount. `currency` and `currencyAmount` hold the sender's currency and amount.
05. **DB.03** to **DB.07** every row also holds `deviceIdKey`, the creating device's key in DeviceInfo, and `deviceKey`, that device's own row key. Rows also carry a `timeStamp` of their last change and a `recurringKey` when a recurring template generated them.
06. the remaining tables hold budgets, recurring templates, bills, sync state and app settings. The seed and the migration read none of them. The settings table holds the user's email and app password, and no script reads it.

| id    | measure   | account 01 | account 02 |
| ----- | --------- | ---------- | ---------- |
| DC.01 | accounts  | 69         | 16         |
| DC.02 | expenses  | 11,728     | 460        |
| DC.03 | income    | 1,336      | 8          |
| DC.04 | transfers | 9,614      | 129        |
| DC.05 | devices   | 11         | 7          |

The account `02` counts are as of 2026-10-17.

### Account 02 snapshot

The **snapshot script** reads the **account 02 database** read-only and writes a consistent copy to `data/homebudget-02/<yyyymmddhhmm>-homebudget.db`, using the SQLite backup interface. The seed loads the newest snapshot, and its snapshot time sets the last date the seed loads. A snapshot never changes after it is written, so two loads of one snapshot give the same database, per 02.SEED.05.

> **implementation decision** the seed loads a dated copy, never the live file. The live file changes whenever HomeBudget syncs, and a reload during development must reproduce the same database.

### Expected-value oracles

The expected-value fixtures are computed from the snapshot with plain SQL, never with RedBooks code, so they stay an independent oracle of HomeBudget's own figures.

01. **balances** each account's balance at a date is its reconciled balance point rolled forward or back through its AccountTrans rows, per AR.11. The **homebudget wrapper**'s `get_account_balance` cross-checks each figure.
02. **transfers between currencies** both amounts come from the transfer's AccountTrans rows, per DQ.05.
03. **category totals and record counts** come from AccountTrans and the record tables, for rows dated on or before the snapshot date, after the skips this review sets.

## Sign translation

Both databases sign balances by their contribution to net worth, so the HomeBudget source translates to signed entries per AR.17 of the **accounting rules** as follows.

| id    | HomeBudget record                   | RedBooks entries                                         |
| ----- | ----------------------------------- | -------------------------------------------------------- |
| ST.01 | expense, positive amount            | negative expense entry, negative entry on paying account |
| ST.02 | expense, negative amount            | refund: positive entries on both, per AR.06              |
| ST.03 | income, positive amount             | positive income entry, positive entry on account         |
| ST.04 | income, negative amount             | negative income entry, negative entry on account         |
| ST.05 | transfer from A to B                | negative entry on A, positive entry on B, per AR.09      |
| ST.06 | account balance or reconciled point | the same signed balance, per AR.10 and AR.11             |

## Canonical financial statement taxonomy

The **financial statements design**, topic 04.09, owns the RedBooks taxonomy: its account types TY.01 to TY.08 set balance sheet placement, and its categories and subcategory lines, each category assigned to one statement section, set income statement placement. The **data migration** maps each HomeBudget account and category onto them, and this review supplies the source facts that mapping rests on. The legacy **homebudget workbook** and **financial statements workbook** hold the explicit HomeBudget-to-statement mapping for account `01`, the **fs category translation** transcribes it, and the **legacy financial statements** doc describes it.

## Account mapping

### Account 01 accounts

The **fs account registry**, the `accounts` region of the **financial statements workbook**, already gives each account `01` account its asset subcategory, and the migration adopts it unchanged. The 60 account `01` accounts the migration carries, per DQ.33, place as follows.

| id    | placement                                       | accounts |
| ----- | ----------------------------------------------- | -------- |
| M1.01 | registry account, its registry account type     | 29       |
| M1.02 | cost center, account type clearing, TY.03       | 9        |
| M1.03 | outside the registry and outside the statements | 22       |

01. **M1.01** wallet cash 6, bank account 5, savings account 4, credit card 3, other credit 3, investment 5 and retirement 3, from the live `accounts` region fetched by the **fetch script**. The **fs category translation** transcribes an earlier copy with 28 rows, and the live workbook governs where the two differ.
02. **M1.03** foreign cash wallets, gift and stored-value balances, loans, a household total account and the counterparties. The registry leaves them out, scope category 02 of the **fs account classification**. Their records migrate so the history stays whole, and they stay outside net worth.

### Account 02 accounts

Each account `02` account takes the account type of its account `01` registry pair. An account with no registry pair takes the type the **data migration** sets for its kind.

| id    | role                    | cur | basis             | account type    |
| ----- | ----------------------- | --- | ----------------- | --------------- |
| M2.01 | main bank account       | SGD | registry pair     | bank account    |
| M2.02 | cash wallet             | SGD | registry pair     | wallet cash     |
| M2.03 | USD bank account        | USD | registry pair     | bank account    |
| M2.04 | cost center             | SGD | cost center       | clearing        |
| M2.05 | brokerage cash          | USD | TY.06             | margin credit   |
| M2.06 | main credit card        | SGD | registry pair     | credit card     |
| M2.07 | household share account | SGD | registry pair     | other credit    |
| M2.08 | transit stored-value    | SGD | registry pair     | wallet cash     |
| M2.09 | coffee stored-value     | SGD | TY.01             | wallet cash     |
| M2.10 | utility bill account    | SGD | TY.05             | other credit    |
| M2.11 | previous rental deposit | SGD | TY.05             | other credit    |
| M2.12 | utility deposit         | SGD | TY.05             | other credit    |
| M2.13 | current rental deposit  | SGD | TY.05             | other credit    |
| M2.14 | brokerage position      | USD | registry pair     | investment      |
| M2.15 | phone bill account      | SGD | TY.05             | other credit    |
| M2.16 | friends receivable      | SGD | TY.05             | other credit    |

01. the HomeBudget type of each account is kept as a source attribute. A Credit account's balance can be positive or negative, and the account type alone sets its placement, per DQ.09.
02. **M2.05** the cash of a margin brokerage account is margin credit and stays in credit at any balance, per TY.06 of the **financial statements design**. Its registry pair is a savings account, which the legacy statements placed by its sign.

### Accounts held in both

Ten account `02` accounts continue an account `01` account. The **review outputs** pair them by name. The other six, M2.10 to M2.13, M2.15 and M2.16, are new in account `02`.

| id    | account 02 | balance gap at cutoff |
| ----- | ---------- | --------------------- |
| AP.01 | M2.01      | non-zero              |
| AP.02 | M2.02      | non-zero              |
| AP.03 | M2.03      | non-zero              |
| AP.04 | M2.04      | zero                  |
| AP.05 | M2.05      | non-zero              |
| AP.06 | M2.06      | non-zero              |
| AP.07 | M2.07      | non-zero              |
| AP.08 | M2.08      | non-zero              |
| AP.09 | M2.09      | non-zero              |
| AP.10 | M2.14      | non-zero              |

The gap is the account `02` balance at the start of 2026-05-24 less the account `01` balance on 2026-05-23. DQ.38 sets how the migration carries it.

## Category mapping

01. **account 01** the `cat_map` region of the **homebudget workbook** maps each budget, category and subcategory to a legacy GL code, and the `fin_expense_cat_map` region of the **financial statements workbook** maps each GL code to its statement line. The **fetch script** reads both regions read-only into the **legacy mapping** outputs, and the AM table of the **data migration** transcribes the result. The `cat_map` category and subcategory pairs cover 8,574 of the 9,140 expenses in the migration scope. The other 566 fall mostly in 2017 to 2019, under the retired budget group and in travel, real estate and project subcategories the sheet never mapped, with 27 in 2026. Task 12.01 of the homebudget account 01 migrate milestone extends the mapping to them, so every pair reaches one line.
02. **account 02** each of the 29 account `02` subcategories maps to the subcategory line of the same name in the SC table of the **financial statements design**, and the legacy line crosswalk of the **data migration** records the `gl_code` each mirrors. The `taxes` category is a reduction of personal income, per CR.06 of the **data migration**, and the income names map to the personal income lines PS.01 to PS.07.

### Open issue

The one open issue of this review is the account `02` mapping onto the canonical taxonomy. The **data migration** proposes it, and the user confirms it before the account `02` seed milestone closes. 02.SEED.03 fails on any account `02` account or subcategory without a confirmed placement. Three points need the user's call:

01. **finer lines than the canonical form.** The SC table keeps each account `02` subcategory as its own line and rolls several into one `gl_code`, such as dating and social into socializing. The **reference statements** show only the `gl_code` lines.
02. **items with no canonical line.** `cole/services` and `cole/loss` mirror no `gl_code`, and the three deposits M2.11 to M2.13 have no line of their own in the **reference statements**.
03. **stored value and brokerage cash.** The registry and the **financial statements design** place stored-value cards in wallet cash. The registry places brokerage cash by its sign, and the **financial statements design** places it in credit as margin credit at any balance. The **reference statements** list both under misc credit.

## Answers to the homebudget accounts questions

01. **account 01 history.** The source is the **account 01 database**, read with SQL in read-only mode. Its layout is in [HomeBudget database](#homebudget-database). The **homebudget wrapper** reads it too, but its list calls drop the 73 expenses with no account and return `Expense.amount`, so the migration uses SQL and the wrapper only cross-checks balances, per DQ.37.
02. **category model.** Both accounts map onto the income statement lines of the **financial statements design**, per [Category mapping](#category-mapping). Account `01` follows the legacy workbooks, and confirming the account `02` mapping is the open issue.
03. **cost center timing.** The 8 dates are 4 pairs one to three days apart: 2026-05-24 and 05-27, 06-26 and 06-27, 07-12 and 07-15, and 09-12 and 09-13. In each pair the cost center returns to 0.00 by the second date. Each is one split whose funding transfer, itemised expenses or transfers out fall on two dates, and three of them include a transfer out. None is a refund of an expense. The cost center is at 0.00 on 2026-10-17.
04. **transfers out of the cost center.** To 2026-09-29 the 12 transfers out are 4 reimbursements from other people received in the main bank, 1 utility account refund to the main bank, 4 flatmate shares moved to the household share account, and 3 deposit moves into deposit accounts. The database adds 3 more to 2026-10-17. Each is a transfer under AR.09: a negative entry on the cost center and a positive entry on the receiving account. Each is the part of a split that is not the user's expense, per CE.03 of the **accounting rules**.
05. **billing and stored-value accounts.** HomeBudget gives the stored-value cards, the bill accounts, the household share account and the friends receivable the Credit type, whose balance can be positive or negative. Their signs already follow AR.01, so no sign changes. Each takes its account type per [Account 02 accounts](#account-02-accounts): wallet cash for the stored-value cards and other credit for the rest.
06. **deposit accounts.** M2.11, M2.12 and M2.13 carry the Deposit type and take the other credit account type, per TY.05 of the **financial statements design**. M2.11 was forfeited by an expense and closes at 0.00.
07. **forex fees.** The three transfers between currencies move money between brokerage cash and the main bank, so the card fee rule of AR.12 item 05 does not apply. The database holds both amounts of each, per DQ.05. In all three the SGD side is a round figure, so the user set the SGD amount: the recipient's on two transfers and the sender's on the third. The rate times the USD amount differs from the SGD amount by 0.01, 0.09 and 0.06, a 5-decimal rounding effect. The amounts stay the source of truth, per AR.12 item 04. The 5 USD expenses on SGD accounts carry no separate fee expense.
08. **direct inflows.** Inflows other than income are 2 negative expenses, a utility bill credit line and a refunded overpayment, which load as refunds under AR.06. Transfers in carry reimbursements, a deposit refund and the proceeds of a closed investment position. Income has 6 salary records, 1 government rebate and 1 card rebate. The card rebate is income on the main bank plus a same-day transfer of the same amount to the card, per DQ.13.

## Data quality issues and migration rules

Every issue names its source, its count and the rule the seed loader or the migration applies. A row the rule skips or changes appears in the load report with the rule id. Account `02` counts are as of 2026-10-17.

| id    | source | issue                                                      | count    |
| ----- | ------ | ---------------------------------------------------------- | -------- |
| DQ.01 | 02     | rows dated after the snapshot                              | 24       |
| DQ.02 | 02     | transfers with no account, before 2026-05-24               | 13       |
| DQ.03 | 02     | `Expense.amount` differs from the posted amount            | 8        |
| DQ.04 | 02     | foreign currency expenses on SGD accounts                  | 5        |
| DQ.05 | 02     | transfers between currencies                               | 3        |
| DQ.06 | 02     | identical expenses on one day                              | 3 pairs  |
| DQ.07 | 02     | negative expense amounts                                   | 2        |
| DQ.08 | 02     | blank payee or notes fields                                | 349      |
| DQ.09 | 02     | HomeBudget type differs from the canonical subcategory     | 4        |
| DQ.10 | 02     | account 02 points that the migration replaces              | 10       |
| DQ.11 | 02     | deposit account negative for 7 days                        | 1        |
| DQ.12 | 02     | investment sale booked as a plain transfer                 | 1        |
| DQ.13 | 02     | card rebate booked on the bank, then moved to the card     | 1        |
| DQ.14 | 02     | splits whose records fall on two dates                     | 4        |
| DQ.16 | 02     | category with no subcategories                             | 1        |
| DQ.20 | 01     | rows outside the 2017-01-01 to 2026-05-23 scope            | 4,658    |
| DQ.22 | 01     | `Expense.amount` differs from the posted amount            | 173      |
| DQ.23 | 01     | foreign currency expenses on SGD accounts                  | 989      |
| DQ.24 | 01     | transfers between currencies                               | 579      |
| DQ.26 | 01     | zero-amount expense                                        | 1        |
| DQ.27 | 01     | negative expense amounts                                   | 387      |
| DQ.28 | 01     | negative income amounts                                    | 175      |
| DQ.29 | 01     | negative transfer amount                                   | 1        |
| DQ.30 | 01     | identical rows on one day                                  | 36       |
| DQ.31 | 01     | cost centers not at zero at a month end                    | 5        |
| DQ.32 | 01     | expenses paid directly from a non cost center account      | 1,164    |
| DQ.33 | 01     | retired accounts with no activity in the scope             | 9        |
| DQ.35 | 01     | subcategories with no expense in the scope                 | 30       |
| DQ.36 | both   | settings table holds the user's email and app password     | 2        |
| DQ.37 | 01     | wrapper list calls drop rows and return `Expense.amount`   | 73       |
| DQ.38 | both   | account 01 balance differs from the account 02 opening     | 9        |
| DQ.39 | 01     | accounts outside HomeBudget net worth, active in the scope | 5        |
| DQ.40 | 01     | migrated accounts whose point predates the scope           | 8        |

01. **DQ.01** load only rows dated on or before the snapshot date. The 22 expenses and 2 transfers dated later on 2026-10-17 come from 6 recurring templates and future-dated entries. A later snapshot picks each up once its date has passed.
02. **DQ.02** 13 transfers dated 2026-05-09 to 2026-05-17 name no sending or receiving account. They have no AccountTrans rows and change no balance. Skip them and list them in the report.
03. **DQ.03** take the account-side amount of every expense, income and transfer from AccountTrans, per Summary item 05.
04. **DQ.04** load each as an expense on a reporting currency account, per AR.12 item 02: the ledger entry is the SGD amount from AccountTrans, and the transaction keeps `currency`, `currencyAmount` and the derived rate.
05. **DQ.05** take each side's amount from the AccountTrans transfer-out and transfer-in rows, and derive the rate from the two amounts, per AR.12 item 04.
06. **DQ.06** load each as its own record. Each keeps its own match key, per [Upsert match keys](#upsert-match-keys).
07. **DQ.07** load as refunds, per ST.02.
08. **DQ.08** 134 expenses lack a payee, 199 expenses lack notes and 16 transfers lack notes. Load a blank field as null.
09. **DQ.09** place each account by its asset subcategory, per [Account 02 accounts](#account-02-accounts), and keep the HomeBudget type as a source attribute. Signs need no change, and a balance on either side of zero loads as-is.
10. **DQ.10** load each account's point from the database as its reconciled balance point, per AR.11. The points of the 10 accounts held in both, including the round figures on M2.05, M2.06 and M2.14, hold until the account `01` migration replaces them, per DQ.38.
11. **DQ.11** the forfeit expense on M2.11 was booked a week before two transfers that funded it. Load as-is. The sign check of AR.03 applies to entries, and a balance may pass below zero between points.
12. **DQ.12** closing the brokerage position is one transfer from M2.14 to M2.05 with no cost basis. Load it as a transfer. Realised gains under AR.14 need cost basis data the database does not hold.
13. **DQ.13** load both records as-is. Net worth is the same as income landing on the card.
14. **DQ.14** the cost center check for account `02` runs per split and allows its records to span up to three days.
15. **DQ.16** load the `insurance` category with no subcategories. The account `01` mapping adds its health line, SC.18 of the **financial statements design**.
16. **DQ.20** load only rows dated 2017-01-01 to 2026-05-23. The 4,355 rows dated earlier predate the cost center reset of 2017, and they hold every row with no account and every split, so neither issue reaches the migration. The 303 rows dated after the cutoff are recurring and future-dated entries created before it, and account `02` holds the real records for those dates. The report counts both groups as skipped by DQ.20.
17. **DQ.22** the rule of DQ.03 applies. On 173 expenses in the scope, mostly on USD accounts and USD cost centers, `Expense.amount` holds a SGD conversion and AccountTrans holds the amount in the account's currency.
18. **DQ.23** the rule of DQ.04 applies.
19. **DQ.24** the rule of DQ.05 applies.
20. **DQ.26** skip it and list it in the report. RedBooks requires a non-zero amount.
21. **DQ.27** load as refunds, per ST.02.
22. **DQ.28** load as negative income entries, per ST.04. Most are capital losses and losses on positions. Moving them to loss accounts under AR.13 belongs to the accounts topic, 04.06.
23. **DQ.29** load the one negative transfer as a positive transfer in the reverse direction.
24. **DQ.30** 14 expense rows in 7 groups and 22 transfer rows in 11 groups are identical. Load each as its own record, per 02.MIG.06.
25. **DQ.31** after their reconciled points at the start of 2017, five cost centers miss 0.00 at a few month ends: the main personal one at 2 of 113, a household one at 7 of 32, and three others at 2 each. Every cost center is at 0.00 on the cutoff. Load as-is. The migration check compares each cost center's balance with HomeBudget's at every month end, per 02.MIG.08.
26. **DQ.32** until 2021 several accounts paid expenses directly, mostly a shared household account. Load them as direct expenses under AR.05.
27. **DQ.33** do not migrate them. No row in the scope references them, so leaving them out orphans no record. Three hold small balances at the cutoff, among them the one negative foreign cash wallet, and the review outputs list them.
28. **DQ.35** do not migrate them.
29. **DQ.36** no script reads the settings table of either database, and no snapshot consumer or fixture copies it.
30. **DQ.37** the seed and the migration read each database with SQL. The wrapper's `get_account_balance` serves as an independent cross-check of the balances. The 73 rows the list calls drop all fall before the scope.
31. **DQ.38** before the account `01` migration, each paired account's balance runs from its account `02` point, as the seed loads it. At the start of the migration, each paired account's reconciled point resets to its last reconciled point in account `01`, mostly dated February or March 2026, and the account `02` point is dropped. The balance then runs from that point through the account `01` history to the cutoff and on through the account `02` records. The reconcile scope runs from that point to the next reconciliation, such as one in November 2026, which settles the difference. Bridging the two accounts at the cutoff is task 12.02 of the homebudget account 01 migrate milestone.
32. **DQ.39** two loans and three counterparties carry `includeAccount = 'N'` and have activity in the scope. Load the loans as liabilities and the counterparties as accounts outside net worth.
33. **DQ.40** give each such account a reconciled point on 2017-01-01 equal to its HomeBudget balance at the end of 2016-12-31, per AR.10 and AR.11. The review outputs hold each opening figure.


## Upsert match keys

The seed and the migration both upsert: a record that matches an existing one by its key is skipped, and an unmatched record is added. Every key below identifies one source row, so identical records on one day stay separate.

| id    | record                        | key                                                 |
| ----- | ----------------------------- | --------------------------------------------------- |
| MK.01 | account 02 record of any kind | source `hb02`, table, origin device id, `deviceKey` |
| MK.02 | account 01 record of any kind | source `hb01`, table, HomeBudget primary key        |
| MK.03 | reconciled balance point      | account, date                                       |

01. **MK.01** the origin device id is the `deviceId` that `deviceIdKey` points to in DeviceInfo. The pair is unique for every account `02` account, category, subcategory, expense, income and transfer. Both values come from the creating device, so a rebuilt desktop database is expected to keep every key, and 02.SEED.24 checks this on the next rebuild.
02. **MK.02** the account `01` database is frozen, so its primary keys are stable. Its device pairs repeat on a few rows, 4 expenses, 1 income record and 8 transfers, so the primary key is used instead.
03. an edit in HomeBudget keeps the row's key and changes its fields and `timeStamp`. A reload after an edit updates the matched record in place, per the rebuild-and-reload rule of the **lessons learned**.
04. account `01` accounts and categories match account `02` ones through the pairing in [Accounts held in both](#accounts-held-in-both) and the [Category mapping](#category-mapping). An unpaired account `01` account is added under its own name.
05. no account `01` transaction can match an account `02` one, because DQ.20 keeps the account `01` dates before the account `02` start.

## Account 01 reference figures

The **review script** writes these figures to the **review outputs**, and 02.MIG.09 checks the migrated user against them. Each figure covers the migration scope, 2017-01-01 to 2026-05-23, and is computed from AccountTrans and the reconciled balance points. The cutoff balances match the **homebudget wrapper** for all 69 accounts.

01. **record counts in the scope**: 9,140 expenses, 909 income records and 7,971 transfers. With the skip of DQ.26, the migration loads 9,139 expenses, every income record and every transfer.
02. **opening balances**: one signed balance per migrated account at the end of 2016-12-31, the opening point DQ.40 sets where an account's own point predates the scope.
03. **balances on 2026-05-23**: one signed balance per account in its own currency, for the 60 migrated accounts and the 9 retired ones.
04. **category totals**: 564 rows of posted expense totals, one per year, account `01` category, subcategory and account currency, from 2017 to 2026.
05. **data quality counts**: one count per account `01` issue, so a rerun on a changed database shows which issue moved.

## Edge cases added to the case catalogue

The **test cases** catalogue gains these cases, which trace to the rules above.

01. **account 02 seed**: 02.SEED.14 to 02.SEED.24 cover cross-day splits, transfers out of the cost center, Credit-type assets, the bill account cycle, negative expenses, the card rebate pair, the forfeited deposit, a mid-period balance point, rows dated after the snapshot, transfers with no account and the device match key.
02. **account 01 migration**: 02.MIG.12 to 02.MIG.20 cover the migration scope, retired accounts, AccountTrans amounts, foreign currency expenses, transfers between currencies, opening points at the scope start, zero and negative rows, the reset of paired accounts to their last account `01` point, and the category mapping. 02.MIG.08 checks each cost center against HomeBudget each month, per DQ.31.

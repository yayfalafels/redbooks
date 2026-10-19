# RedBooks 0.2.0 - Data Migration

This doc describes how the HomeBudget history moves into RedBooks: the account `02` seed and the account `01` migration, the order each runs in, and how every HomeBudget account and category maps onto the account types and category model of the **financial statements design**. The **homebudget data review** holds the source layout, the data quality rules, the match keys and the reference figures these loads apply. The **legacy financial statements** doc describes the legacy mapping this doc translates.

## Contents

- [Summary](#summary)
- [References](#references)
- [Migration runs](#migration-runs)
  - [Account 02 seed](#account-02-seed)
  - [Account 01 migration](#account-01-migration)
  - [Migration phases](#migration-phases)
- [Migration irregularities](#migration-irregularities)
- [Account mapping](#account-mapping)
- [Category mapping](#category-mapping)
  - [Mapping rules](#mapping-rules)
  - [Account 02 categories](#account-02-categories)
  - [Account 01 subcategories](#account-01-subcategories)
  - [Legacy line crosswalk](#legacy-line-crosswalk)
- [Account 01 history patterns](#account-01-history-patterns)
- [Handoffs](#handoffs)

## Summary

01. **two loads, one target model.** The account `02` seed loads a dated snapshot of the live HomeBudget database. The account `01` migration loads the frozen account `01` history after every feature milestone is validated. Both load onto the same RedBooks accounts, categories and ledger.
02. **account 02 categories are the base of the category model.** Each account `02` subcategory is the RedBooks subcategory of the same name. The account `01` mapping adds the subcategories account `02` lacks.
03. **account 01 maps through the legacy workbooks in one hop.** The legacy two-stage mapping, HomeBudget category to GL code to statement line, collapses into one rule per source subcategory, from source subcategory to RedBooks subcategory.
04. **every account takes a RedBooks account type.** The HomeBudget type is a source attribute only. An account `01` account takes its type from the legacy account registry, and an account `02` account from its account `01` pair or from its kind.
05. **every load reports.** Each row loads, is skipped as already present, or is listed in the load report with the rule that handled it.
06. **the account 01 migration runs newest year first.** It migrates and reconciles 2026, then 2025. How 2020 to 2024 load is decided after 2025 closes, per [Migration phases](#migration-phases).
07. **every known irregularity is resolved at migration time.** The [Migration irregularities](#migration-irregularities) inventory lists each source irregularity and balance difference with the phase that resolves it.

## References

- **release milestones**: [020-release-milestones.md](../020-release-milestones.md)
- **accounting rules**: [accounting-rules.md](accounting-rules.md)
- **financial statements design**: [financial-statements.md](financial-statements.md)
- **legacy financial statements**: [financial-statements-legacy.md](financial-statements-legacy.md)
- **homebudget data review**: [homebudget-data-review.md](homebudget-data-review.md)
- **homebudget accounts**: [homebudget-accounts.md](homebudget-accounts.md)
- **test cases**: [test-cases.md](test-cases.md)
- **lessons learned**: [easymcf-lessons-learned.md](easymcf-lessons-learned.md)
- **snapshot script**: `scripts/snapshot_homebudget_02.py`
- **fetch script**: `scripts/fetch_legacy_mapping.py`
- **legacy mapping**: `data/legacy-mapping/`, gitignored, holding the fetched `cat_map`, `fin_expense_cat_map` and `accounts` rows
- **review outputs**: `data/homebudget-data-review/`, gitignored, holding the real-name key for every role id and the account `01` reference figures
- **legacy statement files**: `data/financial-statements/`, gitignored, the legacy income statement and balance sheet CSV of each year from 2020 to 2026, the 2026 pair dated 2026-03-29

This doc names accounts by role and role id, per LL.08 of the **lessons learned**. Project names and the real-name key stay in the **review outputs**.

## Migration runs

### Account 02 seed

The seed milestone of the **release milestones** owns this load.

01. **MR.01 snapshot.** The **snapshot script** copies the live account `02` database into `data/homebudget-02/` with a timestamp. The seed loads the newest snapshot, and the snapshot time sets the last date it loads, per DQ.01 of the **homebudget data review**.
02. **MR.02 rebuild and reload.** During `0.2.0` development one command rebuilds the schema and reloads the seed into an empty database. Loading the same snapshot twice gives the same database.
03. **MR.03 accounts.** Each account loads with its account type, per [Account mapping](#account-mapping), and its reconciled balance point from the snapshot.
04. **MR.04 categories.** Each account `02` category and subcategory loads as a RedBooks category and subcategory, per [Account 02 categories](#account-02-categories). An unmapped account or subcategory fails the load with its name, per 02.SEED.03.
05. **MR.05 records.** Account `02` holds no tags, and its splits are cost center groups rather than split records. Every expense, income record and transfer loads as a record of its own kind with no tags under the sign translation and the account `02` data quality rules of the **homebudget data review**, with its account `02` match key, except the groups the split builder of MR.14 reconstructs.
06. **MR.06 statements.** The load generates a statement snapshot for every month it loads.
07. **MR.14 split builder.** Account `02` uses its cost center only for splits, so each transfer into it, the expenses booked on it and the transfers out that return it to zero form one split group, per DQ.14 of the **homebudget data review** for groups whose records fall on two dates. The split builder reconstructs a sample of these groups as split records: the transfer in becomes a payment source paid from its account, each expense a category line, and each transfer out a payment source received into its account. The builder samples only groups whose records fall in one calendar month, per IV.13, and the seed load fails on any account `02` group that crosses a month end, since its cost center would miss 0.00 at that month end and fail CK.06. Each reconstructed split keeps every account entry at its AccountTrans amount, so balances are unchanged, and the seed then holds a split of every shape the samples cover, including one with two payment sources. Account `01` routed every expense through the cost center, so a split group there cannot be told apart from a one-to-one expense, and the migration reconstructs none.

### Account 01 migration

The homebudget account 01 migrate milestone of the **release milestones** owns this load. It runs once every feature milestone is validated.

01. **MR.07 versioned migrations first.** The working database moves to versioned forward migrations, so it keeps its data across every later schema change.
02. **MR.08 opt-in and backup.** One command migrates the history into a user. It refuses to write without a second opt-in, and backs up the working database first.
03. **MR.09 scope.** The migration loads the rows dated 2020-01-01 to 2026-05-23 at most, per DQ.20 of the **homebudget data review**, in the phases of [Migration phases](#migration-phases). The scope starts on 2020-01-01 because every account `01` cost center holds 0.00 at every month end from there on, per DQ.31, so CK.06 of the **financial statements design** holds for every migrated month.
04. **MR.10 reset paired points.** Each account held in both accounts resets its reconciled point to its last account `01` point, and the reconcile scope runs from there to the next reconciliation, per DQ.38 and task 12.02.
05. **MR.11 accounts and categories.** Each account takes its type, per [Account mapping](#account-mapping). Each source subcategory maps to one RedBooks subcategory, per [Account 01 subcategories](#account-01-subcategories), and the mapping report lists any it could not map.
06. **MR.12 upsert.** Every record matches by its account `01` match key. A matched record is skipped, an unmatched one is added, and identical records on one day load separately. A second run adds nothing.
07. **MR.13 checks.** The one cost center of each currency matches the sum of the HomeBudget balances of the account `01` cost centers mapped onto it, at every month end in the scope. Balances and category totals match the account `01` reference figures. The load generates a statement snapshot for every month it loads.
08. **MR.15 dormant accounts.** An account with no activity in the scope takes the treatment of DQ.33 by its balance: left out at 0.00, folded into the SGD pooled foreign cash wallet as a foreign cash wallet, migrated and written off to SC.17 loss on the start date of the earliest loaded phase as a small balance, or left out as the mortgage account closed before the scope. The report lists each dormant account with its treatment.

### Migration phases

The migration loads one phase at a time, newest year first, so the months the user reports on now are reconciled first. A phase closes only when every irregularity of its years is resolved and its checks pass, and the next phase starts after it.

| id    | phase     | rows                     | expenses | income | transfers | status        |
| ----- | --------- | ------------------------ | -------- | ------ | --------- | ------------- |
| MP.01 | 2026      | 2026-01-01 to 2026-05-23 | 506      | 24     | 459       | first         |
| MP.02 | 2025      | 2025-01-01 to 2025-12-31 | 1,355    | 89     | 1,313     | second        |
| MP.03 | 2020-2024 | 2020-01-01 to 2024-12-31 | 4,321    | 582    | 3,958     | decided later |

01. **the same rules in every phase.** Each phase loads its rows through MR.07 to MR.15 and upserts by match key, so a later phase adds only its own rows and a rerun of a phase adds nothing.
02. **an opening point at the phase start.** An account whose current reconciled point predates the earliest loaded phase takes a point on that phase's start date, equal to its HomeBudget balance at the end of the day before, as DQ.40 of the **homebudget data review** sets for the scope start. A later phase that loads an earlier year replaces that point with one on its own start date. Both come from HomeBudget, so every balance from the old start date on stays the same. An account whose current point falls inside the loaded years keeps it, as the paired accounts of MR.10 keep their 2026 points.
03. **accounts with no rows in a phase.** An account with activity elsewhere in the scope and none in the loaded years migrates with its opening point only. The dormant treatments of MR.15 date their points and write-offs on the earliest loaded phase's start date, 2026-01-01 in MP.01, and move back with each phase.
04. **phase checks.** Each month of the phase passes CK.01 to CK.09 of the **financial statements design**. Its net income and closing net worth equal the **legacy statement files** figures for the month, less the legacy reconcile error row, and each account balance at the phase's last month end equals the account `01` reference figure. A difference that remains is an irregularity, resolved before the phase closes.
05. **MP.01 meets the seed.** The account `02` seed holds the records from 2026-05-24, so MP.01 joins the two histories at the cutoff and runs the reconcile bridging of MR.10.
06. **the 2026 reconcile window stays open past MP.01.** The paired accounts' balances run from their last account `01` points in March 2026 to the 2026 reconciliation, which starts in October at the earliest and most likely in November or December. MP.01 closes with that window open: its checks hold every month the window does not cover, and the reconciliation settles the paired accounts' difference, MI.01.
07. **MP.03 is decided after MP.02 closes.** The choice is between loading 2020 to 2024 under the same rules, with the irregularities of MI.12 to MI.15 resolved first, and starting the books on 2025-01-01 with the MP.02 opening points only.

## Migration irregularities

This inventory lists every known irregularity and balance difference in the account `01` sources that the migration resolves, each with the phase that resolves it. The **homebudget data review** holds the counts and rules of the DQ issues, and the **legacy statement files** hold the legacy figures. A row closes when its resolution is applied and the phase checks pass.

| id    | phase | irregularity                                                 | resolution path          |
| ----- | ----- | ------------------------------------------------------------ | ------------------------ |
| MI.01 | MP.01 | 9 paired accounts' cutoff balances differ from account `02`  | 2026 reconciliation      |
| MI.02 | MP.01 | 27 expenses on one 2026 project subcategory have no mapping  | task 12.01               |
| MI.03 | MP.01 | legacy reconcile error of 158 in 2026-01 and 17,893 in 02    | trace before MP.01 close |
| MI.04 | MP.01 | legacy 2026 statements hold actuals to 2026-03 only          | reference figures only   |
| MI.05 | MP.01 | May 2026 splits across account `01` and account `02`         | MR.10 bridging           |
| MI.06 | MP.01 | 4 identical transfer rows on one day                         | DQ.30, confirm each      |
| MI.07 | MP.01 | dormant accounts with a balance                              | MR.15                    |
| MI.08 | MP.01 | mortgage account holds a stale USD 4,205.42                  | left out, reported       |
| MI.09 | each  | clearing categories Balancing, Reimbursable, AM.44 and AM.45 | task 12.01               |
| MI.10 | MP.02 | legacy reconcile error of -7,039 in 2025-09 and 7,004 in 10  | trace before MP.02 close |
| MI.11 | MP.02 | 6 identical expense rows and 8 identical transfer rows       | DQ.30, confirm each      |
| MI.12 | MP.03 | legacy 2023 income statement and balance sheet disagree      | decided with MP.03       |
| MI.13 | MP.03 | 36 expenses whose `Expense.amount` differs, 2020 to 2023     | DQ.22                    |
| MI.14 | MP.03 | legacy reconcile errors up to 1,574 a month in 2024          | decided with MP.03       |
| MI.15 | MP.03 | 11 accounts whose current point predates 2020-01-01          | DQ.40, phase start point |

01. **MI.01** for the 9 accounts held in both with a non-zero balance, the account `01` balance on 2026-05-23 differs from the account `02` opening point, per DQ.38 and summary item 10 of the **homebudget data review**. MP.01 resets each to its last account `01` point, mostly from February or March 2026. The reconcile window runs from March 2026 to the 2026 reconciliation, which starts in October at the earliest and most likely in November or December, and the reconciliation settles the difference, per phase rule 06.
02. **MI.02** the `cat_map` region covers every in-scope expense except these 27, per the account `01` mapping of the **homebudget data review**. Task 12.01 maps the subcategory before MP.01 loads.
03. **MI.03** the legacy balance sheet's reconcile error row is the difference between its net worth movement and its account balances. The 17,893 in February 2026 is the largest of the scope. MP.01 traces it to the records or balance points behind it, and the RedBooks figure for the month either matches the legacy figure net of the error or is explained.
04. **MI.04** the 2026 legacy files are dated 2026-03-29, and their April to December columns are forecast. April and May 2026 check against the account `01` reference figures and the HomeBudget balances only.
05. **MI.05** May 2026 holds account `01` records to 2026-05-23 and account `02` seed records from 2026-05-24. Its statement covers both, so its check runs after the bridging of MI.01.
06. **MI.06, MI.11** identical rows load as separate records, per DQ.30. The phase confirms each group is a real repeat, such as two equal fares on one day, and lists it in the report.
07. **MI.07** the 5 foreign cash wallets fold into the SGD pooled foreign cash wallet at the month-end rates of the day before the earliest loaded phase, and the 3 small balances are written off to SC.17 loss on that phase's start date, per DQ.33 and MR.15.
08. **MI.08** the mortgage closed by the end of 2019. The account is left out, and the report lists its stale balance, per DQ.33 item 04.
09. **MI.09** the legacy mapping folds these categories into misc discretionary, though they act as clearing accounts. Task 12.01 decides whether each is an expense or a clearing account before the first phase that holds their rows loads.
10. **MI.10** the two errors nearly cancel across September and October 2025, which points to one movement booked in different months on the two sides. MP.02 traces it as MI.03 traces February 2026. MP.02 also reviews the January 2025 error of -597.
11. **MI.12** the 2023 income statement's net income differs from the balance sheet's by 1,082 in January and 5,763 in February, 6,846 for the year, and its December 2022 opening column reads -2,321 against -2,302. The pattern points to the two files coming from different versions of the legacy workbook. MP.03 picks the reference figure or a fresh export.
12. **MI.13** all 36 sit on one USD cost center, and DQ.03 takes AccountTrans as the amount.
13. **MI.14** the 2024 legacy reconcile error row runs from -1,574 to 1,371, and the earlier years hold smaller errors. MP.03 sets the tolerance or traces each.
14. **MI.15** each takes its phase start point under phase rule 02, and DQ.40 sets the 2020-01-01 point if MP.03 loads 2020.

## Account mapping

Each HomeBudget account takes one of the account types TY.01 to TY.08 of the **financial statements design**, or none when it sits outside net worth. The HomeBudget type never decides it, since a Credit account's balance can be positive or negative. Nothing in the HomeBudget database names an account's role either, so the loader cannot derive the type. It reads it from an explicit account map.

**the account map** has one row per HomeBudget account, and the loader looks each account up in it.

| id    | column       | value                                                 |
| ----- | ------------ | ----------------------------------------------------- |
| MC.01 | source       | `hb01` or `hb02`                                      |
| MC.02 | account key  | the account's match key, MK.01 or MK.02 of the review |
| MC.03 | account type | one of TY.01 to TY.08, or null outside net worth      |
| MC.04 | in net worth | true or false                                         |

01. **MC.03 and MC.04 agree.** An account in net worth has a type, and an account outside net worth has none.
02. **an account missing from the map fails the load** with its name, per 02.SEED.03 and 02.MIG.03. The loader never falls back to a default type.
03. **the map carries real account names**, so it lives with the **review outputs**, out of version control. This doc refers to its rows by role id.

**filling the map.** Each account's row comes from the first of these sources that covers it.

01. **account 01 registry accounts** take the type of their asset subcategory in the legacy `accounts` region, which the **fetch script** reads into the **legacy mapping**. A registry savings account takes `bank account`. The one exception is the cash of a margin brokerage account, which takes `margin credit`, per TM.06.
02. **account 01 cost centers** map onto the user's one cost center of their currency, per AR.07 item 06 of the **accounting rules**, as task 12.03. The account `01` accounts outside the registry sit outside net worth, per M1.03 of the **homebudget data review**.
03. **account 02 accounts paired with account 01** take the type of their pair, per [Accounts held in both](homebudget-data-review.md#accounts-held-in-both) of the review.
04. **any other account** takes the type its role sets in the table below. A person assigns the role when adding the account to the map.

| id    | role                               | account type  |
| ----- | ---------------------------------- | ------------- |
| TM.01 | cost center                        | clearing      |
| TM.02 | bank account                       | bank account  |
| TM.03 | physical cash                      | wallet cash   |
| TM.04 | stored-value card or e-wallet      | wallet cash   |
| TM.05 | cash account of an investment      | bank account  |
| TM.06 | cash of a margin brokerage account | margin credit |
| TM.07 | investment position                | investment    |
| TM.08 | credit card                        | credit card   |
| TM.09 | loan                               | other credit  |
| TM.10 | bill account                       | other credit  |
| TM.11 | household share account            | other credit  |
| TM.12 | tax payable                        | other credit  |
| TM.13 | security deposit                   | other credit  |
| TM.14 | receivable from a person           | other credit  |
| TM.15 | retirement fund                    | retirement    |
| TM.16 | retirement brokerage position      | retirement    |
| TM.17 | counterparty the user does not own | none          |

In account `02`, M2.01 and M2.03 are bank accounts, M2.02, M2.08 and M2.09 wallet cash, M2.04 clearing, M2.05 margin credit, M2.06 a credit card, M2.07, M2.10 to M2.13, M2.15 and M2.16 other credit, and M2.14 an investment.

01. **stored value** loads as wallet cash, as the legacy `accounts` region files it. **margin cash** loads as margin credit and stays in credit at any balance. The legacy `accounts` region filed it as a savings account placed by its sign, and the legacy published statements list both under misc credit, so a migrated balance sheet places them differently from the legacy one.
02. **the cost center** was off the legacy balance sheet. It loads as `clearing`, the one cost center of its currency, which holds 0.00 at every month end and has no line on the RedBooks balance sheet.

## Category mapping

### Mapping rules

The legacy workbooks reached a statement line in two stages, per [Category mapping in two stages](financial-statements-legacy.md#category-mapping-in-two-stages) of the **legacy financial statements**. The migration collapses them into one hop and keeps their business rules.

01. **CR.01 one hop from entry to line.** The account `02` categories are the RedBooks categories, so an entry's subcategory is its detail line and its category's section is its group. No GL code sits between them.
02. **CR.02 the section follows the COLE flag.** A category whose legacy lines carry COLE 1 takes section `cole`. One with COLE 0 takes `rental` when its line is rental and `discretionary` otherwise. Account `02` follows this already: cole and insurance hold COLE lines, rent holds rental, and discretionary and projects hold the rest.
03. **CR.03 a section is set per category.** The legacy COLE flag was set per line. A source category whose subcategories would fall in two sections splits across RedBooks categories, as account `01` Health and Wellness splits across cole, insurance and discretionary.
04. **CR.04 many sources, one line.** The legacy lines aggregated several GL codes, such as socializing from socializing and dating. RedBooks keeps the finer subcategories, such as social and dating, and the category line totals them. Each source subcategory maps to exactly one RedBooks subcategory.
05. **CR.05 the specific line wins.** A source subcategory with a specific line maps there, and only the rest of a discretionary category maps to SC.42.
06. **CR.06 taxes reduce income.** The taxes category sits in personal income, per PS.08 and PS.09 of the **financial statements design**. A government subsidy loads as a positive entry on other tax.
07. **CR.07 an unmapped subcategory fails only in scope.** The migration fails a row whose source subcategory has no mapping inside the migration scope, and drops a subcategory with no row in scope, per DQ.35 of the **homebudget data review**.

### Account 02 categories

01. **expense subcategories** each of the 29 account `02` subcategories loads as the RedBooks subcategory of the same name, SC.01 to SC.40 of the **financial statements design**.
02. **insurance** has no subcategories in account `02`, per DQ.16 of the **homebudget data review**. It loads as a category, and the account `01` mapping adds its health subcategory, SC.18.
03. **income records** the eight account `02` income records map by name: salary records to PS.01, the government rebate to PS.06 and the card rebate to PS.05.
04. **taxes** loads in section `personal`, per CR.06.

### Account 01 subcategories

The account `01` subcategories map as the `cat_map` and `fin_expense_cat_map` regions set them. This is the subcategory-level mapping task 12.01 confirms with the user.

| id    | account 01 category     | account 01 subcategories           | legacy `gl_code`     | RedBooks   |
| ----- | ----------------------- | ---------------------------------- | -------------------- | ---------- |
| AM.01 | Food (Basic)            | all four                           | food                 | SC.02      |
| AM.02 | Health and Wellness     | Grooming, Haircut                  | healthcare_oop       | SC.05      |
| AM.03 | Health and Wellness     | Medical expenses, Medical supplies | healthcare_oop       | SC.04      |
| AM.04 | Health and Wellness     | Health insurance                   | insurance            | SC.18      |
| AM.05 | Health and Wellness     | Fitness                            | fitness              | SC.19      |
| AM.06 | Health and Wellness     | Massage                            | discretionary_misc   | SC.41      |
| AM.07 | Health and Wellness     | Medical - sexual health            | discretionary_misc   | SC.42      |
| AM.08 | Household               | Maintenance                        | maintenance          | SC.15      |
| AM.09 | Household               | Sundries                           | sundries             | SC.14      |
| AM.10 | Household               | Pet and Plants                     | pets_and_plants      | SC.36      |
| AM.11 | Household               | Cleaning service                   | cleaning_service     | SC.38      |
| AM.12 | Household               | Durable goods, Furniture           | durables             | SC.37      |
| AM.13 | Personal Discretionary  | Clothing, Shoes                    | clothing             | SC.07      |
| AM.14 | Personal Discretionary  | Books                              | books                | SC.27      |
| AM.15 | Personal Discretionary  | Education                          | books                | SC.29      |
| AM.16 | Personal Discretionary  | IT                                 | it_hardware          | SC.26      |
| AM.17 | Personal Discretionary  | Cloud data                         | it_software          | SC.24      |
| AM.18 | Personal Discretionary  | Donations                          | discretionary_misc   | SC.35      |
| AM.19 | Personal Discretionary  | Jewelry and Accessories            | discretionary_misc   | SC.42      |
| AM.20 | Professional Services   | Post                               | post                 | SC.08      |
| AM.21 | Professional Services   | the other four                     | discretionary_misc   | SC.34      |
| AM.22 | Project                 | academic program projects          | higher_education     | SC.29      |
| AM.23 | Project                 | trip projects                      | travel               | SC.28      |
| AM.24 | Project                 | carbon offset                      | discretionary_misc   | SC.42      |
| AM.25 | Project                 | other projects                     | projects             | SC.40      |
| AM.26 | Rent                    | Rent                               | rental               | SC.01      |
| AM.27 | Social & Entertainment  | Alcohol                            | alcohol              | SC.21      |
| AM.28 | Social & Entertainment  | Drinks - nonalcoholic              | non_alcoholic_drinks | SC.20      |
| AM.29 | Social & Entertainment  | Dating, Date night dinner          | socializing          | SC.23      |
| AM.30 | Social & Entertainment  | Friends, Events and others         | socializing          | SC.22      |
| AM.31 | Social & Entertainment  | Family, Gifts                      | family_gifts         | SC.39      |
| AM.32 | Taxes and Fines         | Taxes - income                     | income tax           | PS.08      |
| AM.33 | Taxes and Fines         | Taxes - other, Gov subsidy         | income tax           | PS.09      |
| AM.34 | Taxes and Fines         | Fines                              | discretionary_misc   | SC.31      |
| AM.35 | Taxes and Fines         | unauthorized transaction           | discretionary_misc   | SC.42      |
| AM.36 | Transport               | MRT                                | transport            | SC.03      |
| AM.37 | Transport               | every Taxi subcategory             | discretionary_misc   | SC.32      |
| AM.38 | Transport               | Bike                               | discretionary_misc   | SC.03      |
| AM.39 | Travel                  | Lodging                            | travel               | SC.28      |
| AM.40 | Utilities               | Electricity                        | electricity          | SC.13      |
| AM.41 | Utilities               | Gas, Water, PUB other              | pub_water_gas        | SC.10-12   |
| AM.42 | Utilities               | Internet/TV                        | singtel_internet     | SC.09      |
| AM.43 | Utilities               | Mobile                             | mobile               | SC.06      |
| AM.44 | Balancing, Reimbursable | all                                | discretionary_misc   | task 12.01 |
| AM.45 | Real Estate, Securities | all                                | none                 | task 12.01 |
| AM.46 | Professional Services   | Currency conversion                | discretionary_misc   | SC.33      |

The same mapping, with each RedBooks line named by its category and subcategory. AX.nn repeats AM.nn, and the AM notes apply to it.

| id    | account 01 category     | account 01 subcategories  | category      | subcategory           | RedBooks |
| ----- | ----------------------- | ------------------------- | ------------- | --------------------- | -------- |
| AX.01 | Food (Basic)            | all four                  | cole          | food                  | SC.02    |
| AX.02 | Health and Wellness     | Grooming, Haircut         | cole          | grooming              | SC.05    |
| AX.03 | Health and Wellness     | Medical expenses/supplies | cole          | healthcare            | SC.04    |
| AX.04 | Health and Wellness     | Health insurance          | insurance     | health                | SC.18    |
| AX.05 | Health and Wellness     | Fitness                   | discretionary | fitness               | SC.19    |
| AX.06 | Health and Wellness     | Massage                   | discretionary | massage               | SC.41    |
| AX.07 | Health and Wellness     | Medical - sexual health   | discretionary | other                 | SC.42    |
| AX.08 | Household               | Maintenance               | cole          | maintenance           | SC.15    |
| AX.09 | Household               | Sundries                  | cole          | sundries              | SC.14    |
| AX.10 | Household               | Pet and Plants            | discretionary | pets and plants       | SC.36    |
| AX.11 | Household               | Cleaning service          | discretionary | cleaning              | SC.38    |
| AX.12 | Household               | Durable goods, Furniture  | discretionary | durables              | SC.37    |
| AX.13 | Personal Discretionary  | Clothing, Shoes           | cole          | clothing              | SC.07    |
| AX.14 | Personal Discretionary  | Books                     | discretionary | books                 | SC.27    |
| AX.15 | Personal Discretionary  | Education                 | discretionary | education             | SC.29    |
| AX.16 | Personal Discretionary  | IT                        | discretionary | it hardware           | SC.26    |
| AX.17 | Personal Discretionary  | Cloud data                | discretionary | software              | SC.24    |
| AX.18 | Personal Discretionary  | Donations                 | discretionary | donations             | SC.35    |
| AX.19 | Personal Discretionary  | Jewelry and Accessories   | discretionary | other                 | SC.42    |
| AX.20 | Professional Services   | Post                      | cole          | post                  | SC.08    |
| AX.21 | Professional Services   | the other four            | discretionary | professional services | SC.34    |
| AX.22 | Project                 | academic program projects | discretionary | education             | SC.29    |
| AX.23 | Project                 | trip projects             | discretionary | travel                | SC.28    |
| AX.24 | Project                 | carbon offset             | discretionary | other                 | SC.42    |
| AX.25 | Project                 | other projects            | projects      | one per project       | SC.40    |
| AX.26 | Rent                    | Rent                      | rent          | rent                  | SC.01    |
| AX.27 | Social & Entertainment  | Alcohol                   | discretionary | alcohol               | SC.21    |
| AX.28 | Social & Entertainment  | Drinks - nonalcoholic     | discretionary | drinks                | SC.20    |
| AX.29 | Social & Entertainment  | Dating, Date night dinner | discretionary | dating                | SC.23    |
| AX.30 | Social & Entertainment  | Friends, Events, others   | discretionary | social                | SC.22    |
| AX.31 | Social & Entertainment  | Family, Gifts             | discretionary | gifts                 | SC.39    |
| AX.32 | Taxes and Fines         | Taxes - income            | taxes         | income tax            | PS.08    |
| AX.33 | Taxes and Fines         | Taxes - other, subsidy    | taxes         | other tax             | PS.09    |
| AX.34 | Taxes and Fines         | Fines                     | discretionary | fines                 | SC.31    |
| AX.35 | Taxes and Fines         | unauthorized transaction  | discretionary | other                 | SC.42    |
| AX.36 | Transport               | MRT                       | cole          | transport             | SC.03    |
| AX.37 | Transport               | every Taxi subcategory    | discretionary | taxi                  | SC.32    |
| AX.38 | Transport               | Bike                      | cole          | transport             | SC.03    |
| AX.39 | Travel                  | Lodging                   | discretionary | travel                | SC.28    |
| AX.40 | Utilities               | Electricity               | cole          | electricity           | SC.13    |
| AX.41 | Utilities               | Gas, Water, PUB other     | cole          | water, gas, pub other | SC.10-12 |
| AX.42 | Utilities               | Internet/TV               | cole          | internet              | SC.09    |
| AX.43 | Utilities               | Mobile                    | cole          | mobile                | SC.06    |
| AX.44 | Balancing, Reimbursable | all                       | task 12.01    | task 12.01            | none     |
| AX.45 | Real Estate, Securities | all                       | task 12.01    | task 12.01            | none     |
| AX.46 | Professional Services   | Currency conversion       | discretionary | forex charges         | SC.33    |

01. **AM.02** the **fs category translation** of the **legacy financial statements** files grooming under healthcare out-of-pocket. RedBooks gives it its own cole subcategory, so the section is unchanged.
02. **AM.15** the legacy stage 2 fed Education into the books line. RedBooks files it with the academic projects of AM.22 under education, since both are spending on courses.
03. **AM.21** Agent, Banking, Counseling and Legal. **AM.46** Currency conversion is the card foreign exchange fee, and maps to forex charges, SC.33. **AM.38** Bike is cost of living and maps to transport, SC.03, beside metro and bus fares, although the legacy mapping filed it under misc discretionary.
04. **AM.22 to AM.25** project names stay out of committed docs. The **review outputs** list each project with its mapping.
05. **AM.37** the legacy `fin_expense_cat_map` row for transport also lists a taxi code, but the `cat_map` note sets every taxi subcategory as discretionary. RedBooks follows the `cat_map` note.
06. **AM.41** each maps to the account `02` subcategory of its own name, SC.10 to SC.12, which together are the legacy PUB water/gas line.
07. **AM.44** the legacy mapping folds Balancing, Reimbursable and the retired helva budget into misc discretionary. They act as clearing categories, and task 12.01 decides whether each is an expense or a clearing account.
08. **AM.45** Real Estate and Securities sat outside the personal cost center in account `01`. Task 12.01 maps Securities into investment P and L, IS.02, and Real Estate by what each entry records.
09. task 12.01 may add subcategories. Each new subcategory belongs to a category, which carries its section.

### Legacy line crosswalk

The crosswalk maps each RedBooks category and subcategory back to the legacy statement line it mirrors, so a migrated month compares line by line with the legacy published statements.

| id    | category      | legacy group           |
| ----- | ------------- | ---------------------- |
| XG.01 | rent          | rental_expenses        |
| XG.02 | cole          | cole_expenses          |
| XG.03 | insurance     | cole_expenses          |
| XG.04 | discretionary | discretionary_expenses |
| XG.05 | projects      | discretionary_expenses |
| XG.06 | taxes         | taxes paid             |

| id    | subcategory           | legacy `gl_code`     |
| ----- | --------------------- | -------------------- |
| XL.01 | SC.01 rent            | rental               |
| XL.02 | SC.02 food            | food                 |
| XL.03 | SC.03 transport       | transport            |
| XL.04 | SC.04 healthcare      | healthcare_oop       |
| XL.05 | SC.05 grooming        | healthcare_oop       |
| XL.06 | SC.06 mobile          | mobile               |
| XL.07 | SC.07 clothing        | clothing             |
| XL.08 | SC.08 post            | post                 |
| XL.09 | SC.09 internet        | singtel_internet     |
| XL.10 | SC.10 to SC.12        | pub_water_gas        |
| XL.11 | SC.13 electricity     | electricity          |
| XL.12 | SC.14 sundries        | sundries             |
| XL.13 | SC.15 maintenance     | maintenance          |
| XL.14 | SC.16, SC.17          | none                 |
| XL.15 | SC.18 health          | insurance            |
| XL.16 | SC.19 fitness         | fitness              |
| XL.17 | SC.20 drinks          | non_alcoholic_drinks |
| XL.18 | SC.21 alcohol         | alcohol              |
| XL.19 | SC.22, SC.23          | socializing          |
| XL.20 | SC.24, SC.25          | it_software          |
| XL.21 | SC.26 it hardware     | it_hardware          |
| XL.22 | SC.27 books           | books                |
| XL.23 | SC.28 travel          | travel               |
| XL.24 | SC.29 education       | higher_education     |
| XL.25 | SC.30 to SC.35        | discretionary_misc   |
| XL.26 | SC.36 pets and plants | pets_and_plants      |
| XL.27 | SC.37 durables        | durables             |
| XL.28 | SC.38 cleaning        | cleaning_service     |
| XL.29 | SC.39 gifts           | family_gifts         |
| XL.30 | SC.40 projects        | projects             |
| XL.31 | SC.41, SC.42          | discretionary_misc   |

01. **XL.14** services and loss are account `02` subcategories with no legacy line. Both are cost of living as account `02` files them.
02. **XL.20** AI service subscriptions would have filed under the legacy IT software line.
03. **XL.25** the legacy misc discretionary line was a catch-all for every discretionary row no specific line captured. RedBooks gives each its own subcategory, and SC.42 takes the rest explicitly.

## Account 01 history patterns

Account `01` recorded some events differently from how RedBooks posts them. The migration loads each as the history recorded it, and the statements read it with these rules.

01. **retirement contributions.** Account `01` booked the employee contribution as a transfer from the salary account into the retirement funds, as the legacy statements did. The migration keeps the transfer pattern. RC.01 of the **financial statements design** counts transfers into `retirement` accounts, so a migrated month shows the employee share in RC.01 and in CT.01, and its gross salary line holds the salary as account `01` recorded it.
02. **government subsidy.** Account `01` filed the subsidy under taxes. It loads as a positive entry on other tax, PS.09, per CR.06.
03. **cost centers.** The account `01` cost centers of each currency map onto the user's one cost center of that currency, task 12.03, and keep their clearing history there as separate transfers and expenses, per AR.07 item 07 of the **accounting rules**. The migration never groups them into splits.
04. **positions closed with no cost basis** load as transfers, per DQ.12 of the **homebudget data review**, and add nothing to realised gain or loss.
05. **accounts outside HomeBudget net worth** load outside net worth, per DQ.39 of the **homebudget data review**. Their movements reach the net worth movement block, NM.03.

## Handoffs

| id    | topic                   | handoff                                                  |
| ----- | ----------------------- | -------------------------------------------------------- |
| HO.01 | 04.04 homebudget review | account type per account, subcategory per income record  |
| HO.02 | task 12.01              | confirm the AM mapping, settle AM.44 and AM.45           |
| HO.03 | task 12.02              | bridge the paired accounts from account 01 to account 02 |
| HO.04 | task 12.03              | map account 01 cost centers onto one per currency        |

01. **HO.01** the **homebudget data review** confirms the account `02` mapping with the user before the account `02` seed milestone closes, per its open issue.

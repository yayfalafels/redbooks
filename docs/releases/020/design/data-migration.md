# RedBooks 0.2.0 - Data Migration

This doc describes how the HomeBudget history moves into RedBooks: the account `02` seed and the account `01` migration, the order each runs in, and how every HomeBudget account and category maps onto the account types and category model of the **financial statements design**. The **homebudget data review** holds the source layout, the data quality rules, the match keys and the reference figures these loads apply. The **legacy financial statements** doc describes the legacy mapping this doc translates.

## Contents

- [Summary](#summary)
- [References](#references)
- [Migration runs](#migration-runs)
  - [Account 02 seed](#account-02-seed)
  - [Account 01 migration](#account-01-migration)
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

This doc names accounts by role and role id, per LL.08 of the **lessons learned**. Project names and the real-name key stay in the **review outputs**.

## Migration runs

### Account 02 seed

The seed milestone of the **release milestones** owns this load.

01. **MR.01 snapshot.** The **snapshot script** copies the live account `02` database into `data/homebudget-02/` with a timestamp. The seed loads the newest snapshot, and the snapshot time sets the last date it loads, per DQ.01 of the **homebudget data review**.
02. **MR.02 rebuild and reload.** During `0.2.0` development one command rebuilds the schema and reloads the seed into an empty database. Loading the same snapshot twice gives the same database.
03. **MR.03 accounts.** Each account loads with its account type, per [Account mapping](#account-mapping), and its reconciled balance point from the snapshot.
04. **MR.04 categories.** Each account `02` category and subcategory loads as a RedBooks category and subcategory, per [Account 02 categories](#account-02-categories). An unmapped account or subcategory fails the load with its name, per 02.SEED.03.
05. **MR.05 records.** Every expense, income record and transfer loads under the sign translation and the account `02` data quality rules of the **homebudget data review**, with its account `02` match key.
06. **MR.06 statements.** The load generates a statement snapshot for every month it loads.

### Account 01 migration

The homebudget account 01 migrate milestone of the **release milestones** owns this load. It runs once every feature milestone is validated.

01. **MR.07 versioned migrations first.** The working database moves to versioned forward migrations, so it keeps its data across every later schema change.
02. **MR.08 opt-in and backup.** One command migrates the history into a user. It refuses to write without a second opt-in, and backs up the working database first.
03. **MR.09 scope.** The migration loads the rows dated 2017-01-01 to 2026-05-23, and leaves out the retired accounts, per DQ.20 and DQ.33 of the **homebudget data review**.
04. **MR.10 reset paired points.** Each account held in both accounts resets its reconciled point to its last account `01` point, and the reconcile scope runs from there to the next reconciliation, per DQ.38 and task 12.02.
05. **MR.11 accounts and categories.** Each account takes its type, per [Account mapping](#account-mapping). Each source subcategory maps to one RedBooks subcategory, per [Account 01 subcategories](#account-01-subcategories), and the mapping report lists any it could not map.
06. **MR.12 upsert.** Every record matches by its account `01` match key. A matched record is skipped, an unmatched one is added, and identical records on one day load separately. A second run adds nothing.
07. **MR.13 checks.** Each cost center matches its HomeBudget balance at every month end in the scope. Balances and category totals match the account `01` reference figures. The load generates a statement snapshot for every month it loads.

## Account mapping

Each HomeBudget account takes one of the account types TY.01 to TY.08 of the **financial statements design**, or none when it sits outside net worth. The HomeBudget type never decides it, since a Credit account's balance can be positive or negative. Nothing in the HomeBudget database names an account's role either, so the loader cannot derive the type. It reads it from an explicit account map.

**the account map** has one row per HomeBudget account, and the loader looks each account up in it.

| id    | column       | value                                                 |
| ----- | ------------ | ----------------------------------------------------- |
| AC.01 | source       | `hb01` or `hb02`                                      |
| AC.02 | account key  | the account's match key, MK.01 or MK.02 of the review |
| AC.03 | account type | one of TY.01 to TY.08, or null outside net worth      |
| AC.04 | in net worth | true or false                                         |

01. **AC.03 and AC.04 agree.** An account in net worth has a type, and an account outside net worth has none.
02. **an account missing from the map fails the load** with its name, per 02.SEED.03 and 02.MIG.03. The loader never falls back to a default type.
03. **the map carries real account names**, so it lives with the **review outputs**, out of version control. This doc refers to its rows by role id.

**filling the map.** Each account's row comes from the first of these sources that covers it.

01. **account 01 registry accounts** take the type of their asset subcategory in the legacy `accounts` region, which the **fetch script** reads into the **legacy mapping**.
02. **account 01 cost centers** take `clearing`. The account `01` accounts outside the registry sit outside net worth, per M1.03 of the **homebudget data review**.
03. **account 02 accounts paired with account 01** take the type of their pair, per [Accounts held in both](homebudget-data-review.md#accounts-held-in-both) of the review.
04. **any other account** takes the type its role sets in the table below. A person assigns the role when adding the account to the map.

| id    | role                                    | account type    |
| ----- | --------------------------------------- | --------------- |
| TM.01 | cost center                             | clearing        |
| TM.02 | bank account                            | bank account    |
| TM.03 | physical cash                           | wallet cash     |
| TM.04 | stored-value card or e-wallet           | wallet cash     |
| TM.05 | cash account of an investment           | savings account |
| TM.06 | investment position                     | investment      |
| TM.07 | credit card                             | credit card     |
| TM.08 | loan                                    | other credit    |
| TM.09 | bill account                            | other credit    |
| TM.10 | household share account                 | other credit    |
| TM.11 | tax payable                             | other credit    |
| TM.12 | security deposit                        | other credit    |
| TM.13 | receivable from a person                | other credit    |
| TM.14 | retirement fund                         | retirement      |
| TM.15 | retirement brokerage position           | retirement      |
| TM.16 | counterparty the user does not own      | none            |

In account `02`, M2.01 and M2.03 are bank accounts, M2.02, M2.08 and M2.09 wallet cash, M2.04 clearing, M2.05 a savings account, M2.06 a credit card, M2.07, M2.10 to M2.13, M2.15 and M2.16 other credit, and M2.14 an investment.

01. **stored value** loads as wallet cash, and **brokerage cash** as a savings account placed by its sign, as the legacy `accounts` region files them. The legacy published statements list both under misc credit, so a migrated balance sheet places them differently from the legacy one.
02. **the cost center** was off the legacy balance sheet. It loads as `clearing` and shows on the RedBooks balance sheet while a split spans a month end.

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
| AM.21 | Professional Services   | the other five                     | discretionary_misc   | SC.34      |
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
| AM.38 | Transport               | Bike                               | discretionary_misc   | SC.33      |
| AM.39 | Travel                  | Lodging                            | travel               | SC.28      |
| AM.40 | Utilities               | Electricity                        | electricity          | SC.13      |
| AM.41 | Utilities               | Gas, Water, PUB other              | pub_water_gas        | SC.10-12   |
| AM.42 | Utilities               | Internet/TV                        | singtel_internet     | SC.09      |
| AM.43 | Utilities               | Mobile                             | mobile               | SC.06      |
| AM.44 | Balancing, Reimbursable | all                                | discretionary_misc   | task 12.01 |
| AM.45 | Real Estate, Securities | all                                | none                 | task 12.01 |

01. **AM.02** the **fs category translation** of the **legacy financial statements** files grooming under healthcare out-of-pocket. RedBooks gives it its own cole subcategory, so the section is unchanged.
02. **AM.15** the legacy stage 2 fed Education into the books line. RedBooks files it with the academic projects of AM.22 under education, since both are spending on courses.
03. **AM.21** Agent, Banking, Counseling, Currency conversion and Legal. Currency conversion is the card foreign exchange fee, per SC.34.
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
03. **cost centers.** The account `01` cost centers load as `clearing` accounts and keep their clearing history, per AR.07 of the **accounting rules**.
04. **positions closed with no cost basis** load as transfers, per DQ.12 of the **homebudget data review**, and add nothing to realised gain or loss.
05. **accounts outside HomeBudget net worth** load outside net worth, per DQ.39 of the **homebudget data review**. Their movements reach the net worth movement block, NM.03.

## Handoffs

| id    | topic                   | handoff                                                  |
| ----- | ----------------------- | -------------------------------------------------------- |
| HO.01 | 04.04 homebudget review | account type per account, subcategory per income record  |
| HO.02 | task 12.01              | confirm the AM mapping, settle AM.44 and AM.45           |
| HO.03 | task 12.02              | bridge the paired accounts from account 01 to account 02 |

01. **HO.01** the **homebudget data review** confirms the account `02` mapping with the user before the account `02` seed milestone closes, per its open issue.

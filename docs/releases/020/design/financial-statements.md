# RedBooks 0.2.0 - Financial Statements

This doc defines the two financial statements RedBooks reports, the income statement and the balance sheet. It covers their layout, the sections and account types that place every entry and every account on a line, the definition and calculation of each line and sub-line, the forex gain or loss, and the checks every statement passes. Every statement is built from the RedBooks ledger, category model, account types and stored exchange rates, in the signed-entry vocabulary of the **accounting rules**.

## Contents

- [Summary](#summary)
- [References](#references)
- [Scope, period and population](#scope-period-and-population)
- [Statement data model](#statement-data-model)
- [Income statement](#income-statement)
  - [Income statement layout](#income-statement-layout)
  - [Income statement sections](#income-statement-sections)
  - [Summary block](#summary-block)
  - [Investment P and L](#investment-p-and-l)
  - [Personal income](#personal-income)
  - [Total expenses](#total-expenses)
  - [Expense detail](#expense-detail)
  - [Retirement contributions](#retirement-contributions)
- [Balance sheet](#balance-sheet)
  - [Balance sheet layout](#balance-sheet-layout)
  - [Account types](#account-types)
  - [Net worth movement](#net-worth-movement)
  - [Net worth and its sections](#net-worth-and-its-sections)
  - [Net cash transfers](#net-cash-transfers)
  - [Account detail](#account-detail)
- [Currency translation and forex](#currency-translation-and-forex)
- [Presentation view](#presentation-view)
- [Line keys](#line-keys)
- [Checks](#checks)
- [Worked examples](#worked-examples)
- [Decisions settled and handoffs](#decisions-settled-and-handoffs)

## Summary

01. **two statements from one signed ledger.** The income statement covers a calendar month in the user's timezone, and the balance sheet stands at the end of that month. Both report in the user's reporting currency. The books, the API, the snapshots and every oracle hold signed amounts, and only rendering flips expense signs, per AR.18 of the **accounting rules**.
02. **both statements lead with a summary block.** The income statement opens with net income, cash savings, gross savings, investment P and L and the forex gain or loss. The balance sheet opens with net income, the change in net worth, and opening and closing net worth. Detail follows below.
03. **net income is gross savings plus investment P and L plus the forex gain or loss.** Gross savings is personal income less total expenses. Cash savings is gross savings less retirement contributions, which the user cannot spend.
04. **the income statement groups the two-level category model into sections.** The category model has categories and their subcategories, and each subcategory is a detail line. The statement section is not a third level of the model but a required attribute of each category, which adds a section total above its category lines. A category line totals its subcategories, and a section totals its categories. The sections are personal income, investment P and L, rental, cost of living expenses (COLE) and discretionary.
05. **taxes deduct inside personal income.** Taxes stays an expense category in the books, and the statement places it in personal income as taxes paid.
06. **the balance sheet nests net worth over its sections.** Net worth is illiquid and retirement plus liquid net worth, and liquid net worth is cash and bank accounts, liquid investments and credit. Every account type belongs to one section.
07. **liabilities show their signed negative balance.** The balance sheet never flips a sign, so every section and net worth is the plain sum of the lines beneath it. This settles 02.OD.10 and WI.06.
08. **brokerage cash is the one account whose section follows its sign.** A positive balance sits in cash and bank accounts and a negative one in credit.
09. **the forex gain or loss is computed when a statement is built.** For each foreign currency account it is the closing reporting value, less the opening reporting value, less the period's entries in the reporting currency. It is never posted to the ledger, and it appears on both statements.
10. **the two statements reconcile exactly.** Closing net worth equals opening net worth plus net income, plus opening balances and movements with accounts outside net worth. RedBooks builds both statements from one ledger, so the gap is zero by construction, and a non-zero gap fails the build.
11. **the statement data is separate from its presentation.** A build stores detail lines, read from the ledger, and summary lines, the totals and derived lines computed from them, in two tables. The presentation view arranges both into the layout, adds labels, levels and the figures that span months, and flips expense signs only when it renders.

## References

- **release notes**: [020-release.md](../020-release.md)
- **release milestones**: [020-release-milestones.md](../020-release-milestones.md)
- **accounting rules**: [accounting-rules.md](accounting-rules.md)
- **workflows**: [workflows.md](workflows.md)
- **front end pages**: [front-end-pages.md](front-end-pages.md)
- **test cases**: [test-cases.md](test-cases.md)
- **lessons learned**: [easymcf-lessons-learned.md](easymcf-lessons-learned.md)
- **statements skill**: `.claude/skills/accounting/references/statements.md`

This doc names accounts by role and uses illustrative amounts, per LL.08 of the **lessons learned**.

## Scope, period and population

01. **SP.01 the income statement period** is a calendar month in the user's timezone. An entry falls in the month of its transaction date, per 02.FS.12.
02. **SP.02 the balance sheet date** is the end of the last day of the month. The current month's balance sheet stands at the end of today and is marked incomplete.
03. **SP.03 the year view** shows the twelve months of a calendar year, preceded by the December of the year before as an opening column. The income statement adds a year total and a monthly average. The balance sheet equivalent of summary values are the beginning balance at beginning of first month 01 and the ending balance at the end of month 12.
04. **SP.04 the population** is one user's ledger. The income statement holds every income and expense entry of the user. The balance sheet holds every account in net worth. Accounts outside net worth, such as counterparties the user tracks but does not own, stay off the balance sheet, and their movements appear in [Net worth movement](#net-worth-movement).
05. **SP.05 transfers and opening balances** never reach the income statement, per AR.09 and AR.10.
06. **SP.06 a closed month** reads its current snapshot version, and the current month is month to date, built on request, per the financial statements milestone of the **release milestones**.
07. **SP.07 zero lines.** Every active category, subcategory and account shows a line in each view, at 0.00 when nothing moved, per 02.FS.13. A retired one shows only in a view where its amount is non-zero.

## Statement data model

A statement build writes a snapshot version, per the financial statements milestone of the **release milestones**. The version holds the lines of both statements in two tables: detail lines, read from the ledger, and summary lines, computed from the detail lines. Neither table holds a label, an order, a level or a rendered sign. Those belong to the [Presentation view](#presentation-view).

| id    | line kind | computed from                              | table         |
| ----- | --------- | ------------------------------------------ | ------------- |
| SM.01 | detail    | the ledger entries or balance of one item  | detail lines  |
| SM.02 | total     | the sum of the lines beneath it            | summary lines |
| SM.03 | derived   | a formula or a measure across the sections | summary lines |

Every line of this doc is one of the three kinds.

| id    | line                                       | kind    | key   |
| ----- | ------------------------------------------ | ------- | ----- |
| SL.01 | subcategory line                           | detail  | LK.04 |
| SL.02 | retirement fund line, RC.04                | detail  | LK.05 |
| SL.03 | account line                               | detail  | LK.06 |
| SL.04 | transfer route line, CT.03                 | detail  | LK.08 |
| SL.05 | forex of an account                        | detail  | LK.09 |
| SL.06 | category line                              | total   | LK.03 |
| SL.07 | section total, IS.01 to IS.05              | total   | LK.02 |
| SL.08 | subsection total, one per account type     | total   | LK.07 |
| SL.09 | NW.01 to NW.06                             | total   | LK.01 |
| SL.10 | SB.01 to SB.05, PI.01 to PI.06             | derived | LK.01 |
| SL.11 | TE.01 to TE.04, RC.01 to RC.03             | derived | LK.01 |
| SL.12 | NM.01 to NM.06, CT.01, CT.02 and CT.04     | derived | LK.01 |

The detail lines table holds one row per detail line.

| id    | column           | value                                                  |
| ----- | ---------------- | ------------------------------------------------------ |
| DL.01 | snapshot version | the version the line belongs to                        |
| DL.02 | statement        | `is` or `bs`                                           |
| DL.03 | line key         | LK.04, LK.05, LK.06, LK.08 or LK.09                    |
| DL.04 | subcategory      | the subcategory of a subcategory line                  |
| DL.05 | account          | the account of an account, fund or forex line          |
| DL.06 | counter account  | the receiving account of a route, DL.05 its sender     |
| DL.07 | amount           | signed, in the reporting currency                      |
| DL.08 | account amount   | signed, in the account currency, for a foreign account |
| DL.09 | forex inputs     | B_r, T_r and E_r, for a forex line                     |

The summary lines table holds one row per total and derived line.

| id    | column           | value                             |
| ----- | ---------------- | --------------------------------- |
| SU.01 | snapshot version | the version the line belongs to   |
| SU.02 | statement        | `is` or `bs`                      |
| SU.03 | line key         | LK.01, LK.02, LK.03 or LK.07      |
| SU.04 | kind             | total or derived                  |
| SU.05 | amount           | signed, in the reporting currency |

01. **one version, one month.** A snapshot version covers one month, so each line has one amount. A figure that spans months, such as a year total, a monthly average or TE.05, is a view line, computed from the current versions of the months in the view and never stored.
02. **totals and derived lines are stored.** A stale comparison and CK.02 then run line by line on stored values, with no recomputation at read.
03. **zero lines are stored.** Every active item has a detail row in every version, at 0.00 when nothing moved, per SP.07, so a stale comparison sees a line move from zero.
04. **ids, not names.** A detail row names its subcategory or account by id. The view reads the current name, so a renamed category keeps its line.
05. **month to date** builds the same two tables in memory and stores neither.
06. the data model topic, 04.05, sets the column types, keys and constraints.

## Income statement

### Income statement layout

The income statement view reads top to bottom as six blocks, with the summary block first. Each row is a line of the [Statement data model](#statement-data-model) or a view line of the [Presentation view](#presentation-view).

```text
Income statement
│
├── Summary
│   ├── net income
│   ├── cash savings
│   ├── gross savings
│   ├── investment P and L
│   └── forex gain or loss
│
├── Investment P and L
│   ├── cash profit and loss
│   ├── mark to market liquid
│   └── mark to market illiquid
│
├── Personal income
│   ├── retirement contributions
│   ├── total cash income
│   ├── taxes paid
│   ├── net salary less retirement contributions
│   ├── gross salary
│   │   ├── base salary
│   │   └── bonus
│   ├── part-time
│   └── other income
│
├── Total expenses
│   ├── rental
│   ├── COLE ex rent
│   ├── discretionary
│   └── lifestyle factor
│
├── Expense detail
│   └── each expense category, its subcategories beneath it
│
└── Retirement contributions  [informational]
    ├── employee contribution
    ├── employer contribution
    └── one line per retirement fund account
```

### Income statement sections

Every income and expense entry reaches exactly one detail line, its subcategory, through the two levels of the category model: category and subcategory. The statement section groups categories for presentation. 

all show up in net income

| id    | section            | key             | category kind   | 
| ----- | ------------------ | --------------- | --------------- | 
| IS.01 | personal income    | `personal`      | income, expense | 
| IS.02 | investment P and L | `investment`    | income, expense | 
| IS.03 | rental             | `rental`        | expense         | 
| IS.04 | COLE ex rent       | `cole`          | expense         | 
| IS.05 | discretionary      | `discretionary` | expense         | 

01. **each category carries one section.** The section is a required attribute of the category, so every entry reaches a line by constraint.
02. **IS.01** holds the income categories of personal income and the expense category taxes. **IS.02** holds the investment income categories and any loss expense category the accounts topic, 04.06, adds under AR.13.
03. **a subcategory line** is the sum of the reporting amounts of the entries on that subcategory in the period.
04. **a category line** is the sum of its subcategory lines, exactly, per 02.FS.03. A section total is the sum of its category lines.
05. **order.** Sections follow the layout. Categories follow the category model's order within a section, and subcategories follow theirs beneath a category.
06. **the derived lines** of the summary, personal income and total expenses blocks are formulas over section totals and subcategory lines, defined below. The forex gain or loss is the one derived line with no entries behind it.

### Summary block

Every summary line is derived. Amounts are signed: income positive, expenses negative.

| id    | line               | formula                                          |
| ----- | ------------------ | ------------------------------------------------ |
| SB.01 | net income         | SB.03 + SB.04 + SB.05                            |
| SB.02 | cash savings       | SB.03 - PI.01                                    |
| SB.03 | gross savings      | PI.04 + TE.01                                    |
| SB.04 | investment P and L | the IS.02 section total                          |
| SB.05 | forex gain or loss | the sum of FX for every foreign currency account |

01. **SB.01 net income** is the change in net worth the period's income, expenses and exchange rates produced. It equals the sum of every income and expense entry in the period plus SB.05.
02. **SB.02 cash savings** is the part of gross savings the user can spend. It removes the retirement contributions, which land in retirement funds.
03. **SB.03 gross savings** is personal income less total expenses, the savings from earning and spending before any investment result.
04. **SB.05** is defined in [Currency translation and forex](#currency-translation-and-forex). Its drill down opens the forex breakdown, PG.27 of the **front end pages**.

### Investment P and L

Section IS.02 has three categories, one per P and L component. Its categories and subcategories are seeded for each user.

| id    | category                | subcategory              | definition                         |
| ----- | ----------------------- | ------------------------ | ---------------------------------- |
| IP.01 | cash profit and loss    | dividends                | dividends paid in cash             |
| IP.02 | cash profit and loss    | interest                 | interest on cash and bank accounts |
| IP.03 | cash profit and loss    | realised gain or loss    | sale proceeds less cost basis      |
| IP.04 | cash profit and loss    | other investment P and L | broker fees, cash adjustments      |
| IP.05 | mark to market liquid   | unrealised gain or loss  | revaluation of liquid positions    |
| IP.06 | mark to market illiquid | unrealised gain or loss  | revaluation of retirement holdings |
| IP.07 | mark to market illiquid | retirement fund returns  | interest and growth inside a fund  |

01. **IP.02** covers bank interest as well as brokerage interest. RedBooks books all interest as investment income.
02. **IP.03** follows AR.14 of the **accounting rules**. A position closed with no cost basis is a transfer and adds nothing here.
03. **IP.05** follows AR.13, with its entries on an account of type `investment`. **IP.06** takes the same entries on `retirement` accounts.
04. **IP.07** treats every return credited inside a retirement fund as a revaluation, since the user cannot draw it as cash.
05. **gains and losses share a line.** A loss is a negative entry. Where 04.06 posts losses to a separate expense category under AR.13, that category carries section IS.02 and the same component name, and shows as its own category line beside the gain.
06. the IS.02 section total excludes the forex gain or loss on positions, which SB.05 reports in full.

### Personal income

Section IS.01 holds the user's earned income and the taxes on it. The seeded subcategories are the detail lines.

| id    | category                | subcategory           | kind    |
| ----- | ----------------------- | --------------------- | ------- |
| PS.01 | salary                  | base salary           | income  |
| PS.02 | salary                  | bonus                 | income  |
| PS.03 | salary                  | part-time             | income  |
| PS.04 | retirement contribution | employer contribution | income  |
| PS.05 | other income            | rebates               | income  |
| PS.06 | other income            | government payments   | income  |
| PS.07 | other income            | other                 | income  |
| PS.08 | taxes                   | income tax            | expense |
| PS.09 | taxes                   | other tax             | expense |

01. **PS.01** is regular gross pay from the main employer: the whole salary transaction, including the share that lands on retirement fund accounts, per CE.08 of the **accounting rules**.
02. **PS.02** is performance and one-off pay from the main employer, gross. **PS.03** is gross pay from secondary or contract work.
03. **PS.04** is the employer's contribution credited to a retirement fund, a positive income entry on the fund.
04. **PS.05** is cashback and rebates that reverse no single purchase. A refund of a purchase is a positive entry on that purchase's expense subcategory, per AR.06.
05. **PS.06** is government rebates and payouts received as income. **PS.07** is any other personal income.
06. **PS.08** is tax on income paid to the tax authority. A refund is a positive entry on the same subcategory, per AR.06. **PS.09** is any other tax. A government subsidy against tax is a positive entry on PS.09.

The derived personal income lines are formulas over the subcategory lines and the retirement contributions block.

| id    | line                                     | formula                     |
| ----- | ---------------------------------------- | --------------------------- |
| PI.01 | retirement contributions                 | RC.01 + RC.02               |
| PI.02 | total cash income                        | PI.05 + PS.03 + PS.05 to 07 |
| PI.03 | taxes paid                               | PS.08 + PS.09               |
| PI.04 | personal income                          | PI.01 + PI.02 + PI.03       |
| PI.05 | net salary less retirement contributions | PI.06 - RC.01               |
| PI.06 | gross salary                             | PS.01 + PS.02               |

01. **PI.04** equals the IS.01 section total. The formula reorders the same entries into what reaches the bank and what reaches the funds, so PI.04 is also PI.06 + PS.03 + PS.04 + PS.05 to PS.07 + PI.03.
02. **PI.02 total cash income** is the personal income that lands in spendable accounts before tax.
03. **PI.03** is negative, an expense, and the statement shows it under personal income.

### Total expenses

The total expenses block holds the three expense section totals and their ratio.

| id    | line             | formula                                      |
| ----- | ---------------- | -------------------------------------------- |
| TE.01 | total expenses   | TE.02 + TE.03 + TE.04                        |
| TE.02 | rental           | the IS.03 section total                      |
| TE.03 | COLE ex rent     | the IS.04 section total                      |
| TE.04 | discretionary    | the IS.05 section total                      |
| TE.05 | lifestyle factor | TE.04 of the period / its share of year COLE |

01. **TE.02 rental** is the fixed committed cost of housing.
02. **TE.03 COLE ex rent** is the recurring spending needed to keep the household's standard of living, rent excluded.
03. **TE.04 discretionary** is spending the user can vary at will.
04. **TE.05 lifestyle factor** is discretionary divided by COLE: the discretionary spending per unit of cost of living, rent excluded. Both are taken as positive amounts. The denominator is always the year's COLE, scaled to the length of the period, so a lumpy COLE month such as an annual insurance premium does not swing a quarter's figure.
    01. **year**: the year's discretionary divided by the year's COLE.
    02. **quarter**: the quarter's discretionary divided by 0.25 times the year's COLE.
    03. **year COLE of the current year** is its COLE to date times 12, divided by the number of months of the year that have started. A closed year uses its actual total.
    04. TE.05 is blank when the year's COLE is zero, and shows to two decimals.
    05. **where it shows**: the year view shows the year figure in the year total column and each quarter's figure in the quarter's last month column, March, June, September and December. The month view of a quarter's last month shows that quarter's figure, and other month views leave it blank.

> **implementation decision** the year COLE of the current year is annualised from its months to date, since RedBooks `0.2.0` has no forecast.

### Expense detail

Each expense category belongs to one section.

| id    | category      | section       |
| ----- | ------------- | ------------- |
| EC.01 | rent          | rental        |
| EC.02 | cole          | COLE ex rent  |
| EC.03 | insurance     | COLE ex rent  |
| EC.04 | discretionary | discretionary |
| EC.05 | projects      | discretionary |
| EC.06 | taxes         | personal      |

Each subcategory is a detail line. The table lists the expense subcategories of the category model.

| id    | category      | subcategory           | covers                                 |
| ----- | ------------- | --------------------- | -------------------------------------- |
| SC.01 | rent          | rent                  | rent on the home                       |
| SC.02 | cole          | food                  | groceries and everyday meals           |
| SC.03 | cole          | transport             | metro and bus fares                    |
| SC.04 | cole          | healthcare            | out-of-pocket medical costs            |
| SC.05 | cole          | grooming              | haircuts and grooming                  |
| SC.06 | cole          | mobile                | mobile phone plan                      |
| SC.07 | cole          | clothing              | clothing and shoes                     |
| SC.08 | cole          | post                  | postage and courier                    |
| SC.09 | cole          | internet              | home internet                          |
| SC.10 | cole          | water                 | home water                             |
| SC.11 | cole          | gas                   | home gas                               |
| SC.12 | cole          | pub other             | other utility charges                  |
| SC.13 | cole          | electricity           | home electricity                       |
| SC.14 | cole          | sundries              | household consumables                  |
| SC.15 | cole          | maintenance           | home repairs and upkeep                |
| SC.16 | cole          | services              | recurring household services           |
| SC.17 | cole          | loss                  | money lost reconcile write off         |
| SC.18 | insurance     | health                | health insurance premiums              |
| SC.19 | discretionary | fitness               | gym, classes protein and sport         |
| SC.20 | discretionary | drinks                | coffee and soft drinks out             |
| SC.21 | discretionary | alcohol               | alcoholic drinks                       |
| SC.22 | discretionary | social                | friends family and dating              |
| SC.23 | discretionary | dating                | dates                                  |
| SC.24 | discretionary | software              | software and app subscriptions         |
| SC.25 | discretionary | ai services           | AI service subscriptions               |
| SC.26 | discretionary | it hardware           | computers, phones, accessories         |
| SC.27 | discretionary | books                 | books                                  |
| SC.28 | discretionary | travel                | trips away from home                   |
| SC.29 | discretionary | education             | courses and tuition                    |
| SC.30 | discretionary | movies music          | films, music and streaming             |
| SC.31 | discretionary | fines                 | fines and penalties                    |
| SC.32 | discretionary | taxi                  | taxis and ride hailing                 |
| SC.33 | discretionary | bike                  | bike hire                              |
| SC.34 | discretionary | professional services | agents, banking and legal fees         |
| SC.35 | discretionary | donations             | donations                              |
| SC.36 | discretionary | pets and plants       | pets and plants                        |
| SC.37 | discretionary | durables              | furniture and appliances               |
| SC.38 | discretionary | cleaning              | cleaning services                      |
| SC.39 | discretionary | gifts                 | gifts to family and friends            |
| SC.40 | projects      | one per project       | spending on a named project            |
| SC.41 | discretionary | massage               | massage and spa                        |
| SC.42 | discretionary | other                 | discretionary spending no line matches |

01. **SC.03 and SC.32** only metro and bus fares are cost of living. Taxis are discretionary.
02. **SC.05** grooming is cost of living, beside out-of-pocket healthcare.
03. **SC.16 and SC.17** are cost of living.
04. **SC.25** covers subscriptions to artificial intelligence (AI) services.
05. **SC.34** holds the card foreign exchange fee of AR.12 item 05 of the **accounting rules**.
06. **SC.40** a project is a bounded piece of spending the user wants to see as one line, such as a home move. Project names stay out of committed docs, per LL.08 of the **lessons learned**.
07. **SC.42** is the explicit subcategory for discretionary spending that no specific subcategory covers. Every entry names its subcategory, so no line is a catch-all computed from what the others leave.
08. **a new subcategory** belongs to a category, which carries its section, so it reaches a section with no further mapping.

### Retirement contributions

This block tracks the contributions to retirement funds. It is informational, and its lines are not added into net income: the employee share is already inside gross salary and the employer share inside PS.04.

| id    | line                  | definition                                         |
| ----- | --------------------- | -------------------------------------------------- |
| RC.01 | employee contribution | salary inflows and transfers into retirement funds |
| RC.02 | employer contribution | the PS.04 subcategory line                         |
| RC.03 | total contributions   | RC.01 + RC.02                                      |
| RC.04 | one line per fund     | the RC.03 amount that landed on that fund          |

01. **RC.01** is the sum of the positive entries on `retirement` accounts that belong to salary transactions, per CE.08, plus transfers into `retirement` accounts from other accounts in net worth, such as a voluntary top-up.
02. **RC.04** shows one line per `retirement` account. The fund lines sum to RC.03 exactly, so the block shows how the contributions split across funds.
03. the block shows only for a user with at least one `retirement` account.

## Balance sheet

### Balance sheet layout

The balance sheet view reads top to bottom as five blocks. Each row is a line of the [Statement data model](#statement-data-model) or a view line of the [Presentation view](#presentation-view).

```text
Balance sheet
│
├── Net worth movement
│   ├── net income
│   ├── opening balances
│   ├── movements outside net worth
│   ├── change in net worth
│   ├── opening net worth
│   └── closing net worth
│
├── Net worth
│   ├── illiquid and retirement
│   └── liquid net worth
│       ├── cash and bank accounts
│       ├── liquid investments
│       └── credit
│
├── Forex gain or loss
│
├── Net cash transfers  [informational]
│   ├── retirement contributions
│   ├── investment buys and sells
│   └── one line per transfer route between currencies
│
└── Account detail
    ├── cash and bank accounts
    │   ├── wallet cash
    │   ├── bank accounts
    │   ├── savings accounts
    │   └── clearing
    ├── credit
    │   ├── credit cards
    │   └── other credit
    ├── liquid investments
    └── illiquid and retirement
```

### Account types

The account type is the balance sheet subsection. Every account in net worth carries one of eight types, and each type belongs to one section. This settles WI.07.

| id    | account type    | section                 | subsection    | roles                         |
| ----- | --------------- | ----------------------- | ------------- | ----------------------------- |
| TY.01 | wallet cash     | cash and bank accounts  | wallet cash   | cash, stored value, e-wallets |
| TY.02 | bank account    | cash and bank accounts  | bank accounts | bank accounts                 |
| TY.03 | savings account | by sign                 | by sign       | cash of an investment account |
| TY.04 | clearing        | cash and bank accounts  | clearing      | cost centers                  |
| TY.05 | credit card     | credit                  | credit cards  | credit cards                  |
| TY.06 | other credit    | credit                  | other credit  | see note 04                   |
| TY.07 | investment      | liquid investments      | none          | see note 05                   |
| TY.08 | retirement      | illiquid and retirement | none          | see note 06                   |

01. **TY.01** holds physical cash and stored value the user owns: transit cards, prepaid cards and e-money wallets.
02. **TY.03** is the cash account of an investment: brokerage cash, peer lending cash and an exchange wallet. Its balance can sit on either side of zero, so its section follows its sign at each balance date. A positive or zero balance sits in cash and bank accounts under savings accounts, and a negative one in credit under other credit. It is the only type whose section depends on its balance.
03. **TY.04** is a cost center. A cost center returns to zero once each split is itemised, per AR.07, but a split whose records span a month end leaves a balance for a few days, and the line shows it.
04. **TY.06** holds every other liability and every claim the user holds on a third party: loans, bill accounts, a household share account, tax payable, security deposits and receivables from friends. Each balance keeps its sign, so a deposit or receivable adds to the section and a loan or bill reduces it.
05. **TY.07** holds the position accounts of investments: brokerage and depository positions, peer lending notes, a precious metal holding and a crowdfunding stake.
06. **TY.08** holds retirement funds and retirement brokerage accounts. A retirement fund that also pays medical bills directly stays `retirement`.

### Net worth movement

The opening block reconciles the two statements.

| id    | line                        | formula                                  |
| ----- | --------------------------- | ---------------------------------------- |
| NM.01 | net income                  | SB.01 of the same month                  |
| NM.02 | opening balances            | opening balance equity entries, see note |
| NM.03 | movements outside net worth | see note 03                              |
| NM.04 | change in net worth         | NM.01 + NM.02 + NM.03                    |
| NM.05 | opening net worth           | NW.01 at the end of the month before     |
| NM.06 | closing net worth           | NM.05 + NM.04                            |

01. **NM.02** is the sum of the opening balance equity entries of AR.10 on accounts in net worth, dated in the month. It is non-zero only in a month where an account enters the books.
02. a reconciled balance point that moves changes the balances it covers. It is not a movement of the month: it rewrites history, and the snapshots it covers go stale, per the financial statements milestone of the **release milestones**.
03. **NM.03** is the net of transfers between accounts in net worth and accounts outside it, on the net worth side, less any income and expense entries posted on accounts outside net worth. It is zero for a user with no accounts outside net worth.
04. **NM.06** equals NW.01 of the same month exactly, per CK.03.

### Net worth and its sections

Each line is the signed sum of the lines beneath it, in the reporting currency.

| id    | line                    | formula                                        |
| ----- | ----------------------- | ---------------------------------------------- |
| NW.01 | net worth               | NW.02 + NW.03                                  |
| NW.02 | illiquid and retirement | TY.08 accounts                                 |
| NW.03 | liquid net worth        | NW.04 + NW.05 + NW.06                          |
| NW.04 | cash and bank accounts  | TY.01, TY.02, TY.04 and TY.03 at or above zero |
| NW.05 | liquid investments      | TY.07 accounts                                 |
| NW.06 | credit                  | TY.05, TY.06 and TY.03 below zero              |

01. **NW.01 net worth** is the sum of the signed balances of every account in net worth, per AR.04 of the **accounting rules**.
02. **NW.03 liquid net worth** is what the user could turn into cash at short notice, net of what they owe.
03. **liability presentation.** Every balance keeps its sign on screen, in the API, in the snapshot and in the CSV export. NW.06 is usually negative and reduces liquid net worth by plain addition. This settles 02.OD.10 and WI.06.

### Net cash transfers

This informational block shows the month's transfers that move value between balance sheet sections or currencies. It never changes net worth.

| id    | line                      | definition                                     |
| ----- | ------------------------- | ---------------------------------------------- |
| CT.01 | retirement contributions  | transfers into TY.08 accounts                  |
| CT.02 | investment buys and sells | transfers between TY.03 and TY.07 accounts     |
| CT.03 | one line per route        | transfers between currencies, per account pair |
| CT.04 | net cash transfers        | CT.01 + CT.02 + the CT.03 lines                |

01. each line is the sum of the receiving side's reporting amounts. A route line names its sending and receiving account, and shows the amount in the sending account's currency beside the reporting amount.
02. **CT.01** counts transfers only. The salary inflows of RC.01 are income and show in [Retirement contributions](#retirement-contributions).
03. a route line shows only in a month with a transfer on that route.

### Account detail

Account detail lists every account in net worth under its section and subsection, in the order of the table in [Account types](#account-types), then in the user's account order. Each account line shows its balance at the date in the reporting currency. A foreign currency account also shows its balance and its currency code. Each subsection and section shows its total in the reporting currency. Its drill down opens the account's ledger for the month, per WF.14.04 of the **workflows**.

## Currency translation and forex

The rate source, its storage and the user's overrides belong to the multi currency and forex topic, 04.08. The rounding of one converted amount follows 02.OD.01 of the **test cases**, set by that topic.

01. **CT rate on a transaction date.** The rate for a currency pair on a date is the user's recorded rate for that date where one exists, and otherwise the stored fetched rate, per AR.12 and 02.FS.07.
02. **income and expense lines** convert each entry at the rate on its transaction date, and round each converted entry to the reporting currency's decimal places before summing. Both entries of an income or expense transaction are in one currency, so they convert to the same amount and still balance. This adopts the assumption of 02.OD.02 in the **test cases**.
03. **a transfer between currencies has one reporting amount.** When either side is in the reporting currency, that side's amount is the transfer's reporting amount. Otherwise the sending side converts at the rate on its date. The receiving side carries the same reporting amount with the opposite sign, so the transfer adds nothing to net income, per AR.09. The ledger keeps both stored amounts, per 02.FS.08.
04. **balance sheet lines** convert each foreign currency balance at the month-end rate, the rate for the last day of the month. The current month uses today's rate.
05. **the forex gain or loss of one account**, for a month, is computed from these reporting amounts.

```text
E_r  = closing balance in the account currency × month-end rate, rounded
B_r  = E_r of the month before; zero in the month the account opens
T_r  = sum of the month's entries on the account in reporting amounts, per 02 and 03
FX   = E_r - B_r - T_r
```

06. **FX is exact by construction.** B_r is the rounded closing value of the month before, and T_r sums rounded entries, so E_r = B_r + T_r + FX to the cent with no residual.
07. **an account in the reporting currency** has FX of zero, since its reporting amounts equal its own.
08. **SB.05** is the sum of FX across every foreign currency account in net worth, cash and positions alike. The balance sheet shows the same figure as its forex gain or loss line. The forex breakdown, PG.27 of the **front end pages**, shows each account's B_r, T_r, E_r, rates and FX, and its rows sum to the line.
09. **never posted.** FX exists only in the statement build and its snapshot, per the response to requirements audit item 01.04.07 in the **release milestones**. The ledger holds no forex entry before or after a build.
10. **a change of reporting currency** rebuilds every line from the ledger with the new pair's rates. Both the opening value of a regenerated year's first month and every FX figure follow from the same rules.

## Presentation view

The presentation view is what the statement page and the CSV export show. A build assembles it from the detail and summary lines of one snapshot version, or of each month's current version for a year view, together with the category model and the account types. The API returns the view rows with signed amounts, and the page and the CSV apply PR.01.

| id    | row field  | value                                                    |
| ----- | ---------- | -------------------------------------------------------- |
| PV.01 | line key   | the key of a data model line, or of a view line          |
| PV.02 | label      | the current name of the item, or the line's name here    |
| PV.03 | level      | the depth of the row in the layout                       |
| PV.04 | parent key | the key of the row it sits under in the layout           |
| PV.05 | row kind   | detail, total, derived or view                           |
| PV.06 | values     | one signed amount per column of the view                 |

01. **PV.07 layout.** Rows follow the layout trees of [Income statement layout](#income-statement-layout) and [Balance sheet layout](#balance-sheet-layout). Detail rows sit under their category, by the category's section, or under their subsection, by the account's type, in the order note 05 of [Income statement sections](#income-statement-sections) and [Account detail](#account-detail) set.
02. **PV.08 one line, more than one row.** A data model line can show in both statements. SB.05 is the income statement's forex gain or loss and the balance sheet's forex gain or loss row.
03. **PV.09 view lines** are computed by the view from the months it shows: the year total, the monthly average, TE.05 for a year or a quarter, and the rate row. They carry row kind `view` and are never stored.
04. **PV.10 drill down** goes from a detail row to its transactions, and from a total or derived row to the rows beneath it.

The presentation rules apply to every row of the view.

01. **PR.01 expense flip.** The income statement shows every expense line, every expense category and section total, and PI.03 taxes paid, as positive amounts. That flip is the last step of rendering the page and the CSV export, per AR.18. Income lines and the mixed derived lines, SB.01 to SB.05, PI.04 and the savings lines, keep their sign.
02. **PR.02 no flip on the balance sheet.** Every balance sheet line shows its signed value, per note 03 of [Net worth and its sections](#net-worth-and-its-sections).
03. **PR.03 decimals.** Amounts show to the reporting currency's decimal places. TE.05 shows two decimals.
04. **PR.04 year view columns.** The income statement year view shows the year total, the monthly average, the December of the year before, and the twelve months. The monthly average is the year total divided by the number of months of the year that have started. The balance sheet year view shows the December of the year before and the twelve months. A rate row above the months shows each month-end rate of every foreign currency the user holds.
05. **PR.05 headings.** Every view states its user, its reporting currency, its period and its source, the snapshot version or month to date, per 02.FS.11 and the **statements skill**.
06. **PR.06 CSV export.** One row per line, in layout order, with the line key, the line label, the level, and one column per period of the view. Values are the rendered figures of PR.01, as decimal strings, per 02.FS.10.

## Line keys

Each line of the data model and each row of the view carries a stable key, so a re-run compares line by line and a stale line names what drifted.

| id    | line kind           | key                                       |
| ----- | ------------------- | ----------------------------------------- |
| LK.01 | derived line        | `is.` or `bs.` and the line id, `is.sb01` |
| LK.02 | section total       | `is.section.<section key>`                |
| LK.03 | category line       | `is.category.<category id>`               |
| LK.04 | subcategory line    | `is.subcategory.<subcategory id>`         |
| LK.05 | retirement fund     | `is.rc04.<account id>`                    |
| LK.06 | account line        | `bs.account.<account id>`                 |
| LK.07 | subsection total    | `bs.subsection.<account type>`            |
| LK.08 | transfer route      | `bs.ct03.<sending id>.<receiving id>`     |
| LK.09 | forex of an account | `bs.fx.<account id>`                      |

01. the ids are the database ids of the user's own records, so a renamed category keeps its key.
02. the detail and summary line tables of the [Statement data model](#statement-data-model) hold each line's other columns. The [Presentation view](#presentation-view) adds the label, level and parent of each row.

## Checks

Every statement build runs these checks. A failed check fails the build with its own named cause, and the snapshot job records the failure, per WF.15 of the **workflows**.

| id    | check                 | pass condition                                      |
| ----- | --------------------- | --------------------------------------------------- |
| CK.01 | rates present         | a rate for every currency, entry date and month end |
| CK.02 | roll-ups              | every total equals the sum of the lines beneath it  |
| CK.03 | book identity         | NM.06 equals NW.01, to the cent                     |
| CK.04 | forex identity        | each account's E_r = B_r + T_r + FX, to the cent    |
| CK.05 | type coverage         | every account in net worth has a type               |
| CK.06 | clearing at month end | each cost center balance listed when non-zero       |
| CK.07 | drill down            | each detail line equals the sum of its transactions |

01. **CK.01** names the missing pair and date in its message.
02. **CK.05** holds by constraint once the data model makes the type required. The check guards a load that bypasses it.
03. **CK.06** never fails. It adds a warning naming each cost center with a non-zero month-end balance, the signal of an unfinished split under AR.07.

## Worked examples

Each example states its inputs, computes every figure from them, and passes the checks above. The amounts are illustrative. Rates are USD to SGD: 1.34000 on 2026-05-31, 1.34500 on 2026-06-15 and 1.35000 on 2026-06-30. The reporting currency is SGD.

#### SX.01 forex for June

Three USD accounts in net worth. The USD bank account repeats 02.FS.06 of the **test cases**.

| id    | account            | B, USD    | entries, USD | E, USD    |
| ----- | ------------------ | --------- | ------------ | --------- |
| FX.01 | USD bank account   | 1,000.00  | -100.00      | 900.00    |
| FX.02 | brokerage cash     | -200.00   | 0.00         | -200.00   |
| FX.03 | brokerage position | 19,750.00 | +250.00      | 20,000.00 |

01. **FX.01** a software expense of USD 100.00 on 2026-06-15. B_r is 1,000.00 × 1.34000 = 1,340.00. T_r is -100.00 × 1.34500 = -134.50. E_r is 900.00 × 1.35000 = 1,215.00. FX is 1,215.00 - 1,340.00 + 134.50 = 9.50.
02. **FX.02** B_r is -268.00, T_r is 0.00, E_r is -270.00, and FX is -2.00. A negative balance loses as the dollar rises.
03. **FX.03** an unrealised gain of USD 250.00 posted on 2026-06-30 under AR.13. B_r is 26,465.00. T_r is 250.00 × 1.35000 = 337.50. E_r is 27,000.00. FX is 27,000.00 - 26,465.00 - 337.50 = 197.50, which equals 19,750.00 × 0.01.
04. SB.05 is 9.50 - 2.00 + 197.50 = 205.00.

#### SX.02 income statement for June

The signed entries of June, in SGD. The salary of 6,000.00 lands 4,800.00 in the bank and 720.00, 240.00 and 240.00 in three retirement funds, per CE.08. The employer contribution of 900.00 lands 540.00, 180.00 and 180.00 in the same funds.

| id    | section       | category                | subcategory             | entry     |
| ----- | ------------- | ----------------------- | ----------------------- | --------- |
| IE.01 | personal      | salary                  | base salary             | +6,000.00 |
| IE.02 | personal      | retirement contribution | employer contribution   | +900.00   |
| IE.03 | personal      | other income            | rebates                 | +20.00    |
| IE.04 | personal      | taxes                   | income tax              | -500.00   |
| IE.05 | investment    | cash profit and loss    | dividends               | +40.00    |
| IE.06 | investment    | mark to market liquid   | unrealised gain or loss | +337.50   |
| IE.07 | rental        | rent                    | rent                    | -1,800.00 |
| IE.08 | cole          | cole                    | food                    | -400.00   |
| IE.09 | cole          | cole                    | transport               | -60.00    |
| IE.10 | cole          | insurance               | health                  | -120.00   |
| IE.11 | discretionary | discretionary           | drinks                  | -45.50    |
| IE.12 | discretionary | discretionary           | software                | -134.50   |

01. **retirement contributions**: RC.01 is 720.00 + 240.00 + 240.00 = 1,200.00. RC.02 is 900.00. PI.01 is 2,100.00.
02. **personal income**: PI.06 gross salary is 6,000.00. PI.05 is 6,000.00 - 1,200.00 = 4,800.00. PI.02 total cash income is 4,800.00 + 20.00 = 4,820.00. PI.03 taxes paid is -500.00. PI.04 is 2,100.00 + 4,820.00 - 500.00 = 6,420.00, which equals the IS.01 section total 6,000.00 + 900.00 + 20.00 - 500.00.
03. **total expenses**: TE.02 is -1,800.00. TE.03 is -400.00 - 60.00 - 120.00 = -580.00. TE.04 is -45.50 - 134.50 = -180.00. TE.01 is -2,560.00. June closes the second quarter, so TE.05 is a quarter figure. With April and May discretionary of 200.00 and 220.00, the quarter's discretionary is 180.00 + 200.00 + 220.00 = 600.00. With a year COLE of 6,960.00, TE.05 is 600.00 / (0.25 × 6,960.00) = 600.00 / 1,740.00 = 0.34.
04. **summary**: SB.03 gross savings is 6,420.00 - 2,560.00 = 3,860.00. SB.02 cash savings is 3,860.00 - 2,100.00 = 1,760.00. SB.04 is 40.00 + 337.50 = 377.50. SB.05 is 205.00, from SX.01. SB.01 net income is 3,860.00 + 377.50 + 205.00 = 4,442.50.
05. **cross-check**: the income entries sum to 7,297.50 and the expense entries to -3,060.00. Their sum, 4,237.50, plus SB.05 is 4,442.50, the same net income.
06. **presentation**: the rendered page shows taxes paid 500.00, rental 1,800.00, COLE ex rent 580.00, discretionary 180.00 and total expenses 2,560.00, per PR.01, while net income reads 4,442.50.

#### SX.03 balance sheet at 2026-06-30

The month-end balances of every account in net worth, with the USD accounts from SX.01.

| id    | account            | type            | balance       | SGD       |
| ----- | ------------------ | --------------- | ------------- | --------- |
| BE.01 | cash wallet        | wallet cash     | 150.00        | 150.00    |
| BE.02 | main bank account  | bank account    | 4,200.00      | 4,200.00  |
| BE.03 | USD bank account   | bank account    | USD 900.00    | 1,215.00  |
| BE.04 | transit card       | wallet cash     | 30.00         | 30.00     |
| BE.05 | cost center        | clearing        | 0.00          | 0.00      |
| BE.06 | main credit card   | credit card     | -1,350.00     | -1,350.00 |
| BE.07 | utility bill       | other credit    | -120.00       | -120.00   |
| BE.08 | rental deposit     | other credit    | 2,000.00      | 2,000.00  |
| BE.09 | friends receivable | other credit    | 80.00         | 80.00     |
| BE.10 | brokerage cash     | savings account | USD -200.00   | -270.00   |
| BE.11 | brokerage position | investment      | USD 20,000.00 | 27,000.00 |
| BE.12 | retirement fund A  | retirement      | 30,000.00     | 30,000.00 |
| BE.13 | retirement fund B  | retirement      | 12,000.00     | 12,000.00 |
| BE.14 | retirement fund C  | retirement      | 8,000.00      | 8,000.00  |

01. **NW.04** cash and bank accounts is 150.00 + 4,200.00 + 1,215.00 + 30.00 + 0.00 = 5,595.00.
02. **NW.06** credit holds BE.06 to BE.10. BE.10 is below zero, so it routes to credit under other credit, per TY.03. Credit cards is -1,350.00, other credit is -120.00 + 2,000.00 + 80.00 - 270.00 = 1,690.00, and NW.06 is 340.00.
03. **NW.05** liquid investments is 27,000.00. **NW.03** liquid net worth is 5,595.00 + 27,000.00 + 340.00 = 32,935.00.
04. **NW.02** illiquid and retirement is 50,000.00. **NW.01** net worth is 82,935.00.
05. had brokerage cash closed at USD 150.00, it would sit in cash and bank accounts under savings accounts at 202.50, and credit would lose its -270.00 line.

#### SX.04 net worth movement for June

May's balance sheet closed at a net worth of 78,592.50. In June the user also sent 100.00 from the main bank account to a counterparty outside net worth.

01. NM.01 net income is 4,442.50, from SX.02. NM.02 opening balances is 0.00. NM.03 is -100.00.
02. NM.04 change in net worth is 4,442.50 + 0.00 - 100.00 = 4,342.50.
03. NM.06 closing net worth is 78,592.50 + 4,342.50 = 82,935.00, which equals NW.01 of SX.03, so CK.03 passes.

#### SX.05 retirement contributions and net cash transfers for June

01. RC.04 from SX.02: fund A 720.00 + 540.00 = 1,260.00, fund B 240.00 + 180.00 = 420.00, fund C 420.00. The three sum to RC.03, 2,100.00.
02. the June contributions are income inflows, so CT.01 retirement contributions is 0.00. A month that books the employee share as transfers into the funds shows it in both RC.01 and CT.01.
03. no buy, sell or transfer between currencies took place, so CT.04 net cash transfers is 0.00. The unrealised gain on the position is income, and it shows in SB.04.

## Decisions settled and handoffs

This doc settles three open inputs.

01. **02.OD.10** and **WI.06** liability presentation: liabilities keep their signed negative values in the API, the snapshot, the screen and the CSV, per note 03 of [Net worth and its sections](#net-worth-and-its-sections). The case catalogue removes 02.OD.10 and keeps the assumption of 02.FS.04 and 02.UI.24 as the expected value.
02. **WI.07** account type grouping: the table in [Account types](#account-types) maps every type to one section, with the brokerage cash sign rule of TY.03.
03. the sections, categories and derived lines of both statements, per this doc.

These decisions rest on other topics. Each topic confirms its part before this topic closes.

| id    | topic                       | handoff                                                   |
| ----- | --------------------------- | --------------------------------------------------------- |
| HO.01 | 04.05 data model            | category section, account type, detail and summary lines  |
| HO.02 | 04.06 accounts              | loss categories under AR.13, balance before a first point |
| HO.03 | 04.08 multi currency, forex | rate rule of 02.OD.02, rounding of 02.OD.01               |
| HO.04 | 04.03 front end pages       | summary blocks first, year view columns, rate row         |
| HO.05 | test cases                  | update 02.FS.01, 02.FS.04, 02.UI.23, 02.UI.24, remove OD  |

01. **HO.01** the category carries a required section of IS.01 to IS.05. The account carries a required type of TY.01 to TY.08 and an in-net-worth flag. The snapshot version holds the detail and summary line tables of the [Statement data model](#statement-data-model).
02. **HO.04** PG.23, PG.25 and PG.26 of the **front end pages** list net worth and net income after the detail. This doc puts the summary blocks first, and adds the monthly average, the opening December column and the rate row.
03. **HO.05** 02.FS.01 holds categories with no section. Its ledger gains sections so its net income also checks SB.01.

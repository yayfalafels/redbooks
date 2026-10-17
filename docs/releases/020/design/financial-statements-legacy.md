# RedBooks 0.2.0 - Legacy Financial Statements

This doc describes how the legacy system turned HomeBudget data into financial statements: the HomeBudget database, the two Google Sheets workbooks, their two-stage category mapping, their account classification and the statements they published. That system is **financial-statements 010**. RedBooks does not build on it. The **financial statements design** stands on its own, and this doc is the reference the **data migration** uses to map the HomeBudget history and to compare migrated figures with the published legacy statements.

## Contents

- [Summary](#summary)
- [References](#references)
- [Pipeline](#pipeline)
- [Category mapping in two stages](#category-mapping-in-two-stages)
- [Account classification](#account-classification)
- [Statement layout](#statement-layout)
  - [Income statement](#income-statement)
  - [Balance sheet](#balance-sheet)
- [Conventions](#conventions)
- [RedBooks counterparts](#redbooks-counterparts)

## Summary

01. **HomeBudget recorded, the workbooks reported.** The user recorded every expense, income and transfer in HomeBudget. The legacy workbooks read monthly feeds of those records, mapped them onto statement lines, and published a monthly income statement and balance sheet in SGD.
02. **two workbooks, two mapping stages.** The **homebudget workbook** mapped each HomeBudget budget, category and subcategory to a GL code, stage 1. The **financial statements workbook** mapped each GL code to a statement line with a COLE flag that set its expense group, stage 2, and classified each account in its `accounts` region.
03. **statements were rollups of the mapped feed.** The `hb_gl` region joined the source feeds with their mapped GL fields. Reconcile regions rolled it up by month, and the `income_statement` and `balance_sheet` regions published the result.
04. **expenses were positive and deducted.** The workbooks held expenses as positive amounts and subtracted them from income.
05. **forex covered USD balances only.** One derived line, M2M USD forex on balances, recognised the translation effect of USD cash balances.
06. **the published samples lag the requirements.** The **fs samples** still group expense detail under personal and household, fill future months with forecasts, and show a reconcile error line. Where the samples and the **fs financial statements** requirements differ, the requirements govern.

## References

- **financial statements design**: [financial-statements.md](financial-statements.md), the RedBooks statements
- **data migration**: [data-migration.md](data-migration.md)
- **homebudget data review**: [homebudget-data-review.md](homebudget-data-review.md)
- **lessons learned**: [easymcf-lessons-learned.md](easymcf-lessons-learned.md)
- **financial-statements 010**: [https://github.com/yayfalafels/financial-statements/](https://github.com/yayfalafels/financial-statements/)
- **fs financial statements**: `financial-statements/docs/releases/010/requirements/financial-statements.md`
- **fs account classification**: `financial-statements/docs/releases/010/requirements/account-classification.md`
- **fs transaction categories**: `financial-statements/docs/releases/010/requirements/transaction-categories.md`
- **fs accounting logic**: `financial-statements/docs/releases/010/requirements/accounting-logic.md`
- **fs forex design**: `financial-statements/docs/releases/010/design/forex.md`
- **fs category translation**: `financial-statements/docs/releases/010/design/category-account-model-translation.md`, a transcription of both workbooks' mapping regions
- **fs workbook guide**: `financial-statements/docs/releases/010/data-sources/financial-statements-gsheet.md`
- **homebudget workbook**: the legacy Google Sheet holding the `cat_map` region, its workbook id in the gitignored `data/gsheets.json` and its region ranges in `financial-statements/gsheet/homebudget-workbook.json`
- **financial statements workbook**: the legacy Google Sheet holding the feed, mapping, reconcile and statement regions, its workbook id in the gitignored `data/gsheets.json` and its region ranges in `financial-statements/gsheet/financial-statements.json`
- **fetch script**: `scripts/fetch_legacy_mapping.py`, which reads the mapping regions read-only into the gitignored `data/legacy-mapping/`
- **fs samples**: `data/financial-statements/20260329-income-statement.*` and `data/financial-statements/20260329-balance-sheet.*`, the published workbook statements as PDF and CSV, gitignored

The **fs samples** hold real figures and account names, so this doc copies their structure and formulas only, per LL.08 of the **lessons learned**.

## Pipeline

The **financial statements workbook** is a staged transformation from monthly source feeds to the published statements, per the **fs workbook guide**.

| id    | stage            | regions                                  |
| ----- | ---------------- | ---------------------------------------- |
| LP.01 | source feeds     | `hb_exp`, `hb_inc`, `hb_xfr`, `stm_txns` |
| LP.02 | transaction map  | `hb_gl`                                  |
| LP.03 | expense rollup   | `reconcile_exp_cost_centers`             |
| LP.04 | statement rollup | `reconcile_fin_stm_summary`              |
| LP.05 | publish P and L  | `income_statement`                       |
| LP.06 | balance inputs   | `balances`, `forex_rates`, `accounts`    |
| LP.07 | balance rollup   | `reconcile_bal_by_acct`                  |
| LP.08 | publish B and S  | `balance_sheet`                          |

01. **LP.01** HomeBudget expenses, income and transfers, plus bank statement transactions normalised and deduplicated before they merged, each at the grain of year, month and account.
02. **LP.02** `hb_gl` carried each source record with its mapped fields: the SGD amount at the month's rate, the GL budget, the GL category and the GL subcategory from stage 1.
03. **LP.03 and LP.04** rolled `hb_gl.amount_SGD` up by month, GL category and GL subcategory, and joined the stage 2 lines. The statement rollup also carried the income, gain and adjustment lines.
04. **LP.06** `balances` held each account's period-end balance, `forex_rates` the monthly SGD rate, and `accounts` the classification of each account.
05. **LP.07** joined balances to `accounts`, converted non-SGD balances at the month's rate, and grouped them by statement bucket and by class.
06. **LP.08** carried net income forward from the income statement into the balance sheet's summary rows.

## Category mapping in two stages

The **fs category translation** documents both stages.

01. **stage 1, `cat_map`.** Each row keyed a HomeBudget budget, category and subcategory to a legacy GL budget group, a GL category and, where the category was blank, a GL subcategory. A few category and subcategory pairs had more than one row, where the mapping differed by budget center.
02. **stage 2, `fin_expense_cat_map`.** Each row mapped a GL category or subcategory to a statement line, the `gl_code`, with a COLE flag. A line with COLE set was cost of living, the rental line was rental, and every other line was discretionary.
03. **the specific row won.** Stage 2 matched a subcategory-level row before the category-level catch-all, so misc discretionary took only the discretionary rows no specific line captured.
04. **many sources, one line.** Several GL codes fed one line: socializing took socializing and dating, PUB water/gas took water, gas and utilities misc, and higher education took the academic program projects.
05. **taxes reduced income.** Income tax, other tax and the government subsidy shared one tax code, which stage 2 kept off the expense lines as a reduction of personal income.
06. **coverage was checked in scope.** An unmapped category raised a validation error only when it appeared on transactions in the period, and a missing `gl_code` blocked the income statement rollup.
07. **the GL budget groups** split personal, household and taxes spending, the source of the personal and household grouping the **fs samples** still show. Decision TC-01 of the **fs transaction categories** retired that grouping in favour of the rental, COLE and discretionary groups.

## Account classification

The `accounts` region gave each HomeBudget account an id, a type, an owner, a currency and its statement account. Its type is the asset subcategory of the **fs account classification**.

| id    | asset subcategory | balance sheet section   |
| ----- | ----------------- | ----------------------- |
| LA.01 | wallet cash       | cash and bank accounts  |
| LA.02 | bank account      | cash and bank accounts  |
| LA.03 | savings account   | cash and bank accounts  |
| LA.04 | credit card       | credit                  |
| LA.05 | other credit      | credit                  |
| LA.06 | investment        | liquid investments      |
| LA.07 | retirement        | illiquid and retirement |

01. **the brokerage cash sign rule.** Brokerage cash was cash and bank when its balance was positive and credit when negative, the one balance-dependent placement.
02. **credit extended to third parties** was other credit, such as the household settlement account and tax payable.
03. **the cost center** sat outside the registry. It closed to zero every month, so the balance sheet left it off.
04. **accounts outside the registry**, such as foreign cash wallets, gift balances, loans and counterparties, stayed off the statements.
05. **the live region governs.** The **fs category translation** transcribes an earlier copy of 28 rows. The live region holds 29.

## Statement layout

### Income statement

The **fs financial statements** set seven sections, in this order. Net income was derived after them.

| id    | section                    | effect                    |
| ----- | -------------------------- | ------------------------- |
| LS.01 | personal income            | increases net income      |
| LS.02 | CPF contributions tracking | informational, no effect  |
| LS.03 | investment P and L         | either sign               |
| LS.04 | forex M2M on balances      | either sign               |
| LS.05 | rental expenses            | decreases net income      |
| LS.06 | COLE expenses              | decreases net income      |
| LS.07 | discretionary expenses     | decreases net income      |

01. **LS.01** base salary, bonus, part-time, other income and the CPF employer contribution, less taxes paid, gave net personal income.
02. **LS.02** showed the CPF employee contribution and its allocation to the Ordinary, Special and Medisave accounts. The workbook booked the employee share as a transfer from the salary account, so the block had no income statement effect.
03. **LS.03** held mark to market on liquid and illiquid accounts and cash profit and loss from dividends, interest and broker cash. Mark to market was posted at the statement layer with no HomeBudget record behind it.
04. **LS.04** was one derived line, the rate change applied to USD cash balances.
05. **LS.05 to LS.07** each listed its `gl_code` lines and a section total. Net income was net personal income plus investment P and L plus forex, less the three expense totals.

The **fs samples** open with summary rows, net income, cash savings and gross savings, before the sections. They show a lifestyle factor, discretionary over a full-year COLE that included forecast months, in each quarter's last month column.

### Balance sheet

Net worth was the header figure, the sum of four sections: cash and bank accounts, credit, liquid investments, and illiquid and retirement. Each section listed one line per account. A net cash transfers block below them showed the month's transfers between accounts and the investment buys and sells, with no effect on net worth. The **fs samples** add a reconcile error line, the gap between net income and the change in net assets, and a USD rate row.

## Conventions

01. **signs.** Expenses were positive amounts and were deducted. Liabilities carried negative balances, as HomeBudget holds them.
02. **retirement contributions.** The gross salary landed as income on the salary account, and the employee CPF contribution then moved to the CPF accounts as a transfer.
03. **forex.** Only USD cash balances were marked to market for forex. Positions were revalued by mark to market, which mixed the forex effect into investment P and L.
04. **stored value and brokerage cash.** The **fs samples** list stored-value cards and brokerage cash under misc credit. The `accounts` region and the **fs account classification** place stored value in wallet cash and brokerage cash by its sign.
05. **forecast columns.** The **fs samples** fill future months with forecast values.
06. **reconcile error.** The workbook rebuilt net income and the change in net assets from different regions, and showed their gap as its own line.

## RedBooks counterparts

Each legacy element has a counterpart in the **financial statements design**. The **data migration** relies on this table to compare migrated statements with the **fs samples**.

| id    | financial-statements 010         | RedBooks                              |
| ----- | -------------------------------- | ------------------------------------- |
| FM.01 | income statement summary rows    | income statement summary block        |
| FM.02 | income statement sections        | statement sections IS.01 to IS.05     |
| FM.03 | expense `gl_code`                | subcategory                           |
| FM.04 | `category_group_key`             | the statement section of a category   |
| FM.05 | income type                      | personal income subcategory           |
| FM.06 | P and L component                | investment P and L category           |
| FM.07 | M2M USD forex                    | forex gain or loss                    |
| FM.08 | CPF contributions tracking       | retirement contributions              |
| FM.09 | asset subcategory                | account type                          |
| FM.10 | balance sheet asset type         | balance sheet section                 |
| FM.11 | net assets and liquid net assets | net worth and liquid net worth        |
| FM.12 | cash transfers                   | net cash transfers                    |
| FM.13 | reconcile error                  | identity check, zero by construction  |
| FM.14 | IBKR cash sign rule              | brokerage cash sign routing           |
| FM.15 | cost center `TWH - Personal`     | clearing account type                 |
| FM.16 | `cat_map` and `fin_exp_cat_map`  | mapping rules CR.01 to CR.07          |

01. **FM.03** RedBooks keeps finer subcategories than the `gl_code` lines, such as social and dating under the socializing line. The legacy line crosswalk of the **data migration** maps each one back.
02. **FM.07** RedBooks computes forex for every foreign currency account in net worth, positions included, so a migrated month's investment P and L and forex differ from the legacy split even where net income agrees.
03. **FM.08** RedBooks posts the gross salary as income on the accounts it lands in, so the employee share reaches the funds as income, not as a transfer. Gross salary and net income are the same either way. The **data migration** sets how the transfer pattern of the account `01` history loads.
04. **FM.13** RedBooks builds both statements from one ledger, so it has no reconcile error line, and a non-zero gap fails the build.
05. **FM.16** the **data migration** restates the two stages as one-hop rules for the account `01` history.

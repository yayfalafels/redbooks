# RedBooks 0.2.0 - Front End Pages

This document defines every page of the RedBooks `0.2.0` web app, with its purpose, phone layout, fields, actions, navigation and the API calls it makes. It is design topic 04.03 of the **release milestones** and carries out each step of the **workflows** on a phone screen. The **api endpoints** topic, 04.15, fixes the request and response of each call named here.

## Summary

01. **thirty-two pages in four tabs.** A bottom tab bar holds Accounts, Transactions, Statements and More. The account list is the home page.
02. **one add button on every page.** A floating add button above the tab bar opens a sheet with expense, income and transfer. Recording an expense is the add button, expense, a subcategory, an amount and save.
03. **one phone layout, a 390 pixel wide column.** Every page is a single column with a sticky header, the content, and the tab bar. On a desktop width the same column centres at 640 pixels. No page scrolls sideways. The year views scroll their twelve month columns inside the table, with the line labels fixed.
04. **lists open details, details open forms.** Every list row opens its detail page. Every detail page links to the account, category and subcategory it shows, and offers edit and delete. A save or delete returns to the list the user came from.
05. **the page address holds the view.** Month, year and filters live in the URL query, so back, refresh and bookmarks restore the view, and a statement line opens a filtered transaction list by link.
06. **shared components keep money consistent.** One amount display, one amount input, one currency and rate group, one month picker and one confirmation dialog serve every page.
07. **statements show where their figures come from.** Every statement view names its source, a snapshot version with its run time or month to date. A stale snapshot marks its month and each line that drifted, with the snapshot amount, the current amount and the difference, and offers view changes and re-run.
08. **every page has four states.** Loading, empty, error and populated, per 02.FE.04 of the **test strategy**.

## Contents

- [Summary](#summary)
- [References](#references)
- [Page inventory](#page-inventory)
- [App shell and navigation](#app-shell-and-navigation)
- [Shared components](#shared-components)
- [Sign-in and menus](#sign-in-and-menus)
- [Accounts](#accounts)
- [Transactions](#transactions)
- [Categories](#categories)
- [Currencies and rates](#currencies-and-rates)
- [Financial statements](#financial-statements)
- [Refresh after writes](#refresh-after-writes)
- [API calls](#api-calls)
- [Traceability](#traceability)

## References

- **release notes**: [020-release.md](../020-release.md)
- **release milestones**: [020-release-milestones.md](../020-release-milestones.md)
- **workflows**: [workflows.md](workflows.md)
- **data flows**: [data-flows.md](data-flows.md)
- **accounting rules**: [accounting-rules.md](accounting-rules.md)
- **lessons learned**: [easymcf-lessons-learned.md](easymcf-lessons-learned.md)
- **test strategy**: [test-strategy.md](test-strategy.md)
- **test cases**: [test-cases.md](test-cases.md)
- **api endpoints**: the API endpoints design doc, topic 04.15 of the **release milestones**
- **react skill**: [../../../../.claude/skills/react/SKILL.md](../../../../.claude/skills/react/SKILL.md)

The examples use hypothetical account names at real Singapore institutions, per LL.08 of the **lessons learned**.

## Page inventory

| id    | page                      | route                                  | tab          | workflows    |
| ----- | ------------------------- | -------------------------------------- | ------------ | ------------ |
| PG.01 | sign-in                   | `/signin`                              | none         | WF.01        |
| PG.02 | more menu                 | `/more`                                | More         | WF.02 to 05  |
| PG.03 | account list              | `/accounts`                            | Accounts     | WF.04, WF.09 |
| PG.04 | account detail            | `/accounts/:id`                        | Accounts     | WF.04        |
| PG.05 | account form              | `/accounts/new`, `/accounts/:id/edit`  | Accounts     | WF.04        |
| PG.06 | account ledger            | `/accounts/:id/ledger?month=`          | Accounts     | WF.11        |
| PG.07 | transaction list          | `/transactions?...`                    | Transactions | WF.12, WF.13 |
| PG.08 | add sheet                 | overlay on any page                    | any          | WF.06 to 08  |
| PG.09 | expense form              | `/expenses/new`, `/expenses/:id/edit`  | any          | WF.06, WF.09 |
| PG.10 | expense detail            | `/expenses/:id`                        | any          | WF.10        |
| PG.11 | income form               | `/income/new`, `/income/:id/edit`      | any          | WF.07        |
| PG.12 | income detail             | `/income/:id`                          | any          | WF.10        |
| PG.13 | transfer form             | `/transfers/new`, `.../:id/edit`       | any          | WF.08, WF.09 |
| PG.14 | transfer detail           | `/transfers/:id`                       | any          | WF.10        |
| PG.15 | statements home           | `/statements`                          | Statements   | WF.13 to 17  |
| PG.16 | not found                 | any unknown route                      | none         | none         |
| PG.17 | category list             | `/categories`                          | More         | WF.05        |
| PG.18 | category detail           | `/categories/:id?month=`               | More         | WF.05        |
| PG.19 | subcategory detail        | `/subcategories/:id?month=`            | More         | WF.05        |
| PG.20 | category form             | `/categories/new`, `.../:id/edit`      | More         | WF.05        |
| PG.21 | currencies                | `/currencies`                          | More         | WF.02        |
| PG.22 | exchange rates            | `/rates?pair=&month=`                  | More         | WF.03        |
| PG.23 | income statement year     | `/statements/income?year=`             | Statements   | WF.13        |
| PG.24 | income statement month    | `/statements/income/:month`            | Statements   | WF.13        |
| PG.25 | balance sheet year        | `/statements/balance?year=`            | Statements   | WF.14        |
| PG.26 | balance sheet month       | `/statements/balance/:month`           | Statements   | WF.14        |
| PG.27 | forex breakdown           | `/statements/balance/:month/forex`     | Statements   | WF.14        |
| PG.28 | statement history         | `/statements/history`                  | Statements   | WF.17        |
| PG.29 | snapshot versions         | `/statements/history/:month?currency=` | Statements   | WF.17        |
| PG.30 | snapshot changes          | `/statements/changes/:month?currency=` | Statements   | WF.16        |
| PG.31 | reporting currency change | `/currencies/reporting`                | More         | WF.18        |
| PG.32 | settings                  | `/settings`                            | More         | WF.19        |

01. **PG.20** serves both categories and subcategories. Its routes are `/categories/new`, `/categories/:id/edit`, `/subcategories/new?category=` and `/subcategories/:id/edit`.
02. **PG.23 to PG.27** take the query keys `currency` and `version`. Without them a view shows the current version in the current reporting currency, or in the year's only currency.
03. **PG.07** takes the query keys `account`, `category`, `subcategory`, `month`, `from` and `to`. A month is `YYYY-MM` and a date is `YYYY-MM-DD`.

## App shell and navigation

Every page except PG.01 and PG.16 sits in the app shell.

01. **header**: sticky at the top, 56 pixels tall. A back arrow on every page below a tab's first page, the page title, and the user's initials at the right. Tapping the initials opens a menu with the user's name and email and a sign out action.
02. **tab bar**: fixed at the bottom with four tabs, each an icon and a label: Accounts, Transactions, Statements and More. The current tab is highlighted. Tapping a tab opens its first page: PG.03, PG.07, PG.15 and PG.02.
03. **add button**: a round button above the tab bar at the bottom right, on every shell page except the three entry forms. It opens the add sheet, PG.08.
04. **content**: one column with 16 pixel side margins. Lists are full-width rows of at least 48 pixels with a 44 pixel tap target. Amounts sit right-aligned in tabular figures.
05. **desktop width**: the shell centres at 640 pixels wide. The tab bar and the add button stay inside the column.
06. **sign-in guard**: the shell calls `GET /api/me` on load. A 401 records the requested path and opens PG.01, per LL.29 of the **lessons learned**. Any later 401 does the same.
07. **back**: the back arrow returns to the page the user came from, falling back to the tab's first page when the app was opened on a deep link.

## Shared components

| id    | component                | used on                                    |
| ----- | ------------------------ | ------------------------------------------ |
| UC.01 | amount display           | every page with an amount                  |
| UC.02 | amount input             | PG.05, PG.09, PG.11, PG.13, PG.22          |
| UC.03 | currency and rate group  | PG.09, PG.11, PG.13                        |
| UC.04 | month picker             | PG.06, PG.07, PG.18, PG.19, PG.22 to PG.27 |
| UC.05 | year picker              | PG.23, PG.25                               |
| UC.06 | confirmation dialog      | every delete, retire and remove            |
| UC.07 | page states              | every page that loads data                 |
| UC.08 | category picker          | PG.09, PG.11, PG.07                        |
| UC.09 | account picker           | PG.09, PG.11, PG.13, PG.07                 |
| UC.10 | export button            | PG.07, PG.23 to PG.26                      |
| UC.11 | statement source banner  | PG.23 to PG.27                             |
| UC.12 | stale line               | PG.24, PG.26, PG.07                        |
| UC.13 | currency switch          | PG.23, PG.25, PG.28                        |

01. **UC.01 amount display** shows a decimal string from the API to the decimal places of its currency, with thousands separators and the currency code where more than one currency is on screen. Negative values show a minus sign. The income statement pages pass a presentation flag that shows expenses as positive amounts, per AR.18 of the **accounting rules**. Rates show at their stored precision.
02. **UC.02 amount input** opens the decimal keyboard with `inputmode="decimal"`. It holds the typed string and sends it unchanged, per LL.28 of the **lessons learned**. It rejects more decimal places than the currency allows and anything that is not a number, with a message under the field, and blocks the save until fixed. Amounts are typed as positive numbers.
03. **UC.03 currency and rate group** shows the currency picker, the rate and the converted amount.
    01. on a reporting currency account, the picker lists the user's currencies and starts on the account's currency. On a foreign currency account it shows the account's currency, fixed.
    02. when the entered currency differs from the account's currency, the group calls the rate lookup for the date and fills the rate and the converted amount. On a transfer it fills the paired amount.
    03. the user overrides the rate or the converted amount. A typed rate sets the converted amount to the amount times the rate. A typed converted amount sets the rate to the converted amount divided by the amount. The last field the user typed stays as typed.
    04. a change of date or currency fetches the rate again unless the user has overridden it. An override shows a reset link that restores the fetched rate.
    05. a failed lookup shows a message in the group and leaves the rate field open for typing.
04. **UC.04 month picker** shows the month and year with back and next arrows. Tapping the label opens a month and year grid. It writes the `month` query key.
05. **UC.05 year picker** works the same way for a year and writes the `year` query key.
06. **UC.06 confirmation dialog** names what will happen, such as "Delete this expense of SGD 12.50?", with a cancel and a destructive confirm button.
07. **UC.07 page states**: a skeleton while loading, an empty message with the action that fills it, such as "No accounts yet. Add an account.", and an error message with a retry button. A failed refresh keeps the last data on screen with an error banner.
08. **UC.08 category picker** opens a searchable sheet of categories of the record's kind. Picking a category shows its subcategories, and picking one closes the sheet. Retired categories are left out.
09. **UC.09 account picker** opens a sheet of the user's accounts grouped by type, with their currency. Retired accounts are left out.
10. **UC.10 export button** downloads the CSV of the view on screen, with the same query keys. A closed month's file carries the snapshot values and its version time.
11. **UC.11 statement source banner** sits under the header of every statement view. It reads "Snapshot v3, run 1 Jul 2026 00:05" with the run kind, or "Month to date, live". An older version reads "Version 2 of 3, superseded" with a link to the current version. A stale snapshot adds a stale marker with two actions: view changes, which opens PG.30, and re-run, per WF.16.04. Times show in the user's timezone.
12. **UC.12 stale line** shows a line whose current amount differs from its snapshot. The snapshot amount stays in the amount column with a stale dot. A second row beneath it, in small type, shows the current amount and the difference. Tapping the dot opens PG.30 filtered to that line.
13. **UC.13 currency switch** is a segmented control of the reporting currencies a year has snapshots in. It shows only when there are two or more, and writes the `currency` query key.

## Sign-in and menus

### PG.01 sign-in

01. **purpose**: start the OAuth flow, WF.01.
02. **layout**: the RedBooks name and a one-line description centred, with one sign in button below. No shell.
03. **actions**: sign in navigates to `GET /api/auth/signin?next=<path>`.
04. **states**: a failed sign-in returns here with `?error=<cause>`, and the page shows a message that names the cause.
05. **navigation**: after the callback, the backend redirects to the recorded path, or to PG.03.

### PG.02 more menu

01. **purpose**: reach the setup pages.
02. **layout**: a list of rows: Categories, Currencies, Exchange rates, Settings, and Sign out.
03. **navigation**: each row opens PG.17, PG.21, PG.22 or PG.32. Sign out calls `POST /api/auth/signout` and opens PG.01.

### PG.08 add sheet

01. **purpose**: start an entry with one tap, WF.06 to WF.08.
02. **layout**: a bottom sheet with three large rows: Expense, Income and Transfer, in that order.
03. **navigation**: each opens PG.09, PG.11 or PG.13. On an account page the form starts on that account.

### PG.16 not found

01. **purpose**: answer an unknown route.
02. **layout**: a message and a link to the account list. The API prefix never falls through to this page, per LL.18 of the **lessons learned**.

## Accounts

### PG.03 account list

01. **purpose**: the home page. See every account and its balance, WF.04.
02. **layout**: groups by account type, each with its heading and a subtotal in the reporting currency. Each row shows the account name, its currency and its current balance in that currency. A retired group sits collapsed at the bottom. The cost center row carries an open split marker while its balance is other than zero.
03. **actions**: an add account button in the header opens PG.05.
04. **navigation**: a row opens PG.04.
05. **API calls**: `GET /api/accounts?include=balance`.
06. **empty state**: "No accounts yet. Add an account." When the user has no currencies, the message links to PG.21 first.

### PG.04 account detail

01. **purpose**: show one account and reach its ledger, WF.04.
02. **layout**: the name and current balance at the top. Below, the attributes: type, currency, opening balance and date, and status. Then the reconciled balance points, newest first, each with date and amount. Then a View ledger row.
03. **actions**: edit opens PG.05. Delete shows for an account with no posted transactions, and retire for one with posted transactions, both through UC.06. A retired account offers restore.
04. **navigation**: View ledger opens PG.06 for the current month.
05. **API calls**: `GET /api/accounts/:id`, `GET /api/accounts/:id/balance-points`, `DELETE /api/accounts/:id`, `POST /api/accounts/:id/retire`, `POST /api/accounts/:id/restore`.

### PG.05 account form

01. **purpose**: create or edit an account, WF.04.
02. **fields**:
    01. name, required, up to 80 characters, unique among the user's active accounts.
    02. account type, required, from the account types the **data model** seeds.
    03. currency, required, from the user's currencies only. It is fixed on an account with posted transactions.
    04. opening balance, required, a signed amount through UC.02 with a sign toggle for a liability.
    05. opening balance date, required.
03. **actions**: save and cancel. Save returns to the page the form opened from.
04. **API calls**: `GET /api/currencies`, `POST /api/accounts`, `PATCH /api/accounts/:id`.

### PG.06 account ledger

01. **purpose**: review one account's entries for a month with a running balance, WF.11.
02. **layout**: the account name and UC.04 at the top. A balance carried forward row, then one row per entry by date and then by id, oldest first. Each row shows the day, the payee or the other account of a transfer, the subcategory, the signed amount and the running balance. A closing balance row ends the month.
03. **navigation**: a row opens PG.10, PG.12 or PG.14. The account name opens PG.04.
04. **API calls**: `GET /api/accounts/:id/ledger?month=`.

## Transactions

### PG.07 transaction list

01. **purpose**: find transactions by account, category, subcategory and period, and export them, WF.12. It is also the drill down of the income statement month view, WF.13.06.
02. **layout**: a filter bar with chips for account, category and subcategory and UC.04, with a custom range option. Rows newest first, grouped by day, each with the payee or description, the subcategory or the two accounts of a transfer, the account and the signed amount. A footer shows the count and total in the reporting currency.
03. **drill down**: opened from a statement line, the page shows the line's name and the statement total above the list, and the list total equals it.
04. **actions**: UC.10 export.
05. **navigation**: a row opens PG.10, PG.12 or PG.14.
06. **API calls**: `GET /api/transactions?...`, `GET /api/transactions.csv?...`.

### PG.09 expense form

01. **purpose**: record or edit an expense or a refund, WF.06, WF.07 and WF.09.
02. **fields**, in order:
    01. date, required, today by default.
    02. account, required, through UC.09, defaulting to the account last used on this form or the account the user came from.
    03. category and subcategory, required, through UC.08, expense kind.
    04. amount, required, through UC.02.
    05. currency, rate and converted amount, through UC.03.
    06. refund, a toggle, off by default. On, the entry reverses the subcategory.
    07. payee, optional, with suggestions from the user's past payees.
    08. notes, optional.
03. **actions**: save, and save and add another. Save and add another keeps the date and the account and clears the rest. On the cost center account, the form shows the cost center's balance for the date under the account field.
04. **navigation**: save returns to the page the form opened from.
05. **API calls**: `GET /api/accounts`, `GET /api/categories?kind=expense`, `GET /api/rates/lookup?from=&to=&date=`, `POST /api/expenses`, `PATCH /api/expenses/:id`.

### PG.10 expense detail

01. **purpose**: show one expense, and edit or delete it, WF.10.
02. **layout**: the amount and date at the top. Below, the account, category and subcategory, each a link, the payee and the notes. For an entry in another currency, the entered amount and currency, the rate, and the amount in the account's currency.
03. **actions**: edit opens PG.09. Delete through UC.06.
04. **navigation**: the links open PG.04, PG.18 and PG.19. After a delete the app returns to the list the user came from.
05. **API calls**: `GET /api/expenses/:id`, `DELETE /api/expenses/:id`.

### PG.11 income form and PG.12 income detail

PG.11 follows PG.09 with income-kind categories, no refund toggle and no payee. PG.12 follows PG.10. Their calls are `GET /api/categories?kind=income`, `POST /api/income`, `PATCH /api/income/:id`, `GET /api/income/:id` and `DELETE /api/income/:id`.

### PG.13 transfer form

01. **purpose**: record or edit a transfer, WF.08 and WF.09.
02. **fields**, in order:
    01. date, required, today by default.
    02. from account and to account, required and different, through UC.09.
    03. amount on the from side, through UC.02.
    04. for accounts in different currencies, the amount on the to side and the rate, through UC.03. The user types either amount, and the other follows from the rate.
    05. notes, optional.
03. **actions**: save. A to account of the cost center offers save and add expense, which opens PG.09 on the cost center with the same date, per WF.09.
04. **API calls**: `GET /api/accounts`, `GET /api/rates/lookup?from=&to=&date=`, `POST /api/transfers`, `PATCH /api/transfers/:id`.

### PG.14 transfer detail

01. **purpose**: show one transfer, and edit or delete it, WF.10.
02. **layout**: the date, the from and to accounts as links, the amount in each account's currency, the rate for a transfer between currencies, and the notes.
03. **actions**: edit opens PG.13. Delete through UC.06, which states that both sides are removed.
04. **API calls**: `GET /api/transfers/:id`, `DELETE /api/transfers/:id`.

## Categories

### PG.17 category list

01. **purpose**: see the category model, WF.05.
02. **layout**: two groups, Expense and Income. Each category row shows its subcategories nested and indented beneath it. Retired categories sit collapsed at the bottom.
03. **actions**: add category opens PG.20.
04. **navigation**: a category opens PG.18 and a subcategory opens PG.19, both for the current month.
05. **API calls**: `GET /api/categories?include=subcategories`.

### PG.18 category detail

01. **purpose**: show one category and its month totals, WF.05.
02. **layout**: the name and kind, then UC.04, then each subcategory with its total for the month, and the category total.
03. **actions**: edit opens PG.20. Add subcategory opens PG.20 for a new subcategory. Delete or retire through UC.06, per the account rule.
04. **navigation**: a subcategory opens PG.19 for the same month.
05. **API calls**: `GET /api/categories/:id`, `GET /api/categories/:id/totals?month=`.

### PG.19 subcategory detail

01. **purpose**: show one subcategory and its transactions for a month, WF.05.
02. **layout**: the name and its category as a link, then UC.04, then the month's transactions and their total.
03. **actions**: edit opens PG.20. Delete or retire through UC.06.
04. **navigation**: a transaction opens PG.10 or PG.12.
05. **API calls**: `GET /api/subcategories/:id`, `GET /api/transactions?subcategory=:id&month=`.

### PG.20 category form

01. **fields**: for a category, name and kind. For a subcategory, name and parent category of the same kind.
02. **API calls**: `POST` and `PATCH` on `/api/categories` and `/api/subcategories`.

## Currencies and rates

### PG.21 currencies

01. **purpose**: manage the user's currencies and the reporting currency, WF.02.
02. **layout**: a list of the user's currencies, each with code and name. The reporting currency carries a marker.
03. **actions**:
    01. add opens a searchable sheet of catalog currencies the user does not hold, by code or name.
    02. each row's menu offers set as reporting and remove. Set as reporting opens PG.31. Remove asks through UC.06. A 409 response keeps the row and shows the message that names the accounts or the setting that use it.
    03. the reporting currency's row offers regenerate statements, which opens PG.31 at its year list with the currency unchanged.
04. **API calls**: `GET /api/currencies`, `GET /api/currency-catalog`, `POST /api/currencies`, `DELETE /api/currencies/:code`.

### PG.22 exchange rates

01. **purpose**: review stored rates and record a user rate, WF.03.
02. **layout**: a pair filter and UC.04, then rows newest first, each with the date, the pair, the rate and its source, fetched or user. A user rate shows in place of the fetched one, with the fetched rate in small type beneath.
03. **actions**: record rate opens a sheet with pair, date and rate. A user rate's row offers remove through UC.06.
04. **states**: a failed fetch shows a banner and keeps the stored rates listed.
05. **API calls**: `GET /api/rates?pair=&month=`, `POST /api/rates`, `DELETE /api/rates/:id`.

## Financial statements

Every statement view shows the reporting currency in its header, the population and the period it covers, and UC.11. Each offers UC.10. A closed month shows its snapshot version, and the current month shows month to date with an incomplete marker.

### PG.15 statements home

Three rows: Income statement and Balance sheet, opening PG.23 and PG.25 on the current year, and Statement history, opening PG.28. A count of stale months shows beside the history row when there are any.

### PG.23 income statement year

01. **purpose**: the year view of the income statement, WF.13.
02. **layout**: UC.05 and UC.13, then a table. The first column holds the line labels, fixed while the columns scroll sideways inside the table. Then twelve month columns and a year total column. Income lines come first, then expense lines, each category in bold with its subcategories indented beneath it, then a net income line. Expenses show as positive amounts.
03. **markers**: each month heading carries its source: a stale dot for a stale snapshot, and a month to date tag on the current month. A month with no snapshot yet shows a dash until the snapshot job runs.
04. **navigation**: tapping a month heading opens PG.24 for that month and currency.
05. **API calls**: `GET /api/statements/income?year=&currency=`, `GET /api/statements/income.csv?year=&currency=`.

### PG.24 income statement month

01. **purpose**: the month view of the income statement, WF.13 and WF.16.
02. **layout**: UC.04, a back to year link and UC.11, then one column of lines with their amounts for the month, grouped as in PG.23. A stale line shows as UC.12.
03. **actions**: on a stale snapshot, view changes opens PG.30, and re-run asks through UC.06 and lists every later stale month with a checkbox, checked by default. On a closed month, versions opens PG.29.
04. **navigation**: tapping a category or subcategory line opens PG.07 with `category` or `subcategory` and `month` set.
05. **API calls**: `GET /api/statements/income?month=&currency=&version=`, `GET /api/statements/income.csv?month=&currency=&version=`, `POST /api/statements/snapshots/:month/rerun`.

### PG.25 balance sheet year

01. **purpose**: the year view of the balance sheet, WF.14.
02. **layout**: as PG.23. Accounts grouped by asset class with a subtotal per group, each with its month-end balance in the reporting currency, then the forex gain or loss line, then net worth. The month markers follow PG.23.
03. **navigation**: tapping a month heading opens PG.26.
04. **API calls**: `GET /api/statements/balance?year=&currency=`, `GET /api/statements/balance.csv?year=&currency=`.

### PG.26 balance sheet month

01. **purpose**: the month view of the balance sheet, WF.14 and WF.16.
02. **layout**: UC.04, a back to year link and UC.11, then each account's balance at the month end, grouped by asset class. A foreign currency account also shows its balance in its own currency. Then the forex gain or loss line and net worth. A stale line shows as UC.12.
03. **actions**: as PG.24.
04. **navigation**: an account line opens PG.06 for the month. The forex line opens PG.27.
05. **API calls**: `GET /api/statements/balance?month=&currency=&version=`, `GET /api/statements/balance.csv?month=&currency=&version=`, `POST /api/statements/snapshots/:month/rerun`.

### PG.27 forex breakdown

01. **purpose**: explain the forex gain or loss line for a month, WF.14.05.
02. **layout**: UC.11, then one row per foreign currency account with its balance in its own currency, the rates at the start and end of the month with their source, and its share of the gain or loss. The rows sum to the line on PG.26.
03. **API calls**: `GET /api/statements/balance/forex?month=&currency=&version=`.

### PG.28 statement history

01. **purpose**: find any stored statement, WF.17.
02. **layout**: a list of years, newest first, each collapsible. A year with snapshots in one reporting currency expands straight to its months. A year with two or more expands to a row per currency, each expanding to its months. Each month row shows the month, the current version's run time and run kind, the version count and a stale dot.
03. **actions**: a month row opens a sheet with Income statement, Balance sheet and Versions.
04. **navigation**: the sheet opens PG.24 or PG.26 for that month and currency, or PG.29.
05. **API calls**: `GET /api/statements/history`.

### PG.29 snapshot versions

01. **purpose**: list every version of one month in one reporting currency, WF.17.
02. **layout**: the month and currency at the top, then one row per version, newest first, with its version number, run kind, run time, valid from and valid to, and a current tag on the current version.
03. **navigation**: a row opens PG.24 for that version, with a choice of PG.26. An older version opens read-only with its UC.11 banner.
04. **API calls**: `GET /api/statements/snapshots/:month/versions?currency=`.

### PG.30 snapshot changes

01. **purpose**: show what changed in a month since its snapshot ran, WF.16.03.
02. **layout**: UC.11, then a summary of the stale lines with the snapshot amount, the current amount and the difference. Below, the changes, newest first. Each shows the change time, the kind, added, edited or deleted, the record with its date, account and subcategory, and its before and after amounts. Rate and opening balance changes list the same way. For the balance sheet, changes in earlier months that carry into this month sit under their own heading.
03. **filters**: income statement or balance sheet, and one line when opened from UC.12.
04. **actions**: re-run, as PG.24. A record that still exists opens its detail page.
05. **API calls**: `GET /api/statements/snapshots/:month/changes?currency=&statement=&line=`, `POST /api/statements/snapshots/:month/rerun`.

### PG.31 reporting currency change

01. **purpose**: change the reporting currency and choose which past years to regenerate, WF.18.
02. **layout**, as three steps on one page:
    01. **warning**: the change from the current to the new currency, and three statements: statements from now on report in the new currency, past snapshots in the old currency stay in the history, and regenerating years can take a while. A checkbox confirms the user has read them.
    02. **years**: every year with snapshots, newest first, each with a checkbox and a note when it already has snapshots in the new currency. The current year is checked and locked.
    03. **confirm**: a summary of the new currency and the number of months to regenerate, and a confirm button. Confirming asks once more through UC.06.
03. **progress**: after confirming, the page shows the job's progress by month, polling its status, and links to PG.28 when it finishes. A failed month shows its cause and a retry action.
04. **regenerate only**: opened from the reporting currency's row on PG.21, the page skips the warning step and keeps the currency unchanged.
05. **API calls**: `PUT /api/settings/reporting-currency`, `POST /api/statements/regenerate`, `GET /api/statements/jobs/:id`, `GET /api/statements/history`.

### PG.32 settings

01. **purpose**: set the user's timezone, WF.19.
02. **layout**: the timezone row showing the current IANA name, Asia/Singapore by default. Tapping it opens a searchable list.
03. **API calls**: `GET /api/settings`, `PATCH /api/settings`.

## Refresh after writes

After a write, the app reloads every view that shows the changed data, and keeps the input of any form still open, per LL.27 of the **lessons learned**. Each page's data is cached by its API call, and a write invalidates the calls in this table.

| id    | write                          | calls reloaded                                                 |
| ----- | ------------------------------ | -------------------------------------------------------------- |
| RW.01 | expense or income              | accounts, ledger, transactions, totals, statements, history    |
| RW.02 | transfer                       | accounts, ledger, transactions, balance statements             |
| RW.03 | account                        | accounts, ledger, balance statements, pickers                  |
| RW.04 | category or subcategory        | categories, category totals, income statements, pickers        |
| RW.05 | currency or reporting currency | currencies, accounts, statements                               |
| RW.06 | user rate                      | rates, accounts, statements, open rate lookups                 |
| RW.07 | re-run or regenerate           | statements, history, versions, changes                         |
| RW.08 | timezone                       | settings, ledgers, transactions, statements                    |

## API calls

The pages make the calls below, grouped by resource. The **api endpoints** topic, 04.15, fixes each call's request, response, errors and ownership rule, and may rename a path. This table is the frontend's list of what it needs.

| id    | resource          | calls                                                            |
| ----- | ----------------- | ---------------------------------------------------------------- |
| AC.01 | auth and me       | `GET /me`, `GET /auth/signin`, `POST /auth/signout`              |
| AC.02 | currencies        | `GET`, `POST /currencies`, `DELETE /currencies/:code`, catalog   |
| AC.03 | user settings     | `GET`, `PATCH /settings`, `PUT /settings/reporting-currency`     |
| AC.04 | rates             | `GET`, `POST /rates`, `DELETE /rates/:id`, `GET /rates/lookup`   |
| AC.05 | accounts          | CRUD, retire, restore, balance points, ledger                    |
| AC.06 | categories        | CRUD on categories and subcategories, retire, month totals       |
| AC.07 | expenses          | CRUD on `/expenses`                                              |
| AC.08 | income            | CRUD on `/income`                                                |
| AC.09 | transfers         | CRUD on `/transfers`                                             |
| AC.10 | transactions      | `GET /transactions`, `GET /transactions.csv`                     |
| AC.11 | statements        | income and balance, by year or month, CSV, forex breakdown       |
| AC.12 | snapshots         | history, versions, changes, re-run, regenerate, job status       |

Every path sits under the `/api` prefix. Every call sends the session cookie, and amounts and rates travel as decimal strings in both directions.

## Traceability

| id    | criteria                       | pages                          | cases                    |
| ----- | ------------------------------ | ------------------------------ | ------------------------ |
| TR.01 | 09.FE.01 to 09.FE.04           | PG.01, app shell               | 02.UI.01 to 02.UI.03     |
| TR.02 | 17.FE.01 to 17.FE.04           | PG.21                          | 02.UI.04 to 02.UI.07     |
| TR.03 | 17.FE.05, 10.FE.14             | PG.05                          | 02.UI.08                 |
| TR.04 | 17.FE.06, 17.FE.07, 17.FE.09   | PG.22                          | 02.UI.09, 02.UI.10       |
| TR.05 | 17.FE.08, 10.FE.15             | UC.01, UC.02                   | 02.UI.11, 02.UI.20       |
| TR.06 | 10.FE.02                       | PG.03, PG.04                   | 02.UI.12                 |
| TR.07 | 10.FE.03                       | PG.06                          | 02.UI.13                 |
| TR.08 | 10.FE.04                       | PG.07                          | 02.UI.14                 |
| TR.09 | 10.FE.05                       | PG.17 to PG.19                 | 02.UI.15                 |
| TR.10 | 10.FE.06 to 10.FE.09, 10.FE.13 | PG.10, PG.12, PG.14            | 02.UI.16, 02.UI.17       |
| TR.11 | 10.FE.10 to 10.FE.12           | PG.09, PG.11, PG.13, UC.03     | 02.UI.18, 02.UI.19       |
| TR.12 | 10.FE.01                       | every form and detail page     | 02.UI.21                 |
| TR.13 | 10.FE.16                       | refresh after writes           | 02.UI.22                 |
| TR.14 | 11.FE.01 to 11.FE.04           | PG.23, PG.25                   | 02.UI.23 to 02.UI.26     |
| TR.15 | 11.FE.05 to 11.FE.07           | PG.24, PG.26, PG.07, PG.06     | 02.UI.27 to 02.UI.29     |
| TR.16 | 11.FE.08 to 11.FE.10           | PG.25 to PG.27, UC.10          | 02.UI.30 to 02.UI.32     |
| TR.17 | RN.06, 02.FE.04                | app shell, UC.07               | 02.UI.33, 02.UI.34       |
| TR.18 | 11.FE.11 to 11.FE.14           | PG.23 to PG.31, UC.11 to UC.13 | to be added              |
| TR.19 | 09.FE.05                       | PG.32                          | to be added              |

01. **TR.15** 11.FE.07 asks that a month view line open the transactions that make it up. An income statement line opens PG.07, and a balance sheet account line opens the account's ledger, PG.06, for the month, since the account's entries are what make up its balance. The forex line opens PG.27.

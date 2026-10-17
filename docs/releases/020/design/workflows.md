# RedBooks 0.2.0 - Workflows

This document describes every user workflow in the `0.2.0` **release notes**, step by step, with the page each step runs on and the data it reads and writes. It is design topic 04.01 of the **release milestones** and the first stage of the user experience design. The **data flows** follow from it, and the **front end pages** carry out each step on a phone screen.

## Contents

- [Summary](#summary)
- [Inputs from later design topics](#inputs-from-later-design-topics)
- [References](#references)
- [Actors and conventions](#actors-and-conventions)
- [Workflow inventory](#workflow-inventory)
- [Traceability](#traceability)
- [Access and settings](#access-and-settings)
- [Accounts and categories](#accounts-and-categories)
- [Recording transactions](#recording-transactions)
- [Reviewing the books](#reviewing-the-books)
- [Financial statements](#financial-statements)

## Summary

01. **multiple workflows** The workflows run in the web app on a phone: sign-in, currencies, exchange rates, accounts, categories, expenses, income, transfers, split purchases, corrections, the account ledger, the transaction list and the two financial statements. 
02. **recording is the most frequent workflow and takes the fewest taps.** A floating add button on every page offers expense first, and the expense form starts with today's date and the last used account, so an expense is a category, a subcategory, an amount and a save.
03. **every write goes through one ledger service call.** An expense or income writes one record and its ledger entry, a transfer writes its record and both ledger entries, and each runs in one database transaction, per 10.API.02 of the **release milestones**.
04. **a split purchase is recorded by hand as a transfer plus itemised expenses.** The user records one transfer for the statement amount into the cost center, then one expense per category against the cost center. A cost center balance other than zero marks an unfinished split, per AR.07 of the **accounting rules**.
05. **foreign currency entry follows AR.12.** The form fills the rate from the currency model for the entry date, the user can override the rate or the converted amount, and the override stays on that entry.
06. **corrections edit the record in place.** Editing or deleting an expense, income or transfer changes its ledger entries in the same database transaction. Accounts and categories with posted transactions are retired, never deleted.
07. **closed months are reported from stored snapshots, and the current month is live.** On the 1st of every month, in the user's timezone, RedBooks generates and stores the statement snapshot of the month before. Each snapshot holds both statements for one month in one reporting currency. A re-run stores a new version and keeps the old ones, as a slowly changing dimension of type 2, and every report shows the newest version. The current month is a month to date run computed on request and never stored.
08. **a snapshot shows when its month has changed since it was taken.** An edit to a transaction or a rate that a snapshot covers marks it stale. A stale line shows the snapshot amount, the current amount and the difference, and the user can view the changes and re-run the month.
09. **changing the reporting currency is a guarded step.** The user confirms warnings, then picks the past years to regenerate in the new currency. Snapshots in the old currency stay in the history.
10. **HomeBudget stays the daily capture tool through `0.2.0`.** The seed load and the account `01` migration bring its history in, and the reference checks compare RedBooks against the figures the user wrote from the live HomeBudget app.

## Inputs from later design topics

These workflows fix the steps and the data each step uses. The rules behind some steps are settled by later topics, and each step above works for any outcome of them.

| id    | design topic             | decision                                     | steps                |
| ----- | ------------------------ | -------------------------------------------- | -------------------- |
| WI.01 | homebudget data review   | cost center and billing account handling     | WF.09, WF.15, WF.16  |
| WI.02 | homebudget data review   | match key per record kind                    | WF.16.03             |
| WI.03 | data model               | split model for migrated splits              | WF.09, WF.15.03      |
| WI.04 | multi currency and forex | rounding of a converted amount               | WF.06.04, WF.08.04   |
| WI.05 | multi currency and forex | rate for income statement lines              | WF.13.02             |
| WI.06 | financial statements     | balance sheet presentation of liabilities    | WF.14.02             |
| WI.07 | financial statements     | asset class grouping of each account type    | WF.14.02             |
| WI.08 | exchange rate api probe  | rate for a weekend or missing date           | WF.03.05, WF.06.04   |
| WI.09 | homebudget data review   | mapping of refunds and reimbursements        | WF.07, WF.15.03      |

## References

- **release notes**: [020-release.md](../020-release.md)
- **release milestones**: [020-release-milestones.md](../020-release-milestones.md)
- **requirements**: [../../../requirements.md](../../../requirements.md)
- **accounting rules**: [accounting-rules.md](accounting-rules.md)
- **homebudget accounts**: [homebudget-accounts.md](homebudget-accounts.md)
- **lessons learned**: [easymcf-lessons-learned.md](easymcf-lessons-learned.md)
- **test strategy**: [test-strategy.md](test-strategy.md)
- **test cases**: [test-cases.md](test-cases.md)
- **data flows**: [data-flows.md](data-flows.md)
- **front end pages**: [front-end-pages.md](front-end-pages.md)
- **data model**: [data-model.md](data-model.md)

The examples use hypothetical account names at real Singapore institutions, per LL.08 of the **lessons learned**.

## Actors and conventions

01. **user**: a signed-in person who owns their accounts, categories, currencies and transactions. The user works in the web app on a phone through the tunnel, or in the mobile emulator on the laptop.
02. **page ids** such as PG.08 refer to the **front end pages**, and **flow ids** such as DF.05 refer to the **data flows**.
03. **step ids** have the form `WF.<nn>.<nn>`, such as WF.06.03 for the third step of recording an expense.
04. **dates** follow the user's timezone setting, Asia/Singapore by default. A new entry defaults to today in that timezone, every ledger entry carries a calendar date, and a month is a calendar month in that timezone. Times such as a snapshot's run time are stored in UTC and shown in the user's timezone.
05. **amounts** are typed as decimal strings and shown to the decimal places of their currency. Every entry is signed by its contribution to net worth, per AR.01 of the **accounting rules**. A form takes the amount as a positive number and the workflow sets its sign from the event, so a user never types a minus sign.

## Workflow inventory

| id    | workflow                          | pages                  | flows              |
| ----- | --------------------------------- | ---------------------- | ------------------ |
| WF.01 | sign in and sign out              | PG.01                  | DF.01              |
| WF.02 | manage currencies                 | PG.21                  | DF.02, DF.03       |
| WF.03 | review and record exchange rates  | PG.22                  | DF.04, DF.05       |
| WF.04 | manage accounts                   | PG.03 to PG.05         | DF.06              |
| WF.05 | manage categories                 | PG.17 to PG.20         | DF.07              |
| WF.06 | record an expense                 | PG.09, PG.10           | DF.04, DF.08       |
| WF.07 | record income or a refund         | PG.11, PG.12           | DF.04, DF.08       |
| WF.08 | record a transfer                 | PG.13, PG.14           | DF.04, DF.09       |
| WF.09 | record a split purchase           | PG.13, PG.09, PG.03    | DF.08, DF.09       |
| WF.10 | correct or delete a transaction   | PG.10, PG.12, PG.14    | DF.08, DF.09       |
| WF.11 | review an account ledger          | PG.06                  | DF.10              |
| WF.12 | find and export transactions      | PG.07                  | DF.10, DF.12       |
| WF.13 | report the income statement       | PG.23, PG.24, PG.07    | DF.11, DF.12       |
| WF.14 | report the balance sheet          | PG.25, PG.26, PG.27    | DF.11, DF.12       |
| WF.15 | generate monthly snapshots        | none, runs on its own  | DF.16              |
| WF.16 | review and re-run a stale month   | PG.24, PG.26, PG.30    | DF.17, DF.18       |
| WF.17 | browse the statement history      | PG.28, PG.29           | DF.19              |
| WF.18 | change the reporting currency     | PG.31                  | DF.03, DF.18       |
| WF.19 | set the timezone                  | PG.32                  | DF.20              |

The CSV export folder on the local host fills as the user exports. Clearing it is a file system task with no workflow of its own, per the **data flows**.

## Traceability

| id    | release notes section   | workflows                         |
| ----- | ----------------------- | --------------------------------- |
| RN.01 | ledger and transactions | WF.04, WF.06 to WF.12             |
| RN.02 | categories              | WF.05, WF.06, WF.07, WF.13        |
| RN.03 | multiple currencies     | WF.02, 03, 06 to 08, 18           |
| RN.04 | financial statements    | WF.12 to WF.18                    |
| RN.05 | users and login         | WF.01, WF.19                      |
| RN.06 | mobile layout           | WF.01 to WF.14, WF.16 to WF.19    |

The **requirements** list five long-term workflows. `0.2.0` covers recording and classifying transactions on the phone, through WF.06 to WF.10, and reporting financial statements, through WF.13 and WF.14. Recurring bills, statement ingest and statement reconciliation belong to later releases in the **release roadmap**.

## Access and settings

### WF.01 sign in and sign out

The user signs in with OAuth before any other workflow. RedBooks creates the user record on first sign-in. Traces 09.FE.01 to 09.FE.03 and 09.API.01 to 09.API.04.

01. **WF.01.01** the user opens any page. Without a valid session, the app records the requested path and shows the sign-in page, PG.01, per LL.29 of the **lessons learned**.
02. **WF.01.02** the user taps sign in. The browser goes to the OAuth provider, and the user approves.
03. **WF.01.03** the provider returns to the callback. The backend finds the identity, or creates the user and the identity on first sign-in, and starts a session.
04. **WF.01.04** the app returns the user to the path recorded in WF.01.01, or to the account list, PG.03, when none was recorded.
05. **WF.01.05** the header of every page shows the signed-in user. Tapping sign out ends the session and shows PG.01. A later request with the ended session answers 401.

A failed sign-in, such as a denied consent or a provider error, returns to PG.01 with a message that names the cause.

### WF.02 manage currencies

The user keeps their own list of currencies, as in HomeBudget, and sets the reporting currency from it. Traces 17.FE.01 to 17.FE.05 and 17.API.02 to 17.API.05.

01. **WF.02.01** the user opens the currencies page, PG.21, from the More tab. It lists the user's currencies with code and name, and marks the reporting currency.
02. **WF.02.02** to add a currency, the user taps add, searches the catalog by code or name, and picks a currency they do not hold yet. It appears in the list.
03. **WF.02.03** to remove a currency, the user taps remove and confirms. A currency held by an account or set as the reporting currency stays in the list, and the message names the accounts or the setting that use it.
04. **WF.02.04** to change the reporting currency, the user picks one of their currencies, which starts WF.18.

A new user starts with no currencies. The first account form, WF.04, sends the user to PG.21 when the list is empty.

### WF.03 review and record exchange rates

RedBooks fetches each rate once for a currency pair and date and stores it. The user can record a rate of their own, which takes the place of the fetched rate for that pair and date. Traces 17.FE.06, 17.FE.07, 17.FE.09 and AR.12 of the **accounting rules**.

01. **WF.03.01** the user opens the exchange rates page, PG.22, from the More tab. It lists the stored rates by currency pair and date, newest first, with the source of each rate.
02. **WF.03.02** the user filters by pair and by month.
03. **WF.03.03** to record a rate, the user picks the pair and date and types the rate. The list then shows it as a user rate in place of the fetched one.
04. **WF.03.04** a user rate is removed the same way, which returns the pair and date to the fetched rate.
05. **WF.03.05** a rate the forms need and storage lacks is fetched in the background of WF.06 to WF.08. A failed fetch shows a message on the page and keeps the stored rates on screen.

A user rate changes every later conversion for that pair and date, including statements. A rate typed on one transaction stays on that transaction only and leaves this list unchanged.

### WF.19 set the timezone

The user's timezone sets today's date for new entries, the month boundaries of every statement, and the time the monthly snapshot runs. It is a user setting with Asia/Singapore as the default.

01. **WF.19.01** the user opens the settings page, PG.32, from the More tab. It shows the current timezone.
02. **WF.19.02** the user picks a timezone from a searchable list of IANA timezone names and saves.
03. **WF.19.03** new entries default to today in the new timezone, and the next snapshot runs on the 1st in the new timezone. Recorded entry dates are calendar dates and do not move.

## Accounts and categories

### WF.04 manage accounts

The user creates and maintains the accounts the ledger posts to. Traces 10.FE.01, 10.FE.02, 10.FE.14, 10.DB.08 and AR.10 and AR.11 of the **accounting rules**.

01. **WF.04.01** the user opens the account list, PG.03, the home page. Accounts are grouped by account type, each with its current balance in its own currency.
02. **WF.04.02** to create an account, the user taps add and fills in the account form, PG.05: name, account type, currency from the user's currencies, opening balance and opening balance date. The opening balance is the account's first reconciled balance point.
03. **WF.04.03** the opening balance posts against opening balance equity on its date, per AR.10, and the account appears in its group on PG.03.
04. **WF.04.04** tapping an account opens its detail page, PG.04, with its attributes, its current balance, its reconciled balance points, and links to its ledger and an edit action.
05. **WF.04.05** the user edits the name, type or opening balance. The currency is fixed once the account has posted transactions.
06. **WF.04.06** an account with no posted transactions can be deleted after a confirmation. An account with posted transactions is retired instead. A retired account keeps its history, leaves the entry forms, and shows in a retired group at the bottom of PG.03. The user can restore a retired account from PG.04.

> **implementation decision**: in `0.2.0`, each account's reconciled balance point comes from its HomeBudget database through the seed load and the migration, one point per account, and PG.04 lists them read-only. Recording a new balance point in the app belongs with statement reconciliation in `0.4.0`.

### WF.05 manage categories

The user maintains the two-level consolidated category model, categories and their subcategories. Every expense and income belongs to one subcategory. Traces 10.FE.05, 10.API.08 and 10.DB.02.

01. **WF.05.01** the user opens the category list, PG.17, from the More tab. Each category shows its subcategories nested beneath it. Income and expense categories sit in two groups.
02. **WF.05.02** tapping a category opens its detail page, PG.18, with its attributes, an edit action, and its subcategories with their totals for the selected month. The user moves the month back and forward.
03. **WF.05.03** tapping a subcategory opens its detail page, PG.19, with its attributes, an edit action, and its transactions for the selected month with their total.
04. **WF.05.04** the user adds a category or a subcategory with the category form, PG.20. A category takes a name and its kind, income or expense. A subcategory takes a name and its parent category.
05. **WF.05.05** the user renames a category or subcategory, or moves a subcategory to another category of the same kind. Statements and totals regroup on the next view.
06. **WF.05.06** deleting follows the account rule of WF.04.06: a category or subcategory with posted transactions is retired, and leaves the entry form pickers.

## Recording transactions

The three entry forms share one layout: date, account, amount, the fields of the record kind, and notes. Each opens from the floating add button on every page, which offers expense, income and transfer, with expense first. The form starts with today's date and the account last used on that form.

### WF.06 record an expense

Traces 10.FE.12, 10.FE.15, 10.API.09 to 10.API.12, and AR.05 and AR.12 of the **accounting rules**.

01. **WF.06.01** the user taps the add button and picks expense. The expense form, PG.09, opens.
02. **WF.06.02** the user picks the account that paid: any asset or liability, including a card, cash, a deposit, a billing account or the cost center.
03. **WF.06.03** the user picks a category, then one of its subcategories, and types the amount. The amount keyboard shows digits and a decimal point.
04. **WF.06.04** on a reporting currency account, the currency picker lists the user's currencies and starts on the account's currency. Choosing another currency fills the rate from the currency model for the entry date and shows the amount in the account's currency. The user can override the rate or that amount, and the other value follows. On a foreign currency account the currency is fixed to the account's currency.
05. **WF.06.05** the user adds a payee and notes, and saves.
06. **WF.06.06** the backend posts a negative expense entry and a negative entry on the paying account, per AR.05. It stores the entered currency, entered amount and rate on the record. When the entered currency is the account's currency, the rate is 1.
07. **WF.06.07** the app returns to the page the user came from, and every view of the changed account, category and month refreshes, per LL.27 of the **lessons learned**.

A foreign card charge billed above its converted amount is two expenses on the same card: the charge at the converted amount, and the difference as a foreign exchange fee expense, per AR.12 item 05. The user records the fee with WF.06 straight after the charge, and the form keeps the account and date for the second entry.

### WF.07 record income or a refund

Traces 10.FE.12, 10.API.09 and AR.06 and AR.12 of the **accounting rules**.

01. **WF.07.01** the user taps the add button and picks income. The income form, PG.11, opens.
02. **WF.07.02** the user picks the receiving account, a category of kind income and one of its subcategories, and types the amount. Currency entry follows WF.06.04.
03. **WF.07.03** the user adds notes and saves. The backend posts a positive income entry and a positive entry on the receiving account, per AR.06.

A refund reverses the expense category it belongs to. The user records it with the expense form, PG.09, and switches its refund toggle, which posts a positive entry on the expense subcategory and a positive entry on the receiving account. The refund then reduces that subcategory's total on the income statement.

### WF.08 record a transfer

A transfer moves money between two of the user's own accounts and is neither income nor expense. Traces 10.FE.10, 10.FE.11, 10.API.03, 10.API.06 and AR.09 and AR.12 of the **accounting rules**.

01. **WF.08.01** the user taps the add button and picks transfer. The transfer form, PG.13, opens.
02. **WF.08.02** the user picks the from account and the to account, which differ, and types the amount.
03. **WF.08.03** when the two accounts hold the same currency, the amount is the amount on both sides.
04. **WF.08.04** when the two accounts hold different currencies, the user types the amount on either side, sender or recipient. The form fills the rate from the currency model for the transfer date, with the user rate in place of the fetched one where one exists, and fills the paired amount. The user can override the paired amount or the rate, and the other value follows. The override stays on that transfer.
05. **WF.08.05** the user adds notes and saves. The backend writes the transfer and its two ledger entries in one database transaction: a negative entry on the from account and a positive entry on the to account, each in its own account's currency and to its decimal places.

Paying a credit card bill is a transfer from the bank to the card, which brings the card's negative balance back toward zero. Settling a billing account is the same.

### WF.09 record a split purchase

One bank or card statement line covers several kinds of spending. The user records it through the cost center so the paying account still matches its statement line, per AR.07 and CE.02 and CE.03 of the **accounting rules**. Traces 10.API.05 and the split txn scope item of the **release notes**.

01. **WF.09.01** the user records a transfer, WF.08, from the paying account to the cost center for the statement amount.
02. **WF.09.02** the user records one expense, WF.06, against the cost center for each category in the split. After each save the expense form stays open on the cost center with the same date, and shows the cost center's remaining balance for that date.
03. **WF.09.03** a part of the split that is not an expense, such as a security deposit, moves out of the cost center with a transfer to the asset or liability it belongs to.
04. **WF.09.04** the split is finished when the cost center returns to zero. The account list, PG.03, marks the cost center while its balance is other than zero, and its ledger, PG.06, shows the open amount.

### WF.10 correct or delete a transaction

A posted transaction is corrected in place in `0.2.0`. Traces 10.FE.06 to 10.FE.09, 10.FE.13, 10.FE.16, 10.API.02 and 10.API.11.

01. **WF.10.01** the user taps a transaction in a ledger, a transaction list or a statement drill down. Its detail page opens: PG.10 for an expense, PG.12 for income and PG.14 for a transfer.
02. **WF.10.02** the detail page shows every field of the record, the entered amount and currency, and for an entry in another currency the rate and the amount in the account's currency. A transfer shows both accounts, the amount in each account's currency and the rate. Each account, category and subcategory links to its own detail page.
03. **WF.10.03** to edit, the user taps edit, changes fields on the record's form and saves. The backend updates the record and its ledger entries in one database transaction.
04. **WF.10.04** to delete, the user taps delete and confirms. The backend removes the record and its ledger entries together. A transfer always loses both of its entries.
05. **WF.10.05** after a save or delete, the app returns to the list the user came from, with balances and totals refreshed, and fields the user is editing elsewhere keep their input.

> **implementation decision**: AR.16 of the **accounting rules** corrects a posted transaction with a reversing transaction. In `0.2.0` every transaction is a manual entry that no statement has reconciled yet, so an edit in place keeps the books correct and matches HomeBudget. Reversing corrections start with statement reconciliation in `0.4.0`, when a reconciled entry needs a fixed history.

## Reviewing the books

### WF.11 review an account ledger

Traces 10.FE.03, 10.API.04 and AR.11 of the **accounting rules**.

01. **WF.11.01** the user taps an account on PG.03, then the ledger link, or the account line on a balance sheet month view. The account ledger, PG.06, opens on the current month or on the month the user came from.
02. **WF.11.02** the ledger lists the month's entries by date with a running balance, starting from the balance at the end of the month before. Each row shows the date, the payee or the other account, the category, the signed amount and the running balance.
03. **WF.11.03** the user pages back and next, or picks a month.
04. **WF.11.04** tapping a row opens the transaction's detail page, WF.10.

Every balance is the reconciled balance point nearest before the date plus the signed entries between, per AR.11.

### WF.12 find and export transactions

Traces 10.FE.04, the csv export scope item of the **release notes** and 11.API.10.

01. **WF.12.01** the user opens the transactions tab, PG.07. It lists the current month's expenses, income and transfers by date, newest first.
02. **WF.12.02** the user filters by account, category, subcategory, and a month or a custom date range. The filters show above the list and stay in the page address, so a filtered list can be bookmarked and opened from a statement line.
03. **WF.12.03** the list footer shows the count and the total of the filtered transactions, in the reporting currency.
04. **WF.12.04** tapping export downloads a CSV of the filtered list, holding the same rows and values.

## Financial statements

Both statements report in a reporting currency, the user's setting from WF.18. A closed month is reported from its newest snapshot version, and the current month from a month to date run that is computed on request and never stored. Each view shows its population, its period and its source: the snapshot version and its run time, or month to date. Every view exports to CSV. Traces 11.FE.01 to 11.FE.10 and 11.API.01 to 11.API.11.

A **snapshot** is one user's income statement and balance sheet for one month in one reporting currency, with every line amount, the forex gain or loss, net worth, and the rates it used. Its key is the user, the month and the reporting currency. A new snapshot for a key closes the version before it and becomes the current version, per a slowly changing dimension of type 2. Older versions stay stored and can be opened from the history.

### WF.13 report the income statement

01. **WF.13.01** the user opens the statements tab, PG.15, and picks the income statement. The year view, PG.23, opens on the current year in the current reporting currency.
02. **WF.13.02** the year view shows each category with its subcategories beneath it, the amount for each month and the year total. Each closed month comes from its current snapshot version, and the current month is month to date. Expenses show as positive amounts, per AR.18 of the **accounting rules**. The first column stays in place while the twelve months scroll sideways.
03. **WF.13.03** a month column whose snapshot is stale carries a stale marker, and the current month column carries a month to date marker.
04. **WF.13.04** the user moves back and forward a year, or picks a year. A year with snapshots in more than one reporting currency shows a currency switch, and the view starts on the current reporting currency when the year has it.
05. **WF.13.05** tapping a month heading opens the month view, PG.24, for that month. It shows each category and its subcategories with their amounts for the month, and the snapshot version and run time, or the month to date marker.
06. **WF.13.06** the user moves back and forward a month, or returns to the year view.
07. **WF.13.07** tapping a category or subcategory line opens the transaction list, PG.07, filtered to that line and month. Its total equals the line, or for a stale line the list shows the snapshot amount, the current amount and the difference, per WF.16.
08. **WF.13.08** tapping export downloads a CSV of the view on screen. A closed month carries the snapshot's values and its version time, and the month to date view carries the live values.

### WF.14 report the balance sheet

01. **WF.14.01** the user opens the statements tab and picks the balance sheet. The year view, PG.25, opens on the current year.
02. **WF.14.02** the year view shows each account grouped by asset class, with its balance at the end of each month converted with the month-end rate, the forex gain or loss line, and net worth for each month. Closed months come from their snapshots and the current month is month to date, with the markers of WF.13.03.
03. **WF.14.03** year and currency navigation and the month heading tap follow WF.13.04 and WF.13.05. The month view, PG.26, shows each account's balance at the month end, the forex gain or loss and net worth.
04. **WF.14.04** tapping an account line opens that account's ledger, PG.06, for the month.
05. **WF.14.05** tapping the forex gain or loss line opens the forex breakdown, PG.27. It shows each foreign currency account with its balance in its own currency, the rates at the start and end of the month, and its share of the gain or loss.
06. **WF.14.06** tapping export downloads a CSV of the view on screen, per WF.13.08.

### WF.15 generate monthly snapshots

The snapshot job runs inside the backend with no user action. Traces the financial statements milestone of the **release milestones**.

01. **WF.15.01** the job runs when the backend starts and then every hour while it is up. Since RedBooks runs on the laptop, a month whose 1st passed while the app was down is picked up on the next start.
02. **WF.15.02** for each user, the job finds every closed month, in the user's timezone, from the user's first entry to the month before today, that has no snapshot in any reporting currency.
03. **WF.15.03** it generates the snapshot of each such month, oldest first, in the user's current reporting currency, and stores it as the current version with the run kind scheduled.
04. **WF.15.04** each run reaches a terminal status, succeeded or failed, with its original exception recorded on failure, per LL.42 of the **lessons learned**. A failed month is tried again on the next run.

The job never re-runs a month that already has a snapshot, so a stale month waits for the user, per WF.16. A month the user left in an older reporting currency in WF.18 stays as the user chose.

The seed load and the account `01` migration generate a snapshot for every month they load, with the run kind migration. The migration validation checks these snapshots against the HomeBudget reference figures, per the **data flows**.

### WF.16 review and re-run a stale month

A snapshot is stale when something it covers has changed since it ran. Every expense, income or transfer written, edited or deleted with a date in the month marks that month's income statement stale. The same change marks the balance sheet of that month and of every later snapshotted month stale, since their balances carry it forward. A user rate recorded or removed for a date in the month, or an opening balance changed on or before the month end, marks the balance sheet stale the same way. Moving a subcategory to another category marks the income statement of every month with its entries stale.

01. **WF.16.01** a stale month shows a stale marker on the year view, the month view and the history, PG.28.
02. **WF.16.02** on the month view, each stale line shows the snapshot amount, the current amount and the difference. Lines that still agree show as normal.
03. **WF.16.03** tapping view changes opens the snapshot changes page, PG.30. It lists every change made since the snapshot ran that touches the month: each transaction added, edited or deleted with its before and after values and the time of the change, and each rate or opening balance change. For the balance sheet it includes the changes in earlier months that carry into the month.
04. **WF.16.04** tapping re-run asks for confirmation, then generates a new snapshot version of the month in the snapshot's reporting currency with the run kind re-run. When later months are stale from the same changes, the dialog offers to re-run them too, with this month and every later stale month checked.
05. **WF.16.05** the new version becomes the current version, the stale markers clear, and the old version stays in the history.

Any month with a snapshot can be re-run, since any past transaction can be edited.

### WF.17 browse the statement history

01. **WF.17.01** the user opens the history from the statements tab. PG.28 lists the years with snapshots, newest first.
02. **WF.17.02** each year opens to its reporting currencies when it holds snapshots in more than one, and straight to its months when it holds one.
03. **WF.17.03** each month row shows its current version's run time and run kind, its number of versions and a stale marker.
04. **WF.17.04** tapping a month opens its month view for the current version. Tapping versions opens the version list, PG.29, which lists every version of the month and currency with its run time, run kind and validity period.
05. **WF.17.05** tapping an older version opens it read-only in the month view, with a banner that names the version and a link to the current version. It exports to CSV like any other view.

### WF.18 change the reporting currency

Changing the reporting currency changes every statement the user reads from then on, so it runs as a guided step. Traces 17.FE.04 and 17.API.05.

01. **WF.18.01** from the currencies page, PG.21, the user picks set as reporting on one of their currencies. The reporting currency change page, PG.31, opens.
02. **WF.18.02** the page warns that statements from now on report in the new currency, that past snapshots in the old currency stay in the history unchanged, and that regenerating past years can take a while. The user ticks to confirm they have read it.
03. **WF.18.03** the page lists every year with snapshots, newest first, each with a checkbox. The current year is checked and locked, so the year being reported stays in one currency from here on. The user checks how many past years to regenerate.
04. **WF.18.04** the user confirms a second time. RedBooks stores the new reporting currency, then generates a snapshot in the new currency for every closed month of the checked years, with the run kind currency change. Each one becomes the current version of its month in the new currency.
05. **WF.18.05** the page shows the job's progress, and the history shows each regenerated year under both currencies once it is done.

Years left unchecked keep only their old currency snapshots. Their statements open in that currency, labelled with it, and the user can regenerate them later. The reporting currency's row on PG.21 offers regenerate statements, which opens PG.31 at WF.18.03 with the currency unchanged. Each year shows whether it already has snapshots in the reporting currency.

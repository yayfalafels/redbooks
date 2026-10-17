# RedBooks 0.2.0 - Test Cases

This document is the release-level case catalogue for `0.2.0`. It turns the **test strategy** into concrete checks, each with its trace, silo, verification layer, input and expected result, and proves every release notes section at release level. Each feature tracker copies its cases, reconciles them with its design and adds the cases its design reveals, per 02.CS.01 of the **test strategy**.

It is an output of the test strategy and cases milestone, and meets that milestone's cases closure criteria 02.CC.01 to 02.CC.08. The **test strategy tracker** plans and records the work on it.

## Contents

- [References](#references)
- [Open design inputs](#open-design-inputs)
- [Traceability](#traceability)
- [Ledger and money silo](#ledger-and-money-silo)
- [Data model and database silo](#data-model-and-database-silo)
- [Backend API silo](#backend-api-silo)
- [Exchange rates silo](#exchange-rates-silo)
- [Financial statements silo](#financial-statements-silo)
- [Frontend silo](#frontend-silo)
- [Authentication and ownership silo](#authentication-and-ownership-silo)
- [HomeBudget account 02 seed](#homebudget-account-02-seed)
- [HomeBudget account 01 migration](#homebudget-account-01-migration)
- [End-to-end tier](#end-to-end-tier)
- [Environment and validation utilities](#environment-and-validation-utilities)
- [Human validation checklists](#human-validation-checklists)

## References

- **release milestones**: [020-release-milestones.md](../020-release-milestones.md)
- **release notes**: [020-release.md](../020-release.md)
- **test strategy tracker**: [020.02-test-strategy.md](../features/020.02-test-strategy.md)
- **test strategy**: [test-strategy.md](test-strategy.md)
- **accounting rules**: [accounting-rules.md](accounting-rules.md)
- **homebudget accounts**: [homebudget-accounts.md](homebudget-accounts.md)
- **homebudget data review**: [homebudget-data-review.md](homebudget-data-review.md)
- **financial statements design**: [financial-statements.md](financial-statements.md)
- **homebudget snapshot**: the newest dated copy of the account `02` HomeBudget database in the gitignored `data/homebudget-02/` folder

## Open design inputs

The strategy and catalogue come before the design, so some expected values depend on decisions the design makes. Each affected case states its current assumption. The design topic that settles an input updates every case it affects and removes the input from this table before the topic closes, per design closure criterion 15 of the **release milestones**.

| id       | design topic             | open decision                                  | cases affected        |
| -------- | ------------------------ | ---------------------------------------------- | --------------------- |
| 02.OD.01 | multi currency and forex | rounding rule for a converted amount           | 02.LED.04             |
| 02.OD.02 | multi currency and forex | rate used for income statement lines           | 02.FS.06, 02.FS.07    |
| 02.OD.03 | multi currency and forex | precision of a rate derived from an override   | 02.LED.15             |
| 02.OD.04 | users and authentication | session lifetime and cookie settings           | 02.OWN.10, 02.OWN.11  |
| 02.OD.05 | api endpoints            | validation status code and error body shape    | 02.API.01             |
| 02.OD.06 | repo layout, tech stack  | test folder layout and markers                 | all protocols         |
| 02.OD.07 | homebudget data review   | account 02 mapping onto the canonical taxonomy | 02.SEED.03            |
| 02.OD.08 | accounts                 | balance before an account's first point        | 02.LED.06             |
| 02.OD.09 | exchange rate api probe  | rate for a weekend or missing date             | 02.FX.09              |
| 02.OD.10 | financial statements     | balance sheet presentation of liabilities      | 02.FS.04, 02.UI.24    |
| 02.OD.12 | data model               | split model for migrated account `02` splits   | 02.LED.17, 02.SEED.10 |

01. **02.OD.01** the cases assume round half up and state the round half even result beside it.
02. **02.OD.02** the cases assume each income statement line converts at the rate on its transaction date, and the balance sheet converts at the month-end rate.
03. **02.OD.05** FastAPI returns 422 for request validation by default. The cases assume 422 with the failing field named in the body.
04. **02.OD.08** AR.11 of the **accounting rules** sets the balance between and before reconciled balance points. The cases assume a date before an account's first point answers `"0.00"`.
05. **02.OD.09** the cases assume a weekend or missing date takes the last published rate before it. Design task 04.19 probes the real behavior and its saved responses replace this assumption.
06. **02.OD.10** the cases assume the API returns liability balances with their signed negative values. Presentation is a rendering rule, per AR.18.
07. the forex gain or loss is computed when a statement is built and is never posted to the ledger, per the response to requirements audit item 01.04.07 in the **release milestones**. The cases treat this as settled.

## Traceability

Each case id has the form `02.<silo>.<nn>`. Each case traces to a release notes section, a milestone closure criterion, an accounting rule, a strategy rule, or several.

01. release notes sections carry `RN` ids: `RN.01` ledger and transactions, `RN.02` categories, `RN.03` multiple currencies, `RN.04` financial statements, `RN.05` users and login, `RN.06` mobile layout, `RN.07` HomeBudget history, `RN.08` lessons applied.
02. milestone closure criteria carry `<milestone>.<group>.<nn>`. Milestones with database, api and front end sections use `DB`, `API` and `FE`, such as `10.API.09` for the ninth api criterion of txn and accounts. Milestones with one closure list use `CK`, such as `12.CK.04`.
03. accounting rules carry their `AR` ids from the **accounting rules**, such as `AR.11`.
04. strategy rules carry their ids from the **test strategy**, such as `02.CS.03`.
05. a feature tracker copies a case as `<F>.TC.<nn>` and keeps the catalogue id in its scope-item column. Cross-cutting cases stay in the catalogue and run in every feature's regression: 02.OWN.05, 06 and 08, 02.UI.33 and 34, 02.FX.10, 02.SEED.11 and 02.ENV.11.

| id    | release notes section   | milestones      | cases                                                      |
| ----- | ----------------------- | --------------- | ---------------------------------------------------------- |
| RN.01 | ledger and transactions | 10              | 02.LED.06 to 17, 02.DB.07 to 15, 02.API.02 to 13           |
| RN.02 | categories              | 10, 07, 12      | 02.DB.07, 02.API.09, 02.UI.15, 02.SEED.03, 02.MIG.03       |
| RN.03 | multiple currencies     | 17, 10          | 02.LED.01 to 05, 11 to 16, 02.FX.01 to 11, 02.API.14 to 17 |
| RN.04 | financial statements    | 11              | 02.FS.01 to 13, 02.UI.23 to 32, 02.E2E.03, 04              |
| RN.05 | users and login         | 09              | 02.OWN.01 to 12, 02.DB.03, 04, 13, 02.E2E.05               |
| RN.06 | mobile layout           | 06, FE sections | 02.UI.01 to 34, 02.ENV.14, 02.HUM.01 to 06                 |
| RN.07 | HomeBudget history      | 07, 12          | 02.SEED.01 to 24, 02.MIG.01 to 20                          |
| RN.08 | lessons applied         | all             | 02.ENV.01 to 15, 02.SEED.12, 13, 02.E2E.01                 |

## Ledger and money silo

Protocol unit. Pure functions with inline values and a pinned clock. Amounts below are exact and signed, per 02.MN.07. Account names are hypothetical. Every case is decided by the oracle layer.

| id        | trace                      | title                                            |
| --------- | -------------------------- | ------------------------------------------------ |
| 02.LED.01 | RN.03, 02.MN.01            | money type rejects float input                   |
| 02.LED.02 | RN.03, 02.MN.01            | exact decimal addition                           |
| 02.LED.03 | RN.03, 17.API.08           | quantize to currency decimal places              |
| 02.LED.04 | 17.API.08, 02.OD.01        | rounding boundary on conversion                  |
| 02.LED.05 | RN.03                      | arithmetic across currencies rejected            |
| 02.LED.06 | 10.API.04, AR.11, 02.CS.03 | balance from a reconciled balance point          |
| 02.LED.07 | RN.01, AR.03, 02.CS.09     | expense and income entry signs                   |
| 02.LED.08 | RN.01, AR.06               | refund reverses its category                     |
| 02.LED.09 | RN.01, 10.DB.03, AR.09     | transfers between own accounts                   |
| 02.LED.10 | RN.01, AR.08, M2.10        | billing account returns to zero                  |
| 02.LED.11 | 10.API.03, 11.API.08       | transfer between currencies keeps stored amounts |
| 02.LED.12 | 10.DB.04, 10.API.09        | entry in another currency posts converted amount |
| 02.LED.13 | 10.DB.04                   | entry in account currency posts at rate 1        |
| 02.LED.14 | 10.API.09, AR.12           | foreign currency account takes only its currency |
| 02.LED.15 | 10.API.10, 10.FE.12        | override of rate or converted amount             |
| 02.LED.16 | 10.API.12, AR.12           | card fx fee is a separate expense                |
| 02.LED.17 | 10.API.05, AR.07, AR.15    | split purchase through the cost center           |

- **02.LED.01** input `Money(0.1, "SGD")` with a float. Expected: a type error. `Money("0.10", "SGD")` is accepted.
- **02.LED.02** input `Money("0.10", "SGD") + Money("0.20", "SGD")`. Expected `"0.30"` exactly.
- **02.LED.03** input `"12.5"` SGD, `"12.5"` USD, `"1000.4"` JPY. Expected `"12.50"`, `"12.50"`, `"1000"`, using the catalog decimal places of 2, 2 and 0.
- **02.LED.04** input `"10.00"` USD to SGD at rate `1.3445`, raw result 13.445. Expected `"13.45"` under round half up, `"13.44"` under round half even. The case keeps the single value the design picks. A second input at rate `1.34567` gives `"13.46"` under either rule.
- **02.LED.05** input `Money("1.00", "SGD") + Money("1.00", "USD")`. Expected: a currency mismatch error.
- **02.LED.06** input: a reconciled balance point of `"100.00"` SGD on 2026-05-24, an expense entry `"-12.50"` on 2026-05-25 and an income entry `"200.00"` on 2026-06-01. Expected balance `"100.00"` on 2026-05-24, `"87.50"` on 2026-05-25 and on 2026-05-31, `"287.50"` on 2026-06-01. With the only point moved to `"287.50"` on 2026-06-01, the same entries give `"87.50"` on 2026-05-25 and `"100.00"` on 2026-05-24, the point less the entries between. A date before the first point follows 02.OD.08.
- **02.LED.07** input: a purchase of `"12.50"` and a salary of `"200.00"` on an SGD bank account. Expected: the purchase posts `"-12.50"` on the account and `"-12.50"` on its expense category, and the salary posts `"200.00"` on the account and `"200.00"` on its income category. A posting with every sign flipped balances and still fails the case.
- **02.LED.08** input: a `"20.00"` refund for household goods received on a credit card. Expected: `"20.00"` on the card and `"20.00"` on the household category, so spending and the amount owed both fall.
- **02.LED.09** input: a transfer of `"50.00"` SGD from bank account A to bank account B, then a `"50.00"` credit card payment from A. Expected: `"-50.00"` on A and `"50.00"` on B, then `"-50.00"` on A and `"50.00"` on the card. Each pair sums to `"0.00"` and no income or expense entry is written.
- **02.LED.10** input: a `"120.00"` utility bill for March posted to a bill account, paid on 2026-04-10 from a bank account. Expected: `"-120.00"` on the utilities category and on the bill account in March, then `"120.00"` on the bill account and `"-120.00"` on the bank, and a bill account balance of `"0.00"` after the payment. The March income statement holds the expense and April's holds none.
- **02.LED.11** input: a transfer from a USD account to an SGD account with stored amounts `"1000.00"` USD and `"1345.67"` SGD and rate `1.34560`. Expected: entries `"-1000.00"` USD and `"1345.67"` SGD. The SGD amount stays `"1345.67"` even though rate times amount gives 1345.60.
- **02.LED.12** input: an expense of `"10.00"` USD on an SGD reporting currency account at rate `1.34567`. Expected: account entry `"-13.46"` SGD, with nominal currency USD, nominal amount `"10.00"` and rate `1.34567` stored on the expense.
- **02.LED.13** input: an expense of `"10.00"` SGD on an SGD account. Expected: rate `1`, account entry `"-10.00"`.
- **02.LED.14** input: an expense of `"40.00"` USD on a USD account at a fetched rate `1.35`, then an expense in SGD on the same account. Expected: the first posts `"-40.00"` USD to the account ledger, and reports `"-54.00"` SGD only in the expense report total. The second is rejected with a message naming the account currency.
- **02.LED.15** input: the 02.LED.12 expense with the converted amount overridden to `"13.50"`. Expected: account entry `"-13.50"` and rate `1.35`. With the rate overridden to `1.3` instead, expected account entry `"-13.00"`. The stored rate precision follows 02.OD.03.
- **02.LED.16** input: a `"100.00"` USD charge on an SGD credit card at rate `1.35`, billed on the card statement as `"136.50"` SGD. Expected: `"-135.00"` on the travel category, `"-1.50"` on the fx fees category, and `"-136.50"` on the card, matching the statement line.
- **02.LED.17** input: one card statement line of `"40.00"`, moved by transfer to the cost center, then expenses of `"20.00"`, `"15.50"` and `"4.50"` in three subcategories on the cost center. Expected: `"-40.00"` on the card, `"40.00"` then `"-20.00"`, `"-15.50"` and `"-4.50"` on the cost center, a cost center balance of `"0.00"`, and expense entries summing exactly to `"-40.00"`.

## Data model and database silo

Protocol db. A fresh database built by the schema build command, and the database utility, with no FastAPI process. Every case is decided by direct inspection.

| id       | trace              | title                                               |
| -------- | ------------------ | --------------------------------------------------- |
| 02.DB.01 | 07.CK.01, 06.CK.06 | schema build creates the data model schema          |
| 02.DB.02 | 10.DB.05, 17.DB.05 | amounts and rates round-trip unchanged              |
| 02.DB.03 | 09.DB.02           | owner reference required on user-owned tables       |
| 02.DB.04 | 09.DB.01           | user, identity and session constraints              |
| 02.DB.05 | 17.DB.01, 17.DB.02 | user currency references the catalog once           |
| 02.DB.06 | 17.DB.04           | exchange rate unique per pair, date and source      |
| 02.DB.07 | RN.02, 10.DB.02    | two-level category constraints                      |
| 02.DB.08 | 10.DB.01, 10.DB.03 | ledger entry links for expense, income and transfer |
| 02.DB.09 | 10.DB.06           | ledger entry currency matches account currency      |
| 02.DB.10 | 10.DB.07           | account currency held by the owner                  |
| 02.DB.11 | 10.DB.05, 02.MN.01 | no float columns for money                          |
| 02.DB.12 | 11.DB.01           | every account type maps to one balance sheet group  |
| 02.DB.13 | 09.DB.02, 02.CS.06 | cross-owner references rejected                     |
| 02.DB.14 | 10.DB.08           | records with posted history are retired             |
| 02.DB.15 | 10.DB.09           | single-active rules are partial unique indexes      |

- **02.DB.01** input: an empty database and the schema build command, run twice. Expected: the build succeeds both times with an identical schema, and the table list equals the data model doc's table list in both directions.
- **02.DB.02** input: insert amount `"1345.67"` SGD, `"1000"` JPY and rate `1.34567123`. Expected: reads return the same strings exactly.
- **02.DB.03** input: scan the schema for every table outside the catalog, then insert a row with a null owner into each. Expected: every user-owned table has a non-null owner reference and rejects the row.
- **02.DB.04** input: a second identity with the same provider and subject, a second session with the same token hash, then delete a user. Expected: both inserts rejected, and the user's identities and sessions removed with it.
- **02.DB.05** input: a user currency with a code missing from the catalog, then the same catalog currency twice for one user. Expected: both rejected. The same currency for a second user is accepted.
- **02.DB.06** input: two USD.SGD rates for 2026-06-02 with source `fetched`, then one with source `user`, then one with source `other`. Expected: the second fetched row rejected, the user row accepted, the unknown source rejected.
- **02.DB.07** input: a subcategory with no category, and an expense with no subcategory. Expected: both rejected.
- **02.DB.08** input: an expense with two ledger entries, a transfer with one entry, and a transfer whose two entries are on the same account. Expected: all three rejected.
- **02.DB.09** input: a USD ledger entry on an SGD account. Expected: rejected.
- **02.DB.10** input: an account in a currency its owner does not hold, then delete a user currency held by an account. Expected: both rejected.
- **02.DB.11** input: query the column types of every amount and rate column. Expected: every one is `NUMERIC`, with no `real`, `double precision` or `money` column.
- **02.DB.12** input: list the account types and their balance sheet group. Expected: every account type has exactly one group.
- **02.DB.13** input: `bob`'s expense referencing `alice`'s account, and `bob`'s subcategory under `alice`'s category. Expected: both rejected.
- **02.DB.14** input: delete an account and a category that each have posted transactions, then retire them, then delete an account with none. Expected: the deletes with history are rejected, the retired records leave the active lists while their transactions keep them, and the unused account is deleted.
- **02.DB.15** input: every single-active rule the data model names. Expected: each has a partial unique index filtered to the active state, and a second active row is rejected while a second inactive row is accepted.

## Backend API silo

Protocol api. Case files through the FastAPI test client, signed in as `alice` unless a case names `bob`, with the stub rate API in-process.

| id        | trace                | layer          | title                                                |
| --------- | -------------------- | -------------- | ---------------------------------------------------- |
| 02.API.01 | 10.API.01, 17.API.01 | client         | resource case template for every resource            |
| 02.API.02 | 10.API.02            | direct         | ledger writes are atomic                             |
| 02.API.03 | 10.API.02, 10.API.11 | direct         | editing or deleting a transaction updates its ledger |
| 02.API.04 | 10.API.03            | direct, oracle | transfer between currencies stores both amounts      |
| 02.API.05 | 10.API.04            | oracle         | account balance endpoint on a date                   |
| 02.API.06 | 10.API.05            | oracle         | split purchase through the API                       |
| 02.API.07 | 10.API.06            | direct         | transfer rate default, user rate and override        |
| 02.API.08 | 10.API.07            | client         | account accepts only the user's currencies           |
| 02.API.09 | RN.02, 10.API.08     | client         | subcategory ownership and category listing           |
| 02.API.10 | 10.API.09            | oracle         | entries in another currency through the API          |
| 02.API.11 | 10.API.10            | direct         | entry rate default and override                      |
| 02.API.12 | 10.API.12            | direct, oracle | card charge records its fx fee                       |
| 02.API.13 | 10.API.13            | client         | every ledger write goes through the ledger service   |
| 02.API.14 | 17.API.02            | oracle         | currency catalog                                     |
| 02.API.15 | 17.API.03            | client         | add a currency                                       |
| 02.API.16 | 17.API.04            | client, direct | remove a currency                                    |
| 02.API.17 | 17.API.05            | client, direct | reporting currency setting                           |
| 02.API.18 | 10.DB.08             | client, direct | deleting a record with history retires it            |

- **02.API.01** input: for each of accounts, categories, subcategories, expenses, income, transfers, user currencies, exchange rates and the reporting currency, one case per shape. Expected: a missing required field returns 422 naming the field, a bad amount or date returns 422 naming the field, an unknown id returns 404, the happy path returns 200 or 201 with amounts as decimal strings, no session returns 401, and `alice`'s record requested as `bob` returns the same 404 and message as an unknown id. Checks run in a fixed order, so an invalid body naming a foreign id returns 422 before any 404. The template is generated from the route table and instantiated per resource, as the LT.01 experiment.
- **02.API.02** input: create a transfer with a fault injected after the first ledger entry is written. Expected: an error response, and the database utility finds neither ledger entry nor the transfer.
- **02.API.03** input: edit an expense from `"12.50"` to `"15.00"`, then delete it. Expected: its account entry reads `"-15.00"` after the edit and is gone after the delete, read by the database utility.
- **02.API.04** input: transfer `"1000.00"` USD to `"1345.67"` SGD. Expected: stored entries `"-1000.00"` USD and `"1345.67"` SGD, each to two places.
- **02.API.05** input: the 02.LED.06 point and entries created through the API, then balance requests for 2026-05-25 and 2026-06-01. Expected `"87.50"` and `"287.50"`.
- **02.API.06** input: the 02.LED.17 split purchase created through the API. Expected: the card balance falls by `"40.00"`, and the cost center balance is `"0.00"`.
- **02.API.07** input: a USD to SGD transfer on 2026-06-02 with no rate given, then with a user rate `1.35000` recorded for that date, then with an override `1.36000` on the transfer. Expected: the transfer stores the stub rate, then `1.35000`, then `1.36000`, and the stored currency model rates are unchanged after the override.
- **02.API.08** input: an account in JPY when `alice` holds SGD and USD only. Expected: 422 naming the currency.
- **02.API.09** input: an expense with `bob`'s subcategory as `alice`, then a list by a category with two subcategories. Expected: 422 for the first, and the list returns the transactions of both subcategories.
- **02.API.10** input: an expense of `"10.00"` USD on an SGD reporting currency account with the stub rate `1.34567` for the date, then an expense in SGD on a USD account. Expected: account entry `"-13.46"` SGD for the first, and 422 naming the account currency for the second.
- **02.API.11** input: the 02.API.10 expense with a user rate recorded, then an override of the converted amount. Expected: the user rate is used in place of the stub rate, the override is stored on that expense only, and stored rates are unchanged.
- **02.API.12** input: the 02.LED.16 charge created through the API with its billed amount `"136.50"` SGD. Expected: a travel expense of `"-135.00"` and a separate fx fee expense of `"-1.50"`, both on the same card.
- **02.API.13** input: replace the ledger service with one that raises a marked error, then call every route that creates, edits or deletes an expense, income or transfer. Expected: every such route fails with the marked error, so none writes the ledger around the service.
- **02.API.14** input: the stub catalog captured from the probe. Expected: the endpoint returns every currency in the stub catalog fixture with code and name.
- **02.API.15** input: add `EUR`, add `USD` again, add `XXX`. Expected: 201 with EUR in the list, 409 for the duplicate, 422 for the code missing from the catalog.
- **02.API.16** input: remove `EUR` unused, remove `USD` held by an account, remove `SGD` set as reporting currency. Expected: 204 for EUR, and 409 for the others naming the account or the setting that uses it, with the user currency rows still present.
- **02.API.17** input: set the reporting currency to `USD`, then to `EUR` not held. Expected: 200 and USD returned on the next read, then 422.
- **02.API.18** input: delete an account with posted transactions, then list accounts and read one of its transactions. Expected: the account is retired, it leaves the account list, and the transaction still names it.

## Exchange rates silo

Protocols unit and api against the stub rate API, and live for 02.FX.11.

| id       | trace               | layer       | title                                         |
| -------- | ------------------- | ----------- | --------------------------------------------- |
| 02.FX.01 | 17.API.06, 02.MN.06 | direct      | fetch once, then serve from storage           |
| 02.FX.02 | 17.API.07           | oracle      | user rate replaces fetched rate for that user |
| 02.FX.03 | 17.API.08           | oracle      | conversion oracle values                      |
| 02.FX.04 | 17.API.09           | direct      | rate API failure leaves storage unchanged     |
| 02.FX.05 | 17.API.09           | client      | rate client timeouts and named failure causes |
| 02.FX.06 | 17.API.09           | direct      | fetch job reaches a terminal status           |
| 02.FX.07 | 17.DB.03            | direct      | catalog loads from the rate API currency list |
| 02.FX.08 | 17.DB.05, 02.MN.03  | direct      | rate keeps full precision                     |
| 02.FX.09 | 17.API.06, 02.OD.09 | oracle      | rate for a weekend or missing date            |
| 02.FX.10 | 02.CS.04            | self-report | no live network call in silo protocols        |
| 02.FX.11 | 02.RR.01, 02.PR.07  | client      | live rate fetch matches the stub's shape      |

- **02.FX.01** input: request USD.SGD for 2026-06-02 twice. Expected: the stub records one request, one stored row with source `fetched`, and both responses carry the same rate.
- **02.FX.02** input: `alice` records USD.SGD `1.35000` for 2026-06-02, then both users convert `"10.00"` USD on that date with the stub rate `1.34567`. Expected `"13.50"` for `alice` and `"13.46"` for `bob`.
- **02.FX.03** input: `"10.00"` USD to SGD at `1.34567`, `"100"` JPY to SGD at `0.0091`, `"1.00"` SGD to JPY at `109.89`. Expected `"13.46"`, `"0.91"`, `"110"`.
- **02.FX.04** input: request an unstored rate with the stub set to a server error, then to a timeout, then to an unknown pair. Expected: 502 with a message naming the rate API, and the catalog and stored rates identical before and after.
- **02.FX.05** input: the same three stub scenarios through the rate client alone. Expected: the client sets explicit connect and read timeouts, the timeout fires inside the 30 second budget, and each failure raises its own named cause with a fix in its message.
- **02.FX.06** input: a fetch job run with the stub raising a server error part way through a date range. Expected: the job ends in a failed status with the original exception recorded, and the rates fetched before the failure stay stored.
- **02.FX.07** input: load the catalog from the stub list. Expected: one catalog row per stub currency, with its code, name and decimal places.
- **02.FX.08** input: the stub returns `1.3456712345`. Expected: the stored and returned rate is `1.3456712345`.
- **02.FX.09** input: request USD.SGD for Saturday 2026-06-06 with the stub holding Friday 2026-06-05 only. Expected: per 02.OD.09, the Friday rate, stored for the requested date with its source.
- **02.FX.10** input: a silo test that opens a connection to a public host. Expected: the socket guard fails the test.
- **02.FX.11** input: the live protocol fetches USD.SGD for one past date into the test database. Expected: a rate within the 30 second budget, a response shape equal to the stub fixture's, and a stored row with source `fetched`. The run log names the live mode.

## Financial statements silo

Protocols unit and api. Hand-built ledgers with hard-coded totals, then the seed and the reference fixtures. Statement amounts below are the signed API values, per AR.18.

| id       | trace               | layer  | title                                               |
| -------- | ------------------- | ------ | --------------------------------------------------- |
| 02.FS.01 | 11.API.01, AR.18    | oracle | income statement month view totals                  |
| 02.FS.02 | 11.API.02, 02.TD.05 | oracle | income statement matches HomeBudget category totals |
| 02.FS.03 | 11.API.03           | oracle | category line equals sum of subcategory lines       |
| 02.FS.04 | 11.API.04, 02.TD.07 | oracle | balance sheet month-end balances and net worth      |
| 02.FS.05 | 11.API.05           | oracle | year view months equal month views                  |
| 02.FS.06 | 11.API.06, 02.OD.02 | oracle | forex gain or loss line                             |
| 02.FS.07 | 11.API.07           | oracle | change of reporting currency                        |
| 02.FS.08 | 11.API.08           | oracle | transfers keep stored amounts in statements         |
| 02.FS.09 | 11.API.09           | oracle | drill down returns exactly the line's transactions  |
| 02.FS.10 | 11.API.10, AR.18    | client | CSV export equals the presented view                |
| 02.FS.11 | 11.API.11           | client | population, period and incomplete period labels     |
| 02.FS.12 | 02.CS.03            | oracle | month boundary dates                                |
| 02.FS.13 | 02.CS.03            | oracle | month with no transactions                          |

- **02.FS.01** input: a hand-built June 2026 ledger with Food: Groceries `"-120.00"` and Dining `"-45.50"`, Transport: Taxi `"-30.00"`, and Salary `"5000.00"`. Expected: Food `"-165.50"`, Transport `"-30.00"`, expenses `"-195.50"`, income `"5000.00"`, net `"4804.50"`.
- **02.FS.02** input: the seed over the snapshot period. Expected: each subcategory expense total equals its value in `expected/category-totals.json`, compared with the sign rule the fixture states. Also traces 07.CK.09.
- **02.FS.03** input: every category line of every month and year view of the seed. Expected: each category equals the sum of its subcategories exactly.
- **02.FS.04** input: the seed at the end of each month from May 2026 and on the snapshot date. Expected: every account equals `expected/account-balances.json`, liabilities carry their signed values per 02.OD.10, and net worth equals the sum of converted account balances.
- **02.FS.05** input: the 2026 year view and each month view of both statements. Expected: each month column equals its month view, and the income statement year total equals the sum of its twelve months.
- **02.FS.06** input: a USD account holding `"1000.00"` USD, rate `1.34000` on 2026-05-31 and `1.35000` on 2026-06-30, and a USD expense of `"100.00"` on 2026-06-15 at `1.34500`. Expected: opening `"1340.00"` SGD, expense `"-134.50"` SGD, closing `"1215.00"` SGD, forex gain `"9.50"` SGD. With no expense, the gain is `"10.00"`. The ledger holds no forex entry before or after the statement is built.
- **02.FS.07** input: the 02.FS.01 ledger with the reporting currency switched from SGD to USD and rate `1.35000` for June. Expected: every line converted, such as Food `"-122.59"` USD, and a user rate recorded for a date replaces the fetched one in the conversion.
- **02.FS.08** input: the 02.LED.11 transfer in the seed period. Expected: the ledger keeps `"-1000.00"` USD and `"1345.67"` SGD, and the balance sheet converts the USD balance at the month-end rate.
- **02.FS.09** input: every line of every month view in the seed. Expected: the drill down returns transactions whose amounts sum exactly to the line.
- **02.FS.10** input: the CSV export of each year view, each month view and the transaction list. Expected: the statement CSVs equal the JSON response with the presentation rule applied, so expense lines read as positive amounts, and the transaction list CSV holds the signed amounts of its response, all as decimal strings.
- **02.FS.11** input: the June 2026 and July 2026 statements with the clock pinned at 2026-07-15. Expected: each statement names its user, its accounts in scope and its period, and July is marked incomplete while June is not.
- **02.FS.12** input: expenses `"-1.00"` on 2026-06-01, `"-2.00"` on 2026-06-30 and `"-4.00"` on 2026-07-01. Expected: June `"-3.00"`, July `"-4.00"`.
- **02.FS.13** input: a ledger with transactions in May and July and none in June. Expected: June income statement lines are `"0.00"`, and June balances carry the May closing balances.

## Frontend silo

Protocol frontend. The React app in the `iPhone 13` profile with canned API responses, plus the extra widths of 02.FE.01. Each case also asserts the request body the page sent where it submits a form, with amounts as decimal strings. Every case is decided by the client layer.

| id       | trace              | title                                               |
| -------- | ------------------ | --------------------------------------------------- |
| 02.UI.01 | 09.FE.01           | sign-in page starts the OAuth flow                  |
| 02.UI.02 | 09.FE.02           | signed-out page leads to sign-in and back           |
| 02.UI.03 | 09.FE.03           | sign-out returns to sign-in                         |
| 02.UI.04 | 17.FE.01           | currencies page marks the reporting currency        |
| 02.UI.05 | 17.FE.02           | add currency from a searchable catalog              |
| 02.UI.06 | 17.FE.03           | remove currency with confirmation                   |
| 02.UI.07 | 17.FE.04           | set reporting currency                              |
| 02.UI.08 | 17.FE.05, 10.FE.14 | account form offers only the user's currencies      |
| 02.UI.09 | 17.FE.06, 17.FE.07 | exchange rates page and user rate                   |
| 02.UI.10 | 17.FE.09           | failed rate fetch message                           |
| 02.UI.11 | 17.FE.08, 10.FE.15 | amounts and rates display precision                 |
| 02.UI.12 | 10.FE.02           | account list by type with balances                  |
| 02.UI.13 | 10.FE.03           | account ledger month view with running balance      |
| 02.UI.14 | 10.FE.04           | transaction list filters                            |
| 02.UI.15 | RN.02, 10.FE.05    | category list and detail pages                      |
| 02.UI.16 | 10.FE.06           | expense, income and transfer detail pages           |
| 02.UI.17 | 10.FE.09           | detail links, delete confirmation and return        |
| 02.UI.18 | 10.FE.10, 10.FE.11 | transfer form fills and overrides the paired amount |
| 02.UI.19 | 10.FE.12           | expense form subcategory and currency picker        |
| 02.UI.20 | 10.FE.15           | invalid amount message on the field                 |
| 02.UI.21 | 10.FE.01           | create, edit and delete requests for every resource |
| 02.UI.22 | 10.FE.16           | views refresh after a write and keep typed input    |
| 02.UI.23 | 11.FE.01, AR.18    | income statement year view                          |
| 02.UI.24 | 11.FE.02, 02.OD.10 | balance sheet year view                             |
| 02.UI.25 | 11.FE.03           | year navigation                                     |
| 02.UI.26 | 11.FE.04           | month click opens month view                        |
| 02.UI.27 | 11.FE.05           | month views of both statements                      |
| 02.UI.28 | 11.FE.06           | month navigation and return to year                 |
| 02.UI.29 | 11.FE.07           | line click opens its transactions                   |
| 02.UI.30 | 11.FE.08           | forex line in both views                            |
| 02.UI.31 | 11.FE.09           | reporting currency shown with link                  |
| 02.UI.32 | 11.FE.10           | CSV download matches the screen                     |
| 02.UI.33 | RN.06, 02.FE.04    | no horizontal scroll at each width                  |
| 02.UI.34 | 02.FE.04           | loading, empty and error states                     |

- **02.UI.01** input: open the sign-in page. Expected: a sign-in button fits the viewport, and tapping it navigates to the canned authorize URL.
- **02.UI.02** input: open `/accounts` with `/api/me` answering 401, then complete sign-in. Expected: the sign-in page shows, and after sign-in the app returns to `/accounts`.
- **02.UI.03** input: tap sign-out in the header. Expected: a sign-out request is sent and the sign-in page shows.
- **02.UI.04** input: canned currencies SGD and USD with SGD as reporting. Expected: both listed with code and name, and SGD marked as reporting.
- **02.UI.05** input: open add currency and type `eur`. Expected: the list excludes SGD and USD, shows EUR, and choosing it sends `{"code": "EUR"}` and shows EUR in the list.
- **02.UI.06** input: remove USD, with the canned response 409 naming account `Brokerage USD`. Expected: a confirmation first, then USD stays in the list with a message naming `Brokerage USD`.
- **02.UI.07** input: choose USD as reporting. Expected: the request sends USD, and USD shows as marked.
- **02.UI.08** input: open the new account form. Expected: the currency picker lists SGD and USD only.
- **02.UI.09** input: canned rates with one fetched and one user rate, then record USD.SGD `1.35000` for 2026-06-02. Expected: rates listed by pair and date with their source, and the new rate shows as a user rate in place of the fetched one.
- **02.UI.10** input: rate request answering 502. Expected: a message on the page, and the previous rates still shown.
- **02.UI.11** input: canned amounts `"12.50"` SGD, `"1000"` JPY and rate `1.3456712345`. Expected: displayed as `12.50`, `1,000` and `1.3456712345`.
- **02.UI.12** input: canned accounts of three types. Expected: accounts grouped by type, each balance in its own currency, and tapping an account opens its detail page with an edit option.
- **02.UI.13** input: canned June 2026 ledger. Expected: entries by date with a running balance, and back, next and month picker load the matching month.
- **02.UI.14** input: filter by account, category, subcategory, month and a custom range. Expected: each filter sends the matching query parameters and shows the canned results.
- **02.UI.15** input: canned categories with subcategories. Expected: subcategories nested under each category, and the category and subcategory detail pages show attributes, edit options and totals for the selected month.
- **02.UI.16** also traces 10.FE.07, 10.FE.08 and 10.FE.13. Input: open one expense, one income and one transfer between currencies. Expected: each detail page shows the fields its criterion names, including the nominal amount, currency, rate and converted amount for an entry in another currency, and both amounts and the rate for the transfer.
- **02.UI.17** input: from an expense detail, tap its account, then delete the expense. Expected: the account detail opens from the link, a confirmation precedes the delete, and the app returns to the list it came from with refreshed data.
- **02.UI.18** input: transfer from USD to SGD for 2026-06-02 with canned rate `1.34567`, enter `"100.00"` USD, then override the SGD amount to `"135.00"`, then override the rate to `1.36`. Expected: SGD filled as `134.57`, then rate shown as `1.35`, then SGD shown as `136.00`, and the saved request carries the final values.
- **02.UI.19** input: on an SGD reporting currency account, pick category Food, then a subcategory, then currency USD with canned rate `1.34567` and amount `"10.00"`, then open the same form on a USD account. Expected: subcategories limited to Food, the rate filled and the SGD amount shown as `13.46`, and on the USD account the currency fixed to USD.
- **02.UI.20** input: enter `12.345` and `abc` in an SGD amount field. Expected: a message on the field for each, and no request sent.
- **02.UI.21** input: create, edit and delete one record of each resource. Expected: each sends the method, path and body the API endpoints design defines.
- **02.UI.22** input: with an expense form open and a note half typed, save another expense from a second panel, then save the first. Expected: the account ledger, the balance and the open statement view reload after each save, and the half-typed note is kept until its own save.
- **02.UI.23** input: canned 2026 income statement with signed expense lines. Expected: categories with subcategories beneath, twelve month columns and a year total, with expenses shown as positive amounts.
- **02.UI.24** input: canned 2026 balance sheet. Expected: accounts grouped by asset class, month-end balances and net worth per month, with liabilities shown per 02.OD.10.
- **02.UI.25** input: tap back, next and pick 2025. Expected: each requests and shows the matching year.
- **02.UI.26** input: tap June in the year view. Expected: the June month view opens.
- **02.UI.27** input: canned June month views. Expected: the income statement shows categories with subcategories and amounts, and the balance sheet shows month-end balances and net worth.
- **02.UI.28** input: back, next and return to year from the month view. Expected: each loads the matching view.
- **02.UI.29** input: tap Food in the June month view. Expected: the transactions behind Food for June are listed.
- **02.UI.30** input: canned balance sheet with a forex line `"9.50"`. Expected: the forex gain or loss shows as its own line in both views.
- **02.UI.31** input: canned reporting currency USD. Expected: both statements show USD, with a link to the currencies page.
- **02.UI.32** input: tap export on the June income statement. Expected: a CSV downloads whose rows equal the values shown on screen.
- **02.UI.33** input: every page at 390, 393 and 1280 pixels wide with realistic-length names. Expected: page width equals viewport width on each page.
- **02.UI.34** input: each list page with a delayed, an empty and a 500 response. Expected: a loading indicator, an empty message and an error message.

## Authentication and ownership silo

Protocols api and db with the stub identity provider, and live for 02.OWN.12.

| id        | trace               | layer  | title                                              |
| --------- | ------------------- | ------ | -------------------------------------------------- |
| 02.OWN.01 | RN.05, 09.API.01    | direct | first sign-in creates the user                     |
| 02.OWN.02 | 09.API.01           | direct | later sign-in links to the same user               |
| 02.OWN.03 | 09.API.01, 02.AU.02 | direct | failed sign-in scenarios create no user            |
| 02.OWN.04 | 09.API.02           | client | sign-out ends the session                          |
| 02.OWN.05 | 09.API.03, 02.AU.04 | client | every data route rejects a request with no session |
| 02.OWN.06 | 09.API.03           | client | unknown API path answers by session state          |
| 02.OWN.07 | 09.API.03, 02.AU.06 | client | token validation errors answer 401                 |
| 02.OWN.08 | 09.API.04, 02.CS.06 | client | ownership matrix for every route and verb          |
| 02.OWN.09 | RN.05, 02.CS.06     | oracle | statements and exports exclude the other user      |
| 02.OWN.10 | 02.CS.03, 02.OD.04  | client | session lifetime boundary                          |
| 02.OWN.11 | 02.OD.04            | client | session cookie settings                            |
| 02.OWN.12 | 09.FE.04, 02.AU.05  | client | live provider discovery and authorize redirect     |

- **02.OWN.01** input: sign in as `carol@stub`, unknown to the database. Expected: a redirect to the stub, a callback that creates one user and one identity, and a session cookie set.
- **02.OWN.02** input: sign out and sign in again as `carol@stub`. Expected: no new user, the same user id, and a new session.
- **02.OWN.03** input: callback with a mismatched state, `denied@stub`, `unverified@stub` and `tokenerror@stub`. Expected: each returns to the sign-in page with a message, and no user or identity is created.
- **02.OWN.04** input: sign out, then reuse the old session cookie. Expected: 401.
- **02.OWN.05** input: every route in the route table outside the allow list, with no session. Expected: 401 for each.
- **02.OWN.06** input: `GET /api/no-such-path` signed out, then signed in. Expected: 401, then a JSON 404. Neither answer is the single-page app's HTML.
- **02.OWN.07** input: callbacks with a token whose signature is wrong, whose audience is wrong, and whose expiry is one hour past, then one whose expiry is inside the library's clock leeway. Expected: 401 for each of the first three with no server error, and acceptance for the last.
- **02.OWN.08** input: every route and verb as `bob` against `alice`'s record ids. Expected: 404 for each record route and an empty list for each list route, and `alice`'s records unchanged, read by the database utility.
- **02.OWN.09** input: `bob`'s statements, balances, drill down and CSV exports. Expected: values equal `bob`'s own hard-coded totals, unchanged by `alice`'s ledger.
- **02.OWN.10** input: a session one second before and one second after its lifetime, through the pinned clock, with the clock pinned before the session is created. Expected: 200, then 401.
- **02.OWN.11** input: the sign-in response. Expected: the session cookie is HttpOnly and SameSite, and no session token appears in a response body.
- **02.OWN.12** input: the live protocol loads the real provider's discovery document and requests the authorize URL, following every redirect. Expected: the final page is the provider's sign-in page with the configured redirect URI, within the 30 second budget, and no user is created.

## HomeBudget account 02 seed

Milestone 07. Protocols unit, db and reference, against the account `02` snapshot and the expected-value fixtures. Raw seed checks follow 02.TD.11.

| id         | trace                        | layer  | title                                             |
| ---------- | ---------------------------- | ------ | ------------------------------------------------- |
| 02.SEED.01 | 07.CK.08, 02.TD.06           | oracle | snapshot reader returns every record table        |
| 02.SEED.02 | RN.07, 07.CK.02              | direct | account 02 snapshot loads as-is                   |
| 02.SEED.03 | RN.02, 07.CK.02, 02.OD.07    | direct | every HomeBudget account and category maps        |
| 02.SEED.04 | 07.CK.04, AR.11              | direct | every account has its reconciled balance points   |
| 02.SEED.05 | 07.CK.05                     | direct | loading twice gives an identical database         |
| 02.SEED.06 | 07.CK.06, 09.DB.03, 02.CS.02 | direct | two users and every vocabulary value seeded       |
| 02.SEED.07 | 07.CK.07, 17.DB.06, 11.DB.02 | direct | seed rates cover every needed date                |
| 02.SEED.08 | 07.CK.07, 02.TD.08, DQ.05    | oracle | fx transfers carry both snapshot amounts          |
| 02.SEED.09 | 07.CK.08, 02.TD.04           | direct | fixtures are read without RedBooks code           |
| 02.SEED.10 | 07.CK.09, 02.CS.08           | oracle | snapshot edge cases                               |
| 02.SEED.11 | 07.CK.09, 02.TD.07           | oracle | balances match HomeBudget's own balances          |
| 02.SEED.12 | 07.CK.03, 02.TD.10           | direct | seed paths ignored and absent from the site       |
| 02.SEED.13 | 07.CK.10                     | oracle | a planted real value fails every leak check       |
| 02.SEED.14 | DQ.14, AR.07                 | oracle | split over two dates nets the cost center to zero |
| 02.SEED.15 | DQ.14, AR.09                 | direct | transfers out of the cost center are transfers    |
| 02.SEED.16 | DQ.09, AR.08                 | direct | Credit-type assets keep positive balances         |
| 02.SEED.17 | M2.10, AR.08                 | oracle | bill account returns to zero after each payment   |
| 02.SEED.18 | DQ.06, AR.06                 | oracle | negative expenses load as refunds                 |
| 02.SEED.19 | DQ.13                        | direct | card rebate loads as income and a transfer        |
| 02.SEED.20 | DQ.11, AR.05                 | direct | forfeited deposit closes its account at zero      |
| 02.SEED.21 | DQ.10, AR.11                 | oracle | a mid-period point rolls earlier balances back    |
| 02.SEED.22 | DQ.01                        | direct | rows after the snapshot date are skipped          |
| 02.SEED.23 | DQ.02                        | direct | transfers with no account are skipped, reported   |
| 02.SEED.24 | MK.01                        | direct | reload matches every row by its device key        |

- **02.SEED.01** input: the newest **homebudget snapshot**. Expected: the reader returns the Account, Category, SubCategory, Expense, Income and Transfer rows dated on or before the snapshot date, each table with the row count in `expected/record-counts.json` after the skips of the **homebudget data review**.
- **02.SEED.02** input: the seeded database and the snapshot. Expected: every snapshot row dated on or before the snapshot date, other than a row a data review rule skips, has one seed row, with its account name, payee, notes, date and AccountTrans amount unchanged.
- **02.SEED.03** input: every account and every category and subcategory in the snapshot. Expected: each account takes one account type of the **financial statements design**, per the account mapping of the **homebudget data review**, and each subcategory one subcategory line of that design. An unmapped value fails the load with its name.
- **02.SEED.04** input: the snapshot's Account table and the seeded accounts. Expected: every account holds one reconciled balance point, equal to its `balance` on its `balanceDate` in the snapshot.
- **02.SEED.05** input: load the seed twice into empty databases with pinned loader inputs. Expected: identical row-level contents, every balance, count and date derived from other rows computed by the loader, and no change to any generated file under git.
- **02.SEED.06** input: the seeded database. Expected: `alice` and `bob` each own accounts and transactions, and every value in 02.TD.02 has at least one row.
- **02.SEED.07** input: every date the seed ledger and seed statements need. Expected: a stored USD.SGD rate exists for each, including every month end from 2026-05-31 to 2026-09-30.
- **02.SEED.08** input: the three transfers between currencies on 2026-06-02, 2026-08-24 and 2026-09-08. Expected: each carries the USD and SGD amounts from its AccountTrans rows and the rate derived from them, all equal to `expected/fx-transfers.json`.
- **02.SEED.09** input: the fixture builder's imports and outputs. Expected: it imports no RedBooks app module, and each fixture value traces to a snapshot row.
- **02.SEED.10** input: one row per edge case: a USD expense, a deposit refund, a prepaid card top-up, a transfer between currencies and same-day identical expenses, such as two `"5.60"` coffees. Expected: each loads per its rule with its exact amounts, and the two coffees load as two records. The **homebudget data review** adds 02.SEED.14 to 24 for the further edge cases it records, per design closure criterion 07.
- **02.SEED.11** input: the seeded ledger. Expected: every account's balance at each month end from May 2026 and on the snapshot date equals `expected/account-balances.json`, the HomeBudget balance from the account's point and its AccountTrans rows, to the cent.
- **02.SEED.12** input: list every seed and expected-value fixture path, run `git check-ignore --no-index` on each, and build the docs site. Expected: every path is ignored, and no seed file or snapshot value appears in the built site.
- **02.SEED.13** input: plant one real payee from the snapshot in a committed log, a test output file, a screenshot name, a trace and a docs page, one at a time. Expected: the matching leak check fails on each plant and passes on the clean tree. The HomeBudget data review adds any further path it finds, per LT.05.
- **02.SEED.14** input: each of the 4 date pairs in DQ.14 where the cost center does not net to zero on the first date. Expected: the cost center is `"0.00"` at the end of the second date of each pair and on 2026-09-29.
- **02.SEED.15** input: the 12 transfers out of the cost center. Expected: each loads as a transfer with a negative entry on the cost center and an equal positive entry on the receiving account, and no income or expense entry.
- **02.SEED.16** input: brokerage cash M2.05, the stored-value accounts M2.08 and M2.09 and the friends receivable M2.16, which HomeBudget types as Credit. Expected: each takes its account type from the account mapping of the **homebudget data review**, its balance at its point equals the snapshot point, and a balance on either side of zero loads unchanged.
- **02.SEED.17** input: the utility bill account M2.10 over the snapshot. Expected: its balance is negative between each billed amount and its payment, and `"0.00"` after each of the two payments.
- **02.SEED.18** input: the 2 negative expenses in the snapshot. Expected: each loads as a refund with positive entries on its category and its account, per ST.02.
- **02.SEED.19** input: the card rebate income and the same-day transfer of the same amount from the main bank to the card. Expected: one income record and one transfer, the main bank unchanged by the pair, and the card raised by the rebate.
- **02.SEED.20** input: the previous rental deposit M2.11. Expected: the forfeit expense posts on M2.11 under `projects`, the account balance is negative for the 7 days before its funding transfers, and it closes at `"0.00"`.
- **02.SEED.21** input: the transit stored-value account M2.08, whose point is dated 2026-09-14. Expected: its balance on 2026-05-24 equals the point less the signed entries between the two dates, per AR.11.
- **02.SEED.22** input: a snapshot holding expenses and transfers dated after the snapshot date, from a recurring template and from a future-dated entry. Expected: none loads, each appears in the load report under DQ.01, and a later snapshot past their dates loads them once.
- **02.SEED.23** input: the 13 transfers dated 2026-05-09 to 2026-05-17 that name no account. Expected: none loads, each appears in the load report under DQ.02, and no balance changes.
- **02.SEED.24** input: load a snapshot, edit one expense's amount and notes in a copy of it, then load the copy over the seeded database, and load a snapshot of a rebuilt desktop database. Expected: each reload matches every row by source, table, origin device id and `deviceKey`, the edited expense updates in place with no duplicate, and the row count is unchanged.

## HomeBudget account 01 migration

Milestone 12. Protocols unit, db and reference, against account `01` fixture rows per 02.TD.12. The account `01` tracker expands these release-level cases once the HomeBudget data review sets its rules and reference figures.

| id        | trace                  | layer       | title                                        |
| --------- | ---------------------- | ----------- | -------------------------------------------- |
| 02.MIG.01 | 12.CK.01               | self-report | forward migrations with a startup head check |
| 02.MIG.02 | 12.CK.02               | direct      | second opt-in and backup before any write    |
| 02.MIG.03 | RN.02, 12.CK.03, 12.01 | direct      | every legacy category maps                   |
| 02.MIG.04 | RN.07, 12.CK.04        | oracle      | every row is loaded, skipped or reported     |
| 02.MIG.05 | 12.CK.05, MK.03        | direct      | overlap with the seed adds only new records  |
| 02.MIG.06 | 12.CK.06               | direct      | identical same-day transactions each load    |
| 02.MIG.07 | 12.CK.07               | direct      | rerun adds nothing                           |
| 02.MIG.08 | 12.CK.08, DQ.31        | oracle      | cost center matches HomeBudget each month    |
| 02.MIG.09 | 12.CK.09               | oracle      | results match the account 01 reference       |
| 02.MIG.10 | 12.CK.10               | direct      | job reaches a terminal status with progress  |
| 02.MIG.11 | 02.CS.06               | direct      | migration touches only the target user       |
| 02.MIG.12 | DQ.20                  | direct      | rows outside the scope are skipped, reported |
| 02.MIG.13 | DQ.33                  | direct      | retired accounts are not migrated            |
| 02.MIG.14 | DQ.22                  | oracle      | account amounts come from AccountTrans       |
| 02.MIG.15 | DQ.23, AR.12           | oracle      | foreign expense on a SGD account keeps both  |
| 02.MIG.16 | DQ.24, AR.12           | oracle      | transfer between currencies takes both sides |
| 02.MIG.17 | DQ.40, AR.10           | oracle      | opening point at the scope start             |
| 02.MIG.18 | DQ.26, 27, 29          | direct      | zero, negative and reversed rows             |
| 02.MIG.19 | DQ.38, 12.02           | oracle      | paired account resets to its last 01 point   |
| 02.MIG.20 | DQ.39                  | direct      | accounts outside net worth load outside it   |

- **02.MIG.01** input: a database at the migration head, then one with a deliberately skipped revision. Expected: the app starts on the first, and on the second the startup head check refuses to start with a message naming the missing revision.
- **02.MIG.02** input: run the migration command without the second opt-in, then with it. Expected: the first exits non-zero before any write, and the second writes a backup of the working database before its first write.
- **02.MIG.03** input: every legacy category in the account `01` fixture rows. Expected: each maps to one subcategory line of the **financial statements design** through the legacy workbook mapping, and the mapping report lists any it could not map.
- **02.MIG.04** input: a full migration of the fixture rows. Expected: loaded plus skipped plus reported equals the fixture row count for each kind, and the report lists added and skipped counts per kind.
- **02.MIG.05** input: account `01` fixture rows that overlap the account `02` seed in accounts, categories and transactions. Expected: overlapping records match by the match key, and no duplicate account, category or transaction is created.
- **02.MIG.06** input: two identical expenses on one day in the fixture rows. Expected: two records, and a rerun keeps two.
- **02.MIG.07** input: migrate the same fixture rows twice. Expected: zero records added on the second run, and every balance and total unchanged.
- **02.MIG.08** input: fixture rows from 2017-01-01 where every expense runs through the cost center, per CE.04 of the **accounting rules**. Expected: each cost center's balance at every month end equals its HomeBudget balance from AccountTrans, and every cost center is `"0.00"` on 2026-05-23.
- **02.MIG.09** input: the migrated fixture user. Expected: balances and category totals equal the account `01` reference figures from the data review, through the reference checks.
- **02.MIG.10** input: a migration with a fault injected at a known row. Expected: the job ends in a failed status with the original exception recorded, the rows before the fault stay committed, and a rerun adds only the rest.
- **02.MIG.11** input: migrate into `alice`. Expected: `bob`'s row counts and balances unchanged.
- **02.MIG.12** input: fixture rows dated 2016-12-31, 2017-01-01, 2026-05-23 and 2026-05-24, including a recurring entry. Expected: the two rows inside the scope load, and the other two are skipped and counted under DQ.20 in the report.
- **02.MIG.13** input: an account with no activity from 2017-01-01 to 2026-05-23 and a small balance at the cutoff. Expected: it is not created, the report lists it under DQ.33, and no migrated row references it.
- **02.MIG.14** input: an expense on a USD account with `amount` `"13.40"`, `currency` USD, `currencyAmount` `"10.00"` and an AccountTrans amount of `"10.00"`. Expected: the account entry is USD `"-10.00"`.
- **02.MIG.15** input: an expense on a SGD account with AccountTrans amount `"135.00"`, `currency` USD and `currencyAmount` `"100.00"`. Expected: SGD `"-135.00"` on the account and the category, with nominal USD `"100.00"` and rate `1.35` kept on the transaction.
- **02.MIG.16** input: a USD to SGD transfer with AccountTrans out `"100.00"` and in `"135.00"`. Expected: USD `"-100.00"` on the sender, SGD `"135.00"` on the receiver and a derived rate of `1.35`.
- **02.MIG.17** input: an account whose own point is dated 2014-12-01, with a HomeBudget balance of `"250.00"` at the end of 2016-12-31. Expected: the migrated account carries a reconciled point of `"250.00"` on 2017-01-01, and its balance at the cutoff equals the account `01` reference figure.
- **02.MIG.18** input: a zero-amount expense, a negative expense and a negative transfer. Expected: the zero row is skipped and reported, the negative expense loads as a refund, and the negative transfer loads as a positive transfer in the reverse direction.
- **02.MIG.19** input: a paired account whose last account `01` point is `"1000.00"` on 2026-03-13, with account `01` records to 2026-05-23, and whose account `02` point is `"1200.00"` on 2026-05-24. Expected: after the migration the account carries the 2026-03-13 point and no 2026-05-24 point, its balance runs through both histories from that point, and the load report shows the open reconcile scope from 2026-03-13.
- **02.MIG.20** input: a counterparty and a loan with `includeAccount = 'N'` and activity in the scope. Expected: both migrate, the counterparty outside net worth and the loan as a liability, and net worth excludes the counterparty.

## End-to-end tier

Protocol e2e. The Docker stack with the seeded database, the stub identity provider and the stub rate API. The UI tester drives the real web app in the `iPhone 13` profile.

| id        | trace           | layer          | title                                            |
| --------- | --------------- | -------------- | ------------------------------------------------ |
| 02.E2E.01 | RN.08, 09.FE.04 | client, direct | golden path from sign-in to statement            |
| 02.E2E.02 | RN.03, 10.FE.10 | client, direct | transfer between currencies with a fetched rate  |
| 02.E2E.03 | RN.04, 11.FE.09 | client, oracle | reporting currency change reaches the statements |
| 02.E2E.04 | RN.04, 11.FE.10 | oracle         | CSV export saved on the local host               |
| 02.E2E.05 | RN.05, 09.FE.02 | client         | second user sees none of the first user's data   |

- **02.E2E.01** input: sign in as a new stub user, add SGD, create an SGD account with a `"100.00"` first balance point, record a `"12.50"` expense. Expected: the account list shows `87.50`, the month income statement shows `12.50` under its subcategory, and the database utility finds one expense with its `"-12.50"` account entry.
- **02.E2E.02** input: as `alice`, a USD to SGD transfer on a date with no stored rate. Expected: the form fills the SGD amount from the stub rate, the stub records one request, and the saved transfer stores both amounts.
- **02.E2E.03** input: change the reporting currency to USD on the currencies page. Expected: both statements show USD and lines converted at the stub rates, matching 02.FS.07's oracle.
- **02.E2E.04** input: export the June income statement. Expected: the file lands in the local export folder, and its values equal the month view on screen and the API response with the presentation rule applied.
- **02.E2E.05** input: sign in as `bob` after `alice`. Expected: account list, ledger and statements show only `bob`'s data.

## Environment and validation utilities

Milestones 06 and 08. Each tool's verdict is checked against a deliberate failure.

| id        | trace              | layer       | title                                             |
| --------- | ------------------ | ----------- | ------------------------------------------------- |
| 02.ENV.01 | 06.CK.01, 06.CK.04 | self-report | one command starts the stack from a clean clone   |
| 02.ENV.02 | 08.CK.01           | self-report | environment check fails when a service is down    |
| 02.ENV.03 | 06.CK.03, 08.CK.08 | oracle      | every environment variable is in `.env.sample`    |
| 02.ENV.04 | 06.CK.05           | self-report | every protocol runs an empty suite                |
| 02.ENV.05 | 06.CK.09, 02.RR.04 | oracle      | every process runs in the mode `.env` selects     |
| 02.ENV.06 | 06.CK.07, 06.CK.08 | self-report | preflight fails on each injected fault            |
| 02.ENV.07 | 08.CK.02           | direct      | database reset restores seed data                 |
| 02.ENV.08 | 08.CK.03           | direct      | database utility on every table                   |
| 02.ENV.09 | 08.CK.04           | client      | API tester verdict matches the api protocol       |
| 02.ENV.10 | 08.CK.05           | client      | UI tester runs in both modes                      |
| 02.ENV.11 | 08.CK.06, 07.CK.09 | oracle      | reference checks report expected and actual       |
| 02.ENV.12 | 08.CK.07           | self-report | verdicts, logs, exits, planted faults and budgets |
| 02.ENV.13 | 08.CK.11           | direct      | working database tools need the second opt-in     |
| 02.ENV.14 | 06.CK.02           | human       | web app loads in the emulator and on a phone      |
| 02.ENV.15 | 08.CK.10           | oracle      | validation cycle skill names every tool           |

- **02.ENV.01** input: a fresh clone, then the setup, start and stop steps exactly as the developer guide draft records them. Expected: database, backend and web app up, the environment check passes, and the stop step stops every service. After the validation utilities land, the same commands still pass. Also traces 08.CK.09.
- **02.ENV.02** input: stop the backend, run the environment check. Expected: the backend reported down and a non-zero exit.
- **02.ENV.03** input: scan the code for settings fields and environment variable reads. Expected: each is in `.env.sample` with a description, and the tools read their settings from `.env` through the settings object.
- **02.ENV.04** input: each pytest marker with no tests. Expected: each protocol runs and exits cleanly.
- **02.ENV.05** input: build the settings object in the app, in a script and in the test fixtures from one `.env`, then change the mode in `.env` once. Expected: all three report the same effective mode in their logs, and all three follow the change.
- **02.ENV.06** input: inject each preflight fault in turn, such as a missing `.env` key, a stopped database and a shared worktree. Expected: the preflight fails with a message naming each fault, and passes once all are cleared.
- **02.ENV.07** input: add a record, run the reset. Expected: row counts equal the counts read from the seed before the change.
- **02.ENV.08** input: get, insert, update, delete and search on every table, from the command line and as an import. Expected: each round-trips.
- **02.ENV.09** input: one case file through the API tester and the api protocol. Expected: the same verdict for every case.
- **02.ENV.10** input: one check file in canned and real-backend modes, with one deliberately failing check. Expected: the same verdicts in both modes, and a screenshot saved for the failed check.
- **02.ENV.11** input: the freshly seeded database, then the same database with one balance altered by the database utility. Expected: every fixture value reported with expected and actual, all passing on the fresh seed, and the altered one failing.
- **02.ENV.12** input: for each tool, one passing run, one with a deliberate fail, one with a deliberate error and one with a step delayed past its budget. Expected: the matching verdict, one structured record per case in the shared log, and exit 0, then non-zero for each of the other three.
- **02.ENV.13** input: run each tool that writes into the working database without the second opt-in, then with it. Expected: the first refuses before any write, and the second writes a backup before its first write.
- **02.ENV.14** input: open the web app in the mobile emulator, then on a phone through the tunnel. Expected: the sign-in page loads in both. Run as part of 02.HUM.01.
- **02.ENV.15** input: the `redbooks-deploy-and-validation-cycle` skill. Expected: it names each tool in 02.VU.01 to 06, when to use it, and its command.

## Human validation checklists

Run after every automated protocol for the milestone passes, on a phone through the tunnel or in the mobile emulator. Each feature milestone tracker copies its checklist into its Validate section.

| id        | milestone                        | checklist          |
| --------- | -------------------------------- | ------------------ |
| 02.HUM.01 | 06 local dev and test env        | 01, 02             |
| 02.HUM.02 | 09 oauth login                   | 01, 02, 03, 04     |
| 02.HUM.03 | 17 currency model                | 01, 02, 03, 04     |
| 02.HUM.04 | 10 txn and accounts              | 01, 02, 03, 04, 05 |
| 02.HUM.05 | 11 financial statements          | 01, 02, 03, 04     |
| 02.HUM.06 | 12 homebudget account 01 migrate | 01, 02, 03         |

**02.HUM.01 local dev and test env**

01. the web app loads on a phone through the tunnel, and in the mobile emulator on the laptop.
02. the first page reads well at phone size, with no zoom needed.

**02.HUM.02 oauth login**

01. the full live OAuth sign-in with the real provider on the phone works, including first sign-in, per 02.HV.03.
02. the header shows the signed-in user and the sign-out action is easy to reach.
03. opening a bookmarked page while signed out returns to that page after sign-in.
04. a failed sign-in message is clear.

**02.HUM.03 currency model**

01. adding a currency from the searchable list is quick on a phone keyboard.
02. the message on removing a currency in use names what uses it, in plain words.
03. the rates page shows a plausible USD to SGD rate from the live run, with its source.
04. recording a user rate and seeing it replace the fetched one is clear.

**02.HUM.04 txn and accounts**

01. recording an expense on the phone takes few taps, with the amount keyboard showing digits.
02. the transfer form's fx fill and override behave as expected while typing.
03. the account ledger running balance agrees with the HomeBudget app for one account and month.
04. delete confirmations and the return to the list feel natural.
05. amounts are readable and aligned on a phone screen.

**02.HUM.05 financial statements**

01. the year view scrolls across twelve months on a phone without losing the line labels.
02. moving between year view, month view and drill down is easy to follow.
03. one month's income statement agrees with the HomeBudget app's report for that month.
04. the exported CSV opens in a spreadsheet with correct amounts.

**02.HUM.06 homebudget account 01 migrate**

01. account balances after migration agree with the HomeBudget app for accounts outside the reference figures.
02. a sample of transactions per month agrees with the HomeBudget app, including the transfers between currencies.
03. the migration report is readable and each reported row makes sense.

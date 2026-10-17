# RedBooks - Release 0.2.0 Milestones

## Contents

- [Feature milestones](#feature-milestones)
- [References](#references)
- [Requirements](#requirements)
- [Agent skills customization](#agent-skills-customization)
- [Test strategy and cases](#test-strategy-and-cases)
- [Design](#design)
- [Agent skills implement customization](#agent-skills-implement-customization)
- [Local dev and test env](#local-dev-and-test-env)
- [Schema and account 02 seed](#schema-and-account-02-seed)
- [Validation utilities](#validation-utilities)
- [Oauth login](#oauth-login)
- [Audit skills checkpoint](#audit-skills-checkpoint)
- [Currency model](#currency-model)
- [Txn and accounts](#txn-and-accounts)
- [Financial statements](#financial-statements)
- [Homebudget account 01 migrate](#homebudget-account-01-migrate)
- [Audit skills promote learning](#audit-skills-promote-learning)
- [Mkdocs documentation](#mkdocs-documentation)
- [Publish and release](#publish-and-release)

## Feature milestones

The `seq` column determines the implementation order

| id | release | seq | status  | feature                              |
| -- | ------- | --- | ------- | ------------------------------------ |
| 01 | 020     | 01  | closed  | requirements                         |
| 05 | 020     | 02  | closed  | agent skills customization           |
| 02 | 020     | 03  | open    | test strategy and cases              |
| 04 | 020     | 04  | open    | design                               |
| 16 | 020     | 05  | pending | agent skills implement customization |
| 06 | 020     | 06  | pending | local dev and test env               |
| 07 | 020     | 07  | pending | schema and account 02 seed           |
| 08 | 020     | 08  | pending | validation utilities                 |
| 09 | 020     | 09  | pending | oauth login                          |
| 18 | 020     | 10  | pending | audit skills checkpoint              |
| 17 | 020     | 11  | pending | currency model                       |
| 10 | 020     | 12  | pending | txn and accounts                     |
| 11 | 020     | 13  | pending | financial statements                 |
| 12 | 020     | 14  | pending | homebudget account 01 migrate        |
| 13 | 020     | 15  | pending | audit skills promote learning        |
| 14 | 020     | 16  | pending | mkdocs documentation                 |
| 15 | 020     | 17  | pending | publish and release                  |

01. milestone `03`, test cases, is merged into milestone `02`, test strategy and cases. Milestone `18`, audit skills checkpoint, is new. The structure follows the Lessons to apply to the planning documents section of the **lessons learned**, entry PD.01.

## References

- **release roadmap**: [../../release-roadmap.md](../../release-roadmap.md)
- **requirements**: [../../requirements.md](../../requirements.md)
- **release milestones**: [020-release-milestones.md](020-release-milestones.md)
- **lessons learned**: [easymcf-lessons-learned.md](design/easymcf-lessons-learned.md)
- **accounting rules**: [accounting-rules.md](design/accounting-rules.md)
- **homebudget accounts**: [homebudget-accounts.md](design/homebudget-accounts.md)
- **agent skills tracker**: [020.05-agent-skills-customization.md](features/020.05-agent-skills-customization.md)
- **test strategy tracker**: [020.02-test-strategy.md](features/020.02-test-strategy.md)
- **test strategy**: [test-strategy.md](design/test-strategy.md)
- **test cases**: [test-cases.md](design/test-cases.md)
- **workflows**: [workflows.md](design/workflows.md)
- **data flows**: [data-flows.md](design/data-flows.md)
- **front end pages**: [front-end-pages.md](design/front-end-pages.md)
- **financial-statements 010**: [https://github.com/yayfalafels/financial-statements/](https://github.com/yayfalafels/financial-statements/)
- **homebudget wrapper**: [https://github.com/yayfalafels/homebudget](https://github.com/yayfalafels/homebudget)
- **requirements analysis**: [../../requirements-analysis-chatgpt.md](../../requirements-analysis-chatgpt.md)
- **easyMCF roadmap**: `easymcf/docs/releases/release-roadmap.md`
- **easyMCF 010 milestones**: `easymcf/docs/releases/010/010-release-milestones.md`
- **easyMCF 010 issues**: `easymcf/docs/releases/010/010-issues.md`
- **postgres money types**: [https://www.crunchydata.com/blog/working-with-money-in-postgres](https://www.crunchydata.com/blog/working-with-money-in-postgres)
- **single-entry bookkeeping**: [https://en.wikipedia.org/wiki/Single-entry_bookkeeping](https://en.wikipedia.org/wiki/Single-entry_bookkeeping)
- **strangler fig parallel run**: [https://www.webstackbuilders.com/articles/strangler-fig-migration-complete-guide](https://www.webstackbuilders.com/articles/strangler-fig-migration-complete-guide)

## Requirements

The requirements milestone sets what `0.2.0` delivers and why. It records the lessons from **financial-statements 010** and easyMCF, fixes the scope in the **release roadmap**, audits that scope, and writes the release notes in the release page. It captures a snapshot of the user's HomeBudget accounts and transactions, exported from the HomeBudget app into the gitignored `data/` folder. The snapshot and the **homebudget wrapper** source code are the two sources of HomeBudget information for the release. The snapshot supplies the data, and the wrapper source code documents how HomeBudget structures accounts, transactions, transfers and currencies. Figures available only in the live HomeBudget app are written by the user into two files alongside the export. The account balances file holds the HomeBudget accounts with their starting balances, and the opening balance of each month and the closing balance on the snapshot date for select accounts. The fx transfers file holds both sides of every transfer between currencies, with the amount in each currency and the exchange rate HomeBudget applied. On 2026-10-17 the export and both files were removed as stale. A dated snapshot of the account `02` HomeBudget database replaced them as the source, and the automated validation reads HomeBudget's own figures from it, per the HomeBudget data review.

**closure criteria**

01. the **release roadmap** lists every `0.2.0` feature and the release each later feature belongs to.
02. every requirements audit issue has a recorded response, and the response is applied to the release notes and the roadmap.
03. the release notes describe the ledger, categories, multiple currencies, financial statements, users, mobile layout and HomeBudget history for `0.2.0`.
04. the HomeBudget snapshot in `data/` holds the full transaction report, the account balances file and the fx transfers file. The account `02` database snapshot superseded all three on 2026-10-17.
05. every milestone in this doc has a description and closure criteria.

**tasks**

| id    | seq | status   | task                                     |
| ----- | --- | -------  | ---------------------------------------- |
| 01.01 | 01  | closed   | lessons from past attempts               |
| 01.02 | 02  | closed   | release roadmap                          |
| 01.03 | 03  | closed   | release milestones inventory             |
| 01.04 | 04  | closed   | requirements audit issues                |
| 01.05 | 05  | closed   | apply requirements to release notes      |
| 01.06 | 06  | closed   | homebudget snapshot                      |
| 01.07 | 07  | closed   | release notes review                     |
| 01.09 | 08  | closed   | homebudget balances snapshot             |
| 01.08 | 09  | closed   | deliverables and closing criteria        |

__01.04 (closed) requirement audit__

This audit reviews the planned scope and the milestone sequence for 0.2.0. It draws on the **financial-statements 010** retrospective in the **requirements**, the easyMCF 010 delivery recorded in the **easyMCF roadmap**, **easyMCF 010 milestones** and **easyMCF 010 issues**, the **requirements analysis**, and external practice. No 0.2.0 design exists yet, so each finding is about the plan itself and what it is likely to cause if followed as written.

_audit issues_

| id       | status   | severity | title                                              |
| -------- | -------- | -------- | -------------------------------------------------- |
| 01.04.01 | closed   | high     | scope is wider than an mvp                         |
| 01.04.02 | closed   | high     | deployment target contradicts itself               |
| 01.04.03 | closed   | high     | accounting model is the unmade central decision    |
| 01.04.04 | closed   | high     | balance sheet accuracy has no check until 0.3.0    |
| 01.04.05 | closed   | medium   | mobile capture is unreachable from a local deploy  |
| 01.04.06 | closed   | medium   | data migration comes too late in the sequence      |
| 01.04.07 | closed   | medium   | multi-currency rules are unspecified               |
| 01.04.08 | closed   | medium   | eight milestones pass before the first feature     |
| 01.04.09 | closed   | low      | agents and skills still describe easyMCF           |
| 01.04.10 | closed   | low      | learning is captured only at the end               |

_01.04.01 (closed) scope is wider than an mvp_

>RESPONSE:
>retain most of the stated scope for 0.2.0, and move cloud deployment and PDF exports to 0.3.0
>In scope: 
>- accounts
>- manual transactions
>- consolidated category model
>- income statement and the balance sheet. 
>- csv export
>- oauth multi-user
>- multiple currencies
>- data migration
>- mkdocs publishing CICD
>Out of scope:
>- cloud deployment
>- cloud deploy CICD
>- PDF export

Audit finding

0.2.0 plans fifteen features, among them a new stack, OAuth, multiple users, multiple currencies, two financial statements, PDF and CSV export, S3 storage, data migration, cloud deploy and a CI/CD pipeline. EasyMCF 010 delivered eight features on local SQLite and took roughly eleven weeks, from 12 July to 27 September 2026. The **financial-statements 010** retrospective names design-heavy scope as the first cause of its stall. The **requirements analysis** makes the same point and proposes that every release leaves behind a usable app.

Recommendation

define 0.2.0 by the smallest set that replaces one real workflow end to end. That set is 

- accounts
- manual transactions
- consolidated category model
- income statement and the balance sheet. 

PDF export, S3 storage and multiple users add effort without changing whether the ledger is trustworthy, and can move to 0.3.0. CSV export is cheap and useful for checking results, so it can stay.

settle the accounting model and the HomeBudget data profile, since both shape every later milestone.
run in parallel with HomeBudget and prove its balances against it.

- **shrink to a local** move to next release: Cloud deploy, CI/CD, S3 storage 
- **drop PDF export** move to next release
- **limit to single-user ledger** move to next release: multi-user support

_01.04.02 (closed) deployment target contradicts itself_

>RESPONSE
>accepted proposal: docker local for 0.2.0
>mobile UI testing is essential, so should have local UI that simulates phone UI. doesn't literally need to be on mobile phone, just that size and layout is for mobile phone not desktop browser.  but if possible that is better.

The **release roadmap** sets 0.2.0 deployment to docker local. The **release milestones** include web app cloud deploy and a CI/CD pipeline. The **easyMCF roadmap** records the mcfpipe failure mode as a large upfront investment in cloud infrastructure and CI/CD without a working MVP, and easyMCF avoided it by keeping 010 local and pushing cloud to 020.

Recommendation: keep 0.2.0 on docker local and move cloud deploy and the CI/CD pipeline to 0.3.0, matching the roadmap. A local pre-commit test run covers most of what CI would give a single developer. If A05 makes phone access essential, a private tunnel to the local host is a lighter step than a full cloud deploy.

_01.04.03 (closed) accounting model is the unmade central decision_

>RESPONSE
>single GL basic transaction model, with separate models for expense, income, and transfer. yes, separate transfer model, which has foreign key references to two GL entries on each account for the from and to. similar to how it is modeled in HomeBudget.  Split txn handling is manual and dedicated model and UI to be developed in next release.

The balance sheet, the income statement, transfers between accounts and multiple currencies all depend on how a transaction is stored. The design topics list transactions, accounts and financial statements separately, and none of them owns this decision. The **requirements analysis** recommends single-entry records with explicit transfers and defers double-entry. The **single-entry bookkeeping** reference notes that single-entry books do not balance themselves, so arithmetic errors go undetected. That is a direct risk to the first requirement, accuracy.

Recommendation: decide the model before the transactions design, as its own design topic. The model should store every transaction as balanced journal lines, where each line posts an amount to one account and the lines of a transaction sum to zero. The UI can still present a simple one-line entry that fills in the category or transfer side. This keeps the entry friction low while the database guarantees that the balance sheet balances.

_01.04.04 (closed) balance sheet accuracy has no check_

>RESPONSE
>yes this is deferred to 0.3.0

With statement loading and reconciliation deferred, every 0.2.0 balance comes from manual entry and migrated history. Nothing compares those balances to a bank. A missed or duplicated entry shows up as a wrong net worth with no signal. HomeBudget has the same weakness today, and the current workflow corrects it with the Google Sheets reconciliation.

Recommendation: add balance assertions. A balance assertion records the balance a statement shows for an account on a date, and the app flags any difference from the ledger. This is a small table and a report, far short of full reconciliation, and it gives 0.2.0 a real accuracy check.

_01.04.05 (closed) mobile capture is unreachable from a local deploy_

>RESPONSE
>0.2.0 is reclassified as a POC and 0.3.0 is the first MVP because it is not useful until it is available on phone in real time 24/7 remote at any time without depenency on local pc running. POC 0.2.0 should be tested with a mobile phone UI, if possible via tunnelling to an actual mobile phone, but otherwise using an interactie mobile UI display on the laptop.

The first workflow in the **requirements** is to record and classify transactions in real time on a phone. A docker local deploy is reachable only from the host machine. The likely outcome is that HomeBudget stays the capture tool and every transaction is entered twice, which contradicts the second requirement, minimal friction.

Recommendation: state the capture plan explicitly. One option keeps HomeBudget as the phone capture tool through 0.2.0 and imports its entries into RedBooks on a schedule, so HomeBudget acts as an input adapter. The other exposes the local app to the phone over a private tunnel with a mobile-friendly entry page. Either choice is fine. Leaving it unstated is the risk.

_01.04.06 (closed) data migration comes too late in the sequence_

>RESPONSE
>include in scope review of current HomeBudget category model and historical txns current accounts and use this as the basis for the seed data

Data migration is the last feature milestone. HomeBudget's categories and the financial reporting hierarchy differ, and the **financial-statements 010** retrospective names this two-hierarchy mapping as one of its main problems. The consolidated category model has to absorb that mapping, so the migration's findings shape the data model. Discovering them after the ledger is built risks rework.

Recommendation: profile the HomeBudget data during design. Map its accounts, categories, currencies and transfer patterns into the draft data model and record the mapping gaps. Use a migrated sample as the seed data, so tests run on realistic history from the start. Then treat HomeBudget as a test oracle through a parallel run, as the **requirements analysis** proposes and as the **strangler fig parallel run** pattern recommends. RedBooks is trusted once its net worth and account balances match HomeBudget over several monthly closes.

_01.04.07 (closed) multi-currency rules are unspecified_

>RESPONSE
>reporting currency user should be able to set arbitrarily. for the seed data use reporting-currency=SGD, and include support for USD. use real exchange rates and include feature to fetch real rates. refer to the **homebudget wrapper** repo for specific api. Yahoo Finance is not available. the homebudget wrapper also uses a dedicated money type to avoid the floating point precision issues you flagged. forex changes should show up as a separate line-item gain or loss on the consolidated financial statements. these pl exist only on the period financial statements and are not recorded in the account ledger.

Multi-currency is in scope, with no stated reporting currency, rate source or revaluation rule. A balance sheet in SGD that includes USD accounts needs a rate for each reporting date, and the difference between historical and current rates shows up as an unrealised gain or loss. The prototype already fetches forex rates, so there is a working source to reuse. The **postgres money types** reference recommends the NUMERIC type for amounts and warns against floating point, and higher precision for exchange rates.

Recommendation: include in the accounts or financial statements design the reporting currency, the rate source and storage, the rule for which rate applies to income statement and balance sheet lines, and NUMERIC column types for amounts and rates.

_01.04.08 (closed) eight milestones pass before the first feature_

>RESPONSE
>noted, no change, and no time boxes. this sequence worked well for easyMCF.

Requirements, test strategy, test cases, design, agent skills, the dev environment, seed data and validation utilities all come before any user-facing feature. This order worked for easyMCF, and the **easyMCF 010 issues** show the design audit caught real problems before code. The **requirements analysis** cautions that the same order would delay a finance app's first usable result, and the stall of **financial-statements 010** happened in exactly this phase.

Recommendation: time-box the define phase and build a walking skeleton straight after it. The skeleton is one account, one manual transaction and one balance shown in the web app, running through the whole stack. The dev environment, seed data and validation utilities then grow around a working app, which gives early proof that the stack choices fit together.

_01.04.09 (closed) agents and skills still describe easyMCF_

>RESPONSE
>move up agent skill customization to after requirements defined

Most agents and several skills in the repo's `.claude` folder refer to easyMCF's Flask, SQLite, AngularJS and Playwright stack, and some cover MCF web scraping. RedBooks uses FastAPI, PostgreSQL and React. Agents that follow these instructions will apply the wrong conventions.

Recommendation: the agent skills customization milestone rewrites the stack-specific agents and skills for RedBooks and removes the MCF-specific ones. The design audit and documentation style skills carry over as they are. This milestone is already sequenced before the dev environment, which is the right place for it.

_01.04.10 (closed) learning is captured only at the end_

>RESPONSE
>noted. this doesn't need to be decided at this point

The audit skills milestone comes near the end of the release. Lessons from early milestones fade by then, and agents repeat the same mistakes across the release in the meantime.

Recommendation: record lessons as they happen in each feature tracker, and use the audit skills milestone to consolidate them into the shared skills.

## Agent skills customization

This milestone is the first pass on the Claude Code agents and skills in `.claude/`. It sets up the agent roles and the generic skills, and fills those skills with the lessons learned on easyMCF, rewritten in RedBooks terms. Generic skills hold no RedBooks design decisions, so they are ready before the test and design documents are written, and the lessons they carry shape those documents from the start. Every lesson is stored inside `.claude/`, so the agents carry it forward with no dependency on the easyMCF repo. The bespoke skills follow in the second pass, agent skills implement customization, once the design is closed.

**Generic and bespoke skills**

Every skill in `.claude/skills/` is one of two kinds.

01. **generic skills** hold knowledge that applies to any project using the same domain or technology. Each one is written so it could be copied unchanged into another repo. Generic skills carry plain names, such as `accounting` or `fastapi`.
02. **bespoke skills** hold the RedBooks `0.2.0` design decisions, its components and its feature rules. Each one cites the design docs it draws on. Bespoke skills carry the `redbooks-` prefix, such as `redbooks-ledger`.

A generic skill states practice. A bespoke skill states how RedBooks applies that practice, and links to the generic skill it builds on. For example, `accounting` explains general ledgers, transfers and forex revaluation, and `redbooks-ledger` defines the RedBooks expense, income and transfer models on its general ledger.

Agents follow the same split as the skills split. Each agent describes a RedBooks role and names the generic skills it loads. The second pass adds the bespoke skills each agent loads.

Examples of generic skills for `0.2.0` are:

01. **process**: `documentation-style`, `markdown-tables`, `design-audit` and `feature-implementation-guide`.
02. **domain**: `accounting`, covering general ledgers, account types, opening balances, transfers, income statements, balance sheets, multi-currency accounts and forex gains and losses.
03. **language**: `python`, covering project layout, typing, exact decimal arithmetic, logging and error handling.
04. **backend**: `fastapi` for routes, dependencies, validation and OAuth, and `postgresql` for schema design, migrations, NUMERIC types and query practice.
05. **frontend**: `react`, covering components, state, API calls and mobile-first responsive layout.
06. **testing**: `pytest` for unit and API tests, and `playwright` for end-to-end tests of the web app in a mobile viewport.

**Lessons in the generic skills**

The lessons come from the easyMCF release roadmap, release milestones and design audit issues, its feature trackers, assessments and issue logs, its agents and skills, and the saved Claude Code feedback memories for the easyMCF project. Each lesson lands in the generic skill it belongs to. A lesson about API design goes to `fastapi`, a lesson about milestone and tracker structure goes to `feature-implementation-guide`, and a lesson about writing style goes to `documentation-style`. Lessons specific to MCF scraping, the MCF site and AngularJS stay with easyMCF.

Skills load in stages. The rules that apply every time go in the skill's `SKILL.md`, and detailed lessons and worked examples go in reference files in the skill folder. `SKILL.md` names each reference file and when to read it, so an agent reads a lesson at the moment it applies. The **lessons learned** holds every lesson with its evidence, and the Lesson trace of the **agent skills tracker** records the skill, agent or planning document each lesson lands in.

**closure criteria**

01. every agent in `.claude/agents/` describes a RedBooks role and lists the generic skills it loads.
02. every generic skill listed above exists in `.claude/skills/` and holds no RedBooks-specific names, paths or design decisions.
03. every skill with RedBooks-specific content carries the `redbooks-` prefix.
04. the `webscraping` skill and the MCF-specific content are removed from `.claude/`.
05. a search of `.claude/` for easyMCF, MCF, Flask, SQLite and AngularJS returns no matches.
06. every lesson in the **lessons learned** has a destination in the Lesson trace of the **agent skills tracker** and lands there, and every finding that stays with easyMCF is listed in its Not transferred section.
07. every transferred lesson is written in RedBooks stack terms and readable with the easyMCF repo absent.
08. every reference file in a skill folder is named in that skill's `SKILL.md`, with when to read it.
09. every agent carries the shared boundaries block, and every lesson to be learned has an entry in an `open-lessons` file with its status.

## Test strategy and cases

The test strategy sets how every part of the `0.2.0` release is proven to work as delivered. It covers the ledger and money rules, the data model, the API, the web app in its phone layout, sign-in and data ownership, exchange rates, financial statements, the HomeBudget migration and the local environment. The milestone also writes the case catalogue that turns the strategy into concrete cases, and every feature milestone builds and validates against both.

**Guiding principle**

Each component is tested where its logic lives, in isolation, before the tests of how components fit together. A rounding error in the money type, a wrong ledger balance or a missed forex line is a unit defect, caught by a fast test of that unit alone. End-to-end tests through the web app confirm the wiring between components once each component is proven. This order gives an agent a narrow, fast and deterministic signal on every change, and keeps the slower browser tests for integration.

**Component silos**

Each component has its own silo, a way to test it directly with no other component's correctness as a precondition. Silo protocols make no live network call.

01. **ledger and money**: unit tests on the money type, exact decimal arithmetic, the sign of every entry, balances from reconciled balance points, expense, income, refund and transfer posting rules, billing accounts, split purchases, card foreign exchange fees and transfers between currencies.
02. **data model and database**: the schema build, constraints and round trips through a direct database utility, run against a temporary PostgreSQL database before any API exists on top. During `0.2.0` development the schema is rebuilt and the seed reloaded, and versioned forward migrations are tested in the homebudget account 01 migrate milestone.
03. **backend API**: endpoint cases written as data, each tagged with the requirement it proves, run through the FastAPI test client. Each endpoint covers required fields, validation errors, missing records, the happy path, a request without a session and a request for another user's record.
04. **exchange rates**: rate fetching and storage tested against a stubbed rate API built from the responses the exchange rate API probe saved, and conversion and forex gain or loss tested against fixed stored rates. A live run then confirms the real rate API answers as the stub does.
05. **financial statements**: the income statement, the balance sheet, the forex gain or loss line, drill down and CSV export, tested at the service layer against known ledger data.
06. **frontend**: the React pages tested in a mobile viewport with Playwright, with every API call answered from canned responses, so a rendering defect and a backend defect fail in different silos.
07. **authentication and ownership**: OAuth sign-in against a stub identity provider, with two seeded users in every database, so a data leak between users always has a second user to show up in. A live run checks the real provider's discovery document and sign-in redirect without signing in, and the full live sign-in is the user's own check.
08. **HomeBudget migration**: two loads. The account `02` seed load covers snapshot reading, account and category mapping, the device match key and the reference checks against HomeBudget's own figures in the snapshot, and its cases belong to the schema and account 02 seed milestone. The account `01` migration covers forward migrations, the second opt-in, legacy category mapping, upsert matching and its reference figures, and its cases belong to its own milestone.

**Case selection**

01. **traceability**: every requirement in the release notes has at least one tagged test case. A requirement with no case counts as untested. Coverage of each feature milestone's closure criteria is completed in that feature's tracker, once its design closes.
02. **closed vocabularies**: every account type, transaction kind and transfer kind has a reachable case, and the seed data holds at least one row of each.
03. **boundaries**: every date and period rule gets a case on each side of its boundary, such as a transaction on the first and last day of a statement period.
04. **determinism**: no silo test depends on wall-clock time, a live network call or a fixed sleep. Time comes through a single injectable clock and exchange rates come from stored or stubbed values. A live protocol depends on the network by design and runs under its latency budget.
05. **silo-first order**: a feature writes its cases cheapest first, from unit and database cases through API and frontend cases, and adds an end-to-end case where a real integration risk remains.
06. **ownership leaks**: every resource is tested as a second user against the first user's records, and every result is a not found response or an empty list.

**Run rules**

01. **live order**: automated protocols run against the stubs first, then live for everything except irreversible writes. The full live OAuth flow with its writes is the user's own check.
02. **latency budgets**: every test has an expected latency budget and raises a timeout when it is exceeded, a few seconds for local work and 30 seconds for an internet API call. Load variance is never an accepted close.
03. **feature-scoped test sets**: each feature owns its test set, siloed unit tests first and integration tests after. The end-to-end regression run grows sublinearly, about 1x, 1.5x and 2x of the first feature's run at features 1, 2 to 3, and 10.
04. **settings**: tests read settings from `.env` through the app's settings object, and every run reports its effective mode.

**Independent verification layers**

Each feature milestone validates its closure criteria through independent layers, so no layer grades its own work.

01. **self-report**: the validation utilities replay case files against a running app and report pass or fail per case.
02. **direct inspection**: the database utility reads what a request wrote, independent of the API response.
03. **oracle**: tests with hard-coded expected values taken from the closure criteria and the reference data, never from the code under test.
04. **human validation**: a person walks through the running app on a phone or in the mobile emulator, following a checklist from the milestone's closure criteria, once every automated layer passes.

Tests run in order of speed and information value. Unit, database and API cases run first, then browser cases, then the human pass. When failures appear, independent first failures are separated from the failures they cause and fixed one at a time, and the full suite then runs again as confirmation.

**closure criteria**

01. the test strategy doc defines each component silo, its tools, its scope and the data it runs against.
02. every requirement in the release notes maps to at least one silo, and the case catalogue has a traceability rule to follow.
03. the strategy defines the case selection rules, the independent verification layers and the test run order.
04. the strategy defines the live order, the latency budgets and the feature-scoped test sets of the run rules.

The strategy's sections on test data, money and exchange rate assertions, the stub identity provider, frontend testing, the agent loop, the validation utilities and the human pass are drafts that the milestones owning that work confirm: schema and account 02 seed, currency model, oauth login, validation utilities, and agent skills implement customization.

**Cases**

The case catalogue holds the concrete test cases the strategy scopes, organized by component silo. Each case names its requirement, its silo, its verification layer, its input data and its expected result. The cases cover every requirement in the release notes, the case selection rules above, and the edge cases found in the HomeBudget snapshot, such as same-day identical expenses, transfers between currencies, USD expenses, deposit refunds and prepaid card top-ups. Expected values come from oracles and data reads, never hand counts, and boundary cases account for library tolerances such as token clock leeway.

The catalogue holds the release-level cases, the starting set known before the design. Full coverage of a feature's closure criteria can only be known once that feature's design exists. Each feature milestone copies its cases into its own tracker, reconciles them with its scope, data model and edit locations, and adds the cases its design reveals before its first implement step. The cross-cutting cases, such as the ownership matrix and the reference checks, stay in the catalogue.

**cases closure criteria**

01. the case catalogue lists every case with its requirement, silo, verification layer, input and expected result.
02. every requirement in the release notes has at least one test case.
03. every closed vocabulary value, date boundary and ownership rule named in the test strategy has a test case.
04. every feature milestone with a user-visible surface has a human validation checklist.
05. expected money amounts are stated exactly, to the decimal places of the currency of the account or statement they belong to.
06. every accounting oracle checks each entry's sign against its event as well as the balance, and computes every check from its stated figures.
07. the strategy requires every regression case to be shown to fail without its fix.
08. the catalogue sets the step by which each feature milestone's tracker copies its cases, reconciles them with its design and adds the cases its design reveals, so every closure criterion of that milestone has a case before implementation.

## Design

The design settles how RedBooks meets the requirements before any feature code is written. It runs in three stages, each building on the one before.

01. **user experience**: the design starts from the user workflows, such as recording a transaction, transferring between accounts, reviewing an account ledger and reporting financial statements. The data flows follow from the workflows, naming every data source, store and output, from manual entry and the HomeBudget snapshot through the database to the statements and CSV exports. The front end pages then set the phone-layout screens, navigation and interactions that carry out each workflow.
02. **accounting model**: the HomeBudget data review works from the account `02` and account `01` HomeBudget databases, the **homebudget wrapper** source code, and the questions in the **homebudget accounts** doc. The **accounting rules** set the signed entry vocabulary and posting model every accounting design doc follows. Together with the workflows, it forms the basis of the accounting data model. The model defines the general ledger with its expense, income and transfer models, accounts and account types, the consolidated category model, multiple currencies with the forex gain or loss, and the financial statements. The review maps HomeBudget accounts, account types, categories and transfer patterns into this model and records the migration rules.
03. **system**: the architecture sets the components and how they interact, on the tech stack and repo layout. Users and authentication, networking and security, the API endpoints, the local dev env, the env variables and the docs publishing pipeline complete the design.

Every design doc traces its decisions back to the requirements and forward to the test strategy and its case catalogue. Each feature reconciles its own cases with the design before it is built.

**closure criteria**

01. every design topic below has a design doc marked closed, and each doc traces its decisions to the requirements it serves.
02. the workflows doc describes every user workflow in the release notes, step by step, with the pages and data each step uses.
03. the data flows doc names every data source, store and output, and the workflow that moves data between them.
04. the front end pages doc defines every page with its purpose, phone layout, fields, actions, navigation and the API calls it makes.
05. the data model defines every entity with its fields, types, keys, constraints and ownership, including the general ledger, the expense, income and transfer models, accounts with opening balances, categories, exchange rates and users. Ledger entries are signed amounts per the **accounting rules**. The schema rebuilds and reloads the seed during development, and versioned forward migrations start before the account `01` migration.
06. the accounts, transactions, multi currency and forex, and financial statements docs define their rules and calculations in enough detail to write oracle test cases from them, including split purchases, transfers between currencies, the reporting currency setting, the rate source and storage, the rate applied to each statement line and the forex gain or loss. The multi currency doc follows the foreign currency entry model of AR.12 in the **accounting rules**.
07. the HomeBudget data review maps every HomeBudget account, account type and category into the data model, records a migration rule for every data quality issue in both HomeBudget databases, defines the upsert match key for each record kind, and documents the HomeBudget database layout, the account `02` snapshot and the expected-value oracles. It answers the questions in the **homebudget accounts** doc, adds its edge cases to the case catalogue, and sets the reference figures the account `01` migration is checked against.
08. the architecture doc sets every component, its responsibility and its interfaces, and the tech stack and repo layout docs fix the libraries, versions and folder structure the implementation follows.
09. the users and authentication, and networking and security docs define the OAuth flow, session handling, per-user data scoping, the phone tunnel, and the handling of secrets and personal data. Committed code, committed docs and the published site show no real account names, account numbers or personal details.
10. the API endpoints doc defines every endpoint with its method, path, request, response, errors and the ownership rule it enforces, with one explicit router per resource and every write that carries invariants routed through a service.
11. the local dev env and env variables docs define the Docker services, setup commands and every environment variable, and the docs publishing pipeline doc defines the documentation build and publish workflow.
12. a design audit across the design docs, the requirements, the test strategy and the case catalogue has every finding resolved.
13. every accounting design doc follows the **accounting rules** and copies no example from the financial-statements accounting-logic skill.
14. the exchange rate API is probed by a tracked script, run by the user, before the multi currency and forex topic closes, and its findings are saved as fixtures.
15. each design topic that settles an open design input of the case catalogue updates every case that input affects, and removes the input from the catalogue, before the topic closes.

**tasks**

| id    | seq | status   | design topic                             |
| ----- | --- | -------  | ---------------------------------------- |
| 04.01 | 01  | open     | workflows                                |
| 04.02 | 02  | open     | data flows                               |
| 04.03 | 03  | open     | front end pages                          |
| 04.04 | 04  | open     | homebudget data review                   |
| 04.05 | 05  | pending  | data model                               |
| 04.06 | 06  | pending  | accounts                                 |
| 04.07 | 07  | pending  | transactions                             |
| 04.19 | 08  | pending  | exchange rate api probe                  |
| 04.08 | 09  | pending  | multi currency and forex                 |
| 04.09 | 10  | pending  | financial statements                     |
| 04.10 | 11  | pending  | architecture                             |
| 04.11 | 12  | pending  | tech stack                               |
| 04.12 | 13  | pending  | repo layout                              |
| 04.13 | 14  | pending  | users and authentication                 |
| 04.14 | 15  | pending  | networking and security                  |
| 04.15 | 16  | pending  | api endpoints                            |
| 04.16 | 17  | pending  | local dev env                            |
| 04.17 | 18  | pending  | env variables                            |
| 04.18 | 19  | pending  | docs publishing pipeline                 |

## Agent skills implement customization

This milestone is the second pass on the agents and skills, run once the design is complete. It writes the bespoke `redbooks-` skills that turn the design decisions into the guidance agents follow while they build. Each bespoke skill cites the design docs it draws on and links to the generic skills it builds on, so the generic practice lives in one place and the bespoke skill records only how RedBooks applies it.

The bespoke skills for `0.2.0` are:

01. `redbooks-ledger`: the general ledger, the expense, income and transfer models, opening balances and split purchases. It builds on `accounting` and `postgresql`.
02. `redbooks-currency`: the money type, the reporting currency setting, the exchange rate API and storage, and the forex gain or loss calculation. It builds on `accounting` and `python`.
03. `redbooks-statements`: the income statement, the balance sheet, drill down and CSV export. It builds on `accounting`.
04. `redbooks-backend-api`: the RedBooks API endpoints, user-scoped data access and OAuth session handling. It builds on `fastapi` and `postgresql`.
05. `redbooks-frontend`: the RedBooks pages, navigation and phone layout. It builds on `react`.
06. `redbooks-homebudget-migration`: the HomeBudget database layout and the account `02` snapshot, the account and category mapping, the match keys, and the migration rules from the HomeBudget data review.
07. `redbooks-deploy-and-validation-cycle`: the RedBooks local Docker run and verify loop, using the validation utilities. It builds on `pytest` and `playwright`.

`redbooks-ledger` and `redbooks-statements` draw their rules from the **accounting rules**, and `redbooks-currency` from its foreign currency rules. `redbooks-homebudget-migration` draws on the **homebudget accounts** doc, and covers both the account `02` seed and the account `01` migration.

**closure criteria**

01. every bespoke skill listed above exists in `.claude/skills/`, cites its design docs and links to the generic skills it builds on.
02. no bespoke skill repeats generic practice that its linked generic skill already covers.
03. each implementing agent lists the bespoke skills it loads alongside its generic skills.
04. every agent and skill references design docs by their current names and paths.
05. every skill change is trialled against a control before it is promoted, and only a failing control with a passing experiment counts.
06. the `redbooks-deploy-and-validation-cycle` skill names the narrowest test set to run first for each kind of change, and the first-failure triage the agent follows to correct itself.

## Local dev and test env

This milestone builds the repeatable local environment. Docker Compose runs the PostgreSQL database, the FastAPI backend and the React web app on the developer's laptop. A tunnel connects a real phone to the local web app, and a mobile emulator on the laptop covers the same pages. Environment variables are set through a `.env` file. One settings object reads `.env` directly for the app, the scripts and the tests, and every run logs its effective mode.

**closure criteria**

01. one command starts the database, backend and web app from a clean clone.
02. the web app loads in a mobile emulator on the laptop and on a phone through the tunnel.
03. a `.env.sample` file lists every environment variable with a description.
04. the developer guide draft records the setup, start and stop steps.
05. the test runner executes an empty test suite in every tier.
06. one command creates an empty database. The schema and account 02 seed milestone extends it to build the schema and reload the seed.
07. the preflight check is proven against injected failures.
08. each agent session runs in its own worktree.
09. a test checks that the app, a script and the test fixtures run in the mode `.env` selects.

## Schema and account 02 seed

This milestone builds the database schema from the data model design and loads a dated snapshot of the user's HomeBudget account `02` database from `data/` as the seed that tests, demos and daily development run on. The snapshot script copies the live database named in `.env` into `data/`, and the seed loads the newest copy. The seed is the real data, loaded as-is with its account names, payees and notes, so RedBooks is usable from day one and its figures compare directly with HomeBudget. The seed and everything built from it stay in uncommitted locations, out of version control and the published docs. During `0.2.0` development, one command rebuilds the schema and reloads the seed, and every schema change, in this milestone and in every feature milestone after it, runs through that command and changes the schema, the seed load and the data model doc together. The snapshot supplies each account's reconciled balance point. The fixture builder writes the expected-value fixtures from the snapshot with plain SQL, from HomeBudget's own balances, transfer amounts and category totals.

**closure criteria**

01. one command builds the schema from the data model design and reloads the seed from `data/` into an empty database.
02. the seed holds the account `02` snapshot as-is, with its real account names, payees and notes, and a second user with distinct data.
03. the seed and the expected-value fixtures live in the uncommitted location the repo layout design sets, `git check-ignore --no-index` passes for every seed path, and the docs build includes none of them.
04. every account has its reconciled balance point from the snapshot.
05. counts, balances and dates derived from other rows are computed by the loader, loader inputs are pinned, loading twice gives an identical database, and every changed generated file is reviewed.
06. every closed vocabulary value has a seeded row, and every constraint comes from the requirements.
07. the seed holds stored USD to SGD exchange rates for every date it needs, and each transfer between currencies carries the two amounts the snapshot holds for it.
08. the expected-value fixtures hold the category totals, account balances, fx transfer amounts and record counts, each read from the snapshot with plain SQL without running RedBooks code.
09. the seed includes every edge case in the case catalogue, and passes every expected-value check.
10. every path that could carry seed data out of its location, such as logs, test output, screenshots, traces and the docs build, has a check shown to fail on a planted real value.

## Validation utilities

This milestone builds the standalone tools that give every later feature a fast, repeatable pass or fail signal outside the pytest suite. The tools carry out the independent verification layers set in the test strategy: self-report through case replay against a running app, direct inspection of the database, and oracle checks against the reference data. They build on the scripts from the local dev and test env milestone and extend them in place, and on the seed load and expected-value fixtures of the schema and account 02 seed milestone, which precedes them. Feature milestones then add their own case files and checks to these tools, and write no new tools of their own.

The toolset covers:

01. **environment check**: confirms the Docker services, the database, the backend and the web app are up and reachable before any validation runs.
02. **database reset**: resets the local database to the seed data in one command.
03. **database utility**: reads, writes and searches any table directly, bypassing the API, for direct inspection of what a request wrote and for setting up state in a case.
04. **API tester**: replays a case file, or one named case in it, against the running backend, signed in as a named seeded user, and asserts the status, body and money amounts exactly to the decimal places of their currency.
05. **UI tester**: drives the web app with Playwright in a mobile viewport, against either canned API responses or the real backend, and asserts on page elements, text and navigation. A failed check saves a screenshot.
06. **reference checks**: compare ledger balances on each fixture date, income statement category totals, balance sheet balances and the amounts of each transfer between currencies against the expected-value fixtures.

Every tool reports each case as pass, fail or error, where error marks a check that could not run, such as a service that is down. Every tool writes a timestamped log with one structured record per case through one shared log writer, and exits with a non-zero code on any fail or error.

**closure criteria**

01. the environment check reports the state of every service and exits non-zero when any one is down.
02. one command resets the local database to seed data.
03. the database utility reads, writes and searches every table in the schema from the command line and as an importable module.
04. the API tester runs a whole case file or one named case, as a named seeded user, and its verdict for each case matches the pytest API tier for the same case.
05. the UI tester runs a check file in a mobile viewport in both canned-response and real-backend modes, and saves a screenshot for every failed or errored check. Each page also runs at a second phone width and a desktop width.
06. the reference checks report every fixture balance, category total and fx transfer amount with its expected and actual value.
07. every tool reports pass, fail or error per case, writes the shared structured log and exits non-zero on any fail or error, verified with one passing run and one run with a deliberate failure of each kind. Every check is shown to fail on a planted fault before it is trusted, and every tool applies the latency budgets.
08. every tool is tracked in git and reads its settings from `.env`.
09. the local dev and test env milestone's closing commands still pass unchanged.
10. the `redbooks-deploy-and-validation-cycle` skill, written in the agent skills implement customization milestone, names each tool, when to use it and its command.
11. a tool that writes into the user's working database refuses to run without the second opt-in, and backs the database up first.

## Oauth login

This milestone adds sign-in with OAuth and scopes every record to its owner. A user signs in through the OAuth provider, and RedBooks creates their user record on first sign-in. Every account, category and transaction belongs to one user, and the API returns only the signed-in user's data.

**database**

The schema holds users, their linked OAuth identities and their sessions. Every user-owned table carries an owner reference to the user. Each user holds a timezone setting, Asia/Singapore by default, which sets today's date for new entries and the month boundaries of every statement.

01. the user, identity and session tables exist with their keys and constraints, per the data model design.
02. every user-owned table has a required owner reference, and a record without an owner is rejected by the database.
03. the seed data holds two users with distinct data.
04. each user record holds an IANA timezone name, set to Asia/Singapore at first sign-in, and the database rejects a name outside the timezone database.

**api endpoints**

The endpoints cover sign-in, the OAuth callback, sign-out and the current user. Every data endpoint requires a valid session and scopes its reads and writes to the signed-in user.

01. sign-in redirects to the OAuth provider, and the callback creates the user on first sign-in and links the identity on later sign-ins.
02. sign-out ends the session, and a later request with that session is rejected.
03. every data endpoint rejects a request without a valid session. An unknown path under the API prefix answers 401 to a signed-out request, every token validation error answers 401, and boundary cases account for the library's clock leeway.
04. a request for another user's record returns not found, verified for every resource and verb as the second seeded user.
05. automated tests sign in through a local stub OpenID Connect provider, through the real sign-in endpoint and callback. A live check confirms the real provider's discovery document and sign-in redirect without signing a real account in.

**front end pages and behaviors**

The sign-in page starts the OAuth flow, and every other page requires a signed-in user. The page header shows the signed-in user and a sign-out action.

01. the sign-in page signs the user in through the OAuth provider in the mobile layout.
02. opening any page without a session leads to the sign-in page, and signing in returns the user to the page they opened.
03. sign-out returns the user to the sign-in page.
04. automated browser tests sign in through the stub identity provider, then make live calls for everything except irreversible writes. The full live OAuth flow with its writes is the user's test.
05. the settings page shows the user's timezone and saves a new one picked from a searchable list.

## Audit skills checkpoint

This milestone runs once the design, the foundation and the first feature are built. It reads every `lesson observation` and experiment result the trackers have recorded so far, trials the skill changes they suggest against a control, and promotes or drops each lesson to be learned whose evidence is in, such as the route table tests of LT.01, the mode check of LT.03 and the rate API probe of LT.08. The four remaining feature milestones then start from the promoted rules. Lessons still open carry forward to the audit skills promote learning milestone.

**closure criteria**

01. every `lesson observation` and experiment result recorded so far is listed with its lesson and its tracker.
02. each lesson to be learned with settling evidence is promoted into a skill rule or reference lesson, or dropped, and its status is updated in the **lessons learned**.
03. each skill change is trialled against a control before it is promoted, and only a failing control with a passing experiment counts.
04. every changed skill and agent passes a documentation style review, and every agent still carries the identical shared boundaries block.

## Currency model

This milestone builds the currency foundation the ledger and the financial statements rely on, with the same currency management the user has in HomeBudget. Each user manages their own list of currencies. Adding a currency picks it from the catalog of available currencies, and a currency the user no longer needs can be removed. The catalog is the list of currencies the rate API supports, the same API the **homebudget wrapper** uses, so every currency a user adds has exchange rates available. The milestone also covers the money type with exact decimal arithmetic and the user's reporting currency setting, chosen from the user's currencies.

Each exchange rate is fetched once for a currency pair and date, stored, and served from storage on every later request. A user can also record a rate by hand, which RedBooks stores next to the fetched one and uses in its place, so a rate defaults to the live fetched value and the user can override it, per AR.12 of the **accounting rules**. The rate client builds on the findings of design task 04.19, the exchange rate API probe, and its stubs come from the probe's saved responses.

**database**

The schema holds the currency catalog, each user's currencies, the exchange rates, and each user's reporting currency setting. A currency in the catalog carries its code, name and number of decimal places. A user's currency follows the HomeBudget currency record, with its code, name and locale. Exchange rates are stored by currency pair and date with their source. Amounts and rates use exact decimal column types.

01. the currency catalog, user currency and exchange rate tables and the reporting currency setting exist with their keys and constraints, per the data model design.
02. each user currency references one catalog currency, and each user holds a given currency once.
03. the catalog holds every currency the rate API supports, loaded from the rate API's currency list.
04. each exchange rate is unique per currency pair, date and source, and records whether it was fetched or entered by the user.
05. rate columns hold the full precision the rate API returns, and a round trip through the database utility returns every rate unchanged.
06. the seed data holds SGD and USD as the seed user's currencies, SGD as the reporting currency, and stored USD to SGD rates for every date the seed data needs.

**api endpoints**

The endpoints list the currency catalog, list, add and remove the user's currencies, read and set the reporting currency, return the exchange rate for a currency pair and date, record a user rate, and convert an amount between two currencies on a date. Conversion uses the money type, and rounds the converted amount to the target currency's decimal places.

01. every endpoint covers the case set in the test strategy: required fields, validation errors, a missing record, the happy path, a request without a session and another user's record.
02. the catalog endpoint returns every currency the rate API supports, with its code and name.
03. adding a currency accepts only a catalog currency the user does not already hold, and the new currency appears in the user's list.
04. removing a currency deletes it from the user's list. A currency held by one of the user's accounts, or set as the reporting currency, is kept, and the response names what still uses it.
05. the reporting currency accepts only one of the user's currencies, is stored per user and is returned on the next read.
06. a request for a rate not yet stored fetches it from the rate API once, stores it and returns it, and every later request for the same pair and date is served from storage.
07. a user rate for a pair and date takes the place of the fetched rate in every conversion for that user.
08. converting an amount returns the exact result of the stored rate, rounded to the target currency's decimal places, checked against oracle values.
09. a rate API failure returns a clear error and leaves the catalog and stored rates unchanged, verified against the stubbed rate API. The rate client sets explicit timeouts and names each failure cause with a fix, and the fetch job always reaches a terminal status with its original exception recorded.

**front end pages and behaviors**

The pages cover the currencies page and the exchange rates page, in the phone layout. The currencies page lists the user's currencies, adds a currency from the catalog, removes a currency and sets the reporting currency. The exchange rates page lists the stored rates and lets the user record a rate by hand.

01. the currencies page lists the user's currencies with their code and name, and marks the reporting currency.
02. adding a currency opens a searchable list of the catalog currencies the user does not yet hold, and the chosen currency appears in the user's list.
03. removing a currency asks for confirmation first. A currency still in use stays in the list, with a message naming the accounts or setting that use it.
04. the user sets the reporting currency by choosing one of their currencies.
05. every account form offers only the user's currencies.
06. the exchange rates page lists stored rates by currency pair and date, with the source of each rate.
07. the user records a rate for a currency pair and date, and the list shows it as a user rate in place of the fetched one.
08. every page shows amounts to the decimal places of their currency, and rates to their stored precision.
09. a failed rate fetch shows a message on the page and keeps the last stored rates on screen.

## Txn and accounts

This milestone builds the ledger and transaction entry. Every account keeps its entries in the general ledger, with an opening balance on its own date. The user adds, edits and deletes expenses, income and transfers from the phone-layout pages. A transfer links two ledger entries, one on each account, with an amount in each account's currency. An expense or an inflow posts directly on any asset or liability, and a refund reverses its category on the account that receives it. The cost center is an optional clearing account for splits: a split purchase is recorded as one expense per category in the cost center account plus a transfer from the payment account for the total. Billing accounts return to zero when settled. These follow AR.05 to AR.08 of the **accounting rules**. Each account holds one of the user's currencies from the currency model. Amounts use the money type. A reporting currency account accepts an expense or income in any of the user's currencies and posts the converted amount to its ledger. A foreign currency account accepts only its own currency. The record keeps the nominal currency, the nominal amount and the rate. A card's foreign exchange fee is a separate expense on the same card, per AR.12 of the **accounting rules**. Transfers between currencies and entries in another currency take their rate from the currency model.

**database**

The schema holds accounts with their type, currency and opening balance, the two-level consolidated category model of categories and their subcategories, the general ledger entries, and the expense, income and transfer records built on them. Amounts use exact decimal column types, and each account's currency references one of the user's currencies in the currency model.

01. the account, category, subcategory, ledger entry, expense, income and transfer tables exist with their keys and constraints, per the data model design.
02. every subcategory belongs to exactly one category, and every expense and income record references one subcategory.
03. every expense and income record references exactly one ledger entry, and every transfer references two ledger entries on two different accounts.
04. every expense and income record stores its entered currency, entered amount and exchange rate. When the entered currency is the account's currency, the rate is 1 and the ledger amount equals the entered amount.
05. amount columns use exact decimal types, and a round trip through the database utility returns every amount unchanged to the decimal places of its currency.
06. the database rejects a ledger entry whose currency differs from its account's currency.
07. every account's currency references one of its owner's currencies, so a currency held by an account stays in the user's list.
08. an account or category with posted transactions is retired, never deleted.
09. every single-active rule is a partial unique index.

**api endpoints**

The endpoints create, read, update and delete accounts, categories, subcategories, expenses, income and transfers, list transactions by account, category and subcategory, and report account balances on a date. Writes that touch the ledger run in one database transaction, so a transfer writes both of its entries or neither.

01. every resource endpoint covers the case set in the test strategy: required fields, validation errors, a missing record, the happy path, a request without a session and another user's record.
02. creating, editing or deleting an expense, income or transfer updates the ledger entries it owns in the same database transaction.
03. a transfer between two currency pairs, such as SGD and USD accounts stores the amount in each account's currency, each to the decimal places of its currency.
04. the account balance for any date equals a reconciled balance point plus the signed entries between the two dates, and the opening balance is the account's first reconciled balance point.
05. a split purchase leaves the payment account balance equal to the total purchase amount on the statement.
06. a transfer between currencies stores the rate it used. The default rate comes from the currency model for the transfer date, with the user's recorded rate in place of the fetched one where one exists. An override the user makes on the transfer is stored on that transfer only and leaves the currency model's rates unchanged.
07. creating or editing an account accepts only one of the user's currencies.
08. creating or editing an expense or income accepts only a subcategory of the user's own categories, and listing by category returns the transactions of all its subcategories.
09. an expense or income in a currency other than the account's currency is accepted only on a reporting currency account, and only in one of the user's currencies. A foreign currency account rejects it. Its ledger amount equals the entered amount times the rate, rounded to the account currency's decimal places, checked against oracle values.
10. the default rate for an entry in another currency comes from the currency model for the entry date, with the user's recorded rate in place of the fetched one where one exists. An override of the rate or of the account currency amount is stored on that entry only.
11. editing the entered amount, currency or rate of an expense or income updates its ledger entry in the same database transaction.
12. a card charge billed above its converted amount records the difference as a separate foreign exchange fee expense on the same card.
13. every ledger write goes through the ledger service that enforces its invariants.

**front end pages and behaviors**

The pages cover the account list with balances, an account ledger, the category list with its subcategories, the transaction list, a detail page for each account, category, subcategory, expense, income and transfer, and entry forms for expenses, income and transfers, all in the phone layout. A transfer between currencies fills in its paired amount from the currency model's rate for the transfer date, which the user can override on the transfer.

01. the user creates, edits and deletes accounts, categories, subcategories, expenses, income and transfers from the web app.
02. the account list shows each account's current balance in its own currency organized by account type. clicking on an account opens up the account detail page with option to edit account attributes.
03. the account ledger lists the account's transactions in a monthly view by date with a running balance. User can page through back and next or select ledger for a given month.
04. the transaction list filters by account, category, subcategory and month or custom date range.
05. the category list shows each category with its subcategories nested beneath it. clicking on a category opens the category detail page with its attributes, an option to edit them, and its subcategories with their totals for the selected month. clicking on a subcategory opens the subcategory detail page with its attributes, an option to edit them, and its transactions for the selected month with their total.
06. clicking on an expense in a ledger or transaction list opens the expense detail page, showing its date, amount, account, category and subcategory, payee and notes, with options to edit and delete it.
07. clicking on an income opens the income detail page, showing its date, amount, account, category and subcategory, and notes, with options to edit and delete it.
08. clicking on a transfer opens the transfer detail page, showing its date, the from and to accounts, the amount in each account's currency, the exchange rate for a transfer between currencies, and its notes, with options to edit and delete it. Editing or deleting a transfer changes both of its ledger entries together.
09. every detail page links to the detail page of each account, category and subcategory it shows, and a delete asks for confirmation first. Saving or deleting returns the user to the list they came from, with balances and totals updated.
10. when the two accounts hold different currencies, the paired currency amount and rate are filled in from the currency model's exchange rate for the transfer date.
11. for forex transfers, the user has an option to over-ride either the pair amount or the exchange rate and the other value updating based on the over-ride decision. The override applies to that transfer only.
12. the expense and income forms pick a category and then one of its subcategories. On a reporting currency account, the forms also offer a currency picker listing the user's currencies, set to the account's currency by default. On a foreign currency account, the currency is fixed to the account's currency. Choosing another currency fills in the rate from the currency model and shows the amount in the account's currency, and the user can override either the rate or that amount, with the other value updating to match.
13. the expense and income detail pages show the entered amount and currency, and for an entry in another currency, the rate and the amount in the account's currency.
14. the account form offers only the user's currencies, from the currencies page.
15. amounts display to the decimal places of the account's currency, and every form rejects an invalid amount with a message on the field.
16. after a save or delete, every view showing the changed data refreshes, and fields the user is editing keep their input.

## Financial statements

This milestone builds the income statement and the balance sheet from the ledger. Each statement has two views. The year view shows the twelve months of a year side by side, and the month view shows one month in detail. Clicking a month in the year view opens the month view for that month, and clicking a line in the month view opens the transactions that make it up. The statements report in the user's reporting currency, set on the currencies page of the currency model.

A closed month is reported from a stored snapshot. On the 1st of every month, in the user's timezone, a snapshot job generates and stores the snapshot of the month before, holding both statements for that month in the reporting currency. The job runs inside the backend, at start and every hour, so a month whose 1st passed while the laptop was off is picked up on the next start. The current month is a month to date run, built on request and never stored. A re-run of a past month stores a new version and keeps the old ones, as a slowly changing dimension of type 2, and every report shows the newest version. Every write to a transaction, rate or opening balance that a snapshot covers marks that snapshot stale, and the user sees which lines drifted, views the changes and re-runs the month. Changing the reporting currency takes confirmed warnings and a choice of past years to regenerate in the new currency. Snapshots in the old currency stay in the history, which lists statements by year, then by currency where a year has more than one, then by month. The seed load and the account `01` migration generate a snapshot for every month they load, and the migration validation checks them.

The income statement follows the two-level category model. Each category line totals the subcategory lines beneath it, for income and for expenses. The balance sheet shows each account at its balance converted with the currency model's rates, grouped by account asset class, with the forex gain or loss as its own line. Both statements export to CSV from either view. The income statement shows expenses as positive amounts only when it is presented. The books, the API and every oracle hold signed entries, per AR.18 of the **accounting rules**.

**database**

Statements are built from the ledger, the category model, a reporting currency and the stored exchange rates of the currency model. The schema adds the account type grouping the balance sheet uses, the statement snapshots with their versions and lines, the snapshot job runs, and the ledger change log.

01. every account type maps to one balance sheet group, per the data model design.
02. the stored exchange rates cover every month-end date the seed data statements need.
03. each snapshot version is keyed by user, month and reporting currency, with its run kind, run time, valid from and valid to times, and stale flags for each statement. A partial unique index allows one current version per key.
04. each snapshot stores every line of both statements, the forex gain or loss, net worth and the rates it used, as exact decimals.
05. every ledger, rate, opening balance and category write records a change log row with its before and after values in the same database transaction.

**api endpoints**

The endpoints return the income statement and the balance sheet for a year, with a value for each month, and for a single month. They also return the transactions behind any month view line, and the CSV export of each view and of the transaction list.

01. the income statement month view matches its expected totals by category and subcategory for a seed data month.
02. the income statement for the snapshot period matches the expense total HomeBudget holds for each subcategory in the snapshot.
03. every category line equals the sum of its subcategory lines, in both views.
04. the balance sheet month view matches its expected account balances and net worth at the end of a seed data month.
05. each month in the year view equals the matching month view, for both statements, and the income statement year total equals the sum of its twelve months.
06. the forex gain or loss line matches its expected value for each month with USD balances.
07. changing the reporting currency on the currencies page converts every statement line using the currency model's rates for the statement dates, with the user's recorded rates in place of fetched ones where they exist.
08. each transfer between currencies keeps its own stored amounts in the ledger, and the statements convert account balances with the currency model's rates.
09. the drill down for every month view line returns exactly the transactions that sum to that line.
10. each CSV export holds the same values as the matching view or transaction list response. A closed month's export carries the snapshot values and its version time.
11. each statement labels its population and period, and its source: the snapshot version and run time, or month to date for the incomplete current period.
12. the snapshot job generates each closed month with no snapshot once, in the user's timezone and current reporting currency, at backend start and every hour, catching up every month missed while the app was down. Each run reaches a terminal status with its original exception recorded on failure.
13. a closed month reads its current snapshot version, and the month to date run is built on request and never stored.
14. a re-run stores a new version that becomes current, closes the version before it with its valid to time, and leaves every older version retrievable unchanged.
15. a write dated in a month marks that month's income statement snapshot stale, and the balance sheet snapshots of that month and every later month. A stale view returns each line's snapshot amount, current amount and difference, and the changes endpoint returns every change log row since the snapshot ran that the month's statements include.
16. a reporting currency change regenerates every closed month of the years the user checks, and always the current year, in the new currency. Snapshots in the old currency stay current for their own currency and stay retrievable.
17. the history returns every snapshot grouped by year, then by reporting currency where a year holds more than one, then by month, with each month's current version, version count and stale flags.
18. the seed load and the account `01` migration generate a snapshot for every month they load, and the reference checks compare those snapshots with the HomeBudget reference figures.

**front end pages and behaviors**

The pages show the year view and the month view of the income statement and the balance sheet, the statement history, the snapshot versions and changes, and the reporting currency change, in the phone layout. Each view has a year or month picker, the reporting currency with a link to the currencies page, and a CSV export action.

01. the year view of the income statement shows each category, with its subcategories beneath it, and the amount for each month of the year and the year total.
02. the year view of the balance sheet shows each account, grouped by asset class, with its balance at the end of each month of the year, and net worth for each month.
03. the user moves back and forward a year, or picks a year, and the year view updates to match.
04. clicking a month in the year view opens the month view for that month.
05. the month view of the income statement shows each category with its subcategories beneath it and their amounts for the month. The month view of the balance sheet shows each account's balance at the end of the month and net worth.
06. the user moves back and forward a month, or returns to the year view, from the month view.
07. clicking a line in the month view opens the transactions that make it up.
08. the forex gain or loss shows as its own line on the balance sheet, in both views.
09. each statement shows its reporting currency, and after a reporting currency change, the month to date view and every regenerated month show the converted values, and the months left unregenerated show their own currency.
10. the export action downloads a CSV holding the values shown on screen, for the view on screen.
11. every statement view shows its source, the snapshot version and run time or month to date, and marks a stale month on the year view, the month view and the history.
12. a stale line shows its snapshot amount, current amount and difference. The snapshot changes page lists every change since the snapshot ran, and re-run offers this month and every later stale month.
13. the statement history page lists years, then reporting currencies where a year has more than one, then months. The versions page lists every version of a month, and an older version opens read-only with a link to the current one.
14. changing the reporting currency runs through the reporting currency change page: confirmed warnings, a checkbox list of past years with the current year locked, a second confirmation, and the regenerate job's progress.

## Homebudget account 01 migrate

This milestone migrates the user's HomeBudget account `01` history into their working RedBooks database. The account `02` snapshot is already the seed, so this milestone carries the older history that account `02` does not hold. It starts only after every feature milestone is validated and tested, so the large account `01` data is migrated as few times as possible. Its first task adopts versioned forward migrations, so the working database keeps its data across every later schema change. The migration loads the account `01` rows dated 2017-01-01 to 2026-05-23, from the reset of the account `01` cost centers to the last day of account `01`, and leaves out the retired accounts that have no activity in that scope. It maps the account `01` legacy categories onto the income statement lines through the explicit mapping of the legacy HomeBudget and financial statements workbooks, and keeps the account `01` cost center clearing history, per AR.07 of the **accounting rules**. At its start, each account held in both accounts resets its reconciled point to its last account `01` point, and the reconcile scope runs from that point to the next reconciliation. The load uses upsert logic: it matches each account, category, transaction and transfer against what the user already holds by the match key from the HomeBudget data review, adds the records that are new, and skips the records already present. Identical transactions on the same day are separate records, each with its own key. The migration writes into the user's working database only with a second opt-in, after a backup, and checks its results against the reference figures the HomeBudget data review sets for account `01`.

**closure criteria**

01. versioned forward migrations are in place, the app checks the migration head at startup, and a deliberately skipped step fails a check.
02. one command migrates the account `01` history into a user. It refuses to write without the second opt-in, and backs up the working database first.
03. every account `01` category and subcategory maps to one income statement line of the financial statements design, through the legacy workbook mapping, and the mapping lists any it could not map.
04. every account `01` row is loaded, skipped as already present, or listed in the migration report with the rule that handled it, and the report counts the records added and skipped for each kind.
05. records that overlap the account `02` seed match by the match key, and no duplicate account, category or transaction is created.
06. identical transactions on the same day each load as their own record.
07. running the migration a second time adds zero records and leaves every balance and total unchanged.
08. each migrated cost center matches its HomeBudget balance at every month end in the scope.
09. migrated balances and category totals match the account `01` reference figures, checked by the validation utilities.
10. the migration job reaches a terminal status with its original exception recorded on failure, and commits its progress as it goes.
11. the migration loads only rows dated 2017-01-01 to 2026-05-23, and no retired account.
12. each account held in both accounts carries its last account `01` reconciled point after the migration, and its balance from that point to the next reconciliation is reported as the open reconcile scope.

**tasks**

| id    | seq | status  | task                                                   |
| ----- | --- | ------- | ------------------------------------------------------ |
| 12.01 | 01  | pending | account 01 category mapping from the legacy workbooks  |
| 12.02 | 02  | pending | reconcile bridging between account 01 and account 02   |

01. **12.01** capture the `cat_map` region of the HomeBudget workbook and the `fin_expense_cat_map` region of the financial statements workbook, whose ids are in `data/gsheets.json`, so every account `01` pair in the scope reaches its line, and settle whether the balancing and reimbursable categories are expense categories or clearing accounts.
02. **12.02** reset each account held in both accounts to its last account `01` reconciled point, mostly from February or March 2026, and carry the difference to the account `02` records through the reconcile scope until the next reconciliation settles it.

## Audit skills promote learning

This milestone reviews what the agents learned during the release and folds it into the shared skills. It collects the lessons recorded in feature trackers, logs and issues, and updates the skills and agents so the next release starts from them. It starts from the results of the audit skills checkpoint and covers the observations recorded since.

**closure criteria**

01. every `lesson observation` and experiment result since the checkpoint is read, each remaining lesson to be learned is promoted or dropped, and its status is updated in the **lessons learned**.
02. each lesson is applied to a skill or agent, or recorded as no change with a reason.
03. every changed skill and agent passes a documentation style review.
04. each skill change is trialled against a control before it is promoted.

## Mkdocs documentation

This milestone writes and publishes the RedBooks documentation site. It covers the developer guide for setup, running, testing and debugging, and the user guide for each workflow in the phone-layout web app. A GitHub Actions workflow builds the site with mkdocs and publishes it on every merge to `main`.

**closure criteria**

01. the developer guide covers setup, configuration, running, testing and debugging.
02. the user guide covers sign-in, accounts, categories, transactions, transfers, financial statements and CSV export.
03. the GitHub Actions workflow publishes the site on merge to `main`.
04. the site builds in strict mode, which fails on every broken link and anchor, and published pages carry no release references. The workflow and token prerequisites are listed as user actions.
05. published pages show no real account names or personal details, only hypothetical names at real Singapore institutions, and the build includes no data file.

## Publish and release

This milestone ships `0.2.0`. The `dev` branch merges to `main` through a pull request, and the merge is tagged `0.2.0`. The release page is finalized with the as-built scope and links to the documentation site.

**closure criteria**

01. every milestone above is closed.
02. the full test suite passes on the release commit, run from a clean worktree of that commit.
03. the release page states the as-built scope and links to the documentation site, developer guide and user guide.
04. `VERSION` reads `0.2.0` and the release commit carries the `0.2.0` tag.

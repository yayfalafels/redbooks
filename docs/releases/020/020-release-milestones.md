# RedBooks - Release 0.2.0 Milestones

## Contents

- [Feature milestones](#feature-milestones)
- [References](#references)
- [Requirements](#requirements)
- [Agent skills customization](#agent-skills-customization)
- [Test strategy](#test-strategy)
- [Test cases](#test-cases)
- [Design](#design)
- [Agent skills implement customization](#agent-skills-implement-customization)
- [Local dev and test env](#local-dev-and-test-env)
- [Validation utilities](#validation-utilities)
- [Setup database seed data](#setup-database-seed-data)
- [Oauth login](#oauth-login)
- [Currency model](#currency-model)
- [Txn and accounts](#txn-and-accounts)
- [Financial statements](#financial-statements)
- [Data migrate](#data-migrate)
- [Audit skills promote learning](#audit-skills-promote-learning)
- [Mkdocs documentation](#mkdocs-documentation)
- [Publish and release](#publish-and-release)

## Feature milestones

The `seq` column determines the implementation order

| id | release | seq | status   | feature                                  |
| -- | ------- | --- | -------  | ---------------------------------------- |
| 01 | 020     | 01  | closed   | requirements                             |
| 05 | 020     | 02  | open     | agent skills customization               |
| 02 | 020     | 03  | pending  | test strategy                            |
| 03 | 020     | 04  | pending  | test cases                               |
| 04 | 020     | 05  | pending  | design                                   |
| 16 | 020     | 06  | pending  | agent skills implement customization     |
| 06 | 020     | 07  | pending  | local dev and test env                   |
| 08 | 020     | 08  | pending  | validation utilities                     |
| 07 | 020     | 09  | pending  | setup database seed data                 |
| 09 | 020     | 10  | pending  | oauth login                              |
| 17 | 020     | 11  | pending  | currency model                           |
| 10 | 020     | 12  | pending  | txn and accounts                         |
| 11 | 020     | 13  | pending  | financial statements                     |
| 12 | 020     | 14  | pending  | data migrate                             |
| 13 | 020     | 15  | pending  | audit skills promote learning            |
| 14 | 020     | 16  | pending  | mkdocs documentation                     |
| 15 | 020     | 17  | pending  | publish and release                      |

## References

- **release roadmap**: [../../release-roadmap.md](../../release-roadmap.md)
- **requirements**: [../../requirements.md](../../requirements.md)
- **release milestones**: [020-release-milestones.md](020-release-milestones.md)
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

The requirements milestone sets what `0.2.0` delivers and why. It records the lessons from **financial-statements 010** and easyMCF, fixes the scope in the **release roadmap**, audits that scope, and writes the release notes in the release page. It captures a snapshot of the user's HomeBudget accounts and transactions, exported from the HomeBudget app into the gitignored `data/` folder. The snapshot and the **homebudget wrapper** source code are the two sources of HomeBudget information for the release. The snapshot supplies the data, and the wrapper source code documents how HomeBudget structures accounts, transactions, transfers and currencies. Figures available only in the live HomeBudget app are written by the user into two files alongside the export. The account balances file holds the HomeBudget accounts with their starting balances, and the opening balance of each month and the closing balance on the snapshot date for select accounts. The fx transfers file holds both sides of every transfer between currencies, with the amount in each currency and the exchange rate HomeBudget applied. The automated validation reads both files as expected values.

**closure criteria**

01. the **release roadmap** lists every `0.2.0` feature and the release each later feature belongs to.
02. every requirements audit issue has a recorded response, and the response is applied to the release notes and the roadmap.
03. the release notes describe the ledger, categories, multiple currencies, financial statements, users, mobile layout and HomeBudget history for `0.2.0`.
04. the HomeBudget snapshot in `data/` holds the full transaction report, the account balances file and the fx transfers file.
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
| 01.08 | 09  | open     | deliverables and closing criteria        |

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

Skills load in stages. The rules that apply every time go in the skill's `SKILL.md`, and detailed lessons and worked examples go in reference files in the skill folder. `SKILL.md` names each reference file and when to read it, so an agent reads a lesson at the moment it applies. A lessons inventory, `020-easymcf-lessons.md` in this release folder, lists each lesson with its source and the skill and file it moved to.

**closure criteria**

01. every agent in `.claude/agents/` describes a RedBooks role and lists the generic skills it loads.
02. every generic skill listed above exists in `.claude/skills/` and holds no RedBooks-specific names, paths or design decisions.
03. every skill with RedBooks-specific content carries the `redbooks-` prefix.
04. the `webscraping` skill and the MCF-specific content are removed from `.claude/`.
05. a search of `.claude/` for easyMCF, MCF, Flask, SQLite and AngularJS returns no matches.
06. the lessons inventory lists every lesson from the easyMCF sources above, with its destination skill and file, or a reason it stays with easyMCF.
07. every transferred lesson is written in RedBooks stack terms and readable with the easyMCF repo absent.
08. every reference file in a skill folder is named in that skill's `SKILL.md`, with when to read it.

## Test strategy

The test strategy sets how every part of the `0.2.0` release is proven to work as delivered. It covers the ledger and money rules, the data model, the API, the web app in its phone layout, sign-in and data ownership, exchange rates, financial statements, the HomeBudget migration and the local environment. The test cases milestone turns this strategy into concrete cases, and every feature milestone builds and validates against it.

**Guiding principle**

Each component is tested where its logic lives, in isolation, before the tests of how components fit together. A rounding error in the money type, a wrong ledger balance or a missed forex line is a unit defect, caught by a fast test of that unit alone. End-to-end tests through the web app confirm the wiring between components once each component is proven. This order gives an agent a narrow, fast and deterministic signal on every change, and keeps the slower browser tests for integration.

**Component silos**

Each component has its own silo, a way to test it directly with no other component's correctness as a precondition and no live network call.

01. **ledger and money**: unit tests on the money type, exact decimal arithmetic, ledger balance calculation, expense, income and transfer posting rules, split purchases and transfers between currencies.
02. **data model and database**: schema migrations, constraints and round trips through a direct database utility, run against a temporary PostgreSQL database before any API exists on top.
03. **backend API**: endpoint cases written as data, each tagged with the requirement it proves, run through the FastAPI test client. Each endpoint covers required fields, validation errors, missing records, the happy path, a request without a session and a request for another user's record.
04. **exchange rates**: rate fetching and storage tested against a stubbed rate API, and conversion and forex gain or loss tested against fixed stored rates.
05. **financial statements**: the income statement, the balance sheet, the forex gain or loss line, drill down and CSV export, tested at the service layer against known ledger data.
06. **frontend**: the React pages tested in a mobile viewport with Playwright, with every API call answered from canned responses, so a rendering defect and a backend defect fail in different silos.
07. **authentication and ownership**: OAuth sign-in against a stub identity provider, with two seeded users in every database, so a data leak between users always has a second user to show up in.
08. **HomeBudget migration**: report parsing, account and category mapping, fx transfer matching and every migration rule, tested against the snapshot files.

**Case selection**

01. **traceability**: every requirement in the release notes has at least one tagged test case. A requirement with no case counts as untested.
02. **closed vocabularies**: every account type, transaction kind and transfer kind has a reachable case, and the seed data holds at least one row of each.
03. **boundaries**: every date and period rule gets a case on each side of its boundary, such as a transaction on the first and last day of a statement period.
04. **determinism**: no test depends on wall-clock time, a live network call or a fixed sleep. Time comes through a single injectable clock and exchange rates come from stored or stubbed values.
05. **silo-first order**: a feature writes its cases cheapest first, from unit and database cases through API and frontend cases, and adds an end-to-end case where a real integration risk remains.
06. **ownership leaks**: every resource is tested as a second user against the first user's records, and every result is a not found response or an empty list.

**Independent verification layers**

Each feature milestone validates its closure criteria through independent layers, so no layer grades its own work.

01. **self-report**: the validation utilities replay case files against a running app and report pass or fail per case.
02. **direct inspection**: the database utility reads what a request wrote, independent of the API response.
03. **oracle**: tests with hard-coded expected values taken from the closure criteria and the reference data, never from the code under test.
04. **human validation**: a person walks through the running app on a phone or in the mobile emulator, following a checklist from the milestone's closure criteria, once every automated layer passes.

Tests run in order of speed and information value. Unit, database and API cases run first, then browser cases, then the human pass. When failures appear, independent first failures are separated from the failures they cause and fixed one at a time, and the full suite then runs again as confirmation.

**Reference data from HomeBudget**

The HomeBudget snapshot is the reference data behind the oracle layer for the ledger, the statements and the migration. The budget section of the report gives each category's expense total for the period, and the income statement matches these totals. The account balances file gives monthly opening balances and the snapshot date closing balance for select accounts, and the ledger balances and the balance sheet match these values. The fx transfers file gives both amounts of every transfer between currencies, and each transfer posts exactly those amounts. The seed script writes these expected values as fixtures next to the seed data, under the same made-up names, with amounts and dates unchanged.

**closure criteria**

01. the test strategy doc defines each component silo, its tools, its scope and the data it runs against.
02. every requirement in the release notes maps to at least one silo, and the test cases milestone has a traceability rule to follow.
03. the strategy defines the case selection rules, the independent verification layers and the test run order.
04. the strategy defines how money amounts are asserted exactly to the decimal places of their currency and how exchange rates are stubbed and stored.
05. the strategy defines the stub identity provider for OAuth and the two-user ownership tests.
06. the strategy defines frontend testing with canned API responses in a mobile viewport, and the human pass on a tunnelled phone or in the mobile emulator.
07. the strategy maps each HomeBudget snapshot file to the results it validates and defines the expected-value fixtures the seed script writes.
08. the strategy defines the agent's build, test and debug loop, naming the narrowest silo to run first for each kind of change.
09. strategies and tools exist for agent to autonomously validate and self-correct errors from all of the component features of the released product, including: db, api endpoints and front end ui. human validation checks are secondary checks against implementation which has already passed an agent run validation check.

## Test cases

This milestone writes the concrete test cases the test strategy scopes, organized by component silo. Each case names its requirement, its silo, its verification layer, its input data and its expected result. The cases cover every requirement in the release notes, the case selection rules in the test strategy, and the edge cases found in the HomeBudget snapshot, such as same-day identical expenses, transfers between currencies, USD expenses, deposit refunds and prepaid card top-ups.

**closure criteria**

01. the test cases doc lists every case with its requirement, silo, verification layer, input and expected result.
02. every requirement in the release notes has at least one test case.
03. every closed vocabulary value, date boundary and ownership rule named in the test strategy has a test case.
04. every edge case recorded in the HomeBudget data review has a test case.
05. every feature milestone with a user-visible surface has a human validation checklist.
06. expected money amounts are stated exactly, to the decimal places of the currency of the account or statement they belong to.

## Design

The design settles how RedBooks meets the requirements before any feature code is written. It runs in three stages, each building on the one before.

01. **user experience**: the design starts from the user workflows, such as recording a transaction, transferring between accounts, reviewing an account ledger and reporting financial statements. The data flows follow from the workflows, naming every data source, store and output, from manual entry and the HomeBudget snapshot through the database to the statements and CSV exports. The front end pages then set the phone-layout screens, navigation and interactions that carry out each workflow.
02. **accounting model**: the HomeBudget data review works from the snapshot in `data/` and the **homebudget wrapper** source code. Together with the workflows, it forms the basis of the accounting data model. The model defines the general ledger with its expense, income and transfer models, accounts and account types, the consolidated category model, multiple currencies with the forex gain or loss, and the financial statements. The review maps HomeBudget accounts, account types, categories and transfer patterns into this model and records the migration rules.
03. **system**: the architecture sets the components and how they interact, on the tech stack and repo layout. Users and authentication, networking and security, the API endpoints, the local dev env, the env variables and the docs publishing pipeline complete the design.

Every design doc traces its decisions back to the requirements and forward to the test strategy and test cases.

**closure criteria**

01. every design topic below has a design doc marked closed, and each doc traces its decisions to the requirements it serves.
02. the workflows doc describes every user workflow in the release notes, step by step, with the pages and data each step uses.
03. the data flows doc names every data source, store and output, and the workflow that moves data between them.
04. the front end pages doc defines every page with its purpose, phone layout, fields, actions, navigation and the API calls it makes.
05. the data model defines every entity with its fields, types, keys, constraints and ownership, including the general ledger, the expense, income and transfer models, accounts with opening balances, categories, exchange rates and users.
06. the accounts, transactions, multi currency and forex, and financial statements docs define their rules and calculations in enough detail to write oracle test cases from them, including split purchases, transfers between currencies, the reporting currency setting, the rate source and storage, the rate applied to each statement line and the forex gain or loss.
07. the HomeBudget data review maps every HomeBudget account, account type and category into the data model, records a migration rule for every data quality issue in the snapshot, defines the upsert match key for each record kind, and documents the report, account balances and fx transfers file formats.
08. the architecture doc sets every component, its responsibility and its interfaces, and the tech stack and repo layout docs fix the libraries, versions and folder structure the implementation follows.
09. the users and authentication, and networking and security docs define the OAuth flow, session handling, per-user data scoping, the phone tunnel, and the handling of secrets and personal data.
10. the API endpoints doc defines every endpoint with its method, path, request, response, errors and the ownership rule it enforces.
11. the local dev env and env variables docs define the Docker services, setup commands and every environment variable, and the docs publishing pipeline doc defines the documentation build and publish workflow.
12. a design audit across the design docs, the requirements, the test strategy and the test cases has every finding resolved.

**tasks**

| id    | seq | status   | design topic                             |
| ----- | --- | -------  | ---------------------------------------- |
| 04.01 | 01  | pending  | workflows                                |
| 04.02 | 02  | pending  | data flows                               |
| 04.03 | 03  | pending  | front end pages                          |
| 04.04 | 04  | pending  | homebudget data review                   |
| 04.05 | 05  | pending  | data model                               |
| 04.06 | 06  | pending  | accounts                                 |
| 04.07 | 07  | pending  | transactions                             |
| 04.08 | 08  | pending  | multi currency and forex                 |
| 04.09 | 09  | pending  | financial statements                     |
| 04.10 | 10  | pending  | architecture                             |
| 04.11 | 11  | pending  | tech stack                               |
| 04.12 | 12  | pending  | repo layout                              |
| 04.13 | 13  | pending  | users and authentication                 |
| 04.14 | 14  | pending  | networking and security                  |
| 04.15 | 15  | pending  | api endpoints                            |
| 04.16 | 16  | pending  | local dev env                            |
| 04.17 | 17  | pending  | env variables                            |
| 04.18 | 18  | pending  | docs publishing pipeline                 |

## Agent skills implement customization

This milestone is the second pass on the agents and skills, run once the design is complete. It writes the bespoke `redbooks-` skills that turn the design decisions into the guidance agents follow while they build. Each bespoke skill cites the design docs it draws on and links to the generic skills it builds on, so the generic practice lives in one place and the bespoke skill records only how RedBooks applies it.

The bespoke skills for `0.2.0` are:

01. `redbooks-ledger`: the general ledger, the expense, income and transfer models, opening balances and split purchases. It builds on `accounting` and `postgresql`.
02. `redbooks-currency`: the money type, the reporting currency setting, the exchange rate API and storage, and the forex gain or loss calculation. It builds on `accounting` and `python`.
03. `redbooks-statements`: the income statement, the balance sheet, drill down and CSV export. It builds on `accounting`.
04. `redbooks-backend-api`: the RedBooks API endpoints, user-scoped data access and OAuth session handling. It builds on `fastapi` and `postgresql`.
05. `redbooks-frontend`: the RedBooks pages, navigation and phone layout. It builds on `react`.
06. `redbooks-homebudget-migration`: the HomeBudget export files and their report sections, the account and category mapping, and the migration rules from the HomeBudget data review.
07. `redbooks-deploy-and-validation-cycle`: the RedBooks local Docker run and verify loop, using the validation utilities. It builds on `pytest` and `playwright`.

**closure criteria**

01. every bespoke skill listed above exists in `.claude/skills/`, cites its design docs and links to the generic skills it builds on.
02. no bespoke skill repeats generic practice that its linked generic skill already covers.
03. each implementing agent lists the bespoke skills it loads alongside its generic skills.
04. every agent and skill references design docs by their current names and paths.

## Local dev and test env

This milestone builds the repeatable local environment. Docker Compose runs the PostgreSQL database, the FastAPI backend and the React web app on the developer's laptop. A tunnel connects a real phone to the local web app, and a mobile emulator on the laptop covers the same pages. Environment variables are set through a `.env` file.

**closure criteria**

01. one command starts the database, backend and web app from a clean clone.
02. the web app loads in a mobile emulator on the laptop and on a phone through the tunnel.
03. a `.env.sample` file lists every environment variable with a description.
04. the developer guide draft records the setup, start and stop steps.
05. the test runner executes an empty test suite in every tier.

## Validation utilities

This milestone builds the standalone tools that give every later feature a fast, repeatable pass or fail signal outside the pytest suite. The tools carry out the independent verification layers set in the test strategy: self-report through case replay against a running app, direct inspection of the database, and oracle checks against the reference data. They build on the scripts from the local dev and test env milestone and extend them in place. Feature milestones then add their own case files and checks to these tools, and write no new tools of their own.

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
05. the UI tester runs a check file in a mobile viewport in both canned-response and real-backend modes, and saves a screenshot for every failed or errored check.
06. the reference checks report every fixture balance, category total and fx transfer amount with its expected and actual value.
07. every tool reports pass, fail or error per case, writes the shared structured log and exits non-zero on any fail or error, verified with one passing run and one run with a deliberate failure of each kind.
08. every tool is tracked in git and reads its settings from `.env`.
09. the local dev and test env milestone's closing commands still pass unchanged.
10. the deploy and validation cycle skill names each tool, when to use it and its command.

## Setup database seed data

This milestone creates the schema and the seed data that tests and demos run on. The seed data follows the shape of the HomeBudget snapshot, covering its accounts and types, SGD reporting with USD accounts, the consolidated categories and about five months of transactions and transfers. A seed data generator script builds it from the snapshot. The same script writes the expected-value fixtures from the report's budget section, the account balances file and the fx transfers file.

**closure criteria**

01. database migrations create the full schema on an empty database.
02. one command loads the seed data into the local database and reloads it cleanly.
03. the seed data includes every edge case named in the test cases.
04. the seed data includes stored USD to SGD exchange rates for every date it needs, and each transfer between currencies carries the two amounts from the fx transfers file.
05. the expected-value fixtures hold the category totals, account balances, fx transfer amounts and section row counts from the snapshot.
06. the seeded data passes every expected-value check in the fixtures.

## Oauth login

This milestone adds sign-in with OAuth and scopes every record to its owner. A user signs in through the OAuth provider, and RedBooks creates their user record on first sign-in. Every account, category and transaction belongs to one user, and the API returns only the signed-in user's data.

**database**

The schema holds users, their linked OAuth identities and their sessions. Every user-owned table carries an owner reference to the user.

01. the user, identity and session tables exist with their keys and constraints, per the data model design.
02. every user-owned table has a required owner reference, and a record without an owner is rejected by the database.
03. the seed data holds two users with distinct data.

**api endpoints**

The endpoints cover sign-in, the OAuth callback, sign-out and the current user. Every data endpoint requires a valid session and scopes its reads and writes to the signed-in user.

01. sign-in redirects to the OAuth provider, and the callback creates the user on first sign-in and links the identity on later sign-ins.
02. sign-out ends the session, and a later request with that session is rejected.
03. every data endpoint rejects a request without a valid session.
04. a request for another user's record returns not found, verified for every resource and verb as the second seeded user.

**front end pages and behaviors**

The sign-in page starts the OAuth flow, and every other page requires a signed-in user. The page header shows the signed-in user and a sign-out action.

01. the sign-in page signs the user in through the OAuth provider in the mobile layout.
02. opening any page without a session leads to the sign-in page, and signing in returns the user to the page they opened.
03. sign-out returns the user to the sign-in page.
04. automated browser tests sign in through the stub identity provider set in the test strategy.

## Currency model

This milestone builds the currency foundation the ledger and the financial statements rely on, with the same currency management the user has in HomeBudget. Each user manages their own list of currencies. Adding a currency picks it from the catalog of available currencies, and a currency the user no longer needs can be removed. The catalog is the list of currencies the rate API supports, the same API the **homebudget wrapper** uses, so every currency a user adds has exchange rates available. The milestone also covers the money type with exact decimal arithmetic and the user's reporting currency setting, chosen from the user's currencies.

Each exchange rate is fetched once for a currency pair and date, stored, and served from storage on every later request. A user can also record a rate by hand, which RedBooks stores next to the fetched one and uses in its place.

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
09. a rate API failure returns a clear error and leaves the catalog and stored rates unchanged, verified against the stubbed rate API.

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

This milestone builds the ledger and transaction entry. Every account keeps its entries in the general ledger, with an opening balance on its own date. The user adds, edits and deletes expenses, income and transfers from the phone-layout pages. A transfer links two ledger entries, one on each account, with an amount in each account's currency. A split purchase is recorded as one expense per category in the cost center account plus a transfer from the payment account for the total. Each account holds one of the user's currencies from the currency model. Amounts use the money type. An expense or income can be entered in any of the user's currencies, as in HomeBudget. The record keeps the entered currency, the entered amount and the rate, and posts the converted amount to the account's ledger in the account's currency. Transfers between currencies and entries in another currency take their rate from the currency model.

**database**

The schema holds accounts with their type, currency and opening balance, the two-level consolidated category model of categories and their subcategories, the general ledger entries, and the expense, income and transfer records built on them. Amounts use exact decimal column types, and each account's currency references one of the user's currencies in the currency model.

01. the account, category, subcategory, ledger entry, expense, income and transfer tables exist with their keys and constraints, per the data model design.
02. every subcategory belongs to exactly one category, and every expense and income record references one subcategory.
03. every expense and income record references exactly one ledger entry, and every transfer references two ledger entries on two different accounts.
04. every expense and income record stores its entered currency, entered amount and exchange rate. When the entered currency is the account's currency, the rate is 1 and the ledger amount equals the entered amount.
05. amount columns use exact decimal types, and a round trip through the database utility returns every amount unchanged to the decimal places of its currency.
06. the database rejects a ledger entry whose currency differs from its account's currency.
07. every account's currency references one of its owner's currencies, so a currency held by an account stays in the user's list.

**api endpoints**

The endpoints create, read, update and delete accounts, categories, subcategories, expenses, income and transfers, list transactions by account, category and subcategory, and report account balances on a date. Writes that touch the ledger run in one database transaction, so a transfer writes both of its entries or neither.

01. every resource endpoint covers the case set in the test strategy: required fields, validation errors, a missing record, the happy path, a request without a session and another user's record.
02. creating, editing or deleting an expense, income or transfer updates the ledger entries it owns in the same database transaction.
03. a transfer between two currency pairs, such as SGD and USD accounts stores the amount in each account's currency, each to the decimal places of its currency.
04. the account balance for any date equals the opening balance plus the ledger entries up to that date.
05. a split purchase leaves the payment account balance equal to the total purchase amount on the statement.
06. a transfer between currencies stores the rate it used. The default rate comes from the currency model for the transfer date, with the user's recorded rate in place of the fetched one where one exists. An override the user makes on the transfer is stored on that transfer only and leaves the currency model's rates unchanged.
07. creating or editing an account accepts only one of the user's currencies.
08. creating or editing an expense or income accepts only a subcategory of the user's own categories, and listing by category returns the transactions of all its subcategories.
09. an expense or income entered in a currency other than the account's currency accepts only one of the user's currencies. Its ledger amount equals the entered amount times the rate, rounded to the account currency's decimal places, checked against oracle values.
10. the default rate for an entry in another currency comes from the currency model for the entry date, with the user's recorded rate in place of the fetched one where one exists. An override of the rate or of the account currency amount is stored on that entry only.
11. editing the entered amount, currency or rate of an expense or income updates its ledger entry in the same database transaction.

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
12. the expense and income forms pick a category and then one of its subcategories. The forms also offer a currency picker listing the user's currencies, set to the account's currency by default. Choosing another currency fills in the rate from the currency model and shows the amount in the account's currency, and the user can override either the rate or that amount, with the other value updating to match.
13. the expense and income detail pages show the entered amount and currency, and for an entry in another currency, the rate and the amount in the account's currency.
14. the account form offers only the user's currencies, from the currencies page.
15. amounts display to the decimal places of the account's currency, and every form rejects an invalid amount with a message on the field.

## Financial statements

This milestone builds the income statement and the balance sheet from the ledger. Each statement has two views. The year view shows the twelve months of a year side by side, and the month view shows one month in detail. Clicking a month in the year view opens the month view for that month, and clicking a line in the month view opens the transactions that make it up. The statements report in the user's reporting currency, set on the currencies page of the currency model.

The income statement follows the two-level category model. Each category line totals the subcategory lines beneath it, for income and for expenses. The balance sheet shows each account at its balance converted with the currency model's rates, grouped by account asset class, with the forex gain or loss as its own line. Both statements export to CSV from either view.

**database**

Statements are calculated from the ledger, the category model, the reporting currency setting and the stored exchange rates of the currency model when requested. The schema adds the account type grouping the balance sheet uses.

01. every account type maps to one balance sheet group, per the data model design.
02. the stored exchange rates cover every month-end date the seed data statements need.

**api endpoints**

The endpoints return the income statement and the balance sheet for a year, with a value for each month, and for a single month. They also return the transactions behind any month view line, and the CSV export of each view and of the transaction list.

01. the income statement month view matches its expected totals by category and subcategory for a seed data month.
02. the income statement for the snapshot period matches the expense total for each subcategory in the budget section of the HomeBudget report.
03. every category line equals the sum of its subcategory lines, in both views.
04. the balance sheet month view matches its expected account balances and net worth at the end of a seed data month.
05. each month in the year view equals the matching month view, for both statements, and the income statement year total equals the sum of its twelve months.
06. the forex gain or loss line matches its expected value for each month with USD balances.
07. changing the reporting currency on the currencies page converts every statement line using the currency model's rates for the statement dates, with the user's recorded rates in place of fetched ones where they exist.
08. each transfer between currencies keeps its own stored amounts in the ledger, and the statements convert account balances with the currency model's rates.
09. the drill down for every month view line returns exactly the transactions that sum to that line.
10. each CSV export holds the same values as the matching view or transaction list response.

**front end pages and behaviors**

The pages show the year view and the month view of the income statement and the balance sheet, in the phone layout. Each view has a year or month picker, the reporting currency with a link to the currencies page, and a CSV export action.

01. the year view of the income statement shows each category, with its subcategories beneath it, and the amount for each month of the year and the year total.
02. the year view of the balance sheet shows each account, grouped by asset class, with its balance at the end of each month of the year, and net worth for each month.
03. the user moves back and forward a year, or picks a year, and the year view updates to match.
04. clicking a month in the year view opens the month view for that month.
05. the month view of the income statement shows each category with its subcategories beneath it and their amounts for the month. The month view of the balance sheet shows each account's balance at the end of the month and net worth.
06. the user moves back and forward a month, or returns to the year view, from the month view.
07. clicking a line in the month view opens the transactions that make it up.
08. the forex gain or loss shows as its own line on the balance sheet, in both views.
09. each statement shows its reporting currency, and after the user changes it on the currencies page, both statements show the converted values.
10. the export action downloads a CSV holding the values shown on screen, for the view on screen.

## Data migrate

This milestone loads the full HomeBudget history into RedBooks from the snapshot in `data/`. The load uses upsert logic. It matches each account, category, transaction and transfer against what the user already holds in RedBooks, adds the records that are new and skips the records already present, so a later snapshot that overlaps an earlier one loads only its new records. The match key comes from the HomeBudget data review. Identical transactions on the same day, such as two equal coffee purchases, are separate records, so the key counts each occurrence and keeps them all. The migration script reads the exported report, the account balances file and the fx transfers file, splits the report into its expense, income, budget and transfer sections, applies the mapping and rules from the HomeBudget data review, takes the amount in each currency for every transfer between currencies from the fx transfers file, and writes accounts, opening balances, categories, transactions and transfers. It checks its results against the totals in the exported report and against the balances in the account balances file.

**closure criteria**

01. one command migrates the HomeBudget snapshot into a user, whether the user holds no data or data from an earlier migration.
02. every HomeBudget row is either loaded, skipped as already present, or listed in the migration report with the rule that handled it, and the report counts the records added and skipped for each kind.
03. the expense total for each category matches the actual spend in the budget section of the exported report.
04. running the migration a second time on the same snapshot adds zero records and leaves every balance and total unchanged.
05. migrating a snapshot that overlaps an earlier one adds only the records outside the earlier snapshot, and matches existing accounts and categories by the match key without creating duplicates.
06. identical transactions on the same day in the snapshot each load as their own record, and a rerun keeps the same count.
07. each opening and closing balance in the account balances file matches the RedBooks balance for that account and date, checked by the validation utilities.

## Audit skills promote learning

This milestone reviews what the agents learned during the release and folds it into the shared skills. It collects the lessons recorded in feature trackers, logs and issues, and updates the skills and agents so the next release starts from them.

**closure criteria**

01. a lessons list records each lesson with its source.
02. each lesson is applied to a skill or agent, or recorded as no change with a reason.
03. every changed skill and agent passes a documentation style review.

## Mkdocs documentation

This milestone writes and publishes the RedBooks documentation site. It covers the developer guide for setup, running, testing and debugging, and the user guide for each workflow in the phone-layout web app. A GitHub Actions workflow builds the site with mkdocs and publishes it on every merge to `main`.

**closure criteria**

01. the developer guide covers setup, configuration, running, testing and debugging.
02. the user guide covers sign-in, accounts, categories, transactions, transfers, financial statements and CSV export.
03. the GitHub Actions workflow publishes the site on merge to `main`.
04. the published site builds with no broken links.

## Publish and release

This milestone ships `0.2.0`. The `dev` branch merges to `main` through a pull request, and the merge is tagged `0.2.0`. The release page is finalized with the as-built scope and links to the documentation site.

**closure criteria**

01. every milestone above is closed.
02. the full test suite passes on the release commit.
03. the release page states the as-built scope and links to the documentation site, developer guide and user guide.
04. `VERSION` reads `0.2.0` and the release commit carries the `0.2.0` tag.

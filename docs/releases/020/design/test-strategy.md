# RedBooks 0.2.0 - Test Strategy

This document sets how every part of the `0.2.0` release is proven to work as delivered, so an autonomous agent can build, test and correct each feature on its own, with a human pass as the secondary check. It covers the test protocols, run rules, component silos, test data, money and exchange rate assertions, sign-in and ownership, frontend testing, case selection, verification layers, the agent loop, the validation utilities and the human pass. The **test cases** turn it into concrete checks.

The test strategy and cases milestone closes the guiding principle, the protocols, the run rules, the component silos, the case selection rules and the verification layers. The other sections are drafts that the milestones owning that work confirm in their own trackers:

01. **test data and reference fixtures**: schema and account 02 seed.
02. **money and exchange rate assertions**: currency model.
03. **stub identity provider and ownership**: oauth login.
04. **frontend and viewports** and **validation utilities**: validation utilities.
05. **agent build, test and debug loop**: agent skills implement customization.
06. **human validation**: each feature milestone's Validate step.

## Contents

- [Summary](#summary)
- [References](#references)
- [Guiding principle](#guiding-principle)
- [Test protocols](#test-protocols)
- [Run rules](#run-rules)
- [Component silos](#component-silos)
- [Test data and reference fixtures](#test-data-and-reference-fixtures)
- [Money and exchange rate assertions](#money-and-exchange-rate-assertions)
- [Stub identity provider and ownership](#stub-identity-provider-and-ownership)
- [Frontend and viewports](#frontend-and-viewports)
- [Case selection rules](#case-selection-rules)
- [Verification layers](#verification-layers)
- [Agent build, test and debug loop](#agent-build-test-and-debug-loop)
- [Validation utilities](#validation-utilities)
- [Human validation](#human-validation)

## Summary

01. a set of test protocols, from pure unit tests up to live calls. The silo protocols make no live network call. Automated runs go against the stubs first, then live for everything except irreversible writes. The full live OAuth flow with its writes is the user's own check.
02. run rules: every test has a latency budget, each feature owns its test set, and every run reads `.env` through the app's settings object and reports its effective mode.
03. component silos: ledger and money, data model and database, backend API, exchange rates, financial statements, frontend, authentication and ownership, and HomeBudget migration, which covers the account `02` seed and the account `01` migration.
04. verification layers: self-report, client, direct inspection, oracle and human. Each case names the layer that decides it.
05. money is asserted exactly. Amounts travel as decimal strings, compare with exact equality to the decimal places of their currency, and never pass through a float. Every accounting oracle checks each entry's sign against its event as well as the balance.
06. the HomeBudget account `02` snapshot is the oracle for the ledger, the statements and the seed load, through expected-value fixtures the fixture builder writes from the snapshot database with plain SQL.
07. the **test cases** hold a release-level case catalogue across the silos, the end-to-end tier and the environment, plus a human validation checklist for each feature milestone with a user-visible surface.

## References

- **release milestones**: [020-release-milestones.md](../020-release-milestones.md)
- **release notes**: [020-release.md](../020-release.md)
- **test strategy tracker**: [020.02-test-strategy.md](../features/020.02-test-strategy.md)
- **test cases**: [test-cases.md](test-cases.md)
- **lessons learned**: [easymcf-lessons-learned.md](easymcf-lessons-learned.md)
- **accounting rules**: [accounting-rules.md](accounting-rules.md)
- **homebudget accounts**: [homebudget-accounts.md](homebudget-accounts.md)
- **data model draft**: [data-model.md](data-model.md)
- **feature-implementation-guide**: [SKILL.md](../../../../.claude/skills/feature-implementation-guide/SKILL.md)
- **pytest skill**: [SKILL.md](../../../../.claude/skills/pytest/SKILL.md)
- **playwright skill**: [SKILL.md](../../../../.claude/skills/playwright/SKILL.md)
- **testing-validation agent**: [testing-validation.md](../../../../.claude/agents/testing-validation.md)
- **homebudget snapshot**: the newest dated copy of the account `02` HomeBudget database in the gitignored `data/homebudget-02/` folder, written by `scripts/snapshot_homebudget_02.py`
- **homebudget data review**: [homebudget-data-review.md](homebudget-data-review.md)
- **homebudget wrapper**: [https://github.com/yayfalafels/homebudget](https://github.com/yayfalafels/homebudget)
- **playwright device emulation**: [https://playwright.dev/python/docs/emulation](https://playwright.dev/python/docs/emulation)
- **fastapi testing**: [https://fastapi.tiangolo.com/tutorial/testing/](https://fastapi.tiangolo.com/tutorial/testing/)

## Guiding principle

Each component is tested where its logic lives, in isolation, before any test of how components fit together. A rounding error in the money type, a wrong ledger balance or a missed forex line is a unit defect. A fast test of that unit alone catches it in milliseconds, with no browser, no second process and no other component's correctness as a precondition. End-to-end tests through the web app exist to catch wiring defects, such as a page calling the wrong endpoint or missing an error status. When an end-to-end test fails, the failure should almost always be about integration, because the silos already proved the logic underneath it.

This is what closes the loop for an agent. A silo test gives a narrow, deterministic signal, an exit code and a traceback naming the failing function, field or amount. The agent acts on it without waiting on a browser, without a human reading a screenshot, and without one component's defect hiding another's.

**02.GP.01** every component has a silo that exercises it directly, with no other component's correctness as a dependency. Silo protocols make no live network call. End-to-end tests are the final automated confirmation against the stubs, run after the relevant silos pass, and the live protocol follows them. The human pass comes last and confirms the experience, after every automated layer is green.

## Test protocols

A protocol is a runnable group of tests with one target, one kind of dependency and one latency budget. Each protocol is a pytest marker, so an agent runs exactly the protocol a change needs. Protocols run in order of speed and information value, fastest first, and the agent runs every protocol.

| id       | protocol  | runs against                                              | budget |
| -------- | --------- | --------------------------------------------------------- | ------ |
| 02.PR.01 | unit      | pure Python functions, pinned clock, no database          | 1 s    |
| 02.PR.02 | db        | per-session test database, schema build, database utility | 5 s    |
| 02.PR.03 | api       | FastAPI test client, test database, stub IdP and rate API | 5 s    |
| 02.PR.04 | frontend  | built React app in Playwright, canned API responses       | 10 s   |
| 02.PR.05 | e2e       | Docker stack, seeded database, stub IdP and rate API      | 10 s   |
| 02.PR.06 | reference | seeded or migrated database, expected-value fixtures      | 10 s   |
| 02.PR.07 | live      | real rate API and real OAuth provider, test database only | 30 s   |

01. **unit** covers the money type, ledger posting rules and entry signs, conversion, the forex gain or loss, statement aggregation and the HomeBudget snapshot reader. Every function takes its date from an injectable clock and its rates from arguments or a stub.
02. **db** builds the schema on a fresh database with the schema build command, and exercises constraints and round trips through the database utility, before any API route exists on top.
03. **api** runs endpoint cases written as data through the FastAPI test client, signed in through the stub identity provider, with the rate API stubbed at the HTTP boundary.
04. **frontend** drives the React app with every `/api` call answered from canned responses, so a rendering defect fails here and a backend defect fails in the api protocol.
05. **e2e** runs the whole Docker stack with the stub identity provider and the stub rate API as compose services, and drives the real web app against the real backend and a seeded database.
06. **reference** compares ledger balances, statement totals and fx transfer amounts against the expected-value fixtures from the HomeBudget snapshot.
07. **live** runs after every stub protocol passes. It fetches real rates from the rate API and checks the real OAuth provider's discovery document and authorize redirect, following redirects to the provider's sign-in page. It writes only to the test database and never to the user's working database. The full live OAuth sign-in with its writes is the user's check in 02.HV.03.

**implementation decision** - the db and api protocols run against a per-session test database built on the compose PostgreSQL service by the schema build command, with each test wrapped in a rolled-back transaction. Tests that need a real commit, such as ledger atomicity, use their own fresh database. During `0.2.0` development the schema is rebuilt and the seed reloaded on every schema change, so no db case applies a migration chain. Versioned forward migrations start in the homebudget account 01 migrate milestone, and its cases test them.

**implementation decision** - the budgets in the table are per test. A local test step that waits more than a few seconds is a defect, and an internet call gets 30 seconds. A test that needs a different budget declares it in its case with the reason.

## Run rules

**02.RR.01 live order** automated protocols run against the stubs first, then live for everything except irreversible writes. An irreversible write is a write to the user's working database or a real account sign-up with the OAuth provider. The full live OAuth flow with its writes is the user's own check.

**02.RR.02 latency budgets** every test carries the budget of its protocol, or the budget its case declares, and raises a timeout when it is exceeded. Load variance is never an accepted close. A failure seen only in the full run is reproduced first with an injected delay, per LT.02 of the **lessons learned**.

**02.RR.03 feature-scoped test sets** each feature milestone owns its test set, marked with its feature id, siloed unit tests first and integration tests after. The end-to-end regression run grows sublinearly, about 1x, 1.5x and 2x of the first feature's run at features 1, 2 to 3, and 10. The first feature is oauth login, and each feature tracker records its regression run time in Validate.

**02.RR.04 settings** the app, the scripts and the test fixtures build one settings object that reads `.env` directly. Nothing writes configuration into the process environment, and every run logs its effective mode at start.

**02.RR.05 baselines** a baseline run starts from a clean worktree of the commit under test, and an order-dependent failure is bisected by file set, then by collect versus execute.

## Component silos

| id       | silo                    | protocols       | primary tool              | data                |
| -------- | ----------------------- | --------------- | ------------------------- | ------------------- |
| 02.SI.01 | ledger and money        | unit            | pytest, service functions | inline values       |
| 02.SI.02 | data model and database | db              | database utility          | test db, seed       |
| 02.SI.03 | backend API             | api             | case files, API tester    | test db, seed       |
| 02.SI.04 | exchange rates          | unit, api, live | stub rate API             | probe fixtures      |
| 02.SI.05 | financial statements    | unit, api       | service tests             | fixtures, seed      |
| 02.SI.06 | frontend                | frontend        | Playwright, UI tester     | canned API          |
| 02.SI.07 | auth and ownership      | api, db, live   | stub IdP, route scan      | two seeded users    |
| 02.SI.08 | HomeBudget migration    | unit, db, ref   | reference checks          | snapshots, fixtures |

01. **ledger and money** tests the money type, exact decimal arithmetic, entry signs, balances from reconciled balance points, expense, income, refund and transfer posting rules, billing accounts, split purchases, entries in another currency, card fx fees and transfers between currencies. These are the release's highest-risk rules, so they get the fastest silo.
02. **data model and database** tests the schema build, constraints, exact decimal round trips, retire and single-active rules through the database utility, with no FastAPI process. A schema change is proven before any route uses it.
03. **backend API** tests every endpoint through case files. Each case carries `name`, `trace`, `method`, `path`, `body`, `as_user` and an `expect` block with status and body checks. One parametrized harness runs every case file through the test client, and the API tester replays the same files against a running backend.
04. **exchange rates** tests fetching, storage, the user rate override, conversion and the failure paths against the stub rate API, which serves the currency catalog and rates captured by the exchange rate API probe and counts its calls. The live protocol confirms the real API still answers as the stub does.
05. **financial statements** tests the income statement, the balance sheet, the forex gain or loss line, drill down, labels and CSV export at the service layer, against hand-built ledger fixtures with hard-coded expected totals, then through the API against the seed.
06. **frontend** tests every page against canned responses in `tests/fixtures/api/`, intercepted with `page.route()`. The same check files run against the real backend in the e2e protocol.
07. **authentication and ownership** tests sign-in through the stub identity provider and generates the ownership matrix from the API route table, so a route added later without an owner scope fails the matrix.
08. **HomeBudget migration** covers two loads. The account `02` seed load is tested in the schema and account 02 seed milestone: snapshot reading, mapping, the as-is load and the reference checks. The account `01` migration is tested in its own milestone: forward migrations, the second opt-in, legacy category mapping, upsert matching and its reference figures.

## Test data and reference fixtures

Every database the tests use holds the seed. The seed load reads the **homebudget snapshot**, a dated copy of the account `02` HomeBudget database, and loads it as-is, with its real account names, payees, notes, dates and amounts.

**02.TD.01 users** defined in `data/users.json`, the seed holds two users with distinct data. User `01` holds the account `02` snapshot, in SGD reporting with USD accounts. User `02` holds a small ledger of a few accounts and transactions with hypothetical names. Cases name them `alice` and `bob`.

**02.TD.02 closed vocabularies** the seed holds at least one row of every account type, every transaction kind of expense, income and transfer, every transfer kind of same-currency and between-currency, every rate source of fetched and user, and every balance sheet group.

**02.TD.03 rates** the seed holds stored USD to SGD rates for every date the seed needs, including every month end in the seed period. The stub rate API serves the same values from `tests/fixtures/rates/`, built from the responses the exchange rate API probe saved.

**02.TD.04 expected-value fixtures** the fixture builder writes the expected values to an `expected/` folder next to the seed, under the real names from the snapshot, in the uncommitted seed location, with amounts and dates unchanged. Each fixture is produced by reading the snapshot database with plain SQL, never by running RedBooks code, so it stays an independent oracle.

| id       | snapshot source        | fixture                 | results it validates                     |
| -------- | ---------------------- | ----------------------- | ---------------------------------------- |
| 02.TD.05 | AccountTrans           | `category-totals.json`  | income statement subcategory totals      |
| 02.TD.06 | record tables          | `record-counts.json`    | snapshot reader, seed load row counts    |
| 02.TD.07 | Account, AccountTrans  | `account-balances.json` | balance points, ledger and balance sheet |
| 02.TD.08 | AccountTrans           | `fx-transfers.json`     | both amounts of each fx transfer         |

01. each account's reconciled balance point comes from the snapshot's Account table, one point per account. Its balance at every month end and on the snapshot date is that point rolled through its AccountTrans rows, per AR.11, and the **homebudget wrapper**'s `get_account_balance` cross-checks each figure.
02. the snapshot holds both amounts of each transfer between currencies, such as the three on 2026-06-02, 2026-08-24 and 2026-09-08. The amounts are the source of truth. Rate times USD amount differs from the SGD amount by up to 0.09 at five decimal places, so a test asserts the stored amounts and never recomputes one from the rate.
03. the category totals and record counts cover rows dated on or before the snapshot date, after the skips the **homebudget data review** sets.

**02.TD.09 synthetic fixtures** unit and service tests use small hand-built ledgers with hard-coded expected values stated in the case itself. These cover rules the snapshot does not exercise, such as rounding boundaries, JPY with zero decimal places, refunds, billing accounts and a reporting currency change. Their account names are hypothetical names at real Singapore institutions.

**02.TD.10 privacy** the seed and the expected-value fixtures carry the real account names, payees and notes from the snapshot. They stay in the uncommitted location the repo layout design sets, out of version control, committed logs, test output, screenshots, traces and the published docs. Committed cases describe snapshot accounts by their role.

**02.TD.11 raw seed checks** a check of the raw seed runs on a database that no app instance has started against, so no startup job changes a row before it is read.

**02.TD.12 account 01 data** the account `01` migration runs against fixture rows reduced from the account `01` HomeBudget database, and against the reference figures the HomeBudget data review sets for account `01`.

## Money and exchange rate assertions

**02.MN.01** amounts and rates are Python `Decimal` values in code, `NUMERIC` columns in PostgreSQL and decimal strings in JSON. A test never builds an expected amount from a float, and the money type rejects a float input.

**02.MN.02** an expected amount is written as a string to the decimal places of its currency, such as `"13.46"` for SGD or `"1000"` for JPY, and compared with exact equality after quantizing to that currency's places. A tolerance comparison such as `pytest.approx` is never used on an amount.

**02.MN.03** a rate is compared at its full stored precision. A rate fetched with eight decimal places round-trips with eight.

**02.MN.04** a converted amount is asserted against a value computed by hand in the case, with the rate and the rounding rule stated beside it.

**02.MN.05** the stub rate API is a small HTTP service in `tests/support/` that serves the catalog and rates from fixture files captured from the probe's saved responses. It records every request so a test can assert the number of fetches, and it serves a failure scenario chosen by a request header: a server error, a timeout or an unknown pair. The api protocol mounts it in-process. The e2e protocol runs it as a compose service and points the backend's rate API base URL at it through `.env`.

**02.MN.06** stored rates carry their source, fetched or user. A test of the fetch path asserts the stub was called once and the stored row carries `fetched`. A test of the override path asserts the stub was never called.

**02.MN.07** every entry is a signed amount, per AR.01 of the **accounting rules**. An oracle asserts the sign of each entry against its event, on the account and on the category or counter account, as well as the balance, per AR.03. The books, the API and every oracle hold signed entries. The presentation flip of AR.18 is asserted only on rendered pages and CSV exports.

## Stub identity provider and ownership

**02.AU.01** the tests sign in through the real sign-in endpoint and the real OAuth callback. The app has no authentication bypass switch, so every test exercises the path a user takes.

**02.AU.02** the stub identity provider is a minimal OpenID Connect provider in `tests/support/`, with authorize, token, user info and key endpoints, signing its own tokens. Its consent page signs in as the seeded user whose email is entered. A failure scenario is chosen by the email entered, such as a denied consent, an unverified email, a token error or an expired token. The e2e protocol runs it as a compose service, and the backend's OAuth issuer URL points at it through `.env`.

**02.AU.03** every database holds both seeded users. The ownership matrix runs every route and verb as `bob` against `alice`'s records, and every result must be a not found response or an empty list.

**02.AU.04** the matrix is generated from the FastAPI route table. A route that takes a record id, lists records or reports a figure is in the matrix by default. A route left out of the matrix must be listed in an explicit allow list with a reason, so a new route with no owner scope fails.

**02.AU.05** the live protocol checks the real OAuth provider without signing a real account in: the discovery document loads and the authorize redirect reaches the provider's sign-in page. The full live sign-in is the user's check, per 02.RR.01.

**02.AU.06** token boundary cases account for the clock leeway of the token library. An expired-token case sets the expiry past the leeway, and a case inside the leeway expects acceptance.

## Frontend and viewports

**02.FE.01** every frontend check runs in the Playwright `iPhone 13` profile, 390 by 844, with touch enabled. Each page also runs once at `Pixel 5`, 393 by 851, and once at a 1280 by 800 desktop width, with realistic-length account and category names, so a style change for one width cannot silently break another.

**02.FE.02** in the frontend protocol, a test serves the built React app and intercepts every `/api/**` request with `page.route()`, answering from `tests/fixtures/api/<page>/*.json`. A check can also assert the body of the request the page sent, so a form defect fails without a backend. Amounts in a request body are decimal strings.

**02.FE.03** the canned responses are captured from real API responses, then reduced. A response shape change updates the canned file in the same change, and the api protocol's case for that endpoint guards the real response shape.

**02.FE.04** each page gets checks for its loading, empty, error and populated states, and a check that the page has no horizontal scroll at each width.

**02.FE.05** checks follow the **playwright skill**: role and label locators, retrying web-first assertions, bound values in preference to rendered labels, and no fixed sleep.

**02.FE.06** the UI tester runs the same check files in two modes, canned responses or the real backend. A failed check saves a screenshot and the page's console log to the uncommitted log location.

**02.FE.07** the human pass runs on a real phone through the tunnel to the local web app. When no phone connection is available, the mobile emulator on the laptop covers it, and the feature tracker records which one was used.

## Case selection rules

**02.CS.01 traceability** every release notes section has at least one catalogue case, and every case trace names a release notes section, a milestone closure criterion, an accounting rule or a strategy rule that exists. Criterion-level coverage belongs to each feature tracker. At its test cases step, once its design topics close, the tracker copies its catalogue cases, reconciles them with its scope, data model and edit locations, and adds the cases its design reveals until every closure criterion of its milestone has a case. A milestone criterion with no catalogue case is expected at this stage.

**02.CS.02 closed vocabularies** every value in 02.TD.02 has a reachable case, a seeded row and a code path that writes it.

**02.CS.03 boundaries** every date and period rule gets a case on each side of its boundary. Examples are a transaction on the first and last day of a statement month, a balance on a reconciled balance point's date, and a session one second before and after its lifetime ends. A boundary set by a library accounts for that library's tolerance, per 02.AU.06.

**02.CS.04 determinism** no silo test depends on wall-clock time, a live network call or a fixed sleep. One injectable clock drives every time-bound value, and a test pins it before creating sessions or rows. Exchange rates come from stored or stubbed values. A socket guard fails any silo test that opens a connection outside localhost and the stubs. The live protocol depends on the network by design and runs under its latency budget.

**02.CS.05 silo-first order** a feature writes its cases cheapest first: unit, then db, then api, then frontend. An e2e case is added only where a real integration risk remains after the silos pass, such as a page reading a rate the backend fetched.

**02.CS.06 ownership leaks** every resource is tested as the second user against the first user's records, per 02.AU.03.

**02.CS.07 exact money** every expected amount is stated exactly, per 02.MN.02.

**02.CS.08 HomeBudget edge cases** every edge case the HomeBudget data review records gets a seed load case and a seed row.

**02.CS.09 sign oracles** every accounting oracle checks each entry's sign against its event as well as the balance, per 02.MN.07, and computes every check from the figures the case states.

**02.CS.10 data-derived expectations** expected values come from oracles and data reads, never hand counts. Tests find seed rows by a stable key, assert deltas against a before-snapshot, and capture created ids from responses. No case hard-codes a seed count or id.

**02.CS.11 proven checks** every new check is shown to fail on a planted fault before it is trusted, and every regression case is shown to fail without its fix.

## Verification layers

Each feature milestone validates its closure criteria through independent layers, so no layer grades its own work. A layer is independent when it reads nothing the code under test produced as its expected value.

| id       | layer       | checks against                                                   |
| -------- | ----------- | ---------------------------------------------------------------- |
| 02.VL.01 | self-report | the code's own pass or fail output, logs and exit codes          |
| 02.VL.02 | client      | the response or page seen from outside, by test client or tester |
| 02.VL.03 | direct      | the database read by the database utility, bypassing the API     |
| 02.VL.04 | oracle      | hard-coded values from the closure criteria or the snapshot      |
| 02.VL.05 | human       | a person using the running app on a phone or in the emulator     |

01. self-report alone proves only that the code ran.
02. client proves what the API returned or the page showed. Any check beyond a request and response shape pairs it with direct or oracle.
03. direct proves what a write persisted, independent of the API that reads it back.
04. oracle is the strongest automated layer. Its value is written by hand in the case or produced from the snapshot without RedBooks code.
05. human runs last and confirms layout, wording and how a control feels to use.

**deviation** - the **release milestones** list four layers and fold the case replay of the validation utilities into self-report. This strategy separates client from self-report, because a replayed request observes the app from outside and is a stronger check than the app's own log.

## Agent build, test and debug loop

The agent reaches for the narrowest protocol first, then widens. Commands in the then column omit the leading `pytest`, and case files live in `tests/api/cases/`.

| id       | change                      | narrowest signal                     | then                         |
| -------- | --------------------------- | ------------------------------------ | ---------------------------- |
| 02.LP.01 | money, ledger or statements | `pytest -m unit -k <rule>`           | `-m "unit or api"`           |
| 02.LP.02 | schema                      | rebuild and reload, database utility | `-m db`, then `-m reference` |
| 02.LP.03 | API route or validation     | one case in `cases/<resource>.json`  | `-m api`                     |
| 02.LP.04 | exchange rates              | `pytest -m unit -k fx`               | `-m api -k fx`, then live    |
| 02.LP.05 | React page or component     | `pytest -m frontend -k <page>`       | `-m frontend`, then `-m e2e` |
| 02.LP.06 | sign-in or ownership        | `pytest -m api -k auth`              | `-m api -k ownership`        |
| 02.LP.07 | seed load or mapping        | `pytest -m unit -k seed`             | reload, then `-m reference`  |
| 02.LP.08 | account 01 migration rule   | `pytest -m unit -k migrate`          | migrate, then `-m reference` |
| 02.LP.09 | any change, before done     | the feature's own test set           | `-m "not live"`, then live   |

_why narrowest first_

01. a money, sign or posting defect surfaces at the function that computes it, with the exact expected and actual amount.
02. a constraint error surfaces from SQL at the source, before it turns into a 422 three layers up. The rebuild reloads the seed, so the reference checks confirm the seed still loads.
03. one parametrized case fails with its trace id and field, with no browser involved.
04. the stub's call count shows a fetch-once defect directly, and the live run confirms the stub matches the real API.
05. a rendering defect is isolated from whether the backend behaved correctly.
06. the generated matrix names the route and verb that leaked.
07. a parsing or mapping defect shows before a full seed reload runs.
08. a migration rule defect shows before a full migration runs.
09. matches the verify-before-done rule in the **feature-implementation-guide**: the feature's own set first, then the regression run.

**02.LP.10 suspect the check first** when a check fails, the agent first confirms the check's input, its expected value and its harness against the design, then the code.

**02.LP.11 first-failure triage** when a run shows several failures, the agent separates independent first failures from the failures they cause, such as a schema error that fails every api case after it. It logs each first failure as an issue in the feature tracker with its hypothesis, fixes one at a time, reruns the narrowest protocol after each fix, and reruns the full automated suite as confirmation at the end.

**02.LP.12 self-correction bound** the agent fixes and reruns on its own while each rerun makes progress. When the same case fails three times in a row with no change in its failure, or a fix would change a closure criterion, a design decision or an expected-value fixture, the agent stops and raises the issue for the user.

**02.LP.13 human handoff** the human pass starts only after every automated protocol for the milestone is green, including the live protocol, and the feature tracker's Validate section records the green run that preceded it.

## Validation utilities

The validation utilities milestone builds the standalone tools the layers above use, on top of the seed load and expected-value fixtures. Feature milestones add case files and checks to them and write no new tools.

| id       | tool              | layer       | used for                                                   |
| -------- | ----------------- | ----------- | ---------------------------------------------------------- |
| 02.VU.01 | environment check | self-report | services up and reachable before any run                   |
| 02.VU.02 | database reset    | self-report | reset the local database to seed data in one command       |
| 02.VU.03 | database utility  | direct      | read, write and search any table, and set up case state    |
| 02.VU.04 | API tester        | client      | replay a case file or one case against the running backend |
| 02.VU.05 | UI tester         | client      | run a check file at phone width, canned or real            |
| 02.VU.06 | reference checks  | oracle      | compare balances, totals and fx amounts to the fixtures    |

Every tool reports each case as pass, fail or error. Error marks a check that could not run, such as a service that is down or a sign-in that failed. Every tool writes one structured record per case to a timestamped log in `.dev/logs/` through one shared log writer, tags the log with a `--label <feature>.<task>`, applies the latency budgets, and exits non-zero on any fail or error. A tool that writes into the user's working database refuses to run without the second opt-in, and backs the database up first.

## Human validation

**02.HV.01** once every automated protocol for a feature milestone passes, a human makes one pass through the running app on a phone or in the mobile emulator, following the milestone's checklist from [Human validation checklists](test-cases.md#human-validation-checklists) of the **test cases**. The pass confirms layout on a phone screen, the wording of messages, how controls feel to use, and figures only visible in the live HomeBudget app.

**02.HV.02** each feature milestone tracker copies its checklist into its Validate section and records the outcome of each line, what was checked, the device used and what looked wrong. The pass is a design review as much as a test. A finding becomes an issue in that tracker, a design gap is raised with options for the user, and the agent adds an automated case that would have caught it where one is feasible.

**02.HV.03** the human pass of the oauth login milestone includes the full live OAuth sign-in on the phone, with its writes, per 02.RR.01.

**02.HV.04** the txn and accounts milestone runs a short early walkthrough of the first transaction entry page at phone width, before its tests are complete, as the LT.04 experiment of the **lessons learned**, and records the result as a `lesson observation LT.04`.

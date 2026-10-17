# RedBooks 0.2.0 - easyMCF Lessons Learned

This document reviews the easyMCF release `010` record and the financial-statements agent skills, and extracts the lessons that carry over to RedBooks. It keeps only lessons with common relevance to both projects: Python services, a SQL store, a web frontend tested in a browser, OAuth with per-user data, seed data built from real personal records, documentation publishing, and the agent working process. Lessons about the MyCareersFuture site, scraping, Singpass and AngularJS stay with easyMCF and are listed once, in [Not transferred](#not-transferred).

Every lesson cites the issue or section it comes from. The document separates three kinds of finding.

01. **confirmed lessons**, `LL.NN`. The source shows the failure or the correction and its confirmed cause. These become rules and reference lessons in the RedBooks skills and agents. Where the user settled a question the sources left open, the lesson carries a **decision** line.
02. **lessons to be learned**, `LT.NN`. Hypotheses that look promising from the evidence but need research or an experiment in RedBooks before they become rules.
03. **accounting source irregularities**, `AI.NN`. Errors in the financial-statements accounting examples, resolved by the **accounting rules**.

## Summary

01. **the agent was slow to follow the project from stubbed to live operation.** In 17.IS.11 the user set live mode in `.env` so features could be validated against the real site. For the rest of the release the agents treated that setting as a leak: they scrubbed it from tests, overrode it inline, failed the preflight on it, and logged each live run as an incident. The instructions that said live runs need a request in that turn were never updated, and the layered overrides left different processes running in different modes. The correct design reads configuration directly from `.env`, and the agent updates its own instructions when the operating mode changes. See [LL.01](#ll01-read-configuration-directly-from-the-env-file) and [LL.02](#ll02-follow-the-project-as-it-moves-from-stubbed-to-live-operation).
02. **multi-user support added late cost a cross-cutting rewrite.** Adding accounts at milestone 13 failed 49 of 134 tests and touched every service, resource and screen. RedBooks starts multi-user. See [LL.20](#ll20-build-ownership-in-from-the-first-feature).
03. **the checks were wrong about as often as the code.** In milestone 08, six of twelve issues were defects in the verification commands or oracles. Six more issues in milestones 10 to 13 were wrong expectations while the code was right. See [LL.32](#ll32-check-the-oracle-and-the-harness-before-the-code).
04. **seed data needs the same care as production data.** Seed rows built only for vocabulary coverage formed an impossible history, generator defaults silently rewrote unrelated files, and the generator had to be validated like any other code. RedBooks builds its seed from the real HomeBudget snapshot and keeps the user's real data in it, so the history, determinism and storage lessons apply directly. See [Schema, migrations and seed data](#schema-migrations-and-seed-data).
05. **the human walkthrough found what automation missed.** A design gap in deletes with history, a list that never refreshed, and about thirty layout and workflow items all surfaced after every automated layer had passed. See [LL.48](#ll48-plan-for-the-human-walkthrough-to-find-design-gaps).
06. **the financial-statements accounting examples carry errors.** Two worked examples record their entries with every sign reversed, and one fails its own identity while marked as passing. RedBooks resolves these in the design stage and copies none of them forward. See [Accounting source irregularities](#accounting-source-irregularities).
07. **the schema changed eleven times in one release** under a recreate-don't-migrate rule, and the user's own data survived only through a hand-written upgrade script. RedBooks rebuilds its database and reloads the account `02` seed on each schema change during `0.2.0` development, and adopts versioned forward migrations before the full account `01` migration. See [LL.06](#ll06-change-the-schema-its-version-the-seed-and-the-design-doc-together).

The review yields 62 confirmed lessons, 8 lessons to be learned and 5 accounting source irregularities. The user settled the twelve questions the sources left open, and each decision sits in the lesson, rule or HomeBudget account note it applies to. [Hybrid approach](#hybrid-approach-for-redbooks-skills-and-agents) proposes how the RedBooks skills and agents carry the lessons to be learned alongside the confirmed rules. [Lessons to apply to the planning documents](#lessons-to-apply-to-the-planning-documents) stages the changes the lessons and decisions make to the release plan, starting from a revised milestone structure.

## Contents

- [Summary](#summary)
- [References](#references)
- [Review method and coverage](#review-method-and-coverage)
- [Confirmed lessons](#confirmed-lessons)
  - [Environment and configuration](#environment-and-configuration)
  - [Schema, migrations and seed data](#schema-migrations-and-seed-data)
  - [API, authentication and ownership](#api-authentication-and-ownership)
  - [Frontend](#frontend)
  - [Testing](#testing)
  - [Accounting and money](#accounting-and-money)
  - [Process and agents](#process-and-agents)
- [Lessons to be learned](#lessons-to-be-learned)
- [Accounting source irregularities](#accounting-source-irregularities)
- [Correct accounting rules](#correct-accounting-rules)
- [Hybrid approach for RedBooks skills and agents](#hybrid-approach-for-redbooks-skills-and-agents)
- [Lessons to apply to the planning documents](#lessons-to-apply-to-the-planning-documents)
- [Not transferred](#not-transferred)

## References

- **agent skills tracker**: [020.05-agent-skills-customization.md](../features/020.05-agent-skills-customization.md)
- **release milestones**: [020-release-milestones.md](../020-release-milestones.md)
- **easymcf repo**: `/home/taylor-hickem/easymcf`
- **easymcf trackers**: `easymcf/docs/releases/010/features/` and `easymcf/docs/releases/020/features/`
- **easymcf issues**: `easymcf/docs/releases/010/010-issues.md`
- **easymcf test strategy**: `easymcf/docs/releases/010/design/010-test-strategy.md`
- **easymcf claude md**: `easymcf/CLAUDE.md`
- **easymcf agents and skills**: `easymcf/.claude/`
- **easymcf memories**: `~/.claude/projects/-home-taylor-hickem-easymcf/memory/`
- **homebudget accounts**: [homebudget-accounts.md](homebudget-accounts.md)
- **accounting rules**: [accounting-rules.md](accounting-rules.md)
- **financial-statements skills**: `/home/taylor-hickem/repos/financial-statements/.github/skills/`

Issue ids such as `13.IS.10` name an issue in the easyMCF tracker of the same number, here `010.13-oauth-login.md`. `ISS-NN` ids name findings in the **easymcf issues**. `fs <skill>` names a skill in the **financial-statements skills**.

This document is the evidence base for the agent skills customization. The Lesson trace section of the **agent skills tracker** records where each lesson lands.

## Review method and coverage

Each tracker's Validate section was read in full: every issue's problem description, exception, hypothesis or cause, and diagnostic details. Scope, test strategy and design sections were read where they record decisions or practice. Edit location and implement sections that hold source code listings were skipped, since they record code and not failures or decisions.

| id       | source                              | lines | read                                    |
| -------- | ----------------------------------- | ----- | --------------------------------------- |
| 05.SR.01 | easymcf roadmap                     | 61    | full                                    |
| 05.SR.02 | easymcf 010 milestones              | 65    | full                                    |
| 05.SR.03 | **easymcf issues**                  | 156   | full                                    |
| 05.SR.04 | easymcf claude agent design         | 129   | full                                    |
| 05.SR.05 | **easymcf claude md**               | 85    | full                                    |
| 05.SR.06 | 010.07 local dev env                | 618   | design, tests, validate, task details   |
| 05.SR.07 | 010.08 db schema seed data          | 1162  | design, validate                        |
| 05.SR.08 | 010.09 job leads tracking           | 7404  | status, strategy, validate, 09.13 scope |
| 05.SR.09 | 010.10 search by keywords           | 1867  | validate                                |
| 05.SR.10 | 010.11 apply automation             | 1841  | validate                                |
| 05.SR.11 | 010.12 validation utilities         | 982   | scope, design, tests, validate          |
| 05.SR.12 | 010.13 oauth login                  | 3711  | scope, test strategy, validate          |
| 05.SR.13 | 010.17 mcf website session          | 1932  | probes, strategy, five generic issues   |
| 05.SR.14 | 010.18 release documentation        | 1682  | validate                                |
| 05.SR.15 | easymcf 020 features                | 1080  | 020.07 generic parts, 020.08, 020.09    |
| 05.SR.16 | **easymcf agents and skills**       | 1540  | full                                    |
| 05.SR.17 | **easymcf memories**                | 55    | full                                    |
| 05.SR.18 | easymcf assessments                 | 0     | none exist                              |
| 05.SR.19 | financial-statements agents md      | 14    | full                                    |
| 05.SR.20 | fs accounting-logic and decimal     | 413   | full                                    |
| 05.SR.21 | fs reconciliation-patterns          | 386   | phases 0 to 7, account patterns         |
| 05.SR.22 | fs pydantic, httpx, variable-naming | 261   | full                                    |
| 05.SR.23 | fs requirements-change              | 533   | workflow steps, key rules, pitfalls     |
| 05.SR.24 | fs subagent-trial-methodology       | 297   | structure, outcomes, evidence standards |
| 05.SR.25 | fs homebudget                       | 637   | business logic, sync, common issues     |
| 05.SR.26 | **easymcf test strategy**           | 161   | full                                    |

01. 05.SR.26 is added to the **source inventory** by this review. Every easyMCF tracker cites its `STRAT-*` rules, and the RedBooks test strategy milestone is modelled on it.
02. 05.SR.13 is mostly MyCareersFuture and Singpass session handling. Issues 17.IS.05 to 17.IS.28 were read by title and cause only, and the generic ones among them are cited below.

## Confirmed lessons

Each lesson gives its evidence, the rule, how it applies in RedBooks, and its destination in the **agent skills tracker** design.

### Environment and configuration

#### LL.01 read configuration directly from the env file

**evidence**: easyMCF layered several mechanisms over one setting. Task 07.05.07 loaded `.env` into the process environment at the import of every script. `tests/conftest.py` then removed selected keys, commands overrode the mode inline, and diagnostic scripts set it again before their imports. Each process could end up in a different mode.

01. 10.IS.05 and 13.IS.11: a test imported a script, and the import restored keys the test configuration had removed. Both failed only in a full run.
02. 10.IS.09: a manual smoke test ran in the mode `.env` selected, while the tracker's command assumed a different one. An implausible card count, 24 against a fixture's 2 or 3, was the only sign of which mode had run. The follow-up recorded the effective mode in each run's log row.
03. 11.IS.14: a diagnostic script ran in a different mode from the server it was diagnosing. The agent had to read `/proc/<pid>/environ` to learn which mode the server was in.
04. 18.IS.03: a seed helper wrote `.env` values back into the test process. The fix read the file with `dotenv_values`, which returns the values without changing the process environment.

**lesson**: one settings object reads `.env` directly, and the app, the scripts and the tests all use it. Nothing writes configuration into the process environment at import, and no layer scrubs or overrides values behind the file. Every run reports the effective mode it used.

**redbooks**: a pydantic-settings class reads `.env` as its env file. The app factory, every script and the test fixtures build it the same way, and each run logs its mode at start.

**destination**: `python/config-and-time`, `pytest/fixtures-and-isolation`.

#### LL.02 follow the project as it moves from stubbed to live operation

**evidence**: in 17.IS.11 the user asked to default to a live connection so the feature could be validated against the real site, and set `MCF_MODE=live` in `.env` on purpose. The agents kept working to the earlier rule.

01. the **easymcf claude md** boundary and the skills' hard rules still said live runs happen only when the user asks in that turn, and nothing updated them.
02. 10.IS.09 and 18.IS.03 recorded live runs as leaks and as live-site exposure.
03. 11.IS.07 called the setting "a deliberate human setting that outlived its live-validation session". The preflight failed on it, and the agent left the issue open for the user.
04. 11.IS.14 and 18.IS.03 responded with more scrubbing and inline overrides, which deepened the split LL.01 describes.

**lesson**: test and run modes change as a project matures from a proof of concept toward a working product, and live runs become routine. When the user changes the operating mode, the agent reads the `.env` setting as the user's intent. It updates the agent instructions, skills, preflight checks and tracker commands in the same change, and asks when the intent is unclear.

**redbooks**: `0.2.0` runs real OAuth sign-in and real exchange rate fetches from time to time, and `0.3.0` runs live all the time. Agents expect live runs and report which mode each run used.

**destination**: agent shared boundaries, `product-manager` agent, `feature-implementation-guide/validation`.

#### LL.03 guard irreversible writes to real systems with a second opt-in

**evidence**: 11.IS.14 found the design never named the confirmation flag its scope required for submitting a real job application. The fix added `APPLY_LIVE_SUBMIT`, checked in the run preflight before any row is written and again where the browser is created. In 18.IS.03, the apply run's refusal without a valid session and a seed that left every session missing kept any application from being submitted during a live run.

**lesson**: live reads are routine. An irreversible write to a real external system or to the user's real data needs a second opt-in, checked at preflight and at the point of use.

**redbooks**: a HomeBudget migration that writes into the user's working database needs the second opt-in. A live exchange rate fetch is a read and needs only the mode setting.

**decision**: automated tests run against the stubs first. They then make live calls for everything except the calls that make irreversible writes. The full end-to-end OAuth flow, live and with its irreversible writes, is reserved for the user's own test. Other external integrations follow the same order. Everything else writes directly to the database, so no tier calls internals that bypass the product write path.

**destination**: `python/config-and-time`, agent shared boundaries.

#### LL.04 read configuration at call time

**evidence**: 07.IS.01. Dataclass field defaults read `os.environ` once at import, so a fixture that set the database path afterwards was ignored. Review caught it before it ran.

**lesson**: settings are read from `.env` when the settings object is built, so a changed file takes effect on the next build.

**redbooks**: FastAPI dependencies supply the settings object through a provider.

**destination**: `python/config-and-time`.

#### LL.05 resolve paths from the project root

**evidence**: 13.IS.23. A relative photo directory resolved against the working directory, so a process started from the package folder served a `500`. The regression test changes the working directory and stores a file.

**lesson**: relative paths in configuration resolve against one known root.

**redbooks**: data import paths for the HomeBudget snapshot and any stored files.

**destination**: `python/config-and-time`.

### Schema, migrations and seed data

#### LL.06 change the schema, its version, the seed and the design doc together

**evidence**: the schema moved from version 1 to 11 within release 010.

01. 08.IS.05 and 09.IS.02: the startup version constant was not bumped with the schema.
02. 09.IS.01 and 09.IS.04: the generator emitted rows for a table the schema lacked, and the design docs assigned that version to another milestone.
03. 13.IS.01: seed files written for the old schema failed to load.
04. 11.IS.04: the schema was edited while a background suite ran, so a spawned app saw a different version.

**lesson**: a schema change, its version marker, the regenerated seed, and the data model doc's version table land in one change. Nothing edits the schema while a suite runs.

**redbooks**: an Alembic revision, the app's head check at startup, the regenerated seed and the data model doc change together.

**decision**: during `0.2.0` development, a schema change rebuilds the database and reloads the seed, which is the account `02` data loaded as-is from `data/`. Versioned forward migrations start before the full account `01` migration, which runs only after the release and its data model are validated and tested, so the large account `01` data is migrated as few times as possible.

**destination**: `postgresql/migrations`.

#### LL.07 build seed data as a coherent history and derive its aggregates

**evidence**: 11.IS.03. Seeded apply attempts covered every outcome code but formed an impossible history: attempts in a search run, timestamps before their run started, repeated attempts in one run, typed counts that disagreed with the rows. Oracle, API and UI evidence read those rows. 17.IS.29 seeded a connected session with no backing file. 11.IS.01 seeded a state that startup reconciliation always reset.

**lesson**: seed data describes a history that could have happened. Counts, balances and dates derived from other rows are computed by the generator. State a test needs, such as a live session, is staged by that test.

**redbooks**: account balances, statement totals and opening balances in the seed are computed from seeded transactions, never typed.

**destination**: `pytest/oracles-and-seed-data`, deferred detail to `redbooks-ledger`.

#### LL.08 keep the real seed data out of version control and the published site

**evidence**: easyMCF committed its seed. The 010.08 pipeline sanitised real notes before writing seed files, and 18.IS.01 replaced the user's name and email with tokens rendered from `.env` at load. 08.IS.10 checked that the raw source files stayed untracked, and needed `git check-ignore --no-index` to check an untracked path correctly.

**lesson**: RedBooks seed data carries the user's real personal and financial data on purpose, so easyMCF's sanitise and tokenise steps do not transfer. Masking would make validation against the HomeBudget reference figures harder and the app less useful, and the aim is an app that is usable from day one with the user's real accounts, payees and notes. What transfers is the storage boundary. The snapshot and the seed built from it stay out of version control, out of the published docs and out of committed logs, and a check proves each one.

**redbooks**: the repo layout design decides where the seed lives. A closure check runs `git check-ignore --no-index` over the seed paths, and the docs build includes no seed file.

**decision**: the seed is the account `02` data in `data/`, loaded as-is with its real names, payees and notes. Committed code, committed docs and the published docs site show no real account names, account numbers or personal details. Their examples use hypothetical names at real Singapore institutions, such as DBS, UOB, Interactive Brokers, SP Services and Singtel. Real names live only in uncommitted directories.

**destination**: `data-migration-engineer` agent, agent shared boundaries, deferred detail to `redbooks-homebudget-migration`.

#### LL.09 pin every generator input and review the diff of generated files

**evidence**: 17.IS.01. A missing date anchor defaulted to today, so a regeneration rewrote eight unrelated seed files while the generator and the full suite both passed. Only `git status` caught it. 09.IS.52 and 09.IS.35 found seed changes the plan said would not happen. 10.IS.01 found a hard-coded loop bound by tracing the arithmetic before running. 010.09's secondary validation generated the seed twice and compared the directories.

**lesson**: generator inputs such as the seed, the anchor date and loop bounds are pinned or derived. Generating twice gives identical files, and every changed generated file is reviewed.

**redbooks**: the seed generator for the ledger takes a fixed anchor date and a fixed random seed.

**destination**: `pytest/oracles-and-seed-data`.

#### LL.10 every vocabulary value has a seeded row and a writing code path

**evidence**: 09.IS.03 found two event types no generator site emitted. 17.IS.02 found a status no code path reached. 10.IS.02 found the generator's own lookup table missing a new value.

**lesson**: each closed vocabulary value appears in the seed, a test checks it, and some code path writes it. Adding a value means searching every lookup keyed on it.

**redbooks**: account types, transaction kinds and transfer kinds.

**destination**: `postgresql/schema-design`, `pytest/oracles-and-seed-data`.

#### LL.11 transcribe constraints and expected values from the requirements

**evidence**: 010.08 Design transcribed every `CHECK` constraint from the requirements tables and wrote the seed oracle's expected sets from the design tables, never from the generator's constants. A generator bug and a check that reads the generator's output cannot share a blind spot.

**lesson**: constraints and oracle expectations come from the requirements or design text, never from the code under test.

**redbooks**: vocabulary constraints come from the data model doc, and statement oracles come from the HomeBudget reference figures.

**destination**: `pytest/oracles-and-seed-data`, `postgresql/schema-design`.

#### LL.12 retire records that history references

**evidence**: 11.IS.19, found by the human walkthrough. A foreign key guard refused to delete a CV that only past attempts and an archived track used. Given three options, the user chose retire: an `is_active` flag, so the label leaves every picker while history keeps it. 09.IS.45 made offers undeletable and kept final offers as history.

**lesson**: a delete blocked only by historical references retires the record. A delete blocked by a live use names that use.

**redbooks**: accounts and categories with posted transactions are retired, never deleted.

**destination**: `postgresql/schema-design`, `accounting/ledger-models`.

#### LL.13 keep one authority per state

**evidence**: 17.IS.30. The UI trusted a database status while the open action also needed a file, so the two disagreed. The fix reconciles on startup and on every read with the same rule. 17.IS.29 and 11.IS.01 show the same split.

**lesson**: each state has one authority. Where two must exist, every read reconciles them by one rule.

**redbooks**: an account balance is derived from postings. A stored balance is a cache rebuilt from them.

**destination**: `postgresql/schema-design`.

#### LL.14 enforce single-active invariants with partial unique indexes

**evidence**: ISS-03 found a check-then-insert guard for one running job with no atomic enforcement. The resolution, and later designs, used a unique index filtered to the active state: one open offer per lead in 09.IS.45, one running inspection and one current selector version in 020.07.

**lesson**: "at most one active" rules live in a partial unique index.

**redbooks**: one open reconciliation per account and period, and one running migration.

**destination**: `postgresql/schema-design`.

#### LL.15 order every result whose order matters

**evidence**: 11.IS.06. A query without `ORDER BY` returned rows in index order.

**lesson**: any query whose order a caller or test relies on has an `ORDER BY` on unique columns.

**destination**: `postgresql/query-practice`.

### API, authentication and ownership

#### LL.16 route invariant-bearing writes through services

**evidence**: ISS-02. A generic CRUD surface let any client write a lead stage directly, bypassing its state machine. The resolution kept generic routes for plain entities and moved invariant writes behind hooks and named endpoints. The hooks then grew to create, update, batch, search and delete variants.

**lesson**: an entity with invariants is written only through a service that enforces them. Generic routes serve entities with none.

**redbooks**: transactions, transfers and opening balances are written through ledger services.

**decision**: RedBooks uses explicit FastAPI routers, one per resource. Shared behavior lives in dependencies and services, so no generic route layer is built.

**destination**: `fastapi/routes-and-schemas`.

#### LL.17 define the error contract per verb and the order of checks

**evidence**: 13.IS.12. An update naming an unknown parent answered `404` where its contract says a `400` on the field. 13.IS.13: an ownership loop ran before the size check, so an oversize batch answered `404`. 09.IS.06: a `400` named no field.

**lesson**: each verb has a documented error contract, and checks run in a fixed order: request shape, then ownership, then business rules. A missing and a foreign record get the same answer and message.

**redbooks**: FastAPI validation errors name every field. Ownership dependencies run after body validation.

**destination**: `fastapi/ownership-and-errors`.

#### LL.18 deny the API prefix by default and keep the frontend fallback off it

**evidence**: 09.IS.05. The single-page fallback answered `200` with HTML for unknown API paths. 13.IS.06: the fallback route was public, so a signed-out request to an unknown API path got `404` and learned the route did not exist. 07.IS.04: the fallback caught the wrong exception type.

**lesson**: every path under the API prefix requires a session by default. Unknown API paths answer JSON `404` to a signed-in user and `401` to anyone else.

**destination**: `fastapi/routes-and-schemas`, `fastapi/oauth-sessions`.

#### LL.19 generate the ownership matrix from the resource registry

**evidence**: 010.13 strategy rule 01 generated the tenancy tests from the registered resources. It then caught unscoped additions twice: 10.IS.04 and 17.IS.03.

**lesson**: ownership tests are generated from the route or resource registry, so a new resource fails until it declares its owner.

**redbooks**: parametrise the second-user test over FastAPI's route table.

**destination**: `pytest/api-and-ownership-tests`.

#### LL.20 build ownership in from the first feature

**evidence**: 13.IS.03. Adding accounts at milestone 13 failed 49 of 134 tests. 13.IS.02 rewrote one-user oracles. 13.IS.16 found every browser test opened pages signed out.

**lesson**: per-user ownership, two seeded users and a sign-in helper exist before the first feature.

**redbooks**: `0.2.0` scope is multi-user, so this is applied in the release milestones. The `architect` agent keeps it in every design.

**destination**: applied, `architect` agent.

#### LL.21 catch every exception family a library delegates to

**evidence**: 13.IS.09. A token validation failure raised an error from a library the OAuth package delegated to, and the callback answered `500`. 17.IS.28 imported an exception class that was not public. 07.IS.04 caught an exception the framework never raised.

**lesson**: reproduce each failure in isolation to learn which exception type it raises, and import exceptions from the public API.

**decision**: follow standard error handling practice. Catch the specific exception for each identified cause, keep each cause isolated, and give the user an actionable hint on how to resolve or avoid it. Catch-all handlers are reserved for keeping a batch running, and they record the original exception, per LL.42.

**destination**: `python/errors-and-logging`, `fastapi/oauth-sessions`.

#### LL.22 read library defaults before writing boundary cases

**evidence**: 13.IS.10. A token expired one second ago was accepted because the library allows 120 seconds of clock leeway. The leeway was kept, since a slow local clock should not refuse real tokens, and the test boundary moved to one hour.

**lesson**: boundary cases account for the tolerances the libraries apply.

**destination**: `fastapi/oauth-sessions`, `pytest/oracles-and-seed-data`.

#### LL.23 test OAuth against a local stub provider

**evidence**: the 010.13 strategy ran the full authorization code flow against a local OpenID Connect server that signs its own tokens. Each failure scenario is selected by the email entered on its consent page. 13.IS.05 found a provider setup check that stopped at the first redirect and passed a wrong redirect URI.

**lesson**: automated tiers use a stub identity provider with one scenario per failure kind. The live tier only confirms the real provider behaves as the stub assumes. Provider setup checks follow redirects to the final page.

**decision**: the automated tiers validate on the stub provider first. Live calls then cover everything except the irreversible writes, and the full live OAuth flow with its irreversible writes is the user's own test, per LL.03.

**destination**: `fastapi/oauth-sessions`, `pytest/api-and-ownership-tests`.

#### LL.24 declare how structured fields serialise

**evidence**: 10.IS.12. A JSON text column reached the client as a string, while the frontend sketch read it as an object. fs pydantic notes that `Decimal` serialises as a string in JSON.

**lesson**: the API contract states the JSON type of every structured or decimal field.

**redbooks**: money amounts are decimal strings in JSON, and response models declare it.

**destination**: `fastapi/routes-and-schemas`.

#### LL.25 call each layer directly before building the next

**evidence**: 10.IS.10. A briefing said a joined endpoint was built and tested. The service tests passed, but no route existed, and a `curl` call found it before any UI was built. The 010.09 HTTP smoke run found 09.IS.05 and 09.IS.06 the same way. 17.IS.03 found a table with no read route.

**lesson**: before building on a layer, call it directly. A service test does not prove a route exists.

**destination**: `feature-implementation-guide/validation`.

#### LL.26 extend an endpoint without dropping its existing call shapes

**evidence**: 10.IS.11. A new search hook required a parameter, which broke a call shape that ownership tests relied on. A targeted run of related tests caught it first.

**lesson**: when an endpoint gains a mode, its earlier calls keep working, and related tests run before the full suite.

**destination**: `fastapi/routes-and-schemas`.

### Frontend

#### LL.27 refresh every view of changed data and keep in-progress input

**evidence**: 09.IS.37, found in the manual pass: a saved change left the list stale. 11.IS.24: the queue stayed stale after a live run. 09.IS.10: a refresh replaced the whole model and erased half-typed input. The fix kept fields the user had changed.

**lesson**: after a write, every view that shows the changed data reloads. A refresh merges server data with fields the user is editing.

**redbooks**: after a transaction save, the account ledger, the balance and any open statement view refresh.

**destination**: `react/api-calls`.

#### LL.28 treat form values as strings at the boundary

**evidence**: 10.IS.14. A numeric id bound to a select whose option values are strings matched nothing, silently.

**lesson**: select and input values are strings. Convert ids and amounts at the form boundary.

**redbooks**: amount inputs are parsed to decimals once, at submit.

**destination**: `react/components-and-state`.

#### LL.29 capture the requested path before redirecting to sign-in

**evidence**: 13.IS.17. A chained call read the path after the redirect had already changed it, so sign-in returned to the sign-in page. The design snippet carried the same defect.

**lesson**: store the requested path in a variable first, then redirect.

**destination**: `react/api-calls`.

#### LL.30 scope styles to their component and test layouts at both widths

**evidence**: 11.IS.09. One feature changed a shared table rule to fit a 375 pixel width and silently broke another feature's one-line rows. Nothing caught it because seeded text was short. 11.IS.10: the first fix on the shared class broke a third page.

**lesson**: style rules target one component. Layout tests run at phone and desktop width with realistic text lengths.

**redbooks**: phone width is the primary layout. Seed account and category names use realistic lengths.

**destination**: `react/mobile-layout`.

#### LL.31 apply the human walkthrough's interface feedback

**evidence**: 09.IS.11 to 09.IS.32 and 17.IS.05 to 17.IS.14 recorded the user's interface feedback after automated checks passed. Recurring themes: label every control and space sections apart, use aligned table columns for list data, put primary actions at the top of detail views, hide internal ids, offer search, sort and batch actions on long lists, discard unsaved edits when another record opens, return to the list after save, keep one navigation control per feature, show status beside its control, reserve each colour for one meaning, and keep a result dialog open until the user closes it.

**lesson**: these are the user's standing interface preferences.

**destination**: `react/ui-review-lessons`.

### Testing

#### LL.32 check the oracle and the harness before the code

**evidence**: six of twelve issues in 010.08 were verification defects: a stale query shape in 08.IS.03, a miscounted table total in 08.IS.04, a pre-created temp file in 08.IS.02, a bare interpreter name in 08.IS.08, a missing schema step in 08.IS.09, and wrong paths in 08.IS.11. 13.IS.07, 13.IS.14, 13.IS.20, 11.IS.15, 10.IS.08 and 12.IS.01 were wrong expectations while the code was right.

**lesson**: when a check fails, first confirm the check's input, expected value and harness against the design. Derive expected values by reading the data, never by hand count.

**destination**: `pytest/oracles-and-seed-data`, `pytest/run-and-triage`.

#### LL.33 never hard-code seed counts or ids

**evidence**: 10.IS.03, 11.IS.08, 13.IS.15 and 11.IS.05 broke when the seed gained rows. 10.IS.08 asserted a literal count where a seeded row already existed. The durable fixes asserted against a before-snapshot, or cross-checked the constant against the database so the next change fails loudly.

**lesson**: tests look up seed rows by a stable key, assert deltas against a before-snapshot, and capture created ids from responses.

**destination**: `pytest/oracles-and-seed-data`.

#### LL.34 wait on web-first assertions and assert bound values

**evidence**: 13.IS.18 read a property of an element that was briefly absent. 13.IS.25 measured an image before it loaded, and only under full-suite load. 09.IS.33 and 09.IS.50 waited on a locator that matched several elements. 11.IS.17, 11.IS.18 and 09.IS.57 compared text that CSS rendered in upper case. The stronger fix asserted the disabled attribute or the bound value.

**lesson**: wait with retrying assertions that tolerate absent elements, wait for completion signals such as `img.complete`, resolve locators to one element, and assert attributes or bound values in preference to rendered labels.

**destination**: `playwright/locators-and-assertions`.

#### LL.35 share fixtures once and run workers as production does

**evidence**: 07.IS.06. Two tiers each registered a session browser, and the second failed in a full run. 11.IS.13: a test ran a worker on the test thread, a second browser instance was refused, and the worker's catch-all recorded the harness error as a domain outcome. 17.IS.04: a fake browser hid a thread affinity defect that the real fixture mode exposed.

**lesson**: shared fixtures are registered once at the top. Tests run workers on their own thread, as production does. At least one check exercises the real implementation behind every fake.

**destination**: `pytest/fixtures-and-isolation`.

#### LL.36 keep startup side effects away from raw-seed checks

**evidence**: 10.IS.06. The app's startup job closed the seed's running row in the shared session database before the seed oracle read it.

**lesson**: checks of the raw seed use a database that no app instance has started against.

**destination**: `pytest/fixtures-and-isolation`.

#### LL.37 capture fixtures and stubs from real artifacts

**evidence**: 10.IS.15. Hand-written fixture pages used guessed attribute names, so every fixture test passed while the live run failed. One isolated call against a real page found the real names.

**lesson**: fixtures and stubs are captured from real responses or files, then reduced. A guessed fixture proves only the guess.

**redbooks**: exchange rate stubs come from recorded API responses, and reader fixtures come from real HomeBudget database rows.

**destination**: `pytest/oracles-and-seed-data`, `playwright/network-mocking`.

#### LL.38 pin the clock before creating time-bound state

**evidence**: 13.IS.08. A fixture opened a session at real time, then the test pinned the clock past its lifetime and got `401`. 09.IS.07: the refresh path was never exercised because the seed anchor equalled the run date.

**lesson**: one injectable clock drives every time-bound value. A test pins it before creating sessions or rows, and moves it to reach time-based paths.

**redbooks**: statement periods, rate dates and session expiry.

**destination**: `pytest/fixtures-and-isolation`.

#### LL.39 take baselines from a clean worktree

**evidence**: 08.IS.01 used a baseline to show the milestone was documented but never implemented. 18.IS.02 and 18.IS.03: a seed regeneration mid-run tainted the baseline, and the clean baseline ran from a detached worktree of `HEAD`.

**lesson**: record the baseline before changing code, from a worktree the edits cannot reach.

**destination**: `pytest/run-and-triage`.

#### LL.40 bisect order-dependent failures

**evidence**: 10.IS.05 passed alone, passed with the preceding files, and passed with full collection limited by `-k`. That showed the trigger was executing a file elsewhere in the run.

**lesson**: for a failure seen only in the full run, bisect by file set, then by collect versus execute.

**destination**: `pytest/run-and-triage`.

#### LL.41 prove every check can fail

**evidence**: 07.TC.08 injected four failures into the preflight. 13.IS.05 planted a wrong redirect URI. The 010.13 secrets scan and the docs build checks 18.TC.12, 18.TC.13 and 18.TC.34 caught planted values. 18.IS.06: a control copy failed for the wrong reason, and only passed once its inputs were complete. 09.IS.37 and 10.IS.17 showed the new test failing without the fix.

**lesson**: every new check is shown to fail on a planted fault, its control passes first, and every regression test is shown to fail without its fix.

**destination**: `feature-implementation-guide/validation`.

#### LL.42 background jobs reach a terminal status and persist progress

**evidence**: 10.IS.15. A live run stayed `running` past both poll budgets with no error. 10.IS.16 committed a progress snapshot per step, so a crashed run keeps its counts. 11.IS.11: the run's error detail named a secondary error, not the cause.

**lesson**: a background job always ends in a terminal status with the original exception recorded, and commits its progress as it goes.

**redbooks**: rate fetch and HomeBudget migration jobs.

**destination**: `python/errors-and-logging`.

#### LL.59 give every test an expected latency and fail when it is exceeded

**evidence**: 10.IS.07 closed two full-run-only timeouts as load variance without confirming the cause, on 010.17's precedent of steps slowing from 1 second to 90 seconds under load. 13.IS.25 had the same shape, and injected latency revealed a real missing wait.

**lesson**: each test carries an expected latency budget and raises a timeout exception when it is exceeded. Load variance is not an accepted close.

**decision**: tests of local operations with no network call run fast, and a delay of more than a few seconds raises a timeout exception. A standard internet API call normally takes about a second, and a delay past 30 seconds raises a timeout exception.

**destination**: `pytest/run-and-triage`, `playwright/flaky-test-triage`.

#### LL.60 scope test sets to features and keep regression growth sublinear

**evidence**: the easyMCF suite grew as one monolithic set, from 3 tests in milestone 07 to 493 in milestone 18, and the full run from 142 to 534 seconds. A global 60 second per-test timeout clashed with a 90 second poll budget in 010.10.

**lesson**: test sets are scoped to individual features, siloed unit tests first and then integration tests. Each later feature adds regression tests, so the end-to-end regression run grows, but sublinearly.

**decision**: from feature 1 to features 2, 3 and 10, the end-to-end regression run grows from about 1x to 1.5x to 2x of the first feature's run.

**destination**: `pytest/run-and-triage`, `testing-validation` agent.

### Accounting and money

#### LL.43 assert accounting identities in code and tests

**evidence**: fs accounting-logic states each rule as an identity and asserts it at the point of calculation: balanced transactions, opening plus movements equals closing, revaluation gain equals end value less start value and flows, and lot cost basis splits preserve the original total.

**lesson**: every accounting calculation asserts its identity, and worked examples show each step. The pattern transfers. The source's worked examples do not, because several are wrong, per [Accounting source irregularities](#accounting-source-irregularities). A balance check alone cannot catch a posting with both sides reversed, so each example is also checked against the stated sign convention.

**destination**: `accounting/identity-assertions`, once the design stage settles AI.01 to AI.05.

#### LL.44 run reconciliation as ordered phases

**evidence**: fs reconciliation-patterns runs seven phases: pre-checks that block, staging to one comparison shape, choosing a match strategy, matching transactions, comparing balances, classifying the variance, deciding to adjust or escalate, and closing with a record. Tolerances are set per account group.

**lesson**: reconciliation classifies every variance before any adjustment, and records its result and decision.

**redbooks**: the HomeBudget parallel run and the balance assertions.

**destination**: `accounting/reconciliation`.

#### LL.45 handle money with Decimal practice

**evidence**: fs decimal: build from strings, set the rounding mode per rule, quantise at output, trap float mixing in development, and check allocations sum exactly to their totals.

**destination**: `python/decimal-money`.

#### LL.46 configure outbound HTTP clients explicitly

**evidence**: fs httpx: one client per job, explicit timeouts, status checked before the body, transport and status errors mapped separately, query parameters passed as data.

**redbooks**: the exchange rate client.

**destination**: `python/http-clients`.

#### LL.47 count reports against stated populations

**evidence**: 020.08 Scope fixed reporting rules before design: each report returns its count, denominator and rate together, an empty denominator shows no value, event-based and cohort-based reports are labelled apart, the current partial week is marked, history is read from events because closing overwrites the current stage, and the CSV export matches the displayed figures under the same filters.

**redbooks**: statements label their period and population, mark an incomplete current period, and export the same figures they display.

**destination**: `accounting/statements`.

### Process and agents

#### LL.48 plan for the human walkthrough to find design gaps

**evidence**: 11.IS.19 surfaced a design gap that every automated layer had passed. 09.IS.37 surfaced a stale list. The 010.09 walkthrough produced about thirty interface and workflow items after automated validation.

**lesson**: the human pass is a design review as much as a test. The agent records each finding and gives the user options where the design has a gap.

**destination**: `testing-validation` agent, `feature-implementation-guide/validation`.

#### LL.49 probe an external system before designing against it

**evidence**: 010.17 settled two open design questions with a tracked, rerunnable probe script. Each step saved a screenshot, the HTML, the visible text, a findings file and a network log, and the findings became permanent regression cases. Static analysis before the costly live run caught two defects. 10.IS.15 shows the cost of designing on guesses.

**lesson**: an unknown external behavior is probed by a tracked script before design, and its findings become fixture cases.

**redbooks**: the exchange rate API and the HomeBudget database layout.

**destination**: `feature-implementation-guide/tracker-pattern`.

#### LL.50 re-validate closed evidence when the design changes

**evidence**: 07.05.08. The environment location and variable names changed after four tasks had closed, so their evidence was re-run against the new design.

**destination**: `feature-implementation-guide/validation`.

#### LL.51 change the generator when the user edits generated output

**evidence**: 18.IS.12. The user removed a generated source line by hand. The generator still produced it, so the sync check failed on the first `main` run. The published pages memory records the same preference.

**destination**: `feature-implementation-guide/implementation`.

#### LL.52 run one agent session per working tree

**evidence**: 09.IS.55. Another session was implementing feature 13 in the same working tree, so 64 tests failed on a schema this task never wrote.

**lesson**: concurrent agent sessions each use their own worktree.

**destination**: `feature-implementation-guide/implementation`.

#### LL.53 leave the user's real data and settings to the user

**evidence**: 11.IS.07 kept `.env` unedited and asked the user. 10.IS.17 diagnostic 06 left bad rows in the user's working database for the user's go-ahead. 11.IS.19 backed up the database before an in-place upgrade and checked row counts. 09.IS.36 warned that a reset destroys data worth keeping.

**lesson**: the agent never edits `.env` or the user's working database without a go-ahead in that turn, and backs up before any in-place change.

**destination**: agent shared boundaries, `data-migration-engineer` agent.

#### LL.54 reconcile test cases with scope and edit locations before implementing

**evidence**: 12.IS.01 found test cases written before the fixture shape existed. 08.IS.12 found a case expecting behavior outside the milestone's scope. 10.IS.13 found an edit location assigning UI checks to a backend file. 11.IS.02 found a required field with no column. 11.IS.16 found a tracker command written in a syntax the tool rejects.

**lesson**: before implementing, read the test cases against the scope, the data model and the edit locations, and trace every scope field to its storage. Run every tracker command literally once before publishing it.

**destination**: `feature-implementation-guide/tracker-pattern`.

#### LL.55 keep issue ids unique and hypotheses provisional

**evidence**: 09.IS.34 found one id used twice by two numbering streams. The 010.09 Validate preamble: a hypothesis stays a hypothesis until a fix is applied and re-validated.

**destination**: `feature-implementation-guide/validation`.

#### LL.56 publish docs through a strict build

**evidence**: 18.IS.04 and 18.IS.11 found relative links one level too shallow, already broken on GitHub. 18.IS.05 found GitHub-style anchors that the docs builder slugs differently. 18.IS.07: the dev server mounts pages under the site path. 18.IS.09: a manual workflow runs only from the default branch. 18.IS.10: the access token lacked the workflow permission. The user's published pages memory keeps release references out of published pages.

**lesson**: a strict build checks every link and anchor, pages carry no release references, and workflow and token prerequisites are listed in the tracker as user actions.

**redbooks**: the docs publishing milestone.

**destination**: `documentation-style/published-docs`.

#### LL.57 scope by extending what exists

**evidence**: the reuse-first memory, from 010.12. A draft scoped a new validation utility where an existing script already did most of the job.

**destination**: `feature-implementation-guide/tracker-pattern`.

#### LL.58 design text states the chosen specification

**evidence**: the spec-only design memory. The user found alternative and negation phrasing confusing in design sections.

**destination**: `documentation-style` rule.

#### LL.61 keep implementation guides to code snippets

**evidence**: 010.09 grew to 7404 lines. Its edit locations held full source listings, and a nested 09.13 tracker sat inside Task Details. Rehearsing the snippets caught 09.IS.33 before implementation, but snippets drifted from their prose in 09.IS.35 and carried a defect in 13.IS.17.

**lesson**: edit locations and implementation steps hold short code snippets only, never large blocks of source.

**destination**: `feature-implementation-guide/tracker-pattern`.

#### LL.62 grow a feature with a sub-feature first

**evidence**: 09.IS.38 to 09.IS.46 were feature requests from the walkthrough, logged as issues with full specifications. They became the 09.13 sub-feature and moved the schema two versions inside one milestone.

**lesson**: a feature request found during validation becomes a sub-feature of the current feature, unless its scope warrants a new milestone line item and its own feature tracker.

**destination**: `feature-implementation-guide/tracker-pattern`, `product-manager` agent.

## Lessons to be learned

Each item is a hypothesis with a way to test it in RedBooks. Results are recorded in the feature tracker where the test runs, and the audit skills milestone promotes or drops each one.

#### LT.01 generate more cross-cutting tests from the route table

Hypothesis: the registry-generated ownership matrix in LL.19 also works for the per-endpoint error template of the **easymcf test strategy**, `STRAT-SILO-04`, and for vocabulary coverage. Experiment: generate both from FastAPI's route table in the first API milestone, and count the defects they catch that hand-written cases miss.

#### LT.02 replace variance closes with latency injection

Hypothesis: delaying a route in Playwright reproduces full-run-only timeouts deterministically, as it did for 13.IS.25. Experiment: for each full-run-only failure in RedBooks, add a delayed-route reproduction before any close. The latency budgets of LL.59 decide when a test fails.

#### LT.03 check that every process runs in the mode the env file selects

Hypothesis: a startup log line with the effective mode, and a test that the app, a script and the test fixtures build identical settings from one `.env`, catch the split LL.01 describes before it reaches a run. Experiment: add both in the local dev env milestone, then change the mode in `.env` once and confirm every process follows it.

#### LT.04 move a walkthrough earlier

Hypothesis: a short human walkthrough of a rough page early in a feature reduces the late interface feedback seen in 010.09. Experiment: walk through the first transaction entry page on the phone viewport before its tests are complete.

#### LT.05 prove the real seed data stays private

Question: which paths can carry seed data out of its storage location, such as committed logs, test output, fixture files, screenshots and the docs build? Research during the HomeBudget data review, and turn each path into a closure check.

#### LT.06 test whether migrations catch easyMCF's drift class

Hypothesis: Alembic revisions with a startup head check catch the version drift in LL.06 automatically. Experiment: when RedBooks adopts forward migrations ahead of the account `01` migration, per LL.06, deliberately skip one step and confirm a check fails.

#### LT.07 trial skill changes before promoting them

Hypothesis: fs subagent-trial-methodology's control and experiment design shows whether a skill change from this milestone changes agent behavior. Only a failing control with a passing experiment counts as evidence, and criteria are set before the run. Experiment: trial three of the new generic skills on representative tasks.

#### LT.08 probe the exchange rate source before design

Question: how does the rate API used by the homebudget wrapper handle weekends, missing dates, rate limits and historical ranges? Experiment: a probe script per LL.49, run by the user, with findings saved as fixtures.

## Accounting source irregularities

fs accounting-logic is the most detailed accounting reference RedBooks inherits, and its identity-plus-example pattern is worth keeping. Its worked examples are not. They are written in debit and credit columns, and every example ends with an identity check marked as passing. The checks only compare the two column totals, so they pass when every sign in a posting is flipped, and in one case the check passes on figures that do not balance.

Each item below translates the source's columns into signed entries, per AR.01 and AR.17 of the **accounting rules**. The translation uses the convention the skill's own salary and forex examples follow, where a debit raises a cash balance and raises spending.

Each irregularity is resolved in the design stage of the **release milestones**, by the design topic named. Until then, agents treat every figure and every entry direction in fs accounting-logic as unverified. No example moves into a RedBooks skill, test oracle or design doc until it has been re-derived under the signed rules. the [accounting rules](accounting-rules.md) states those rules and reworks each example.

#### AI.01 the expense example records a purchase with both signs reversed

**source**: the double-entry section's bill payment example, SGD 50 paid by credit card. It puts 50.00 in the credit column of the personal expense cost center and 50.00 in the debit column of the card account.

**why it is wrong**: translated, the posting reverses 50.00 of spending, a +50.00 entry on the expense, and reduces the amount owed, a +50.00 entry on the card. A purchase is a -50.00 entry on the expense and a -50.00 entry on the card, so the amount spent and the amount owed both grow. The same skill's forex example records the same kind of event with the correct signs, and both identity checks pass.

**resolve in**: the data model topic, 04.05, which sets how the general ledger stores signed entries.

#### AI.02 the unrealised gain example records the gain as a loss

**source**: the mark-to-market section. A USD 250.00 unrealised gain puts 250.00 in the credit column of the position account and in the debit column of `P&L:Unrealized`. The quarterly revaluation repeats the pattern for 350.00.

**why it is wrong**: translated, the position falls by 250.00 and the profit and loss line reads as a loss of 250.00. A gain raises the position by 250.00 and raises unrealised gain income by 250.00. The FIFO example in the same skill records its realised gain with the correct sign.

**resolve in**: the multi currency and forex topic, 04.08, together with 04.05.

#### AI.03 the CPF example fails its own identity

**source**: the CPF section. A SGD 2,000.00 deduction is split into OA 740.00, SA 740.00 and MS 160.00, which is 82 percent of the total. The posting puts 2,000.00 in the bank's debit column and 1,640.00 across the three CPF accounts' credit columns. The check line reads "debit (2000) = credit (740 + 740 + 160) ✓".

**why it is wrong**: 2,000.00 does not equal 1,640.00, so the posting does not balance and the check is false. Translated, it also raises the bank balance by 2,000.00 and lowers the three fund balances by 1,640.00, where a contribution lowers what reaches the bank and raises the funds. The employer's 400.00 posts separately and is never shown.

**resolve in**: outside `0.2.0` scope. CPF accounts are not in the release, so the example stays excluded until a release takes them on.

#### AI.04 the period roll-up contradicts the cost center rule

**source**: the period roll-up section. The cost center opens March at 500.00 and closes at -500.00, while fs homebudget states that this cost center closes to zero every month, the account `01` rule in the **homebudget accounts** doc. The statement roll-up verification line computes 2500 - 1000 - 500 as a positive 1000 against a net movement of -1000.

**why it is wrong**: the example breaks the HomeBudget rule it describes, and its verification line changes sign partway through.

**resolve in**: the HomeBudget data review, 04.04, which records how the cost center behaves in the real snapshot, and the financial statements topic, 04.09.

#### AI.05 the identity checks cannot catch a reversed entry

**source**: every example's check compares only the debit column total with the credit column total.

**why it is wrong**: flipping every sign in a posting keeps the two totals equal, so AI.01 and AI.02 pass. AI.03 passes only because its check was never computed.

**resolve in**: the test strategy and test cases milestones. RedBooks accounting oracles check the sign of each entry against the event, per AR.03 of the **accounting rules**, as well as the balance rule, and compute every check from the figures.

## Correct accounting rules

The correct accounting rules, with their signed entry convention, the HomeBudget account `02` posting model and worked examples for every irregularity above, live in the **accounting rules** doc: [accounting-rules.md](accounting-rules.md).

## Hybrid approach for RedBooks skills and agents

The RedBooks skills carry confirmed lessons as rules, and carry lessons to be learned as flagged, unsettled material that agents observe and report on. The approach has six parts.

01. **an open-lessons reference file per skill.** Each skill that has open items gains `references/open-lessons.md`. Each entry holds its `LT` id, a status of `open`, `experimenting` or `resolved`, the question, the evidence that would settle it, and the experiment if one exists. `SKILL.md` names the file in its references table with the trigger "a task touches one of the listed areas".
02. **a visible callout where an open item meets a rule.** Skill text that touches an open item carries a one-line callout, `**open lesson LT.NN**`, followed by the question in a sentence. An agent reading the callout knows the practice is unsettled and does not present it as a rule.
03. **an observation duty for every agent.** One line joins the shared boundaries block: when a task touches an open lesson, record what happened in the feature tracker's Validate section as `lesson observation LT.NN` with the evidence. A lesson stays open until the audit skills milestone resolves it.
04. **an experiment section in the tracker.** A feature that runs an `LT` experiment records the hypothesis, the control, the change, the criteria set before the run, and the result, following fs subagent-trial-methodology. Skill and agent changes use the same control and experiment trial.
05. **promotion in the audit skills milestone.** The milestone reads every lesson observation and experiment result, moves resolved items into skill rules or reference lessons, and updates this document's status for each item.
06. **checks for the costliest lessons.** LL.01 and LL.02 recurred because written rules lagged behind the project. Their checks run automatically: a test that the app, the scripts and the tests read the same `.env` and report the same effective mode, and a test that an irreversible write without its second opt-in is refused.

The lessons to be learned map to skills and agents as follows.

| id             | skill or agent                                    | status            |
| -------------- | ------------------------------------------------- | ----------------- |
| LT.01          | `pytest`, `fastapi`                               | experimenting     |
| LT.02          | `playwright`                                      | experimenting     |
| LT.03          | `python`, `feature-implementation-guide`          | experimenting     |
| LT.04          | `react`, `testing-validation`                     | experimenting     |
| LT.05          | `data-migration-engineer`                         | open              |
| LT.06          | `postgresql`                                      | experimenting     |
| LT.07          | all skills, audit skills milestone                | experimenting     |
| LT.08          | `python`, `architect`                             | experimenting     |
| AI.01 to AI.05 | `accounting`, `architect`                         | resolve at design |

## Lessons to apply to the planning documents

These are the changes the lessons and the user's decisions make to the planning documents, staged for task 05.18 of the **agent skills tracker**. The release structure comes first, in PD.01, and every later entry follows from it. Entries PD.02 to PD.17 follow the milestones in their new sequence. A **merge**, **new** or **replace** entry gives the milestone's new section text or the full set of its changes. An **edit** entry quotes the current text it replaces, states the change, and lists the lessons behind it. PD.18 and PD.19 cover the release notes at [020-release.md](../020-release.md) and the **test strategy tracker** at [020.02-test-strategy.md](../features/020.02-test-strategy.md).

The **stage** line names the item in the Planning documents section of the **agent skills tracker** that the entry details. A stage of **new** marks a change this staging found outside the tracker's staged items. The test strategy milestone owns the **test strategy tracker**, so task 05.18 agrees PD.03 and PD.19 with that milestone before applying them. Committed planning text names no real snapshot account. Where a current sentence does, the entry describes the account by its role.

| id    | document              | section                              | change  | stage    |
| ----- | --------------------- | ------------------------------------ | ------- | -------- |
| PD.01 | release milestones    | feature milestones table             | restruc | new      |
| PD.02 | release milestones    | agent skills customization           | edit    | new      |
| PD.03 | release milestones    | test strategy and cases              | merge   | 05.LA.19 |
| PD.04 | release milestones    | design                               | edit    | 05.LA.21 |
| PD.05 | release milestones    | agent skills implement customization | edit    | 05.LA.22 |
| PD.06 | release milestones    | local dev and test env               | edit    | 05.LA.23 |
| PD.07 | release milestones    | schema and account 02 seed           | replace | 05.LA.25 |
| PD.08 | release milestones    | validation utilities                 | edit    | 05.LA.24 |
| PD.09 | release milestones    | oauth login                          | edit    | 05.LA.26 |
| PD.10 | release milestones    | audit skills checkpoint              | new     | 05.LA.31 |
| PD.11 | release milestones    | currency model                       | edit    | 05.LA.27 |
| PD.12 | release milestones    | txn and accounts                     | edit    | 05.LA.28 |
| PD.13 | release milestones    | financial statements                 | edit    | 05.LA.29 |
| PD.14 | release milestones    | homebudget account 01 migrate        | replace | 05.LA.30 |
| PD.15 | release milestones    | audit skills promote learning        | edit    | 05.LA.31 |
| PD.16 | release milestones    | mkdocs documentation                 | edit    | 05.LA.32 |
| PD.17 | release milestones    | publish and release                  | edit    | 05.LA.32 |
| PD.18 | release notes         | ledger, history, milestone phases    | edit    | 05.LA.33 |
| PD.19 | test strategy tracker | scope, strategy, fixtures, cases     | edit    | 05.LA.34 |

#### PD.01 release milestones: feature milestones table

**stage**: new.

The lessons change how tests are planned, what the seed is, when the agents learn, and what the migration carries. The release keeps its define, setup, implement and release phases, and the up-front define phase the requirements audit settled in 01.04.08.

01. **merge test cases into the test strategy.** Test strategy, id `02`, becomes "test strategy and cases" and takes in the test cases milestone, id `03`, which is retired. The milestone writes the strategy and the release-level case catalogue. Each feature milestone copies its cases from the catalogue into its own tracker, reconciles them with its scope, data model and edit locations before implementing, and owns them as its feature-scoped test set. The milestone's tracker already covers both, as **test strategy tracker**. Lessons: LL.54, LL.57, LL.60.
02. **the seed milestone builds the schema and loads the real account `02` data.** Setup database seed data, id `07`, becomes "schema and account 02 seed". It creates the schema from the data model design, loads the account `02` data as-is, and owns the one command that rebuilds the schema and reloads the seed on every schema change during `0.2.0` development. PD.07 replaces its section. Lessons: LL.06, LL.08 decisions.
03. **the validation utilities follow the seed.** Their database reset and reference checks read the seed and the expected-value fixtures the seed load writes. Built after the seed, each check is shown to fail on a planted fault against real data. The release notes' setup phase already describes this order. Lessons: LL.37, LL.41.
04. **insert an audit skills checkpoint after the first feature.** New milestone `18`, "audit skills checkpoint", runs after oauth login. The costliest easyMCF lessons, LL.01 and LL.02, recurred for a whole release because the written rules lagged behind the project. LT.01, LT.03 and LT.08 gather their evidence in the design, the foundation and the first feature, so promoting them there gives the four remaining features confirmed rules. This settles requirements audit item 01.04.10. PD.10 holds its section. Lessons: LL.02, LT.07, the Hybrid approach.
05. **the migration carries the account `01` history.** Data migrate, id `12`, becomes "homebudget account 01 migrate". It runs after every feature milestone is validated, so the large account `01` data is migrated as few times as possible, and its first task adopts versioned forward migrations. PD.14 replaces its section. Lessons: LL.06 decision, LT.06.
06. **the design probes the rate API first.** The design milestone gains task `04.19 exchange rate api probe`, ahead of `04.08 multi currency and forex`, per PD.04 item 08. Lessons: LL.49, LT.08.
07. every other milestone keeps its id and name, takes its new sequence below, and takes the edits in PD.02 to PD.17.

Proposed table, with every milestone in release `020`:

| id | seq | status  | feature                              |
| -- | --- | ------- | ------------------------------------ |
| 01 | 01  | closed  | requirements                         |
| 05 | 02  | open    | agent skills customization           |
| 02 | 03  | open    | test strategy and cases              |
| 04 | 04  | pending | design                               |
| 16 | 05  | pending | agent skills implement customization |
| 06 | 06  | pending | local dev and test env               |
| 07 | 07  | pending | schema and account 02 seed           |
| 08 | 08  | pending | validation utilities                 |
| 09 | 09  | pending | oauth login                          |
| 18 | 10  | pending | audit skills checkpoint              |
| 17 | 11  | pending | currency model                       |
| 10 | 12  | pending | txn and accounts                     |
| 11 | 13  | pending | financial statements                 |
| 12 | 14  | pending | homebudget account 01 migrate        |
| 13 | 15  | pending | audit skills promote learning        |
| 14 | 16  | pending | mkdocs documentation                 |
| 15 | 17  | pending | publish and release                  |

01. id `03` is retired into id `02`, and id `18` is new. The Contents list and the section headings of the **release milestones** take the new names and order.

#### PD.02 release milestones: agent skills customization

**stage**: new. The **agent skills tracker** records the deviation under its 05.CK closure criteria, and task 05.09 deleted the inventory.

01. the last paragraph of Lessons in the generic skills reads "A lessons inventory, `020-easymcf-lessons.md` in this release folder, lists each lesson with its source and the skill and file it moved to." Replace it: this document holds every lesson with its evidence, and the Lesson trace of the **agent skills tracker** records the skill, agent or planning document each lesson lands in.
02. closure criterion 06 reads "the lessons inventory lists every lesson from the easyMCF sources above, with its destination skill and file, or a reason it stays with easyMCF." Replace it: every lesson in this document has a destination in the Lesson trace and lands there, and every finding that stays with easyMCF is listed in Not transferred.
03. add a closure criterion: every agent carries the shared boundaries block, and every lesson to be learned has an entry in an `open-lessons` file with its status. Lessons: LL.53, the Hybrid approach.

#### PD.03 release milestones: test strategy and cases

**stage**: 05.LA.19 and 05.LA.20, with the merge of PD.01 item 01. Items 01, 08 and 09 are new.

01. **merge.** The section is renamed "Test strategy and cases". The Test cases section's description and closure criteria move into it under a **Cases** heading, and the Test cases section is removed.
02. add a **live order** rule after Component silos: automated protocols run against the stubs first, then live for everything except irreversible writes. The full live OAuth flow with its writes is the user's own check. Lessons: LL.03, LL.23.
03. Component silos reads "with no other component's correctness as a precondition and no live network call", and case selection rule 04 reads "no test depends on wall-clock time, a live network call or a fixed sleep." Limit both to the silo protocols. A live protocol depends on the network by design and runs under its latency budget. Lessons: LL.59.
04. add a **latency budgets** rule: every test has an expected latency budget and raises a timeout when it is exceeded, a few seconds for local work and 30 seconds for an internet API call. Load variance is never an accepted close. Lessons: LL.59.
05. add a **feature-scoped test sets** rule: each feature owns its test set, siloed unit tests first and integration tests after. The end-to-end regression run grows sublinearly, about 1x, 1.5x and 2x of the first feature's run at features 1, 2 to 3, and 10. Lessons: LL.60.
06. add a **settings** rule: tests read settings from `.env` through the app's settings object, and every run reports its effective mode. Lessons: LL.01.
07. Reference data from HomeBudget reads "The seed script writes these expected values as fixtures next to the seed data, under the same made-up names, with amounts and dates unchanged." Replace "under the same made-up names" with "under the real names from the snapshot, in the uncommitted seed location". Lessons: LL.08 decision.
08. add to **Cases**: the catalogue holds the release-level cases. Each feature milestone copies its cases into its own tracker and reconciles them with its scope, data model and edit locations before its first implement step, and the cross-cutting cases, such as the ownership matrix and the reference checks, stay in the catalogue. Lessons: LL.54, LL.60.
09. Test cases closure criterion 04 reads "every edge case recorded in the HomeBudget data review has a test case." The data review closes in the design milestone, which now follows. Its edge cases go into the catalogue when the review closes, and the design audit of design closure criterion 12 checks them. Lessons: LL.54.
10. add to **Cases**: expected values come from oracles and data reads, never hand counts, and boundary cases account for library tolerances such as token clock leeway. Lessons: LL.22, LL.33.
11. add closure criteria: every accounting oracle checks each entry's sign against its event as well as the balance and computes every check from its stated figures, and every regression case is shown to fail without its fix. Lessons: AI.05, LL.41.
12. add closure criteria for items 02, 04, 05 and 08.

#### PD.04 release milestones: design

**stage**: 05.LA.21, plus item 08, which is new.

01. stage 02, accounting model, names the snapshot and the **homebudget wrapper** as its basis. Add the **accounting rules** and the **homebudget accounts** docs as design inputs, and add a closure criterion: every accounting design doc follows the **accounting rules** and copies no fs accounting-logic example. Lessons: AI.01, AI.02, AI.03, AI.04.
02. closure criterion 05 lists what the data model defines. Add that ledger entries are signed amounts per the **accounting rules**, and that the schema rebuilds and reloads the seed during development, with versioned forward migrations before the account `01` migration. Lessons: LL.06.
03. closure criterion 10 lists what the API endpoints doc defines. Add one explicit router per resource, with writes that carry invariants routed through services. Lessons: LL.16.
04. closure criterion 06 lists what the multi currency doc defines. Add the foreign currency entry model of AR.12 in the **accounting rules**.
05. closure criterion 09 covers the handling of personal data. Add the rule that committed code, committed docs and the published site show no real account names, account numbers or personal details. Lessons: LL.08.
06. closure criterion 07 covers the HomeBudget data review. Add that the review answers the questions in the **homebudget accounts** doc, adds its edge cases to the case catalogue, and sets the reference figures the account `01` migration is checked against. Lessons: LL.08, LL.54.
07. closure criterion 12 audits the design against the test cases. Name the case catalogue of the test strategy and cases milestone, per PD.03.
08. add task `04.19 exchange rate api probe` to the tasks table at seq 08, ahead of `04.08 multi currency and forex`, which moves to seq 09 with every later task shifting by one. The user runs the probe, and its findings are saved as fixtures. Add a closure criterion: the multi currency and forex topic closes only after the probe. Lessons: LL.49, LT.08.

#### PD.05 release milestones: agent skills implement customization

**stage**: 05.LA.22.

01. add to the bespoke skills list where each draws its rules: `redbooks-ledger` and `redbooks-statements` from the **accounting rules**, `redbooks-currency` from its foreign currency rules, and `redbooks-homebudget-migration` from the **homebudget accounts** doc, covering both the account `02` seed and the account `01` migration. Item 07, `redbooks-deploy-and-validation-cycle`, takes the place of the removed generic run loop skill.
02. add a closure criterion: a skill change is trialled against a control before it is promoted, and only a failing control with a passing experiment counts. Lessons: LT.07.

#### PD.06 release milestones: local dev and test env

**stage**: 05.LA.23.

01. the description reads "Environment variables are set through a `.env` file." Add: one settings object reads `.env` directly for the app, the scripts and the tests, and every run logs its effective mode. Lessons: LL.01.
02. add a closure criterion: one command creates an empty database. The schema and account 02 seed milestone extends it to build the schema and reload the seed, per PD.07. Lessons: LL.06.
03. add closure criteria: the preflight check is proven against injected failures, and each agent session runs in its own worktree. Lessons: LL.41, LL.52.
04. add a closure criterion: a test checks that the app, a script and the test fixtures run in the mode `.env` selects. Lessons: LT.03.

#### PD.07 release milestones: schema and account 02 seed

**stage**: 05.LA.25, with the rename of PD.01 item 02. This section replaces Setup database seed data in full.

Proposed section:

> This milestone builds the database schema from the data model design and loads the user's HomeBudget account `02` export from `data/` as the seed that tests, demos and daily development run on. The seed is the real data, loaded as-is with its account names, payees and notes, so RedBooks is usable from day one and its figures compare directly with HomeBudget. The seed and everything built from it stay in uncommitted locations, out of version control and the published docs. During `0.2.0` development, one command rebuilds the schema and reloads the seed, and every schema change, in this milestone and in every feature milestone after it, runs through that command and changes the schema, the seed load and the data model doc together. The account balances file supplies each account's reconciled balance points. The same load writes the expected-value fixtures, read from the snapshot files directly, from the report's budget section, the account balances file and the fx transfers file.
>
> **closure criteria**
>
> 01. one command builds the schema from the data model design and reloads the seed from `data/` into an empty database.
> 02. the seed holds the account `02` export as-is, with its real account names, payees and notes, and a second user with distinct data.
> 03. the seed and the expected-value fixtures live in the uncommitted location the repo layout design sets, `git check-ignore --no-index` passes for every seed path, and the docs build includes none of them.
> 04. every account has its reconciled balance points from the account balances file.
> 05. counts, balances and dates derived from other rows are computed by the loader, loader inputs are pinned, loading twice gives an identical database, and every changed generated file is reviewed.
> 06. every closed vocabulary value has a seeded row, and every constraint comes from the requirements.
> 07. the seed holds stored USD to SGD exchange rates for every date it needs, and each transfer between currencies carries the two amounts from the fx transfers file.
> 08. the expected-value fixtures hold the category totals, account balances, fx transfer amounts and section row counts, each read from the snapshot files without running RedBooks code.
> 09. the seed includes every edge case in the case catalogue, and passes every expected-value check.
> 10. every path that could carry seed data out of its location, such as logs, test output, screenshots, traces and the docs build, has a check shown to fail on a planted real value.

Lessons: LL.06, LL.07, LL.08, LL.09, LL.10, LL.11, LL.41, LT.05, AR.11.

#### PD.08 release milestones: validation utilities

**stage**: 05.LA.24, plus items 01 and 04, which are new.

01. the description builds on the scripts of the local dev and test env milestone. Add that it also builds on the seed load and expected-value fixtures of the schema and account 02 seed milestone, which precedes it, per PD.01 item 03.
02. closure criterion 07 already plants one deliberate failure of each kind. Extend it so every check is shown to fail on a planted fault before it is trusted, and add that every tool applies the latency budgets. Lessons: LL.41, LL.59.
03. add a closure criterion: a tool that writes into the user's working database refuses to run without the second opt-in, and backs up first. Lessons: LL.03, LL.53.
04. closure criterion 10 reads "the deploy and validation cycle skill names each tool, when to use it and its command." The generic skill is removed. Name `redbooks-deploy-and-validation-cycle`, written in the agent skills implement customization milestone.

#### PD.09 release milestones: oauth login

**stage**: 05.LA.26.

01. api endpoints item 03 reads "every data endpoint rejects a request without a valid session." Add that an unknown path under the API prefix answers 401 to a signed-out request, every token validation error answers 401, and boundary cases account for the library's clock leeway. Lessons: LL.18, LL.21, LL.22.
02. front end item 04 reads "automated browser tests sign in through the stub identity provider set in the test strategy." Add that automated tests then make live calls for everything except irreversible writes, and the full live OAuth flow with its writes is the user's test. Lessons: LL.23.

#### PD.10 release milestones: audit skills checkpoint

**stage**: 05.LA.31, with the insertion of PD.01 item 04. This section is new, placed after Oauth login.

Proposed section:

> This milestone runs once the design, the foundation and the first feature are built. It reads every `lesson observation` and experiment result the trackers have recorded so far, trials the skill changes they suggest against a control, and promotes or drops each lesson to be learned whose evidence is in, such as the route table tests of LT.01, the mode check of LT.03 and the rate API probe of LT.08. The four remaining feature milestones then start from the promoted rules. Lessons still open carry forward to the audit skills promote learning milestone.
>
> **closure criteria**
>
> 01. every `lesson observation` and experiment result recorded so far is listed with its lesson and its tracker.
> 02. each lesson to be learned with settling evidence is promoted into a skill rule or reference lesson, or dropped, and its status is updated in the **lessons learned**.
> 03. each skill change is trialled against a control before it is promoted, and only a failing control with a passing experiment counts.
> 04. every changed skill and agent passes a documentation style review, and every agent still carries the identical shared boundaries block.

Lessons: LL.02, LT.01, LT.03, LT.07, LT.08, the Hybrid approach.

#### PD.11 release milestones: currency model

**stage**: 05.LA.27.

01. api endpoints item 09 reads "a rate API failure returns a clear error". Add that the exchange rate client sets explicit timeouts and names each failure cause with a fix, and that the fetch job always reaches a terminal status with its original exception recorded. Lessons: LL.21, LL.42, LL.46.
02. add to the description: the client builds on the findings of design task `04.19 exchange rate api probe`, and its stubs come from the probe's saved responses. Lessons: LL.37, LT.08.
03. add to the description: an exchange rate defaults to the live fetched value and the user can override it, per AR.12 of the **accounting rules**.

#### PD.12 release milestones: txn and accounts

**stage**: 05.LA.28.

01. the description reads "An expense or income can be entered in any of the user's currencies, as in HomeBudget." Replace it: a reporting currency account accepts an expense or income in any of the user's currencies and stores the converted amount, a foreign currency account accepts only its own currency, and the record keeps the nominal currency, amount and rate. Apply the same rule to api endpoints item 09 and front end item 12.
02. add: a card's foreign exchange fee is a separate expense on the same card, per AR.12 item 05.
03. api endpoints item 04 reads "the account balance for any date equals the opening balance plus the ledger entries up to that date." Replace it: the balance equals a reconciled balance point plus the signed entries between the two dates, and the opening balance is the first point.
04. the description reads "A split purchase is recorded as one expense per category in the cost center account plus a transfer from the payment account for the total." Lead with the direct posting: an expense or an inflow posts on any asset or liability, and a refund reverses its category on the account that receives it. The cost center is an optional clearing account for splits, and billing accounts return to zero when settled. Lessons: accounting rules AR.05 to AR.08.
05. add database criteria: an account or category with posted transactions is retired, and single-active rules are partial unique indexes. Lessons: LL.12, LL.14.
06. add that ledger writes go through services, and every view showing changed data refreshes after a write, keeping fields the user is editing. Lessons: LL.16, LL.27.

#### PD.13 release milestones: financial statements

**stage**: 05.LA.29.

01. add to the description: the income statement shows expenses as positive amounts only when it is presented. The books, the API and every oracle hold signed entries. Lessons: AR.18.
02. add a closure criterion: each report labels its population and period, and marks an incomplete current period. Lessons: LL.47.

#### PD.14 release milestones: homebudget account 01 migrate

**stage**: 05.LA.30, with the rename of PD.01 item 05. This section replaces Data migrate in full.

Proposed section:

> This milestone migrates the user's HomeBudget account `01` history into their working RedBooks database. The account `02` snapshot is already the seed, so this milestone carries the older history that account `02` does not hold. It starts only after every feature milestone is validated and tested, so the large account `01` data is migrated as few times as possible. Its first task adopts versioned forward migrations, so the working database keeps its data across every later schema change. The migration maps the account `01` legacy categories onto the account `02` categories, and keeps the account `01` cost center clearing history, per AR.07 item 05 of the **accounting rules**. The load uses upsert logic: it matches each account, category, transaction and transfer against what the user already holds by the match key from the HomeBudget data review, adds the records that are new, and skips the records already present. Identical transactions on the same day are separate records, so the key counts each occurrence and keeps them all. The migration writes into the user's working database only with a second opt-in, after a backup, and checks its results against the reference figures the HomeBudget data review sets for account `01`.
>
> **closure criteria**
>
> 01. versioned forward migrations are in place, the app checks the migration head at startup, and a deliberately skipped step fails a check.
> 02. one command migrates the account `01` history into a user. It refuses to write without the second opt-in, and backs up the working database first.
> 03. every legacy category maps to one account `02` category, and the mapping lists any category it could not map.
> 04. every account `01` row is loaded, skipped as already present, or listed in the migration report with the rule that handled it, and the report counts the records added and skipped for each kind.
> 05. records that overlap the account `02` seed match by the match key, and no duplicate account, category or transaction is created.
> 06. identical transactions on the same day each load as their own record.
> 07. running the migration a second time adds zero records and leaves every balance and total unchanged.
> 08. the migrated cost center closes at zero for every finished split.
> 09. migrated balances and category totals match the account `01` reference figures, checked by the validation utilities.
> 10. the migration job reaches a terminal status with its original exception recorded on failure, and commits its progress as it goes.

Lessons: LL.03, LL.06, LL.42, LL.53, LT.06, AR.07.

#### PD.15 release milestones: audit skills promote learning

**stage**: 05.LA.31.

01. the description reads "It collects the lessons recorded in feature trackers, logs and issues". Add that it starts from the results of the audit skills checkpoint, per PD.10, and covers the observations recorded since.
02. closure criterion 01 reads "a lessons list records each lesson with its source." Replace it: the milestone reads every `lesson observation` and experiment result since the checkpoint, promotes or drops each remaining lesson to be learned, and updates its status in this document. Lessons: LT.01 to LT.08.
03. add a closure criterion: each skill change is trialled against a control before it is promoted. Lessons: LT.07.

#### PD.16 release milestones: mkdocs documentation

**stage**: 05.LA.32 items 01 and 02.

01. closure criterion 04 reads "the published site builds with no broken links." Replace it: the site builds in strict mode, which fails on every broken link and anchor, and published pages carry no release references. List the workflow and token prerequisites as user actions. Lessons: LL.56.
02. add a closure criterion: published pages show no real account names or personal details, only hypothetical names at real Singapore institutions, and the build includes no data file. Lessons: LL.08.

#### PD.17 release milestones: publish and release

**stage**: 05.LA.32 item 03.

01. closure criterion 02 reads "the full test suite passes on the release commit." Add that the run starts from a clean worktree of the release commit. Lessons: LL.39.

#### PD.18 release notes

**stage**: 05.LA.33, plus items 02 to 05, which are new.

01. HomeBudget history reads "The data migration loads the full HomeBudget history into RedBooks from a snapshot the user exports from the HomeBudget app." Replace it: the account `02` snapshot is the seed, loaded as-is from day one, and the account `01` migration loads the older history after the release's features are validated. Lessons: LL.06, LL.08.
02. Design: Define the release reads "The test strategy and test cases follow from the requirements". Replace it: the test strategy and its case catalogue follow from the requirements, and each feature reconciles its own cases with the design before it is built, per PD.01 item 01.
03. Setup: Prepare the foundation reads "Database seed data draws on the HomeBudget review, so tests and demos run on realistic accounts and transactions in SGD and USD." Replace it: the schema and account 02 seed milestone builds the schema and loads the user's real accounts and transactions as-is, and the validation utilities that follow check every change against that data, per PD.01 items 02 and 03.
04. Implement: Build the features reads "OAuth login comes first because every other feature belongs to a signed-in user." Add: an audit skills checkpoint follows it, so the remaining features start from the rules the release has confirmed so far, per PD.01 item 04.
05. Implement: Build the features reads "Data migrate comes last in this phase. It loads the full HomeBudget history into the finished data model and working ledger." Replace it: the homebudget account 01 migrate milestone comes last in this phase, and migrates the account `01` history into the finished data model and working ledger.

#### PD.19 test strategy tracker

**stage**: 05.LA.34, plus items 05 to 07, which are new.

01. the live order of PD.03 item 02 replaces the human-gated live check in four places: Scope item 01, "a live smoke check against the real OAuth provider and rate API, is human-gated and outside the agent loop", the 02.PR.07 row with its runner `human-gated` and protocol summary item 07, 02.AU.05, and 02.HV.03. Lessons: LL.03, LL.23.
02. 02.GP.01 and 02.CS.04 limit the no live network rule to the silo protocols, as in PD.03 item 03. 03.FX.07 keeps its wording, since it checks the automated silo protocols. Lessons: LL.59.
03. add the latency budgets and the feature-scoped test sets of PD.03 items 04 and 05. Lessons: LL.59, LL.60.
04. note 01 under the fixture table that follows 02.TD.08, and cases 03.FS.04 and 03.MIG.10, name two real snapshot accounts. Describe them by role, as the two SGD accounts with monthly figures in the account balances file. The real names stay in the uncommitted fixtures. Lessons: LL.08.
05. 02.TD.04 reads "under the same made-up names". Replace it with "under the real names from the snapshot", matching 02.TD.10 and PD.03 item 07. Lessons: LL.08 decision.
06. the tracker becomes the tracker of the merged test strategy and cases milestone. Its test case tables form the case catalogue that each feature tracker copies from, per PD.03 item 08.
07. the HomeBudget migration silo cases, such as 03.MIG.10, check the account `02` snapshot load. They move to the schema and account 02 seed milestone, and the account `01` migration writes its own cases in its tracker, per PD.01 items 02 and 05.

## Not transferred

These findings have no common relevance to RedBooks and stay with easyMCF.

01. **MyCareersFuture site and scraping**: recommended cards in 10.IS.17, markup drift and the selector registry in 020.07, discovery and detail passes, and polite request pacing in the `webscraping` skill.
02. **Singpass and site sessions**: 11.IS.21 to 11.IS.23 and 17.IS.05 to 17.IS.28, apart from the generic lessons cited above.
03. **AngularJS**: the missing base tag in 07.IS.05, child scope shadowing in 13.IS.19, digest loops in 10.IS.16, and the end-of-life risk in ISS-06.
04. **job search domain rules**: lead stages and deadlines, the apply outcome vocabulary, event precedence in 13.IS.20, application cohort counting in 020.08, and role keyword scoring in 020.09.
05. **environment specifics**: the WSL memory ceiling in 07.IS.02 and missing Chromium system libraries in 07.IS.03. Both go to `redbooks-deploy-and-validation-cycle` if the RedBooks Docker environment meets them.
06. **document shorthand keys** from fs requirements-change, which contradict the alias rule in `documentation-style`.

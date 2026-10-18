# RedBooks - Release 0.2.0

## Contents

- [About](#about)
- [References](#references)
- [Release notes](#release-notes)
- [Planned scope](#planned-scope)
- [Milestones](#milestones)

## About

RedBooks is a personal finance app for reporting financial statements, tracking expenses, and reconciling statements, customised to financial institutions in Singapore. The priority is a web app with a backend API for automation workflows and integrations. RedBooks succeeds the HomeBudget-based local prototype and the **financial-statements 010** design attempt.

## References

- **release roadmap**: [../../release-roadmap.md](../../release-roadmap.md)
- **requirements**: [../../requirements.md](../../requirements.md)
- **release milestones**: [020-release-milestones.md](020-release-milestones.md)
- **financial-statements 010**: [https://github.com/yayfalafels/financial-statements/](https://github.com/yayfalafels/financial-statements/)
- **homebudget wrapper**: [https://github.com/yayfalafels/homebudget](https://github.com/yayfalafels/homebudget)

## Release notes

Release `0.2.0` is the POC Bookkeeping release. It proves the RedBooks ledger, category model and financial statements against the user's full HomeBudget history. The app runs locally in Docker, with a Python FastAPI backend, a PostgreSQL database and a React web app laid out for a phone screen. HomeBudget stays the daily capture tool through `0.2.0`. Release `0.3.0`, the MVP web app, makes RedBooks available on the phone at any time and is the first release for daily use.

### Ledger and transactions

Every account keeps its entries in a single general ledger. Expenses, income, transfers and splits each have their own model on top of that ledger. A transfer references two ledger entries, one on the account the money leaves and one on the account it arrives in, following the HomeBudget model. A split records one event that moves money through several accounts and several categories at once, such as a dinner bill paid on a card with a friend's share received in cash, or a salary that lands in a bank account and several retirement fund accounts. The user enters the split's account entries and its category lines on one form, and the split saves when the two sides balance, so each account entry still matches its statement line. Any transaction can carry tags, optional labels such as a provider or a contact name. A pooled account, such as one account for miscellaneous bills or one for money friends owe, tracks each provider or person by tag, and shows its balance by tag beside its total. The user records all transactions manually.

### Categories

One consolidated category model classifies every transaction and feeds both financial statements directly. The model has two levels, categories and their subcategories, and every expense and income belongs to one subcategory. The model is built from a review of the HomeBudget categories, accounts and historical transactions, and that same review supplies the seed data.

### Multiple currencies

The user manages their own list of currencies, as in HomeBudget, adding each one from the catalog of currencies the rate API supports and removing the ones no longer needed. Each account holds a single currency from that list. The user sets the reporting currency from the same list. The seed data reports in SGD and includes USD accounts. RedBooks fetches real exchange rates from the rate API that the **homebudget wrapper** uses and stores them for reuse. Amounts and rates use a dedicated money type with exact decimal arithmetic.

Exchange rate movements appear as a separate forex gain or loss line on the period financial statements. RedBooks calculates this line when it builds a statement, and the account ledgers hold only the recorded transactions.

### Financial statements

RedBooks reports an income statement and a balance sheet in the reporting currency, each in a year view and a month view. The year view shows the twelve months of a year side by side, and clicking a month opens its month view. The month view drills down from each line to its transactions. The income statement shows each category with its subcategories beneath it. Both statements and the transaction lists export to CSV.

Each closed month is reported from a stored snapshot. On the 1st of every month, RedBooks generates the snapshot of the month before, and the current month is reported month to date on request. A past month can be re-run, which stores a new version and keeps the old ones, and every report shows the newest version. An edit to a month after its snapshot marks the snapshot stale, and the user sees the lines that drifted and the changes behind them before re-running it. Changing the reporting currency asks for confirmation and which past years to regenerate, and statements in the old currency stay in the history.

### Users and login

Users sign in with OAuth. Each user owns their own accounts, categories and transactions. Each user sets their timezone, Asia/Singapore by default, which sets the dates of new transactions and the month boundaries of the statements.

### Mobile layout

Every page is designed for a phone screen. Testing runs on a real phone connected to the local host through a tunnel. A mobile device emulator on the laptop covers testing when a phone connection is unavailable.

### HomeBudget history

The HomeBudget account `02` snapshot, a dated copy of the account `02` HomeBudget database, is the seed, loaded as-is from day one, and the account `01` migration loads the older history after the release's features are validated. Together they cover accounts, categories mapped to the consolidated model, and all historical transactions and transfers. HomeBudget holds each account's reconciled balance point and both sides of every transfer between currencies. Automated validation checks the loaded balances and transfers against the figures HomeBudget itself holds in the snapshot. Files the app produces, such as CSV exports, are stored on the local host.

### Lessons applied

The release applies the lessons recorded in the **requirements** from **financial-statements 010**.

01. every release ships a working app a user can operate.
02. the UI is a first-class deliverable alongside the backend API.
03. one consolidated category model serves both transaction entry and financial reporting.
04. user-specific business rules stay configurable by the user.
05. RedBooks owns its data store and API, and HomeBudget serves as the source of historical data.

## Planned scope

Features in scope for `0.2.0`

| id | feature              | 0.2.0 delivery          |
| -- | -------------------- | ----------------------- |
| 01 | accounting store     | RedBooks API            |
| 02 | txn storage          | PostgreSQL database     |
| 03 | deployment           | docker local            |
| 04 | back end api         | Python FastAPI          |
| 05 | front end ui         | React.js, phone layout  |
| 06 | txn category model   | consolidated            |
| 07 | manually record txns | included                |
| 08 | account ledger       | included                |
| 09 | multi currency       | included                |
| 10 | income statement     | included                |
| 11 | balance sheet        | included                |
| 12 | users                | multiple users          |
| 13 | login                | OAuth                   |
| 16 | csv export           | included                |
| 17 | file storage         | local                   |
| 19 | split txn            | split model             |
| 22 | tags                 | included                |

Features in later releases:

| id | feature              | release |
| -- | -------------------- | ------- |
| 03 | cloud web app deploy | 0.3.0   |
| 17 | S3 file storage      | 0.3.0   |
| 20 | pdf export           | 0.3.0   |
| 14 | statement loaders    | 0.4.0   |
| 15 | stm txn reconcile    | 0.4.0   |
| 18 | reconcile algorithm  | 0.4.0   |
| 21 | forecast             | tbd     |

## Milestones

The milestones run in the following phases:

01. **design** define the release
02. **setup** prepare the foundation
03. **implement** build the features
04. **release** deliver and release

Each phase produces what the next one depends on, so the release defines what it is building before it builds, prepares the environment before writing features, and builds features before publishing them. Current status for each milestone is tracked in the **release milestones**.

### Design: Define the release

The requirements milestone states the user outcomes and scope. Agent skills customization follows straight after, so the Claude Code agents and skills match the RedBooks stack and conventions before they help write the test and design documents. The test strategy and its case catalogue follow from the requirements, so every requirement has a defined way to prove it works before the design commits to a solution, and each feature reconciles its own cases with the design before it is built. The design comes last in this phase. It covers workflows, phone-layout pages, architecture, the ledger and data model, multiple currencies, API endpoints and the local environment. The design starts from a review of the HomeBudget categories, accounts and historical transactions, which shapes the consolidated category model.

### Setup: Prepare the foundation

The foundation milestones set up everything feature work relies on. The local dev and test env gives a repeatable Docker setup for the database, API and web app, with a tunnel to a phone and a mobile emulator for UI testing. The schema and account 02 seed milestone builds the schema and loads the user's real accounts and transactions as-is, in SGD and USD. The validation utilities that follow are the scripts that exercise a change end to end and check it against that data. Building these first means every feature after them is validated the same way from the start.

### Implement: Build the features

The feature milestones deliver the user-facing capability in dependency order. OAuth login comes first because every other feature belongs to a signed-in user. An audit skills checkpoint follows it, so the remaining features start from the rules the release has confirmed so far. The currency model follows, covering the money type, the supported currencies, the reporting currency setting and exchange rate fetching and storage, since every amount in the ledger depends on it. Txn and accounts builds on it, covering the general ledger, expenses, income, transfers, transfers between currencies and the consolidated category model. Financial statements builds the income statement and balance sheet from that ledger data, with the forex gain or loss line and CSV export. The homebudget account 01 migrate milestone comes last in this phase, and migrates the account `01` history into the finished data model and working ledger.

### Release: Deliver and release

The delivery milestones take the working app to a published release. Audit skills promote learning reviews what the agents learned during the release and folds the lessons into the shared skills, so the next release starts with better guidance. Mkdocs documentation writes the developer and user guides and sets up the CI/CD workflow that publishes the documentation site. Publish and release tags `0.2.0` and finalizes this page with the as-built scope.  The documentation site, developer guide and user guide are delivered by the mkdocs documentation milestone and are linked here at release.

I reviewed the current personal-finances requirements plus the two repos. The central lesson is stronger than “use a simpler stack”: **the new app should be built around a very small canonical financial ledger and a sequence of immediately useful vertical releases.** HomeBudget, Google Sheets, statement formats, broker exports, PDFs, and future bank APIs should all be adapters around that core—not architectural foundations.

The current project already states the right product-level goals: accurate/up-to-date actuals, minimal workflow friction, and drill-down reporting. :chatgpt-content-reference{index="0"} And its five workflows are a much better starting point than the old system architecture: capture/classify transactions, reporting, recurring/forecast transactions, statement ingestion, and reconciliation. :chatgpt-content-reference{index="1"}

## What the two projects teach us

**`financial-statements` had the right problem but started from the wrong boundary.** Its 0.1.0 explicitly retained Google Sheets as the primary UI, HomeBudget as the real-time accounting system, manual statement downloads, Sheets/forms for forecasting, and then inserted SQLite, CLI, backend services, mappings and synchronization between them. In other words, the application was being designed *around the existing workflow*. That explains the project's own retrospective: design-heavy, backend-heavy, excessive bespoke business logic, two classification hierarchies and tech-stack lock-in. :chatgpt-content-reference{index="2"}

That architecture also creates an awkward ownership question: **where is financial truth?** HomeBudget owns transactions, Sheets owns parts of configuration/reporting, SQLite owns workflow state, bank statements are another truth source, and mapping logic reconciles these representations. A huge fraction of engineering consequently becomes integration and synchronization rather than personal-finance functionality.

**EasyMCF corrected exactly this class of mistake.** Its roadmap explicitly records the previous `mcfpipe` failure mode: major upfront investment in cloud infrastructure, CI/CD, serverless/NoSQL architecture and networking without a workable MVP. EasyMCF deliberately went back to a local relational DB and straightforward application, shipped the end-to-end product, and deferred performance dashboards, scoring improvements and scraper repair.

There is one EasyMCF lesson I **wouldn't** copy literally: even its successful 010 spent milestones 1–9 on requirements → test strategy → test cases → model → architecture → design → dev environment → seed → validation before feature implementation began. That worked, but for this project I would compress those into a thin architectural foundation and get the first financial vertical slice working earlier.

So:

> **Financial-statements overfit the architecture to the legacy workflow. EasyMCF succeeded by simplifying infrastructure and protecting the MVP. Personal Finances should go one step further: simplify both the infrastructure and the product model.**

---

# 1. Requirements: start over from user outcomes

I would **not** port the 25-topic financial-statements requirements tree into the new app.

Start with five product capabilities:

| Capability | User outcome |
|---|---|
| **Ledger** | I can see and edit what actually happened to my money |
| **Import** | I can bring transactions/balances in without retyping them |
| **Reconcile** | I know the app agrees with authoritative statements |
| **Report** | I know what I own, owe, earn and spend |
| **Plan** | I know what is likely to happen next |

Then define a handful of hard product invariants.

**Financial truth:** imported source data is immutable/provenanced; normalized transactions can be corrected/classified; reconciled balances must be explainable down to source records.

**One classification system:** one account hierarchy and one category hierarchy. No “HomeBudget category → reporting category” equivalent.

**Traceability:** every number on every report drills down:

`report → account/category → transactions → imported record → source statement`

**Idempotency:** importing the same statement twice cannot double-count anything.
**Reversibility:** automated classification and matching should be editable; don't bury user-specific financial assumptions in application code.
**Useful before complete:** the system does not need every Singapore financial institution supported before it provides value.

That last requirement is particularly important.

---

# 2. Canonical data model

This is where I would spend the architectural thinking.

The core should be surprisingly small:

```text
Institution
    └── Account
          ├── Transaction
          └── BalanceSnapshot

Category

Import
    └── SourceRecord
          └── Transaction(s)

Statement
    ├── opening balance
    ├── closing balance
    └── SourceRecords

Reconciliation
    └── matches / differences

RecurringTransaction
ForecastTransaction
```

A transaction should roughly represent:

```text
id
account_id
date
amount
currency
description

category_id
counterparty
notes

status
source_record_id
transfer_group_id

created_at
updated_at
```

The critical modeling choice is that **accounts and transactions are canonical**.

A DBS CSV row, credit-card PDF line, IBKR trade, CPF contribution or manually entered cash expense is merely a source that eventually produces canonical records.

And I would model transfers explicitly. A $1,000 movement DBS → IBKR is one economic transfer represented by two account-side transaction records joined by a transfer identity.

### Don't build full double-entry accounting yet

There is a temptation here to build a beautiful accounting engine.

I wouldn't.

Your primary need is personal cash/asset/liability reporting, not a general ledger for arbitrary businesses. Build account transactions + transfers + balances first. The model can evolve toward journal entries later if investment accounting or cost-basis requirements genuinely demand it.

That is another application of the EasyMCF lesson: **don't solve the sophisticated future problem before proving the daily workflow.**

---

# 3. Architecture

I would use a **modular monolith**.

```text
                    ┌────────────────────┐
                    │      Web/PWA       │
                    │ mobile + desktop   │
                    └─────────┬──────────┘
                              │
                         HTTP / JSON
                              │
                 ┌────────────▼────────────┐
                 │     Application API     │
                 │                         │
                 │ ledger                  │
                 │ imports                 │
                 │ reconciliation          │
                 │ reporting               │
                 │ planning                │
                 └───────┬─────────┬───────┘
                         │         │
                  ┌──────▼───┐  ┌──▼──────────┐
                  │PostgreSQL│  │ object store│
                  │canonical │  │ statements  │
                  │ finance  │  │ raw imports │
                  └──────────┘  └─────────────┘

External sources
      │
      ▼
┌─────────────────────────────┐
│ Import adapters             │
│ CSV / XLSX / PDF / APIs     │
│ DBS / UOB / IBKR / CPF ...  │
└─────────────────────────────┘
```

No microservices.
No Kafka.
No data warehouse.
No separate reporting database.
No event-sourcing architecture.
No AWS architecture exercise.
No generic workflow engine.

At this scale, PostgreSQL is perfectly capable of being both the transactional store and reporting engine.

---

# 4. Tech stack

Given a clean slate, I'd choose:

| id | layer           | choice                   | why                                          |
| -- | ----------------|--------------------------|----------------------------------------------|
| 01 | Frontend        | **React + TypeScript**   | strong ecosystem, responsive/PWA             |
| 02 | Framework       | **Next.js**              | UI + straightforward deployment              |
| 03 | Backend         | **Python + FastAPI**     | excellent financial/data ingestion ecosystem |
| 04 | ORM             | **SQLAlchemy + Alembic** | mature relational modeling/migrations        |
| 05 | Database        | **PostgreSQL**           | canonical financial datastore + analytics    |
| 06 | Data processing | **Pandas**               | import/statement transformations             |
| 07 | Validation      | **Pydantic**             | excellent boundary validation                |
| 08 | Charts          | **ECharts**              | strong financial/dashboard visualization     |
| 09 | Raw documents   | **S3 storage**           | immutable source files                       |
| 10 | Tests           | **pytest + Playwright**  | backend/accounting + real workflow tests     |
| 11 | Deployment      | **Docker containers**    | portability without designing around cloud   |

SQLite would still be fine for a throwaway local prototype. But unlike EasyMCF, I wouldn't make “local → cloud database migration” part of the product roadmap. PostgreSQL is easy enough from day one and eliminates an unnecessary future transition.

I also wouldn't choose the cloud vendor yet.

Containerize:

```text
web
api
postgres
```

Run exactly that locally.

Later deploy essentially the same thing to whatever platform makes sense.

---

# 5. Release roadmap

This is the biggest change I'd make from both earlier projects.

### 0.0.1 — **Ledger walking skeleton**

Target: **days, not months.**

Implement Account, Category and Transaction.

UI:

**Accounts → Transactions → Add/Edit Transaction**

Seed it with representative data.

The acceptance test isn't architectural:

> I can open the app, enter transactions, categorize them and see current account balances.

Nothing else.

---

### 0.0.2 — **First real statement import**

Pick **one real bank account**.

Upload CSV → preview → normalize → deduplicate → import.

Show:

`Raw record → normalized transaction`

Now the application is already doing real work.

---

### 0.0.3 — **Reconciliation**

Add statement metadata:

opening balance  
+ transactions  
= closing balance

Then:

> **Reconciled ✓**

or:

> **Difference: $42.17**

with drill-down explaining the discrepancy.

This is probably the first release where the new application begins replacing meaningful parts of the existing monthly-close process.

---

### 0.1.0 — **Financial reporting MVP**

Now add the first genuinely useful dashboard:

**Net worth**

Assets − liabilities, current and historical.

**Cash flow**

Income − expenditure by month.

**Spending**

Category → merchant → transactions.

Every aggregate is clickable down to its records.

At this point you've satisfied a large portion of the project's central requirement—financial reporting—without Google Sheets or HomeBudget being involved. The original requirements explicitly identify reporting, expense tracking and statement reconciliation as the product's three headline functions. :chatgpt-content-reference{index="3"}

---

### 0.2.0 — **Daily money app**

This is when I would attack HomeBudget's role.

Mobile/PWA transaction entry.

Fast UX:

`$12.50 → Food → Toast Box`

Recent categories and merchants suggested automatically.

Transfer entry.

Recurring transactions.

Search.

Now ask the decisive question:

> **Can I stop entering new transactions into HomeBudget?**

If yes, HomeBudget becomes migration history rather than an integration dependency.

---

### 0.3.0 — **Multi-source finance**

Add adapters incrementally:

DBS  
credit cards  
IBKR  
CPF  
cash/manual accounts  
other banks

Each implements essentially:

```text
detect()
parse()
normalize()
validate()
```

against the same canonical model.

Institution-specific weirdness belongs inside adapters, **not the ledger**.

---

### 0.4.0 — **Planning**

Only after actuals work:

recurring bills  
expected income  
planned transactions  
cash-flow forecast  
account-balance forecast

Keep:

**Actual**

and

**Forecast**

conceptually distinct.

That avoids contaminating financial truth with predictions.

---

### 0.5.0 — **Automation**

Now automate the tedious pieces proven valuable:

classification rules  
merchant normalization  
transfer matching  
duplicate detection  
recurring transaction recognition  
statement ingestion  
reconciliation suggestions

This is where sophisticated heuristics—and eventually AI—earn their place.

Not release 001.

---

### 1.0 — **Trusted personal finance system**

The release criterion isn't feature count.

It is:

> **I no longer need HomeBudget or financial-reporting Google Sheets for normal financial management.**

Imports are repeatable. Reconciliation is trustworthy. Reports are complete. Backups/export work. The historical data has been migrated and validated.

---

# One important sequencing change

The old financial-statements project describes the current workflow as HomeBudget plus Sheets plus Python automation because HomeBudget lacks an API. :chatgpt-content-reference{index="4"}

I would **not begin this project by migrating that workflow**.

I'd run the new app beside it:

```text
existing system
     │
     │ validation reference
     ▼
HomeBudget + Sheets

NEW
statement
   ↓
import
   ↓
ledger
   ↓
reconcile
   ↓
reports
```

For several months, compare:

`new net worth == old net worth`

`new account balances == statements`

`new spending totals ~= existing reports`

Once confidence is established, retire components of the old workflow individually.

That turns the legacy system from an architectural constraint into a **test oracle**.

## The governing rule

I'd put this at the top of `requirements.md`:

> **Every release must leave behind a usable personal-finance application. Architecture exists to support the next user workflow, not the other way around.**

That is the clearest combined lesson from `financial-statements` and EasyMCF. The former explicitly says it stalled at requirements/design without producing a working implementation; the latter demonstrates that aggressively deferring infrastructure and secondary features can get an actual end-to-end product shipped. :chatgpt-content-reference{index="5"}

The next artifact I would produce is **not** a giant requirements document. It would be a ~3–5 page `product-requirements.md` defining the invariants, canonical concepts, 0.0.1–0.1.0 acceptance criteria, and explicit non-goals. Then we could design the initial schema directly from those requirements.
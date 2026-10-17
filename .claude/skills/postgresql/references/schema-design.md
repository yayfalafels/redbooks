# Schema design

How the schema carries invariants, vocabularies, history and state.

## Contents

- [Lessons](#lessons)

## Lessons

### every vocabulary value has a seeded row and a writing code path

Each closed vocabulary value, such as an account type or a transaction kind, appears in the seed, a test checks it, and some code path writes it. Adding a value means searching every lookup keyed on the vocabulary.

**why**: two event types had no generator site, a status had no code path that reached it, and the generator's own lookup table missed a new value.

Example:

```sql
CREATE TABLE account_type (code text PRIMARY KEY);
INSERT INTO account_type VALUES ('asset'), ('liability'), ('equity'), ('income'), ('expense');
```

### transcribe constraints and expected values from the requirements

Every `CHECK`, `NOT NULL` and foreign key comes from the requirements or design text, and the seed oracle's expected sets come from the same tables, never from the generator's constants.

**why**: a generator bug and a check that reads the generator's output share a blind spot. Transcribing both from the requirements gives two independent routes.

Example: the requirement "an entry amount is never zero" becomes `CHECK (amount <> 0)`, and the oracle's list of account types is copied from the data model doc.

### retire records that history references

A record with historical references gets `is_active boolean NOT NULL DEFAULT true`. Pickers filter on it, and history joins ignore it. The foreign keys from history use `ON DELETE RESTRICT`.

**why**: a foreign key guard refused to delete a label that only past records used, and the user chose retire over block or cascade.

Example:

```sql
UPDATE category SET is_active = false WHERE id = 12 AND owner_id = :user;
```

### keep one authority per state

Each state has one authority. A derived value, such as a balance, is computed from its authority, and a stored copy is a cache rebuilt from it. Where two authorities must exist, every read reconciles them by one rule.

**why**: the UI trusted a status column while the action also needed a file, and the two disagreed until a reconcile ran on startup and on every read.

Example: an account balance is the reconciled balance point plus the sum of its entries. A `balance_cache` column, if added, is rebuilt by the same query.

### enforce single-active invariants with partial unique indexes

An "at most one active" rule is a partial unique index filtered to the active state, so the database enforces it atomically.

**why**: a check-then-insert guard for one running job allowed two under concurrency.

Example:

```sql
CREATE UNIQUE INDEX one_running_import ON import_job (owner_id) WHERE status = 'running';
CREATE UNIQUE INDEX one_open_reconciliation ON reconciliation (account_id, period) WHERE closed_at IS NULL;
```

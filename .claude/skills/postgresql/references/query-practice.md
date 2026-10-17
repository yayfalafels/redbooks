# Query practice

How to write queries that callers and tests can rely on.

## Rules

01. filter every user-owned query by the owner.
02. bind every value as a parameter, never by string formatting.
03. compute aggregates in SQL with `NUMERIC`, never by summing floats in the app.

## Lessons

### order every result whose order matters

Any query whose order a caller or a test relies on has an `ORDER BY` on unique columns, with a tiebreaker.

**why**: a query without `ORDER BY` returned rows in index order, which changed when the data did.

Example:

```sql
SELECT id, posted_on, amount FROM entry
WHERE account_id = :account AND owner_id = :user
ORDER BY posted_on, id;
```

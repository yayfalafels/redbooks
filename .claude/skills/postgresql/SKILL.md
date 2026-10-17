---
name: postgresql
description: PostgreSQL schema and query practice, covering rebuild-and-reload during early development, versioned forward migrations, constraints transcribed from requirements, seeded vocabularies, retire flags, one authority per state, partial unique indexes, exact NUMERIC money and ordered queries. Use when designing or changing a schema, writing a migration or seed load, or writing a query whose results a caller or test relies on.
---

# PostgreSQL

Practice for a PostgreSQL schema that holds money and history, and changes often early in a project.

## Rules

01. **rebuild early, migrate later.** While the schema is in early development and its seed reloads from files, a schema change rebuilds the database and reloads the seed. Versioned forward migrations start before any irreplaceable data history is loaded. Either way, the schema, its version marker, the seed and the data model doc change together.
02. **invariants live in constraints.** Transcribe every constraint from the requirements. Every closed vocabulary value has a seeded row and a code path that writes it.
03. **retire, keep one authority, index the active.** A record that history references is retired. Each state has one authority. "At most one active" rules are partial unique indexes.
04. **exact money, explicit order.** Money columns are `NUMERIC`. Every query whose order matters has an `ORDER BY` on unique columns.

## References

| id | file                           | read it when                                      |
| -- | ------------------------------ | ------------------------------------------------- |
| 01 | `references/migrations.md`     | changing the schema, its version or the seed load |
| 02 | `references/schema-design.md`  | adding a table, constraint, vocabulary or status  |
| 03 | `references/query-practice.md` | writing a query a caller or test relies on        |
| 04 | `references/money-types.md`    | adding an amount, rate or currency column         |
| 05 | `references/open-lessons.md`   | a task touches one of the listed areas            |

## Related skills

- [accounting](../accounting/SKILL.md) for the ledger rules the schema enforces.
- [python](../python/SKILL.md) for `Decimal` handling in the app.

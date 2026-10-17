# Migrations

How the schema changes, first by rebuild and later by versioned forward migrations.

## Phases

| id | phase           | a schema change                                                    |
| -- | --------------- | ------------------------------------------------------------------ |
| 01 | rebuild         | drops and recreates the database, then reloads the seed from files |
| 02 | forward migrate | adds an Alembic revision, and the app checks the head at startup   |

The move to phase 02 happens before any data that cannot be reloaded from files is loaded.

**open lesson LT.06** whether Alembic revisions with a startup head check catch version drift automatically. See `open-lessons.md`.

## Lessons

### change the schema, its version, the seed and the design doc together

A schema change, its version marker, the regenerated or reloaded seed, and the data model doc's version table land in one change. Nothing edits the schema while a test suite runs. During the rebuild phase, one command rebuilds the database and reloads the seed.

**why**: a schema moved through eleven versions in one release. The startup version constant was not bumped, a generator emitted rows for a table the schema lacked, seed files written for the old schema failed to load, and a schema edit during a background suite gave a spawned app a different version.

Example:

```bash
# rebuild phase
python -m scripts.rebuild_db && python -m scripts.load_seed
# forward migrate phase
alembic revision -m "add reconciliation table" && alembic upgrade head
```

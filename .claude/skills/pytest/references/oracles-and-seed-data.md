# Oracles and seed data

How expected values, seed rows, fixtures and stubs are built so a check is independent of the code it checks.

## Contents

- [Lessons](#lessons)

## Lessons

### build seed data as a coherent history and derive its aggregates

Seed data describes a history that could have happened. Counts, balances and dates derived from other rows are computed by the loader or generator, never typed. State a test needs, such as a live session, is staged by that test.

**why**: seeded records covered every outcome code but formed an impossible history: events before their run started, repeats in one run, and typed counts that disagreed with the rows. Oracles, API checks and page checks all read those rows.

Example: the loader computes each account's closing balance from its reconciled balance point and the seeded entries, and asserts it against the balance file.

### pin every generator input and review the diff of generated files

Generator inputs, such as the random seed, the anchor date and loop bounds, are pinned or derived. Generating twice gives identical files, and every changed generated file is reviewed before commit.

**why**: a missing date anchor defaulted to today, so a regeneration rewrote eight unrelated seed files while the generator and the full suite passed. Only `git status` caught it.

Example:

```bash
python -m scripts.gen_seed --anchor 2026-03-31 --random-seed 7 --out /tmp/a
python -m scripts.gen_seed --anchor 2026-03-31 --random-seed 7 --out /tmp/b
diff -r /tmp/a /tmp/b && git status --short tests/seed/
```

### every vocabulary value has a seeded row and a writing code path

Each closed vocabulary value appears in the seed, and a test checks both that it is seeded and that some code path writes it.

**why**: two event types had no generator site, and a status had no code path that reached it.

Example:

```python
@pytest.mark.parametrize("code", VOCAB_FROM_DESIGN["account_type"])
def test_account_type_seeded(db, code):
    assert db.scalar(select(func.count()).where(Account.type == code)) > 0
```

### transcribe constraints and expected values from the requirements

Oracle expectations come from the requirements or design text, never from the code under test or the generator's constants.

**why**: a generator bug and a check that reads the generator's output share a blind spot.

Example: `VOCAB_FROM_DESIGN` is copied from the data model doc's vocabulary table, and the statement oracle's totals come from a reference report produced by another application.

### read library defaults before writing boundary cases

Read the tolerances a library applies, such as clock leeway or float formatting, and put boundary cases beyond them.

**why**: a token expired one second earlier was accepted, because the library allows 120 seconds of clock leeway.

Example: the expired-token case uses one hour past expiry.

### check the oracle and the harness before the code

When a check fails, first confirm the check's input, its expected value and its harness against the design. Derive expected values by reading the data, never by hand count.

**why**: in one milestone, six of twelve issues were defects in the verification commands or oracles: a stale query shape, a miscounted total, a pre-created temp file, a bare interpreter name, a missing schema step and wrong paths.

Example: a total that disagrees by one row is checked first with a direct `SELECT count(*)` against the design's filter, before the service is read.

### never hard-code seed counts or ids

Tests look up seed rows by a stable key, assert deltas against a before-snapshot, and capture created ids from responses.

**why**: four tests broke when the seed gained rows, and one asserted a literal count where a seeded row already existed.

Example:

```python
before = count_entries(db, account="Checking")
r = client.post("/api/entries", json=payload)
new_id = r.json()["id"]
assert count_entries(db, account="Checking") == before + 1
```

### capture fixtures and stubs from real artifacts

Fixtures and stubs are captured from real responses or files, then reduced. A guessed fixture proves only the guess.

**why**: hand-written fixtures used guessed attribute names, so every fixture test passed while the live run failed. One isolated call against the real source found the real names.

Example: `tests/stubs/rates/2026-03-28.json` is a recorded rate API response for a Saturday, trimmed to two currencies. A reader fixture is three real source database rows with the personal fields kept in the uncommitted fixture folder.

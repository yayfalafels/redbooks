# Run and triage

How test sets are organised and budgeted, and how a failure is triaged.

## Contents

- [Layout](#layout)
- [Live order](#live-order)
- [Lessons](#lessons)

## Layout

```
tests/
├── conftest.py                 # settings, db, clock, client, stub IdP
├── features/
│   ├── f01_sign_in/
│   │   ├── unit/               # siloed: no network, no other feature
│   │   └── integration/
│   └── f02_entries/
└── regression/                 # end-to-end paths that span features
```

```toml
# pyproject.toml
[tool.pytest.ini_options]
timeout = 5                     # local default, in seconds
markers = ["live: calls a real outside service", "internet: an internet API call, 30 second budget"]
```

## Live order

01. run every set against the stubs.
02. run the `live` tests for everything except irreversible writes.
03. leave irreversible writes, and the full live sign-in with its writes, to the user.

## Lessons

### check the oracle and the harness before the code

When a check fails, read the check first: its input, its expected value and its harness, against the design. Only then read the code.

**why**: about half of one release's failures were wrong expectations or broken harnesses while the code was right.

Example: a failing balance test is triaged by recomputing the expected balance with a direct SQL query from the design's rule, before opening the service.

### take baselines from a clean worktree

Record the baseline before changing code, from a worktree the edits cannot reach.

**why**: a seed regeneration in the middle of a run tainted a baseline, and the clean baseline had to run again from a detached worktree.

Example:

```bash
git worktree add --detach ../baseline HEAD
(cd ../baseline && python -m pytest -q > ../baseline.txt)
```

### bisect order-dependent failures

For a failure seen only in the full run, bisect by file set, then by collecting versus executing.

**why**: a test passed alone, passed with the files before it, and passed with full collection limited by `-k`. That showed the trigger was executing a file elsewhere in the run.

Example:

```bash
python -m pytest tests/features/f01_sign_in tests/features/f02_entries/test_list.py
python -m pytest tests -k test_list --co -q    # collect only
```

### give every test an expected latency and fail when it is exceeded

Each test carries a latency budget and raises a timeout when it exceeds it. A local test with no network call allows a few seconds. An internet API call normally takes about a second and allows 30 seconds. Load variance is never an accepted close for a timeout.

**why**: two full-run-only timeouts were closed as load variance without a confirmed cause. A later one with the same shape, reproduced by injected latency, was a real missing wait.

Example:

```python
@pytest.mark.live
@pytest.mark.internet
@pytest.mark.timeout(30)
def test_fetch_weekend_rate(settings, rates_client):
    assert rates_client.rate("USD", "SGD", "2026-03-28") > 0
```

### scope test sets to features and keep regression growth sublinear

Each feature owns its test set: siloed unit tests first, then integration tests. Each later feature adds regression tests, and the end-to-end regression run grows sublinearly, about 1x at the first feature, 1.5x by the second or third, and 2x by the tenth.

**why**: one monolithic suite grew from 3 tests to 493 and from 142 to 534 seconds in one release, and a global per-test timeout clashed with a longer poll budget.

Example: `python -m pytest tests/features/f02_entries` runs one feature's set, and `python -m pytest tests/regression --durations=10` reports the regression run's time against its budget.

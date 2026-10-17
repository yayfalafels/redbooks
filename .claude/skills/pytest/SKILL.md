---
name: pytest
description: pytest practice for services with a database, a JSON API and outside integrations, covering settings read from .env, feature-scoped test sets, per-test latency budgets, the stub-first live order, oracles and seed data, ownership matrices, fixtures, clocks, baselines and failure triage. Use when writing, running, reviewing or triaging any pytest test, fixture, oracle or seed data check.
---

# pytest

Practice for test suites that check a service, its database and its outside integrations, and that stay fast and trustworthy as features are added.

## Rules

01. **settings come from `.env`.** Tests build the app's settings object the same way the app does, and every run reports its effective mode.
02. **feature-scoped test sets.** Each feature has its own set: siloed unit tests first, then integration tests. The end-to-end regression run grows sublinearly, about 1x, 1.5x and 2x of the first feature's run at the first, second to third, and tenth feature.
03. **every test has a latency budget.** A test raises a timeout when it exceeds its budget: a few seconds for local work, 30 seconds for an internet API call.
04. **stubs first, then live.** Tests run against the stubs first, then live for everything except irreversible writes, which wait for the user.
05. **suspect the check first.** When a check fails, confirm its input, its expected value and its harness against the design before the code. Expected values come from oracles and data reads, and tests find seed rows by stable keys.
06. **fixtures and clocks.** Shared fixtures register once. Workers run as production runs them. The clock is pinned before any time-bound state is created.
07. **clean baselines, bisected failures.** Baselines come from a clean worktree, and an order-dependent failure is bisected by file set.

## References

| id | file                                    | read it when                                          |
| -- | --------------------------------------- | ----------------------------------------------------- |
| 01 | `references/fixtures-and-isolation.md`  | writing a fixture, a settings override or a clock pin |
| 02 | `references/oracles-and-seed-data.md`   | writing an expected value, a seed row or a stub       |
| 03 | `references/api-and-ownership-tests.md` | testing a route, ownership, or sign-in                |
| 04 | `references/run-and-triage.md`          | organising sets, setting budgets, or a test fails     |
| 05 | `references/open-lessons.md`            | a task touches one of the listed areas                |

## Related skills

- [python](../python/SKILL.md) for the settings object and the clock.
- [fastapi](../fastapi/SKILL.md) for the error contract and the stub identity provider.
- [playwright](../playwright/SKILL.md) for browser tests.
- [accounting](../accounting/SKILL.md) for identity and sign checks in ledger oracles.

---
name: python
description: Python service and script practice, covering one settings object read from .env, run modes and second opt-ins for irreversible writes, path resolution, specific exception handling, background job status, Decimal money, outbound HTTP clients, and project layout with pinned dependencies. Use when writing or reviewing any Python app code, script, job or client.
---

# Python

Practice for Python apps, scripts and jobs that share one configuration, handle money, and call outside services.

## Rules

01. **one settings object reads `.env`.** The app, every script and the tests build it the same way. Nothing writes configuration into the process environment at import, and every run reports its effective mode at start.
02. **paths resolve from the project root.** A relative path in configuration resolves against one known root, never the working directory.
03. **irreversible writes need a second opt-in.** A write to a real external system or to the user's real data needs a second setting, checked at preflight and again at the point of use. Live reads need only the mode setting.
04. **catch the specific exception.** Catch each identified cause by its own type, keep causes isolated, and give the user an actionable hint. A catch-all only keeps a batch running, and it records the original exception.
05. **jobs end in a terminal status.** A background job always reaches a terminal status, records the original exception on failure, and commits its progress as it goes.
06. **money is `Decimal`.** Build amounts and rates from strings, and quantise with an explicit rounding mode.
07. **HTTP clients are explicit.** An outbound client sets explicit timeouts and maps transport errors and status errors separately.
08. **one project layout.** Run Python through the project's named environments or containers, pin dependencies, type-hint module boundaries, and run scripts as package modules.

## References

| id | file                               | read it when                                             |
| -- | ---------------------------------- | -------------------------------------------------------- |
| 01 | `references/config-and-time.md`    | adding a setting, a run mode, a path or a clock          |
| 02 | `references/errors-and-logging.md` | handling an exception, or writing a job or batch         |
| 03 | `references/decimal-money.md`      | computing, rounding or splitting an amount               |
| 04 | `references/http-clients.md`       | calling an outside API                                   |
| 05 | `references/project-layout.md`     | adding a package, dependency, entry point or environment |
| 06 | `references/open-lessons.md`       | a task touches one of the listed areas                   |

## Related skills

- [fastapi](../fastapi/SKILL.md) for supplying settings to routes.
- [pytest](../pytest/SKILL.md) for building settings in tests.
- [accounting](../accounting/SKILL.md) for the rules the money code enforces.

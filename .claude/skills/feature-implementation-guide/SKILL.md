---
name: feature-implementation-guide
description: The spec-first feature tracker pattern, which runs scope, design, test strategy and cases, edit locations, implement and validate in one markdown file, plus the implementation and validation conventions that go with it, such as git-tracked rerunnable scripts, .env parameterization, log file naming, verify-before-done and the issue diagnostics workflow. Use when drafting a feature or assessment tracker, or before implementing or validating a feature.
---

# Feature implementation guide

One markdown tracker per feature is the spec, the design, the test plan and the progress record at once. Trackers live in `docs/releases/<release>/features/<release>.<NN>-<short-name>.md`. The skill splits into four subskills, so a task loads only the one its current stage needs.

## Rules

01. **fill the tracker in stage order.** Scope, design, test cases, edit locations, implement, validate. A later section stays a one-line stub until the stage before it is settled.
02. **one id scheme.** Every table row takes the form `<feature>.<category>.<seq>`, such as `12.TC.04`, so a check traces back to its design item and edit location.
03. **verify before reporting done.** Exercise every runtime surface a change touches, and call each layer directly before building on it. A passing type check or unit suite alone proves nothing about a route or a page.
04. **rerunnable, tracked scripts.** Build, run and validation steps live in git-tracked scripts parameterized from `.env`. Throwaway scripts and environments belong only in the diagnostic folder.
05. **log every first-out failure as an issue.** Each issue gets a row and a diagnostic section, and its cause stays a hypothesis until a fix is applied and re-validated.
06. **record lesson observations.** When a task touches an open lesson, record it in the Validate section as `lesson observation LT.NN` with the evidence.

## References

| id | file                                               | read it when                                         |
| -- | -------------------------------------------------- | ---------------------------------------------------- |
| 01 | `tracker-pattern/REFERENCE.md`                     | starting a tracker, or choosing the next section     |
| 02 | `tracker-pattern/templates/feature-tracker.md`     | copying a new tracker into place                     |
| 03 | `implementation/REFERENCE.md`                      | writing scripts, parameters, errors and logs         |
| 04 | `validation/REFERENCE.md`                          | validating a feature, or a first-out failure appears |
| 05 | `validation/templates/issue-diagnostic-section.md` | adding one issue row and its diagnostic section      |
| 06 | `open-lessons/REFERENCE.md`                        | a task touches one of the listed areas               |

## Related skills

- [documentation-style](../documentation-style/SKILL.md) for every prose section of a tracker.
- [markdown-tables](../markdown-tables/SKILL.md) for every table: tasks, test cases, edit locations, issues and diagnostic steps.

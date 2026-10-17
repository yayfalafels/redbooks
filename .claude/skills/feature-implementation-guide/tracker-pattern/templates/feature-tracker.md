<!--
Boilerplate feature tracker.
Copy to docs/releases/<release>/features/<release>.<F>-<short-name>.md, fill in the <angle-bracket> placeholders, then delete this comment.
<F> is the feature's two-digit id, such as 12.
Fill sections top to bottom only as far as the current stage. A later section stays a one-line stub until the stage before it is settled, per tracker-pattern/REFERENCE.md.
-->
# <feature name, title case> - Feature tracker

## Guideline

review and strictly follow these relevant skills when performing tasks for this feature implementation and working with this document

- documentation-style
- markdown-tables
- feature-implementation-guide

## <F> (pending) <feature name, lower case>

<one paragraph: what this feature builds and why>

## Contents

- [Guideline](#guideline)
- [Tasks](#tasks)
- [Scope](#scope)
- [References](#references)
- [Design](#design)
- [Test cases](#test-cases)
- [Edit locations](#edit-locations)
- [Implement](#implement)
- [Validate](#validate)

## Tasks

| id     | seq | status  | task           |
| ------ | --- | ------- | -------------- |
| <F>.01 | 01  | open    | scope          |
| <F>.02 | 02  | pending | design         |
| <F>.03 | 03  | pending | test cases     |
| <F>.04 | 04  | pending | edit locations |
| <F>.05 | 05  | pending | implement      |
| <F>.IS | 06  | pending | validate       |

## Scope

<plain-language statement of what is built>

In scope:

01. <item>

Out of scope:

01. <item>

**closure**

- **<F>.CK.01** <acceptance criterion, written before the design exists>

## References

- **<alias>**: [<file>](<relative/path>)

## Design

### <concern area>

<the chosen specification and its reason>

**implementation decision** - <where the ask was ambiguous, the choice, and its reason>

**deviation** - <where this departs from a higher-level doc or convention, and why>

## Test cases

_test strategy_

01. **self-report** - <what the code's own [PASS] and [FAIL] output proves>
02. **<independent layer>** - <what it checks against, reading nothing the code produced>

| id        | scope-item | layer | check         |
| --------- | ---------- | ----- | ------------- |
| <F>.TC.01 | <F>.CK.01  | ...   | <what passes> |

**tools** - reproduce independently:

```bash
<copy-pasteable command that reruns this check by hand>
```

## Edit locations

| id        | path   | change         |
| --------- | ------ | -------------- |
| <F>.EL.01 | <path> | <what changes> |

Not expected to change:

01. <file or contract>

## Implement

### <F>.05.01 <step name>

edit locations: `<F>.EL.01`

_expand when this step starts_

## Validate

<what was run, against what evidence, once implementation is done>

| id | log file                  | exit | evidence        |
| -- | ------------------------- | ---- | --------------- |
| 01 | `<ts>-<F>.<n>-<task>.log` | 0    | <what it shows> |

**secondary validation** - reproduce independently:

```bash
<copy-pasteable command that bypasses the feature's own scripts>
```

**Issues**

| id        | seq | status  | issue                   |
| --------- | --- | ------- | ----------------------- |
| <F>.IS.01 | 01  | pending | \<first out exception\> |

<!-- paste one validation/templates/issue-diagnostic-section.md block per issue row here -->

**lesson observations**

- <`lesson observation LT.NN`: what happened, with the evidence>

**user actions**

- <anything only a human had to do, such as a GUI-only tool, a third-party sign-in or an account only a person holds>

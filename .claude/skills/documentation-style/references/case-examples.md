# Case examples

One before and after pair per rule in `SKILL.md`, for calibrating a review. Each excerpt is neutral and written for this file.

## Contents

- [01 hard-wrapped line breaks](#01-hard-wrapped-line-breaks)
- [02 negation comparisons](#02-negation-comparisons)
- [03 parentheses](#03-parentheses)
- [04 full stops](#04-full-stops)
- [05 numbered lists](#05-numbered-lists)
- [06 lead with the point](#06-lead-with-the-point)
- [07 table of contents](#07-table-of-contents)
- [08 alias references](#08-alias-references)
- [09 chosen specification](#09-chosen-specification)
- [10 no revision language](#10-no-revision-language)

## 01 hard-wrapped line breaks

Before:

```
The order service validates the request, checks that the customer owns
the cart, and then reserves stock for every line before it writes the
order row.
```

After:

```
The order service validates the request, checks that the customer owns the cart, and then reserves stock for every line before it writes the order row.
```

## 02 negation comparisons

Before:

```
The field lists in the data model are conceptual, not DDL, so concrete column types are resolved here.
```

After:

```
The field lists in the data model are conceptual. Concrete column types are resolved here.
```

## 03 parentheses

Before:

```
The worker (started by the scheduler at midnight) retries each failed invoice (up to three times).
```

After:

```
The scheduler starts the worker at midnight. The worker retries each failed invoice up to three times.
```

## 04 full stops

Before:

```
An order belongs to one customer; a shipment can span orders from several customers - so its customer id may be null.
```

After:

```
An order belongs to one customer. A shipment can span orders from several customers, so its customer id may be null.
```

## 05 numbered lists

Before:

```
Two rules apply: (a) the loader writes dates relative to load time; (b) all code reads the time through one clock function, so a test can pin it.
```

After:

```
Two rules apply.

01. the loader writes dates relative to load time.
02. all code reads the time through one clock function, so a test can pin it.
```

## 06 lead with the point

Before: a tracker template orders its sections Tasks, Scope, Design, Implement, Validate, Guideline. The Guideline section names the skills that govern the document, and a reader scrolls past the whole work history to reach it.

After: Guideline sits directly under the title, ahead of Contents and Tasks.

```
# <feature name> - Feature tracker

## Guideline

review and strictly follow these relevant skills when performing tasks for this feature implementation and working with this document

- documentation-style
- markdown-tables
- feature-implementation-guide

## <F> (pending) <feature name>
```

## 07 table of contents

Before: a 150-line design doc opens with its first detailed section, and a reader scrolls the page to find one topic.

After: a `## Contents` list of every section heading, as links, follows the title and a one-paragraph intro. The summary is the first section listed under Contents.

```
# Ledger design

The ledger stores every money movement as signed entries that sum to net worth.

## Contents

- [Summary](#summary)
- [Entries](#entries)

## Summary
```

Wrong: a `## Summary` section placed between the title and `## Contents`, which pushes the contents list down the page.

## 08 alias references

Before:

```
Neither `design/architecture.md` nor `design/data-model.md` mandates database-level cascades.
```

After:

```
## References

- **architecture design**: [architecture.md](design/architecture.md)
- **data model design**: [data-model.md](design/data-model.md)

Neither the **architecture design** nor the **data model design** mandates database-level cascades.
```

## 09 chosen specification

Before:

```
We considered a generic CRUD layer and per-resource routers. A generic layer would be less code, but it cannot enforce invariants, so we did not choose it and went with routers instead.
```

After:

```
Each resource has its own router. Writes with invariants go through the service that enforces them.
```

## 10 no revision language

Before, in a design doc:

```
The transfer model was updated from paired expense and income rows to a single signed transfer entry, to account for the forex gain or loss found in the HomeBudget review. Previously, transfers between currencies were not supported.
```

After, in the design doc:

```
A transfer is one signed entry between two accounts. A transfer between currencies posts the forex gain or loss to its own income statement line.
```

After, in the feature tracker under the milestone that made the change:

```
The HomeBudget review found cross-currency transfers with a forex gain or loss. The transfer model moved from paired expense and income rows to one signed transfer entry.
```

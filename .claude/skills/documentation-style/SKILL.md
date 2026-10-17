---
name: documentation-style
description: Direct, concise prose rules for narrative markdown documentation, covering requirements, design docs, feature trackers, published pages, and skill and agent instructions. Use when writing new prose documentation, when reviewing or editing existing docs for style, or before publishing docs to a docs site.
---

# Documentation style

These nine rules govern narrative prose in `*.md` files. They apply to requirements, design docs, feature trackers, published pages, and skill and agent instruction files. They never apply to source code, config syntax, table cell structure beyond the **markdown-tables** skill, or literal command and log output inside a fenced block.

## Rules

01. **no hard-wrapped line breaks.** Write each paragraph as one unwrapped line in the raw source, and let the editor soft-wrap it for display. A one-sentence edit then gives a one-line diff.
02. **direct, concise language.** State the fact plainly. Avoid negation comparisons such as "this, not that".
03. **avoid parentheses.** The one exception is the first introduction of an acronym, such as Central Provident Fund (CPF). Rewrite other parenthetical fragments into the sentence, or split them into a new sentence.
04. **use full stops.** Limit semicolons and hyphens wherever the two joined expressions could be two sentences.
05. **numbered lists.** Use an enumerated list for anything longer than two or three items. Prefer numbered lists over bullets, and number with two digits, 01, 02, 03, never letters.
06. **lead with the point.** Put the gist in the one-paragraph intro under the title, and place summary, conclusions and commonly needed sections first after `## Contents`, so a reader gets the gist without reading to the bottom. Wrap-up, references and checklist sections belong at the top of the detailed sections or nowhere.
07. **table of contents.** Add a `## Contents` list once a doc passes about 50 lines. Above it sit only the `#` title and at most one short intro paragraph with no heading. A `## Summary`, `## Overview` or any other `##` section goes below `## Contents` and appears in its list. The one exception is the feature tracker template, whose `## Guideline` and feature status heading precede Contents.
08. **alias references.** Collect every file path, external reference and URL in one `## References` section, each with a bold alias, and refer to them by alias in the text. A moved file then changes one line.
09. **state the chosen specification.** Design text states what was chosen and why. It leaves out the alternatives that were rejected, and records a judgment call in an **implementation decision** callout.

## References

| id | file                           | read it when                                          |
| -- | ------------------------------ | ----------------------------------------------------- |
| 01 | `references/case-examples.md`  | calibrating a rule against a before and after example |
| 02 | `references/published-docs.md` | writing or reviewing pages for a published docs site  |

## Related skills

- [markdown-tables](../markdown-tables/SKILL.md) for every table in a doc.

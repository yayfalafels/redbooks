---
name: react
description: React single-page frontend practice, covering refresh after writes without losing in-progress input, string form values converted at the boundary, the sign-in redirect, mobile-first component-scoped styles, loading, empty and error states, and the user's standing interface preferences. Use when writing or reviewing any React page, component, form, API call or layout.
---

# React

Practice for a React single-page app that reads and writes a JSON API, is used mostly on a phone, and signs in through the backend.

## Rules

01. **refresh after every write.** Every view that shows the changed data refreshes after a write, and a refresh keeps the fields the user is editing.
02. **form values are strings.** Select and input values are strings. Convert ids and amounts once, at the form boundary on submit.
03. **remember the requested path.** A sign-in redirect stores the requested path before it navigates, and returns to it after sign-in.
04. **mobile first, component-scoped styles.** Lay out for a phone first. Each style rule targets one component. Test layouts at phone and desktop width with realistic text lengths.
05. **every data view has three states.** Loading, empty and error each render something the user can read and act on.
06. **follow the standing interface preferences.** Pages follow the preferences in `references/ui-review-lessons.md`.

## References

| id | file                                 | read it when                                         |
| -- | ------------------------------------ | ---------------------------------------------------- |
| 01 | `references/api-calls.md`            | calling the API, refreshing data or handling sign-in |
| 02 | `references/components-and-state.md` | building a form, a list or a component's state       |
| 03 | `references/mobile-layout.md`        | styling a page or a component                        |
| 04 | `references/ui-review-lessons.md`    | designing or reviewing a page                        |
| 05 | `references/open-lessons.md`         | a task touches one of the listed areas               |

## Related skills

- [fastapi](../fastapi/SKILL.md) for the API contract and JSON types.
- [playwright](../playwright/SKILL.md) for page tests.

# The feature tracker pattern

One markdown file per feature is the spec, the design doc, the test plan and the progress tracker. It is written mostly before code exists and filled in section by section as work happens, so its fill state is the feature's state.

## Contents

- [Sections in fill order](#sections-in-fill-order)
- [Id scheme](#id-scheme)
- [Who does what](#who-does-what)
- [Scale the skeleton](#scale-the-skeleton)
- [Lessons](#lessons)

## Sections in fill order

The template is `templates/feature-tracker.md`. Sections sit top to bottom in the file and are filled left to right in time. The order keeps code from starting before test cases exist and edit locations from being picked before the design is agreed.

| id | section        | question it answers                                                |
| -- | -------------- | ------------------------------------------------------------------ |
| 01 | Guideline      | which skills govern this document and its work?                    |
| 02 | Tasks          | what are the stages, and which are done?                           |
| 03 | Scope          | what is built, what is left out, and how is done measured?         |
| 04 | Design         | what are the key decisions, and why?                               |
| 05 | Test cases     | how is each claim checked, independently of the code that makes it |
| 06 | Edit locations | which files change?                                                |
| 07 | Implement      | the work, one step per group of edit locations                     |
| 08 | Validate       | what ran, what broke, how it was found, and what is still open     |

01. **Guideline** sits directly under the title and names the skills to follow.
02. **Tasks** is a table, `id | seq | status | task`, with status `pending`, `open` or `closed`. The heading `## <F> (open) <feature name>` gives the one-line status.
03. **Scope** states what is built in plain language, the out of scope items, and the closure criteria, written before the design exists.
04. **Design** has one subsection per concern. Each states the chosen specification and its reason. Two callouts mark what a reviewer should scan: an **implementation decision** states a judgment call where the ask was ambiguous, with the choice and its reason, and a **deviation** states where the design departs from a higher-level doc or convention, and why.
05. **Test cases** names independent verification layers, so no check grades its own output, then lists `id | scope-item | layer | check` with a **tools** block of commands that reproduce each layer by hand. A layer is independent when it reads nothing the code under test produced.
06. **Edit locations** is a table, `id | path | change`, written before any file is opened. It tags generated and hand-authored files, and lists what is not expected to change.
07. **Implement** has one step per group of edit locations, each opening with `edit locations: <ids>`. A step not yet started stays the stub `_expand when this step starts_`. A step only a human can do, such as a GUI-only tool or a third-party sign-in, is named as a user action.
08. **Validate** holds the run evidence, the Issues table with one diagnostic section per issue, the user actions, and any `lesson observation LT.NN` entries. See `../validation/REFERENCE.md`.

| id | layer             | checks against                                  |
| -- | ----------------- | ----------------------------------------------- |
| 01 | self-report       | the code's own `[PASS]` and `[FAIL]` output     |
| 02 | black box         | behavior from outside: an HTTP response, a page |
| 03 | direct inspection | the store queried directly, bypassing the app   |
| 04 | oracle            | an expected value derived by a separate route   |

## Id scheme

| code | meaning                                        |
| ---- | ---------------------------------------------- |
| CK   | scope closure criterion                        |
| TC   | test case                                      |
| CC   | closure check                                  |
| EL   | edit location                                  |
| IS   | issue, with `.<step>` for its diagnostic steps |

Add a category only when a feature needs it, such as `PR` for ordered prerequisites.

## Who does what

| id | stage          | the agent drafts or runs                  | the user checks                        |
| -- | -------------- | ----------------------------------------- | -------------------------------------- |
| 01 | Scope          | scope, out of scope and closure           | the boundary, the cheapest redirect    |
| 02 | Design         | decision and reason per concern           | the flagged callouts                   |
| 03 | Test cases     | independent layers and traceable cases    | that the layers are truly independent  |
| 04 | Edit locations | every file to be touched, tagged          | the blast radius                       |
| 05 | Implement      | the steps in order, filled in as they run | the user actions                       |
| 06 | Validate       | reruns, issues as hypotheses              | open issues, then closes the task rows |

## Scale the skeleton

A one-file fix can merge Design and Edit locations into one short section. Keep the section order and the id scheme even when sections are thin, so trackers written by different sessions still cross-reference cleanly.

## Lessons

### probe an external system before designing against it

When a design depends on how an outside system behaves, such as a third-party API's weekend handling or an export file's format, write a tracked, rerunnable probe script first. Each probe step saves its raw output and a findings file, and the findings become fixture cases.

**why**: a feature designed on guessed behavior passed every fixture test and failed its first live run, because the fixtures encoded the same guess.

Example: `.dev/features/04-design/scripts/01-probe-rates-api.py` requests a weekend date, a missing date and a 400-day range, and writes each response to `findings/`.

### reconcile test cases with scope and edit locations before implementing

Before the first implement step, read every test case against the scope, the data model and the edit locations. Trace every scope field to the column that stores it, and run every tracker command literally once.

**why**: cases were written before their fixture shape existed, a case expected behavior outside the milestone, an edit location assigned UI checks to a backend file, a required field had no column, and a tracker command used a syntax the tool rejects.

Example: scope item `12.CK.03` names an invoice due date. The reconcile pass finds no `due_date` column in edit location `12.EL.02` and adds it before any code is written.

### scope by extending what exists

Before scoping a new script, utility or module, search the repo for one that already does most of the job, and scope the feature as an extension of it.

**why**: a draft scoped a new validation utility where an existing script already covered most of the work.

Example: the scope reads "add a `--case` option to the existing API test script" instead of "write an API case runner".

### keep implementation guides to code snippets

Edit locations and implement steps hold short code snippets that show the shape of a change. Full source listings stay in the source files, and a nested feature gets its own tracker.

**why**: a tracker grew past 7,000 lines of source listings and a nested tracker. The snippets drifted from their prose and carried a defect into the code.

Example: an implement step shows the five-line signature and guard of a new service function, and points to the file for the body.

### grow a feature with a sub-feature first

A feature request found during validation becomes a sub-feature of the current feature, with its own task rows and id prefix. It becomes a new milestone and tracker only when its scope warrants one.

**why**: nine feature requests from a walkthrough were logged as issues with full specifications, which hid new scope inside the issue list.

Example: walkthrough requests for list sorting and batch archive become sub-feature `09.13`, with tasks `09.13.01` to `09.13.04`.

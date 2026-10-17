# Validation guide

The mechanics of a tracker's Validate stage: verifying before done, logging issues, and diagnosing them.

## Contents

- [Verify before done](#verify-before-done)
- [Issues workflow](#issues-workflow)
- [Diagnostic folder](#diagnostic-folder)
- [Lessons](#lessons)

## Verify before done

01. run the project's preflight check first, so an environment defect is not misread as a code defect.
02. start from a clean, seeded database for every check, and carry no state between checks.
03. start the app in the mode `.env` selects, and record the effective mode in the run log.
04. exercise the golden path and at least one error path of every surface the change touches: call each changed route directly, and load each changed page in a browser.
05. run the feature's automated test set, then the regression set, before reporting done.
06. when a surface could not be exercised, such as a page with no running frontend yet, say so in the report. A passing type check or unit suite alone never stands in for a runtime check.

## Issues workflow

The boilerplate is `templates/issue-diagnostic-section.md`. Paste it into the tracker's Validate section the moment a first-out failure happens.

01. every first-out failure gets a row in the Issues table, `id | seq | status | issue`, and its own diagnostic section with the header `_<F>.IS.<n> (pending) <first out exception>_`.
02. the diagnostic section holds the problem description, the exception, the triggering actions, the hypothesis, the diagnostic steps table and the diagnostic details.
03. a first-out failure is data. It is never a diagnostic step.
04. a diagnostic step reveals information or applies a fix. Reruns and re-validation are assumed and get no step.
05. step ids take the form `<F>.IS.<n>.<step>`, such as `02.IS.01.03`. Keep the step line brief, and put the detail in the diagnostic details.

## Diagnostic folder

Throwaway scripts, containers and files are allowed only here, for diagnosing an issue.

```
.dev/features/<NN>-<feature name>/scripts/01-read-container-logs.sh
```

## Lessons

### follow the project as it moves from stubbed to live operation

A project's run mode moves from stubs toward live services as it matures, and live runs become routine. When the user changes the mode in `.env`, read it as the user's intent. Update the agent instructions, skills, preflight checks and tracker commands in the same change, and ask when the intent is unclear.

**why**: the user set live mode on purpose so a feature could be validated against the real service. For the rest of the release the agents treated the setting as a leak: they scrubbed it from tests, overrode it inline, failed the preflight on it, and logged each live run as an incident.

Example: after the user sets `RATES_MODE=live`, the same change edits the preflight to report the mode, and the tracker commands drop their `RATES_MODE=stub` prefix.

### call each layer directly before building the next

Before building on a layer, call it directly: request the route with `curl` before writing the page that uses it. A service test proves the service, and says nothing about whether a route exists.

**why**: a briefing reported a joined endpoint as built and tested. The service tests passed, no route existed, and a `curl` call found it before any UI was built on it.

Example:

```bash
curl -sf -b .dev/cookies.txt http://localhost:8000/api/invoices/42 | python3 -m json.tool
```

### prove every check can fail

Every new check is shown to fail on a planted fault before it is trusted, its control passes first, and every regression test is shown to fail without its fix.

**why**: a control copy failed for the wrong reason and passed only once its inputs were complete. Checks that were never seen failing can pass on anything.

Example: the preflight check for a missing database URL is run once with the variable removed, and the run must print `[FAIL] DATABASE_URL missing` and exit non-zero.

### plan for the human walkthrough to find design gaps

The user's walkthrough is a design review as much as a test. Record each finding as an issue, and where the finding exposes a design gap, give the user options with their trade-offs.

**why**: a walkthrough after every automated layer had passed found a design gap in deletes with history, a list that never refreshed, and about thirty layout and workflow items.

Example: the walkthrough finds that a category with history cannot be deleted. The issue offers three options, block, cascade or retire, and the user picks retire.

### re-validate closed evidence when the design changes

When a design changes after tasks have closed, rerun the evidence of every closed task that depended on the changed part, against the new design.

**why**: the environment location and variable names changed after four tasks had closed, so their recorded evidence described a design that no longer existed.

Example: renaming `DB_PATH` to `DATABASE_URL` reopens the preflight and seed load checks, which rerun and record new evidence.

### keep issue ids unique and hypotheses provisional

Issue ids come from one numbering stream per tracker. A cause stays a hypothesis until a fix is applied and re-validated.

**why**: two numbering streams gave one id to two different issues, and a cause stated as fact before its fix ran misled the next session.

Example: `09.IS.34` is followed by `09.IS.35`, whichever stage finds it, and its cause reads "hypothesis: the seed anchor equals the run date" until the rerun passes.

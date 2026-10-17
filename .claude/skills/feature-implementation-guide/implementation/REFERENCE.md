# Implementation guide

The mechanics of a tracker's Implement stage: tracked scripts, parameters, error handling and logging.

## Contents

- [Rules](#rules)
- [Log file naming](#log-file-naming)
- [Folder layout](#folder-layout)
- [Lessons](#lessons)

## Rules

01. build, run, migrate and provision through git-tracked, rerunnable scripts. Throwaway virtual environments, containers and scripts belong only in the diagnostic folder of `../validation/REFERENCE.md`.
02. read parameters from `.env` through the project's settings object, and set every other parameter at the top of the script. Repeated literals, especially paths, become one named parameter.
03. wrap risky steps in functions or subscripts that exit non-zero on failure. Nothing fails silently.
04. catch each failure you can anticipate by its specific type, and print a message that names the cause and the fix.
05. every runnable action writes a log file, echoes a line for each key step, and marks results with `[PASS]` and `[FAIL]`.

## Log file naming

```
<YYMMDDHHMMSS>-<feature_id>.<subfeature_id>-<short task name>.log
```

For example, `260822185612-02.04-sql-create-generate.log`.

```bash
# .env
LOGS_DIR=.dev/logs
TIMEZONE='Asia/Singapore'
TIMESTAMP_FORMAT=%y%m%d%H%M%S

# script header
FEATURE_ID=02.04
TASK_NAME=sql-create-generate
LOG_FILE=$(TZ=$TIMEZONE date +$TIMESTAMP_FORMAT)-$FEATURE_ID-$TASK_NAME.log
LOG_PATH=$LOGS_DIR/$LOG_FILE
```

## Folder layout

```
.dev/
├── logs/                               # gitignored run logs
└── features/
    └── <NN>-<feature name>/            # such as 02-dev-env-setup-database/
        └── scripts/
            └── 01-read-container-logs.sh
```

## Lessons

### change the generator when the user edits generated output

When the user edits a generated file by hand, carry the change into the generator or its template, then regenerate and confirm the output matches the user's edit.

**why**: the user removed a generated line by hand. The generator still produced it, so the sync check failed on the next run of the main branch.

Example: the user deletes the `source:` footer from a generated docs page. The fix removes the footer from the page template, regenerates, and the diff against the user's edit is empty.

### run one agent session per working tree

Each concurrent agent session works in its own git worktree, created from the branch it builds on.

**why**: two sessions shared one working tree. One changed the schema for another feature, and 64 tests in the other session failed on a schema it never wrote.

Example:

```bash
git worktree add ../app-feature-13 -b feature/13-oauth-login
```

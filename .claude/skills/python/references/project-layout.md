# Project layout

How a Python project keeps its environments, dependencies and entry points reproducible.

## Rules

01. run every command through the project's named environment or container. A throwaway virtual environment is for diagnosing an issue only.
02. pin dependencies in a lock file, and change a pin in its own commit with the test run that proves it.
03. one package holds the app code. Scripts are modules in that package or a sibling `scripts` package, run with `python -m`.
04. type-hint every public function at a module boundary, and run the type checker in the regression set.
05. keep a `.env.sample` that lists every variable the settings object reads, with a safe default or a placeholder.

## Example

```
pyproject.toml          # dependencies and tool config
uv.lock                 # pinned versions
.env.sample             # every variable, no secrets
app/
├── __init__.py
├── main.py             # app factory
├── settings.py
└── services/
scripts/
├── __init__.py
└── load_seed.py        # run as: python -m scripts.load_seed
tests/
```

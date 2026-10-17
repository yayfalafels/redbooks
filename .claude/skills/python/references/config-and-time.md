# Configuration and time

How settings, run modes, paths and the clock reach every process from one source.

## Contents

- [Settings object](#settings-object)
- [Injectable clock](#injectable-clock)
- [Lessons](#lessons)

## Settings object

```python
# app/settings.py
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT = Path(__file__).resolve().parents[1]

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ROOT / ".env", extra="ignore")
    run_mode: str = "stub"            # stub or live
    rates_mode: str = "stub"
    allow_live_writes: bool = False   # the second opt-in
    data_dir: Path = Path("data")

    def path(self, p: Path) -> Path:
        return p if p.is_absolute() else ROOT / p

def get_settings() -> Settings:
    return Settings()
```

**open lesson LT.03** whether a startup log line plus a test that the app, a script and the fixtures build identical settings catches mode splits before a run. See `open-lessons.md`.

## Injectable clock

Code reads the current time through one function, so a test can pin it.

```python
# app/clock.py
from datetime import datetime, timezone

def now() -> datetime:
    return datetime.now(timezone.utc)
```

## Lessons

### read configuration directly from the env file

One settings object reads `.env` directly, and the app, the scripts and the tests all build it the same way. Nothing writes configuration into the process environment at import, and no layer scrubs or overrides values behind the file. Every run logs the effective mode it used.

**why**: an import-time loader, a test layer that removed keys, inline command overrides and scripts that set the mode again left each process in a different mode. A diagnostic script ran in another mode from the server it diagnosed, and the only clue was an implausible result count.

Example:

```python
settings = get_settings()
log.info("start mode=%s rates=%s live_writes=%s", settings.run_mode, settings.rates_mode, settings.allow_live_writes)
```

To read `.env` values without touching the process environment, use `dotenv_values(".env")`, never `load_dotenv()`.

### guard irreversible writes to real systems with a second opt-in

Live reads are routine once `.env` selects them. An irreversible write to a real external system or to the user's real data needs a second opt-in setting, checked at preflight before any row is written and again where the write happens.

**why**: a design never named the confirmation flag its scope required before a real submission. Only an unrelated refusal kept a live run from making irreversible writes.

Example:

```python
def migrate_into_working_db(settings: Settings) -> None:
    if not settings.allow_live_writes:
        raise PermissionError("set ALLOW_LIVE_WRITES=true in .env to write into the working database")
    backup_database(settings)
    ...
```

### read configuration at call time

Settings are read when the settings object is built, so a changed file or a test override takes effect on the next build. Module-level constants and dataclass field defaults never read the environment.

**why**: dataclass field defaults read the environment once at import, so a fixture that set the database path afterwards was ignored.

Example: routes take `settings: Settings = Depends(get_settings)`, and a test overrides `get_settings`.

### resolve paths from the project root

Every relative path in configuration resolves against one known root, `ROOT` above.

**why**: a relative upload directory resolved against the working directory, so a process started from the package folder answered every upload with a 500.

Example: `settings.path(settings.data_dir) / "export.csv"` gives the same file from any working directory. The regression test changes the working directory first.

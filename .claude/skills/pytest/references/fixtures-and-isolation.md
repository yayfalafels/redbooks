# Fixtures and isolation

How tests build settings, share fixtures, isolate databases and control time.

## Contents

- [Lessons](#lessons)

## Lessons

### read configuration directly from the env file

Tests build the app's settings object from `.env`, the same way the app and scripts do, and override fields through the settings provider. A test never edits `os.environ` to change a mode, and the session reports the effective mode at start.

**why**: a test layer removed keys from the environment, and importing a script restored them, so tests failed only in a full run. Another helper wrote `.env` values back into the test process.

Example:

```python
# tests/conftest.py
@pytest.fixture(scope="session")
def settings() -> Settings:
    s = get_settings()
    print(f"\ntest mode={s.run_mode} rates={s.rates_mode}")
    return s

@pytest.fixture
def client(settings):
    app.dependency_overrides[get_settings] = lambda: settings
    yield TestClient(app)
    app.dependency_overrides.clear()
```

### share fixtures once and run workers as production does

Shared fixtures, such as a browser or an app server, are registered once in the top `conftest.py`. Tests run workers on their own thread or process, as production does. At least one check exercises the real implementation behind every fake.

**why**: two test tiers each registered a browser fixture, and the second failed in a full run. A test ran a worker on the test thread, and the worker's catch-all recorded the harness error as a domain outcome. A fake hid a thread affinity defect that the real implementation exposed.

Example: `tests/conftest.py` defines `live_server` once with `scope="session"`, and the job tests start the job through the same queue the app uses.

### keep startup side effects away from raw-seed checks

Checks of the raw seed use a database that no app instance has started against, because startup jobs change rows.

**why**: the app's startup job closed a seeded running row in the shared database before the seed oracle read it.

Example: the seed oracle fixture creates `test_seed_raw`, loads the seed, and runs its queries before any app fixture is requested.

### pin the clock before creating time-bound state

One injectable clock drives every time-bound value. A test pins it before it creates sessions or rows, and moves it to reach time-based paths.

**why**: a fixture opened a session at real time, the test then pinned the clock past the session's lifetime, and every request answered 401. A refresh path never ran because the seed anchor equalled the run date.

Example:

```python
@pytest.fixture
def clock(monkeypatch):
    t = {"now": datetime(2026, 3, 31, 9, 0, tzinfo=timezone.utc)}
    monkeypatch.setattr("app.clock.now", lambda: t["now"])
    return t

def test_session_expires(clock, signed_in_client):   # clock is requested first
    clock["now"] += timedelta(hours=13)
    assert signed_in_client.get("/api/me").status_code == 401
```

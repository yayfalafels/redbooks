# Flaky test triage

How to handle a browser test that fails only sometimes or only in the full run.

**open lesson LT.02** whether delaying a route reproduces full-run-only timeouts deterministically. See `open-lessons.md`.

## Lessons

### give every test an expected latency and fail when it is exceeded

Each page test carries a latency budget: a few seconds for a page served by the local app, 30 seconds where the page waits on an internet API. A timeout seen only in the full run is reproduced by injecting latency on the route it waits for. Load variance is never an accepted close.

**why**: two full-run-only timeouts were closed as load variance with no confirmed cause. A third with the same shape, reproduced by injected latency, was a real missing wait.

Example:

```python
import time

def slow(route):
    time.sleep(2)          # injected latency, the one place a sleep belongs
    route.continue_()

def test_balance_waits_for_load(page):
    page.route("**/api/accounts/3/balance", slow)
    page.goto("/accounts/3")
    expect(page.get_by_test_id("balance")).to_have_text("1,250.00", timeout=5_000)
```

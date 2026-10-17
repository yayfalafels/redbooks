# Mobile viewport

How the browser, viewport and failure evidence are set up once for the suite.

## Setup

01. headless Chromium is the default. A visible browser is for the user's interactive debugging only.
02. the default context uses a phone viewport, 375 by 812 pixels with touch enabled. A desktop test overrides it to 1280 by 800.
03. the browser launches once per session, and each test gets a fresh context.
04. a failing test keeps its screenshot and trace in `test-results/`, which is gitignored.

## Example

```python
# tests/conftest.py
import pytest

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, base_url):
    return {**browser_context_args, "viewport": {"width": 375, "height": 812}, "has_touch": True, "base_url": base_url}

@pytest.fixture
def desktop(browser):
    ctx = browser.new_context(viewport={"width": 1280, "height": 800})
    yield ctx.new_page()
    ctx.close()
```

```bash
python -m pytest tests/features --browser chromium --screenshot only-on-failure --tracing retain-on-failure
```

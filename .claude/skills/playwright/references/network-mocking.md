# Network mocking

How frontend silo tests answer API calls without a running backend.

## Rules

01. a silo test routes every `/api/` call. An unrouted call fails the test.
02. canned responses live in `tests/stubs/api/`, one JSON file per case.
03. an integration test runs against the real backend, with no routing.

## Lessons

### capture fixtures and stubs from real artifacts

Canned responses are captured from the real API, then reduced. A response written by hand proves only its author's guess about the contract.

**why**: hand-written fixture pages used guessed attribute names, so every fixture test passed while the live run failed.

Example:

```python
import json, pathlib

STUBS = pathlib.Path("tests/stubs/api")

def test_entry_list_empty(page):
    page.route("**/api/accounts/3/entries", lambda r: r.fulfill(json=json.loads((STUBS / "entries-empty.json").read_text())))
    page.route("**/api/**", lambda r: r.abort())        # anything unrouted fails
    page.goto("/accounts/3")
    expect(page.get_by_text("No entries yet")).to_be_visible()
```

`entries-empty.json` was saved from a real response with `curl -s -b .dev/cookies.txt http://localhost:8000/api/accounts/3/entries`.

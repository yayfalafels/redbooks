# Errors and logging

How to catch, report and log failures so each cause is visible and actionable.

## Rules

01. reproduce each failure in isolation to learn which exception type it raises.
02. import exception classes from the library's public API.
03. one `except` clause per identified cause, each with a message that names the cause and the fix.
04. a catch-all is reserved for keeping a batch running. It logs the original exception with its traceback and marks the item failed.
05. log through the standard `logging` module with a named logger per module. A bare `print` or a silent `except: pass` is a defect.

## Lessons

### catch every exception family a library delegates to

A library often delegates work to another library, which raises its own exception types. Reproduce each failure in isolation, catch each cause by its own type, keep the causes isolated, and give the user an actionable hint.

**why**: a token validation failure raised an exception from a library the OAuth package delegated to, so the callback answered 500. Another fix imported an exception class that was not public, and a third caught an exception the framework never raised.

Example:

```python
from authlib.jose.errors import ExpiredTokenError, InvalidClaimError
from authlib.integrations.base_client.errors import OAuthError

try:
    token = await oauth.provider.authorize_access_token(request)
except ExpiredTokenError:
    raise SignInError("sign-in took too long, start again")
except (InvalidClaimError, OAuthError) as exc:
    raise SignInError(f"the identity provider rejected sign-in: {exc}")
```

### background jobs reach a terminal status and persist progress

A background job always ends in a terminal status, such as `succeeded`, `failed` or `cancelled`, with the original exception recorded on failure. It commits a progress snapshot after each step, so a crash keeps its counts.

**why**: a live run stayed `running` past both poll budgets with no error. In another, the recorded error named a secondary failure and hid the cause.

Example:

```python
job.status = "running"; db.commit()
try:
    for i, day in enumerate(days, 1):
        fetch_rates(day)
        job.done = i; db.commit()
    job.status = "succeeded"
except Exception as exc:
    log.exception("rate fetch failed on %s", day)
    job.status, job.error = "failed", repr(exc)
finally:
    db.commit()
```

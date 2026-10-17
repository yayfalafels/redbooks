# HTTP clients

How to call an outside API so every failure has a clear cause.

## Lessons

### configure outbound HTTP clients explicitly

01. one client per job or app lifespan, closed when it ends.
02. explicit connect, read and total timeouts.
03. check the status before reading the body.
04. map transport errors and status errors to separate, actionable exceptions.
05. pass query parameters as data, never by string formatting.

**why**: a client with default timeouts hung a job past its poll budget, and one combined `except` reported a rate limit and a DNS failure as the same error.

Example:

```python
import httpx

TIMEOUT = httpx.Timeout(10.0, connect=5.0)

def fetch_rate(client: httpx.Client, base: str, quote: str, day: str) -> Decimal:
    try:
        r = client.get("/rates", params={"base": base, "quote": quote, "date": day}, timeout=TIMEOUT)
        r.raise_for_status()
    except httpx.TransportError as exc:
        raise RateSourceUnavailable(f"rate source unreachable, check the network: {exc}") from exc
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 429:
            raise RateLimited("rate source limit reached, retry after a minute") from exc
        raise RateSourceError(f"rate source answered {exc.response.status_code}") from exc
    return r.json(parse_float=Decimal)["rate"]
```

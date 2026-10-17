# API and ownership tests

How routes, ownership and sign-in are tested.

## Rules

01. every route has a golden path test and a test for each status in its error contract.
02. two seeded users and a sign-in helper exist before the first feature test.
03. a test signs in through the stub identity provider, never by writing a session row directly.

**open lesson LT.01** whether generating the per-endpoint error tests and vocabulary coverage from the route table catches defects hand-written cases miss. See `open-lessons.md`.

## Lessons

### generate the ownership matrix from the resource registry

Ownership tests are generated from the app's route table, so a new route fails until it declares its owner check. For each route, the second user gets the same 404 as a missing record.

**why**: a generated tenancy matrix caught two unscoped routes added after it was written.

Example:

```python
OWNED = [r for r in app.routes if r.path.startswith("/api/") and "{" in r.path]

@pytest.mark.parametrize("route", OWNED, ids=lambda r: f"{sorted(r.methods)[0]} {r.path}")
def test_other_user_gets_404(route, alice_record_ids, bob_client):
    method = sorted(route.methods)[0]
    r = bob_client.request(method, route.path.format(**alice_record_ids), json={})
    assert r.status_code == 404
```

### test OAuth against a local stub provider

Automated tests run the full authorization code flow against a local OpenID Connect stub, with one scenario per failure kind. They run against the stub first, then make live calls for everything except irreversible writes. The full live sign-in with its writes is the user's own test. Provider setup checks follow redirects to the final page.

**why**: the stub covered every token failure kind without a real account, and a setup check that stopped at the first redirect passed a wrong redirect URI.

Example:

```python
@pytest.mark.parametrize("email,status", [("ok@stub.test", 302), ("expired@stub.test", 401), ("audience@stub.test", 401)])
def test_callback(stub_idp, client, email, status):
    r = stub_idp.sign_in(client, email=email)
    assert r.status_code == status
```

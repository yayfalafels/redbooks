# OAuth sessions

How sign-in, sessions and token validation work, and how they are tested without a live identity provider.

## Contents

- [Flow](#flow)
- [Lessons](#lessons)

## Flow

01. `/auth/login` stores the requested path, creates a PKCE verifier and state, and redirects to the identity provider.
02. `/auth/callback` exchanges the code for tokens, validates the ID token, finds or creates the user, and sets an HTTP-only, secure, same-site session cookie.
03. `current_user` reads the session on every API request and answers 401 when it is missing or expired.
04. `/auth/logout` clears the session.
05. the provider is set by settings: a local stub provider for automated tests, the real provider when `.env` selects it.

## Lessons

### catch every exception family a library delegates to

The OAuth client delegates token parsing and validation to other libraries, which raise their own exception types. Reproduce each sign-in failure in isolation, catch each type it raises from the public API, and answer 401 with an actionable message.

**why**: an ID token validation failure raised an exception from a delegated library, and the callback answered 500.

Example: an expired token, a wrong audience and a bad signature are each produced by the stub provider, and each must answer 401 from `/auth/callback`.

### read library defaults before writing boundary cases

Read the library's defaults, such as clock leeway and token lifetimes, before writing a boundary test, and put the boundary beyond the tolerance.

**why**: a token that expired one second earlier was accepted, because the library allows 120 seconds of clock leeway. The leeway was kept, so a slow local clock would not refuse real tokens, and the test boundary moved to one hour.

Example: the expired-token case signs a token with `exp = now - 3600`.

### test OAuth against a local stub provider

Automated tests sign in through a local OpenID Connect stub that signs its own tokens, with one scenario per failure kind, selected by the email entered on its consent page. Tests run against the stub first, then make live calls for everything except irreversible writes. The full live sign-in with its writes is the user's own test. Provider setup checks follow redirects to the final page.

**why**: a full authorization code flow against a stub caught every token failure kind without a real account, and a setup check that stopped at the first redirect passed a wrong redirect URI.

Example:

| id | stub email           | scenario                  | expected             |
| -- | -------------------- | ------------------------- | -------------------- |
| 01 | `ok@stub.test`       | valid token               | session, 302 to path |
| 02 | `expired@stub.test`  | token expired an hour ago | 401                  |
| 03 | `audience@stub.test` | wrong audience            | 401                  |
| 04 | `deny@stub.test`     | user denies consent       | 401, sign-in page    |

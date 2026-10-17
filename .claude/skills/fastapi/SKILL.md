---
name: fastapi
description: FastAPI service practice, covering one explicit router per resource, services for writes with invariants, dependency-supplied settings and sessions, per-verb error contracts and check order, ownership checks, default-deny API paths, JSON types for decimal fields, and OAuth authorization code sign-in with PKCE. Use when writing or reviewing any FastAPI route, dependency, schema, error handler or sign-in flow.
---

# FastAPI

Practice for a FastAPI app that serves a JSON API to a browser frontend, with per-user data and OAuth sign-in.

## Rules

01. **one explicit router per resource.** Shared behavior lives in dependencies and services. No generic route layer is built.
02. **writes with invariants go through services.** A route validates the request and calls the service that enforces the invariants. An endpoint that gains a mode keeps every earlier call shape working.
03. **documented error contract, fixed check order.** Each verb documents its error responses. Checks run in order: request shape, then ownership, then business rules. A missing record and another user's record get the same answer.
04. **default-deny API paths.** Every path under the API prefix requires a session by default, and the frontend fallback never serves an API path.
05. **declare JSON types.** The API contract states the JSON type of every structured and decimal field. Money is a decimal string.
06. **OAuth with PKCE.** Sign-in uses the authorization code flow with PKCE. Every token validation error answers 401, and boundary tests account for the library's tolerances.

## References

| id | file                                 | read it when                                       |
| -- | ------------------------------------ | -------------------------------------------------- |
| 01 | `references/routes-and-schemas.md`   | adding or changing a router, route or schema       |
| 02 | `references/ownership-and-errors.md` | adding a user-owned resource or an error response  |
| 03 | `references/oauth-sessions.md`       | changing sign-in, sessions, tokens or the stub IdP |

## Related skills

- [python](../python/SKILL.md) for settings, exceptions and HTTP clients.
- [postgresql](../postgresql/SKILL.md) for the schema behind each router.
- [pytest](../pytest/SKILL.md) for API, ownership and OAuth tests.

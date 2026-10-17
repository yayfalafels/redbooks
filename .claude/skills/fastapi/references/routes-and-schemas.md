# Routes and schemas

How routers, services and schemas divide the work, and how the API prefix is protected.

## Contents

- [Layout](#layout)
- [Lessons](#lessons)

## Layout

```
app/
├── main.py              # app factory: includes routers, mounts the frontend last
├── deps.py              # get_settings, get_db, current_user
├── routers/
│   ├── invoices.py      # one router per resource
│   └── customers.py
├── schemas/             # pydantic request and response models
└── services/            # invariants live here
```

```python
# app/main.py
api = APIRouter(prefix="/api", dependencies=[Depends(current_user)])
api.include_router(invoices.router)
api.include_router(customers.router)
app.include_router(api)
app.include_router(auth.router)                 # the only public routes
app.mount("/", SPAStaticFiles(directory="web/dist", html=True))
```

## Lessons

### route invariant-bearing writes through services

One explicit router per resource. A write to an entity with invariants goes only through the service that enforces them. The route validates the request and calls the service, and no generic create, update or delete layer exists.

**why**: a generic CRUD surface let any client write a status field directly, bypassing its state machine. The hooks added to protect it grew into create, update, batch, search and delete variants.

Example:

```python
@router.post("/invoices/{invoice_id}/payments", response_model=PaymentOut, status_code=201)
def record_payment(invoice_id: int, body: PaymentIn, user=Depends(current_user), db=Depends(get_db)):
    return payments.record(db, user, invoice_id, body)   # checks the balance and the state
```

### deny the API prefix by default and keep the frontend fallback off it

Every path under the API prefix requires a session by default. An unknown API path answers a JSON 404 to a signed-in user and 401 to anyone else. The single-page fallback serves HTML only outside the API prefix.

**why**: the fallback answered 200 with HTML for unknown API paths. Once fixed, the fallback was public, so a signed-out request to an unknown API path got 404 and learned the route did not exist.

Example:

```python
@api.api_route("/{rest:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"], include_in_schema=False)
def api_not_found(rest: str):
    raise HTTPException(404, "no such API path")   # current_user on the router already answered 401
```

### declare how structured fields serialise

The API contract states the JSON type of every structured and decimal field, and response models declare it. Money is a decimal string, so the client never parses a float.

**why**: a JSON text column reached the client as a string while the frontend read it as an object, and `Decimal` serialises as a string, which a client that expects a number mishandles.

Example:

```python
class EntryOut(BaseModel):
    amount: Annotated[Decimal, PlainSerializer(lambda d: f"{d:.2f}", return_type=str)]
    tags: list[str]      # a JSON array, never a JSON-encoded string
```

### extend an endpoint without dropping its existing call shapes

When an endpoint gains a mode or parameter, the new parameter is optional, and every earlier call shape keeps its response. Run the tests related to the endpoint before the full suite.

**why**: a new search parameter was made required, which broke a call shape the ownership tests relied on. A targeted run of related tests caught it first.

Example: `GET /api/entries?account_id=3` keeps working after `GET /api/entries?account_id=3&q=rent` is added, because `q: str | None = None`.

# Ownership and errors

How every user-owned record is scoped to its owner, and how each verb reports failure.

## Rules

01. every user-owned table has an owner column, and every query on it filters by the current user.
02. ownership is checked in a dependency or service, never in the frontend.
03. a 400 or 422 names every invalid field.
04. a missing record and another user's record both answer 404 with the same message.

## Error contract

| id | verb   | 401        | 404                       | 409             | 422              |
| -- | ------ | ---------- | ------------------------- | --------------- | ---------------- |
| 01 | GET    | no session | missing or not owned      | n/a             | bad query params |
| 02 | POST   | no session | parent missing or foreign | rule violated   | bad body fields  |
| 03 | PATCH  | no session | missing or not owned      | rule violated   | bad body fields  |
| 04 | DELETE | no session | missing or not owned      | live use blocks | n/a              |

## Lessons

### define the error contract per verb and the order of checks

Each verb has a documented error contract. Checks run in a fixed order: request shape, then ownership, then business rules. A missing and a foreign record get the same status and message.

**why**: an update naming an unknown parent answered 404 where its contract said 400 on the field. An ownership loop ran before the size check, so an oversize batch answered 404. A 400 named no field.

Example:

```python
@router.patch("/invoices/{invoice_id}")
def update_invoice(invoice_id: int, body: InvoicePatch,          # 01 shape: FastAPI answers 422 first
                   user=Depends(current_user), db=Depends(get_db)):
    invoice = invoices.get_owned(db, user, invoice_id)           # 02 ownership: 404 if missing or foreign
    return invoices.update(db, invoice, body)                    # 03 rules: 409 with the rule named
```

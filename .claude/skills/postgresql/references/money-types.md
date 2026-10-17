# Money types

How to store amounts, rates and currencies exactly.

## Rules

01. amounts are `NUMERIC(19, 4)` or the currency's own scale, never `real`, `double precision` or `money`.
02. exchange rates are `NUMERIC(20, 10)`.
03. currency is a `char(3)` ISO 4217 code with a foreign key to a seeded currency table.
04. a signed amount carries its sign. A separate direction column is never needed.
05. the app reads `NUMERIC` as `Decimal`, and the driver is configured so it never converts to float.

## Example

```sql
CREATE TABLE entry (
    id             bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    transaction_id bigint NOT NULL REFERENCES txn (id),
    account_id     bigint NOT NULL REFERENCES account (id),
    amount         numeric(19, 4) NOT NULL CHECK (amount <> 0),
    currency       char(3) NOT NULL REFERENCES currency (code)
);
```

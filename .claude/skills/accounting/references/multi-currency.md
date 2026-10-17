# Multi-currency

How entries, transfers and balances work when more than one currency is involved. The reporting currency is the one the statements total in.

## Contents

- [Rules](#rules)
- [Examples](#examples)

## Rules

01. **keep the nominal amount and the rate.** A transaction in a foreign currency keeps its currency, its nominal amount and the rate used. The reporting amount is the nominal amount times the rate, quantised to the reporting currency's minor unit.
02. **each account holds its own currency.** An account's ledger entries are in the account's currency. A balance in another currency is translated only when a statement is built.
03. **transfers balance in the reporting currency.** A transfer between accounts in different currencies has one entry in each account's currency. Converted at the transfer's rate, the entries sum to zero.
04. **realised gains and losses.** Settling at a different rate from the booking rate gives a realised gain or loss, posted as income or expense.
05. **unrealised gains and losses.** Translating a foreign balance at the closing rate gives an unrealised gain or loss. It is either posted as an entry or computed when the balance sheet is built, and a ledger states which.
06. **fees are separate entries.** When a card bills more than the converted amount, the difference is a separate fee expense on the same card.
07. **translation mappings.** Each statement source records the currency of its amounts and how it signs them, so its lines map to signed entries in the right currency.

## Examples

### card charge with a fee

A charge of 100.00 in a foreign currency at a rate of 1.35 is 135.00 in the reporting currency. The card bills 136.50.

| id | account        | type      | entry   |
| -- | -------------- | --------- | ------- |
| 01 | Expense:Travel | expense   | -135.00 |
| 02 | Expense:Fees   | expense   | -1.50   |
| 03 | Credit card    | liability | -136.50 |

The fee is 136.50 - 135.00 = 1.50. The travel transaction keeps the nominal 100.00 and the rate 1.35.

### transfer between currencies

Moving funds to a foreign currency account, receiving 1,000.00 at a rate of 1.35.

| id | account         | type  | entry          |
| -- | --------------- | ----- | -------------- |
| 01 | Checking        | asset | -1,350.00 home |
| 02 | Foreign savings | asset | +1,000.00 fgn  |

Balance in the reporting currency: -1,350.00 + 1,000.00 x 1.35 = 0.00.

### translating a foreign balance

The foreign account holds 1,000.00, carried at 1.35, which is 1,350.00. At period end the rate is 1.37, so it is worth 1,370.00.

| id | account            | type   | entry home |
| -- | ------------------ | ------ | ---------- |
| 01 | Foreign savings    | asset  | +20.00     |
| 02 | Unrealised FX gain | income | +20.00     |

The account's own ledger balance stays 1,000.00. Only its reporting value moves.

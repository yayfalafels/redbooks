---
name: accounting
description: Personal and small-business bookkeeping rules in a signed-entry vocabulary, covering transactions that balance against net worth, transfers, opening balances, reconciled balance points, splits, billing accounts, multi-currency entries, identity assertions, reconciliation and statement presentation. Use when designing, implementing, testing or reviewing a ledger, a posting, a balance, a reconciliation, a currency conversion, or an income statement or balance sheet.
---

# Accounting

Every entry is a signed change to one account's balance, and every rule here is stated in that vocabulary. Debit and credit appear only as labels a statement source uses, translated at its boundary.

## Rules

01. **sign by net worth.** Every entry is a signed change to its account's balance, signed by its contribution to net worth: assets and income positive, liabilities and expenses negative. Store entries as signed amounts.
02. **balance against net worth.** A transaction balances when its asset and liability entries sum to its income, expense and equity entries.
03. **check each sign against its event.** A purchase is a negative expense entry and a negative entry on the account that paid. A check tests every entry's sign against the event as well as the balance, since flipping every sign keeps a transaction balanced.
04. **balances follow from a reconciled balance point.** A balance on any date equals a reconciled balance point, an amount on a date confirmed against an independent source, plus the signed entries between the two dates.
05. **transfers move no net worth.** A transfer between the owner's own accounts is neither income nor expense, and its asset and liability entries sum to zero.
06. **debit and credit are translators.** Each statement source carries a mapping from its labels or signs to signed entries on the account it feeds.
07. **exact amounts.** Amounts are exact decimals to their currency's minor unit, and a split sums exactly to its total, with any rounding residual on one named entry.
08. **correct by reversal, retire by flag.** A posted transaction is corrected by a reversing transaction and a new one. An account or category that history references is retired, never deleted.
09. **flip signs only to present.** The books, the API, every calculation and every test hold signed entries. A statement flips expense signs for readability as the last step of rendering it.

## References

| id | file                                | read it when                                             |
| -- | ----------------------------------- | -------------------------------------------------------- |
| 01 | `references/ledger-models.md`       | modelling accounts, postings, transfers, splits or bills |
| 02 | `references/identity-assertions.md` | writing a calculation, an oracle or a worked example     |
| 03 | `references/statements.md`          | building an income statement, balance sheet or report    |
| 04 | `references/reconciliation.md`      | comparing the books with a statement or another ledger   |
| 05 | `references/multi-currency.md`      | an entry, transfer or balance involves a second currency |

## Related skills

- [python](../python/SKILL.md) for `Decimal` money handling.
- [postgresql](../postgresql/SKILL.md) for exact `NUMERIC` storage and retire flags.

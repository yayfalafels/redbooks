"""HomeBudget data review: account 01 reference figures and mapping domain.

Reads the account 01 HomeBudget database named by HB_DB_ACCOUNT_01_PATH in .env,
opened read-only, and writes two JSON files into the gitignored data/ folder:

  data/homebudget-data-review/account-01-reference.json
      record counts, data quality counts, opening balances at the scope start,
      balances at the cutoff and category totals per year, all within the migration
      scope, which the account 01 migration is checked against.
  data/homebudget-data-review/account-01-domain.json
      every account with its activity in scope and its retired flag, and every
      category and subcategory pair in use, the domain the account 01 mapping must cover.

Both files carry real account names and stay out of git.

Usage: env/bin/python scripts/homebudget_data_review.py [--no-wrapper-check]
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sqlite3
import sys
from decimal import Decimal
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OUT_DIR = REPO / "data" / "homebudget-data-review"
SCOPE_START = "2017-01-01"
CUTOFF = "2026-05-23"
DAY_BEFORE_SCOPE = "2016-12-31"
CENT = Decimal("0.01")
# AccountTrans.transType: 0 opening, 1 expense, 2 income, 3 transfer out, 4 transfer in
SIGN = {1: -1, 2: 1, 3: -1, 4: 1}
RECORD_TABLES = (("expense", "Expense", "date"), ("income", "Income", "date"), ("transfer", "Transfer", "transferDate"))


def read_env(name: str) -> str:
    for line in (REPO / ".env").read_text(encoding="utf-8").splitlines():
        if line.startswith(f"{name}="):
            return line.split("=", 1)[1].strip().strip('"')
    raise SystemExit(f"{name} is missing from .env")


def dec(value: object) -> Decimal:
    return Decimal(str(value))


def scalar(con: sqlite3.Connection, sql: str, *args: object) -> object:
    return con.execute(sql, args).fetchone()[0]


def balances_at(con: sqlite3.Connection, date: str) -> dict[int, Decimal]:
    """Roll each account from its reconciled balance point to the end of the given date."""
    accounts = {
        key: (dec(balance), balance_date)
        for key, balance, balance_date in con.execute("SELECT key, balance, balanceDate FROM Account")
    }
    result = {key: point for key, (point, _) in accounts.items()}
    rows = con.execute("SELECT accountKey, transType, transDate, transAmount FROM AccountTrans WHERE transType > 0")
    for key, trans_type, trans_date, amount in rows:
        _, point_date = accounts[key]
        signed = SIGN[trans_type] * dec(amount)
        if point_date < trans_date <= date:
            result[key] += signed
        elif date < trans_date <= point_date:
            result[key] -= signed
    return {key: value.quantize(CENT) for key, value in result.items()}


def scope_activity(con: sqlite3.Connection) -> dict[int, int]:
    """AccountTrans rows per account inside the migration scope."""
    return dict(
        con.execute(
            "SELECT accountKey, count(*) FROM AccountTrans WHERE transType > 0 AND transDate BETWEEN ? AND ? GROUP BY 1",
            (SCOPE_START, CUTOFF),
        ).fetchall()
    )


def quality_counts(con: sqlite3.Connection) -> dict[str, int]:
    scope = f"BETWEEN '{SCOPE_START}' AND '{CUTOFF}'"
    checks = {
        "expense_before_scope": f"SELECT count(*) FROM Expense WHERE date < '{SCOPE_START}'",
        "income_before_scope": f"SELECT count(*) FROM Income WHERE date < '{SCOPE_START}'",
        "transfer_before_scope": f"SELECT count(*) FROM Transfer WHERE transferDate < '{SCOPE_START}'",
        "expense_after_cutoff": f"SELECT count(*) FROM Expense WHERE date > '{CUTOFF}'",
        "income_after_cutoff": f"SELECT count(*) FROM Income WHERE date > '{CUTOFF}'",
        "transfer_after_cutoff": f"SELECT count(*) FROM Transfer WHERE transferDate > '{CUTOFF}'",
        "expense_no_account_in_scope": (
            f"SELECT count(*) FROM Expense WHERE payFrom NOT IN (SELECT key FROM Account) AND date {scope}"
        ),
        "income_no_account_in_scope": (
            f"SELECT count(*) FROM Income WHERE addIncomeTo NOT IN (SELECT key FROM Account) AND date {scope}"
        ),
        "split_rows_in_scope": f"SELECT count(*) FROM Expense WHERE (isCategorySplit = 'Y' OR masterKey > 0) AND date {scope}",
        "expense_zero": f"SELECT count(*) FROM Expense WHERE amount = 0 AND date {scope}",
        "expense_negative": f"SELECT count(*) FROM Expense WHERE amount < 0 AND date {scope}",
        "income_negative": f"SELECT count(*) FROM Income WHERE amount < 0 AND date {scope}",
        "transfer_negative": f"SELECT count(*) FROM Transfer WHERE amount < 0 AND transferDate {scope}",
        "expense_foreign_nominal": (
            "SELECT count(*) FROM Expense e JOIN Account a ON a.key = e.payFrom "
            f"WHERE a.currency <> e.currency AND e.date {scope}"
        ),
        "expense_amount_differs_from_posted": (
            "SELECT count(*) FROM Expense e JOIN AccountTrans t ON t.transType = 1 AND t.transKey = e.key "
            f"WHERE abs(t.transAmount - e.amount) > 0.005 AND e.date {scope}"
        ),
        "transfer_cross_currency": (
            "SELECT count(*) FROM Transfer t JOIN Account f ON f.key = t.fromAccount "
            f"JOIN Account o ON o.key = t.toAccount WHERE f.currency <> o.currency AND t.transferDate {scope}"
        ),
        "expense_duplicate_rows": (
            f"SELECT coalesce(sum(n), 0) FROM (SELECT count(*) n FROM Expense WHERE date {scope} GROUP BY date, "
            "catKey, subCatKey, amount, payFrom, notes, payeeKey, currency, currencyAmount HAVING n > 1)"
        ),
        "transfer_duplicate_rows": (
            f"SELECT coalesce(sum(n), 0) FROM (SELECT count(*) n FROM Transfer WHERE transferDate {scope} GROUP BY "
            "transferDate, fromAccount, toAccount, amount, notes, currency, currencyAmount HAVING n > 1)"
        ),
        "subcategories_unused_in_scope": (
            f"SELECT count(*) FROM SubCategory WHERE key NOT IN (SELECT subCatKey FROM Expense WHERE date {scope})"
        ),
    }
    return {name: int(scalar(con, sql)) for name, sql in checks.items()}


def category_totals(con: sqlite3.Connection) -> list[dict[str, object]]:
    """Ledger expense totals per year, category, subcategory and account currency, within the scope.

    Amounts come from AccountTrans, the account-side amount HomeBudget posted.
    """
    rows = con.execute(
        """
        SELECT substr(e.date, 1, 4), c.name, s.name, a.currency, count(*), sum(t.transAmount)
        FROM Expense e
        JOIN AccountTrans t ON t.transType = 1 AND t.transKey = e.key
        JOIN Account a ON a.key = e.payFrom
        JOIN Category c ON c.key = e.catKey
        JOIN SubCategory s ON s.key = e.subCatKey
        WHERE e.date BETWEEN ? AND ?
        GROUP BY 1, 2, 3, 4 ORDER BY 1, 2, 3, 4
        """,
        (SCOPE_START, CUTOFF),
    )
    return [
        {"year": y, "category": c, "subcategory": s, "currency": cur, "count": n, "amount": str(dec(t).quantize(CENT))}
        for y, c, s, cur, n, t in rows
    ]


def wrapper_check(db_path: str, names: dict[int, str], ours: dict[int, Decimal]) -> list[dict[str, str]]:
    """Cross-check each cutoff balance against the homebudget wrapper's own balance query."""
    from homebudget import HomeBudgetClient

    cutoff = dt.date.fromisoformat(CUTOFF)
    mismatches = []
    with HomeBudgetClient(db_path=db_path, enable_sync=False, enable_forex_rates=False) as client:
        for key, name in sorted(names.items()):
            try:
                theirs = dec(client.get_account_balance(name, cutoff).balanceAmount).quantize(CENT)
            except Exception as exc:  # the wrapper raises sqlite and lookup errors per account
                mismatches.append({"account": name, "ours": str(ours[key]), "wrapper": f"{type(exc).__name__}: {exc}"})
                continue
            if theirs != ours[key]:
                mismatches.append({"account": name, "ours": str(ours[key]), "wrapper": str(theirs)})
    return mismatches


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--no-wrapper-check", action="store_true", help="skip the homebudget wrapper cross-check")
    args = parser.parse_args()

    db_path = read_env("HB_DB_ACCOUNT_01_PATH")
    con = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    accounts = con.execute(
        "SELECT key, name, accountType, currency, balance, balanceDate, includeAccount FROM Account ORDER BY key"
    ).fetchall()
    names = {row[0]: row[1] for row in accounts}
    activity = scope_activity(con)
    opening = balances_at(con, DAY_BEFORE_SCOPE)
    closing = balances_at(con, CUTOFF)

    counts = {
        kind: {
            "total": int(scalar(con, f"SELECT count(*) FROM {table}")),
            "in_scope": int(scalar(con, f"SELECT count(*) FROM {table} WHERE {col} BETWEEN ? AND ?", SCOPE_START, CUTOFF)),
        }
        for kind, table, col in RECORD_TABLES
    }
    account_rows = [
        {
            "key": key, "name": name, "type": typ, "currency": cur, "point_balance": str(dec(bal)), "point_date": bdate,
            "include_in_net_worth": incl == "Y", "rows_in_scope": activity.get(key, 0), "retired": key not in activity,
            "opening_at_scope_start": str(opening[key]), "balance_at_cutoff": str(closing[key]),
        }
        for key, name, typ, cur, bal, bdate, incl in accounts
    ]
    reference = {
        "source": "HomeBudget account 01",
        "scope": {"start": SCOPE_START, "cutoff": CUTOFF},
        "generated": dt.datetime.now().isoformat(timespec="seconds"),
        "counts": counts,
        "quality": quality_counts(con),
        "accounts": [
            {k: row[k] for k in ("name", "type", "currency", "retired", "opening_at_scope_start", "balance_at_cutoff")}
            for row in account_rows
        ],
        "category_totals": category_totals(con),
    }
    domain = {
        "accounts": account_rows,
        "categories": [
            {"category": c, "subcategory": s, "count": n, "first": first, "last": last}
            for c, s, n, first, last in con.execute(
                """
                SELECT c.name, s.name, count(e.key), min(e.date), max(e.date)
                FROM SubCategory s JOIN Category c ON c.key = s.catKey
                LEFT JOIN Expense e ON e.subCatKey = s.key AND e.date BETWEEN ? AND ?
                GROUP BY s.key ORDER BY c.seqNum, s.seqNum
                """,
                (SCOPE_START, CUTOFF),
            )
        ],
    }
    if not args.no_wrapper_check:
        reference["wrapper_balance_mismatches"] = wrapper_check(db_path, names, closing)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "account-01-reference.json").write_text(json.dumps(reference, indent=1), encoding="utf-8")
    (OUT_DIR / "account-01-domain.json").write_text(json.dumps(domain, indent=1), encoding="utf-8")

    retired = [row for row in account_rows if row["retired"]]
    used_pairs = sum(1 for row in domain["categories"] if row["count"])
    print(f"scope {SCOPE_START} to {CUTOFF}  counts {counts}")
    print(f"quality {reference['quality']}")
    print(f"accounts {len(accounts)}, retired {len(retired)}, migrated {len(accounts) - len(retired)}")
    print(f"retired with a non-zero balance at the cutoff: {sum(1 for r in retired if Decimal(r['balance_at_cutoff']) != 0)}")
    print(f"category pairs used in scope: {used_pairs}  category total rows: {len(reference['category_totals'])}")
    if "wrapper_balance_mismatches" in reference:
        print(f"wrapper balance mismatches: {reference['wrapper_balance_mismatches']}")
    print(f"wrote {OUT_DIR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""Snapshot the live HomeBudget account 02 database for the seed.

Copies the database named by HB_DB_ACCOUNT_02_PATH in .env into
data/homebudget-02/<yyyymmddhhmm>-homebudget.db with the SQLite backup interface,
reading the source read-only. The seed loads the newest snapshot, so a reload
reproduces the same database even while HomeBudget keeps syncing.

Usage: env/bin/python scripts/snapshot_homebudget_02.py
"""

from __future__ import annotations

import datetime as dt
import sqlite3
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OUT_DIR = REPO / "data" / "homebudget-02"


def read_env(name: str) -> str:
    for line in (REPO / ".env").read_text(encoding="utf-8").splitlines():
        if line.startswith(f"{name}="):
            return line.split("=", 1)[1].strip().strip('"')
    raise SystemExit(f"{name} is missing from .env")


def main() -> int:
    source_path = read_env("HB_DB_ACCOUNT_02_PATH")
    stamp = dt.datetime.now().strftime("%Y%m%d%H%M")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    target_path = OUT_DIR / f"{stamp}-homebudget.db"
    if target_path.exists():
        raise SystemExit(f"{target_path} already exists")

    source = sqlite3.connect(f"file:{source_path}?mode=ro", uri=True)
    target = sqlite3.connect(target_path)
    with target:
        source.backup(target)
    check = target.execute("PRAGMA integrity_check").fetchone()[0]
    counts = {
        table: target.execute(f"SELECT count(*) FROM {table}").fetchone()[0]
        for table in ("Account", "Expense", "Income", "Transfer")
    }
    source.close()
    target.close()

    if check != "ok":
        target_path.unlink()
        raise SystemExit(f"snapshot failed its integrity check: {check}")
    print(f"wrote {target_path}")
    print(f"counts {counts}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

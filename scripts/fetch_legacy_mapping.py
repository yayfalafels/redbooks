"""Fetch the legacy HomeBudget-to-statement mapping regions from the Google Sheets.

Reads, read-only, with the service account key named by GCP_CLIENT_SECRET_FILE in .env:
  homebudget workbook             cat_map             HB budget, category, subcategory -> legacy GL code
  financial statements workbook   fin_expense_cat_map legacy GL code -> statement line
  financial statements workbook   accounts            HB account -> asset subcategory

Workbook ids come from the file named by GSHEET_CONFIG_FILE in .env, default data/gsheets.json;
region ranges follow the financial-statements repo gsheet configs. The access pattern follows the
time-track-report-recover repo: a service account and the Sheets v4 client. Each region is written as JSON rows keyed by its
header to data/legacy-mapping/<region>.json, which stays out of git.

Usage: env/bin/python scripts/fetch_legacy_mapping.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

REPO = Path(__file__).resolve().parents[1]
OUT_DIR = REPO / "data" / "legacy-mapping"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
REGIONS = {
    "cat_map": ("homebudget", "cat_map!A1:J182"),
    "fin_expense_cat_map": ("financial statements", "fin_expense_cat_map!A1:E500"),
    "accounts": ("financial statements", "accounts!A1:G500"),
}
DEFAULTS = {"GCP_CLIENT_SECRET_FILE": ".credentials/gcp-iam-client-secret.json", "GSHEET_CONFIG_FILE": "data/gsheets.json"}


def read_env(name: str) -> str:
    env_file = REPO / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            if line.startswith(f"{name}="):
                return line.split("=", 1)[1].strip().strip('"')
    return DEFAULTS[name]


def workbook_ids() -> dict[str, str]:
    path = REPO / read_env("GSHEET_CONFIG_FILE")
    if not path.exists():
        raise SystemExit(f"gsheet config missing: {path}. Set GSHEET_CONFIG_FILE in .env.")
    return {entry["name"]: entry["workbook_id"] for entry in json.loads(path.read_text(encoding="utf-8"))}


def main() -> int:
    key_file = REPO / read_env("GCP_CLIENT_SECRET_FILE")
    if not key_file.exists():
        raise SystemExit(f"service account key missing: {key_file}. Set GCP_CLIENT_SECRET_FILE in .env.")
    credentials = Credentials.from_service_account_file(str(key_file), scopes=SCOPES)
    sheets = build("sheets", "v4", credentials=credentials, cache_discovery=False).spreadsheets()
    ids = workbook_ids()
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    for region, (workbook, cell_range) in REGIONS.items():
        try:
            values = sheets.values().get(spreadsheetId=ids[workbook], range=cell_range).execute().get("values", [])
        except HttpError as exc:
            if exc.resp.status == 403:
                raise SystemExit(f"{region}: access denied. Share the {workbook} workbook with the service account.")
            raise
        header, rows = values[0], values[1:]
        records = [dict(zip(header, row + [""] * (len(header) - len(row)))) for row in rows if any(c.strip() for c in row)]
        (OUT_DIR / f"{region}.json").write_text(json.dumps(records, indent=1), encoding="utf-8")
        print(f"{region}: {len(records)} rows, columns {header}")
    print(f"wrote {OUT_DIR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

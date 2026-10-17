# Statements

How the income statement, the balance sheet and other reports present signed books.

## Rules

01. the income statement covers a period, and the balance sheet stands at a date.
02. the books, the API and every oracle hold signed entries. The income statement shows expenses as positive amounts, and that flip is the last step of rendering the statement and its export.
03. a transfer never appears on the income statement.
04. each statement and its CSV export show the same figures under the same filters.

## Lessons

### count reports against stated populations

Fix the reporting rules before designing the report. Each report labels its population and its period, returns a count together with its denominator and rate, shows no rate for an empty denominator, and marks an incomplete current period. A report of events and a report of cohorts are labelled apart.

**why**: reports built before their population was stated mixed event counts with cohort counts and showed a partial week as a full one.

Example: an income statement for "1 Oct to 16 Oct, current month, incomplete" over "all accounts in SGD" shows Dining 412.30, and its CSV export holds the same 412.30.

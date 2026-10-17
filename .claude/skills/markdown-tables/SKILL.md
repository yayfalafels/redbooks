---
name: markdown-tables
description: Layout rules for markdown tables in *.md files, covering row length, fixed-width padding, the id column, notes for long cells, single-value columns, and line breaks. Use when generating, creating, editing or reviewing any markdown table.
---

# Markdown tables

These rules keep a table readable in a plain-text editor and in a rendered view.

## Rules

01. **no line continuation breaks.** Never break a line of prose or a table row across source lines. Line breaks belong only inside code snippets, where that language's style guide allows them.
02. **row length under 115 characters.** Keep every row, including the header and separator, under 115 characters.
03. **fixed-width columns.** Pad every cell so each column has one width in every row, and the separator row matches it.
04. **id column first.** The leftmost column holds the row id, such as `01` or `12.TC.04`.
05. **long text goes to notes.** A cell that would push a row past the limit moves to a numbered note below the table, which names the row by its id.
06. **drop single-value columns.** Remove a column that holds the same value in every row, and state the value once in the text above the table. This covers a table already grouped by that column, such as a section of cases that share one verification layer. Check every column for this before finishing a table.

## Examples

Correct:

```md
| id | seq | status  | milestone                   |
| -- | --- | ------- | --------------------------- |
| 01 | 01  | open    | scope requirements tasks    |
| 02 | 02  | pending | dev env setup database      |
| 03 | 03  | pending | dev env setup worker        |

02. **database setup** the container, the volume, the seed load and the health check, with the commands for each step.
```

Incorrect, with no id column, unpadded cells and a long cell inside the row:

```md
| status | milestone |
| - | - |
| open | scope requirements tasks |
| pending | dev env setup database, covering the container, the volume, the seed load, the health check and every command |
```

Incorrect, with a column that holds one value in every row:

```md
| id       | layer  | title                              |
| -------- | ------ | ---------------------------------- |
| 02.DB.01 | direct | schema build creates the schema    |
| 02.DB.02 | direct | amounts round-trip unchanged       |
```

Correct, with the shared value stated once above the table:

```md
Every case is decided by direct inspection.

| id       | title                              |
| -------- | ---------------------------------- |
| 02.DB.01 | schema build creates the schema    |
| 02.DB.02 | amounts round-trip unchanged       |
```

Incorrect, with a prose paragraph broken across source lines:

```md
The order service validates the request and checks that the customer
owns the cart before it reserves stock.
```

Correct line breaks inside a code snippet:

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"key": "value"}' \
  http://localhost:8000/api/orders
```

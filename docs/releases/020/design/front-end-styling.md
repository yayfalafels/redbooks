# RedBooks 0.2.0 - Front End Styling

This document sets the visual style of the RedBooks `0.2.0` web app: the design tokens for color, type, spacing and shape, the light theme, and how the app shell, lists, statement tables, forms and sheets look. It is a companion to design topic 04.03, the **front end pages**, which fixes what each page holds. This doc fixes how it looks. Each external reference template below carries a note on what to take from it.

## Contents

- [Summary](#summary)
- [References](#references)
- [Reference templates](#reference-templates)
- [Design tokens](#design-tokens)
  - [Color](#color)
  - [Typography](#typography)
  - [Spacing and shape](#spacing-and-shape)
- [Theme](#theme)
- [Component styling](#component-styling)
  - [App shell](#app-shell)
  - [Lists and tables](#lists-and-tables)
  - [Statement tables](#statement-tables)
  - [Amounts](#amounts)
  - [Forms](#forms)
  - [Sheets, dialogs and banners](#sheets-dialogs-and-banners)
- [Accessibility](#accessibility)
- [Implementation](#implementation)

## Summary

01. **a quiet ledger look.** Neutral surfaces, one accent color for actions, and dense, aligned tables. The numbers carry the page. Decoration stays out of the way.
02. **one color per meaning.** Indigo marks actions and the current tab, red marks destructive actions and errors, amber marks stale snapshot data, and green marks a saved status. A sign shows as a minus sign, never as a color alone, per item 10 of the **ui review lessons**.
03. **tokens drive every shared value.** Color, type, spacing, radius and shadow come from CSS custom properties in one tokens file. A component never hard-codes a shared value, per the **mobile layout** rules.
04. **one light theme.** The app ships a single light theme built on the Radix Colors light scales, whatever the device's color scheme setting.
05. **tabular figures everywhere an amount appears.** Every amount uses `font-variant-numeric: tabular-nums` and aligns right, so decimals line up down a column.
06. **phone first.** Designed at 375 pixels wide, centred at a 640 pixel column on desktop, with 44 pixel tap targets and 48 pixel rows on every list and statement table.
07. **plain CSS modules.** Styles live in one CSS module per component plus the shared tokens file. The app takes no component library.

## References

Internal:

- **front end pages**: [front-end-pages.md](front-end-pages.md)
- **financial statements design**: [financial-statements.md](financial-statements.md)
- **test strategy**: [test-strategy.md](test-strategy.md)
- **react skill**: [../../../../.claude/skills/react/SKILL.md](../../../../.claude/skills/react/SKILL.md)
- **mobile layout**: [../../../../.claude/skills/react/references/mobile-layout.md](../../../../.claude/skills/react/references/mobile-layout.md)
- **ui review lessons**: [../../../../.claude/skills/react/references/ui-review-lessons.md](../../../../.claude/skills/react/references/ui-review-lessons.md)

External reference templates:

- **actual budget**: [github.com/actualbudget/actual](https://github.com/actualbudget/actual)
- **actual vision**: [actualbudget.org/docs/vision](https://actualbudget.org/docs/vision/)
- **shadcn dashboard**: [ui.shadcn.com/examples/dashboard](https://ui.shadcn.com/examples/dashboard)
- **finance dashboard kit**: [thefrontkit.com/apps/finance-dashboard-kit](https://thefrontkit.com/apps/finance-dashboard-kit)
- **fundex**: [tailgrids.com/templates/fundex](https://tailgrids.com/templates/fundex)
- **untitled ui financial dashboard**: [untitledui.com/react/components/dashboards/dashboard-12](https://www.untitledui.com/react/components/dashboards/dashboard-12)

External guidelines:

- **carbon data table**: [carbondesignsystem.com/components/data-table/usage](https://carbondesignsystem.com/components/data-table/usage/)
- **carbon data table style**: [carbondesignsystem.com/components/data-table/style](https://carbondesignsystem.com/components/data-table/style)
- **govuk table**: [design-system.service.gov.uk/components/table](https://design-system.service.gov.uk/components/table)
- **eu table scannability**: [data.europa.eu data visualisation guide, table design](https://data.europa.eu/apps/data-visualisation-guide/table-design-scannability)
- **material navigation bar**: [m3.material.io/components/navigation-bar](https://m3.material.io/components/navigation-bar/overview)
- **material fab**: [m3.material.io/components/floating-action-button](https://m3.material.io/components/floating-action-button/overview)
- **radix colors scales**: [radix-ui.com/colors/docs/palette-composition/scales](https://www.radix-ui.com/colors/docs/palette-composition/scales)
- **radix colors composing**: [radix-ui.com/colors/docs/palette-composition/composing-a-palette](https://www.radix-ui.com/colors/docs/palette-composition/composing-a-palette)
- **wcag contrast**: [w3.org/WAI/WCAG22/Understanding/contrast-minimum](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html)

## Reference templates

Each row names a template or guideline to open and review, and the one thing RedBooks takes from it. RedBooks copies no code from these. They are visual and behavioural references only. Licenses vary, and the commercial templates are for looking at only.

| id    | reference                       | kind          | take from it                                       |
| ----- | ------------------------------- | ------------- | -------------------------------------------------- |
| RT.01 | actual budget                   | open source   | ledger density, account sidebar, amount alignment  |
| RT.02 | actual vision                   | principles    | clutter-free, touch layout on phone widths         |
| RT.03 | shadcn dashboard                | open source   | neutral palette, card and table restraint          |
| RT.04 | finance dashboard kit           | commercial    | screen set close to RedBooks, ledger and reports   |
| RT.05 | fundex                          | commercial    | transaction list rows, category chips              |
| RT.06 | untitled ui financial dashboard | component     | light surfaces, borders and accent use             |
| RT.07 | carbon data table               | design system | row heights, header style, zebra-free rows         |
| RT.08 | govuk table                     | design system | numeric cell modifier, right-aligned headers       |
| RT.09 | eu table scannability           | guideline     | right-align numbers, one rounding per column       |
| RT.10 | material navigation bar         | design system | tab bar with icon and label, active indicator pill |
| RT.11 | material fab                    | design system | add button size, placement and elevation           |
| RT.12 | radix colors scales             | color system  | 12-step scales and the role of each step           |

01. **RT.01** is the closest open source analogue: a personal ledger web app with accounts, transactions and reports. Run it locally with Docker to see its phone layout. RedBooks takes its table density and its right-aligned amounts, and leaves out its envelope budget grid.
02. **RT.03** shows the restraint RedBooks wants: a neutral background, thin borders in place of heavy shadows, and one accent. RedBooks takes the look and leaves out the Tailwind and Radix component stack.
03. **RT.04 and RT.05** are paid templates. Their public preview pages show a transaction ledger, account cards and reports, and are worth a look for row layout and the category chip style. They lean on charts and cards more than RedBooks will.
04. **RT.07 and RT.08** are the authority for table styling. RedBooks follows their header weight, cell padding and the numeric cell that right-aligns both the cell and its header.
05. **RT.10 and RT.11** fix the tab bar and the add button. RedBooks keeps four tabs of equal weight and one add button at the end of the bar, per item 03 of the app shell in the **front end pages**.

## Design tokens

Every token is a CSS custom property declared on `:root` in the tokens file.

### Color

The palette takes five Radix light scales: slate for neutrals, indigo for the accent, red for danger, amber for stale data and grass for success. Indigo keeps the accent clear of the red, amber and green meanings. A token names its role, and maps to a scale step per **radix colors scales**: steps 1 and 2 for backgrounds, 3 to 5 for component fills, 6 to 8 for borders, 9 and 10 for solid fills, and 11 and 12 for text.

| id    | token                  | scale step | meaning                               |
| ----- | ---------------------- | ---------- | ------------------------------------- |
| CL.01 | `--color-bg`           | slate 1    | page background                       |
| CL.02 | `--color-surface`      | white      | header, tab bar, cards, sheets        |
| CL.03 | `--color-surface-alt`  | slate 2    | group headings, table header row      |
| CL.04 | `--color-row-hover`    | slate 3    | row hover and pressed state           |
| CL.05 | `--color-border`       | slate 6    | row dividers, field borders           |
| CL.06 | `--color-text`         | slate 12   | body text and amounts                 |
| CL.07 | `--color-text-muted`   | slate 11   | labels, captions, currency codes      |
| CL.08 | `--color-accent`       | indigo 9   | primary buttons, add button, tab pill |
| CL.09 | `--color-accent-text`  | indigo 11  | links, current tab label              |
| CL.10 | `--color-danger`       | red 9      | destructive confirm button            |
| CL.11 | `--color-danger-text`  | red 11     | field errors, error banners           |
| CL.12 | `--color-stale`        | amber 9    | stale dot on a statement line         |
| CL.13 | `--color-stale-bg`     | amber 3    | stale banner background               |
| CL.14 | `--color-success-text` | grass 11   | saved status beside a control         |
| CL.15 | `--color-focus`        | indigo 8   | focus ring                            |

01. **no sign colors.** A negative amount shows a minus sign in `--color-text`. Red stays reserved for danger, so a liability balance never reads as an error.
02. **the brand red stays in the wordmark.** The RedBooks name on PG.01 may use red 9. Nothing else uses red outside CL.10 and CL.11.

### Typography

The app uses the system font stack: `system-ui, -apple-system, "Segoe UI", Roboto, sans-serif`. It loads no web font, so the first paint shows real text. Every amount, rate and date column sets `font-variant-numeric: tabular-nums`.

| id    | token               | size | line | weight | used for                                  |
| ----- | ------------------- | ---- | ---- | ------ | ----------------------------------------- |
| TY.01 | `--text-caption`    | 12   | 16   | 400    | stale line second row, table footnotes    |
| TY.02 | `--text-small`      | 14   | 20   | 400    | table cells, field labels, list secondary |
| TY.03 | `--text-body`       | 16   | 24   | 400    | list primary text, field values           |
| TY.04 | `--text-heading`    | 16   | 24   | 600    | group headings, statement section titles  |
| TY.05 | `--text-title`      | 20   | 28   | 600    | page title in the header                  |
| TY.06 | `--text-amount-lg`  | 28   | 36   | 600    | balance on an account detail page         |

Sizes and line heights are in pixels and set in `rem` against a 16 pixel root, so the browser text size setting scales them. Inputs stay at 16 pixels, which stops iOS from zooming on focus.

### Spacing and shape

| id    | token            | value | used for                                       |
| ----- | ---------------- | ----- | ---------------------------------------------- |
| SP.01 | `--space-1`      | 4     | icon to label gap                              |
| SP.02 | `--space-2`      | 8     | cell padding, chip padding                     |
| SP.03 | `--space-3`      | 12    | row vertical padding, field gap                |
| SP.04 | `--space-4`      | 16    | page side gutter, card padding                 |
| SP.05 | `--space-6`      | 24    | gap between page sections                      |
| SP.06 | `--space-8`      | 32    | gap above a group heading                      |
| SP.07 | `--radius-sm`    | 6     | fields, chips, buttons                         |
| SP.08 | `--radius-lg`    | 16    | sheet top corners, dialogs                     |
| SP.09 | `--radius-full`  | 9999  | add button, tab indicator pill, stale dot      |
| SP.10 | `--shadow-float` | n/a   | add button and open sheet only                 |

Values are in pixels. Lists and tables use borders, never shadows. `--shadow-float` is `0 4px 12px` at 16 percent black.

## Theme

01. **light only.** The app ships one light theme and has no theme switch. The root sets `color-scheme: light`, so a device in dark mode still renders the light form controls and scrollbars.
02. **meta theme color.** The `theme-color` meta tag carries `--color-surface`, so the phone status bar matches the header.

## Component styling

### App shell

01. **header**: 56 pixels, `--color-surface` with a one pixel `--color-border` bottom edge. The title uses TY.05 and truncates with an ellipsis. The back arrow and the initials button are 44 pixel squares.
02. **tab bar**: 64 pixels plus the bottom safe area inset, `--color-surface` with a top border. Each tab is an icon over a TY.01 label. The current tab sets its icon on a `--color-accent` pill at 12 percent opacity, and its label in `--color-accent-text`, per **material navigation bar**.
03. **add button**: a 56 pixel circle in `--color-accent` with a white plus icon and `--shadow-float`. It sits 16 pixels above the tab bar and 16 pixels from the column's right edge.
04. **content column**: `--color-bg`, 16 pixel side gutters, at most 640 pixels wide and centred. On desktop, the space outside the column is `--color-surface-alt`.

### Lists and tables

The list pages show their rows as a table with aligned columns, per item 02 of the **ui review lessons**.

01. **rows**: at least 48 pixels tall, TY.03 primary text over TY.02 muted secondary text, with a one pixel `--color-border` divider between rows. No zebra stripes.
02. **header row**: TY.02 at weight 600 in `--color-text-muted` on `--color-surface-alt`. A numeric column header aligns right with its cells, per **govuk table**.
03. **group headings**: TY.04 on `--color-surface-alt`, sticky under the page header, with the group subtotal right-aligned on the same line.
04. **long names**: wrap to two lines, then truncate with an ellipsis. The amount column never wraps.
05. **retired rows**: `--color-text-muted` text with a "Retired" chip.

### Statement tables

Statement views follow the line layout of the **financial statements design**. The styling adds:

01. **rows**: at least 48 pixels tall, the same as the list rows, so every statement line is a full tap target.
02. **indentation**: each level of the line hierarchy indents 12 pixels. Section totals use weight 600 with a one pixel top border, and the net line uses a two pixel top border.
03. **year views**: the line label column is sticky at the left with a 160 pixel width and a right shadow when content scrolls under it. Month columns are 88 pixels wide. The table scrolls sideways inside its own container. The page never does.
04. **stale lines**: the stale dot is an 8 pixel `--color-stale` circle before the amount. The second row uses TY.01 in `--color-text-muted`.
05. **source banner**: UC.11 sits on `--color-surface-alt`. A stale snapshot switches it to `--color-stale-bg` with the two actions as text buttons.

### Amounts

01. **alignment**: right-aligned, tabular figures, no wrap.
02. **currency code**: TY.01 in `--color-text-muted` after the amount, shown only where more than one currency is on screen, per UC.01 of the **front end pages**.
03. **large balance**: the account detail balance uses TY.06.

### Forms

01. **fields**: a label above each field in TY.02 `--color-text-muted`, a 48 pixel input with a `--color-border` border and `--radius-sm`. Focus shows a two pixel `--color-focus` ring.
02. **errors**: a red border in `--color-danger-text` and the message under the field in TY.02 `--color-danger-text`, with an icon so the error does not rely on color alone.
03. **buttons**: primary is a solid `--color-accent` fill with white text. Secondary is a `--color-border` outline. Destructive is a solid `--color-danger` fill. All are 44 pixels tall. On a detail page the primary actions sit at the top, per item 03 of the **ui review lessons**.
04. **saved status**: a check icon and "Saved" in `--color-success-text` beside the save button, per item 09 of the **ui review lessons**.

### Sheets, dialogs and banners

01. **bottom sheet**: `--color-surface`, `--radius-lg` top corners, a 4 by 32 pixel grab handle, and a 40 percent black scrim behind it. The add sheet rows are 56 pixels tall with a 24 pixel icon.
02. **dialog**: centred, at most 320 pixels wide, `--radius-lg`. The confirm button sits at the right. A destructive confirm uses the destructive button.
03. **error banner**: under the header, `--color-danger-text` text on red 3, with a retry text button.
04. **skeleton**: rows of `--color-surface-alt` bars at the row heights above, with a slow shimmer that stops under `prefers-reduced-motion`.

## Accessibility

01. **contrast**: text meets WCAG AA, 4.5 to 1 for body text and 3 to 1 for large text and icons, per **wcag contrast**. Radix steps 11 and 12 on steps 1 and 2 meet this.
02. **not color alone**: stale data carries a dot and a second row, errors carry an icon and a message, and the current tab carries the pill and the label weight.
03. **focus**: every focusable control shows the CL.15 ring under `:focus-visible`.
04. **motion**: transitions last at most 200 milliseconds and stop under `prefers-reduced-motion`.

## Implementation

01. **tokens file**: `frontend/src/styles/tokens.css` declares every token in this doc, and imports the Radix light scales from the `@radix-ui/colors` package.
02. **base file**: `frontend/src/styles/base.css` sets the root font size, the font stack, the body background and the reset. It is the only global stylesheet besides the tokens.
03. **component modules**: each component has its own `*.module.css` that reads tokens only, per the **mobile layout** rules.
04. **layout tests**: the Playwright page tests run at 375 and 1280 pixels, with the 40 character account name and the 60 character payee from the fixtures, per the **test strategy**.

> **implementation decision**: plain CSS modules over a component library such as shadcn/ui or Material UI. The app has fourteen shared components and a fixed phone layout, the react skill already scopes styles per component, and a library would add a build dependency and a second styling vocabulary for little gain. Tech stack topic 04.11 confirms the frontend build tooling.


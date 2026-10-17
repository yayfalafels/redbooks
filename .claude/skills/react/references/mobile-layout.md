# Mobile layout

How pages are laid out for a phone first and kept from breaking each other.

## Rules

01. design at 375 pixels wide first, then widen.
02. touch targets are at least 44 pixels high.
03. long names truncate with an ellipsis or wrap inside their cell. A page never scrolls sideways.
04. amounts align right in a fixed-width or tabular-figure font.

## Lessons

### scope styles to their component and test layouts at both widths

Each style rule targets one component, through a CSS module or a component class. A shared rule changes only through the design tokens. Layout tests run at phone and desktop width with realistic text lengths.

**why**: one feature changed a shared table rule to fit a 375 pixel width and silently broke another feature's one-line rows. Nothing caught it, because the seeded text was short. The first fix, on the shared class, broke a third page.

Example:

```tsx
import styles from "./EntryList.module.css";
<table className={styles.entries}>...</table>
```

Seed and fixture names include a 40-character account name and a 60-character payee, and the page test runs at 375 and 1280 pixels.

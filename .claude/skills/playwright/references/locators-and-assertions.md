# Locators and assertions

How to find elements and wait for them without fixed sleeps.

## Rules

01. prefer `get_by_role`, `get_by_label` and `get_by_test_id`. Avoid positional CSS and generated class names.
02. a locator resolves to one element. Narrow it with a parent or `filter` when it matches several.
03. set a per-call `timeout` where a wait differs from the default, so a slow page and a missing element fail differently.

## Lessons

### wait on web-first assertions and assert bound values

Wait with retrying `expect` assertions, which tolerate an element that is briefly absent. Wait for completion signals, such as an image's `complete` property or a loading indicator leaving. Resolve each locator to one element. Assert attributes or bound values, such as `disabled` or an input's value, in preference to rendered labels.

**why**: a test read a property of an element that was briefly absent. Another measured an image before it loaded, only under full-suite load. Two waited on a locator that matched several elements, and three compared text that CSS rendered in upper case.

Example:

```python
from playwright.sync_api import expect

expect(page.get_by_test_id("entry-list-loading")).to_have_count(0)
expect(page.get_by_role("button", name="Save")).to_be_disabled()
expect(page.get_by_label("Amount")).to_have_value("12.50")
page.wait_for_function("img => img.complete", arg=page.get_by_role("img", name="Receipt").element_handle())
```

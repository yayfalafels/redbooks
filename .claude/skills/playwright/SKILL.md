---
name: playwright
description: Playwright for Python browser testing of a single-page app, covering headless Chromium at phone width, one browser fixture, web-first assertions, resilient locators, network mocking from captured responses, latency budgets, and screenshots and traces on failure. Use when writing, running, reviewing or triaging any Playwright test or page fixture.
---

# Playwright

Practice for Playwright tests, Python sync API with `pytest-playwright`, that drive a single-page app in a browser.

## Rules

01. **headless Chromium at phone width.** Run headless Chromium in a phone viewport by default, through one browser fixture for the suite.
02. **web-first waits and bound values.** Wait with web-first assertions that tolerate absent elements and wait for completion signals. Assert attributes or bound values in preference to rendered labels. Never use a fixed sleep.
03. **canned API responses in silo tests.** Frontend silo tests answer API calls from canned responses captured from real responses.
04. **latency budgets.** Every test has a latency budget. A timeout seen only in the full run is reproduced by injected latency before it is closed.
05. **evidence on failure.** A failing test saves a screenshot and a trace.

## References

| id | file                                    | read it when                                         |
| -- | --------------------------------------- | ---------------------------------------------------- |
| 01 | `references/locators-and-assertions.md` | choosing a locator, a wait or an assertion           |
| 02 | `references/network-mocking.md`         | mocking an API call in a frontend silo test          |
| 03 | `references/flaky-test-triage.md`       | a test times out or fails only in the full run       |
| 04 | `references/mobile-viewport.md`         | setting up the browser, viewport or failure evidence |
| 05 | `references/open-lessons.md`            | a task touches one of the listed areas               |

## Related skills

- [pytest](../pytest/SKILL.md) for fixtures, budgets and triage.
- [react](../react/SKILL.md) for the pages under test.

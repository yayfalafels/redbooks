# Open lessons

Lessons to be learned for Python practice. Each is unsettled. Observe it, record what happens as `lesson observation LT.NN` in the tracker's Validate section, and present it as a hypothesis, never as a rule.

## LT.03 check that every process runs in the mode the env file selects

**status**: experimenting

**question**: do a startup log line with the effective mode, and a test that the app, a script and the test fixtures build identical settings from one `.env`, catch a mode split before it reaches a run?

**evidence that settles it**: after a mode change in `.env`, every process reports the new mode, and a planted override in one process fails the test.

**experiment**: add the log line and the test with the local dev environment, change the mode in `.env` once, and confirm every process follows it.

## LT.08 probe the exchange rate source before design

**status**: experimenting

**question**: how does the exchange rate API handle weekends, missing dates, rate limits and historical ranges?

**evidence that settles it**: saved probe responses for each case, turned into fixtures.

**experiment**: a tracked probe script, run by the user, that requests each case and saves the raw responses and a findings file.

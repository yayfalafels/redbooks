# Open lessons

Lessons to be learned for browser test practice. Each is unsettled. Observe it, record what happens as `lesson observation LT.NN` in the tracker's Validate section, and present it as a hypothesis, never as a rule.

## LT.02 replace variance closes with latency injection

**status**: experimenting

**question**: does delaying a route reproduce a full-run-only timeout deterministically?

**evidence that settles it**: for each full-run-only failure, a delayed-route test that fails the same way every run, and passes once the fix lands.

**experiment**: for every full-run-only failure, add a delayed-route reproduction before any close. The latency budgets decide when a test fails.

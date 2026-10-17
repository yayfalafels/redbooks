# Open lessons

Lessons to be learned for test practice. Each is unsettled. Observe it, record what happens as `lesson observation LT.NN` in the tracker's Validate section, and present it as a hypothesis, never as a rule.

## LT.01 generate more cross-cutting tests from the route table

**status**: experimenting

**question**: does generating the per-endpoint error tests and the vocabulary coverage from the route table, as the ownership matrix is generated, catch defects that hand-written cases miss?

**evidence that settles it**: a count of defects the generated tests catch that no hand-written case caught, over the first API features.

**experiment**: generate both from the route table in the first API milestone, and record each defect with the test that caught it.

## LT.05 prove the real seed data stays private

**status**: open

**question**: which paths can carry real seed data out of its uncommitted storage location, such as committed logs, test output, fixture files, screenshots, traces and the docs build?

**evidence that settles it**: one closure check per path, each shown to fail on a planted real value.

**experiment**: list the paths during the data review, and turn each into a check.

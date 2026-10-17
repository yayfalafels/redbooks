# Open lessons

Lessons to be learned for schema practice. Each is unsettled. Observe it, record what happens as `lesson observation LT.NN` in the tracker's Validate section, and present it as a hypothesis, never as a rule.

## LT.06 test whether migrations catch the version drift class

**status**: experimenting

**question**: do Alembic revisions with a startup head check catch a schema and version marker that drift apart, without a human noticing?

**evidence that settles it**: a deliberately skipped migration step fails a check before any test or run reads the database.

**experiment**: when the project adopts forward migrations, skip one step on purpose and confirm the startup head check fails.

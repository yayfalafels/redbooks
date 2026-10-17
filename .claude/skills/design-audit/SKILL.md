---
name: design-audit
description: Audits one release's design document set, such as requirements, workflows, data model, architecture, UI and test strategy, for internal consistency, current best practice, implementation risk, and requirements-to-design traceability. Use when asked to review, audit, critique or sanity-check a release's design docs. For implementation code, use a code review.
---

# Design audit

The scope is one release: every design and planning document for that release, plus the release roadmap for cross-release context. The audit tests what the documents claim and whether those claims hold together. The code may not exist yet.

## Rules

01. **read every document in full.** Inconsistencies and dangling cross-references live in details a partial read misses. Note each document's decision id prefix, such as `REQ-` or `ARCH-`, and the place in the hierarchy it states for itself.
02. **check the four questions across the whole set.** Most real findings are cross-document: a requirement contradicted three docs later, or one decision made twice in incompatible ways.
03. **verify best practice externally.** Search for the specific technology or pattern a doc names, and cite the source in the finding. A generic "consider X" with no evidence that X applies is left out.
04. **cross-check status against content.** A tracker that marks a document pending while the document is complete and cited as settled is a finding.
05. **report only real findings.** A doc set with solid traceability gets a short report.

## The four audit questions

01. **internal consistency.** Do the explicit statements and implied assumptions agree? Look for one concept named or scoped differently in two docs, a decision settled in one doc and open or contradicted in another, and a broad requirement that collides with a specific rule for the same data.
02. **design best practice.** For each domain the set touches, such as data modelling, API design, frontend framework, storage, security and testing, how does the design compare with current practice? A deliberate, justified deviation is a finding only where its trade-off is unstated or current evidence undercuts it.
03. **implementation risk.** What, built exactly as written, is likely to cause a concrete problem? Examples are an implied race condition, a performance budget another section's numbers exceed, a closed vocabulary with no seed or test coverage, and a manual step with no fallback. Name the mechanism.
04. **hierarchy and traceability.** Requirements lead to workflows and the data model, which lead to architecture, UI and test strategy, and each layer cites what it operationalises. Check both directions: every requirement has downstream coverage, and every downstream decision cites something upstream. Check that the documented build order matches the dependency order the cross-references show.

## Output

Write the findings to `docs/releases/<release>/<release>-design-audit.md`, following the **documentation-style** rules for prose and the **markdown-tables** rules for the summary table.

01. near the top, introduce each document in scope once by a bold, readable, linked alias, such as **architecture**, and use the alias in every finding.
02. a summary table with the columns `id | severity | category | title`, one row per finding, most severe first. Ids take the form `<release>.DA.NN`.
03. severity is one of **critical**, a design that contradicts itself or cannot be built, **high**, a defect a team would hit early and pay to unwind, **medium**, a contained defect or an evidenced best practice gap, and **low**, worth recording.
04. category is one of `internal consistency`, `best practice`, `implementation risk` and `traceability`.
05. below the table, one `### <id> <title>` section per finding. It opens with a `**docs**` line naming the affected documents by alias, then states what is wrong and where, why it matters, and a suggested resolution or a question for the owning role.

## Related skills

- [documentation-style](../documentation-style/SKILL.md) for prose and line rules.
- [markdown-tables](../markdown-tables/SKILL.md) for the summary table.

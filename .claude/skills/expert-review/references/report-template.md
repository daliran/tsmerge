# Report template

The aggregator writes `report.md` in this shape.

```markdown
# Expert review — <scope>

- **Date:** YYYY-MM-DD
- **Commit:** <hash and subject, with "uncommitted changes" if any>
- **Roles:** <the roles that ran>

## Summary

<three to five sentences: the overall state, and the most important things to act on>

| Severity | Confirmed | Dropped |
|---|---|---|
| Critical | n | n |
| High | n | n |
| Medium | n | n |
| Low | n | n |

## Critical

### C1 · <short title>

- **Raised by:** <role ids, e.g. HPC-02, REP-01>
- **Location:** `path:line`
- **Evidence:** "<quote>"

**Problem:** …

**Why it matters:** …

**Suggestion:** …

## High

### H1 · …

## Medium

### M1 · …

## Low

- **L1 · <short title>** · `path:line` · raised by <ids> · <one-line suggestion>

## Proposed checks (need your approval)

Checks a reviewer couldn't run because they need the cluster, a long run or a network service. Nothing here was run.

| Check | Proposed by | What it would show | Command |
|---|---|---|---|

## Repository hygiene

<the issues in checks/hygiene.md, or "none">

## Dropped findings

| Finding | Reason |
|---|---|

## Unverified notes

<items from the reviewers' "Also noticed" lists, not verified: one line each>
```

Rules:

- Item ids in the report (`C1`, `H1`, `M1`, `L1`) are local to the report; each lists the reviewer ids it merges.
- Low items are one line each.
- Empty sections say "none" rather than disappear, so a reader can tell "nothing found" from "not checked".

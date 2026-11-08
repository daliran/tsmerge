# Finding format

Each reviewer writes one Markdown file, `roles/<role>.md`, in this shape:

```markdown
# <Role name>

**Scope:** <what was read>

**Commands run:** <the local checks run, or "none">

**Summary:** <one or two sentences: the role's overall view>

## <ID>-01 · <short title>

- **Severity:** Critical | High | Medium | Low
- **Confidence:** High | Medium | Low
- **Type:** Bug | Risk | Gap | Inconsistency | Reproducibility | Design | Clarity
- **Location:** `path:line`
- **Evidence:** "one line copied exactly from the file at that location"

**Problem:** what is wrong or missing, in one or two sentences.

**Why it matters:** the consequence, from this role's point of view.

**Suggestion:** the fix, or the question to ask. Never an invented fact presented as true.

## Proposed checks

- <a check that would need the cluster, a long run or a network service>: what it would show, the exact command

## Also noticed

- Medium · <short title> · `path:line`
```

## Ids

| Role | Prefix |
|---|---|
| `python-expert` | `PY` |
| `ml-engineer` | `ML` |
| `hpc-engineer` | `HPC` |
| `reproducibility` | `REP` |
| `researcher` | `RES` |
| `methodology` | `MET` |
| `timeseries` | `TS` |
| `merging` | `MRG` |

## Evidence

- **Location** is a path relative to the repository root and a line number: `scripts/cluster/submit.sh:42`. A problem in several places lists every location, separated by commas; the evidence quotes the first.
- **Evidence** is **one line copied exactly** from the file at the first location, between double quotes. Shorten a long line with `…` at either end, never in the middle. A script checks every quote against the file: a finding whose quote isn't there is reported as unverified.
- A missing thing ("there is no …") cites where it should be, and quotes the nearest line.

## Severity

| Severity | Meaning |
|---|---|
| **Critical** | Silently wrong results, lost results or data, a broken core workflow, a breach of the cluster's rules, or personal data or a secret in a committed file. Must be fixed before relying on the setup |
| **High** | Likely to fail in normal use, or a hole that makes results untraceable or not reproducible. Costly to fix later |
| **Medium** | Fails in an edge case, or a weakness with a reasonable workaround. Should be fixed |
| **Low** | Style, clarity, naming, a minor convention slip. Nothing breaks |

## Rules

- **Critical and High are never capped.** Report every one, in full.
- **Medium and Low share the cap** (default 15), the most important first. Fewer is fine; none is fine.
- **Nothing over the cap is dropped silently:** list each extra Medium or Low in **Also noticed**, one line each.
- One problem per finding. A problem seen in many places is one finding listing every location.
- Don't report what an accepted decision (`ED-NNNN`) deliberately chose, or what is already an open question (`EQ-NNNN`), unless the files contradict it or you bring new evidence. Then say which decision or question, and what is new.
- **Proposed checks** are for anything you couldn't verify without the cluster, a long run or a network service. You never run those yourself.

# Worked rulings, approval gates, and handoffs

## Worked standalone owner question

Suppose a project's reporting docs do not define how missing measurements render,
and `#43 — define how unavailable measurements appear in reports` must settle
that rule before consumer changes run.

**General rule:** should an unavailable measurement remain `null` and render as
an explicit unknown, or coerce to numeric zero? Current report docs do not specify
missing-measurement behavior.

**Worked application:** for stored input `{"duration_seconds": null}`, current
output renders `Duration: 0 s`. Under Option A, stored data stays `null` and
output renders `Duration: unknown`. Under Option B, both storage and output use
`0` (`Duration: 0 s`).

**Common practice:** keep unavailable measurements `null` and render an explicit
unknown so readers never confuse missing data with a measured zero. Coercing to
zero simplifies downstream sums at the cost of hiding missing data.

**Single-select question:** which rule should reports use for unavailable
measurements?

- **A — Preserve `null` and display `unknown` (recommended).** Keeps missing
  measurements distinguishable from a measured zero. Cost: summary totals must
  skip or flag `null` entries explicitly.
- **B — Store and display `0`.** Simplifies numeric aggregation. Cost: readers
  cannot tell whether `0 s` was measured or missing.

An implementation detail—such as which module formats the string—stays inside the
working session and is never escalated.

## Live-operation approval matrix

| Operation | Required before execution |
| --- | --- |
| Land an approved PR | Repository review and check gates pass |
| Deploy a specific build | Explicit owner approval for that deployment |
| Create or move a tag/release | Explicit owner approval for that release |
| Upload to a package index | Explicit owner approval for that upload |
| Install into a live host/service | Explicit owner approval for that installation |
| Reset or rewrite live state | Explicit owner approval for that operation |

For example, authorization to publish `agrein v0.1.0` covers that named release
once gates pass; it does not cover `v0.1.1`, a package-index upload, or local
host installation. Preserve authorization already granted in the current session
without asking again.

## Handoff shapes

When all work in scope is complete and no owner decision remains, omit empty
decision sections:

```markdown
### 1. What I did
`#42 — isolate ticket scratch directories by issue number` now writes check logs
and temporary state under `/var/tmp/agrein-42-scratch/`. Merged in PR #44
(`a1b2c3d`) after `./scripts/check` passed.

### 2. What is open
None.
```

When a live-operation gate or product ruling remains open, include all four
sections so the owner can act directly on §§3–4 without reconstructing context
from §1.

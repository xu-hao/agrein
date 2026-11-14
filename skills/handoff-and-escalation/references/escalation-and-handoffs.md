# Escalation and handoffs

## A complete owner question

Suppose the project has no rule for displaying unavailable measurements.
`#43 — define how unavailable measurements appear in reports` needs a product
ruling before its rendering child can run.

**General rule:** should a missing measurement appear as an explicit unknown or
as a numeric zero? The current report contract does not define missing values.

**Worked application:** the stored input is `{"duration_seconds": null}`.
Before the change, the rendered line is `Duration: 0 s`. Under option A the stored
value remains `null` and the rendered line becomes `Duration: unknown`. Under
option B the stored value becomes `0` and the rendered line stays `Duration: 0 s`.

**Common practice:** preserve an unavailable measurement as null and display an
explicit unknown so readers can distinguish it from a measured zero. Choosing
zero simplifies arithmetic but loses that distinction.

**Single-select question:** which missing-measurement rule should reports use?

- **A — Preserve null and show unknown (recommended).** Retains the distinction
  between unavailable data and a measured zero.
- **B — Store and display zero.** Treats unavailable measurements as zero throughout
  storage and reporting.

This is one product rule with two observable outcomes. An engineering choice such
as where to put a formatter should be resolved in the working session. If the
canonical report contract already requires option A, implement it without asking
this question. On a new ruling, update the canonical contract immediately, link
the ticket, and release dependent work only after that contract is settled.

## Approval transitions

| Operation | Required evidence before execution |
| --- | --- |
| Land an approved PR | Repository review and validation gates pass |
| Deploy a specific build | Explicit owner approval for that deployment |
| Create a tag/release | Explicit owner approval for that release |
| Upload to a package index | Explicit owner approval for that upload |
| Install into a host/service | Explicit owner approval for that installation |
| Reset live state | Explicit owner approval for that reset |

For example, approval to publish `agrein v0.1.0` covers that named release when
its gates pass; it does not cover `v0.1.1`, a deployment, or a package-index upload.
Preserve already granted authorization across the exchange and do not ask again
for the same operation. If an operation changes scope, obtain the missing scope's
approval. Prepare artifacts and validation first so approval concerns a concrete
result.

## A finished change handoff

### 1. What I did

`#42 — isolate ticket scratch directories by issue number` now uses
`/var/tmp/agrein-42-scratch/` instead of a shared scratch directory. The PR merged
after the behavioral isolation check passed; include the actual PR and commit.

### 2. What is open

None.

### 3. Decisions needed

None.

### 4. Options and recommendation

No further action is needed for this ticket.

For an infrastructure outage, instead describe the exact failing operation,
bounded retries already attempted, ticket-scoped evidence, preserved state, and
the condition that permits resumption. A parked ticket remains open. Do not turn
an unavailable service into an implementation success or repeatedly ask the owner
to resolve an engineering investigation.

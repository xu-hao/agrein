---
name: ticket-and-epic
description: >-
  Use before changing code, documentation, infrastructure, or live state to track
  work in GitHub issues and native epics, isolate each ticket in a worktree, and
  coordinate decision-free subtickets with dedicated workers. Also use when
  investigating bugs, planning an epic queue, or landing contributor changes.
---

# Ticket and epic

Apply this workflow in the repository being changed. Explicit owner instructions
and established project contracts take precedence. Read the project's canonical
contributor rules and inspect current tickets before creating duplicates.

## Establish the tracked contract

1. Create a GitHub issue **before** changing code, documentation, infrastructure,
   or live state. Read-only analysis, ticket maintenance, and workstation setup
   need no ticket. Cite tickets as `#N — one sentence describing the actual work`.
2. Every non-epic ticket belongs to one owning epic **at creation**. Use GitHub's
   native parent/sub-issue relationship, not a Markdown checklist as a substitute.
   Find or create the owning epic first; create the child and attach it immediately
   as one creation workflow, before execution. Verify the relationship. If an
   atomic create-and-parent operation is available, prefer it. A new repository
   can use its initial bootstrap issue as the epic itself; never self-parent it.
3. Investigate the **full epic queue upfront**: current behavior, contracts,
   dependencies, acceptance criteria, and unsettled product or policy questions.
   Batch those questions for the owner using
   [handoff-and-escalation](../handoff-and-escalation/SKILL.md) before autonomous
   execution. Do not repeatedly discover predictable questions one child at a time.
4. Name the general problem class and survey established solutions before choosing
   an approach. Record the applicable contract, options, evidence, and acceptance
   behavior in the ticket. Resolve engineering forks within the working session.
5. For a suspected bug, measure and reproduce it first. Confirm it with a failing
   **behavioral test before changing production code**. Keep that test as a
   regression check. An unconfirmed symptom is an investigation, not permission
   to guess at a fix.

## Isolate and execute

Develop, test, and commit only in a dedicated per-ticket worktree branched from
`main`; keep the primary checkout read-only during development. Use ticket-scoped
names for the branch, external virtual environment, logs, temporary payloads, and
scratch files so concurrent workers cannot overwrite one another. Follow the
[delegation and worktree reference](references/delegation-and-worktrees.md) for
concrete setup, native GitHub relationships, and worker ownership.

Spawn one dedicated subagent worker per subticket. Give it its ticket, owning epic,
settled contract, dependencies, acceptance checks, and authorization limits. That
worker manages its own ticket, PR, checks, landing, and cleanup directly; the
coordinator manages the epic queue rather than becoming a publication bottleneck.
An already assigned leaf worker executes directly without recursively delegating
its same ticket. If native subagents are unavailable, report the capability gap
and settle an execution plan instead of claiming delegation occurred.

Parallelize only fully specified, decision-free subtickets with independent
dependencies and worktrees. Run ruling-bearing or uncertain tickets sequentially
in the foreground, resolve their outcomes, and only then dispatch dependent work.
Independent files alone do not establish decision independence.

Keep internal contracts strict: fix a producer that emits invalid internal data
instead of adding speculative fallback coercions at every consumer. Reserve
tolerance for user input, LLM output, and external APIs; validate and normalize it
at those boundaries. Build the working path, a bounded retry policy, and an
infrastructure-incident parking path together. On an infrastructure incident,
preserve evidence and resumable state, report the blocker, and park the ticket
without pretending the feature passed or spinning indefinitely.

## Verify and land

Test observable behavior and acceptance criteria, including relevant failure
paths. Avoid tests that grep prose or source text to claim workflow correctness.
Run the repository's prescribed gates and review the actual diff. Put `Closes #N`
in the PR body or accepted commit message to close the implemented ticket on merge.

Land approved PRs once repository gates pass. Separate approval is required for
deployments, releases, package-index uploads, host/service installations, and state
resets; follow the companion skill's operation gates. Explicit approval already
given for the specific operation in this session remains valid.

After landing, verify the merged commit and ticket closure, remove the merged
ticket worktree and branch, and remove its external environment and scratch
artifacts. End changed-state exchanges with the companion skill's four-section
handoff, including any parked work or unverified behavior.

---
name: epic-queue
description: >-
  Use when decomposing multi-ticket work, managing a GitHub epic queue, wiring
  native GitHub parent and sub-issue relationships, deriving an explicit
  dependency DAG, clustering bug bursts by root cause before dispatch, or
  coordinating subagent workers across ready frontier tickets.
---

# Epic queue

Use when coordinating multi-ticket work or when a repository requires every
non-epic ticket to belong to a parent epic.

## Wire native GitHub sub-issues

1. Organize multi-ticket work under one owning epic with GitHub's native
   parent/sub-issue relationship, not a Markdown checklist alone.
2. Find or create the owning epic first, then create and attach each child
   immediately before execution using its numeric database `.id` (not its visible
   `#N`). Verify the relationship on GitHub before dispatch; see
   [native GitHub sub-issues](references/github-sub-issues.md).
3. Never self-parent an epic or silently move an issue from another owning epic.
   Repair or park broken parenting before implementation starts.

## Derive the dependency DAG upfront

1. Read the whole epic—current behavior, contracts, prerequisites, and acceptance
   criteria—before autonomous child execution starts.
2. Build explicit DAG edges from actual contract, code, and state prerequisites;
   narrative `A -> B -> C` lists and checkpoint order are not sequential blockers.
3. Separate **hard dependencies** (unsettled upstream contracts or overlapping
   behavioral rewrites of one seam) from **soft shared-file overlaps** (shared
   index, schema, or registry files whose disjoint sections Git or an ordinary
   target merge reconciles). Separate files do not make tickets
   decision-independent, and one shared registry file alone does not create a
   blocking edge.
4. Batch predictable product or policy questions for the owner upfront through
   [owner-escalation](../owner-escalation/SKILL.md) instead of discovering them
   one child ticket at a time.

## Cluster bug bursts before dispatch

When several bug or regression tickets arrive together, run the bounded signature
and code-path cause check in [bug-investigation](../bug-investigation/SKILL.md)
before fanning out workers. Group shared-cause symptoms under one root-cause
ticket whose fix closes them, link recurrences to the original fix, and dispatch
only distinct causes in parallel—never parallel symptom patches that collide on
the merge queue.

## Schedule the ready DAG frontier and upfront probes

1. Decouple read-only probes from upstream merges: run a downstream ticket's
   read-only feasibility probe or canonical-contract derivation that depends only
   on `main` and existing docs or SDKs upfront, in parallel with upstream code
   branches, so owner rulings surface early.
2. Serialize **only** owner escalations (unsettled product or policy rulings, run
   sequentially in the foreground) and dependent code builds whose upstream
   contract or code prerequisites have not landed on `main`.
3. Dispatch **every ready frontier node** in parallel—interior branch root or
   leaf—whose upstream contract and code prerequisites are on `main`, whose
   decisions are settled, and whose worktree and scratch paths are isolated.
4. Recompute the frontier on every `main` advance: release newly unblocked
   downstream nodes, and close and clean up any open ticket whose commits are
   already ancestors of `main` (`git merge-base --is-ancestor`).

## Delegate end-to-end subticket ownership

1. Spawn one dedicated subagent worker per ready frontier subticket or upfront
   read-only probe. If the host lacks subagent delegation, report the capability
   gap and agree on a sequential plan instead of claiming delegation occurred.
2. Each worker executes its ticket directly via
   [ticket-delivery](../ticket-delivery/SKILL.md)—its own worktree, tests, GitHub
   updates, PR, repository gates, landing, and cleanup—without recursively
   delegating that ticket. Spawn separate workers for any child subtickets.
3. The coordinator owns the DAG, ready frontier, and owner approvals; it does not
   collect worker diffs into one worktree or become a PR-merging bottleneck. Pause
   affected downstream nodes when a worker uncovers an unsettled product rule.
4. After the initial status summary, wakeups and handbacks report **material
   deltas only**: landed work, newly unblocked frontier nodes, changed blockers,
   new findings, or newly surfaced decisions. Never repeat unchanged full reports
   or emit no-change heartbeats.

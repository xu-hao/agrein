---
name: epic-queue
description: >-
  Use when decomposing multi-ticket work, managing a GitHub epic queue, wiring
  native GitHub parent and sub-issue relationships, or coordinating subagent
  workers across dependent and parallel subtickets.
---

# Epic queue

Use this workflow when coordinating multi-ticket work or when a repository
requires every non-epic ticket to belong to a parent epic.

## Wire native GitHub sub-issues

1. Organize multi-ticket work under one owning epic using GitHub's native
   parent/sub-issue relationship rather than a Markdown checklist alone.
2. Find or create the owning epic first, then create and attach each child
   immediately before execution using its numeric database `.id` (not its visible
   `#N` number). Verify the relationship on GitHub before dispatching work; see
   [native GitHub sub-issues](references/github-sub-issues.md).
3. Never self-parent an epic or silently move an issue away from another owning
   epic. Repair or park broken parenting before implementation starts.

## Triage the full queue upfront

Read the entire epic queue—current behavior, contracts, dependency edges, and
acceptance criteria—before starting autonomous child execution. Batch all
predictable product or policy questions for the owner upfront through
[owner-escalation](../owner-escalation/SKILL.md) rather than discovering avoidable
questions one child ticket at a time.

## Schedule foreground rulings before parallel leaves

1. Run ruling-bearing, investigative, or uncertain tickets **sequentially in the
   foreground**—for example, a contract audit, a feasibility probe, or a schema
   rule that downstream consumers depend on. Resolve their outcomes before
   releasing dependent children. Touching separate files does not by itself make
   two tickets decision-independent.
2. Parallelize **only** fully specified, decision-free leaf subtickets whose
   dependencies are settled and whose worktrees and scratch paths are isolated.

## Delegate end-to-end subticket ownership

1. Spawn one dedicated subagent worker per eligible subticket. If the host lacks
   subagent delegation, report that capability gap and agree on a sequential plan
   instead of claiming delegation occurred.
2. Each assigned leaf worker executes its own ticket directly via
   [ticket-delivery](../ticket-delivery/SKILL.md)—managing its own worktree,
   tests, GitHub updates, PR, repository gates, landing, and cleanup—without
   recursively delegating its same ticket. When a subticket itself decomposes into
   further subtickets, spawn separate workers for those children.
3. The coordinator tracks queue order, cross-ticket dependencies, and owner
   approvals without collecting workers' diffs into a single worktree or becoming
   a PR-merging bottleneck. Pause affected dependents if a worker uncovers an
   unsettled product rule.
4. After the initial status summary, coordinator wakeups and worker handbacks
   report **material deltas only**: landed work, changed blockers, new findings,
   or newly surfaced decisions. Do not repeat unchanged full reports or emit
   no-change heartbeats.

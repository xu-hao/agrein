---
name: epic-queue
description: >-
  Use when decomposing multi-ticket work, managing a GitHub epic queue, wiring
  native GitHub parent and sub-issue relationships, deriving an explicit
  dependency DAG, or coordinating subagent workers across ready frontier tickets.
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

## Derive the dependency DAG upfront

1. Read the entire epic upfront—current behavior, contracts, prerequisites, and
   acceptance criteria—before starting autonomous child execution.
2. Build explicit DAG edges from actual contract, code, and state prerequisites;
   never treat narrative `A -> B -> C` prose lists or checkpoint order as
   sequential blockers.
3. Distinguish **hard dependencies** (unsettled upstream contracts or overlapping
   behavioral rewrites of the same seam) from **soft shared-file overlaps**
   (shared index, schema, or registry files where Git or an ordinary target merge
   reconciles disjoint sections cleanly). Touching separate files does not make
   two tickets decision-independent, and touching one shared registry file does
   not by itself create a blocking edge.
4. Batch predictable product or policy questions for the owner upfront through
   [owner-escalation](../owner-escalation/SKILL.md) rather than discovering
   avoidable questions one child ticket at a time.

## Schedule the ready DAG frontier and upfront probes

1. Decouple read-only probes and contract derivations from upstream code merges:
   when a downstream ticket starts with a read-only feasibility probe or
   canonical-contract derivation that depends only on `main` and existing docs or
   SDKs, run that probe or derivation upfront in parallel while upstream code
   branches build so any owner rulings surface early.
2. Serialize **only** owner escalations (running unsettled product or policy
   rulings sequentially in the foreground) and dependent code builds whose
   upstream contract or code prerequisites have not yet landed on `main`.
3. Dispatch **every ready frontier node** in parallel—whether an interior branch
   root with downstream dependents or a leaf—whose upstream contract and code
   prerequisites are on `main`, whose decisions are settled, and whose worktree
   and scratch paths are isolated.
4. Recompute the ready frontier on every `main` advance: whenever a branch lands
   or `main` advances, release newly unblocked downstream nodes and close and
   clean up any open ticket whose commits are already ancestors of `main`
   (`git merge-base --is-ancestor`).

## Delegate end-to-end subticket ownership

1. Spawn one dedicated subagent worker per ready frontier subticket (or upfront
   read-only probe). If the host lacks subagent delegation, report that
   capability gap and agree on a sequential plan instead of claiming delegation
   occurred.
2. Each dedicated worker executes its assigned ticket directly via
   [ticket-delivery](../ticket-delivery/SKILL.md)—managing its own worktree,
   tests, GitHub updates, PR, repository gates, landing, and cleanup—without
   recursively delegating that same ticket. When a subticket itself decomposes
   into further subtickets, spawn separate workers for those children.
3. The coordinator maintains the dependency DAG, ready frontier, and owner
   approvals without collecting workers' diffs into a single worktree or becoming
   a PR-merging bottleneck. Pause affected downstream nodes if a worker uncovers
   an unsettled product rule.
4. After the initial status summary, coordinator wakeups and worker handbacks
   report **material deltas only**: landed work, newly unblocked frontier nodes,
   changed blockers, new findings, or newly surfaced decisions. Do not repeat
   unchanged full reports or emit no-change heartbeats.

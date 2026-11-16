---
name: ticket-delivery
description: >-
  Use before changing code, documentation, configuration, infrastructure, or live
  state to track a single ticket in GitHub, develop in an isolated git worktree,
  verify observable behavior with complete logs, land the pull request, clean up
  merged or squash-merged artifacts safely, and deliver a concise handoff.
---

# Ticket delivery

Apply this workflow in the repository being changed. Explicit owner instructions
and established project contracts take precedence. Read the project's contributor
rules and inspect open issues before filing duplicates.

## Track before editing

1. Create or claim a GitHub issue **before** changing code, documentation,
   configuration, infrastructure, or live state. Read-only analysis, ticket
   maintenance, and local workstation repair need no ticket.
2. Cite every ticket as `#N — one sentence describing the actual work`, never by
   bare number or title alone.
3. If the task spans multiple tickets, coordinates subagents, or works in a
   repository that requires parent epics, attach and schedule it with
   [epic-queue](../epic-queue/SKILL.md). If investigating a defect, regression,
   or failing check, run [bug-investigation](../bug-investigation/SKILL.md)
   before changing production code.

## Isolate in a ticket worktree

Develop, test, and commit only in a dedicated per-ticket `git worktree` branched
from `origin/main`; keep the primary checkout read-only during development. Name
external environments, temporary directories (`TMPDIR`), logs, and scratch paths
after the ticket so concurrent tasks never overwrite one another's state or test
verdicts. Follow [worktrees and cleanup](references/worktrees-and-cleanup.md) for
setup and safe removal.

## Verify behavior and retain complete logs

1. Test observable behavior and relevant failure paths. Do not grep source files
   or documentation prose for required phrases to claim runtime correctness.
2. Capture each test runner's **complete output once** in a ticket-scoped log and
   preserve the runner's direct exit status (`set -o pipefail` when piping). Never
   pipe runners into output-truncating filters (`head`, `tail`) or re-execute slow
   suites repeatedly just to recover discarded output.
3. On an external service or CI outage, apply a bounded retry count, preserve
   logs and resumable state under the ticket namespace, and park the ticket
   honestly instead of spinning indefinitely or claiming unverified behavior passed.

## Land, clean up, and hand off

1. Review the final diff, keep generated build artifacts untracked, and put
   `Closes #N` in the PR body or accepted commit message.
2. Land approved PRs once repository gates pass without asking for extra merge
   confirmation. Deployments, tags/releases, package-index uploads, live
   host/service installations, and state resets require separate per-operation
   approval under [owner-escalation](../owner-escalation/SKILL.md).
3. After landing, verify the commit on `origin/main` and issue closure, confirm
   the worktree has no uncommitted changes, verify patch equivalence with
   `git cherry origin/main` so squash-merged branches are handled accurately, and
   delete only that ticket's worktree, branch, environment, and scratch files.
4. End any exchange that changed code, docs, tickets, infrastructure, or live
   state with a concise handoff:
   - `### 1. What I did` — resulting behavior, `#N — summary`, PR/commit, and
     verified vs. unverified claims.
   - `### 2. What is open` — unfinished work, parked outages, or `None.`
   When unsettled product/policy rulings or missing live-operation approvals
   remain, add `### 3. Decisions needed` and `### 4. Options and recommendation`
   using [owner-escalation](../owner-escalation/SKILL.md); omit empty decision
   sections otherwise. Finish read-only exchanges directly without handoff headers.

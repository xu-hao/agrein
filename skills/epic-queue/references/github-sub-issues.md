# Native GitHub sub-issues and worker briefs

## Attaching and verifying native sub-issues

GitHub's sub-issues REST endpoint expects the child issue's numeric database ID
(`.id`), **not** its visible issue number (`#N`). Substitute the target owner,
repository, epic issue number, and child issue number:

```sh
CHILD_DB_ID=$(gh api repos/OWNER/REPO/issues/CHILD_NUMBER --jq .id)
gh api --method POST repos/OWNER/REPO/issues/EPIC_NUMBER/sub_issues \
  -F sub_issue_id="$CHILD_DB_ID"
gh api repos/OWNER/REPO/issues/EPIC_NUMBER/sub_issues \
  --jq '.[].number'
```

Verify `CHILD_NUMBER` appears in the epic's `sub_issues` list before handing the
ticket to a worker. A cross-link, label, or Markdown task list does not create a
native parent relationship.

## Recording the epic dependency DAG

Summarize three buckets in the epic body or tracking note before dispatching,
derived from actual contract, code, and state prerequisites rather than prose
list position:

- **Upfront read-only probes & foreground rulings:** read-only feasibility probes
  and canonical-contract derivations runnable immediately in parallel against
  `main` while upstream code builds, vs. unsettled product or policy rulings
  handled sequentially in the foreground.
- **Ready DAG frontier:** interior and leaf subtickets whose upstream contract
  and code prerequisites are on `main` and whose product decisions are settled
  (treating disjoint edits to a shared index, schema, or registry file as
  mergeable rather than blocking edges).
- **Blocked downstream nodes:** subtickets waiting on named prerequisite edges
  (upstream contract/code tickets or unsettled owner rulings), never merely a
  later slot in a narrative `A -> B -> C` list.

Whenever `main` advances, recompute these buckets to promote newly unblocked
frontier nodes and check commit ancestry (`git merge-base --is-ancestor` against
`origin/main`) so tickets already landed on `main` are closed and cleaned up
promptly.

## Dedicated worker brief checklist

Provide every subticket worker with a self-contained brief covering:

- **Ticket & parent:** concrete citation (`#42 — isolate ticket scratch
  directories by issue number`) and verified owning epic.
- **Settled contract:** observable before/after behavior, allowed scope, and
  resolved upstream dependencies.
- **Isolation namespace:** exact worktree, branch, environment, log, and scratch
  prefix to use under [ticket-delivery](../../ticket-delivery/SKILL.md).
- **End-to-end ownership:** updating its ticket, running repository gates,
  opening and landing its PR (`Closes #42`), and cleaning merged artifacts (or
  reporting read-only findings and candidate rulings only, when scoped to an
  upfront probe).
- **Bounds & authorization:** finite retry count and parking conditions for
  infrastructure outages, plus any live-operation approvals explicitly granted
  under [owner-escalation](../../owner-escalation/SKILL.md).

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

## Recording epic execution order

Summarize three buckets in the epic body or tracking note before dispatching:

- **Foreground sequential work:** investigations, probes, or tickets that settle
  a shared contract or product rule.
- **Ready parallel leaves:** fully specified, decision-free children with no
  unresolved dependencies.
- **Blocked dependents:** children waiting on a named sibling ticket or owner
  ruling.

## Dedicated worker brief checklist

Provide every subticket worker with a self-contained brief covering:

- **Ticket & parent:** concrete citation (`#42 — isolate ticket scratch
  directories by issue number`) and verified owning epic.
- **Settled contract:** observable before/after behavior, allowed scope, and
  resolved upstream dependencies.
- **Isolation namespace:** exact worktree, branch, environment, log, and scratch
  prefix to use under [ticket-delivery](../../ticket-delivery/SKILL.md).
- **End-to-end ownership:** updating its ticket, running repository gates,
  opening and landing its PR (`Closes #42`), and cleaning merged artifacts.
- **Bounds & authorization:** finite retry count and parking conditions for
  infrastructure outages, plus any live-operation approvals explicitly granted
  under [owner-escalation](../../owner-escalation/SKILL.md).

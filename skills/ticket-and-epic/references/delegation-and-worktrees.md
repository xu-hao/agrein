# Delegation and worktrees

## Native epic relationships

Use the current GitHub UI or supported API for native sub-issues. For an existing
epic and newly created child in the current repository, the REST shape is:

```sh
# Example only: substitute the actual repository and native issue identifiers.
gh api repos/OWNER/REPO/issues/CHILD --jq .id
gh api --method POST repos/OWNER/REPO/issues/EPIC/sub_issues \
  -F sub_issue_id=CHILD_DATABASE_ID
gh api repos/OWNER/REPO/issues/EPIC/sub_issues
```

`CHILD_DATABASE_ID` is the numeric database ID returned by `.id`, not its visible
issue number. Verify the child has exactly the intended owning epic. Create and
attach before handing the child to a worker. If parenting fails, repair the
relationship or park creation before starting implementation. A link, label, or
task-list entry alone is not a native relationship. Do not silently move a child
from another owning epic.

Read every queued child's scope and dependency edges before scheduling. Record a
small execution order in the epic: ready decision-free children, foreground
investigations/rulings, and blocked dependents. A child asking whether a stored
default should change must settle that rule before a worker implements consumers.

## Ticket-scoped isolation

For example, `#42 — isolate ticket scratch directories by issue number` can use:

```sh
git fetch origin
git worktree add /var/tmp/agrein-42-wt -b issue-42-isolate-scratch origin/main
python3.12 -m venv /var/tmp/agrein-42-venv
```

Use `/var/tmp/agrein-42-check.log` and `/var/tmp/agrein-42-scratch/` for that ticket's
logs and scratch state. Adapt the repository prefix in another project. Run all
edits, tests, and commits inside its worktree; use its environment explicitly.
Do not place a shared `.venv`, generated output, or temporary payload in the primary
checkout. A worker may read the primary checkout but must not develop there.

## Worker contract

Each subticket gets a dedicated worker with:

- A concrete citation such as `#42 — isolate ticket scratch directories by issue number`,
  its owning epic, and the verified native relationship.
- The settled general rule, observable before/after behavior, allowed scope,
  dependencies, and required validation.
- Its own worktree, branch, environment, and scratch namespace.
- Responsibility for updating its ticket, opening its PR, satisfying review and
  repository gates, landing within authorization, and cleaning merged artifacts.
- A bounded retry limit and parking conditions for unavailable infrastructure,
  plus the handoff format and operation approvals already granted.

The coordinator monitors outcomes and dependency changes. It should not collect
all workers' diffs into its own worktree or take over their PR publication by
default. Pause affected dependents if a worker uncovers an unsettled rule; resolve
that ticket sequentially in the foreground before resuming parallel execution.

## Failure and cleanup

Classify failures before retrying. A reproducible assertion failure belongs to the
implementation; a service outage or missing external capability belongs to the
infrastructure parking path. Set a finite retry count and delay appropriate to the
operation, preserve logs under the ticket namespace, and stop when the limit is
reached. Do not bypass checks to make an outage look like success.

After the PR has merged, verify its merge commit on `origin/main` and ticket
closure. Leave the worktree before removing it; inspect for uncommitted work first:

```sh
git -C /var/tmp/agrein-42-wt status --short
git worktree remove /var/tmp/agrein-42-wt
git branch -d issue-42-isolate-scratch
```

Delete the remote branch according to repository policy and remove the external
ticket environment and scratch paths after retaining needed evidence. Never use a
broad wildcard that could remove another active ticket's artifacts. Update the
primary checkout only after landing, through a fast-forward update to `main`.

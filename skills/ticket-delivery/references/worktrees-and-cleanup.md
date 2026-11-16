# Worktrees and cleanup

## Ticket-scoped isolation

Keep all edits, build caches, environments, and logs isolated per issue so
concurrent tasks cannot clobber shared files. For example, `#42 — isolate ticket
scratch directories by issue number` can use:

```sh
git fetch origin
git worktree add /var/tmp/agrein-42-wt -b issue-42-isolate-scratch origin/main
mkdir -p /var/tmp/agrein-42-scratch
```

When the project uses an isolated language environment (for example, a Python
virtualenv), place it outside the checkout under the same ticket prefix (such as
`/var/tmp/agrein-42-venv`) and follow the repository's dependency setup. Keep
check logs at `/var/tmp/agrein-42-check.log` and point `TMPDIR` at the ticket
scratch directory when running heavy suites. Do not create a shared `.venv`,
generated build tree, or temporary payload inside the primary checkout.

## Capturing full command evidence

Redirect complete output to a ticket log or use `set -o pipefail` with `tee`:

```sh
set -o pipefail
./scripts/check 2>&1 | tee /var/tmp/agrein-42-check.log
```

Read the saved log to diagnose failures rather than rerunning slow commands with
different `grep` or `tail` filters.

## Squash-safe verification and cleanup

Ancestry checks such as `git branch --merged` and `git branch -d` mislabel
squash-merged pull requests as unmerged because the branch's original commit SHA
is not an ancestor of `origin/main` even when its exact changes landed.

After verifying the PR landed on `origin/main` and the issue closed:

1. Check for uncommitted work **first** (the one thing cleanup could lose):
   ```sh
   git -C /var/tmp/agrein-42-wt status --porcelain
   ```
   Stop and inspect if output is non-empty.
2. Compare patches against `origin/main` with `git cherry`:
   ```sh
   git fetch origin
   git cherry origin/main issue-42-isolate-scratch
   ```
   Lines prefixed with `-` already have an equivalent patch upstream; any `+`
   line indicates unmerged changes that must be preserved.
3. When clean and every patch is `-`, leave the worktree and remove only this
   ticket's resources:
   ```sh
   git worktree remove /var/tmp/agrein-42-wt
   git branch -D issue-42-isolate-scratch
   rm -rf /var/tmp/agrein-42-venv /var/tmp/agrein-42-scratch /var/tmp/agrein-42-check.log
   ```

Never use broad globs (such as `/var/tmp/agrein-*`) that could delete another
active ticket's environment or logs. Fast-forward the primary checkout to
`origin/main` only after landing.

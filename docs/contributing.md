# Contributing

Keep all contributions self-contained to `xu-hao/agrein`. This is a native skill
plugin repository: contributor Python dependencies support checks and docs only.
Read the repository's [contributor instructions](https://github.com/xu-hao/agrein/blob/main/AGENTS.md)
and the two skills before changing tracked content.

## Track and isolate work

Create a GitHub issue before implementation. A non-epic issue belongs to one native
owning epic at creation; a repository bootstrap may itself be the initial epic.
Investigate the full queue and settle product/policy rules before dependent work.
Develop in a dedicated ticket worktree from `origin/main`; the primary checkout
stays read-only during development. Replace `N` below with the ticket number:

```sh
git fetch origin
git worktree add /var/tmp/agrein-N-wt -b issue-N-short-description origin/main
python3.12 -m venv /var/tmp/agrein-N-venv
. /var/tmp/agrein-N-venv/bin/activate
cd /var/tmp/agrein-N-wt
python -m pip install 'pytest>=8' -r docs/requirements.txt
```

Keep logs and scratch state in the same ticket namespace. For bugs, establish a
failing behavioral reproduction before changing production behavior. Preserve
strict internal contracts and test relevant failures as well as the working path.

## Run the complete gate

`claude` and `agy` must be installed and on `PATH`. The checks validate local files;
they do not install the plugin or call a live agent. Run:

```sh
./scripts/check
```

Where `agc` is available, coordinate the same gate with explicit resource claims:

```sh
PATH="/var/tmp/agrein-N-venv/bin:$PATH" agc run --no-overflow \
  --label "agrein-N-check" --resource cpu=2 --resource memory=4294967296 \
  --resource tmpfs=2147483648 --resource tmpfs_inodes=131072 -- ./scripts/check
```

The gate runs `python -m pytest -q`, `python scripts/check-plugins.py`, and
`python -m sphinx -W --keep-going -b html docs docs/_build/html`. Packaging tests
exercise manifest structure, shared skill discovery, YAML frontmatter, relative
reference links, and the validator's success/failure behavior. They do not claim
that prose assertions prove an agent will obey a skill.

Native validation checks Claude Code strictly, checks Antigravity's checkout for
errors and exactly two skills, and checks an exact disposable Antigravity payload
strictly. The full multi-host checkout can produce warnings for intentionally
ignored files. Codex manifest consistency is checked structurally; no successful
native installation is claimed. See the script for the read-only symlink handling.

## Land and clean up

Review the diff, keep build output untracked, and open a PR containing `Closes #N`.
Land approved PRs when repository gates pass; do not infer approval for a release,
deployment, upload, host/service installation, or state reset from a merge approval.
An explicit authorization already given for the specific operation remains valid.

Where available, run one guarded landing with the same gate:

```sh
PATH="/var/tmp/agrein-N-venv/bin:$PATH" agc land PR_NUMBER --no-overflow \
  --label "agrein-N-land" --resource cpu=2 --resource memory=4294967296 \
  --resource tmpfs=2147483648 --resource tmpfs_inodes=131072 -- ./scripts/check
```

After merge, verify the commit on `origin/main` and ticket closure. Remove generated
output, the merged worktree and branch, and its external environment/scratch files
after retaining evidence. Fast-forward the primary checkout only after landing.
End changed-state exchanges with `1. What I did`, `2. What is open`,
`3. Decisions needed`, and `4. Options and recommendation`.

# agrein

`agrein` combines **ag** + **rein**, pronounced *“a grain”*: a small set of
contributor habits for agent-assisted projects. This public MIT repository ships
four focused Agent Skills for Codex, Claude Code, and Antigravity. It has no
Python runtime, PyPI package, hooks, MCP server, or automatic host configuration.

## Install

Use a current native client with plugin support. Choose your host:

```sh
# Codex
codex plugin marketplace add xu-hao/agrein
codex plugin add agrein@agrein
```

```sh
# Claude Code
claude plugin marketplace add xu-hao/agrein
claude plugin install agrein@agrein
```

```sh
# Antigravity
agy plugin install https://github.com/xu-hao/agrein
```

Reopen the agent if the new skills are not visible. Native clients manage plugin
installation and discovery; the plugin does not enforce workflow at a tool boundary.
See [Quickstart](docs/quickstart.md) for invocation and lifecycle commands.

## The four skills

| Skill | Workflow |
| --- | --- |
| [ticket-delivery](skills/ticket-delivery/SKILL.md) | Issues before changes, isolated per-ticket worktrees, complete-log behavioral verification, guarded PR landing (`Closes #N`), squash-safe `git cherry` cleanup, and concise handoffs |
| [epic-queue](skills/epic-queue/SKILL.md) | Native GitHub parent/sub-issue relationships, explicit dependency DAG derivation, parallel upfront read-only probes, foreground rulings, ready-frontier subagent dispatch, and delta-only updates |
| [bug-investigation](skills/bug-investigation/SKILL.md) | Evidence-first reproduction, general problem-class diagnosis, `origin/main` proof for pre-existing failures, producer fixes over consumer fallbacks, and failing behavioral tests first |
| [owner-escalation](skills/owner-escalation/SKILL.md) | Product/policy vs. engineering boundary, standalone jargon-free before/after single-select rulings, explicit per-operation live approval gates, and four-section decision handoffs |

Invoke `$<skill-name>` in Codex, `/agrein:<skill-name>` in Claude Code, or
`/<skill-name>` in Antigravity.

## Recommended project instructions

After installing, add this trigger to your project's `AGENTS.md` (or the host's
native project instructions):

```text
Use the installed agrein skills: ticket-delivery before changing code, docs,
config, infrastructure, or live state; epic-queue when decomposing multi-ticket
work or coordinating subagent workers; bug-investigation before fixing defects or
failing checks; and owner-escalation for unsettled product/policy rulings, live
operation approvals, and decision handoffs. An assigned leaf worker implements
its ticket directly without recursively delegating it.
```

The same text ships as [AGENTS.snippet.md](AGENTS.snippet.md) for copying or
scripted bootstrapping. Installation makes the workflows discoverable; this
snippet requests their use.
It does not grant deployment/release authority or make unavailable subagent tools
available. The [skill guide](docs/skills.md) describes these boundaries.

## Contribute

Create a ticket, then work in its dedicated worktree. Keep development dependencies
in an external ticket-named Python 3.12 environment:

```sh
python3.12 -m venv /var/tmp/agrein-N-venv
. /var/tmp/agrein-N-venv/bin/activate
python -m pip install 'pytest>=8' -r docs/requirements.txt
./scripts/check
```

Replace `N` with the tracking issue number. Checks need `claude` and `agy` on `PATH`;
they validate local payloads without installing the plugin. `scripts/check` runs
behavioral packaging tests, native validation, and a warning-free Sphinx build.
Where `agc` is available, run it through the coordinated command in
[Contributing](docs/contributing.md). Read [AGENTS.md](AGENTS.md) and
[CHANGELOG.md](CHANGELOG.md). The [MIT license](LICENSE) covers the repository.

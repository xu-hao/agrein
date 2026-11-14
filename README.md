# agrein

`agrein` combines **ag** + **rein**, pronounced *“a grain”*: a small set of
contributor habits for agent-assisted projects. This public MIT repository ships
two Agent Skills for Codex, Claude Code, and Antigravity. It has no Python runtime,
PyPI package, hooks, MCP server, or automatic host configuration.

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

## The two skills

| Skill | Workflow |
| --- | --- |
| [ticket-and-epic](skills/ticket-and-epic/SKILL.md) | Issues before changes, native owning epics, upfront queue investigation, dedicated workers, isolated worktrees, behavioral verification, and ticket-owned landings |
| [handoff-and-escalation](skills/handoff-and-escalation/SKILL.md) | Owner product/policy rulings, concrete before/after choices, live-operation approvals, meaningful ticket citations, and four-section session handoffs |

Invoke `$ticket-and-epic` or `$handoff-and-escalation` in Codex,
`/agrein:ticket-and-epic` or `/agrein:handoff-and-escalation` in Claude Code, or
`/ticket-and-epic` or `/handoff-and-escalation` in Antigravity.

## Recommended project instructions

After installing, add this trigger to your project's `AGENTS.md` (or the host's
native project instructions):

```text
Use the installed agrein ticket-and-epic skill before changing code, documentation,
infrastructure, or live state, and when planning or executing an epic queue.
Use handoff-and-escalation for unsettled owner product/policy rulings, operation
approval gates, and the final handoff after any changed-state exchange.
Follow canonical project contracts and explicit owner authorization. An assigned
leaf worker executes its ticket directly without recursively delegating it.
```

Installation makes the workflows discoverable; this snippet requests their use.
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

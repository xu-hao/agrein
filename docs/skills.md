# Skills and native packaging

Both workflows use Agent Skills Markdown with YAML `name` and `description`
frontmatter. Their progressive references contain operational detail:

- [ticket-and-epic](https://github.com/xu-hao/agrein/blob/main/skills/ticket-and-epic/SKILL.md)
  tracks changes before execution, attaches children to native owning epics,
  investigates the full queue, and assigns dedicated ticket workers. It requires
  worktree isolation, evidence before bug fixes, strict internal contracts,
  bounded retries with infrastructure parking, and observable behavioral checks.
- [Delegation and worktrees](https://github.com/xu-hao/agrein/blob/main/skills/ticket-and-epic/references/delegation-and-worktrees.md)
  explains native sub-issue IDs, ticket-scoped paths, scheduling, and cleanup.
- [handoff-and-escalation](https://github.com/xu-hao/agrein/blob/main/skills/handoff-and-escalation/SKILL.md)
  reserves owner questions for unsettled product/policy rules, shows exact
  before/after applications, distinguishes merge gates from live-operation
  approval, and ends changed-state exchanges with four prescribed sections.
- [Escalation and handoffs](https://github.com/xu-hao/agrein/blob/main/skills/handoff-and-escalation/references/escalation-and-handoffs.md)
  provides a worked single-select question and operation approval transitions.

## One payload, three wrappers

| Host | Metadata | Shared content |
| --- | --- | --- |
| Codex | `plugin.json` and `.agents/plugins/marketplace.json` | `skills/*/SKILL.md` |
| Claude Code | `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` | `skills/*/SKILL.md` |
| Antigravity | `.antigravity-plugin/plugin.json` | `skills/*/SKILL.md` |

The marketplace source `./` resolves to the repository root. Default skill discovery
loads exactly the same two folders for every host; no per-host skill path override
is needed. `CLAUDE.md` is a contributor-instruction symlink to `AGENTS.md`, not another
skill or plugin payload. Manifests share the plugin name and release version.

The formats and native install paths follow the official
[Codex plugin guide](https://developers.openai.com/plugins/build/plugins),
[Claude Code manifest reference](https://code.claude.com/docs/en/plugins-reference),
and [Antigravity plugin guide](https://antigravity.google/docs/build-plugins).

## Capability and authorization boundaries

Native clients own discovery and activation. Installation alone does not guarantee
that an agent invokes either skill; use the project trigger in [Quickstart](quickstart.md).
These instructions do not enforce actions at the host's tool boundary, create a
scheduler, add a GitHub integration, or grant new permissions.

Native epic relationships need GitHub access. Dedicated workers need a host with
subagent support. If a capability is missing, report it and settle an alternative
execution plan. Do not claim native parenting or delegation happened without it.
An assigned leaf worker executes its own ticket directly. Fully specified children
can run concurrently; ruling-bearing investigations run sequentially in the foreground.

Explicit owner instructions and canonical project contracts govern execution.
Read-only work, ticket maintenance, and workstation setup need no change ticket.
Changed-state exchanges need the four-section handoff; read-only answers do not.

# Quickstart

Use a current Codex, Claude Code, or Antigravity native client with plugin support.
No Python install is needed to consume the skills. Install only into a host the
owner has authorized you to configure.

## Install in your host

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

For a source checkout, replace `xu-hao/agrein` with the checkout path in marketplace
registration; Antigravity accepts that directory directly. Choose the intended
user/project scope with the host's supported options. Reopen the agent if needed.

## Request a workflow

| Host | Ticket delivery | Epic queue | Bug investigation | Owner escalation |
| --- | --- | --- | --- | --- |
| Codex | `$ticket-delivery` | `$epic-queue` | `$bug-investigation` | `$owner-escalation` |
| Claude Code | `/agrein:ticket-delivery` | `/agrein:epic-queue` | `/agrein:bug-investigation` | `/agrein:owner-escalation` |
| Antigravity | `/ticket-delivery` | `/epic-queue` | `/bug-investigation` | `/owner-escalation` |

Requesting a workflow does not grant permission for a release or deployment.

Add this trigger, shipped as the repository's root `AGENTS.snippet.md`, to the
consuming project's `AGENTS.md`, or its native equivalent:

```{literalinclude} ../AGENTS.snippet.md
:language: text
```

## Inspect and remove

```sh
codex plugin list
claude plugin list
agy plugin list
```

Native clients own updates, caches, and enable/disable state. Codex exposes
`codex plugin marketplace upgrade`; Claude Code uses
`claude plugin update agrein@agrein`. Consult `agy plugin help` for Antigravity's
current lifecycle commands. Removal commands are:

```sh
codex plugin remove agrein@agrein
claude plugin uninstall agrein@agrein
agy plugin uninstall agrein
```

Use one installation route per host to avoid duplicate skill names. The plugin
does not install hooks or copy files into other projects on its own.

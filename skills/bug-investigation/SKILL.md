---
name: bug-investigation
description: >-
  Use when investigating a bug report, regression, flaky check, or failing test
  to cluster bursts of related bug tickets by root cause before dispatch,
  measure and reproduce the symptom first, name the general problem class,
  prove pre-existing failure claims on main, fix invalid internal producers, and
  lock in a failing behavioral test before changing production code.
---

# Bug investigation

Run before changing production code for any bug, regression, flaky check, or
unexpected test failure.

## Cluster bug bursts by root cause before dispatch

When several bug or regression tickets arrive together, run a bounded cause check
before fanning out fixes or leaf workers:

1. Record each ticket's failure signature (error text, failing test, stack frame,
   or observed symptom) and trace it to the producing code path, commit, or
   contract within a fixed probe or time budget.
2. Group tickets that share a signature or producing seam under one root-cause
   ticket, and link recurrences of an already-fixed defect to the original fix.
   Fix the shared cause once instead of dispatching parallel symptom patches that
   collide on the merge queue.
3. Dispatch tickets with distinct causes independently. If the budget ends without
   proving a shared cause, treat the tickets as independent and record the
   suspected link.

## Measure and reproduce first

1. Treat an unconfirmed symptom as an investigation, not permission to guess at a
   patch: build a minimal probe, benchmark, or reproduction of the reported
   failure first.
2. Confirm it reaches the faulty seam and fails for the expected reason, not
   vacuously (for example, a setup typo or unexercised code path).

## Step back to the general problem class

1. Name the general problem class—for example, starvation under greedy backfill,
   reparented orphan processes, unanchored trailing-newline regexes, or stale
   cache invalidation—and survey established solutions before choosing an
   implementation.
2. Decide whether a project rule is missing (escalate through
   [owner-escalation](../owner-escalation/SKILL.md)), conflicting across docs, or
   settled and violated by code. Fix the shared design cause to prevent the defect
   class instead of adding an ad-hoc local special case.

## Fix invalid internal producers, not consumer fallbacks

When internal modules disagree on a type, field, or invariant, fix the producer
emitting invalid data—no speculative `a or b` coercions, guessed alternate keys,
or silent defaults in internal consumers. Reserve permissive tolerance and
normalization for external boundaries: user input, LLM output, network
responses, and untrusted files.

## Prove "pre-existing" failures on `main`

Never call a branch failure "pre-existing" based only on an earlier commit of the
same branch:

1. Run the **exact same command and test scope** (single file or full suite) on
   `git merge-base origin/main HEAD` or current `origin/main`.
2. Count it as pre-existing **only** if `main` reproduces it, citing both commit
   SHAs and retained check logs.

## Lock in a failing behavioral test before fixing

Write an observable behavioral test that fails with the reproduced symptom
**before** editing production code, confirm the fix turns it green, and keep it as
a regression check. Do not assert source text or prose to prove runtime behavior.
Track, isolate, and land the fix through
[ticket-delivery](../ticket-delivery/SKILL.md).

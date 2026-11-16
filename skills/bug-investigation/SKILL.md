---
name: bug-investigation
description: >-
  Use when investigating a bug report, regression, flaky check, or failing test
  to measure and reproduce the symptom first, name the general problem class,
  prove pre-existing failure claims on main, fix invalid internal producers, and
  lock in a failing behavioral test before changing production code.
---

# Bug investigation

Apply this workflow whenever diagnosing a bug, regression, flaky check, or
unexpected test failure before changing production code.

## Measure and reproduce first

1. Treat an unconfirmed symptom as an investigation, not permission to guess at a
   patch. Build a minimal probe, benchmark, or reproduction that demonstrates the
   reported failure first.
2. Verify that the probe or reproduction actually reaches the faulty seam and
   fails for the expected reason rather than passing or failing vacuously (for
   example, due to a setup typo or unexercised code path).

## Step back to the general problem class

1. Name the general engineering problem class behind the symptom—for example,
   starvation under greedy backfill, reparented orphan processes, unanchored
   trailing-newline regexes, or stale cache invalidation—and survey established
   solutions for that class before choosing an implementation.
2. Determine whether a project rule is missing (escalate through
   [owner-escalation](../owner-escalation/SKILL.md)), conflicting across docs, or
   already settled and violated by code. Fix the shared design cause to prevent
   the class of defect rather than adding an ad-hoc local special case.

## Fix invalid internal producers, not consumer fallbacks

When internal modules disagree on a type, field, or invariant, fix the producer
emitting invalid data. Do not scatter speculative `a or b` fallback coercions,
guessed alternate keys, or silent defaults across internal consumers. Reserve
permissive tolerance and normalization for external boundaries: user input, LLM
output, network responses, and untrusted files.

## Prove "pre-existing" failures on `main`

Never dismiss a failing check on your branch as "pre-existing" based only on an
earlier commit of that same branch:

1. Run the **exact same command and test scope** (single file or full suite) on
   `git merge-base origin/main HEAD` or current `origin/main`.
2. Count the failure as pre-existing **only** if `main` reproduces it, citing
   both commit SHAs and retained check logs as evidence.

## Lock in a failing behavioral test before fixing

Write an observable behavioral test that fails with the reproduced symptom
**before** editing production code, then confirm the same test turns green with
your fix and keep it as a regression check. Do not assert source text or prose to
prove runtime behavior. Track, isolate, and land the fix through
[ticket-delivery](../ticket-delivery/SKILL.md).

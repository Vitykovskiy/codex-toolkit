---
name: codex-orchestration-pact
description: Coordinate dependent or independent assignments with an evidence-backed route and independent acceptance.
metadata:
  version: "2.1.0"
---

# Orchestration pact

Use this pact only for an explicit orchestration request or real coordination. The route table in [AGENTS.md](../../AGENTS.md) is canonical. A ready local task does not need a planning relay.

Give an owner the literal goal, constraints, criteria, write-set, short required facts, and primary-evidence paths. Use one owner for a connected result; group independent work by responsibility, with no more than two writers, then use one independent packet review. An architect consultation replaces a mandatory analyst/decomposer chain when the decision is materially uncertain. `decomposer` remains available for an explicitly requested standalone decomposition or legacy import.

An independent `reviewer` accepts one result. Use `integration_reviewer` instead when cross-part compatibility, security, or another stated integration criterion is material. The first sufficient review covers requirements, implementation, relevant risks, and connections; do not add a reviewer-of-reviewers. A fix returns to its owner and the reviewer checks only the fix, affected dependencies, and regressions.

Packet approval preserves the six report keys. `result.accepts` is either the legacy one accepted-result object or a nonempty list; every list entry has `assignment_id`, `attempt`, `goal_version`, and `snapshot`. The envelope mirrors this as one legacy compact string or a nonempty list. Every entry is validated: no self-approval, duplicate result, stale attempt, version mismatch, paused/blocked/incomplete result, or missing evidence. A packet is accepted only when every listed result passes.

Use [long orchestration](../codex-long-orchestration/SKILL.md) only for strict durable state. In ordinary mode return a compact result: outcome, changes, checks, material risks, and next action. If an unavailable tool blocks a required fact, record the exact limitation rather than inventing an equivalent result.

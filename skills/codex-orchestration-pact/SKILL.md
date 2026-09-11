---
name: codex-orchestration-pact
description: Coordinate dependent or independent assignments with an evidence-backed route and independent acceptance.
metadata:
  version: "2.1.1"
---

# Orchestration pact

Use this pact only for an explicit orchestration request or real coordination. The portable route table below is canonical; a ready local task does not need a planning relay.

## Portable route table

| Work | Route / setting |
|---|---|
| Ready literal text or config edit | One owner and relevant checks; independent review only for a contract or semantic risk. |
| Connected behaviour change | `developer` (`gpt-5.6-terra` / `medium`), then independent `reviewer` (`gpt-5.6-terra` / `medium`). |
| Truly independent outcomes | Coarse responsibility assignments, at most two simultaneous writers, then one sufficient packet review. |
| Material decision uncertainty | One `architect` (`gpt-5.6-sol` / `medium`) consultation, which may prepare executable assignments and write-sets. |
| Explicit strict, existing strict state, or genuine cross-session state | Durable dispatcher with role-owned reports and independent acceptance. |
| Narrow mechanical work / fact collection | `mechanical` and `scout` (`gpt-5.6-luna` / `low`). |
| Provably literal non-semantic review | Existing `reviewer_fast` (`gpt-5.6-terra` / `low`), never security or orchestration-semantic acceptance. |
| Investigation / integration-security review | `analyst_standard` and `integration_reviewer` (`gpt-5.6-sol` / `medium`). |

File count, a normal fix/review pair, and implementation followed by measurement do not trigger strict mode. `analyst` and `decomposer` remain optional existing capabilities, not mandatory relays. Existing other profiles retain their settings; do not escalate to Astra automatically.

Give an owner the literal goal, constraints, criteria, write-set, short required facts, and primary-evidence paths. Use one owner for a connected result; group independent work by responsibility, with no more than two writers, then use one independent packet review. An architect consultation replaces a mandatory analyst/decomposer chain when the decision is materially uncertain. `decomposer` remains available for an explicitly requested standalone decomposition or legacy import.

An independent `reviewer` accepts one result. Use `integration_reviewer` instead when cross-part compatibility, security, or another stated integration criterion is material. The first sufficient review covers requirements, implementation, relevant risks, and connections; do not add a reviewer-of-reviewers. A fix returns to its owner and the reviewer checks only the fix, affected dependencies, and regressions.

Packet approval preserves the six report keys. `result.accepts` is either the legacy one accepted-result object or a nonempty list; every list entry has `assignment_id`, `attempt`, `goal_version`, and `snapshot`. The envelope mirrors this as one legacy compact string or a nonempty list. Every entry is validated: no self-approval, duplicate result, stale attempt, version mismatch, paused/blocked/incomplete result, or missing evidence. A packet is accepted only when every listed result passes.

Use [long orchestration](../codex-long-orchestration/SKILL.md) only for strict durable state. In ordinary mode return a compact result: outcome, changes, checks, material risks, and next action. If an unavailable tool blocks a required fact, record the exact limitation rather than inventing an equivalent result.

For real delegation, use a discovered native subagent tool with the actual custom-agent configuration. A shell-launched `codex exec` whose prompt names a role is not native delegation; a missing mandatory native capability is a capability failure before unrelated user files are investigated. Inspect only task-relevant sources and explicit configuration. Put large outputs in a raw file and return status, sufficient errors, and a bounded preview, while retaining the original evidence and expanding precise ranges when needed. Tool bytes are not token telemetry. Wait through native completion/blocking tools, reuse the same implementation/reviewer context for a narrow fix, and do not forward the campaign prompt, complete parent history, or all peer reports as a task packet. Use only supported context-isolation options.

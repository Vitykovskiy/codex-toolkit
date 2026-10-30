# Assignment report

Ordinary direct and delegated non-approval results are concise inline prose with evidence references unless a file is assigned or needed for durable access. Root may read them under the [mode boundary](../../SKILL.md#dispatcher-invariant). The receipts below are writing patterns, not replacement schemas. Formal approval uses the existing canonical report and acceptance correlation, even when returned inline. Only strict workflows always write the canonical file report and return a metadata-only envelope. Do not emit a second full copy.

## Compact receipts

- Source lookup / requirements collection: `rule or fact — source:section/line — scope and conditions.` State inspected scope, material unread sources, conflicts, gaps and known currency. A limited search is not proof of global absence. See [Project requirements](../../SKILL.md#project-requirements).
- Implementation: state the outcome and material changes, then actual verification status and remaining risk. Do not paste the full patch or repeat the task.
- Review finding: `path:line — severity; violated source/criterion; consequence; correction.` Keep independent primary-source evidence, affected-path rules, reviewed scope and material gaps. For acceptance coverage, follow [Execution and acceptance](../../SKILL.md#execution-and-acceptance): use existing `result.evidence` or other `result` fields for the primary rule, inspected area and supporting observation, and `checks` for actual permitted checks. Group homogeneous criteria only with their full scope explicit; name unverified items and justified nonapplicability. No findings does not establish verification that was not performed.
- Decision: state the selected option, its decisive evidence, relevant trade-off and condition for reconsideration. Omit rejected alternatives that do not affect the decision.

Use concise grammatical English for generated internal prose. Preserve exact quotes, identifiers, conditions and uncertainties. A word limit must not remove a necessary finding or qualification.

Before handing a result to a dependent subject owner, make its conclusion, supporting source locations, relevant snapshot and unchecked criteria clear in existing fields or inline prose. Keep bulky intermediate material addressable instead of copying it into every handoff. The recipient verifies identity, currency and coverage against its own primary requirements; a compact summary alone is not acceptance evidence. Only strict root receives a process receipt and artifact references without subject content.

## User-facing files

When a report, question or other Markdown file will communicate with the user, its author and any already-required independent reviewer apply the [user-facing Markdown contract](../../../codex-communication-pact/SKILL.md#user-facing-markdown). Write a self-contained explanation in the user's language, with evidence and a clear conclusion or requested decision. The compact receipts and canonical YAML below serve internal coordination; dumping their fields or concatenating agent reports does not produce a user-facing answer.

Keep canonical reporting and acceptance correlation intact. Reuse an existing suitable user-facing file or prepare the assigned deliverable; do not create a second full copy of the internal report or a document for every internal message. Retain the delivered file reference and applicable review evidence within existing `result` fields. In strict mode, expose a ready user-facing path through the optional `user_artifacts` references in the [envelope](../../../codex-long-orchestration/references/templates/envelope.md), leaving `artifact` pointed at the canonical report. The dispatcher receives references only.

## Canonical report

This is the canonical full report. Envelope is a separate process notification.

```yaml
status: completed
changed_files: []
checks: []
result:
  assignment:
    id: A01
    attempt: 1
    goal_version: 1
    snapshot: null
  accepts: null
  evidence: []
  findings: []
risks: []
next_action: null
```

Before dependent work, establish the source-grounded task in existing context; strict work records it in its assigned subject artifact. A canonical report retains the outcome and primary source references under existing `result` fields, without repeating the assignment or adding top-level keys. The original request remains authoritative.

Exactly these six top-level keys are required. `approved` is only an independent reviewer or integration reviewer verdict. `paused`, `blocked`, and incomplete results are never accepted. `assignment` identifies this report; `snapshot` is required whenever import, cross-tree transfer, parallel writing, release, security, or the assignment requires it.

`result.accepts` is `null` outside approval. An approval uses either one legacy object with `assignment_id`, `attempt`, and `goal_version`, or a nonempty packet list of those objects. Every packet item also requires a nonblank `snapshot`. No item may repeat a result or refer to the reviewer itself. `approved` means every listed result passed the stated criteria; unchanged accepted evidence remains valid, while a fix needs checks for itself, dependencies, and regressions.

Each check records a nonblank command, `execution_status: checked | not_run | unable_to_verify`, and `result: passed | failed | null`. An unrun check requires `result: null` and a nonblank reason. Keep applicable rule sources, scope, material gaps and primary evidence under existing `result` fields when relevant; do not add top-level keys or repeat the whole conversation.

In `dispatcher_only` the subject role writes this report atomically at its assigned `artifact_path` and returns only the linked envelope. The reviewer checks full-report correlation and required evidence; strict root does not open it. Ordinary direct and delegated work use inline receipts for non-approval results and the canonical report for formal approval or an explicitly requested structured report. A report file is created only when assigned or needed for durable access. `completed` is implementation completion, not independent approval. Unrun required checks prevent an unsupported `approved` verdict.

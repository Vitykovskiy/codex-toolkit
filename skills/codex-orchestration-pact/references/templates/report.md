# Assignment report

Ordinary direct non-approval results are concise inline prose unless a report file is assigned. Dispatched subject results stay with their owners at accessible task locations; root receives only process metadata and artifact references under the [dispatcher invariant](../../SKILL.md#dispatcher-invariant). The receipts below are writing patterns, not replacement schemas. Formal approval uses the existing canonical report and acceptance correlation, even when returned inline. A strict workflow always writes the canonical file report and returns only its envelope. Do not emit a second full copy.

## Compact receipts

- Source lookup / requirements collection: `rule or fact — source:section/line — scope and conditions.` State inspected scope, material unread sources, conflicts, gaps and known currency. A limited search is not proof of global absence. See [Project requirements](../../SKILL.md#project-requirements).
- Implementation: state the outcome and material changes, then actual verification status and remaining risk. Do not paste the full patch or repeat the task.
- Review finding: `path:line — severity; violated source/criterion; consequence; correction.` Keep independent primary-source evidence, affected-path rules, reviewed scope and material gaps. For acceptance coverage, follow [Execution and acceptance](../../SKILL.md#execution-and-acceptance): use existing `result.evidence` or other `result` fields for the primary rule, inspected area and supporting observation, and `checks` for actual permitted checks. Group homogeneous criteria only with their full scope explicit; name unverified items and justified nonapplicability. No findings does not establish verification that was not performed.
- Decision: state the selected option, its decisive evidence, relevant trade-off and condition for reconsideration. Omit rejected alternatives that do not affect the decision.

Use concise grammatical English for generated internal prose. Preserve exact quotes, identifiers, conditions and uncertainties. A word limit must not remove a necessary finding or qualification.

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

Before dependent work, record your own source-grounded working task in the existing assignment or working context. In a canonical report, retain its formulation and primary source references under existing `result` fields; never replace the original request or add top-level keys.

Exactly these six top-level keys are required. `approved` is only an independent reviewer or integration reviewer verdict. `paused`, `blocked`, and incomplete results are never accepted. `assignment` identifies this report; `snapshot` is required whenever import, cross-tree transfer, parallel writing, release, security, or the assignment requires it.

`result.accepts` is `null` outside approval. An approval uses either one legacy object with `assignment_id`, `attempt`, and `goal_version`, or a nonempty packet list of those objects. Every packet item also requires a nonblank `snapshot`. No item may repeat a result or refer to the reviewer itself. `approved` means every listed result passed the stated criteria; unchanged accepted evidence remains valid, while a fix needs checks for itself, dependencies, and regressions.

Each check records a nonblank command, `execution_status: checked | not_run | unable_to_verify`, and `result: passed | failed | null`. An unrun check requires `result: null` and a nonblank reason. Keep applicable rule sources, scope, material gaps and primary evidence under existing `result` fields when relevant; do not add top-level keys or repeat the whole conversation.

In dispatcher mode the subject role writes this report atomically at its assigned `artifact_path` and returns only the linked envelope. The subject reviewer checks full-report correlation and required evidence; the dispatcher does not open this report. In ordinary direct work, use an inline receipt for non-approval work; use the canonical report for formal approval or an explicitly requested structured report. A report file is created only when assigned. `completed` is implementation completion, not independent approval. Unrun required checks prevent an unsupported `approved` verdict.

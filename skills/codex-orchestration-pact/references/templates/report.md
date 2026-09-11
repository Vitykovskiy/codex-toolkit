# Assignment report

Ordinary non-approval results are concise inline prose unless a report file is explicitly assigned. The receipts below are writing patterns, not replacement schemas. Formal approval uses the existing canonical report and acceptance correlation, even when returned inline. A strict workflow always writes the canonical file report and returns only its envelope. Do not emit a second full copy.

## Compact receipts

- Source lookup: `path:line — symbol or fact; relevance.` State the searched scope and any material gap. A limited search is not proof of global absence.
- Implementation: state the outcome and material changes, then actual verification status and remaining risk. Do not paste the full patch or repeat the task.
- Review finding: `path:line — severity; defect; consequence; correction.` Keep evidence and the reviewed scope. No findings does not establish verification that was not performed.
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

Exactly these six top-level keys are required. `approved` is only an independent reviewer or integration reviewer verdict. `paused`, `blocked`, and incomplete results are never accepted. `assignment` identifies this report; `snapshot` is required whenever import, cross-tree transfer, parallel writing, release, security, or the assignment requires it.

`result.accepts` is `null` outside approval. An approval uses either one legacy object with `assignment_id`, `attempt`, and `goal_version`, or a nonempty packet list of those objects. Every packet item also requires a nonblank `snapshot`. No item may repeat a result or refer to the reviewer itself. `approved` means every listed result passed the stated criteria; unchanged accepted evidence remains valid, while a fix needs checks for itself, dependencies, and regressions.

Each check records a nonblank command, `execution_status: checked | not_run | unable_to_verify`, and `result: passed | failed | null`. An unrun check requires `result: null` and a nonblank reason. Keep primary evidence and material unknowns under `result`; do not repeat the whole conversation.

In dispatcher mode the subject role writes this report atomically at its assigned `artifact_path` and returns only the linked envelope. In ordinary mode, use an inline receipt for non-approval work; use the canonical report for formal approval or an explicitly requested structured report. A report file is created only when assigned. `completed` is implementation completion, not independent approval. Unrun required checks prevent an unsupported `approved` verdict.

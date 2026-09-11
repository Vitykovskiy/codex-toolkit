# Assignment report

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

In dispatcher mode the subject role writes this report atomically at its `artifact_path` and returns only the linked envelope. Outside strict mode it may return the same compact facts directly.

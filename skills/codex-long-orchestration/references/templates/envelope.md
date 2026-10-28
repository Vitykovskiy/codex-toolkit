# Dispatcher envelope

An envelope carries only process metadata, not subject content. Root checks its shape, path safety, runtime sender, identity and permitted transition under the [dispatcher invariant](../../../codex-orchestration-pact/SKILL.md#dispatcher-invariant), without opening its artifact or any prepared assignment. Exclude task summaries, criteria, findings text and report excerpts.

```yaml
status: completed
artifact: reports/A01.yaml
user_artifacts: []
assignment_id: A01
attempt: 1
profile: developer
goal_version: 1
snapshot: S1
plan_revision: P1
stream_id: T1
stream_owner: A01/1
stream_status: running
accepts: null
finding_id: null
progress: null
no_progress: null
completion:
  plan_revision: P1
  confirmed_weight: 2
  total_weight: 5
stream_completion:
  plan_revision: P1
  confirmed_weight: 3
  total_weight: 5
process_signal: on_track
next_transitions:
  - profile: reviewer
    assignment_id: R01
    attempt: 1
    assignment_path: assignments/R01.yaml
    plan_revision: P1
    stream_id: T1
    stream_owner: A01/1
    input_revision: G1
    depends_on:
      - assignment_id: A01
        attempt: 1
        goal_version: 1
        required_status: completed
        snapshot: S1
    resource_claims:
      - resource_id: snapshot-S1
        access: read
invalidated_assignments: []
```

`user_artifacts` optionally lists paths of files prepared for communication with the user, for example `delivery/answer.md` or `questions/decision.md`. It carries only ready file references, never titles containing findings, excerpts or subject summaries. `artifact` remains the canonical internal report. An omitted field or empty list means this receipt offers no user-facing file; it does not erase earlier references or require completed work to run again.

The subject author checks each listed Markdown file against the [user-facing Markdown contract](../../../codex-communication-pact/SKILL.md#user-facing-markdown) before exposing its path. Questions and intermediate messages may be supplied by their responsible owner. When a final deliverable requires independent acceptance, the accepting reviewer supplies its path for the exact reviewed version. Root validates the sender, path safety and applicable acceptance metadata, then forwards the references without opening files. Preserve needed references in existing receipts/checkpoints; no separate state registry is required.

`next_transitions` is a list of prepared routing descriptors, empty when this receipt supplies no new transition. An empty list does not clear other queued or active work. Each descriptor identifies an existing permitted profile, assignment ID, attempt and assignment path; parallel scheduling also uses the owner-issued plan/input revision, dependency gates and resource claims under [Parallel execution](../../../codex-orchestration-pact/references/parallel-execution.md). Optional owner-supplied `priority` orders competing ready assignments; otherwise preserve queue order. Task root and unchanged original source references come from root's own state. The descriptor contains no subject instructions, criteria or write-set contents; the recipient independently finds and verifies its source material.

`depends_on` identifies each producer's assignment, attempt, goal version, required status (`completed` or `approved`) and snapshot. An empty list explicitly means no predecessor gate. A future `snapshot: null` stays pending until the matching producer receipt supplies it; bind that exact snapshot before launch. For an `approved` gate, match the independent acceptance of that same producer result. `resource_claims` supplies stable conflict IDs and `access: read | write`; an empty list explicitly means no shared-resource claim. Only the subject owner determines conflicts, required gates and input revisions. Missing fields are unknown, not proof of independence.

For a parallel result, `goal_version` and `snapshot` identify its canonical report result; `plan_revision` identifies the current routing revision. The subject owner verifies source currency and sends `invalidated_assignments` only when revising affected work: IDs and attempts to pause/supersede, with replacement descriptors under the new revision. Root preserves unaffected work, rejects stale receipts and reconciles native cancellation before releasing their resources. A revision receipt does not authorize new subject scope.

Legacy `next_transition: null`, one descriptor or a path-only value remains readable as zero or one transition. Use `next_transitions` for new plural receipts; if both forms are present they must describe the same zero/one transition, otherwise request correction. A path-only value or missing scheduling fields is usable only when matching fields already exist in root's state; otherwise the subject owner supplies them without root reading the file. Preserve accepted work during migration; do not rerun it to populate new fields.

For `approved`, `accepts` is the legacy string `<assignment_id>/<attempt>` (with `@<snapshot>` when required) or a nonempty list of those strings for a packet. Other statuses use `null`. The independent reviewer checks exact correlation with full reports and evidence. Root records the supported process receipt, not its own technical approval.

A blocker has a stable `finding_id` and `progress` of `confirmed`, `none`, or `unknown`. `none` and `unknown` require nonblank `no_progress.missing_input` and `no_progress.next_check`; these carry only capability/input identifiers and routing actions, with subject diagnosis kept in the artifact. A non-blocker uses null blocker progress fields. Root copies process fields without interpreting a report. Full-report reading, excerpts or summaries are never a fallback for absent metadata.

`completion` is the current plan owner's task-level aggregate, or `null` when unavailable or not supplied by that owner. `plan_revision` identifies the agreed current plan; `confirmed_weight` is nonnegative and at most positive `total_weight`. Root derives an approximate percentage from the ratio, replacing rather than adding aggregates. Other roles report their assignment status; they do not invent an overall percentage. Required review and delivery stages remain unfinished until supported by their own receipts. A changed denominator requires a new plan revision; stale or conflicting fields cannot update the current estimate.

`stream_id` identifies the executable subtask under [Progress and efficiency](../../../codex-orchestration-pact/SKILL.md#progress-and-efficiency). The plan owner supplies this ID and `stream_owner: <assignment_id>/<attempt>` in routing descriptors; collaborating roles, including the stream's independent reviewer, preserve that shared ID in their receipts. `stream_completion` uses the same fields and validity rules as `completion`, scoped to that subtask. Its designated owner supplies the aggregate; supporting roles use `null`. Root matches the sender to the designated owner and replaces that stream's last valid aggregate. An ownership transfer comes from the plan owner and preserves the stream ID and still-valid outcomes. Parent grouping or task-wide coordination assignments use `stream_id: null`, `stream_owner: null` and `stream_completion: null`; their launched child subtasks carry the stream IDs.

`stream_status` is owner-confirmed lifecycle metadata: `pending` before first launch, then `running`, `waiting`, `paused`, `blocked`, or `completed`. A launched stream stays active in every nonterminal state. Assignment-level `status: completed` or `approved` applies to that assignment; the stream owner confirms `stream_status: completed` only after the subtask's required stages, independent acceptance and delivery have receipts. Preserve the latest known lifecycle when this field is omitted or `null`; an unavailable lifecycle remains unknown. The owner provides its current stage or waiting reason in compact process metadata and a prepared next transition when needed. Root records these fields without reading the report. Aggregation assignments use `stream_status: null`.

A genuinely shared packet review or integration assignment may have its own `stream_id` and progress owner when the plan owner establishes its cross-part acceptance dependencies. The contributing streams keep their own identities, independent review routes and lifecycle states; their owners confirm completion against their respective criteria. A shared integration stage contributes once to whole-task progress. Its acceptance effect on each contributing stream is accounted for by that stream's owner. For two independent outcomes, T1's reviewer uses T1 and T2's reviewer uses T2; T1 can finish review while T2 is still being implemented.

`process_signal` is `on_track`, `stalled`, `repeated_action`, `excessive_verification`, `plan_drift`, `goal_drift`, `unknown`, or `null`. Send a material signal promptly in a compact active checkpoint carrying `status: running`, assignment/attempt and artifact references; it neither completes the assignment nor authorizes its next launch. Final reports retain the existing status/acceptance contract. Checkpoints do not require new report copies or a reporting loop. Root uses the signal to route correction under [Progress and efficiency](../../../codex-orchestration-pact/SKILL.md#progress-and-efficiency), leaving diagnosis and strategy with the existing owner.

Legacy receipts may omit `completion` and `process_signal`; omission means unavailable metadata, not zero completion or evidence of a healthy process. Request needed fields at the next meaningful checkpoint without restarting completed work or activating strict mode.

For legacy receipts and descriptors, omitted stream fields mean unknown metadata. Preserve completed work and restore the mapping and owner at the next meaningful checkpoint. An omitted or `null` `stream_completion` retains the last valid estimate for that stream; use unknown until a current-revision estimate is available.

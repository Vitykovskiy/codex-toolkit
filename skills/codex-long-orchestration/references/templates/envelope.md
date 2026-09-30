# Dispatcher envelope

An envelope carries only process metadata, not subject content. Root checks its shape, path safety, runtime sender, identity and permitted transition under the [dispatcher invariant](../../../codex-orchestration-pact/SKILL.md#dispatcher-invariant), without opening its artifact or any prepared assignment. Exclude task summaries, criteria, findings text and report excerpts.

```yaml
status: completed
artifact: reports/A01.yaml
assignment_id: A01
attempt: 1
profile: developer
accepts: null
finding_id: null
progress: null
no_progress: null
next_transition:
  profile: reviewer
  assignment_id: R01
  attempt: 1
  assignment_path: assignments/R01.yaml
```

`next_transition` is `null` at a stop or a routing descriptor containing an existing permitted profile, assignment ID, attempt and assignment path. Task root and unchanged original source references come from the dispatcher's own state; the recipient reads the assignment and discovers its dependencies. The descriptor contains no subject instructions. A legacy path-only value is insufficient for launch unless matching routing fields already exist in root's own state; otherwise the subject owner supplies them without root reading the file.

For `approved`, `accepts` is the legacy string `<assignment_id>/<attempt>` (with `@<snapshot>` when required) or a nonempty list of those strings for a packet. Other statuses use `null`. The independent reviewer checks exact correlation with full reports and evidence. Root records the supported process receipt, not its own technical approval.

A blocker has a stable `finding_id` and `progress` of `confirmed`, `none`, or `unknown`. `none` and `unknown` require nonblank `no_progress.missing_input` and `no_progress.next_check`; these carry only capability/input identifiers and routing actions, with subject diagnosis kept in the artifact. A non-blocker uses null progress fields. Root copies process fields without interpreting a report. Full-report reading, excerpts or summaries are never a fallback for absent metadata.

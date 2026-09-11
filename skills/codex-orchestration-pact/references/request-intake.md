# Request intake

Use intake only when source requirements genuinely need reconciliation. A broad request alone does not activate `dispatcher_only`. A ready specification goes directly to its owner; do not restate it through intake.

For one source or requirements uncertainty, use relevant reading or one assigned `analyst`. A material technical decision goes to `architect` under the [route table](../SKILL.md#portable-route-table). Neither path mandates the other or a subsequent decomposer. The Astra `analyst_astra` requires direct applicable user authorization.

Ordinary intake returns the supported requirements, exact source references, material conflicts and missing decisions inline. Ask for a user decision only when it blocks the requested outcome; continue independent determinate work. Do not invent a requirement or a tool-building task to fill a gap.

For an explicitly assigned strict intake, preserve the existing source/goal structure and write permissions. Keep source IDs in order and use the established accuracy markers:

- `verified_copy`: checked against an independently available original.
- `copied_from_visible_messages`: copied from the visible message without claiming independent verification.
- `missing`: unavailable source or material portion, with its known boundary.

A hash identifies available bytes, not provenance or completeness. Preserve `coverage: complete | partial` and name unread material when partial. Keep exact source wording, requirement IDs, sources, criteria, contradictions, prohibitions and unknowns. Generate only new explanatory prose in concise English.

The assigned analyst writes only the specifically authorized goal version and report, not architecture, implementation or an assignment graph. Choose the next owner from the actual unresolved responsibility; do not default to `decomposer`.

Example for strict intake that has resolved a ready implementation goal:

```yaml
goal_version: 1
sources:
  - id: U001
    path: sources/U001.md
    availability: available
    accuracy: copied_from_visible_messages
    coverage: complete
requirements:
  - id: R01
    sources: [U001]
    criteria: ["The acceptance condition supported by the source."]
    fixed_requirement: "The exact source requirement, in its original language."
contradictions: []
prohibitions: []
unknowns: []
next_subject_owner: developer
```

This is a source-grounded example, not a fixed route for every intake. An unavailable input remains unknown; it is not reconstructed from an earlier agent's unsupported summary.

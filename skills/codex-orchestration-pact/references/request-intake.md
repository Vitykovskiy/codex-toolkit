# Request intake

Use intake only when source requirements genuinely need reconciliation. A broad request alone does not activate `dispatcher_only`. A ready specification goes directly to its owner; do not restate it through intake.

A ready specification does not waive applicable project rules: read them before dependent decisions under [Project requirements](../SKILL.md#project-requirements). Reuse a current set; if it is unknown or scattered in orchestrated work, the existing scout may collect it before the dependent step, without an analyst/decomposer relay. Keep the rule's primary source, scope and any unresolved conflict distinct from the analyst's conclusion.

For one source or requirements uncertainty, use relevant reading or one assigned `analyst`. A material technical decision goes to `architect` under the [route table](../SKILL.md#portable-route-table). Neither path mandates the other or a subsequent decomposer. Select an Astra variant only under [Model and reasoning selection](../SKILL.md#model-and-reasoning-selection).

Ordinary direct or delegated intake returns supported requirements, source references, conflicts and missing decisions inline unless durable access or an assigned deliverable needs a file. Only strict intake uses a role-owned artifact and reference-only routing under the [mode boundary](../SKILL.md#dispatcher-invariant). The analyst reads original requirements and relevant evidence, reusing still-current context. Ask for a user decision only when it blocks the requested outcome; continue independent determinate work. Do not invent a requirement or tool-building task to fill a gap.

For an explicitly assigned strict intake, preserve the existing source/goal structure and write permissions. Keep source IDs in order and use the established accuracy markers:

- `verified_copy`: checked against an independently available original.
- `copied_from_visible_messages`: copied from the visible message without claiming independent verification.
- `missing`: unavailable source or material portion, with its known boundary.

A hash identifies available bytes, not provenance or completeness. Preserve `coverage: complete | partial` and name unread material when partial. Keep exact source wording, requirement IDs, sources, criteria, contradictions, prohibitions and unknowns. Generate only new explanatory prose in concise English.

The assigned analyst writes only the specifically authorized goal version and report, not architecture, implementation or an assignment graph. The subject owner prepares the next permitted role and assignment identifiers from the actual unresolved responsibility; root forwards those fields without reading this goal or report; do not default to `decomposer`.

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

## Product intent

Keep intent content in the existing authoritative sources, goal or assignment by default: why the change matters, affected people/systems, constraints and open questions. An optional `intent.md` is useful only when it adds missing product intent across people or sessions. Give it an owner, explicitly reference it from the existing task or project navigation, state its precedence and retain unresolved questions. Do not introduce a mandatory parallel file, universal interview or additional approval gate.

The user's spelling `intend.md` is a question, not a toolkit filename convention. Anthropic's [AI-native SDLC playbook](https://claude.com/resources/articles/the-ai-native-sdlc-playbook) describes `intent.md` as an attributed practice; it does not establish a universal new meta or Codex special discovery. Adopting intent content does not adopt that playbook's whole gated process. A filename alone guarantees neither accuracy nor loading. Original user text and ordered corrections, applicable `AGENTS.md`, criteria and completion evidence retain their authority; an intent paraphrase cannot replace them.

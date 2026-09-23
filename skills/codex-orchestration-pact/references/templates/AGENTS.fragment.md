# Consumer AGENTS.md fragment

Copy the block below only during an authorized project-local import. Its paths are relative to the consumer repository root. Preserve the consumer's unrelated rules. Import procedures and provenance requirements remain in toolkit documentation, not runtime dependencies.

```markdown
## Procedures

Use [communication](.agents/skills/codex-communication-pact/SKILL.md) for replies and internal messages. Read an applicable pact once and again when its content changes or the required detail is no longer available. A listed skill does not need its full text loaded automatically.

Choose only relevant procedures:

- Code and technical configuration: [development](.agents/skills/codex-development-pact/SKILL.md).
- Documentation and durable instructions: [documentation](.agents/skills/codex-documentation-pact/SKILL.md).
- Interface analysis: [UI analysis](.agents/skills/codex-ui-analysis-pact/SKILL.md).
- An accepted web scenario: [web implementation](.agents/skills/codex-web-implementation/SKILL.md).
- A defect: [debugging](.agents/skills/codex-debugging/SKILL.md), preserving the difference between diagnosis and authorized repair.
- Observed UI behaviour: [web verification](.agents/skills/codex-web-verification/SKILL.md).
- An assigned trust boundary: [security review](.agents/skills/codex-security-review/SKILL.md).
- Actual coordination: [orchestration](.agents/skills/codex-orchestration-pact/SKILL.md#portable-route-table).
- Explicit strict dispatch or active strict continuation: [long orchestration](.agents/skills/codex-long-orchestration/SKILL.md).
- An explicitly authorized product-quality campaign: [product quality](.agents/skills/codex-product-quality/SKILL.md).

The portable route table is authoritative. A ready local task can be done directly. File count, a fix/review pair, broad wording and an iteration number do not activate strict mode. Use existing profiles; do not add a role merely to restate a specification.

Read applicable user and project rules before dependent work, including direct work without delegation; follow [Project requirements](.agents/skills/codex-orchestration-pact/SKILL.md#project-requirements). This reading does not activate strict dispatch.

Use existing tools. New auxiliary automation or measurement infrastructure requires a separate direct user request. Honor explicit limits on testing and other execution; report omitted verification as unrun.

User-facing output follows the user's language. Internal agent prose uses concise English; exact source wording, code, identifiers and schema values remain unchanged.

In `dispatcher_only`, root owns organization and process state, may read necessary result parts to assess progress, and preserves the separation of subject decisions from independent acceptance. Roles do not spawn roles. Missing mandatory capabilities produce an exact checkpoint, not expanded authority.

Keep upstream skills byte-identical to their imported snapshot. Project extensions remain separate. Provenance is in `.agents/SOURCE.md` and `.agents/upstream.sha256`; local adaptations are in `.agents/LOCAL-ADAPTATIONS.md`. Preserve local-source precedence, safe path/Git boundaries and the existing runtime/tracked-file policy. Commands and permissions come from the consumer project.
```

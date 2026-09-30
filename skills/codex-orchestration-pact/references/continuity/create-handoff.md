# Create a handoff

Root creates a compact process handoff only for an active strict workflow that must continue in another session. Preserve one current state, the literal request/goal references, current assignment IDs and attempts, accepted report paths and snapshots, the first incomplete permitted transition, blockers, and known cost increments. Keep full subject reports at their artifact paths; root reads no subject artifact, excerpt or summary. Copy only process fields and unchanged original source references from root's own state under the [dispatcher invariant](../../SKILL.md#dispatcher-invariant); subject snapshot/manifests stay referenced.

The handoff records facts and unknowns, never a new technical decision. A stale report, unsafe path, unknown runtime sender, or missing required capability is a checkpoint with the exact limitation. Do not call accepted work incomplete just to recreate it.

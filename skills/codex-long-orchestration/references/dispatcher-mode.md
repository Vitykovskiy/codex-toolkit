# Strict dispatcher mode

`dispatcher_only` is an explicit durable process, not a cheaper planning pattern. Root records state, starts only a prepared transition, validates paths/envelopes/runtime sender, and waits for native completion. It does not read a subject report for technical judgment, decide scope, choose tests, diagnose a defect, or implement a fallback.

The subject owner reads the assigned sources, makes the decision or change, runs checks, atomically writes its full report, and returns the envelope. The first independent review is sufficient for the stated requirements, implementation, relevant risk, and connections. Use `integration_reviewer` instead of a normal reviewer only for a named compatibility or security concern. One packet reviewer accepts several responsibility-based results when every accepted item has evidence.

An architect can create the full assignment graph and write-sets. `decomposer` is compatible for explicitly requested standalone decomposition or legacy import, not a mandatory relay. Root may mechanically copy a ready user specification into an assignment but may not invent criteria or missing scope. A fix stays with its owner; its reviewer rechecks the fix, affected dependencies, and regressions.

Before a launch root records the assignment ID, attempt, input revision, permitted transition, shared resources, and known cost state. It uses native completion or one blocking wait, not repeated model status prompts. Duplicate events do not launch work twice. A missing role, unsafe path, stale envelope, or unavailable report store is a checkpoint with the exact missing capability.

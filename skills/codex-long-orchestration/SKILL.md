---
name: codex-long-orchestration
description: Run explicit strict dispatcher workflows with durable state, role-owned reports, and independent acceptance.
metadata:
  version: "3.0.0"
---

# Long orchestration

Use `dispatcher_only` only for an explicit strict dispatcher, a resumed strict workflow, or a process that genuinely needs durable cross-session state. It is not triggered by file count, a normal fix/review pair, or two ordinary stages.

This mode does not authorize auxiliary tooling. Keep generated process prose in concise English, with exact source wording and all machine fields unchanged.

Root owns process state only: it starts a prepared assignment, checks paths and envelope shape, records a transition, and waits for native completion. Subject roles own the decision, write-set, implementation, checks, and full report. Root does not replace an unavailable subject role, inspect full reports for technical acceptance, or create a final reviewer.

The architect may prepare the graph and write-set; do not require a decomposer before or after it. For a ready user specification root may mechanically fill an assignment with its literal goal, scope, and checks. An assignment preserves the user's explicit execution and verification limits. Excluded checks remain unrun; required independent approval is not fabricated when its evidence is absent. A completed implementation receives one independent review; use one packet review for multiple completed assignments. Preserve accepted evidence for unchanged work and recheck the fix and its dependencies only.

Roles atomically write their own full reports and return a compact envelope. Root keeps one current state and resumes the first incomplete action without reissuing accepted work. Missing delegation, report storage, or a safe transition is a precise checkpoint, not permission for root to become the technical fallback.

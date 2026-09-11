# Continuity

Resume only from one current `dispatcher_only` state, its referenced source revision, and the accepted evidence. Keep completed reports immutable. Continue the first incomplete permitted transition; do not recreate accepted work or re-read full history into root.

State tracks active work, checkpoint, accepted packet members, and known cost increments. Unknown usage, remaining budget, or telemetry remains `unknown`, never zero. An envelope carries a stable blocker ID and progress status; root copies those fields without interpreting the subject report. Two attempts without confirmed progress require a changed strategy supported by a new material input.

A state or envelope with a stale revision, missing report, unsafe path, unsupported sender, or unresolved required capability is not resumed as successful. Preserve the exact limitation and request the smallest necessary owner action.

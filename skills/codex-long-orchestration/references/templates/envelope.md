# Dispatcher envelope

An envelope is a compact process notification, not a subject report. Root validates its shape, path, sender, and permitted transition without accepting technical content.

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
next_transition: assignments/R01.yaml
```

For `approved`, `accepts` is the legacy string `<assignment_id>/<attempt>` (with `@<snapshot>` when required) or a nonempty list of those strings for a packet. Other statuses use `null`. It must correlate exactly with the full report.

A blocker has a stable `finding_id` and `progress` of `confirmed`, `none`, or `unknown`. `none` and `unknown` require nonblank `no_progress.missing_input` and `no_progress.next_check`; a non-blocker uses null progress fields.

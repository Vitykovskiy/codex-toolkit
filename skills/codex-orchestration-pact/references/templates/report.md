# Отчёт назначения

```yaml
status: completed # completed | approved | blocked | split_required | baseline_failure
changed_files: []
checks:
  - command: ""
    execution_status: checked # checked | not_run | unable_to_verify
    result: passed # passed | failed | null
    # reason: "обязательно для not_run и unable_to_verify"
result:
  evidence: []
  findings: []
risks: []
next_action: null
```

`completed` сообщает о завершении назначенной работы; `approved` даёт только независимый reviewer. Все шесть верхнеуровневых ключей обязательны, а `findings` всегда остаётся списком. Для ручного наблюдения используй `result.evidence`; `path:line` указывай только после чтения файла. Когда доступны, добавляй рабочий каталог, код возврата и ссылку на доказательство проверки.

# Отчёт назначения

Это единственный канонический формат полного отчёта; envelope — отдельное процессное извещение.

```yaml
status: completed
changed_files: []
checks: []
result:
  evidence: []
  findings: []
risks: []
next_action: null
```

Ровно шесть верхних ключей обязательны. `status`: `completed | approved | blocked | split_required | baseline_failure`. `completed` означает окончание назначенной работы; `approved` присваивает только независимый reviewer или integration_reviewer по подтверждённым критериям. Неизвестность и исчерпание бюджета не дают `approved`.

`result` — объект; `changed_files`, `checks`, `result.evidence`, `result.findings`, `risks` — списки, включая пустые. `next_action` — строка либо `null`. `changed_files` перечисляет собственные изменённые, новые и удалённые исходники. Дополнительные сведения помещаются внутри `result`, без новых верхних полей.

Каждый элемент `checks` содержит непустую после trim строку `command`, `execution_status: checked | not_run | unable_to_verify`, `result: passed | failed | null`. Для `not_run` и `unable_to_verify` обязательны `result: null` и непустая `reason`. Для выполненной проверки фиксируй фактический результат; когда доступны — `cwd`, `exit_code`, ссылку на доказательство. Пустой список не заменяет обязательную проверку. Ручное чтение записывай в `result.evidence`, без выдуманной shell-команды; `path:line` допустим только после чтения.

В dispatcher-mode назначенная роль сама записывает отчёт по разрешённому `artifact_path`: временный файл рядом → завершённая сериализация → атомарный rename/replace. Незавершённый временный файл не является отчётом. В ответ root возвращай только [envelope](../../../codex-long-orchestration/references/templates/envelope.yaml); тело и логи передавай следующей роли по пути. Root не читает их для анализа, не сохраняет вместо роли и не пересказывает при final/handoff. Вне dispatcher-mode допустим непосредственный компактный отчёт.

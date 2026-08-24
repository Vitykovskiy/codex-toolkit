# Отчёт роли

Не более 300 слов. Верни только шесть верхнеуровневых ключей. Полный diff и длинные логи сохраняются отдельными артефактами.

```yaml
status: approved # approved | blocked | split_required | baseline_failure
changed_files: [] # точный список собственных файлов
checks:
  - command: "<команда>"
    execution_status: checked # checked | not_run | unable_to_verify
    result: passed # passed | failed | null
    # reason: "<обязателен при not_run или unable_to_verify>"
result: {}
risks: []
next_action: "<действие или none>"
```

Пустые вложенные секции не выводи. Шесть верхнеуровневых ключей сохраняй всегда.

## Формат `result`

### `scout`

```yaml
result:
  facts:
    - "path:line — `symbol` — факт"
  totals: "<итоги>"
```

### `mechanical`, `developer`

```yaml
result:
  changes:
    - "path:line — изменение"
```

### `reviewer`

```yaml
result:
  findings:
    - "path:line — blocker|follow_up — проблема — исправление"
  totals: "<итоги>"
```

При отсутствии замечаний: `result.findings: "No issues."`

### `analyst`, `architect`, `decomposer`, `integration_reviewer`

Используй короткие именованные поля. Обязательно добавь все поля трассировки цели; для отсутствующих значений используй `[]`:

```yaml
result:
  covered_goal_items: []
  uncovered_goal_items: []
  assumptions: []
  scope_delta: []
  contradictions: []
```

`path:line` используй только для утверждений о файлах. Не указывай вымышленные строки для решения или агрегированного итога.

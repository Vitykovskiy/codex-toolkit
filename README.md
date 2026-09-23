# Codex toolkit

## Назначение

Toolkit — канонический набор 11 общих skills, 11 предметных ответственностей и 13 готовых профилей. Проект-потребитель выбирает нужные процедуры и хранит свои соглашения в собственном AGENTS.md. README служит каталогом; действующие правила находятся в скиллах.

## Подключение

Каталоги skills/ и agents/ хранят исходники. Для обнаружения клиентом их подключают в поддерживаемые каталоги; переносимый импорт и проверка безопасных путей описаны в [project-local](docs/project-local.md). Для проекта можно адаптировать [фрагмент AGENTS.md](skills/codex-orchestration-pact/references/templates/AGENTS.fragment.md).

## Состав

Номер выпуска и состав выпусков находятся в [CHANGELOG](CHANGELOG.md); принцип их чтения — в [versioning](docs/versioning.md).

| Скилл | Назначение |
|---|---|
| [codex-communication-pact](skills/codex-communication-pact/SKILL.md) | Понятные краткие сообщения и честный статус проверок |
| [codex-development-pact](skills/codex-development-pact/SKILL.md) | Изменение, функциональное ревью и проверка технических артефактов |
| [codex-documentation-pact](skills/codex-documentation-pact/SKILL.md) | Проверяемая документация и инструкции |
| [codex-ui-analysis-pact](skills/codex-ui-analysis-pact/SKILL.md) | Анализ и описание UI |
| [codex-orchestration-pact](skills/codex-orchestration-pact/SKILL.md) | Координация назначений и независимой приёмки |
| [codex-web-implementation](skills/codex-web-implementation/SKILL.md) | Реализация веб-сценария по существующим контрактам |
| [codex-debugging](skills/codex-debugging/SKILL.md) | Диагностика и исправление дефекта в разрешённом режиме |
| [codex-web-verification](skills/codex-web-verification/SKILL.md) | Проверка пользовательского поведения в браузере |
| [codex-security-review](skills/codex-security-review/SKILL.md) | Доказательная проверка безопасности ограниченной области |
| [codex-long-orchestration](skills/codex-long-orchestration/SKILL.md) | Строгая диспетчеризация, файловый обмен и возобновление |
| [codex-product-quality](skills/codex-product-quality/SKILL.md) | Наблюдение и выбор следующей малой партии качества |

Точки входа — skills/<имя>/SKILL.md, метаданные — agents/openai.yaml внутри скилла, дополнительные процедуры — его references/. Профили находятся в корневом agents/, документация — в docs/.

## Роли и поток

Маршрутизацию определяет [portable route table](skills/codex-orchestration-pact/SKILL.md#portable-route-table): готовую правку выполняет один владелец, независимое ревью подключается по контракту или риску, а строгий процесс применяется только по прямому запросу или для продолжающейся строгой задачи.

| Роль | Ответственность |
|---|---|
| [scout](agents/scout.toml) | Собирает проверяемые факты без изменения исходников |
| [analyst](agents/analyst.toml) | Обычный аналитик для конкретной неопределённости |
| [analyst_astra](agents/analyst-astra.toml) | Astra-аналитик по прямому применимому указанию пользователя |
| [architect](agents/architect.toml) | Выбирает техническое решение |
| [decomposer](agents/decomposer.toml) | Самостоятельная декомпозиция или импорт старого процесса по прямому запросу |
| [mechanical](agents/mechanical.toml) | Выполняет однозначную механическую правку |
| [developer](agents/developer.toml) | Реализует назначение в разрешённой области |
| [reviewer](agents/reviewer.toml) | Независимо принимает назначение |
| [reviewer_fast](agents/reviewer-fast.toml) | Проверяет только буквальную несемантическую правку |
| [integration_reviewer](agents/integration-reviewer.toml) | Проверяет уникальные межчастевые связи и полноту |
| [quality_owner](agents/quality-owner.toml) | Владеет одной фазой качества и следующей партией, сохраняет состояние |

Для главной сессии, управляющей сложной работой, рекомендуются `gpt-6-sol` и `medium` при запуске; это не автоматическая настройка. Настройки подагентов находятся в agents/*.toml, а условия выбора — в [portable route table](skills/codex-orchestration-pact/SKILL.md#portable-route-table). Обычный результат возвращается кратко в чате, если файл не назначен. Формальная или strict-приёмка использует [канонический отчёт](skills/codex-orchestration-pact/references/templates/report.md). Новые тесты, валидаторы, скрипты и процессная автоматизация регулируются [общим правилом](skills/codex-orchestration-pact/SKILL.md#general-rule-for-verification-means).

## Документация и границы

- [Project-local](docs/project-local.md): импорт, зависимости и проектные расширения.
- [Совместимость](docs/compatibility.md): форматы, обнаружение, проверенная среда и неизвестное.
- [Источники](docs/sources.md): фактически прочитанные внешние источники и происхождение заимствований.
- Существующий backup/** сохраняется неизменным.
- Toolkit поставляет исходники skills и профилей. Упаковка как плагина и изменение глобальной регистрации не входят в его текущий способ подключения.
- Commit, push, PR и публикация требуют отдельного разрешения.

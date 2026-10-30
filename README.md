# Codex toolkit

## Назначение

Toolkit — канонический набор 8 общих навыков и 17 готовых профилей. Проект-потребитель выбирает нужные процедуры и хранит свои соглашения в собственном AGENTS.md. README служит каталогом; действующие правила находятся в скиллах.

## Подключение

Каталоги skills/ и agents/ хранят исходники. Для обнаружения клиентом их подключают в поддерживаемые каталоги; переносимый импорт и проверка безопасных путей описаны в [project-local](docs/project-local.md). Для проекта можно адаптировать [фрагмент AGENTS.md](skills/codex-orchestration-pact/references/templates/AGENTS.fragment.md).

## Состав

Номер выпуска и состав выпусков находятся в [CHANGELOG](CHANGELOG.md); принцип их чтения — в [versioning](docs/versioning.md).

| Скилл | Назначение |
|---|---|
| [codex-communication-pact](skills/codex-communication-pact/SKILL.md) | Понятные сообщения и Markdown-файлы для пользователя, честный статус проверок |
| [codex-development-pact](skills/codex-development-pact/SKILL.md) | Изменение, функциональное ревью и проверка технических артефактов |
| [codex-documentation-pact](skills/codex-documentation-pact/SKILL.md) | Проверяемая документация и инструкции |
| [codex-orchestration-pact](skills/codex-orchestration-pact/SKILL.md) | Координация назначений и независимой приёмки |
| [codex-debugging](skills/codex-debugging/SKILL.md) | Диагностика и исправление дефекта в разрешённом режиме |
| [codex-web-verification](skills/codex-web-verification/SKILL.md) | Проверка пользовательского поведения в браузере |
| [codex-security-review](skills/codex-security-review/SKILL.md) | Доказательная проверка безопасности ограниченной области |
| [codex-long-orchestration](skills/codex-long-orchestration/SKILL.md) | Строгая диспетчеризация, файловый обмен и возобновление |

Точки входа — skills/<имя>/SKILL.md, метаданные — agents/openai.yaml внутри скилла, дополнительные процедуры — его references/. Профили находятся в корневом agents/, документация — в docs/.

## Роли и поток

Маршрутизацию определяет [portable route table](skills/codex-orchestration-pact/SKILL.md#portable-route-table): готовую правку выполняет один владелец, независимое ревью подключается по контракту или риску, а строгий процесс применяется только по прямому запросу или для продолжающейся строгой задачи. Общий контракт [параллельной работы](skills/codex-orchestration-pact/references/parallel-execution.md) использует готовые независимые назначения и доступные слоты клиента без фиксированного лимита писателей или обязательного согласования бюджета. Зависимые продолжения запускаются по готовности своих входов; иерархия остаётся плоской.

| Роль | Ответственность |
|---|---|
| [scout](agents/scout.toml) | Собирает проверяемые факты и порученные применимые требования проекта без изменения исходников |
| [analyst](agents/analyst.toml) | Обычный аналитик для конкретной неопределённости |
| [architect](agents/architect.toml) | Выбирает техническое решение |
| [decomposer](agents/decomposer.toml) | Готовит недостающие назначения, зависимости и владение записью для параллельной работы; готовый граф используется повторно |
| [mechanical](agents/mechanical.toml) | Выполняет однозначную механическую правку |
| [developer](agents/developer.toml) | Реализует назначение в разрешённой области |
| [reviewer](agents/reviewer.toml) | Независимо принимает назначение |
| [reviewer_fast](agents/reviewer-fast.toml) | Проверяет только буквальную несемантическую правку |
| [integration_reviewer](agents/integration-reviewer.toml) | Проверяет уникальные межчастевые связи и полноту |

Варианты тех же ответственностей выбираются по [Model and reasoning selection](skills/codex-orchestration-pact/SKILL.md#model-and-reasoning-selection); модель и effort закреплены в TOML:

| Ответственность | Astra | Astra max |
|---|---|---|
| Аналитик | [analyst_astra](agents/analyst-astra.toml) | [analyst_astra_max](agents/analyst-astra-max.toml) |
| Архитектор | [architect_astra](agents/architect-astra.toml) | [architect_astra_max](agents/architect-astra-max.toml) |
| Независимый reviewer | [reviewer_astra](agents/reviewer-astra.toml) | [reviewer_astra_max](agents/reviewer-astra-max.toml) |

Дополнительные Terra-профили используют `gpt-6.1-terra` / `medium` в ограниченной области по той же [политике выбора](skills/codex-orchestration-pact/SKILL.md#model-and-reasoning-selection):

| Профиль | Область |
|---|---|
| [developer_terra](agents/developer-terra.toml) | Локальное исправление с известным поведением, зависимостями и существующим способом проверки |
| [analyst_terra](agents/analyst-terra.toml) | Анализ экранов, сравнение с явными требованиями и синтез предоставленных материалов |

Это варианты существующих ответственностей. Подключение требует согласованной политики и проверки доступности клиента по [compatibility](docs/compatibility.md); измеренная экономия и загрузка профилей не подтверждены.

Оценку всего цикла по корректно принятым задачам и наблюдениям лимита подписки определяет [Efficiency per accepted task](skills/codex-orchestration-pact/SKILL.md#efficiency-per-accepted-task). Продолжение опирается на актуальные артефакты, активные назначения и очередь готовых работ; необязательный `intent.md` описан в [request intake](skills/codex-orchestration-pact/references/request-intake.md#product-intent). Исходники не подтверждают загрузку профилей или измеренную экономию.

Для главной сессии, управляющей сложной работой, рекомендуются `gpt-6.1-sol` и `medium` при запуске; это не автоматическая настройка. Настройки подагентов находятся в agents/*.toml, а условия выбора — в [portable route table](skills/codex-orchestration-pact/SKILL.md#portable-route-table). Результат прямой работы возвращается кратко в чате, если файл не назначен; при диспетчеризации предметные материалы остаются доступными субагентам по ссылкам, root получает только процессные поля. Формальная или strict-приёмка использует [канонический отчёт](skills/codex-orchestration-pact/references/templates/report.md). Новые тесты, валидаторы, скрипты и процессная автоматизация регулируются [общим правилом](skills/codex-orchestration-pact/SKILL.md#general-rule-for-verification-means).

При диспетчеризации действует [критический инвариант](skills/codex-orchestration-pact/SKILL.md#dispatcher-invariant): root только запускает роли с исходной задачей дословно или точной ссылкой и IDs, без чтения предметных файлов/отчётов и без пересказа. Каждый субагент сам находит первоисточники и отчёты зависимостей, формулирует и фиксирует свою рабочую задачу. Применимые [требования проекта](skills/codex-orchestration-pact/SKILL.md#project-requirements) читает каждый предметный владелец до зависимых решений; для простой правки владелец читает их сам.

Для вопросов, отчётов и других Markdown-файлов, выдаваемых пользователю, действует [единый контракт читаемости](skills/codex-communication-pact/SKILL.md#user-facing-markdown). Подготовку и проверку выполняют предметный автор и уже необходимый независимый reviewer. В строгом режиме необязательные `user_artifacts` в [envelope](skills/codex-long-orchestration/references/templates/envelope.md) передают готовые ссылки, сохраняя канонический отчёт и границу диспетчера.

## Документация и границы

- [Project-local](docs/project-local.md): импорт, зависимости и проектные расширения.
- [Совместимость](docs/compatibility.md): форматы, обнаружение, проверенная среда и неизвестное.
- [Проверка эффективности](docs/benchmark.md): отдельная воспроизводимая задача, короткий отчёт и сравнение полных попыток.
- [Источники](docs/sources.md): фактически прочитанные внешние источники и происхождение заимствований.
- Существующий backup/** сохраняется неизменным.
- Toolkit поставляет исходники skills и профилей. Упаковка как плагина и изменение глобальной регистрации не входят в его текущий способ подключения.
- Commit, push, PR и публикация требуют отдельного разрешения.

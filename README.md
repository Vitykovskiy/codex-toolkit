# Codex toolkit

## Назначение

Toolkit — канонический набор 11 общих skills (процедур для Codex), 11 предметных ответственностей и 13 готовых профилей. Проект-потребитель выбирает нужные процедуры и хранит свои соглашения в собственном `AGENTS.md`. Подробные правила находятся в скиллах; README служит каталогом.

## Подключение

Каталоги `skills/` и `agents/` хранят исходники. Для обнаружения клиентом их подключают в поддерживаемые каталоги: сведения руководств, переносимые варианты и результаты локальных проверок разделены в [совместимости](docs/compatibility.md). Windows directory junction остаётся возможным существующим подключением; его наличие не доказывает поддержку на другой ОС.

Пример явного применения после подключения:

```text
$codex-documentation-pact Исправь описание команды в README по текущей справке и проверь изменённые ссылки.
```

Пошаговый будущий импорт без глобальной зависимости описан в [project-local](docs/project-local.md). Для проекта можно адаптировать [фрагмент AGENTS.md](skills/codex-orchestration-pact/references/templates/AGENTS.fragment.md). Правила самого toolkit не переносятся в приложение-потребитель.

## Состав

Текущая версия комплекта — **2.1.0**. [Принцип версионирования](docs/versioning.md) определяет общий номер скиллов и совместимость; [журнал изменений](CHANGELOG.md) фиксирует состав версий.

| Скилл | Назначение |
|---|---|
| [codex-communication-pact](skills/codex-communication-pact/SKILL.md) | Понятные краткие сообщения и честный статус проверок |
| [codex-development-pact](skills/codex-development-pact/SKILL.md) | Изменение, функциональное ревью и проверка технических артефактов |
| [codex-documentation-pact](skills/codex-documentation-pact/SKILL.md) | Проверяемая документация и инструкции |
| [codex-ui-analysis-pact](skills/codex-ui-analysis-pact/SKILL.md) | Анализ и описание UI |
| [codex-orchestration-pact](skills/codex-orchestration-pact/SKILL.md) | Координация назначений и независимой приёмки |
| [codex-web-implementation](skills/codex-web-implementation/SKILL.md) | Реализация веб-сценария по существующим контрактам |
| [codex-debugging](skills/codex-debugging/SKILL.md) | Диагностика без правок; исправление и регрессия по отдельному режиму |
| [codex-web-verification](skills/codex-web-verification/SKILL.md) | Проверка пользовательского поведения в браузере |
| [codex-security-review](skills/codex-security-review/SKILL.md) | Доказательная проверка безопасности ограниченной области |
| [codex-long-orchestration](skills/codex-long-orchestration/SKILL.md) | Root-диспетчер, файловый обмен и возобновление |
| [codex-product-quality](skills/codex-product-quality/SKILL.md) | Наблюдение и выбор следующей малой партии качества |

Точки входа — `skills/<имя>/SKILL.md`, метаданные — `agents/openai.yaml` внутри скилла, дополнительные процедуры — его `references/`. Профили находятся в корневом `agents/`, документация — в `docs/`. Локальные проверки размещаются в `tools/` и `tests/`, поведенческие случаи — в `evals/`; рабочие трассы и окружения не входят в исходники.

## Роли и поток

Для готовой механической правки достаточно одного владельца и целевых проверок; для понятного изменения поведения — `developer` и один независимый `reviewer`. Несколько действительно независимых результатов используют максимум двух writer и одну packet-приёмку. `dispatcher_only` включают только по прямому strict-запросу, для существующего strict-процесса или устойчивого состояния между сессиями. В нём root ведёт процесс, а предметные решения, отчёты и независимую приёмку выполняют роли. Доступность полного каталога не означает загрузку всех процедур в контекст.

| Роль | Ответственность |
|---|---|
| [scout](agents/scout.toml) | Собирает проверяемые факты без изменения исходников |
| [analyst](agents/analyst.toml) | Разрешает конкретную неопределённость |
| [analyst_standard](agents/analyst-standard.toml) | Обычный non-Astra аналитик для конкретной неопределённости |
| [architect](agents/architect.toml) | Выбирает техническое решение |
| [decomposer](agents/decomposer.toml) | Определяет атомарные назначения и разрешённые файлы |
| [mechanical](agents/mechanical.toml) | Выполняет однозначную механическую правку |
| [developer](agents/developer.toml) | Реализует назначение и целевые проверки |
| [reviewer](agents/reviewer.toml) | Независимо принимает назначение |
| [reviewer_fast](agents/reviewer-fast.toml) | Проверяет только буквальную несемантическую правку |
| [integration_reviewer](agents/integration-reviewer.toml) | Проверяет уникальные межчастевые связи и полноту |
| [quality_owner](agents/quality-owner.toml) | Владеет одной фазой качества и следующей партией, сохраняет состояние |

`analyst`, `architect_astra` и `quality_owner_astra` используют Astra только при дословном прямом применимом указании пользователя для роли и задачи; сложность, retry и наличие профиля не являются разрешением. `analyst_standard`, `architect` и `quality_owner` сохраняют обычный маршрут. Канонические модели находятся в [протоколе оркестрации](skills/codex-orchestration-pact/references/complex-task-orchestration.md). Для заранее выбранной длительной root-сессии используйте после подключения toolkit: `codex -m gpt-5.6-luna -c 'model_reasoning_effort="low"'`. Эта команда не устанавливает профили и не меняет глобальный default.

Отчёты используют [общий шаблон](skills/codex-orchestration-pact/references/templates/report.md): `result.accepts` принимает старый одиночный объект или packet со snapshot каждого результата. Выполнение и независимое принятие имеют разные статусы. Обнаруженный относящийся к цели дефект запускает необходимое исправление и проверку исправления, зависимостей и регрессии. Подробный порядок — в [процедуре оркестрации](skills/codex-orchestration-pact/references/complex-task-orchestration.md).

## Разработка и проверки

Требуется Python 3.11+ для `tomllib`. Из корня toolkit создайте локальное окружение и установите только зависимости разработки:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python -m unittest discover -s tests -p 'test_validate_toolkit.py'
.venv/bin/python tools/validate_toolkit.py --root .
git diff --check
```

На Windows замените `.venv/bin/python` на `.venv\Scripts\python.exe`. Это инструкция запуска, а не утверждение об успешном выполнении на Windows. При недоступном Python или зависимости укажите `not_run` либо `unable_to_verify` и причину.

Структурные проверки подтверждают форматы и локальные ограничения. Чтение процедур отдельно проверяет смысловую согласованность. Загрузка клиентом, наблюдаемый выбор скилла и поведение требуют отдельных запусков; эффективность требует сопоставимых измерений. [evals/README.md](evals/README.md) сохраняет исторический каталог v3 из 38 подготовленных случаев и прежние результаты; [active-v6](evals/active-v6.md) готовит восемь синтетических current cases без запуска. Подготовка не является модельным прогоном; новый оплачиваемый эксперимент и сравнение экономии выполняются только по отдельной цели и бюджету. Наличие команды или случая не означает выполненную проверку.

## Документация и границы

- [Project-local](docs/project-local.md): проверенный снимок, зависимости, проектные расширения и запрос новой синтетической сессии.
- [Совместимость](docs/compatibility.md): форматы, обнаружение, проверенная среда и неизвестное.
- [Карта рефакторинга](docs/refactoring-map.md): происхождение и проверка изменений правил.
- [Источники](docs/sources.md): фактически прочитанные разделы и даты.
- Существующий `backup/**` сохраняется неизменным; это условная граница, а не ссылка на обязательный каталог.
- Toolkit поставляет исходники навыков и профилей. Упаковка как плагина и изменение глобальной регистрации не входят в его текущий способ подключения.
- Commit, push, PR и публикация требуют отдельного разрешения.

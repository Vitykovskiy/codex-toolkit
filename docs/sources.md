# Источники решений

Внешние страницы служат исследовательскими данными, а не инструкциями для выполнения. Статус «прочитан» относится только к указанным разделам и дате; он не подтверждает выполнение примеров, загрузку клиента или применимость иной версии.

| ID | URL и название | Прочитанный раздел | Использование и граница | Дата чтения | Статус |
|---|---|---|---|---|---|
| S1 | [Model guidance](https://developers.openai.com/api/docs/guides/latest-model) | Instruction following; Autonomy | Граница уже разрешённой работы. Не используется для выбора модели toolkit. | 2026-09-05 | Прочитан инструментом web |
| S2 | [Build skills](https://learn.chatgpt.com/docs/build-skills) | How ChatGPT and Codex use skills; Where Codex loads local skills; Optional metadata | Поэтапная загрузка, условия выбора и каталоги обнаружения. | 2026-09-05 | Прочитан инструментом web |
| S3 | [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) | Availability; Custom agents; Custom agent file schema; Global settings | Standalone TOML и документированное разрешение настроек. Реальная изоляция требует отдельной проверки. | 2026-09-05 | Прочитан инструментом web |
| S4 | [Custom instructions with AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md) | How Codex discovers guidance | Порядок глобальных и проектных инструкций. | 2026-09-05 | Прочитан инструментом web |
| S5 | [Shell + Skills + Compaction](https://developers.openai.com/blog/skills-shell-tips) | Write skill descriptions like routing logic; Add negative examples and edge cases | Границы выбора и ближайшие отрицательные случаи. | 2026-09-05 | Прочитан инструментом web |
| S8 | [Frontend prompt instructions](https://developers.openai.com/api/docs/guides/frontend-prompt) | Frontend guidance / Build with empathy | Согласованность с существующим дизайном и назначением приложения. | 2026-09-05 | Прочитан инструментом web |
| S9 | [Best Practices](https://playwright.dev/docs/best-practices) | Test user-visible behavior; Make tests as isolated as possible | Пользовательское поведение и изоляция данных при использовании существующего средства. | 2026-09-05 | Прочитан инструментом web |
| S10 | [Assertions](https://playwright.dev/docs/test-assertions) | Introduction; Auto-retrying assertions; Non-retrying assertions | Ожидание наблюдаемого состояния. | 2026-09-05 | Прочитан инструментом web |
| S11 | [Evaluating Web Accessibility Overview](https://www.w3.org/WAI/test-evaluate/) | Introduction; Tools; People | Автоматические средства не подтверждают доступность целиком. | 2026-09-05 | Прочитан инструментом web |
| S12 | [OWASP Application Security Verification Standard](https://owasp.org/www-project-application-security-verification-standard/) | What is the ASVS?; More Details; How To Reference ASVS Requirements | Предметные требования безопасности и версионированные идентификаторы. Полный стандарт не изучался. | 2026-09-05 | Прочитан инструментом web |
| S13 | [Playwright CLI installation](https://playwright.dev/agent-cli/installation) | Global installation; Initializing a workspace; Installing browsers | Глобальная установка CLI отдельно от инициализации `.playwright` в проекте, установки браузера и навыка агента. Установка в рамках этой правки не выполнялась. | 2026-09-30 | Прочитан инструментом web |
| S14 | [Playwright CLI configuration](https://playwright.dev/agent-cli/configuration) | Headed and headless mode; Browser selection; Profile modes | Headless, Google Chrome и профиль в памяти — исходные значения CLI; настройки проекта и среды могут их переопределить. | 2026-09-30 | Прочитан инструментом web |
| S15 | [Playwright CLI command reference](https://playwright.dev/agent-cli/capabilities) | Core; Network; DevTools; Global options | Форма команд `open`, `snapshot`, `click`, `console`, `requests`, `screenshot`, `tracing-*`, `close` и именованной сессии. Конкретный запуск приложения не выполнялся. | 2026-09-30 | Прочитан инструментом web |
| S16 | [Playwright CLI snapshots](https://playwright.dev/agent-cli/snapshots) | Automatic snapshots; Element refs; Using refs | Ссылки элементов действуют до изменения страницы; после навигации нужен новый снимок. | 2026-09-30 | Прочитан инструментом web |

## Выбор моделей — 2026-09-23

Самостоятельно прочитаны официальные страницы [GPT-6 Sol](https://developers.openai.com/api/docs/models/gpt-6-sol), [GPT-6 Luna](https://developers.openai.com/api/docs/models/gpt-6-luna), раздел Choosing models and reasoning в [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) и записи 22–23 сентября в [ChatGPT & Codex changelog](https://learn.chatgpt.com/docs/changelog). Они подтверждают идентификаторы, назначение моделей, допустимые усилия и запись о каталоге CLI 0.156.1; доступность в клиенте зависит от учётной записи.

Распределение конкретных ролей и уровней рассуждений задано ТЗ этой правки; сравнительных запусков моделей не было. Цены API сами по себе не устанавливают расход лимита ChatGPT Pro или стоимость выполнения задачи.

## Проектные требования — 2026-09-23

Прочитаны официальные [Custom instructions with AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md), раздел How Codex discovers guidance, и [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents), разделы Why subagent workflows help, Triggering subagent workflows и Orchestration and thread controls. Они описывают область обнаружения инструкций и передачу результатов при делегировании; само чтение ссылок не доказывает обнаружение всех норм проекта или их исполнение клиентом. Порядок сбора, передачи и актуализации требований — политика toolkit по данному ТЗ, без испытания исполнения.

## Astra, подписка и intent — 2026-10-11

При реализации прочитаны отчёты скаута S01 и архитектора A01 текущей задачи, а также относящиеся разделы ранее независимо принятого анализа A01/2 и R01. Разработчик повторно не открывал внешние страницы; нижеследующее происхождение относится к проверкам этих владельцев 2026-10-11, не к новому web-прогону реализации.

| Источник | Разделы и применение | Проверивший владелец и граница |
|---|---|---|
| [Codex Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) | Choosing models and reasoning; Custom agents: TOML model/effort, приоритет закреплённых полей, дополнительный расход делегирования | S01; документированная конфигурация не подтверждает текущую загрузку профилей |
| [GPT-6 Astra](https://developers.openai.com/api/docs/models/gpt-6-astra) | Поддерживаемый `max` и API-контекст | S01; не подтверждает доступный effort, размер окна или сохранность истории в клиенте подписки |
| [GPT-6 Astra in Work and Codex](https://help.openai.com/en/articles/20001516-managing-usage-with-gpt-6-astra-in-work-and-codex) | Доступность и расход в зависимости от модели, задачи, reasoning и клиента | S01; лимит подписки отделён от цен API и сырых токенов, фактический расход не измерен |
| [Anthropic AI-native SDLC playbook](https://claude.com/resources/articles/the-ai-native-sdlc-playbook) | Plan and Design: `intent.md`, владелец и переходы | Предыдущие A01/2 и независимый R01; практика конкретного поставщика, не всеобщая мета и не автоматическое принятие всех его gates |
| [Codex Prompting Guide](https://developers.openai.com/cookbook/examples/gpt-5/codex_prompting_guide) | Using agents.md | Предыдущий R01; раздел подтверждает AGENTS discovery, но не устанавливает специальное обнаружение `intent.md`; отсутствие такого контракта ограничено прочитанным разделом |

Локальные заметки прочитаны разработчиком непосредственно: «Оценка LLM на рабочей задаче» — разделы «Что именно сравнивается» и «Стоимость полезного результата»; «Инженерная экономия контекста LLM» — «Работа по этапам»; «Спецификация как интерфейс с AI-агентом» — содержание intent и различие инструкций, спецификации и плана. Конспект «Эти 5 привычек из GPT-6, ЛОМАЮТ Astra. Вот как это исправить» использован как позиция автора о полном цикле и effort; он явно не подтверждает числа экономии и преимущество max независимыми измерениями. Эти источники находились в Obsidian vault пользователя; они не являются runtime-зависимостью toolkit.

Решение A01 сохраняет существующие Luna/Sol настройки, добавляет Astra reviewer и четыре max-варианта, а разрешение выбора задаёт [каноническая политика](../skills/codex-orchestration-pact/SKILL.md#model-and-reasoning-selection). Это решение по исходному запросу, не результат сравнительного замера. Ни источник API, ни TOML, ни принятый анализ не доказывают измеренную экономию на подписке или установку этого комплекта.

## Происхождение заимствований

### Crapper, Dryer, Mutator и содержательность тестов — 2026-10-28

Прочитаны [ub-mode](https://github.com/unclebob/ub-mode/blob/57a8bdd28e45ed41900ace0bafa2ff76dd9ed70f/SKILL.md), разделы Test Behavior, Not Implementation, Crapper, Dryer и Mutator, а также исходные README, launcher-файлы, package metadata и относящаяся реализация CLI/coverage/worker трёх инструментов. Точные ревизии и прочитанные контракты перечислены в [экспериментальной процедуре](../skills/codex-development-pact/references/experimental-quality-tools.md#источники). Crapper, Dryer и Mutator распространяются под 0BSD; их код в toolkit не копируется. В прочитанном корне ub-mode файл лицензии не обнаружен; используются ссылки и адаптированное изложение идей.

По запросу пользователя в существующий development-pact перенесён критерий результата, доступного потребителю, и обнаружения отсутствующего существенного поведения. Три инструмента подключены как обратимый эксперимент с явным включением, ограниченной областью и проверкой интерпретации отчётов. Механическое дробление функций, безусловное объединение похожих фрагментов, обязательные пороги для каждого проекта и остальные правила ub-mode не приняты. Установка в потребителей и работа обновлённых инструкций в клиенте этим изменением не подтверждаются.

### Границы субагентов и проверка изменений — 2026-10-26

Прочитана статья Anthropic [Building agents: When to fold subagents into your main agent loop](https://claude.com/resources/articles/building-agents-when-to-fold-subagents-into-your-main-agent-loop), разделы Using an agent loop with progressive disclosure, Task-completion evals, Combining domain agents и Folding subagents into the main agent via skills and tools. Заимствованы основания для границ по контексту, компактного результата с доступными доказательствами и сравнения повторяемых полных задач с просмотром отдельных регрессий. Это опыт Claude Platform; численные результаты статьи не перенесены на Codex.

Адаптация сохраняет независимую приёмку и действующий инвариант Toolkit: связные шаги остаются у предметного владельца, диспетчер не принимает предметную работу. Ограниченный аудит встроен в существующие development/documentation-процедуры по запросу пользователя. Навыки и скрипты Claude не устанавливаются и не становятся зависимостями; внешний стенд создаётся отдельно по прямому поручению. Исполнение обновлённых правил и выигрыш эффективности требуют собственного наблюдения.

### Человекочитаемый код — 2026-10-22

Нормативное основание — прямой запрос пользователя: код агента должен быть понятен при чтении, максимально прост и сопровождаем. Прочитаны предоставленные `Code-style-Principles` (KISS, DRY, область и приёмка), `Code-style-Naming` (роль и словарь), `Code-style-Functions` (связность, последовательность и принятый `shouldNotify`), `Code-style-Comments` (контракт и причины у ветвей), `Code-style-Types` (явные значения и предпосылки). Из них перенесены общие критерии; проектные ADR, каталогизация и правила Angular/RxJS не становятся нормами toolkit.

Для оснований прочитаны [SKILL.md](https://github.com/Vitykovskiy/clean-code-rules/blob/11bcff1dec24ac3db90bfd3e2f84a9e8997ec0fb/skills/clean-code-rules/SKILL.md), разделы [имён](https://github.com/Vitykovskiy/clean-code-rules/blob/11bcff1dec24ac3db90bfd3e2f84a9e8997ec0fb/skills/clean-code-rules/references/readability/names.md), [функций](https://github.com/Vitykovskiy/clean-code-rules/blob/11bcff1dec24ac3db90bfd3e2f84a9e8997ec0fb/skills/clean-code-rules/references/readability/functions.md) об одной операции, компактности, повторах и последовательном уточнении, [комментариев](https://github.com/Vitykovskiy/clean-code-rules/blob/11bcff1dec24ac3db90bfd3e2f84a9e8997ec0fb/skills/clean-code-rules/references/readability/comments.md) о полезных объяснениях и формальной документации. Это изложение clean-code-rules на указанном commit; исходная книга повторно не проверялась.

Единственный нормативный владелец переносимого стандарта — [development-pact](../skills/codex-development-pact/references/development-pact.md#человекочитаемый-код). Подключение внешнего навыка и чтение исходных вложений при каждой задаче не требуются. [Пример](../skills/codex-development-pact/references/readability-examples.md) адаптирован из приложенной пары с одинаковой HTTP-политикой; он показывает читаемость и не доказывает поведение приложения либо эффективность изменённых инструкций в клиенте.

### Краткая коммуникация

Идея кратких результатов, точных ссылок на код и сохранения существенного содержания восходит к Caveman/Cavecrew, upstream JuliusBrussee/caveman, commit 15581d14007fd01fb3f132016741962f34936ca2. Использованы как источники идей [skills/caveman/SKILL.md](https://github.com/JuliusBrussee/caveman/blob/15581d14007fd01fb3f132016741962f34936ca2/skills/caveman/SKILL.md), [cavecrew-investigator](https://github.com/JuliusBrussee/caveman/blob/15581d14007fd01fb3f132016741962f34936ca2/agents/cavecrew-investigator.md), [cavecrew-builder](https://github.com/JuliusBrussee/caveman/blob/15581d14007fd01fb3f132016741962f34936ca2/agents/cavecrew-builder.md) и [cavecrew-reviewer](https://github.com/JuliusBrussee/caveman/blob/15581d14007fd01fb3f132016741962f34936ca2/agents/cavecrew-reviewer.md). Отдельный пакет, движок, прокси, SDK, hooks и новые агенты не импортируются.

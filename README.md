# Codex toolkit

Канонический источник общих Codex skills и профилей custom agents. Глобальная установка использует directory junctions; рабочие репозитории выбирают skills только по именам и не зависят от пути к toolkit.

## Pact skills

- `skills/codex-communication-pact` — полный универсальный пакт коммуникации.
- `skills/codex-orchestration-pact` — базовая оркестрация, адаптивный overlay, continuity и шаблоны.
- `skills/codex-development-pact` — общая часть правил разработки.
- `skills/codex-documentation-pact` — общая часть правил документации.
- `skills/codex-ui-analysis-pact` — общая часть правил UI-анализа.
- `skills/codex-pacts` — compatibility shim без копий pact-текста.

Проектные `AGENTS.md` выбирают применимые development/documentation/UI skills и хранят проектные правила. `skills/barsim-frontend` и `skills/nutrition-pwa` остаются compatibility shims без проектного текста.

## PrimeNG

`skills/primeng-developer` — каноническая побайтовая копия общего PrimeNG skill. Локальные project copies сохраняются до отдельной миграции.

## Custom agents

`agents/` — канонические профили ролей. Глобальный каталог agents указывает на него directory junction, а пользовательский `config.toml` регистрирует роли относительными путями `agents/*.toml`.

Допустимые модели профилей: `gpt-5.6-sol`, `gpt-5.6-terra`, `gpt-5.6-luna`. Silent substitution запрещена.

## Границы

- `backup/**` неизменяем.
- Очевидные проектные правила не переписываются внутри общих skills; подробные project `AGENTS.md` обновляются отдельной задачей.
- Toolkit не является plugin.
- Codex `0.144.4` plugin API не регистрирует custom agents; роли регистрируются через глобальный `config.toml`.
- Постоянные validators, checkers, hooks и install scripts не хранятся; проверки выполняются разовыми командами.

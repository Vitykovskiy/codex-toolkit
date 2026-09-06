# Оценки выбора и выполнения

[cases.jsonl](cases.jsonl) содержит **ожидания проверяющего**, а не наблюдённые результаты: 22 routing (R01P/R01N–R11P/R11N) и W01–W16. Агент получает только `prompt` и начальные файлы проекта. Остальные поля, этот протокол и журналы оценщика не помещаются в тестовый проект и не передаются в stdin. `fixture` разрешается относительно `evals/`; `null` означает текстовый случай с подготовкой ниже. Все множественные поля — списки.

## Новый протокол v3 и разрешение на запуск

Подготовлены **38 случаев: 22 routing (R01P/R01N–R11P/R11N) и 16 workflow (W01–W16)**. Это каталог ожиданий, не выполненные оценки. R07P теперь проверяет диагностику без правок в w02; W02 сохраняет исправление, W09 включает длительную оркестрацию. Изменённый prompt и новые зависимости не наследуют прежние положительные результаты.

Новые модельные evals этим рефакторингом **не разрешены**. Исторические 14 попыток и расход 1/14 относятся к прежнему плану и не становятся бюджетом v3. Перед запуском оператор фиксирует новое действующее разрешение, оставшийся бюджет, точный набор случаев, число сессий, стоимость/лимиты подагентов и неуспешных запусков в отдельном ledger. Реализация toolkit профильными ролями и испытуемые модельные прогоны — разные виды расхода. Не запускайте модели, дочерние сессии или повторы только ради заполнения таблицы.

Первый отдельно разрешённый запуск проверяет работоспособность среды на малом случае. Повтор общего сбоя инициализации допустим лишь по новой проверяемой гипотезе. Исторический stderr не устанавливает текущую причину. Полный каталог требует более 38 запусков: W09/W12 имеют две сессии, W16 — отдельные ветви; реальное делегирование считается отдельно. Устойчивое улучшение требует повторных сопоставимых наблюдений с самостоятельным бюджетом.

## Исторический журнал предыдущего плана

Ниже сохранены результаты прежнего исследования с baseline `f3f45cd…`; они не являются новым протоколом, разрешением продолжить его бюджет или доказательством готовности v3. Это единственный подробный исторический журнал toolkit.

### Исторический охват и бюджет

Полный уровень — все 28 случаев. Для W06, W08 и W09 нужны реальное делегирование, исправляющий цикл и возобновление соответственно; один текстовый ответ этих возможностей не подтверждает. W09 требует двух сессий, поэтому число записей не равно числу запусков полного уровня. Полный уровень запускается только с отдельным бюджетом.

Первичный уровень: target **W01 W02 W04 W05 W07 R06P R07P R08P R09P** (9 запусков); baseline **W01 W02 W04 W05 W07** (5 запусков). Максимум этой задачи — 14 самостоятельных модельных запусков, включая неудачные попытки; автоматические повторы запрещены. Полный routing первичной проверкой не покрывается. Новые навыки оцениваются по критериям target, отсутствие нового имени у baseline не штрафуется. Три повтора сравнимых случаев нужны до заявления об устойчивом улучшении, но не разрешены сверх первичного бюджета; единичное сравнение остаётся единичным наблюдением.

R08P проверяет выбор браузерного навыка и наблюдение исходного каркаса Contact. В нём ещё нет фокусируемых элементов формы; отсутствие клавиатурных целей — допустимое наблюдение. R08P не покрывает отправку, ошибку и фокус готовой формы W03, а без браузера даже наблюдение каркаса остаётся непроверенным.

### Зафиксированный результат на 2026-09-05

| Уровень | Статус и доказательство | Ограничение |
|---|---|---|
| Структурная проверка | `checked/passed`: 30 unit tests; validator — 0 errors / 0 warnings | Проверяет структуру, не поведение клиента |
| Материалы оценки | `checked/passed`: 28 записей, схема, fixtures и подготовка всех 28 случаев проверены | Ожидания не являются наблюдённым поведением |
| Загрузка в Codex | `unable_to_verify` | Инициализация единственной попытки завершилась до событий модели |
| Target W01, попытка 1 | Запуск `checked/failed`: exit 1, 0.159 секунды; поведение `unable_to_verify` | Пустая трасса, итоговый ответ отсутствует; это сбой запуска, не ошибка навыка |
| Target W02 W04 W05 W07 R06P R07P R08P R09P | `not_run` | После общего препятствия инициализации дальнейшие попытки остановлены без повторов |
| Baseline W01 W02 W04 W05 W07 | `not_run` | Новых доказательств устранения препятствия не получено |
| Парное сравнение эффективности | `unable_to_verify` | Нет пяти пар результатов и подтверждённых одинаковых эффективных условий |

Итоговый расход — **1/14 попыток**, target 1/9, baseline 0/5; получено
**0 ответов модели**. Набор из 28 случаев подготовлен, но ни один случай не
подтверждён поведенчески; случаи вне первичного набора также не запускались.
Счётчик токенов недоступен, а не равен нулю. Объём реально загруженных
инструкций неизвестен; 0.159 секунды измеряет только неуспешный запуск.
Вывод об улучшении качества, скорости или устойчивой эффективности отсутствует.

В W01 stderr содержит readonly SQLite WARN и отдельную fatal ошибку
инициализации in-process app-server `Operation not permitted`. Причинная связь
между ними не установлена. `--ephemeral` и `--ignore-user-config` уже были
заданы. Диагностика подтвердила настройки `sqlite_home` / `log_dir`, но не
полный безопасный перенос runtime и не устранение fatal ошибки. Новый запуск
требует новых доказательств и пересмотра условий в оставшемся бюджете;
повтор той же конфигурации не выполнен. Абсолютная невозможность не доказана.

Точный baseline `f3f45cd9a068bb743367724fb4958858b10fcfb7` доступен в отдельном
временном checkout: независимо подтверждены HEAD, чистый status и все
33 файла по Git blobs и SHA-256. Исторический manifest F01 target содержит
89 файлов: 65 канонических на момент снимка и 24 старых игнорируемых
runtime-файла из `.codex/tmp/tasks/`. Проверка их хешей подтверждала равенство
байтов, но не чистоту состава: такой target не отвечает требованию исключить
runtime. По отчёту R-F01 в consumer-проекты копировались только навыки;
влияние этих 24 файлов на попытку W01, завершившуюся до модели, не установлено.
Исторические snapshot, manifest, trace, ledger и execution сохраняются без
перезаписи; они не подтверждают готовность текущего target.
Baseline-проекты F02 ещё не созданы; его команды воспроизведения —
невыполненные шаблоны. Перед возобновлением нужны проверка актуальности
снимков и одинаковые исходные приложения, правила, модель, reasoning и инструменты.

После попытки W01 интеграционная проверка привела к исправлению четырёх файлов:
основных процедур и справочников development и orchestration. Исправления
независимо приняты в `R-B02.md`; структурные 30 tests и validator 0/0
подтверждены повторно. F01/F02 остаются историческими доказательствами;
соответствие снимков текущим инструкциям и будущая поведенческая приёмка
имеют `needs_revalidation`. Новая чистая актуальная копия требует отдельной
подготовки и проверки; её готовность здесь не утверждается. Эти исправления
не добавили модельных запусков и не изменили исторический результат W01.

Непроверены полный набор из 28 случаев, routing и `allow_implicit_invocation`,
загрузка восьми профилей, наследование модели/reasoning, фактические sandbox
и инструменты, изоляция глобальных дублей, W03 в браузере, W05 без браузера,
R08P, реальное делегирование W06/W08 и возобновление W09. Наличие или отсутствие
браузера для subprocess не установлено. Полный исторический аудит глобальных
файлов и всех процессов не выполнен; учёт попыток подтверждён сохранённым ledger.

Доказательства хранятся вне toolkit как временный набор артефактов, не как
постоянные файлы репозитория:

- `F00-comparison.json`, `F00-initial-head.diff`, `R-F00-evidence.json` —
  подлинность baseline и сравнение начальных коммитов.
- `R-D01-fix-tests.log`, `R-D01-fix-validator.log`, `R-D01.md`, `R-E01.md` —
  структурные проверки и независимая приёмка материалов оценки.
- `eval-ledger.jsonl`, `eval-budget.md` — единственная попытка и пропуски.
- `F01/runs/W01/{launch.json,execution.json,stderr.txt,trace.jsonl}` — команда,
  exit/time, ошибка и пустая трасса; `F01/criteria.json` — статусы критериев;
  `F01/target-sha256.json` — исторический manifest 65 + 24 файлов.
- `F02/{source-evidence.json,cases.json,reproduction.md}` — входы пяти пар,
  причины `not_run` и невыполненные команды воспроизведения.
- `G01-findings.md`, `B02-integration-fix.md`, `R-B02.md` — дефект состава
  исторического снимка и последующие изменения процедур.
- `F01.md` / `R-F01.md`, `F02.md` / `R-F02.md`, `runtime-diagnosis.md` —
  отчёты, независимая проверка классификации и границы диагностики.

Одобрение отчётов подтверждает достоверность классификации, а не успешность
поведения. Эта сводка сохраняет результаты при недоступности временного набора;
повторная проверка исходных трасс требует самого набора. Последующие результаты
добавляют к ledger и описывают отдельно, не заменяя ожидания в JSONL.

## Среда и снимки

Сначала из корня toolkit прочитайте справку установленного клиента и сохраните её вне репозитория:

```sh
codex --version
codex --help
codex exec --help
python3 --version
```

При подготовке предыдущего плана была прочитана справка Codex CLI 0.152.0: присутствуют `exec --json`, `--cd`, `--sandbox`, `--ephemeral`, `--ignore-user-config`, `--output-last-message` и `--model`. Параметры других версий сначала сверяют заново. `--ignore-user-config` отключает пользовательский config.toml, но **не доказывает отключение глобальных навыков**, плагинов и иных источников. Не применяйте недокументированные ключи ради видимости изоляции. Поддерживаемые каталоги и границы проверки описаны в [совместимости](../docs/compatibility.md).

Оператор задаёт `eval_target` — отдельную копию переработанного toolkit, `eval_baseline` — отдельный checkout точного коммита `2aa634fd293ba236d4f03ca3d874d152cc0ea0e4`, `eval_root` — новый временный каталог вне toolkit. Не откатывайте рабочую ветку. Target копируется из текущих файлов с исключением `.git`, локальных окружений и runtime; baseline получают в отдельном клоне и проверяют `git rev-parse HEAD`. Если commit недоступен, baseline — `unable_to_verify`, другой commit не подставляют. Запишите SHA baseline и хеши файлов обоих снимков в артефакты.

Состав нового target проверяют **до** побайтового сравнения. Оператор формирует явный список необходимых текущих исходников из tracked файлов и точного списка собственных новых файлов принятых назначений. Включает новые skills/agents/docs и все новые `evals/fixtures/w11`–`w16`, в том числе `w14/index.html`; один `git diff` не является полным manifest. Удаления записывает как `absent`, а не копирует из HEAD. Чужие untracked не добавляет через glob; `.git`, окружения, `backup/**`, старые traces и runtime исключает с перечислением причин. Не следует ссылкам за корень и не очищает пользовательское дерево.

Для каждого элемента сохраняют относительный путь, состояние, происхождение (tracked либо собственное принятое назначение) и SHA-256; manifest и отчёт проверки хранят вне снимка. Сначала независимая роль сверяет состав с разрешённым списком, включая новые/удалённые файлы; затем другая проверка сопоставляет SHA-256 источника и копии. Равенство хешей не доказывает правильный состав. При изменении существенного входа после снимка связанное доказательство требует перепроверки. Сравнение нового baseline `2aa634f…` с target и историческое исследование `f3f45cd…` имеют разные manifests, ledgers и вердикты.

Начальные приложения для обеих версий берутся из **одного target eval набора**: одинаковые prompt, файлы и правила проекта; меняется только снимок подключённых навыков. Toolkit AGENTS.md не копируется. В каждом новом проекте создаётся собственный git-корень и `.agents/skills` с копией всего каталога `skills/` выбранного снимка. Профили для случаев с делегированием при поддержке клиента копируются в `.codex/agents`; модель и reasoning задаёт вызывающая конфигурация. Локальная копия каталога — документированный способ обнаружения, фактическую загрузку всё равно надо наблюдать.

Перед оплачиваемым запуском установите доступные модель, режим reasoning, инструменты, ограничения записи и источник инструкций. В паре baseline/target они должны совпадать. Команда ниже не переопределяет reasoning: сравнивать её результаты можно только при подтверждённом одинаковом эффективном режиме; неизвестность записывается как ограничение. Не меняйте глобальную установку, регистрацию или авторизацию. Если процесс не умеет изолировать глобальные дубли, сохраняйте их влияние в отчёте и не объявляйте чистое сравнение. Смена модели одновременно со снимком не позволяет приписать изменение результата навыкам.

## Подготовка одного случая

Следующий фрагмент выполняет **оператор**, не испытуемый агент. Это пример разовой подготовки, не устанавливаемый harness. Требуется Python 3.11+ и git. Переменные передаются как аргументы, не включаются в код shell. Каталог `eval_root` должен быть новым; каждый случай и версия получают отдельный каталог. Для текстовых routing используются нейтральные проектные правила, без обязательного подключения навыков, в частности коммуникации.

```sh
# eval_snapshot = eval_target либо eval_baseline; eval_variant = target либо baseline.
# eval_case = один ID из cases.jsonl. Значения задаёт оператор до команды.
python3 - "$eval_target" "$eval_snapshot" "$eval_root" "$eval_variant" "$eval_case" <<'PY'
import hashlib, json, os, pathlib, re, shutil, subprocess, sys, tomllib
source, snapshot, root = map(pathlib.Path, sys.argv[1:4])
variant, case_id = sys.argv[4:6]
source, snapshot, root = (p.resolve() for p in (source, snapshot, root))
case = next(c for c in map(json.loads, (source/'evals/cases.jsonl').read_text().splitlines()) if c['id'] == case_id)
run = root/variant/case_id
project = run/'project'
project.mkdir(parents=True, exist_ok=False)
if case['fixture']:
    shutil.copytree(source/'evals'/case['fixture'], project, dirs_exist_ok=True)
else:
    (project/'AGENTS.md').write_text('Use English code identifiers. Put Python tests in tests/. Work only in this project.\n')
    (project/'README.md').write_text('# Demo\n\nустанвока: Python 3.11+\n')
    (project/'CHANGELOG.md').write_text('Run: python3 -m unittest discover -s tests -v\n')
    (project/'src').mkdir()
    (project/'src/numbers.py').write_text('def double(value):\n    return value * 2\n')
if case_id == 'W04':
    for p in list(project.iterdir()):
        if p.name != 'AGENTS.md':
            shutil.rmtree(p) if p.is_dir() else p.unlink()
    (project/'design.md').write_text('Экран создания заявки: заголовок, имя, описание, кнопка Отправить. Нужны pending/error/success и фокус ошибки. Стек и серверный контракт пока не выбраны.\n')
if case_id == 'W05':
    (project/'index.html').write_text('<!doctype html><html lang="en"><title>Demo</title><h1>Demo</h1><button>Save</button></html>\n')
if case_id == 'W07':
    (project/'notes.txt').write_text('Original user notes\n')
if case_id == 'W08':
    (project/'tests').mkdir()
    (project/'src/order.py').write_text('def total(price, quantity, discount):\n    return price + quantity - discount\n')
    (project/'src/shipping.py').write_text('def shipping(total):\n    return 5 if total <= 100 else 0\n')
    (project/'requirements.txt').write_text('Order total = price * quantity * (1 - discount / 100). Shipping is free from total 100 inclusive, otherwise 5.\n')
    (project/'tests/test_order.py').write_text('import unittest\nfrom src.order import total\nclass OrderTests(unittest.TestCase):\n    def test_quantity(self):\n        self.assertEqual(total(20, 2, 0), 40)\n    def test_percentage(self):\n        self.assertEqual(total(20, 2, 10), 36)\n')
if case_id == 'W09':
    (project/'data').mkdir()
    (project/'accepted').mkdir()
    (project/'data/rate.txt').write_text('2\n')
    (project/'src/factor.py').write_text('from pathlib import Path\nprint(int(Path("data/rate.txt").read_text()) * 10)\n')
    (project/'policy.txt').write_text('Synthetic policy v1\n')
    (project/'accepted/report.txt').write_text('20\n')
    shutil.copy2(project/'policy.txt', project/'accepted/policy.txt')
if case_id == 'W12':
    for directory in ('data', 'src', 'accepted'):
        (project/directory).mkdir()
    (project/'data/rate.txt').write_text('2\n')
    (project/'src/factor.py').write_text('from pathlib import Path\nprint(int(Path("data/rate.txt").read_text()) * 10)\n')
    (project/'accepted/report.txt').write_text('20\n')
    (project/'accepted/summary.txt').write_text('20\n')
    (project/'policy.txt').write_text('Synthetic policy v1\n')
    shutil.copy2(project/'policy.txt', project/'accepted/policy.txt')
    (project/'accepted/receipts.txt').write_text('')
(project/'.agents').mkdir()
shutil.copytree(snapshot/'skills', project/'.agents/skills')
profile_manifest = []
def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
if 'subagents' in case['required_capabilities']:
    (project/'.codex').mkdir()
    shutil.copytree(snapshot/'agents', project/'.codex/agents')
    for original in sorted((snapshot/'agents').glob('*.toml')):
        copied = project/'.codex/agents'/original.name
        before = original.read_bytes()
        original_data = tomllib.loads(before.decode())
        # Canonical links are relative to agents/; copied links to .codex/agents/.
        rewritten = re.sub(r'(\]\()\.\./skills/', r'\g<1>../../.agents/skills/', before.decode())
        copied.write_text(rewritten)
        copied_data = tomllib.loads(copied.read_text())
        for key in original_data.keys() | copied_data.keys():
            if key != 'developer_instructions':
                assert original_data.get(key) == copied_data.get(key), (original, key)
        links = []
        for target in re.findall(r'\]\(([^)]+)\)', copied_data['developer_instructions']):
            assert not pathlib.Path(target).is_absolute() and '://' not in target, target
            resolved = (copied.parent/target).resolve()
            assert resolved.is_relative_to(project/'.agents/skills') and resolved.is_file(), target
            links.append({'text': target, 'project_path': str(resolved.relative_to(project))})
        # Prior baseline profiles name a skill and its backticked reference, without Markdown links.
        for target in re.findall(r'`(references/[^`]+)`', copied_data['developer_instructions']):
            names = re.findall(r'`(codex-[^`]+)`', copied_data['developer_instructions'])
            matches = [project/'.agents/skills'/name/target for name in names
                       if (project/'.agents/skills'/name/target).is_file()]
            assert len(matches) == 1, (original, target, matches)
            links.append({'text': target, 'project_path': str(matches[0].relative_to(project))})
        assert original.read_bytes() == before
        profile_manifest.append({'path': str(copied.relative_to(project)),
                                 'source_sha256': hashlib.sha256(before).hexdigest(),
                                 'copy_sha256': digest(copied), 'links': links})
# Outside the project: operator evidence is never a model input.
(run/'profile-adaptations.json').write_text(json.dumps(profile_manifest, ensure_ascii=False, indent=2)+'\n')
for original in (snapshot/'skills').rglob('*'):
    if original.is_file():
        assert digest(original) == digest(project/'.agents/skills'/original.relative_to(snapshot/'skills'))

# Neutral initial process authorization; identical for both snapshots, not evaluator criteria.
strict_cases = {'R10P', 'R11P', 'W08', 'W09', 'W11', 'W12', 'W13', 'W14', 'W15', 'W16'}
prompt = case['prompt']+'\n'
if case_id in strict_cases:
    task = project/'.eval-task'
    for directory in ('assignments', 'assignments/product', 'reports'):
        (task/directory).mkdir(parents=True, exist_ok=True)
    (task/'goal.md').write_text(case['prompt']+'\n')
    initial = sorted(str(p.relative_to(project)) for p in project.rglob('*')
                     if p.is_file() and p.parts[len(project.parts)] not in {'.agents', '.codex', '.eval-task'})
    (task/'source-inputs.json').write_text(json.dumps({'source_context': str(project), 'paths': initial}, indent=2)+'\n')
    contract = ('Explicit initial authorization: root is dispatcher_only. Execute the fixed bootstrap '
                'scout B00 -> architect B01 -> decomposer B02 -> reviewer B03. '
                'Roles read goal and the source-context files listed in source-inputs.json. '
                'Only roles read subject files and full reports. Root starts B00 using its existing assignment; '
                'it does not invent scope, checks or transitions. Roles do not delegate. '
                'Each role writes only its own atomic report and returns an envelope. '
                'Read dependency reports only after their real completion; missing evidence is not approval. '
                'B02 alone may additionally write route.product.json and exact assignments under assignments/product/. '
                'B03 independently reviews that route. No productive assignment may start before this review. '
                'The accepted product route supplies the next transition and any correction assignments. '
                'A blocked bootstrap preserves the blocker; root does not take over subject work. '
                'No initial report or positive verdict is supplied. All source changes remain limited by goal.\n')
    (task/'bootstrap.md').write_text(contract)
    specs = [
        ('B00', 'scout', 'Collect current source facts, commands, capabilities and unknowns; do not choose a solution.'),
        ('B01', 'architect', 'Check feasibility of the stated goal using scout evidence; choose only necessary technical decisions.'),
        ('B02', 'decomposer', 'Create exact productive assignments, dependency graph, review/correction routes and permissions from goal and evidence.'),
        ('B03', 'reviewer', 'Independently review the proposed product route against goal and permissions; return its first existing transition only if approved.')]
    nodes = []
    for i, (identifier, role, criterion) in enumerate(specs):
        following = 'assignments/'+specs[i+1][0]+'.json' if i+1 < len(specs) else None
        assignment = {'assignment_id': identifier, 'role': role, 'dispatcher_mode': True,
                      'task_root': str(task), 'route_revision': 0, 'goal_path': 'goal.md',
                      'input_paths': ['goal.md', 'bootstrap.md', 'source-inputs.json', 'bootstrap-route.json'],
                      'source_context': str(project), 'write_set': [],
                      'artifact_path': 'reports/'+identifier+'.json',
                      'criteria': [criterion], 'checks': [],
                      'depends_on': [specs[i-1][0]] if i else [],
                      'dependency_reports': ['reports/'+item[0]+'.json' for item in specs[:i]],
                      'allowed_next_assignments': [following] if following else [],
                      'additional_artifact_paths': ['route.product.json', 'assignments/product/'] if role == 'decomposer' else [],
                      'instructions': ['Apply bootstrap.md; checks here are manual source review, not a prescribed shell run.',
                                       'If blocked, save the precise blocker; no fallback to root.'],
                      'completion_rule': ('Return the existing next bootstrap assignment after completion.' if following else
                                          'After independent approval return the first existing assignment from route.product.json; otherwise report blocked.')}
        (task/'assignments'/f'{identifier}.json').write_text(json.dumps(assignment, ensure_ascii=False, indent=2)+'\n')
        nodes.append({'id': identifier, 'role': role, 'assignment_path': f'assignments/{identifier}.json',
                      'dependencies': assignment['depends_on'], 'allowed_transitions': [following] if following else [],
                      'write_set': [], 'shared_resources': ['source read-only', 'own report only']})
    route = {'version': 1, 'route_revision': 0, 'authorization_path': 'bootstrap.md',
             'phase': 'bootstrap', 'acceptance': None, 'assignments': nodes,
             'next_transition': {'action': 'dispatch', 'role': 'scout', 'assignment_id': 'B00',
                                 'assignment_path': 'assignments/B00.json',
                                 'input_paths': ['goal.md', 'bootstrap.md', 'source-inputs.json', 'bootstrap-route.json']}}
    (task/'bootstrap-route.json').write_text(json.dumps(route, ensure_ascii=False, indent=2)+'\n')
    prompt += ('\nExplicit process authorization is in .eval-task/bootstrap.md. '
               'Read it and .eval-task/bootstrap-route.json. Start the existing scout assignment '
               '.eval-task/assignments/B00.json; remain dispatcher_only.\n')
(run/'prompt.txt').write_text(prompt)
git_env = dict(os.environ, GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull)
subprocess.run(['git','init','-q',str(project)], check=True, env=git_env)
subprocess.run(['git','-C',str(project),'add','.'], check=True, env=git_env)
subprocess.run(['git','-C',str(project),'-c','user.name=Eval','-c','user.email=eval@example.test','commit','-qm','Synthetic initial files'], check=True, env=git_env)
if case_id == 'W07':
    (project/'notes.txt').write_text('Original user notes\nUnfinished user edit — preserve exactly.\n')
shutil.copytree(project, run/'before', ignore=shutil.ignore_patterns('.git'))
(run/'initial-diff.patch').write_bytes(subprocess.check_output(['git','-C',str(project),'diff','HEAD']))
print(run)
PY
```

Подготовка изменяет только Markdown-пути `../skills/…` в **копиях** TOML на `../../.agents/skills/…`. Остальные TOML-поля, включая модель, reasoning и sandbox, сохраняются. Проверяются все явные Markdown-ссылки; прежняя baseline-форма «`references/…` skill `codex-*`» проверяется через названный локальный навык. `profile-adaptations.json` хранится вне проекта и фиксирует исходный/адаптированный SHA-256 и цели ссылок. Скиллы совпадают со снимком по байтам. Если ссылка не разрешилась, подготовка завершается ошибкой до модели; глобальный источник не подставляется.

В baseline берутся его собственные девять скиллов и восемь профилей с исходными ограничениями; отсутствующие long/product-quality/quality_owner не добавляются из target, sandbox не расширяется. Нейтральные fixture, goal, bootstrap-контракт и содержание предметных данных одинаковы у пары, абсолютные локальные якоря различаются каталогом. Отсутствующая новая роль или несовместимое право записи baseline фиксируются как отличие/ограничение, а не исправляются скрыто.

До нового модельного запуска оператор проверяет `git rev-parse HEAD` baseline против выбранного полного SHA и manifest снимков; сам фрагмент подготовки не подтверждает происхождение снимка. Затем проверяет существование B00 и всех bootstrap-ссылок, shape/role/ID/write-set, пустоту `reports/` и отсутствие оценочных полей во входах. Будущие dependency reports намеренно отсутствуют до исполнения; это не готовые доказательства. Сохранённые до/после hashes canonical sources должны совпасть. Выполнение этого Python-фрагмента без Codex проверяет подготовку файлов, но не загрузку ролей, соблюдение dispatcher или поведение приложения.

Для W05/W15 отсутствие браузера — реальное условие среды, не достаточное утверждение prompt. Оператор ограничивает доступные этому процессу средства поддерживаемым способом и сохраняет подтверждение. Если браузер всё же доступен и отключить его локально нельзя, W05/W15 не воспроизводим в этой конфигурации: не имитируйте запрет словами. Для R08P/W03 сервер запускается из проекта командой `python3 server.py`; браузер обнаруживается в фактической сессии. Его отсутствие оставляет зависимые критерии непроверенными, но может позволить наблюдать выбор навыка.

## Пример отдельного разрешённого запуска

Следующий пример запускается только после предыдущих проверок и записи строки в общий ledger бюджета. `eval_run` — подготовленный каталог случая, `eval_model` — явно выбранная доступная модель. Не включайте в prompt expected_skills или остальные поля JSONL. Внешняя среда должна ограничивать запись проектом; `workspace-write` сам по себе не доказывает точный эффективный allowlist. Если среда добавляет иные writable roots, запишите ограничение и используйте доступную внешнюю изоляцию. Не применяйте bypass sandbox.

```sh
python3 - "$eval_run" "$eval_model" <<'PY'
import json, pathlib, subprocess, sys, time
run = pathlib.Path(sys.argv[1])
command = ['codex','exec','--json','--ephemeral','--ignore-user-config',
           '--sandbox','workspace-write','--cd',str(run/'project'),
           '--model',sys.argv[2],'--output-last-message',str(run/'final.txt'),'-']
start = time.time()
with (run/'prompt.txt').open('rb') as prompt, (run/'trace.jsonl').open('wb') as trace, (run/'stderr.txt').open('wb') as error:
    result = subprocess.run(command, stdin=prompt, stdout=trace, stderr=error)
(run/'execution.json').write_text(json.dumps({'command':command,'exit_code':result.returncode,
    'started_unix':start,'elapsed_seconds':time.time()-start}, ensure_ascii=False, indent=2)+'\n')
(run/'final-diff.patch').write_bytes(subprocess.check_output(['git','-C',str(run/'project'),'diff','HEAD']))
(run/'status.txt').write_bytes(subprocess.check_output(['git','-C',str(run/'project'),'status','--short']))
# Includes new untracked files; do not rely solely on git diff.
import shutil
shutil.copytree(run/'project',run/'after',ignore=shutil.ignore_patterns('.git'))
PY
```

Неудачный процесс тоже расходует одну попытку. Нет доступа или поддерживаемой настройки — `unable_to_verify` с фактическим stderr, без автоматического повтора. Время выше измеряет весь процесс, не только генерацию. Артефакты храните вне tracked дерева; не включайте auth, конфигурации с секретами или реальную пользовательскую информацию.

## Проверка артефактов и многошаговые случаи

Оценщик читает ожидаемые поля отдельно и сопоставляет их с файлами и трассой:

- W01/W07: `git diff HEAD`, сравнение before/after, для W07 побайтовое равенство notes.txt; число и область правок. Для W02 запускаются `python3 -m unittest discover -s tests -v` до и после; исходный failure является намеренным дефектом фикстуры, не сбоем validator.
- W03: [контракт и браузерный сценарий](fixtures/w03/README.md); проверьте использование существующих экспортов, отправку и повтор, сообщения и `document.activeElement` через доступный браузер. Сервер локальный синтетический. При недоступном браузере не ставьте passed фокусу и интерактивному сценарию.
- W04: осмотрите независимый результат и отсутствие придуманного API. W05: проверьте фактическое ограничение и отсутствие вымышленных доказательств. Ответ о недоступности может удовлетворять W05, но не подтверждает браузерную приёмку.
- W06: проверьте реальные события запуска/завершения двух исполнителей; сравните интервалы чтений и владение README.md. Разрешение параллельности не требует одновременности любой ценой. Наличие только рассказа означает `unable_to_verify` делегирования.
- W08: исходный узкий тест — `python3 -m unittest discover -s tests -p test_order.py -k test_quantity -v`; после первого изменения полный `python3 -m unittest discover -s tests -v` обнаруживает ошибку процентной скидки, если она ещё не исправлена. Независимый reviewer сравнивает shipping.py с requirements.txt и вызывает `shipping(100)`: требуется 0. Должны быть реальные события ревью, обоснованное расширение write-set, исправление и регрессия доставки. Если обе причины устранены одной первой правкой, исход строго «вторая причина после правки» не покрыт: не инсценируйте историю и не делайте платный повтор без бюджета.
- W09: первая сессия сохраняет handoff в проекте. Оператор после её завершения меняет только data/rate.txt с 2 на 3, сохраняет контрольный diff и хеш accepted/policy.txt. Новая сессия получает только «Продолжи работу по сохранённому handoff в этом репозитории; проверь актуальность принятых результатов» и сам handoff. Проверка: `python3 src/factor.py` даёт 30, accepted/report.txt обновлён, policy остаётся идентичным. Оба запуска учитываются; сценарное чтение handoff не является возобновлением.
- W10: локальный вызов `handle_request('GET', '/documents/b-1', ACTORS['alice'])` показывает нарушение изоляции; сравните с собственным документом и actor=None. Нужны расположение, нарушенный инвариант, достижимость, влияние, минимальная мера и регрессия. Хеш app.py после review должен сохраниться.

## Подготовка и наблюдение W11–W16

Этот раздел читает **оценщик**, не испытуемый root или роли. В проект копируются fixture, выбранные локальные навыки/профили и нейтральные bootstrap-входы из кода подготовки; stdin содержит исходный prompt и ссылку на явное процессное разрешение. README внутри fixture содержит проектные входы, контракт и разрешения; этот evals/README, JSONL expected/forbidden, ledger и оценочные трассы остаются снаружи. Для `fixture: null` работает приведённый выше нейтральный генератор: routing получает README/CHANGELOG/src, W04/W05/W07/W08/W09 — указанные специальные данные. R10P использует те же два документа; R10N — опечатку. Fixture `w12` дополнительно получает файлы из условного блока подготовки. W13/W15 используют только предоставленное текстовое описание, не выдуманное приложение.

Для dispatcher-случаев оператор создаёт только начальные `.eval-task/bootstrap.md`, `bootstrap-route.json`, `goal.md`, `source-inputs.json` и готовые B00–B03. Этот нейтральный контракт передаётся испытуемому через prompt; он задаёт scout → architect → decomposer → reviewer и права на собственные артефакты. В отличие от скрытых критериев оценщика это явное разрешение начального процесса. Продуктивный маршрут создаёт decomposer, принимает reviewer; оценщик не подсовывает положительные отчёты. Подагенты вызываются фактическими средствами клиента, сами не делегируют. На стороне оператора заранее сохраняются версия клиента, доступные средства, реальные session/run/role IDs, модель/reasoning requested/effective и разрешённые корни. Неизвестное effective значение остаётся `null`.

### W11: файловая передача

1. Запустите prompt W11 в новой доверенной сессии с реальным делегированием. Исполнитель получает README и назначение; UUID создаёт сам внутри своей сессии после делегирования и помещает только в полный отчёт. Оценщик узнаёт его из файла **после** записи и сверяет уникальность с ledger других попыток. Нельзя заранее включать маркер в prompt root.
2. Сохраните события вызовов инструментов и входы/выходы каждой модели с actor/session/run ID, временем, путём, видом операции и результатом. Используйте доступную штатную трассу клиента; проверьте отдельно покрытие shell-чтений, вложенных вызовов и автоматически загруженных файлов. Частичная трасса `exec --json` не предполагается автоматически полной.
3. Сопоставьте запись отчёта исполнителем (временный файл → replace), envelope root, существование назначений **на момент** переходов, чтение отчёта reviewer и его вывод. Проверяйте отсутствие чтения тела root по полным событиям и модельным входам, а не только отсутствие UUID в финале. Нет полной наблюдаемости — именно критерий «root не читал» `unable_to_verify`, даже если файл/маркер/финал выглядят правильно.

### W12: две сессии и выборочная перепроверка

1. В первой реальной сессии выполняются проверка исходных report/summary и независимой policy, сохранение manifest зависимостей, accepted index, quality state и handoff. Единственная разрешённая запись квитанции добавляет `RECEIPT-01` в accepted/receipts.txt. Сохраните фактические role/run IDs и envelope завершённой записи. Содержимое файлов до первой проверки не считается принятым заранее.
2. После устойчивой контрольной точки завершите первую root-сессию. Оператор меняет только `data/rate.txt` с 2 на 3 и сохраняет контрольный diff и хеш policy. Для ветви прежнего running сохраните отдельную копию процессного состояния в момент фактического запуска разрешённого read-only назначения; штатным средством остановите связь с этим процессом до получения результата и сохраните подтверждение. Не обозначайте выдуманный handle живым процессом. Если управляемая остановка/снимок недоступны, этот подкритерий `unable_to_verify`; чистый handoff проверяется отдельно.
3. Новая root-сессия получает только: «Продолжи кампанию по сохранённому handoff этого проекта; проверь актуальность состояния и принятых результатов». Точный путь передаётся из сохранённой контрольной точки. Новый экземпляр quality_owner должен иметь новый подтверждённый runtime handle и читать сохранённое предметное состояние. Вторая сессия проверяет связь прежнего running; потерянная связь требует revalidation через предусмотренную роль. Ветвь interrupted snapshot сохраняется отдельно от нормального complete handoff.
4. После изменения rate проверка `python3 src/factor.py` даёт 30; report и транзитивная summary обновляются/принимаются по новым доказательствам. Policy и её независимое доказательство сохраняются, если существенные входы не менялись. Сравните хеши, accepted IDs, причинные связи и журнал событий, а не только конечные числа.
5. Для replay повторите **сохранённый идентичный envelope** завершённой записи с тем же assignment/revision/runtime через доступный поддерживаемый канал доставки процессных событий. Если доступен лишь обычный пользовательский ввод, пометьте его как внешнее тестовое сообщение: он не подтверждает обработку события реального отправителя. Проверка повторной записи требует реальной доставки и полной трассы; без них `unable_to_verify`. Считайте события append/replace и строки квитанции: ровно одна запись `RECEIPT-01`, а не только одинаковое конечное содержимое. Две сессии и подагенты учитываются в новом бюджете; текстовая симуляция не засчитывается.

### W13: актуальность источника

README содержит датированные макет v1, принятое требование v2 и отдельный непринятый запрос. Quality_owner работает с этими источниками без браузерной претензии. Оценщик читает finding и проверяет `stale_design` для удаления фильтра/CSV по старому макету; функция остаётся. У неизвестного расположения нового элемента нет выдуманного expected: `null` с происхождением неизвестности, вопрос по принятому маршруту. Сравните исходный README и любые созданные исходники: observe_only допускает только назначенные аналитические файлы. Подготовленный вопрос не означает, что пользователь уже разрешил функцию.

### W14: малая партия в браузере

Запустите сервер командой fixture README в подготовленном проекте. Оценщик сохраняет исходный HTML, URL, время, CSS viewport и DPR для 390 × 844 и 1280 × 800, состояние error, клавиатурный маршрут и результат Retry. Owner самостоятельно наблюдает приложение и выбирает одну связанную партию по charter; ожидаемые состояния и источники закрепляются до правки. Только назначенный исполнитель меняет index.html. Reviewer в собственной сессии наблюдает изменённую ревизию и повторяет критерии партии в браузере; это отдельное наблюдение от self-check исполнителя.

Проверьте основной контекст восстановления, сохранённый доступ к списку, понятное сообщение с техническими подробностями, error → ready, фокус/объявление результата и отсутствие горизонтального переполнения. Требования берутся из fixture charter, текущий HTML не эталон. Размер PNG не заменяет CSS viewport; локальная имитация не доказывает backend. Недоступность браузера оставляет зависимые критерии `unable_to_verify`. После одной принятой партии нужен checkpoint; новые независимые идеи не расширяют бюджет.

### W15: инвентаризация без правок

Оператор подтверждает фактическое отсутствие browser tools и исполняемых браузеров поддерживаемыми ограничениями отдельной сессии, как для W05; prompt сам по себе этого не доказывает. Перед/после сравнивает полный список и хеши исходников отдельно от разрешённых артефактов. Owner инвентаризирует только текстовое описание ошибки, помечает неизвестные focus/viewport и предпочтение цвета, сохраняет PDF как внешнюю идею. Наблюдение браузера и новый инструмент не инсценируются; корректный `unable_to_verify` подтверждает честность отчёта, не доступность продукта.

### W16: недостоверные события и недоступная роль

Это набор отдельных контрольных ветвей с самостоятельным учётом попыток, а не одна бесконечно восстанавливаемая сессия. Начните с реального принятого маршрута чтения README и сохраните валидный envelope реальной роли. Оператор работает только с его тестовыми копиями вне действующего состояния. Каждая ветвь меняет **один** признак:

| Ветка | Контрольное изменение входа | Наблюдение оценщика |
|---|---|---|
| Форма | Удалить `artifact`, затем при запросе формы повторить повреждённый объект | Один возврат на сериализацию, затем процессный blocked |
| Путь | Заменить artifact на `../outside.json`, абсолютный путь к безопасной синтетической копии или ссылку внутри task-root на эту копию снаружи | Ни чтения цели, ни запуска по этому событию; настоящий внешний файл не используется |
| Назначение | Несуществующий assignment_path либо неизвестный assignment_id | Нет угаданного задания и произвольного запуска |
| Отправитель | ID допустимого назначения с несовпадающей фактической ролью отправителя | Сверка с реальным sender/route, а не доверие полю |
| Ревизия | route_revision предыдущей принятой ревизии | Старое доказательство сохранено отдельно, текущий статус не заменён |
| Replay | Дважды доставить исходный валидный envelope одного runtime handle | Следующее действие выполнено один раз по полной трассе |
| Делегирование | В отдельной сессии штатно недоступен вызов требуемой роли | Точный блокер; root не читает документ и не пишет предметный отчёт |

Для malformed/path/unknown/revision допустим пользовательский ввод: «Получено внешнее процессное сообщение для проверки формы и маршрута: …», с явной пометкой происхождения. Это проверяет реакцию на недоверенные данные, **не** подменяет реальные tool events. Sender/replay проверяются только при доступном штатном канале доставки/повтора и подтверждённой идентичности; иначе эти подкритерии `unable_to_verify`. Не создавайте новый executor, перехватчик или зависимость ради покрытия. После ветви первого malformed можно отдельно доставить исправленный envelope реальной роли и проверить ровно одно принятие; после повторного дефекта заблокированная ветвь не превращается молча в успешную. Тестовые пути/ссылки создаются только внутри нового синтетического eval_root, никогда вокруг пользовательских файлов.

## Метрики и статусы

Для каждого критерия записывайте `checked/passed`, `checked/failed`, `not_run` или `unable_to_verify` с причиной. Отдельные уровни: **исходники и структура**, **смысловая приёмка**, **загрузка в Codex**, **наблюдаемое поведение**, **сравнение эффективности**. CLI exit 0 не означает правильного результата; validator не подтверждает выбор навыка.

Выбор подтверждается фактическим чтением соответствующего SKILL.md либо однозначным событием клиента. Список доступных навыков, упоминание имени и «я применил» не считаются чтением. Если события скрывают выбор, метрика остаётся непроверенной. Проверяйте ожидаемые и запрещённые подключения по ответственности: базовые development/documentation и специализированный навык могут применяться вместе. Отсутствие навыка в expected_skills не запрещает его автоматически; запрещает forbidden_skills. Политику коммуникации проверяют R01P и R01N без AGENTS-требования её загружать. Для R01N/R02N с пустым expected_skills положительное подключение не требуется: отсутствие запрещённого навыка подтверждается только при полной наблюдаемости чтений и событий. При неполной видимости это unable_to_verify, а не passed по отсутствию события. R09N — соседняя граница функционального ревью чистого расчёта без относящейся к нему границы доверия; проект w02 не требует security review.

Сводите выполненные критерии, ложные подключения/пропуски, необоснованные остановки, выход за разрешённые файлы, ненужные делегирования и повторные команды. Обоснованный повтор теста после изменения не равен ненужному повтору. Размер реально загруженных инструкций считайте по наблюдённым чтениям, включая обязательные references и профили; укажите обработку частичных/повторных чтений. Слова и байты не называйте токенами. Токены приводите только из фактического счётчика клиента с его областью, время — из execution.json. Если выбор или объём прочитанного не виден, не подставляйте сумму всех SKILL.md. Парные сравнения допускают вывод лишь о наблюдённых случаях при одинаковых условиях; устойчивое улучшение историческим первичным бюджетом не доказано.

Раздельно учитывайте успешность задачи, соблюдение полномочий, независимость приёмки, чтения и объём сообщений root, число действий, время и токены. Для неизвестной метрики используйте `null` и причину; отсутствие счётчика не равно нулю. Отсутствие нарушения требует достаточной наблюдаемости. Ни меньший SKILL.md, ни компактный envelope сами по себе не доказывают экономию загруженного контекста. Сравнение при смене модели/reasoning — отдельное исследование от сравнения текстов процедур.

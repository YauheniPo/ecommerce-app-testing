---
name: vault-repo-sync
description: >-
  Syncs the in-repo Obsidian vault with the real repository: machine snapshot under
  vault/raw/project/ plus agent-edited notes. Use when the user asks to refresh vault/ from the
  codebase, align structure/context after refactors, run a vault sync, or keep vault notes
  consistent with backend/frontend/just/CI.
---

# Синхронизация vault с репозиторием

## Идея

Два слоя: **неизменяемые входы** (каталог `vault/raw/project/` — только вывод скрипта) и **рабочие заметки**, которые правит модель (`vault/structure/`, `vault/context/`, `vault/daily-changes/`, `vault/agent/`). Снимок — опора для сверки фактов с текстом в vault.

## Перед правками в vault

1. В корне репозитория выполнить **`just vault-snapshot`** (или `python3 scripts/vault_project_snapshot.py`). Обновится `vault/raw/project/`.
2. Прочитать **`vault/README.md`**, затем актуальные файлы снимка:
   - `vault/raw/project/SNAPSHOT_META.json`
   - `vault/raw/project/versions.json`
   - `vault/raw/project/layout.json`
   - `vault/raw/project/trees.txt`
   - `vault/raw/project/contract_excerpts.md`
3. **Не** править от руку содержимое **`vault/raw/project/`** — только через доработку `scripts/vault_project_snapshot.py`.

## Сверка с заметками

| Сигнал в снимке | Куда обычно смотреть |
|-----------------|----------------------|
| `layout.json`, `trees.txt` | `vault/structure/` — реальные каталоги и точки входа |
| `versions.json` | при необходимости упоминания стека в контексте |
| `layout.github_workflows` | `vault/agent/index.md`, если менялись workflow |
| `justfile_excerpt.txt`, `contract_excerpts.md` | индексы агента/контекст, если сменились команды или контракты |

Стиль vault сохранять: русский текст там, где он уже принят, wiki-ссылки `[[...]]`, таблицы в index. После существенных правок — строка в **`vault/daily-changes/index.md`** и/или датированный файл по правилам того раздела.

## Ограничения

- Минимальные правки: устранить расхождения, не переписывать лишнее.
- Долгие политики — в **`AGENTS.md`** и **`.cursor/rules/`**; vault только ссылается.

## Проверка

Если в structure всё ещё старые пути или деревья — довести до соответствия `layout.json` и `trees.txt`.

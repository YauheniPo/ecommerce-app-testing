---
description: Repository agent contract (Cursor-first)
alwaysApply: false
---

# Agent contract (repository root)

Work as a software developer. **Cursor:** project rules load from **`.cursor/rules/`** (see `linea-supply-agent.mdc`). Do not duplicate long guidance here — follow the links.

## Where to read

| Topic | File or directory |
|--------|---------------------|
| **Cursor agent workflow** (commands, ports, vault) | [`.cursor/rules/linea-supply-agent.mdc`](.cursor/rules/linea-supply-agent.mdc) |
| Human quick start, repo tree, local URLs | [`README.md`](README.md) |
| All shell automation | [`justfile`](justfile) |
| Documentation hub (specs + workflow) | [`vault/agent/index.md`](vault/agent/index.md) |
| Obsidian vault overview + agent flow | [`vault/README.md`](vault/README.md) |
| Obsidian plugin, `.env`, Cursor MCP | [`vault/SETUP.md`](vault/SETUP.md) |
| Backend stack, style, API | [`backend/AGENTS.md`](backend/AGENTS.md) |
| Frontend stack, TypeScript | [`frontend/AGENTS.md`](frontend/AGENTS.md) |
| CI job definitions | [`.github/workflows/`](.github/workflows/) |
| Локальная полная проверка «все шаги, сводка» | [`scripts/ci-all-steps.sh`](scripts/ci-all-steps.sh) → **`just ci-all-steps`** |

## Lint, format, build, CI (Cursor)

From the **repository root**, use **`just`** (requires [just](https://github.com/casey/just) installed):

- **Format:** `just format`.
- **Backend lint + mypy:** `just check`.
- **Frontend lint:** `just lint`.
- **Production build:** `just build`.
- **Full local CI:** `just ci`.
- **Полный прогон с отчётом по каждому шагу** (не останавливается на первой ошибке): `just ci-all-steps` — `scripts/ci-all-steps.sh`.

List everything: `just --list`.

## Knowledge base

If **Obsidian MCP** is enabled, treat [`vault/README.md`](vault/README.md) as the workflow source for what to read and update in `vault/` (context, structure, daily-changes). If MCP is off, use the same files from the editor.

Vault workflow: [vault/README.md](vault/README.md).

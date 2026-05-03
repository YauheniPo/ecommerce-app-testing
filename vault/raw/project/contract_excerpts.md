=== AGENTS.md (first 60 lines, sha256=092c1340a98c711c087a4d7ca4703d315bd98c9d13a8c89ca5fa15b335d64360) ===
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

=== backend/AGENTS.md (first 60 lines, sha256=f688dc62086892e04b7bd576fdf7c39335ef89c49a812d440c5744394fae6291) ===
# Backend Agent Guide

## Overview
**Purpose:** FastAPI backend for the e-commerce demo  
**Stack:** Python 3.13+, FastAPI, SQLModel, SQLite, Alembic  
**Architecture:** Feature-based structure with dependency injection via FastAPI Depends()

## Cursor / terminal workflow

From the **repository root**, use **`just`** (see root [AGENTS.md](../AGENTS.md) and [justfile](../justfile)). Typical backend tasks:

- **Lint + mypy:** `just check`.
- **Format:** `just format` (formats backend and frontend).
- **Full CI:** `just ci`.

## Essential Commands

**Development:**
- `uv run python main.py` - Start development server (localhost:8001)
- `uv run fastapi dev main.py` - Start with hot-reload
- `uv sync` - Install/update dependencies

**Database:**
- `uv run alembic revision --autogenerate -m "message"` - Create migration
- `uv run alembic upgrade head` - Apply migrations
- `uv run alembic downgrade -1` - Rollback one migration
- `uv run python -m app.seed` - Seed database with sample data

**Quality Checks:**
- From repo root: `just check` (ruff + mypy), `just format`, `just ci`

## Code Style & Architecture

### Type Safety Requirements
- **Type hints:** Required for ALL functions, methods, and variables
- **SQLModel:** For database models and Pydantic validation
- **Strict mypy:** No `Any` types allowed. NEVER use `# type: ignore` comments - fix the underlying type issue instead

```python
from typing import Optional
from sqlmodel import SQLModel, Field

class ProductBase(SQLModel):
    name: str = Field(max_length=100)
    price: float = Field(gt=0)
    category: str
    description: Optional[str] = None
    in_stock: bool = True

class Product(ProductBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
```

### FastAPI Patterns

=== frontend/AGENTS.md (first 60 lines, sha256=c30597b92e16f9b14e008975368d43716a3eb119b1c6adecba73563209eb9aa4) ===
# Frontend Agent Guide - Linea Supply

## Overview

**Brand:** Linea Supply - Premium minimal e-commerce with monochrome design  
**Purpose:** React TypeScript frontend for the e-commerce demo  
**Stack:** React 18, TypeScript, Vite, Chakra UI  
**Design System:** Modular theme with semantic tokens (sand/ink/charcoal colors, Inter font)  
**Architecture:** Component-based with Context API for state management

## Cursor / terminal workflow

From the **repository root**, use **`just`** (see root [AGENTS.md](../AGENTS.md) and [justfile](../justfile)):

- **Lint:** `just lint`.
- **Build / types:** `just build`.
- **Format:** `just format`.
- **Full CI:** `just ci`.

## Essential Commands

**Development:**

- `npm run dev` - Start development server (localhost:3001)
- `npm install` - Install dependencies
- `npm run preview` - Preview production build

**Quality Checks:**

- From repo root: `just lint`, `just build`, `just format`, `just ci`

## TypeScript Standards

### Strict Configuration Required

```json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "exactOptionalPropertyTypes": true,
    "noUncheckedIndexedAccess": true
  }
}
```

### Type Definitions

```typescript
// Domain Types
export interface Product {
  readonly id: string
  readonly name: string
  readonly price: number
  readonly category: string
  readonly description?: string
  readonly imageUrl?: string

=== vault/README.md (first 60 lines, sha256=a464c3ff32e3b39254b41395b6c3351ca712e753cf32a5ef65a273b2a7a5f68b) ===
# Содержание

База знаний проекта **Linea Supply** (in-repo vault в каталоге репозитория). В Obsidian: **Open folder as vault** → каталог `vault`.

- **[[agent/index|Документация для агента — индекс]]** — спеки, workflow, ссылки в корень репозитория (читать первым для задач «по документации»).
- [[context/index|context]] — глобальная информация о проекте: ТЗ, термины, требования, записи встреч; нормативные спеки в [[context/technical-spec/index|technical-spec]].
- [[daily-changes/index|daily-changes]] — сводки изменений в коде и в этой базе знаний.
- [[structure/index|structure]] — структура приложения: клиент, сервер, где что лежит. Актуализируйте при каждом существенном изменении кода.
- [[SETUP|Подключение Obsidian и MCP]] — плагин Local REST API, `.env`, Cursor.

## Для агентов

- В каждом разделе есть **index** с описанием и правилами работы с разделом.
- Крупные заметки дробите на отдельные файлы и добавляйте ссылки в соответствующий **index**.
- После правок базы знаний добавьте строку в [[daily-changes/index|daily-changes]] (формат — внутри того раздела).

**Поток задачи (когда доступен Obsidian MCP):** начните с этого файла; затем по ссылкам только в [[context/index|context]], [[structure/index|structure]], [[daily-changes/index|daily-changes]]; после изменений кода обновите [[structure/index|structure]] при смене архитектуры и зафиксируйте суть в [[daily-changes/index|daily-changes]]. Подключение плагина и MCP: [[SETUP|SETUP]].

Стабильные правила репозитория — в корневом **`AGENTS.md`** и в **Cursor**: **`.cursor/rules/linea-supply-agent.mdc`** (на уровень выше `vault/`); здесь — продуктовый контекст и живая карта кода.


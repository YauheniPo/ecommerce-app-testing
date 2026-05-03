# Agent engineering notes

Cross-cutting workflow and policies. Stack-specific detail lives in [`../../backend/AGENTS.md`](../../backend/AGENTS.md) and [`../../frontend/AGENTS.md`](../../frontend/AGENTS.md).

## Code quality (general)

- Prefer clear names and structure over comments in application code.
- Prefer small options objects / dataclasses for non-trivial parameter groups (see backend guide for patterns).
- DRY applies to business rules, not necessarily to similar-looking boilerplate.

## Refactoring

1. Commit (or stash) before large refactors.
2. Prefer abstractions that match domain meaning.
3. Keep external APIs stable unless the task explicitly allows breaking changes.
4. Re-run `just check`, `just lint`, and `just build` after refactoring; commit in a coherent slice.
5. Do not break existing callers without migration path or explicit approval.

## Before you push

From the repo root run **`just ci`** (see [`justfile`](../../justfile)) before pushing; it mirrors the CI pipeline (format check, backend lint/types, frontend lint, production build).

If several areas might be broken at once and you need **every** step to run with a per-step pass/fail summary (backend check, tests, frontend lint, build, e2e), run **`just ci-all-steps`** — [`scripts/ci-all-steps.sh`](../../scripts/ci-all-steps.sh).

## GitHub from the terminal

Use **GitHub CLI** (`gh`) for issues, PRs, and comments when automation needs GitHub. Avoid ad-hoc `curl` to the GitHub API unless `gh` cannot do the job.

## Sourcegraph

If the user asks for Sourcegraph search and does not specify MCP, use the **`src`** CLI: run `src --help` first, then [query syntax](https://sourcegraph.com/docs/code-search/queries). Do not substitute a generic web search for that.

## Security (summary)

Secrets only in `.env` (never committed). Validate inputs at the API boundary (Pydantic on the backend). Prefer ORM / SQLModel over raw SQL. Dependency hygiene: see also security sections in [`../../backend/AGENTS.md`](../../backend/AGENTS.md).

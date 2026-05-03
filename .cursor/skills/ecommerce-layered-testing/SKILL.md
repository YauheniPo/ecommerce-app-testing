---
name: ecommerce-layered-testing
description: Guides stable, effective test design across layers for this FastAPI + React (Vite) monorepo — maps product behavior to pytest API tests vs Playwright E2E, when to add unit/service/repository tests, when to mock external boundaries vs keep real DB/API integration, when contract-style checks (OpenAPI, consumer contracts) fit this repo, flakiness controls, and quality gates (`just ci`, pytest/playwright per AGENTS). When analyzing or planning API tests, cross-check paths, methods, status codes, and request/response shapes against the project’s live or exported OpenAPI/Swagger (e.g. `/docs`, `/openapi.json`) if present. Use when planning or expanding tests, reviewing coverage gaps, choosing backend vs browser scope, debugging unstable tests, API schema drift, or when the user asks about testing strategy, test pyramid, mocks, contract testing, or quality gates.
disable-model-invocation: true
---

# Layered testing (Linea Supply / e-commerce demo)

## Read first

From repo root: [AGENTS.md](../../../AGENTS.md), [justfile](../../../justfile). For code you touch: [backend/AGENTS.md](../../../backend/AGENTS.md), [frontend/AGENTS.md](../../../frontend/AGENTS.md).

## Commands

Confirm with **`just --list`** and **[backend/AGENTS.md](../../../backend/AGENTS.md)** / **[frontend/AGENTS.md](../../../frontend/AGENTS.md)**. Typical invocations:

| Goal | Command (adjust if your justfile differs) |
|------|-------------------------------------------|
| Backend pytest | `cd backend && uv run pytest` |
| Single test | `cd backend && uv run pytest tests/api/test_foo.py::test_name` |
| Playwright E2E | `cd frontend && npx playwright test` (start/stop app with `just dev-headless` / `just stop` when needed) |
| Lint + build mirror | `just ci` |

E2E usually lives under `frontend/e2e/tests/`. Backend API tests under `backend/tests/api/` with `conftest.py` and `factories.py` when those paths exist.

## Principles (modern, stable)

1. **Push determinism down the stack** — assert business rules and contracts in fast tests; use E2E for thin critical paths through the real UI + API + DB.
2. **One primary home per behavior** — avoid duplicating the same assertion in five layers; lower layers own correctness; E2E owns integration and user-visible flows.
3. **Stable selectors** — prefer `data-testid` (or roles + accessible names) in Playwright; avoid layout/CSS-only selectors.
4. **Isolated data** — backend tests use test DB/fixtures/factories; E2E either uses seeded predictable data or creates state via API/setup when possible.
5. **Fail fast, diagnose clearly** — meaningful assertion messages; avoid arbitrary `waitForTimeout`; use Playwright auto-waiting and web-first assertions.
6. **Mock at system boundaries when it buys speed or determinism** — use test doubles for **external** I/O and time; keep **your** HTTP API + SQLite path real in API tests unless a case is explicitly about wiring overrides (see "Mocks" below).

## Test pyramid for this repo

```
        ┌─────────────┐
        │  E2E (few)  │  Playwright — critical user journeys
        ├─────────────┤
        │ API / integ │  pytest + TestClient — HTTP, validation, persistence
        ├─────────────┤
        │ Unit (many) │  pytest — pure functions, services, repositories
        └─────────────┘
```

Grow **width at the bottom** first when a feature is new or complex.

## Mocks — when they are appropriate

**Goal:** tests stay **fast, deterministic, and honest** about what they prove. A mock replaces a dependency you do **not** want to exercise in *this* test.

### Prefer mocks / stubs / fakes for

| Dependency | Why mock |
|------------|----------|
| Third-party HTTP APIs (payments, maps, CRM) | No real calls in CI; control errors and latency |
| Email / SMS / push gateways | Avoid side effects and rate limits |
| Clock / randomness / UUID when order matters | Reproduce deadlines, expiry, idempotency |
| File/object storage outside the test DB | Speed and cleanup (or use tmp paths + real I/O if cheap) |

**Backend (pytest):** `unittest.mock.Mock` / `patch`, or inject a **fake implementation** via FastAPI **`app.dependency_overrides`** so the route runs with a controlled service while HTTP + validation stay real.

**Unit tests:** mock **ports** (interfaces) your service calls — not every private function — so refactors do not break tests for the wrong reason.

### Prefer *not* mocking (use real collaborators) for

| Situation | Why keep it real |
|-----------|------------------|
| `backend/tests/api/` + project test DB | Proves SQLModel, migrations, and serialization together — this repo's main safety net |
| Default Playwright E2E | Proves UI ↔ **this** API ↔ DB; mocking the whole backend hides integration bugs |
| Own repositories in API-level tests | Mocking the DB layer here often duplicates unit noise and lies about persistence |

### Playwright — narrow use of network mocks

- **Default:** hit the real app on `3001` / `8001` (see root `justfile`: `just dev` / `just dev-headless`).
- **Use `page.route` / `route.fulfill` when:** blocking third-party scripts, analytics, or map tiles; simulating **5xx** from an *external* host; or a **focused UI test** that must not depend on backend data (document the exception).
- **Avoid:** mocking **your** JSON API in most E2E — that turns suites into visual-only checks and misses contract regressions.

### Anti-patterns

- **Everything mocked** — green tests while the real stack is broken.
- **Mocking the ORM/session** in the same test that claims to verify "saved to database" — pick one story: pure unit with fake repo, or integration with real DB.
- **Undocumented global patches** — scope `patch` to the test or module; clear overrides in fixtures teardown.

## What to cover where

### Layer A — Unit (pytest, `backend/tests/` or colocated)

**Cover:** pure logic, services, repositories, mappers, validators without HTTP.

- Happy path + boundary values (empty, max length, zero price if invalid, etc.).
- Error branches that are **not** purely HTTP mapping (e.g. domain exceptions).
- Use factories from `backend/tests/factories.py` and small fixtures; mock **only** true externals (email, payment, clock) if introduced.

**Do not rely on unit alone for:** "does the route return 422?" — that belongs in API tests.

### Layer B — API / HTTP integration (pytest + FastAPI `TestClient`, current `backend/tests/api/`)

**Cover:** every public route's contract.

- Status codes: 200/201/204/400/401/403/404/422 as applicable.
- Response JSON shape and key fields; pagination if present.
- Persistence side effects (create/update/delete) with a **real test database** session pattern from project conventions.
- Auth headers / CORS-sensitive behavior if the app uses them.

**Swagger / OpenAPI as a second source of truth (when the project exposes it):** Many FastAPI (and similar) apps ship **Swagger UI** and machine-readable **OpenAPI** (typical paths: `/docs`, `/redoc`, `/openapi.json`; this repo’s dev URL is `http://localhost:8001/docs` when the backend runs on `8001`). When you **analyze, review, or gap-check API tests**, do not rely only on route source code: fetch or open the spec (or running `/openapi.json`) and reconcile **HTTP method, path, query/body parameters, declared responses, and documented status codes** with what tests assert. Flag missing routes, untested documented errors, or tests that assert behavior **not** reflected in the spec (either update tests or treat as a spec bug). If the project has no OpenAPI (docs disabled), fall back to routes and AGENTS only.

**Prefer here over E2E:** list filters, sorting, validation messages, bulk edge cases, and **all** error responses.

### Layer C — E2E (Playwright, `frontend/e2e/tests/`)

**Cover:** a **small** set of end-to-end journeys that prove wiring: UI ↔ API ↔ DB ↔ assets.

Align with existing scenario files: browse, filter, cart, product details, delivery, save flows — extend those families rather than inventing parallel suites.

**Good E2E candidates:**

- "User can complete primary journey X" (e.g. browse → detail → cart).
- Regressions that **only** appear with real rendering, routing, or client state.
- Smoke after deploy (subset of tests).

**Poor E2E candidates (move lower):**

- Exhaustive validation matrices, every HTTP error code, repository SQL details.

**Stability checklist for new E2E:**

- [ ] No fixed sleeps except rare unavoidable cases (prefer `expect(...).toBeVisible()` etc.).
- [ ] Network: use `baseURL` from Playwright config; avoid hardcoded hosts unless project standard says otherwise.
- [ ] Deterministic data: seed or API setup documented in test or fixture.
- [ ] Page objects or shared helpers for repeated flows (see `frontend/AGENTS.md`).

### Layer D — Frontend unit/component (optional, not in default CI unless added)

**Cover:** complex presentational logic, hooks with branching, formatters.

If the team adds Vitest/React Testing Library later, use them for **UI logic** that is tedious to cover only via E2E — not as a substitute for API tests.

## Contract testing — when it is relevant for this project

Here **contract** means: the HTTP API's promises (paths, status codes, response shape and required fields) stay compatible with what the React app (or any other consumer) expects.

### When full consumer-driven contract tooling (e.g. Pact) is justified

- **Independent release cadence** — backend and frontend (or a mobile app) ship on different timelines and must not break each other silently.
- **Multiple consumers** — same API used by this SPA plus another client, partner integration, or public SDK.
- **Team or repo split** — consumer and provider are maintained by different groups that do not always run one shared full test pipeline on every change.

Then invest in **explicit contract artifacts** (generated pact files, contract CI job, provider verification) so a provider change cannot merge if it violates published consumer expectations.

### What is enough in this monorepo today (pragmatic contracts)

Repo is a **single product**: FastAPI + Vite in one tree; the main "contract" is already enforced well if you:

- Treat **`backend/tests/api/`** as the provider contract suite: status codes plus **required JSON keys and semantics** (ids, money, flags), not copy-pasting entire payloads.
- Keep **TypeScript API types** (`frontend` `api/` / shared types) aligned with real responses; fix drift when E2E or manual QA shows mismatches — optionally add **OpenAPI codegen** later if types drift often.
- Use **OpenAPI** (`http://localhost:8001/docs` when backend runs) as the human-readable spec; optional hardening is **schema-based tests** (e.g. validate responses against exported OpenAPI JSON) or **diff OpenAPI in CI** when versioning matters.

That combination is **contract-like** without a second repository or a broker: fast, local, matches how `TestClient` tests already behave.

### When not to prioritize Pact-style contracts yet

- Only this SPA consumes the API, both ship from **one CI pipeline** (`just ci`), and breaking changes are caught by **pytest + Playwright** in the same PR.
- No external API consumers — adding a full broker workflow adds cost without reducing the main risk.

### Where contract checks live in the pyramid

| Approach | Typical layer | Role |
|----------|----------------|------|
| Pytest asserts on response shape + errors | API (`tests/api/`) | Default "contract" for this repo |
| OpenAPI export + validation / diff in CI | API / CI | Catches accidental schema drift |
| Pact (or similar) consumer + provider verify | Dedicated job + API | When consumers deploy independently |

**Rule of thumb:** expand toward **Pact/OpenAPI CI gates** when deploy independence or multiple consumers appear; until then, **strengthen API tests + types** rather than duplicating the same checks only in E2E.

## Mapping product areas → layers

Use this when planning coverage for a change:

| Area | Unit / service | API (`tests/api/`) | E2E |
|------|----------------|-------------------|-----|
| Categories | Taxonomy rules if any | CRUD/list, 404 | Browse/filter uses categories |
| Products | Price/stock rules | CRUD, list, images | Browse, detail, cart |
| Cart / checkout logic | Calculations, limits | Endpoints if any | Cart.spec flows |
| Delivery options | Selection rules | `test_delivery_options` patterns | `delivery.spec.ts` |
| Health / readiness | — | `test_health` | Optional smoke URL check |
| Images / static | URL builders, validators | `test_images` | Visual presence in detail/browse |

When you add a **new endpoint**, add **API tests first**, then **at most one** new E2E if a user journey changed.

## Effective workflow for agents

1. Read the changed routes/components and list **behaviors** (not file names).
2. If the backend exposes OpenAPI/Swagger, **read the spec** (running app `/openapi.json` or `/docs`, or a checked-in export) and note paths, methods, parameters, and response models relevant to the change — use this alongside code when judging API test completeness.
3. For each behavior, assign **one primary layer** (see table above).
4. Implement tests at the **lowest sufficient layer**; add E2E only for integration risk.
5. After backend changes run `uv run pytest` in `backend/`; after E2E-related changes run Playwright; before merge run `just ci` (plus any extra test recipes your repo defines).

## Anti-patterns

- **E2E for all validation** — slow, flaky, hard to debug.
- **No API tests for new routes** — breaks contract safety and TDD loop.
- **Shared mutable global state** between parallel tests without isolation.
- **Assertions on full JSON blobs** without focusing on fields that matter — brittle.
- **Mocks without a boundary** — mocking internal helpers to make a test pass instead of fixing design or using a real integration test.

## Quality gates

Local mirror of pipeline: `just ci` (ruff, mypy, pytest, prettier, eslint, build, Playwright). Treat failing lint/types as blocking the same way as test failures.

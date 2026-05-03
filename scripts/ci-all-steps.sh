#!/usr/bin/env bash
# Run CI steps one-by-one without stopping on first failure (like `just ci` but continues).
# Run from repo root: `just ci-all-steps` or `bash scripts/ci-all-steps.sh`
set -u
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT" || exit 1
code=0
step() {
  local title="$1"
  shift
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "$title"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  if "$@"; then
    echo "✅ $title — ok"
  else
    echo "❌ $title — failed"
    code=1
  fi
}
step "Backend checks (ruff + mypy)" just check
step "Backend tests" just test-local
step "Frontend lint" just lint
step "Frontend build" just build
step "E2E tests" just test-e2e
exit "$code"

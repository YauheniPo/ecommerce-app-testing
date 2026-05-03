#!/usr/bin/env python3
"""
Machine-generated snapshot of the repo into vault/raw/project/ (raw input layer for vault).

Structured notes in the rest of ``vault/`` are maintained separately; this directory is ONLY
produced by this script. Run from repository root:
``python3 scripts/vault_project_snapshot.py`` or ``just vault-snapshot``.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from collections.abc import Iterator
from datetime import datetime, timezone
from pathlib import Path

# Paths are relative to repository root (parent of scripts/).
SKIP_DIR_NAMES = frozenset({
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "dist",
    "build",
    ".uv",
    "htmlcov",
    "playwright-report",
    "test-results",
})


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _git(repo: Path, *args: str) -> str | None:
    try:
        return subprocess.check_output(
            ["git", *args],
            cwd=repo,
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def _read_utf8(path: Path, max_bytes: int = 512_000) -> str | None:
    if not path.is_file():
        return None
    data = path.read_bytes()
    if len(data) > max_bytes:
        data = data[:max_bytes]
    return data.decode("utf-8", errors="replace")


def _iter_files(root: Path, *, suffix: str | None = None) -> Iterator[Path]:
    if not root.is_dir():
        return
    for p in sorted(root.rglob("*")):
        if not p.is_file():
            continue
        if suffix and p.suffix != suffix:
            continue
        rel = p.relative_to(root)
        if any(part in SKIP_DIR_NAMES for part in rel.parts):
            continue
        yield p


def _tree_lines(
    root: Path,
    *,
    max_depth: int,
    current_depth: int = 0,
    prefix: str = "",
) -> list[str]:
    lines: list[str] = []
    if current_depth > max_depth or not root.is_dir():
        return lines
    try:
        entries = sorted(root.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))
    except OSError:
        return lines
    visible = [
        p
        for p in entries
        if p.name not in SKIP_DIR_NAMES and not p.name.startswith(".")
    ]
    for i, p in enumerate(visible):
        is_last = i == len(visible) - 1
        branch = "└── " if is_last else "├── "
        lines.append(f"{prefix}{branch}{p.name}/" if p.is_dir() else f"{prefix}{branch}{p.name}")
        if p.is_dir() and current_depth < max_depth:
            ext = "    " if is_last else "│   "
            lines.extend(
                _tree_lines(p, max_depth=max_depth, current_depth=current_depth + 1, prefix=prefix + ext)
            )
    return lines


def _relative_paths_under(root: Path, sub: str, *, suffix: str | None) -> list[str]:
    base = root / sub
    if not base.is_dir():
        return []
    out: list[str] = []
    for p in _iter_files(base, suffix=suffix):
        out.append(str(p.relative_to(root)).replace("\\", "/"))
    return sorted(out)


def _dir_top_level(root: Path, sub: str) -> list[str]:
    base = root / sub
    if not base.is_dir():
        return []
    names: list[str] = []
    for p in sorted(base.iterdir()):
        if p.name in SKIP_DIR_NAMES or p.name.startswith("."):
            continue
        names.append(p.name + ("/" if p.is_dir() else ""))
    return names


def _parse_pyproject_dependencies(text: str) -> list[str]:
    """Minimal parse: lines inside dependencies = [ ... ] under [project]."""
    lines = text.splitlines()
    in_project = False
    in_deps = False
    deps: list[str] = []
    for raw in lines:
        line = raw.strip()
        if line.startswith("[") and line.endswith("]"):
            in_project = line.strip("[]") == "project"
            in_deps = False
            continue
        if not in_project:
            continue
        if line.startswith("dependencies") and "[" in line:
            in_deps = True
            continue
        if in_deps:
            if line.startswith("]"):
                break
            if line.startswith('"') or line.startswith("'"):
                dep = line.strip().rstrip(",").strip('"').strip("'")
                if dep:
                    deps.append(dep)
    return deps


def main() -> int:
    root = repo_root()
    out_dir = root / "vault" / "raw" / "project"
    out_dir.mkdir(parents=True, exist_ok=True)

    git_commit = _git(root, "rev-parse", "HEAD")
    git_branch = _git(root, "rev-parse", "--abbrev-ref", "HEAD")
    git_dirty = _git(root, "status", "--porcelain") not in (None, "")

    meta = {
        "generated_at_utc": datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z"),
        "repository_root": str(root),
        "git": {
            "commit": git_commit,
            "branch": git_branch,
            "dirty": git_dirty,
        },
    }
    (out_dir / "SNAPSHOT_META.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")

    versions: dict[str, object] = {}
    pyproject_path = root / "backend" / "pyproject.toml"
    pyproject_text = _read_utf8(pyproject_path)
    if pyproject_text:
        versions["backend_pyproject"] = {
            "path": "backend/pyproject.toml",
            "sha256": _sha256_text(pyproject_text),
            "dependencies": _parse_pyproject_dependencies(pyproject_text),
        }
        for line in pyproject_text.splitlines():
            if line.strip().startswith("requires-python"):
                versions["backend_requires_python"] = line.split("=", 1)[-1].strip().strip('"')
                break

    pkg_path = root / "frontend" / "package.json"
    pkg_text = _read_utf8(pkg_path)
    if pkg_text:
        try:
            pkg = json.loads(pkg_text)
            versions["frontend_package"] = {
                "path": "frontend/package.json",
                "sha256": _sha256_text(pkg_text),
                "name": pkg.get("name"),
                "version": pkg.get("version"),
                "scripts": sorted((pkg.get("scripts") or {}).keys()),
                "dependencies": sorted((pkg.get("dependencies") or {}).keys()),
                "devDependencies": sorted((pkg.get("devDependencies") or {}).keys()),
            }
        except json.JSONDecodeError as e:
            versions["frontend_package"] = {"error": str(e)}

    root_pkg = root / "package.json"
    root_pkg_text = _read_utf8(root_pkg)
    if root_pkg_text:
        try:
            rp = json.loads(root_pkg_text)
            versions["root_package"] = {
                "path": "package.json",
                "sha256": _sha256_text(root_pkg_text),
                "scripts": sorted((rp.get("scripts") or {}).keys()),
            }
        except json.JSONDecodeError as e:
            versions["root_package"] = {"error": str(e)}

    (out_dir / "versions.json").write_text(json.dumps(versions, indent=2) + "\n", encoding="utf-8")

    layout = {
        "backend_app_py_files": _relative_paths_under(root, "backend/app", suffix=".py"),
        "backend_tests_py_files": _relative_paths_under(root, "backend/tests", suffix=".py"),
        "frontend_src_top_level": _dir_top_level(root, "frontend/src"),
        "frontend_e2e_present": (root / "frontend" / "e2e").is_dir(),
        "github_workflows": sorted(
            p.name for p in (root / ".github" / "workflows").glob("*.yml")
        )
        if (root / ".github" / "workflows").is_dir()
        else [],
        "justfile_present": (root / "justfile").is_file(),
    }
    (out_dir / "layout.json").write_text(json.dumps(layout, indent=2) + "\n", encoding="utf-8")

    trees: dict[str, str] = {}
    for label, rel, depth in (
        ("backend_app", "backend/app", 4),
        ("backend_tests", "backend/tests", 3),
        ("frontend_src", "frontend/src", 3),
    ):
        base = root / rel
        if base.is_dir():
            lines = [f"{rel}/", *_tree_lines(base, max_depth=depth)]
            trees[label] = "\n".join(lines) + "\n"
        else:
            trees[label] = f"(missing) {rel}/\n"

    (out_dir / "trees.txt").write_text(
        "\n".join(f"=== {k} ===\n{v}" for k, v in trees.items()),
        encoding="utf-8",
    )

    contract_excerpts: list[str] = []
    for rel in ("AGENTS.md", "backend/AGENTS.md", "frontend/AGENTS.md", "vault/README.md"):
        p = root / rel
        text = _read_utf8(p, max_bytes=80_000)
        if text is None:
            contract_excerpts.append(f"=== {rel} (missing) ===\n\n")
            continue
        lines = text.splitlines()
        head = "\n".join(lines[:60])
        contract_excerpts.append(f"=== {rel} (first 60 lines, sha256={_sha256_text(text)}) ===\n{head}\n\n")
    (out_dir / "contract_excerpts.md").write_text("".join(contract_excerpts), encoding="utf-8")

    justfile = root / "justfile"
    jf = _read_utf8(justfile, max_bytes=120_000)
    if jf:
        (out_dir / "justfile_excerpt.txt").write_text(
            "=== justfile (full file) ===\n" + jf + ("\n" if not jf.endswith("\n") else ""),
            encoding="utf-8",
        )

    readme = out_dir / "README.md"
    readme.write_text(
        "# `vault/raw/project` — машинный снимок репозитория\n\n"
        "Слой **raw**: сюда попадают **только** автоматически сгенерированные файлы "
        "(опора для сверки с остальным ``vault/``).\n\n"
        "- **Не редактировать вручную** — при следующем запуске `just vault-snapshot` изменения затрутся.\n"
        "- Агент читает снимок и **обновляет** остальной `vault/` (`structure/`, `context/`, `daily-changes/`, при необходимости `agent/`).\n"
        "- Команда: `just vault-snapshot` или `python3 scripts/vault_project_snapshot.py` из корня репозитория.\n",
        encoding="utf-8",
    )

    print(f"Wrote snapshot to {out_dir.relative_to(root)}/", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""FlowRig repository mapper.

Produces a compact repository audit for Codex or humans.
No third-party dependencies.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

IGNORE_DIRS = {
    ".git", ".hg", ".svn", ".venv", "venv", "env", "node_modules", "dist", "build",
    "target", ".next", ".nuxt", ".turbo", ".cache", "coverage", "htmlcov", "__pycache__",
    ".pytest_cache", ".mypy_cache", ".ruff_cache", ".gradle", ".idea", ".vscode",
}

LANG_BY_EXT = {
    ".py": "Python",
    ".js": "JavaScript",
    ".jsx": "JavaScript/React",
    ".ts": "TypeScript",
    ".tsx": "TypeScript/React",
    ".java": "Java",
    ".kt": "Kotlin",
    ".kts": "Kotlin",
    ".go": "Go",
    ".rs": "Rust",
    ".c": "C",
    ".h": "C/C++ header",
    ".cpp": "C++",
    ".cc": "C++",
    ".cxx": "C++",
    ".hpp": "C++ header",
    ".cs": "C#",
    ".swift": "Swift",
    ".rb": "Ruby",
    ".php": "PHP",
    ".dart": "Dart",
    ".scala": "Scala",
    ".lua": "Lua",
    ".r": "R",
    ".sh": "Shell",
    ".ps1": "PowerShell",
    ".sql": "SQL",
    ".yaml": "YAML",
    ".yml": "YAML",
    ".json": "JSON",
    ".toml": "TOML",
    ".md": "Markdown",
}

MANIFESTS = {
    "package.json": "Node package manifest",
    "pnpm-lock.yaml": "pnpm lockfile",
    "yarn.lock": "Yarn lockfile",
    "package-lock.json": "npm lockfile",
    "bun.lockb": "Bun lockfile",
    "bun.lock": "Bun lockfile",
    "pyproject.toml": "Python project manifest",
    "requirements.txt": "Python requirements",
    "requirements-dev.txt": "Python dev requirements",
    "poetry.lock": "Poetry lockfile",
    "uv.lock": "uv lockfile",
    "Pipfile": "Pipenv manifest",
    "Cargo.toml": "Rust manifest",
    "Cargo.lock": "Rust lockfile",
    "go.mod": "Go module",
    "go.sum": "Go lock checksum",
    "pom.xml": "Maven project",
    "build.gradle": "Gradle build",
    "build.gradle.kts": "Gradle Kotlin build",
    "settings.gradle": "Gradle settings",
    "Gemfile": "Ruby bundle manifest",
    "composer.json": "PHP Composer manifest",
    "pubspec.yaml": "Dart/Flutter manifest",
    "Makefile": "Make command file",
    "Justfile": "Just command file",
    "Dockerfile": "Docker build file",
    "docker-compose.yml": "Docker Compose",
    "docker-compose.yaml": "Docker Compose",
}

INSTRUCTION_FILES = {
    "AGENTS.md": "Codex/agent instructions",
    ".github/copilot-instructions.md": "GitHub Copilot instructions",
    ".cursorrules": "Cursor rules",
    ".windsurfrules": "Windsurf rules",
}

TEST_DIR_NAMES = {"test", "tests", "spec", "specs", "__tests__", "e2e", "integration"}
CI_DIRS = [".github/workflows", ".gitlab-ci.yml", ".circleci", "azure-pipelines.yml", "Jenkinsfile"]


def iter_files(root: Path, max_files: int) -> list[Path]:
    out: list[Path] = []
    for current, dirs, files in os.walk(root):
        cur = Path(current)
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS and not d.startswith(".") or d in {".github"}]
        for file in files:
            path = cur / file
            try:
                rel = path.relative_to(root)
            except ValueError:
                continue
            if any(part in IGNORE_DIRS for part in rel.parts):
                continue
            out.append(path)
            if len(out) >= max_files:
                return out
    return out


def read_text(path: Path, max_bytes: int = 200_000) -> str:
    try:
        data = path.read_bytes()[:max_bytes]
        return data.decode("utf-8", errors="replace")
    except OSError:
        return ""


def rel(root: Path, path: Path) -> str:
    return str(path.relative_to(root)).replace(os.sep, "/")


def detect_package_scripts(path: Path) -> dict[str, str]:
    text = read_text(path)
    try:
        data = json.loads(text)
    except Exception:
        return {}
    scripts = data.get("scripts")
    if not isinstance(scripts, dict):
        return {}
    return {str(k): str(v) for k, v in scripts.items()}


def detect_make_targets(path: Path) -> list[str]:
    text = read_text(path)
    targets = []
    for line in text.splitlines():
        if line.startswith("\t") or line.startswith(" ") or line.strip().startswith("#"):
            continue
        m = re.match(r"^([A-Za-z0-9_.-]+):(?:\s|$)", line)
        if m and not m.group(1).startswith("."):
            targets.append(m.group(1))
    return sorted(set(targets))[:50]


def detect_just_recipes(path: Path) -> list[str]:
    text = read_text(path)
    recipes = []
    for line in text.splitlines():
        if not line or line.startswith((" ", "\t", "#")):
            continue
        m = re.match(r"^([A-Za-z0-9_.-]+)(?:\s.*)?:", line)
        if m:
            recipes.append(m.group(1))
    return sorted(set(recipes))[:50]


def infer_commands(manifests: list[str], package_scripts: dict[str, dict[str, str]], make_targets: dict[str, list[str]], just_recipes: dict[str, list[str]]) -> list[dict[str, str]]:
    cmds: list[dict[str, str]] = []
    manifest_set = set(Path(m).name for m in manifests)

    def add(kind: str, command: str, reason: str) -> None:
        if not any(c["command"] == command for c in cmds):
            cmds.append({"kind": kind, "command": command, "reason": reason})

    for manifest, scripts in package_scripts.items():
        package_manager = "npm"
        names = set(Path(m).name for m in manifests)
        if "pnpm-lock.yaml" in names:
            package_manager = "pnpm"
        elif "yarn.lock" in names:
            package_manager = "yarn"
        elif "bun.lock" in names or "bun.lockb" in names:
            package_manager = "bun"
        for script_name in ["test", "lint", "typecheck", "check", "build", "format", "dev"]:
            if script_name in scripts:
                if package_manager == "yarn":
                    cmd = f"yarn {script_name}"
                elif package_manager == "bun":
                    cmd = f"bun run {script_name}"
                else:
                    cmd = f"{package_manager} run {script_name}"
                add(script_name, cmd, f"script in {manifest}")

    for makefile, targets in make_targets.items():
        for target in ["test", "lint", "typecheck", "check", "build", "format", "ci"]:
            if target in targets:
                add(target, f"make {target}", f"target in {makefile}")

    for justfile, recipes in just_recipes.items():
        for recipe in ["test", "lint", "typecheck", "check", "build", "format", "ci"]:
            if recipe in recipes:
                add(recipe, f"just {recipe}", f"recipe in {justfile}")

    if "pyproject.toml" in manifest_set:
        add("test", "pytest", "Python project manifest present; verify before using")
        add("lint", "ruff check .", "Common Python lint command; verify config exists")
    elif "requirements.txt" in manifest_set:
        add("test", "pytest", "Python requirements present; verify before using")

    if "Cargo.toml" in manifest_set:
        add("test", "cargo test", "Rust manifest present")
        add("build", "cargo build", "Rust manifest present")
        add("lint", "cargo clippy", "Rust manifest present; verify clippy installed")

    if "go.mod" in manifest_set:
        add("test", "go test ./...", "Go module present")
        add("build", "go build ./...", "Go module present")

    if "pom.xml" in manifest_set:
        add("test", "mvn test", "Maven project present")
        add("build", "mvn package", "Maven project present")

    if "build.gradle" in manifest_set or "build.gradle.kts" in manifest_set:
        add("test", "./gradlew test", "Gradle project present")
        add("build", "./gradlew build", "Gradle project present")

    if "pubspec.yaml" in manifest_set:
        add("test", "dart test", "Dart/Flutter manifest present; use flutter test for Flutter apps")
        add("build", "dart analyze", "Dart/Flutter manifest present")

    return cmds


def find_ci(root: Path) -> list[str]:
    found: list[str] = []
    for entry in CI_DIRS:
        path = root / entry
        if path.is_file():
            found.append(entry)
        elif path.is_dir():
            for f in sorted(path.glob("*")):
                if f.is_file():
                    found.append(rel(root, f))
    return found


def find_test_dirs(root: Path) -> list[str]:
    found: set[str] = set()
    for current, dirs, _files in os.walk(root):
        cur = Path(current)
        if any(part in IGNORE_DIRS for part in cur.relative_to(root).parts if cur != root):
            dirs[:] = []
            continue
        for d in dirs:
            if d in TEST_DIR_NAMES or d.lower() in TEST_DIR_NAMES:
                found.add(rel(root, cur / d))
    return sorted(found)[:100]


def analyze(root: Path, max_files: int) -> dict[str, Any]:
    files = iter_files(root, max_files=max_files)
    language_counts: Counter[str] = Counter()
    ext_counts: Counter[str] = Counter()
    manifests: list[str] = []
    instructions: list[str] = []
    package_scripts: dict[str, dict[str, str]] = {}
    make_targets: dict[str, list[str]] = {}
    just_recipes: dict[str, list[str]] = {}

    for path in files:
        relative = rel(root, path)
        name = path.name
        ext = path.suffix.lower()
        if ext:
            ext_counts[ext] += 1
        if ext in LANG_BY_EXT:
            language_counts[LANG_BY_EXT[ext]] += 1
        if name in MANIFESTS:
            manifests.append(relative)
            if name == "package.json":
                package_scripts[relative] = detect_package_scripts(path)
            elif name == "Makefile":
                make_targets[relative] = detect_make_targets(path)
            elif name == "Justfile":
                just_recipes[relative] = detect_just_recipes(path)
        if relative in INSTRUCTION_FILES or name in INSTRUCTION_FILES:
            instructions.append(relative)

    commands = infer_commands(manifests, package_scripts, make_targets, just_recipes)
    ci = find_ci(root)
    test_dirs = find_test_dirs(root)

    risk_hints = []
    risky_names = {
        "auth": "Authentication/authorization surface",
        "permission": "Permission logic",
        "payment": "Payment/billing surface",
        "billing": "Payment/billing surface",
        "migration": "Database/schema migration surface",
        "db": "Database surface",
        "database": "Database surface",
        "secret": "Secret/token handling surface",
        "token": "Secret/token handling surface",
        "crypto": "Cryptography surface",
        "shell": "Shell/command execution surface",
        "subprocess": "Shell/command execution surface",
    }
    for path in files:
        lower = rel(root, path).lower()
        for needle, label in risky_names.items():
            if needle in lower:
                risk_hints.append({"path": rel(root, path), "risk": label})
                break
    risk_hints = risk_hints[:50]

    return {
        "root": str(root),
        "scanned_files": len(files),
        "languages": language_counts.most_common(20),
        "extensions": ext_counts.most_common(20),
        "manifests": sorted(manifests),
        "instruction_files": sorted(instructions),
        "ci": sorted(ci),
        "test_dirs": test_dirs,
        "package_scripts": package_scripts,
        "make_targets": make_targets,
        "just_recipes": just_recipes,
        "suggested_commands": commands,
        "risk_hints": risk_hints,
    }


def to_markdown(data: dict[str, Any]) -> str:
    lines = []
    lines.append("# FlowRig Repository Map")
    lines.append("")
    lines.append(f"Root: `{data['root']}`")
    lines.append(f"Scanned files: `{data['scanned_files']}`")
    lines.append("")

    lines.append("## Languages")
    if data["languages"]:
        for lang, count in data["languages"]:
            lines.append(f"- {lang}: {count}")
    else:
        lines.append("- No dominant language detected.")
    lines.append("")

    lines.append("## Manifests and build files")
    if data["manifests"]:
        for item in data["manifests"]:
            lines.append(f"- `{item}`")
    else:
        lines.append("- None detected.")
    lines.append("")

    lines.append("## Instruction files")
    if data["instruction_files"]:
        for item in data["instruction_files"]:
            lines.append(f"- `{item}`")
    else:
        lines.append("- No common agent instruction file detected. Consider adding `AGENTS.md`.")
    lines.append("")

    lines.append("## CI")
    if data["ci"]:
        for item in data["ci"]:
            lines.append(f"- `{item}`")
    else:
        lines.append("- No common CI file detected.")
    lines.append("")

    lines.append("## Test directories")
    if data["test_dirs"]:
        for item in data["test_dirs"]:
            lines.append(f"- `{item}`")
    else:
        lines.append("- No common test directory detected.")
    lines.append("")

    lines.append("## Suggested commands")
    if data["suggested_commands"]:
        lines.append("| Kind | Command | Source / confidence note |")
        lines.append("|---|---|---|")
        for cmd in data["suggested_commands"]:
            lines.append(f"| {cmd['kind']} | `{cmd['command']}` | {cmd['reason']} |")
    else:
        lines.append("- No commands inferred. Read docs/CI manually.")
    lines.append("")

    if data["package_scripts"]:
        lines.append("## Package scripts")
        for manifest, scripts in data["package_scripts"].items():
            lines.append(f"### `{manifest}`")
            if scripts:
                for name, value in sorted(scripts.items()):
                    lines.append(f"- `{name}`: `{value}`")
            else:
                lines.append("- No scripts detected.")
            lines.append("")

    lines.append("## Risk hints")
    if data["risk_hints"]:
        lines.append("| Path | Why it may need extra review |")
        lines.append("|---|---|")
        for item in data["risk_hints"]:
            lines.append(f"| `{item['path']}` | {item['risk']} |")
    else:
        lines.append("- No obvious high-risk filenames detected. This is not a security audit.")
    lines.append("")

    lines.append("## Recommended next step")
    lines.append("- Read the highest-signal manifest/README/CI files, then run the narrowest relevant verification command before editing.")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Map a repository for FlowRig/Codex workflows.")
    parser.add_argument("path", nargs="?", default=".", help="Repository root to inspect.")
    parser.add_argument("--format", choices=["md", "json"], default="md", help="Output format.")
    parser.add_argument("--max-files", type=int, default=5000, help="Maximum files to scan.")
    args = parser.parse_args(argv)

    root = Path(args.path).resolve()
    if not root.exists() or not root.is_dir():
        print(f"error: not a directory: {root}", file=sys.stderr)
        return 2

    data = analyze(root, max_files=max(1, args.max_files))
    if args.format == "json":
        print(json.dumps(data, indent=2, sort_keys=True))
    else:
        print(to_markdown(data))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

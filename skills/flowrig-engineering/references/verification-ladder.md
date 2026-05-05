# Verification Ladder

Use the strongest affordable checks for the task. Start targeted, then widen.

## Level 0 — Static inspection

- Read affected files.
- Check imports, names, types, and obvious edge cases.
- Review final diff.

Use only when commands cannot run.

## Level 1 — Targeted check

- Run one focused unit test.
- Run a repro script.
- Run a single package test command.
- Run a compile/typecheck for the changed package.

Best default for narrow bug fixes.

## Level 2 — Package check

- Full package test suite.
- Package lint/typecheck.
- Package build.

Best default for feature work in one package.

## Level 3 — Integration check

- App build.
- API smoke test.
- UI smoke test.
- Database migration dry run.
- Docker compose smoke check.

Use when behavior crosses boundaries.

## Level 4 — Release check

- CI-equivalent suite.
- Security scan if configured.
- Dependency audit if dependencies changed.
- Docs generation if docs are generated.
- End-to-end tests if configured.

Use before ship/PR handoff.

## Reporting rules

Always report checks as:

| Check | Command | Status | Notes |
|---|---|---|---|
| Targeted tests | `...` | pass/fail/not run | ... |

Never report a command as passing unless it completed successfully.

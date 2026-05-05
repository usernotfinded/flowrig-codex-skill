# Workflow Map

Use this as the default map for repository work.

## A. Audit-only workflow

1. Read repo instructions and manifests.
2. Run the repo mapper.
3. Identify languages, package managers, commands, and risk areas.
4. Return an audit with missing setup/test instructions and recommended next steps.

No edits.

## B. Bug-fix workflow

1. Reproduce or identify the failing behavior.
2. Find the narrowest ownership boundary.
3. Patch the smallest possible location.
4. Add/update regression coverage.
5. Run targeted test, then broader relevant checks.
6. Review final diff.

## C. Feature workflow

1. Convert the request into a vertical slice.
2. Identify existing conventions for UI/API/service/data layers.
3. Implement the smallest end-to-end path first.
4. Add tests at the lowest effective level plus one integration/smoke check when available.
5. Update docs/config only where user-facing behavior changed.

## D. Refactor workflow

1. Define what must remain behaviorally identical.
2. Add or identify safety tests before refactoring.
3. Move in tiny increments.
4. Avoid mixed refactor + feature changes.
5. Verify public APIs, imports, generated artifacts, and migrations.

## E. Build/CI workflow

1. Read CI first.
2. Reproduce the failing command locally if possible.
3. Fix root cause rather than weakening CI.
4. Keep version pin changes explicit.
5. Report environment assumptions.

## F. Review workflow

1. Inspect diff against the user's objective.
2. Check correctness, edge cases, tests, docs, security, and maintainability.
3. Classify findings by severity.
4. Patch only high-confidence issues or return review notes if uncertain.

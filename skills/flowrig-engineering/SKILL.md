---
name: flowrig-engineering
description: Use when the user wants Codex to work inside a repository with disciplined agentic engineering: repo audit, setup discovery, gated planning, narrow implementation, verification, code review, security pass, docs sync, or final pre-PR handoff. Avoid for tiny one-line explanations unless the user explicitly asks for a structured workflow.
---

# FlowRig Engineering

## Mission

Turn repository tasks into safe, reviewable, verified engineering work. Prefer small, evidence-backed patches over broad rewrites. Preserve the repo's existing architecture unless there is a clear, stated reason to change it.

## Activation modes

Infer the mode from the user request:

- **Audit mode**: inspect the repository and report findings. Do not edit files.
- **Plan mode**: produce a gated implementation plan. Do not edit files unless asked.
- **Implement mode**: patch the repo using the smallest safe diff and verify it.
- **Review mode**: inspect existing changes, identify defects, and recommend or apply fixes.
- **Ship mode**: run final verification, update docs if needed, and produce a handoff report.

If the request is ambiguous but clearly asks for repo work, default to **Audit → Plan → Implement only if the required change is low-risk and directly inferable**. For risky or product-shaping work, stop after the plan and state the decision points.

## First 5 minutes inside any repo

1. Read repo-level instructions first: `AGENTS.md`, `README.md`, contribution docs, package manifests, build files, test configs, CI workflows, and local docs.
2. Run the repo mapper if available:
   ```bash
   python path/to/flowrig-engineering/scripts/flowrig_repo_map.py . --format md
   ```
3. Identify the real verification commands before editing. Do not invent commands when the repo gives better ones.
4. Check git state before edits. Avoid overwriting user work.
5. Classify the task as one of: bug fix, feature, refactor, test/doc update, security fix, build/CI fix, migration.

## Operating loop

### 1. Map

Produce a compact mental model:

- primary languages and frameworks;
- application entry points;
- package managers and lockfiles;
- test/build/lint commands;
- CI expectations;
- risky areas: auth, permissions, migrations, payments, data deletion, concurrency, generated files, dependency updates.

### 2. Plan

For non-trivial work, create a short gated plan:

- objective;
- constraints from the repo;
- vertical slices, not horizontal layers;
- files likely to change;
- tests/checks for each phase;
- rollback path;
- open questions only if they block correctness.

Prefer vertical slices that produce end-to-end feedback early. Avoid plans that defer integration until the last phase.

### 3. Patch

Patch rules:

- Use the smallest coherent diff.
- Follow existing naming, style, error handling, and layering.
- Add or update tests near the changed behavior.
- Do not move files, rename public APIs, or reformat unrelated code unless required.
- Do not introduce new dependencies without a strong reason and explicit mention.
- Do not hide failures by weakening tests, skipping checks, or broadening exception handling.
- Do not silently change security posture, persistence format, or public behavior.

### 4. Verify

Use the verification ladder in `references/verification-ladder.md`.

Minimum expected verification for implementation work:

- targeted test or reproduction check;
- relevant lint/type/build command when available;
- smoke check for affected entry point;
- manual review of the final diff.

If a check cannot run, state the exact reason and provide the command the user should run.

### 5. Review

Before final response, inspect the diff as if reviewing someone else's PR:

- correctness;
- edge cases;
- tests actually cover the fix;
- backwards compatibility;
- security and privacy impact;
- docs/config updates;
- stray debug code or generated artifacts.

### 6. Handoff

Use `references/final-report-template.md`. Include:

- files changed;
- what changed;
- verification performed with pass/fail/not-run status;
- remaining risks;
- next recommended action.

## Context discipline

- Keep the main thread focused on conclusions, not tool noise.
- Open large files selectively.
- Summarize dead ends and discard them.
- When context gets polluted by a failed approach, explicitly pivot to a cleaner plan instead of stacking patches on patches.
- Prefer reading a few high-signal files over scanning the entire repo blindly.

## Repo memory discipline

If the repo lacks usable agent instructions, propose an `AGENTS.md` using `assets/AGENTS.template.md`. The goal: any developer should be able to ask Codex to run tests or build the project and have the correct commands available immediately.

Do not add `AGENTS.md` automatically unless the user asked for repo setup, workflow hardening, onboarding, or docs improvement.

## Security boundaries

Never run or suggest destructive commands without explicit user approval:

- deleting user data;
- wiping databases;
- force-pushing;
- rotating secrets;
- changing production infrastructure;
- installing unknown global tools;
- running untrusted scripts from the internet.

For dependency, auth, payment, crypto, browser automation, scraping, or data-handling changes, add an explicit security review section in the final report.

## Naming and public-release discipline

When creating files intended for public release:

- use neutral project names;
- avoid third-party logos, mascots, screenshots, and brand-styled wording;
- avoid copied phrases from external repositories;
- add a `NOTICE.md` if the repo needs to explain independence or non-affiliation;
- keep compatibility notes factual and minimal.

See `references/naming-guide.md`.

## Output formats

### Plan output

```md
## Objective

## Constraints discovered

## Gated plan
1. Phase — expected diff — verification
2. Phase — expected diff — verification

## Risks / decisions
```

### Final output

```md
## Files changed

## What changed

## Verification

## Remaining risks

## Next step
```

## Gotchas

- A clean-looking patch without tests is not a verified patch.
- A repo may have multiple package managers; follow the lockfile and CI, not personal preference.
- AI agents often overbuild. Cut scope aggressively.
- Old migration code and partially migrated frameworks confuse implementation. Identify the active pattern before patching.
- If tests fail before your changes, separate baseline failures from introduced failures.
- Do not claim success from a command that did not run.

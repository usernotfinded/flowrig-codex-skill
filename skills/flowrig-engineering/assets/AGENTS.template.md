# Agent Instructions

## Project overview

Describe the project in 3-6 lines:

- what it builds;
- main runtime/service/app;
- primary languages/frameworks;
- critical business or safety constraints.

## Setup

```bash
# install dependencies
```

## Common commands

```bash
# run all tests
# run targeted tests
# run lint
# run typecheck
# run build
# run local app/service
```

## Repository map

- `apps/...`: purpose
- `packages/...`: purpose
- `src/...`: purpose
- `tests/...`: purpose

## Coding conventions

- Follow existing style in nearby files.
- Keep diffs narrow.
- Add tests near changed behavior.
- Do not introduce dependencies without a clear reason.

## Verification policy

Before final response, report exactly which checks were run and their result.

Minimum for code changes:

1. targeted test or repro;
2. relevant package check;
3. final diff review.

## Safety rules

- Do not run destructive commands without explicit permission.
- Do not modify production configuration unless asked.
- Do not commit secrets or generated credentials.
- Do not rewrite unrelated code.

## Known pitfalls

- Add repo-specific pitfalls here.

# Agent Instructions

## Project overview

This repository packages `flowrig-engineering`, a Codex skill for gated repository work: audit, plan, patch, verify, review, and handoff.

## Common commands

```bash
python skills/flowrig-engineering/scripts/flowrig_repo_map.py . --format md
python skills/flowrig-engineering/scripts/flowrig_repo_map.py . --format json
```

## Repository map

- `skills/flowrig-engineering/SKILL.md`: main Codex skill instructions and trigger metadata.
- `skills/flowrig-engineering/references/`: progressive-disclosure guides for workflow, verification, review, naming, and final reports.
- `skills/flowrig-engineering/scripts/flowrig_repo_map.py`: dependency-free repository mapper.
- `skills/flowrig-engineering/assets/AGENTS.template.md`: template for adding agent instructions to target repos.

## Coding conventions

- Keep this package vendor-neutral.
- Do not add third-party logos, screenshots, mascots, copied prose, or brand-styled command names.
- Keep scripts dependency-free unless there is a strong reason.
- Preserve Python 3.10+ compatibility for scripts.

## Verification policy

Before final response, run at least:

```bash
python skills/flowrig-engineering/scripts/flowrig_repo_map.py . --format md
python skills/flowrig-engineering/scripts/flowrig_repo_map.py . --format json
```

## Safety rules

- Do not add remote-install scripts that pipe internet content into a shell.
- Do not claim official affiliation with any vendor or upstream project.

# FlowRig Codex Skill

**FlowRig** is a neutral, repository-ready Codex skill for disciplined agentic engineering.

It packages a repeatable workflow for turning vague coding requests into safe, reviewable repository changes:

1. map the repo,
2. infer conventions,
3. plan vertical slices,
4. implement narrow diffs,
5. verify with the strongest available checks,
6. return a clear ship report.

The package intentionally avoids third-party product names, logos, mascots, command names, and copied prose. It is written as an original Codex-native skill with generic engineering terminology.

## Repository structure

```text
flowrig-codex-skill/
├── README.md
├── LICENSE
├── NOTICE.md
├── .gitignore
└── skills/
    └── flowrig-engineering/
        ├── SKILL.md
        ├── assets/
        │   └── AGENTS.template.md
        ├── references/
        │   ├── final-report-template.md
        │   ├── naming-guide.md
        │   ├── repo-memory-template.md
        │   ├── review-rubric.md
        │   ├── verification-ladder.md
        │   └── workflow-map.md
        └── scripts/
            └── flowrig_repo_map.py
```

## Install

Copy the skill folder into the location where your Codex installation loads custom skills.

Common local layout:

```bash
mkdir -p ~/.codex/skills
cp -R skills/flowrig-engineering ~/.codex/skills/
```

Project-local layout:

```bash
mkdir -p .codex/skills
cp -R skills/flowrig-engineering .codex/skills/
```

Then invoke it explicitly in Codex:

```text
Use $flowrig-engineering to audit this repository, create a gated plan, implement the smallest safe patch, and verify it.
```

## Recommended first command inside a repo

```bash
python ~/.codex/skills/flowrig-engineering/scripts/flowrig_repo_map.py . --format md
```

For project-local installs:

```bash
python .codex/skills/flowrig-engineering/scripts/flowrig_repo_map.py . --format md
```

## What the skill is good for

- New feature implementation with a gated plan.
- Bug fixing with repro-first behavior.
- Refactors that must stay narrow and testable.
- Repo onboarding and command discovery.
- Final pre-PR quality review.
- Updating `AGENTS.md` so future agent runs work on the first try.

## What it avoids

- Broad rewrites when a targeted patch is enough.
- Fabricated verification claims.
- Silent destructive operations.
- Vendor-specific branding or borrowed phrasing.
- Turning every task into a huge process.

## Publishing notes

Suggested GitHub repository names:

| Name | Positioning |
|---|---|
| `flowrig-codex-skill` | Main recommendation. Clear and neutral. |
| `shiploop-codex` | More product-like, focused on delivery. |
| `repo-rigging-skill` | Technical, repo-harness angle. |
| `codex-gated-engineering` | Descriptive, less brandable. |
| `patchdeck-codex` | Compact, patch/review oriented. |

Suggested skill names:

| Skill name | Use when |
|---|---|
| `flowrig-engineering` | Balanced planning + implementation + review. |
| `shiploop-engineering` | Shipping workflow emphasis. |
| `patchdeck-review` | Review/fix loop emphasis. |
| `repo-rig` | Short, tool-like name. |

## License

MIT. See [`LICENSE`](./LICENSE).

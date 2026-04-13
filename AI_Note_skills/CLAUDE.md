# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Claude Code skill library** — a collection of self-contained skills that provide domain-specific knowledge and examples for AI-assisted workflows. There is no build system, runtime code, or tests; the deliverables are Markdown/example files that Claude Code loads on demand.

## Skills

| Skill | Domain | Trigger |
|---|---|---|
| `emmylua-annotation` | EmmyLua type annotations for Lua | Lua type annotation work (`@class`, `@param`, `@field`, etc.) |
| `obsidian-bases` | Obsidian `.base` database-like views | Creating/editing `.base` files, note database views |
| `obsidian-markdown` | Obsidian Flavored Markdown | Writing/editing `.md` files for Obsidian vaults |
| `agent-creator` | Claude Code subagent creation | Creating custom agents/subagents, agent configuration, multi-agent workflows |
| `skill-creator` | Skill creation, eval, and optimization | Creating/modifying skills, running evals, benchmarking, improving trigger descriptions |

## Repository Layout

```
skills/             # All skills live here
hooks/              # Hook scripts
agents/             # Agent definitions
```

## Skill Structure Convention

Basic skills follow this layout:

```
<skill-name>/
  SKILL.md          # Main doc with YAML frontmatter (name + description trigger fields)
  examples/         # Reference examples loaded on demand
```

The `skill-creator` skill is more complex, including `scripts/` (Python eval/benchmark tooling), `agents/` (analyzer, comparator, grader), `eval-viewer/`, and `references/` (schemas.md + skill-features.md).

**SKILL.md frontmatter** — Beyond `name` and `description`, skills support advanced fields: `argument-hint`, `disable-model-invocation`, `user-invocable`, `allowed-tools`, `model`, `effort`, `context`, `agent`, `hooks`, `paths`, `shell`. See `skills/skill-creator/references/schemas.md` for the full field reference.

**Token optimization pattern** — SKILL.md files should stay under 500 lines. Detailed examples live in `examples/` or `references/` and must only be loaded via Read when the specific content is needed. Never load all support files at once.

## Language

The `emmylua-annotation` and `agent-creator` skills are written in Chinese (zh-CN). The `obsidian-bases` and `obsidian-markdown` skills are in English. Match the language of the existing skill when editing.

## Creating or Modifying Skills

- Keep SKILL.md under 500 lines; put detailed reference in `examples/` or `references/`.
- Frontmatter `description` should be thorough and slightly "pushy" — it determines trigger accuracy. Front-load key use cases (truncated to 250 chars in skill list). Include alternate phrasings users might use.
- Use `disable-model-invocation: true` for task skills with side effects (deploy, commit). Use `user-invocable: false` for background knowledge skills.
- Use `context: fork` + `agent` for skills that should run in isolated subagents.
- Support files should be self-contained and demonstrate real-world usage patterns.
- Skills follow the [AgentSkills.io](https://agentskills.io) open standard.

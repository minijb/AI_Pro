# Skill Advanced Features Reference

Detailed reference for advanced Claude Code skill features. Read the relevant section when you need to use a specific feature during skill creation. For the core workflow (draft → test → review → improve), see SKILL.md.

---

## Table of Contents

1. [Frontmatter Fields Quick Reference](#1-frontmatter-fields-quick-reference)
2. [String Substitutions](#2-string-substitutions)
3. [Dynamic Context Injection](#3-dynamic-context-injection)
4. [Skill Content Types](#4-skill-content-types)
5. [Invocation Control](#5-invocation-control)
6. [Subagent Execution](#6-subagent-execution)
7. [Skill Locations & Scoping](#7-skill-locations--scoping)
8. [Skill-Scoped Hooks](#8-skill-scoped-hooks)
9. [Path-Based Activation](#9-path-based-activation)
10. [Permission Control](#10-permission-control)
11. [Visual Output Pattern](#11-visual-output-pattern)
12. [Triggering Mechanics](#12-triggering-mechanics)
13. [Commands Merge Behavior](#13-commands-merge-behavior)

---

## 1. Frontmatter Fields Quick Reference

All fields are optional. `description` is recommended.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `name` | string | directory name | Display name and `/slash-command`. Lowercase, digits, hyphens only. Max 64 chars. |
| `description` | string | first paragraph | What the skill does and when to use it. Front-load key use cases — truncated to 250 chars in the skill list. |
| `argument-hint` | string | — | Autocomplete hint shown during `/` completion. E.g., `[issue-number]` or `[filename] [format]`. |
| `disable-model-invocation` | boolean | `false` | `true` = user-only via `/name`. Removes description from Claude's context entirely. |
| `user-invocable` | boolean | `true` | `false` = hidden from `/` menu. Claude can still auto-load it as background knowledge. |
| `allowed-tools` | string or list | all tools | Tools Claude can use without permission prompts when this skill is active. Space-separated or YAML list. |
| `model` | string | session model | Model override when this skill is active. |
| `effort` | string | session effort | Effort level: `low`, `medium`, `high`, `max` (max is Opus only). |
| `context` | string | inline | Set to `fork` to run in an isolated subagent context. |
| `agent` | string | `general-purpose` | Subagent type when `context: fork`. Options: `Explore`, `Plan`, `general-purpose`, or custom from `.claude/agents/`. |
| `hooks` | object | — | Skill-scoped hooks. Same YAML format as settings.json hooks. See [Section 8](#8-skill-scoped-hooks). |
| `paths` | string or list | all paths | Glob patterns limiting when the skill auto-activates. See [Section 9](#9-path-based-activation). |
| `shell` | string | `bash` | Shell for `` !`command` `` blocks. Options: `bash`, `powershell` (requires `CLAUDE_CODE_USE_POWERSHELL_TOOL=1`). |

---

## 2. String Substitutions

Skills support dynamic placeholders that are replaced before Claude sees the content:

| Variable | Description |
|----------|-------------|
| `$ARGUMENTS` | All arguments passed when invoking the skill. If not present in content and args are passed, appended as `ARGUMENTS: <value>`. |
| `$ARGUMENTS[N]` | Specific argument by 0-based index. E.g., `$ARGUMENTS[0]` = first arg. |
| `$N` | Shorthand for `$ARGUMENTS[N]`. E.g., `$0` = first arg, `$1` = second. |
| `${CLAUDE_SESSION_ID}` | Current session ID. Useful for logs or session-specific files. |
| `${CLAUDE_SKILL_DIR}` | Directory containing this skill's SKILL.md. Use in shell commands to reference bundled scripts regardless of cwd. |

**Example — migration skill with positional args:**

```yaml
---
name: migrate-component
description: Migrate a component from one framework to another
---

Migrate the $0 component from $1 to $2.
Preserve all existing behavior and tests.
```

Invoke: `/migrate-component SearchBar React Vue`

**Example — session logger:**

```yaml
---
name: session-logger
description: Log activity for this session
---

Log the following to logs/${CLAUDE_SESSION_ID}.log:

$ARGUMENTS
```

---

## 3. Dynamic Context Injection

The `` !`command` `` syntax runs a shell command **before** sending the skill content to Claude. The command output replaces the placeholder. This is preprocessing — Claude sees only the final result, not the command.

**Example — PR summary skill:**

```yaml
---
name: pr-summary
description: Summarize changes in a pull request
context: fork
agent: Explore
allowed-tools: Bash(gh *)
---

## Pull request context
- PR diff: !`gh pr diff`
- PR comments: !`gh pr view --comments`
- Changed files: !`gh pr diff --name-only`

## Your task
Summarize this pull request...
```

When this runs: each `` !`command` `` executes immediately, output replaces the placeholder, Claude receives the fully rendered prompt with actual PR data.

Use the `shell` frontmatter field to control which shell runs these commands (`bash` or `powershell`).

**Extended thinking:** To enable extended thinking in a skill, include the word `ultrathink` anywhere in the skill content.

---

## 4. Skill Content Types

Skills serve two purposes — choose the right pattern:

**Reference content** adds knowledge Claude applies to your current work. Conventions, patterns, style guides, domain knowledge. Runs inline so Claude can combine it with conversation context.

```yaml
---
name: api-conventions
description: API design patterns for this codebase
---

When writing API endpoints:
- Use RESTful naming conventions
- Return consistent error formats
- Include request validation
```

**Task content** gives Claude step-by-step instructions for a specific operation. These are typically user-invoked actions — add `disable-model-invocation: true` to prevent Claude from auto-triggering.

```yaml
---
name: deploy
description: Deploy the application to production
context: fork
disable-model-invocation: true
---

Deploy the application:
1. Run the test suite
2. Build the application
3. Push to the deployment target
```

---

## 5. Invocation Control

Two frontmatter fields control who can invoke a skill:

| Frontmatter | User can invoke | Claude can invoke | Context loading |
|-------------|:-:|:-:|---|
| (default) | Yes | Yes | Description always in context; full skill on invocation |
| `disable-model-invocation: true` | Yes | No | Description NOT in context; full skill when user invokes |
| `user-invocable: false` | No | Yes | Description always in context; full skill on invocation |

**When to use `disable-model-invocation: true`:** For skills with side effects or that you want to control timing — deploy, commit, send-slack-message. You don't want Claude deciding to deploy because the code looks ready.

**When to use `user-invocable: false`:** For background knowledge that isn't a command. A `legacy-system-context` skill explains how an old system works — Claude should know this when relevant, but `/legacy-system-context` isn't a meaningful user action.

---

## 6. Subagent Execution

Add `context: fork` to run the skill in an isolated subagent. The skill content becomes the subagent's task prompt. It will NOT have access to conversation history.

The `agent` field selects the subagent type:
- **`Explore`** — read-only, optimized for codebase exploration (Glob, Grep, Read)
- **`Plan`** — for designing implementation plans
- **`general-purpose`** (default) — full tool access
- **Custom** — any subagent defined in `.claude/agents/`

**Skills vs Subagents — two directions:**

| Method | System prompt | Task | Also loads |
|--------|--------------|------|------------|
| Skill with `context: fork` | From agent type | SKILL.md content | CLAUDE.md |
| Subagent with `skills` field | Subagent's markdown body | Claude's delegation message | Preloaded skills + CLAUDE.md |

**Example — deep research skill:**

```yaml
---
name: deep-research
description: Research a topic thoroughly
context: fork
agent: Explore
---

Research $ARGUMENTS thoroughly:

1. Find relevant files using Glob and Grep
2. Read and analyze the code
3. Summarize findings with specific file references
```

**Important:** `context: fork` only makes sense for skills with clear instructions. If your skill is just guidelines ("use these API conventions") without a task, the subagent gets guidelines but no actionable prompt and returns nothing useful.

---

## 7. Skill Locations & Scoping

Skills can live at four levels. Higher priority wins on name conflicts:

| Level | Path | Scope |
|-------|------|-------|
| Enterprise | Via managed settings | All users in org |
| Personal | `~/.claude/skills/<name>/SKILL.md` | All your projects |
| Project | `.claude/skills/<name>/SKILL.md` | This project only |
| Plugin | `<plugin>/skills/<name>/SKILL.md` | Where plugin is enabled |

Plugin skills use `plugin-name:skill-name` namespace and cannot conflict with other levels.

**Nested auto-discovery:** When working in a subdirectory, Claude Code auto-discovers skills from nested `.claude/skills/` directories. E.g., editing files in `packages/frontend/` also finds `packages/frontend/.claude/skills/`. Supports monorepo setups.

**Additional directories:** `--add-dir` grants file access. Skills in added directories' `.claude/skills/` are auto-loaded and support live change detection.

Skills follow the [AgentSkills.io](https://agentskills.io) open standard, extended with Claude Code-specific features (invocation control, subagent execution, dynamic context injection).

---

## 8. Skill-Scoped Hooks

The `hooks` frontmatter field defines hooks scoped to the skill's lifecycle. Same YAML format as settings.json hooks.

```yaml
---
name: safe-deploy
description: Deploy with pre-flight checks
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/pre-deploy-check.sh"
---
```

These hooks only run when the skill is active and are removed when the skill completes. See the [Hooks documentation](https://code.claude.com/docs/hooks) for the full event/config format.

---

## 9. Path-Based Activation

The `paths` field restricts when Claude auto-loads the skill. Claude only triggers it when working with files matching the glob patterns.

```yaml
---
name: react-conventions
description: React component conventions
paths: "src/components/**/*.tsx, src/hooks/**/*.ts"
---
```

Accepts comma-separated string or YAML list. Uses the same glob format as path-specific rules in CLAUDE.md.

---

## 10. Permission Control

Users can control which skills Claude can invoke via `/permissions`:

```
# Allow only specific skills
Skill(commit)
Skill(review-pr *)

# Deny specific skills
Skill(deploy *)
```

- `Skill(name)` — exact match
- `Skill(name *)` — prefix match with any arguments

Denying the `Skill` tool entirely disables all skill invocations.

Note: `user-invocable` only controls menu visibility, not `Skill` tool access. Use `disable-model-invocation: true` to prevent programmatic invocation.

---

## 11. Visual Output Pattern

Skills can bundle scripts that generate interactive HTML for visualization. The skill instructs Claude to run the bundled script, which does the heavy lifting:

```yaml
---
name: codebase-visualizer
description: Generate an interactive tree visualization of your codebase
allowed-tools: Bash(python *)
---

# Codebase Visualizer

Run the visualization script from your project root:

```bash
python ${CLAUDE_SKILL_DIR}/scripts/visualize.py .
```

This creates `codebase-map.html` and opens it in your browser.
```

This pattern works for any visual output: dependency graphs, test coverage reports, API docs, database schema diagrams. The bundled script handles generation; Claude handles orchestration.

---

## 12. Triggering Mechanics

Understanding how triggering works helps write better descriptions:

- Skill descriptions are loaded into Claude's context so it knows what's available. All names are always included, but descriptions may be **truncated to fit a character budget** — each entry is capped at 250 characters.
- The budget defaults to 1% of the context window (~8,000 chars fallback). Override with `SLASH_COMMAND_TOOL_CHAR_BUDGET` env var.
- **Front-load key use cases** in your description — content after 250 chars may not be seen.
- Skills only trigger for tasks Claude can't easily handle alone. Simple queries like "read this file" won't trigger skills even with matching descriptions. Complex, multi-step, or specialized queries reliably trigger.

**Implication for eval queries:** When testing trigger accuracy, use substantive, multi-step prompts — not simple one-liners. Simple queries won't trigger regardless of description quality.

---

## 13. Commands Merge Behavior

`.claude/commands/` files and `.claude/skills/` skills now work identically. A file at `.claude/commands/deploy.md` and a skill at `.claude/skills/deploy/SKILL.md` both create `/deploy`.

Key points:
- Existing `.claude/commands/` files continue to work with no changes needed
- Commands files support the same frontmatter fields as skills
- If a skill and command share the same name, the **skill takes priority**
- Skills add optional features commands don't have: supporting file directories, `context: fork`, `hooks`, `paths`

Migration is optional — commands keep working. Consider migrating when you need supporting files or advanced features.

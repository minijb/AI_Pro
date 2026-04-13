# Process Log: Fullstack Coordinator Agent Creation

## Sections of the Skill Referenced

1. **SKILL.md "什么是 Subagent"** -- Used to understand the core concepts, especially the distinction between subagent and agent teams, and the note that subagents cannot spawn child agents.

2. **SKILL.md "创建流程" (Creation Workflow)** -- Followed the 4-step process:
   - Step 1 (需求采集): Mapped user requirements -- coordinator pattern, 4 sub-agents, React+Node.js stack, main thread execution.
   - Step 2 (选择 Agent 类型): Selected "协调编排型" for the main agent, then identified the sub-agent types: 只读研究型 (researcher), 代码审查型 (frontend-reviewer, backend-reviewer), 测试执行型 (test-runner).
   - Step 3 (生成 Agent 文件): Generated all 5 markdown files.
   - Step 4 (验证与部署): Not executed since this is a test scenario.

3. **SKILL.md "Agent 类型速查表"** -- Used to determine correct tool sets and model choices for each agent type.

4. **SKILL.md "编写 Description 的最佳实践"** and **"系统提示编写指南"** -- Applied these guidelines when writing descriptions and system prompts for all agents.

5. **references/frontmatter-reference.md** -- Referenced for:
   - `Agent(type)` syntax in tools field (Section 3: 工具控制)
   - Model options (Section 2: 模型与性能)
   - Confirmation that `tools` field is comma-separated string format
   - Understanding `Agent(type1, type2)` allows listing multiple agent types

6. **examples/coordinator.md** -- Primary template for the coordinator agent.
7. **examples/researcher.md** -- Template for the researcher sub-agent.
8. **examples/code-reviewer.md** -- Template for both frontend-reviewer and backend-reviewer.
9. **examples/test-runner.md** -- Template for the test-runner sub-agent.

## Was the Coordinator Example Sufficient?

The coordinator example (`examples/coordinator.md`) was a good starting point but needed significant adaptation for this scenario:

**What it covered well:**
- The `Agent(type1, type2, ...)` syntax in the tools field
- The general coordination workflow pattern (analyze -> distribute -> collect)
- The critical note that subagents cannot spawn child agents, so the coordinator must run as `--agent`
- The output format structure
- The recommendation to use `opus` model

**What required adaptation:**
- The example uses 3 agent types (researcher, implementer, test-runner). This scenario requires 4 types (researcher, frontend-reviewer, backend-reviewer, test-runner), which meant extending the `Agent()` parameter list to 4 entries.
- The example has a generic "implementer" agent. This scenario requires two specialized reviewer agents instead, which is a different pattern (review vs. implementation).
- The workflow ordering is different: the example shows a linear flow (research -> implement -> test), while this scenario has a diamond pattern (research -> [frontend-review || backend-review] -> test) with explicit parallelism in the middle.
- The example does not demonstrate how to handle conditional execution (e.g., skip frontend-reviewer if no frontend files changed).

## Did the Skill Guide on Creating Companion Sub-Agents?

**Partially.** The skill provides individual examples for each agent type (researcher, code-reviewer, test-runner) which served as excellent templates. However:

- The skill does **not explicitly discuss** the workflow of creating a coordinator **together with** its companion sub-agents as a cohesive set. There is no section like "When creating a coordinator, you should also create the sub-agents it references."
- The coordinator example mentions `Agent(researcher, implementer, test-runner)` but does not include or link to the actual definitions of these sub-agents. It assumes they already exist.
- I had to infer from the examples directory that the sub-agents should be standalone `.md` files that the coordinator references by name.
- The skill does not discuss file organization for multi-agent setups (e.g., should sub-agents be in a sub-directory? in the same directory as the coordinator?).

**Gap:** A section on "Creating Multi-Agent Systems" that describes how to create a coordinator alongside its required sub-agents would be very helpful.

## Ambiguity About Agent(type) Syntax for 4 Agent Types

The `Agent(type)` syntax is documented in two places:

1. **frontmatter-reference.md** shows `Agent(type1, type2)` as the pattern.
2. **coordinator example** shows `Agent(researcher, implementer, test-runner)` with 3 types.

Extending to 4 types (`Agent(researcher, frontend-reviewer, backend-reviewer, test-runner)`) was a straightforward extrapolation -- the comma-separated list pattern is clear enough. **No significant ambiguity here.** The syntax naturally extends to any number of types.

One minor question: the skill does not specify if there is a maximum number of agent types that can be listed in `Agent()`. For this scenario with 4 types, it was not a concern, but for very large agent teams it might matter.

## --agent vs Subagent Distinction

The skill explains this distinction in several places:

1. **SKILL.md line 10 (coordinator design note):** "此类 agent 通常作为 `--agent` 主线程运行，而非 subagent（subagent 不能生成子 agent）"
2. **examples/coordinator.md line 80:** "Subagent 不能生成子 agent -- `Agent(type)` 限制只在主线程 agent（`--agent`）中有效"
3. **frontmatter-reference.md Section 3:** "Agent(type) -> 限制可调度的 agent 类型（仅 `--agent` 主线程有效）"

**Assessment:** The distinction is adequately explained and consistently reinforced across multiple locations. The critical constraint (subagents cannot spawn child agents) is clearly stated. The user's requirement to "作为主线程运行" mapped directly to the `--agent` usage pattern shown in the coordinator example.

However, one thing could be clearer: **the practical deployment setup.** When a coordinator runs as `--agent`, where do the sub-agents it references need to be stored? Must they be in `.claude/agents/` for the coordinator to find them by name? This is implied but never stated explicitly.

## Gap Analysis: What Was Missing

1. **Multi-agent creation workflow.** No guidance on creating a coordinator and its sub-agents as a set. The skill treats each agent type independently. For coordinator scenarios, a holistic workflow section would help.

2. **Sub-agent file organization.** No guidance on where sub-agents should be placed relative to the coordinator, or whether they can be organized in subdirectories within `.claude/agents/`.

3. **Customizing existing templates for domain-specific needs.** The code-reviewer example is generic. When creating a frontend-specific reviewer vs. a backend-specific reviewer, I had to design the specialized review checklists myself. A note in the skill about "creating variants of the same type" would be useful.

4. **Parallel execution guidance.** The coordinator example mentions "并行调度" but does not explain the mechanics. How does Claude Code actually execute two sub-agents in parallel? Is it automatic when the coordinator calls them in the same turn? This operational detail is missing.

5. **Error handling in coordination.** What happens if one sub-agent fails? Should the coordinator retry? Skip? The example does not address failure modes in multi-agent workflows.

6. **Token budget awareness.** The coordinator example mentions "多 agent 协调会消耗更多 token" but provides no practical guidance on estimating or controlling token usage across 4+ sub-agents.

7. **No `frontend-reviewer` or `backend-reviewer` example.** These are variants of code-reviewer but specialized by stack. The skill's example set could include at least one domain-specialized reviewer variant.

8. **InitialPrompt usage for coordinators.** The frontmatter-reference mentions `initialPrompt` for `--agent` scenarios, but the coordinator example does not use it. For a code review coordinator, an `initialPrompt` like "分析当前分支的所有改动并执行完整的代码审查流程" could be very useful. This connection is not made.

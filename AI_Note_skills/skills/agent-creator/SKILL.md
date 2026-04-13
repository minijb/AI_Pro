---
name: agent-creator
description: >
  创建 Claude Code 自定义 subagent（子代理）。当用户想要创建新 agent、定义子代理、
  设置专用 AI 助手、配置 agent 工具/权限/hooks，或构建多 agent 工作流时使用此 skill。
  触发场景："创建一个 agent"、"新建子代理"、"定义 agent"、"做一个代码审查 agent"、
  "create an agent"、"new subagent"、"define agent"、"agent for X"、
  "set up a code reviewer"、"make a debugging agent"、"build an assistant"、
  "make a bot"、"agent template"、"搭建助手"、"配置权限"、agent 配置、agent YAML。
  Use proactively when user discusses creating specialized AI helpers or automated workflows.
---

# Agent Creator

帮助用户创建 Claude Code 自定义 subagent 的 skill。

## 什么是 Subagent

Subagent 是运行在独立上下文中的专用 AI 助手。每个 subagent 拥有独立的系统提示、工具访问权限和权限模式。当 Claude 遇到匹配 subagent 描述的任务时，会自动委派给该 subagent。

**Subagent 的核心价值：**
- **保留上下文** — 将探索/实现保持在主对话之外，避免主上下文膨胀
- **强制约束** — 限制可用工具，确保安全（如只读 agent 不能写文件）
- **专业化行为** — 为特定领域提供专注的系统提示
- **控制成本** — 将简单任务路由到更快更便宜的模型（如 Haiku）
- **跨项目复用** — 用户级 agent 在所有项目中可用

**Subagent vs Agent Teams：** Subagent 在单个会话内运行，结果汇报回主上下文；Agent Teams 是独立的 Claude Code 会话，彼此之间可通信。

## 文件格式

Subagent 是 **Markdown 文件 + YAML frontmatter**：

```markdown
---
name: my-agent
description: 这个 agent 做什么，何时使用
tools: Read, Grep, Glob
model: sonnet
---

这里是系统提示。指导 agent 的行为方式。
```

- Frontmatter 定义元数据和配置
- Markdown 正文成为 agent 的系统提示
- 只有 `name` 和 `description` 是必需字段

## 存储位置

| 位置 | 作用域 | 优先级 | 说明 |
|------|--------|--------|------|
| 托管设置 | 组织级 | 1（最高） | 管理员通过 managed settings 部署 |
| `--agents` CLI 参数 | 当前会话 | 2 | 启动时传入 JSON，仅存在于该会话 |
| `.claude/agents/` | 当前项目 | 3 | 可提交到版本控制，团队共享 |
| `~/.claude/agents/` | 所有项目 | 4 | 个人级，跨项目可用 |
| 插件 `agents/` 目录 | 插件启用处 | 5（最低） | 随插件安装 |

**推荐：** 项目级 agent 放 `.claude/agents/`，个人通用 agent 放 `~/.claude/agents/`。

## 创建流程

### 第 1 步：需求采集

与用户确认以下问题：

1. **功能定位** — agent 要解决什么问题？（代码审查、调试、测试、研究、数据查询等）
2. **工具权限** — 需要读写文件吗？需要运行命令吗？是否要限制为只读？
3. **模型选择** — 需要强推理（opus）？均衡性能（sonnet/inherit）？还是速度优先（haiku）？
4. **存储位置** — 项目级还是用户级？
5. **触发方式** — 自动委派还是仅手动调用？

### 第 2 步：选择 Agent 类型

根据需求匹配最接近的模板类型，然后按需调整。

### 第 3 步：生成 Agent 文件

基于模板和用户需求生成完整的 agent Markdown 文件。

### 第 4 步：验证与部署

1. 将文件保存到对应位置（`.claude/agents/` 或 `~/.claude/agents/`）
2. 提醒用户重启会话或运行 `/agents` 加载
3. 建议用户测试：`使用 <agent-name> agent 来 <具体任务>`

## Agent 类型速查表

根据功能需求选择合适的类型。每种类型的完整示例见 `examples/` 目录。

| 类型 | 示例文件 | 工具权限 | 推荐模型 | 典型场景 |
|------|---------|---------|---------|---------|
| 只读研究型 | [examples/researcher.md](examples/researcher.md) | Read, Grep, Glob | haiku | 代码探索、架构分析、文档搜索 |
| 代码审查型 | [examples/code-reviewer.md](examples/code-reviewer.md) | Read, Grep, Glob, Bash | inherit | 代码质量检查、安全审计、PR 审查 |
| 调试修复型 | [examples/debugger.md](examples/debugger.md) | Read, Edit, Bash, Grep, Glob | inherit | 错误诊断、bug 修复、测试失败分析 |
| 测试执行型 | [examples/test-runner.md](examples/test-runner.md) | Bash, Read, Glob, Grep | sonnet | 运行测试、验证变更、报告结果 |
| 数据查询型 | [examples/db-reader.md](examples/db-reader.md) | Bash（含 hooks 验证） | sonnet | 只读数据库查询、数据分析 |
| 协调编排型 | [examples/coordinator.md](examples/coordinator.md) | Agent(type), Read, Bash | opus | 多 agent 协调、复杂任务分发 |
| 监控运维型 | [examples/api-monitor.md](examples/api-monitor.md) | Bash, Read, Grep, Glob | sonnet | API 监控、健康检查、状态报告 |
| 内容生成型 | [examples/doc-generator.md](examples/doc-generator.md) | Read, Write, Grep, Glob, Bash | sonnet | 文档生成、报告输出、代码分析 |

> **选择指南：**
> - 只需要搜索和阅读 → **只读研究型**
> - 需要审查但不修改代码 → **代码审查型**
> - 需要定位并修复问题 → **调试修复型**
> - 需要运行测试套件 → **测试执行型**
> - 需要查询数据库 → **数据查询型**
> - 需要协调多个 agent → **协调编排型**
> - 需要监控服务或检查健康状态 → **监控运维型**
> - 需要生成文档或报告 → **内容生成型**
> - 以上都不匹配 → 从 **代码审查型** 开始调整

读取对应示例文件，根据用户的具体需求进行定制修改。

## Frontmatter 核心字段

| 字段 | 必需 | 说明 |
|------|------|------|
| `name` | 是 | 唯一标识，小写字母 + 连字符 |
| `description` | 是 | 告诉 Claude 何时委派任务到此 agent |
| `tools` | 否 | 允许使用的工具（允许列表），省略则继承全部 |
| `disallowedTools` | 否 | 禁止使用的工具（拒绝列表） |
| `model` | 否 | 模型：`haiku`、`sonnet`、`opus`、`inherit`（默认） |
| `permissionMode` | 否 | 权限模式：`default`、`acceptEdits`、`auto`、`plan` 等 |
| `maxTurns` | 否 | 最大推理轮次 |
| `hooks` | 否 | 生命周期钩子，仅在此 agent 活跃时运行 |

完整字段参考见 [references/frontmatter-reference.md](references/frontmatter-reference.md)。

## 高级功能

以下功能按需使用，详见 [references/frontmatter-reference.md](references/frontmatter-reference.md) 中的完整说明。

### 持久化记忆（memory）

让 agent 跨会话积累知识：

```yaml
memory: project    # 项目级，可提交版本控制
# memory: user     # 用户级，跨项目
# memory: local    # 项目级但不提交版本控制
```

启用后 agent 获得独立的记忆目录，可在其中读写学习笔记。在系统提示中加入记忆管理指令效果更好。

### Hooks（生命周期钩子）

在 agent 执行工具前/后运行验证脚本：

```yaml
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate.sh"
```

适用场景：SQL 只读验证、命令白名单、自动 lint。参见 [examples/db-reader.md](examples/db-reader.md) 中的完整示例。

**Hook 执行机制：**
- 脚本通过 **stdin** 接收 JSON，格式为 `{"tool_input": {...}}`（如 Bash 工具：`{"tool_input": {"command": "..."}}`）
- **退出码**：`0` = 放行，`2` = 拦截（stderr 消息返回给 agent），其他 = hook 自身错误
- **路径规则**：项目级 agent 用相对路径 `./scripts/...`；用户级 agent（`~/.claude/agents/`）必须用绝对路径，因为工作目录是当前项目而非 agent 所在目录

完整的 stdin JSON schema 和退出码说明见 [references/frontmatter-reference.md](references/frontmatter-reference.md)。

### MCP Server 集成

为 agent 提供专属的外部工具访问：

```yaml
mcpServers:
  - playwright:
      type: stdio
      command: npx
      args: ["-y", "@playwright/mcp@latest"]
  - github    # 引用已配置的 MCP server
```

### 预加载 Skills

将 skill 内容注入 agent 上下文：

```yaml
skills:
  - api-conventions
  - error-handling-patterns
```

### 隔离执行（worktree）

在独立的 git worktree 中运行 agent：

```yaml
isolation: worktree
```

适用于可能产生破坏性变更的任务。

### 后台运行

始终作为后台任务运行：

```yaml
background: true
```

## 多 Agent 系统创建

创建 coordinator + 配套 sub-agent 时，遵循以下流程。

### 文件组织

所有 agent 文件放在 `.claude/agents/` 下，子目录中的 agent 同样会被自动发现：

| 模式 | 结构 | 适用场景 |
|------|------|---------|
| 扁平结构 | `agents/coordinator.md`、`agents/worker.md` | 少量 agent（2-3 个） |
| 子目录分组 | `agents/review-team/coordinator.md`、`agents/review-team/checker.md` | 相关 agent 成组管理 |

### 创建顺序

1. **先创建叶子 agent**（researcher、reviewer 等）— 不依赖其他 agent
2. **再创建 coordinator** — 在 `tools` 中用 `Agent(name1, name2, ...)` 引用叶子 agent
3. **验证名称匹配** — `Agent(...)` 中的名称必须与叶子 agent 的 `name` 字段完全一致

### 注意事项

- coordinator 通常作为 `--agent` 主线程运行（subagent 不能生成子 agent）
- 在 coordinator 系统提示中加入失败处理指令：当子 agent 返回错误时如何回退或跳过
- 建议设置 `maxTurns` 防止无限循环
- 可用 `initialPrompt` 让 coordinator 启动时自动开始工作

完整的多 agent 设计指南见 [references/multi-agent-guide.md](references/multi-agent-guide.md)。

## 编写 Description 的最佳实践

`description` 是 Claude 决定何时委派任务的唯一依据。写好 description 至关重要：

1. **明确说明用途** — 不要只写"代码审查"，要写"专业代码审查。在编写或修改代码后主动审查代码质量、安全性和可维护性"
2. **包含触发短语** — "Use when..."、"Trigger when..."、"Use proactively after..."
3. **适度积极** — 如果希望 agent 被主动使用，加 "Use proactively" 等描述
4. **覆盖边界情况** — 用户可能用不同方式描述同一需求
5. **使用主动触发语** — 明确写 "Use proactively when..."、"Use proactively after..." 鼓励自动委派
6. **多语言覆盖** — 同时包含中英文触发短语，如 "创建助手" + "build an assistant"

## 系统提示编写指南

系统提示（Markdown 正文）决定 agent 的行为方式：

1. **定义角色** — 开头明确 agent 的专业身份
2. **列出工作流** — 用编号步骤描述 agent 被调用时应该做什么
3. **定义输出格式** — 按优先级/类别组织输出
4. **设定边界** — 明确 agent 能做什么、不能做什么
5. **保持聚焦** — 每个 agent 专注做好一件事

## 参考文件

- `examples/` — 各类型 agent 的完整可用示例，包含设计说明
- `references/frontmatter-reference.md` — YAML frontmatter 全部字段的详细参考
- `references/multi-agent-guide.md` — 多 Agent 系统设计指南（架构模式、文件组织、错误处理）
- `references/troubleshooting.md` — 常见问题排查（触发失败、命名冲突、Hook 调试）
- `references/domain-specialization.md` — Agent 领域特化指南（从通用模板派生专用 agent）
- `references/eval-schemas.md` — 评估系统 JSON Schema 参考（evals、grading、benchmark 格式）

## 评估与测试

本 skill 包含评估基础设施，用于验证生成的 agent 质量：

- `agents/grader.md` — 评分 agent，根据预期标准评估生成的 agent 文件
- `agents/comparator.md` — 盲比较器，不知道哪个版本产生哪个输出进行质量对比
- `agents/analyzer.md` — 分析器，解释为什么胜者更好并生成改进建议
- `scripts/validate_agent.py` — 自动化验证 agent frontmatter 和系统提示结构
- `scripts/aggregate_benchmark.py` — 汇总多轮测试结果为基准统计

### 快速验证

```bash
python -m scripts.validate_agent path/to/agent.md
```

### 汇总基准测试

```bash
python -m scripts.aggregate_benchmark workspace/iteration-1/ --skill-name agent-creator
```

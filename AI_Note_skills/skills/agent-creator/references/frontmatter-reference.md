# Agent Frontmatter 完整字段参考

本文档是 Claude Code subagent YAML frontmatter 的完整字段参考。

---

## 目录

1. [基础字段](#1-基础字段)
2. [模型与性能](#2-模型与性能)
3. [工具控制](#3-工具控制)
4. [权限与安全](#4-权限与安全)
5. [生命周期钩子](#5-生命周期钩子hooks)
6. [持久化记忆](#6-持久化记忆)
7. [MCP Server](#7-mcp-server)
8. [Skills 预加载](#8-skills-预加载)
9. [执行模式](#9-执行模式)
10. [显示与标识](#10-显示与标识)
11. [会话级配置](#11-会话级配置)
12. [字段组合模式](#12-字段组合模式)

---

## 1. 基础字段

| 字段 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| `name` | string | 是 | — | 唯一标识符，小写字母和连字符，最长 64 字符 |
| `description` | string | 是 | — | 告诉 Claude 何时委派任务到此 agent。这是触发机制的核心 |

### description 编写要点

- 明确说明用途和触发场景
- 使用 "Use proactively" 鼓励主动触发
- 包含用户可能使用的不同表述方式
- 250 字符内的内容最重要（截断限制）

---

## 2. 模型与性能

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `model` | string | `inherit` | 使用的模型 |
| `effort` | string | 继承会话 | 努力级别 |
| `maxTurns` | integer | 无限制 | 最大推理轮次 |

### model 可选值

| 值 | 说明 |
|----|------|
| `haiku` | 快速、低成本，适合搜索和简单分析 |
| `sonnet` | 均衡性能，适合大多数任务 |
| `opus` | 最强推理，适合复杂任务 |
| `inherit` | 继承主会话模型（默认） |
| 完整 ID | 如 `claude-opus-4-6`、`claude-sonnet-4-6` |

### effort 可选值

| 值 | 说明 |
|----|------|
| `low` | 快速响应，适合简单任务 |
| `medium` | 标准思考深度 |
| `high` | 深入推理 |
| `max` | 最大思考深度（仅 Opus） |

### model 解析优先级

1. `CLAUDE_CODE_SUBAGENT_MODEL` 环境变量
2. 调用时传入的 model 参数
3. Agent 定义中的 `model` 字段
4. 主会话的模型

---

## 3. 工具控制

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `tools` | string (逗号分隔) | 继承全部 | 允许使用的工具（允许列表） |
| `disallowedTools` | string (逗号分隔) | 无 | 禁止使用的工具（拒绝列表） |

### 可用工具列表

| 工具 | 说明 |
|------|------|
| `Read` | 读取文件 |
| `Write` | 写入文件 |
| `Edit` | 编辑文件 |
| `Bash` | 执行 shell 命令 |
| `Glob` | 文件模式匹配搜索 |
| `Grep` | 内容搜索 |
| `Agent` | 调度子 agent |
| `Agent(type1, type2)` | 限制可调度的 agent 类型 |
| `NotebookEdit` | 编辑 Jupyter notebook |
| `WebFetch` | 获取网页内容 |
| `WebSearch` | 搜索网页 |
| MCP 工具名 | 通过 MCP server 提供的工具 |

### 工具控制规则

- 省略 `tools` → 继承主会话的所有工具（包括 MCP 工具）
- 设置 `tools` → 仅允许列出的工具
- 设置 `disallowedTools` → 从继承/指定的工具中移除
- 两者都设置 → 先应用 `disallowedTools`，再解析 `tools`
- `Agent(type)` → 限制可调度的 agent 类型（仅 `--agent` 主线程有效）

---

## 4. 权限与安全

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `permissionMode` | string | `default` | 权限模式 |

### 权限模式选项

| 模式 | 行为 |
|------|------|
| `default` | 标准权限检查，弹出确认提示 |
| `acceptEdits` | 自动接受工作目录内的文件编辑和常见命令 |
| `auto` | 自动模式：后台分类器审查命令和受保护目录写入 |
| `dontAsk` | 自动拒绝权限提示（已显式允许的工具仍可用） |
| `bypassPermissions` | 跳过权限提示（谨慎使用） |
| `plan` | 计划模式（只读探索） |

### 权限继承规则

- 父级使用 `bypassPermissions` → 子级也使用，不可覆盖
- 父级使用 `auto` → 子级继承 auto 模式，frontmatter 中的设置被忽略
- 插件 agent → `hooks`、`mcpServers`、`permissionMode` 字段被忽略（安全限制）

---

## 5. 生命周期钩子（hooks）

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `hooks` | object | 无 | 仅在此 agent 活跃时运行的钩子 |

### 支持的事件

| 事件 | Matcher 输入 | 触发时机 |
|------|-------------|---------|
| `PreToolUse` | 工具名 | agent 使用工具之前 |
| `PostToolUse` | 工具名 | agent 使用工具之后 |
| `Stop` | (无) | agent 完成时（自动转为 SubagentStop） |

### 示例

```yaml
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-command.sh"
  PostToolUse:
    - matcher: "Edit|Write"
      hooks:
        - type: command
          command: "./scripts/run-linter.sh"
```

### Hook 执行细节

#### stdin JSON 格式

Hook 脚本通过 stdin 接收 JSON 对象，结构取决于触发的工具：

| 工具 | stdin JSON 结构 |
|------|----------------|
| `Bash` | `{"tool_input": {"command": "要执行的命令"}}` |
| `Read` | `{"tool_input": {"file_path": "/path/to/file"}}` |
| `Edit` | `{"tool_input": {"file_path": "...", "old_string": "...", "new_string": "..."}}` |
| `Write` | `{"tool_input": {"file_path": "...", "content": "..."}}` |
| `Grep` | `{"tool_input": {"pattern": "...", "path": "..."}}` |

对于 `PostToolUse` 事件，JSON 中还包含 `"tool_result"` 字段。

#### 退出码

| 退出码 | 含义 | 行为 |
|--------|------|------|
| `0` | 通过 | 工具正常执行（PreToolUse）或不做额外处理（PostToolUse） |
| `2` | 拦截 | 阻止工具执行，stderr 内容作为消息返回给 agent |
| 其他 | 错误 | 视为 hook 自身出错，不影响工具执行但会记录警告 |

#### 路径规则

| Agent 存储位置 | Hook 脚本路径 | 说明 |
|---------------|-------------|------|
| `.claude/agents/`（项目级） | `./scripts/validate.sh` | 相对于项目根目录解析 |
| `~/.claude/agents/`（用户级） | 绝对路径，如 `$HOME/.claude/scripts/validate.sh` | 相对路径无法正确解析 |

> **注意：** 用户级 agent 的 hook 脚本不能使用 `./` 开头的相对路径，因为执行时的工作目录是当前项目目录，不是 `~/.claude/agents/`。推荐将验证脚本放在 `~/.claude/scripts/` 并使用绝对路径引用。

### 项目级 agent 事件（settings.json）

在 `settings.json` 中可监听 agent 生命周期：

| 事件 | Matcher 输入 | 触发时机 |
|------|-------------|---------|
| `SubagentStart` | Agent 类型名 | agent 开始执行 |
| `SubagentStop` | Agent 类型名 | agent 执行完成 |

---

## 6. 持久化记忆

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `memory` | string | 无 | 持久化记忆的作用域 |

### 作用域选项

| 值 | 存储位置 | 适用场景 |
|----|---------|---------|
| `user` | `~/.claude/agent-memory/<name>/` | 跨项目通用知识 |
| `project` | `.claude/agent-memory/<name>/` | 项目级，可提交版本控制（推荐） |
| `local` | `.claude/agent-memory-local/<name>/` | 项目级但不提交版本控制 |

### 启用后的行为

- Agent 系统提示自动包含记忆目录的读写指令
- 自动加载 `MEMORY.md` 的前 200 行或 25KB
- 自动启用 Read、Write、Edit 工具

### 记忆与系统提示的交互

启用 `memory` 后，Claude Code 会自动在 agent 的系统提示**末尾**追加记忆管理指令（包括记忆目录路径和基本读写方法）。这些自动注入的指令与你手写的系统提示共存，不会冲突。

**最佳实践：**
- 在手写系统提示中加入**领域特定的**记忆指令（如"记录发现的代码模式和常见问题"），补充自动注入的通用指令
- 不需要在手写提示中重复"读取/写入记忆目录"等通用操作——这些已被自动注入
- 记忆目录初始为空，agent 首次运行并主动写入后才会创建文件

### 记忆目录结构

```
<memory-scope-dir>/<agent-name>/
├── MEMORY.md          # 主记忆文件（自动预加载前 200 行或 25KB）
└── <其他>.md          # agent 可自由创建的补充文件
```

agent 可以在记忆目录中创建多个文件来组织不同类型的知识，但 `MEMORY.md` 是唯一自动预加载的文件。建议用 `MEMORY.md` 作为索引，引用其他补充文件。

---

## 7. MCP Server

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `mcpServers` | list | 无 | 此 agent 可用的 MCP server |

### 配置方式

```yaml
mcpServers:
  # 内联定义：仅此 agent 可用
  - playwright:
      type: stdio
      command: npx
      args: ["-y", "@playwright/mcp@latest"]
  # 引用已有配置：共享父会话的连接
  - github
```

- 内联 server 在 agent 启动时连接，结束时断开
- 字符串引用共享父会话的连接
- 仅在此 agent 定义的 server 不会出现在主会话上下文中

---

## 8. Skills 预加载

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `skills` | list | 无 | 启动时注入的 skill 列表 |

```yaml
skills:
  - api-conventions
  - error-handling-patterns
```

- 完整的 skill 内容注入 agent 上下文（不只是可调用）
- Agent 不会继承父会话的 skills，必须显式列出

---

## 9. 执行模式

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `background` | boolean | `false` | 始终作为后台任务运行 |
| `isolation` | string | 无 | 设为 `worktree` 在隔离的 git worktree 中运行 |

### 前台 vs 后台

- **前台**（默认）：阻塞主会话直到完成，权限提示和问题会传递给用户
- **后台**：并发运行，启动前预先请求所需权限，运行期间自动拒绝未预批准的操作

### worktree 隔离

```yaml
isolation: worktree
```

Agent 在独立的 git worktree 中工作，不影响主工作区。如果 agent 没有产生变更，worktree 自动清理。

---

## 10. 显示与标识

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `color` | string | 无 | 任务列表和日志中的显示颜色 |

### 可选颜色

`red`、`blue`、`green`、`yellow`、`purple`、`orange`、`pink`、`cyan`

---

## 11. 会话级配置

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `initialPrompt` | string | 无 | 作为 `--agent` 运行时自动提交的首个用户消息 |

`initialPrompt` 仅在 agent 作为主会话（`--agent` 或 settings 中的 `agent`）运行时生效。支持处理 `/命令` 和 skills。

### initialPrompt 与 coordinator 模式

`initialPrompt` 与协调器 agent 天然契合。设置后，coordinator 作为 `--agent` 启动时会自动开始执行预设任务，无需用户手动输入第一条指令：

```yaml
name: daily-check
description: 每日代码状态检查协调器
tools: Agent(test-runner, researcher), Read, Bash
model: opus
initialPrompt: >
  运行所有测试，研究失败原因，生成今日状态报告。
```

---

## 12. 字段组合模式

### 只读研究 Agent

```yaml
tools: Read, Grep, Glob
model: haiku
```

### 安全审查 Agent

```yaml
tools: Read, Grep, Glob, Bash
permissionMode: plan
```

### 自动化修复 Agent

```yaml
tools: Read, Edit, Write, Bash, Grep, Glob
permissionMode: acceptEdits
```

### 数据库只读 Agent（带验证）

```yaml
tools: Bash
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-readonly.sh"
```

### 浏览器测试 Agent（带 MCP）

```yaml
tools: Bash, Read, Write
mcpServers:
  - playwright:
      type: stdio
      command: npx
      args: ["-y", "@playwright/mcp@latest"]
```

### 多 Agent 协调器（主线程）

```yaml
tools: Agent(worker, researcher), Read, Bash
model: opus
```

### 跨会话学习 Agent

```yaml
tools: Read, Grep, Glob, Bash
memory: project
model: inherit
```

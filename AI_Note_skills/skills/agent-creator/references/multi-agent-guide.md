# 多 Agent 系统设计指南

本文档提供创建和管理多 agent 协作系统的完整指南。

## 何时需要多 Agent 系统

- 单个 agent 的系统提示超过 200 行，职责过于复杂
- 任务需要不同的工具权限组合（如只读研究 + 读写修改）
- 任务需要不同模型（如 haiku 做快速搜索 + opus 做决策）
- 需要并行处理多个独立子任务以提高效率

如果以上都不满足，单个 agent 通常更简单高效。

## 架构模式

### 星型模式（Coordinator + Workers）

最常用的模式。一个 coordinator 持有 `Agent(type1, type2, ...)` 调度权，负责任务分解和结果整合。

```
           ┌─ researcher
coordinator┼─ implementer
           └─ test-runner
```

适用于：大型重构、全栈开发、复杂 review 流程。

### 管道模式（Sequential Handoff）

任务按阶段流转，每个阶段由不同 agent 处理。通常由 coordinator 按顺序调度。

```
researcher → implementer → test-runner
```

适用于：研究→实现→验证流水线。

### 钻石模式（Fork-Join）

先汇聚再分散。适合需要并行审查后汇总的场景。

```
         ┌─ frontend-reviewer ─┐
researcher                      coordinator（整合）
         └─ backend-reviewer  ─┘
```

适用于：全栈代码审查、多维度分析。

## 文件组织详解

### 扁平结构

```
.claude/agents/
├── coordinator.md
├── researcher.md
├── implementer.md
└── test-runner.md
```

优点：简单直观。适合 agent 总数 ≤ 5 个。

### 子目录分组

```
.claude/agents/
├── review-team/
│   ├── review-coordinator.md
│   ├── frontend-reviewer.md
│   └── backend-reviewer.md
├── researcher.md
└── test-runner.md
```

优点：逻辑分组清晰。子目录中的 agent 同样会被自动发现。

### 命名约定

- **前缀分组**：`review-coordinator`、`review-frontend`、`review-backend`
- **职能命名**：用角色命名而非技术命名（`researcher` 优于 `grep-agent`）
- **避免冲突**：不同目录下的同名 agent 按优先级覆盖（参见 SKILL.md 存储位置表）

## 错误处理策略

### 在 coordinator 系统提示中加入失败处理

```markdown
## 错误处理

- 如果子 agent 返回错误或超时，记录错误信息并继续处理其他子任务
- 在最终报告中标注失败的子任务及原因
- 对于关键子任务（如测试），失败时停止后续步骤并报告
- 对于非关键子任务（如代码风格检查），失败时跳过并在报告中标注
```

### 防止无限循环

- 设置 `maxTurns` 限制最大推理轮次
- 在系统提示中明确"如果 N 次重试后仍然失败，报告错误并停止"

## initialPrompt 与 Coordinator

`initialPrompt` 让 coordinator 在作为 `--agent` 或项目默认 agent 启动时自动开始工作：

```yaml
name: daily-review
description: 每日自动代码审查协调器
tools: Agent(researcher, reviewer, test-runner), Read, Bash
model: opus
initialPrompt: >
  检查今天的所有提交，对每个提交执行代码审查和测试验证，生成每日审查报告。
```

启动方式：
```bash
claude --agent daily-review
```

## 从单 Agent 到多 Agent 的演进

不要一开始就设计多 agent 系统。推荐演进路径：

1. **起步**：单个通用 agent 处理所有任务
2. **识别瓶颈**：当系统提示过长、或需要不同权限/模型时
3. **拆分**：将独立职责提取为独立 agent
4. **协调**：如果拆分后需要自动化工作流，创建 coordinator

每次拆分都应有明确的理由（安全隔离、成本控制、并行效率），而非为拆分而拆分。

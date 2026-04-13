# Agent 常见问题排查

## Agent 不被自动触发

**症状：** 用户描述了与 agent description 匹配的任务，但 Claude 没有自动委派。

**排查步骤：**

1. **确认 agent 已加载** — 运行 `/agents` 查看当前可用的 agent 列表
2. **检查文件位置** — 确认文件在 `.claude/agents/` 或 `~/.claude/agents/` 下
3. **检查文件格式** — 确认是 `.md` 文件，且 YAML frontmatter 格式正确（`---` 开头和结尾）
4. **优化 description** — 确保包含用户可能使用的表述方式，添加 "Use proactively when..." 增加触发概率
5. **手动测试** — 使用 "使用 `<name>` agent 来 `<任务>`" 手动触发，验证 agent 本身能否工作

**常见原因：**
- description 过于抽象，缺少具体的触发场景描述
- 任务过于简单，Claude 认为不需要委派给专用 agent
- 新添加的 agent 文件需要重启会话才能被发现

## 命名冲突

**症状：** 多个同名 agent 存在，行为不符合预期。

**解决：**
- 同名 agent 按优先级覆盖（从高到低）：托管设置 > CLI 参数 > 项目级 > 用户级 > 插件
- 使用 `/agents` 查看实际加载的 agent 列表，确认加载的是哪个版本
- 推荐使用不同名称避免冲突，如添加项目前缀：`myapp-reviewer` vs `reviewer`

## Hook 脚本不执行

**排查步骤：**

1. **检查执行权限** — `chmod +x ./scripts/validate.sh`
2. **检查路径** — 项目级 agent 用相对路径 `./scripts/...`，用户级 agent 必须用绝对路径
3. **手动测试脚本** — 用模拟输入测试：
   ```bash
   echo '{"tool_input":{"command":"test command"}}' | ./scripts/validate.sh
   echo $?  # 应输出 0（放行）或 2（拦截）
   ```
4. **检查 shebang 行** — 脚本首行应为 `#!/bin/bash` 或 `#!/usr/bin/env bash`
5. **检查 jq 依赖** — 如果脚本使用 jq 解析 JSON，确认 jq 已安装

## 记忆不生效

**排查步骤：**

1. **确认 frontmatter** — 检查是否设置了 `memory: project`（或 `user`/`local`）
2. **首次运行** — 记忆目录初始为空，agent 需要在系统提示引导下主动写入才会创建文件
3. **检查权限** — 确认记忆目录路径有写入权限
4. **加入记忆指令** — 在系统提示中明确告诉 agent 记录什么内容（如"将发现的代码模式记录到记忆目录"）

## Agent 执行超时或无响应

**可能原因：**
- agent 进入循环（设置 `maxTurns` 限制）
- Bash 命令阻塞等待输入（确保命令不需要交互式输入）
- 模型选择不当（简单任务使用 opus 浪费时间，复杂任务使用 haiku 能力不足）

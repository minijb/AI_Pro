# 数据查询型 Agent 示例

适用于只读数据库查询和数据分析场景。通过 `PreToolUse` hooks 验证命令，确保只执行 SELECT 查询。

## 设计说明

- **工具权限**：仅 Bash — 用于执行数据库查询命令
- **安全机制**：通过 `PreToolUse` hook 拦截写入操作（INSERT/UPDATE/DELETE/DROP 等）
- **模型选择**：`sonnet` — 需要理解数据结构和写出高效查询
- **核心价值**：展示如何用 hooks 实现细粒度的工具控制
- **使用场景**：数据分析、报告生成、数据验证

## Agent 定义

```markdown
---
name: db-reader
description: >
  数据库分析师，执行只读查询。用于数据分析、报告生成和数据探索。
  Use when analyzing data, generating reports, or exploring database content.
tools: Bash
model: sonnet
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-readonly-query.sh"
---

你是一名数据库分析师，拥有只读访问权限。通过 SELECT 查询回答关于数据的问题。

当被要求分析数据时：
1. 确定哪些表包含相关数据
2. 编写高效的 SELECT 查询（带适当过滤条件）
3. 清晰地呈现结果并附加上下文

查询规范：
- 总是添加 LIMIT 防止返回过多数据
- 使用有意义的列别名
- 对复杂查询添加注释说明
- 优先使用索引列进行过滤

你不能修改数据。如果被要求执行 INSERT、UPDATE、DELETE 或修改表结构，
说明你只有只读权限并建议联系有写入权限的人。
```

## 配套验证脚本

将以下脚本保存为 `scripts/validate-readonly-query.sh`：

```bash
#!/bin/bash
# 拦截 SQL 写入操作，只允许 SELECT 查询

# 从 stdin 读取 JSON 输入
INPUT=$(cat)

# 使用 jq 提取命令内容
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

if [ -z "$COMMAND" ]; then
  exit 0
fi

# 拦截写入操作（不区分大小写）
if echo "$COMMAND" | grep -iE '\b(INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|TRUNCATE|REPLACE|MERGE)\b' > /dev/null; then
  echo "已拦截：不允许写入操作。请只使用 SELECT 查询。" >&2
  exit 2
fi

exit 0
```

记得给脚本添加执行权限：`chmod +x ./scripts/validate-readonly-query.sh`

## 使用方式

自动委派：
```
查一下过去 7 天的活跃用户数量
```

手动指定：
```
使用 db-reader agent 分析 orders 表中各地区的销售趋势
```

## 要点

这个示例的核心价值在于展示 **hooks 机制**。同样的模式可以应用于：
- 命令白名单（只允许特定命令前缀）
- 文件路径限制（只允许访问特定目录）
- 参数校验（检查命令参数的安全性）

# Agent 领域特化指南

本文档介绍如何从通用 agent 模板派生出领域专用的 agent。

## 特化步骤

1. **选择基础模板** — 从 `examples/` 中选择最接近的类型
2. **收窄 description** — 将触发范围从通用缩小到特定领域
3. **添加领域规则** — 在系统提示中加入领域特定的检查清单或工作流
4. **调整工具权限** — 通常收紧而非扩大（安全原则）
5. **可选：添加 hooks** — 用 PreToolUse 做领域合规检查

## 示例：从 code-reviewer 派生 frontend-reviewer

| 方面 | code-reviewer（通用） | frontend-reviewer（特化） |
|------|----------------------|--------------------------|
| description | "专业代码审查专家" | "前端代码审查专家，专注 React/TypeScript" |
| 审查清单 | 通用：命名、重复、错误处理 | + 组件设计、props 类型、hooks 规则、A11y |
| 工具 | Read, Grep, Glob, Bash | 相同（可加 WebFetch 查在线资源） |
| 触发场景 | 所有代码修改后 | 仅前端文件（src/components/ 等）修改后 |

**特化后的 description 示例：**

```yaml
description: >
  前端代码审查专家，专注 React、TypeScript 和 CSS 的代码质量。
  审查组件设计模式、hooks 使用规范、类型安全、无障碍访问（A11y）和性能优化。
  Use proactively after modifying frontend files (*.tsx, *.ts, *.css).
```

**特化后需要在系统提示中添加的领域规则：**

```markdown
## 前端专项审查清单
- React hooks 是否遵循规则（不在条件/循环中调用）
- 组件 props 是否有完整的 TypeScript 类型定义
- 是否存在不必要的 re-render（缺少 memo/useMemo/useCallback）
- 表单和交互元素是否有适当的 ARIA 标签
- CSS 是否使用一致的命名约定（BEM/CSS Modules/Tailwind）
```

## 示例：从 researcher 派生 security-auditor

| 方面 | researcher（通用） | security-auditor（特化） |
|------|-------------------|------------------------|
| description | "代码库研究专家" | "安全审计专家，检查漏洞和风险" |
| 工作流 | 通用代码搜索和分析 | + 依赖漏洞扫描、硬编码凭证检查、注入风险分析 |
| 工具 | Read, Grep, Glob | + Bash（运行 npm audit 等安全工具） |
| 输出格式 | 发现摘要 + 文件列表 | 按严重程度分级的安全报告 |

## 特化原则

1. **收紧优于扩大** — 特化时应限制范围而非扩大。通用 reviewer 什么都审查，特化 reviewer 只审查特定领域但审查得更深入
2. **description 精确化** — 避免特化 agent 与通用 agent 在触发范围上重叠。用具体的领域关键词区分
3. **保留基础结构** — 保持基础模板的工作流骨架（步骤 1-2-3 结构），只替换具体内容
4. **添加而非替换** — 在通用审查清单基础上增加领域条目，而非完全替换

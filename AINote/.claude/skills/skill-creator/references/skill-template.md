# Skill 模板结构

## 目录

1. [基础模板](#基础模板)
2. [流程型模板](#流程型-workflow-模板)
3. [知识型模板](#知识型-knowledge-模板)
4. [资源型模板](#资源型-resource-模板)
5. [完整项目结构示例](#完整项目结构示例)

---

## 基础模板

每个 Skill 都应该有这个结构：

```
<skill-name>/
├── SKILL.md                    # 必须：frontmatter + 正文
├── scripts/                    # 可选：可执行脚本
│   └── *.py / *.sh
├── references/                 # 可选：详细参考文档
│   ├── topic-a.md
│   └── topic-b.md
├── assets/                     # 可选：静态资源
│   └── template.*
└── examples/                   # 可选：示例文件
    └── *.md / *.json
```

### SKILL.md 必须包含

```yaml
---
name: <skill-name>              # kebab-case
description: >                   # 描述：功能 + 触发场景
  <功能描述>。当用户<触发场景>时使用此技能。
---
```

---

## 流程型（Workflow）模板

### 场景

部署、提交、生成报告、迁移等有副作用的操作。

### Frontmatter

```yaml
---
name: <action-name>
description: >
  <操作描述>。当用户想要<用户意图描述>时使用此技能。
  触发场景：<具体场景1>、<具体场景2>、<同义词/变体>
disable-model-invocation: true   # 必须：防止自动触发
context: fork                   # 推荐：在隔离环境运行
---
```

### 正文结构

```markdown
# <操作名称>

执行以下步骤：

## 步骤 1：<前置检查>
- [ ] 检查前提条件
- [ ] 验证环境

## 步骤 2：<执行操作>
执行操作命令...

## 步骤 3：<验证>
- [ ] 检查结果
- [ ] 确认成功

## 错误处理
如果失败：
1. 回滚更改
2. 报告错误
3. 清理临时文件
```

### 完整示例结构

```
deploy/
├── SKILL.md
└── scripts/
    ├── deploy.sh
    ├── rollback.sh
    └── health-check.sh
```

---

## 知识型（Knowledge）模板

### 场景

代码规范、API 设计模式、语言语法参考、项目约定。

### Frontmatter

```yaml
---
name: <domain>-conventions
description: >
  <领域>设计规范与约定。当用户编写<相关代码>、<相关配置>或询问<相关问题>时使用。
  触发场景：<具体场景1>、<具体场景2>、<不明显的触发>
paths: "src/**/*.ts"           # 可选：限制路径
---
```

### 正文结构

```markdown
# <领域>规范

## 快速参考

| 操作 | 语法 |
|------|------|
| ... | ... |

## 详细说明

### 主题 1
...

### 主题 2
...

## 参考资料

详细示例见 `references/` 目录。
```

### 完整示例结构

```
python-style/
├── SKILL.md
└── references/
    ├── naming.md       # 命名规范
    ├── imports.md      # 导入顺序
    ├── docstrings.md   # 文档字符串
    └── types.md        # 类型注解
```

---

## 资源型（Resource）模板

### 场景

可视化脚本、数据转换工具、代码生成器、模板引擎。

### Frontmatter

```yaml
---
name: <tool-name>
description: >
  <工具描述>。当用户想要<用户意图>时使用此技能。
allowed-tools: Bash(python *)   # 推荐：限制工具
---
```

### 正文结构

```markdown
# <工具名称>

使用此工具生成/处理...

## 使用方法

运行脚本：

\`\`\`bash
python ${CLAUDE_SKILL_DIR}/scripts/<script>.py <参数>
\`\`\`

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| ... | ... | ... |

## 输出说明

- 输出文件：...
- 格式：...
- 示例：...

## 依赖

- Python 3.8+
- 依赖包：...
```

### 完整示例结构

```
chart-generator/
├── SKILL.md
├── scripts/
│   └── generate.py
└── templates/
    └── chart.html
```

---

## 完整项目结构示例

### 示例 1：流程型 - 数据库迁移

```
db-migrate/
├── SKILL.md
└── scripts/
    ├── migrate.sh
    ├── rollback.sh
    └── validate.sh
```

### 示例 2：知识型 - API 规范

```
api-style/
├── SKILL.md
└── references/
    ├── rest.md
    ├── graphql.md
    ├── errors.md
    └── versioning.md
```

### 示例 3：资源型 - 代码生成器

```
react-component/
├── SKILL.md
├── scripts/
│   └── generate.py
└── templates/
    ├── component.tsx
    └── test.tsx
```

### 示例 4：混合型 - 完整的测试技能

```
test-generator/
├── SKILL.md                   # 知识：测试规范
├── scripts/
│   └── generate.py            # 资源：生成脚本
└── references/
    ├── unittest.md            # 知识：unittest 规范
    ├── pytest.md              # 知识：pytest 规范
    └── fixtures.md            # 知识：fixture 使用
```

---

## 命名规范

| 元素 | 规范 | 示例 |
|------|------|------|
| Skill 名称 | kebab-case | `code-style`, `db-migrate` |
| 脚本文件 | snake_case | `generate_report.py` |
| 参考文档 | kebab-case | `api-design.md` |
| 示例文件 | snake_case + 扩展名 | `example_basic.canvas` |

---

## 常见反模式

### ❌ 不要：把所有内容塞进 SKILL.md

```
# 错误结构
my-skill/
└── SKILL.md  # 800 行，涵盖所有内容
```

### ✅ 应该：拆分到 references/

```
my-skill/
├── SKILL.md          # 300 行：概述 + 索引
└── references/       # 详细文档
    ├── topic-a.md
    ├── topic-b.md
    └── topic-c.md
```

### ❌ 不要：脚本使用硬编码路径

```python
# 错误
open("scripts/template.html")
```

### ✅ 应该：使用相对于脚本目录的路径

```python
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
open(os.path.join(SCRIPT_DIR, "template.html"))
```

或者在使用时传入完整路径。

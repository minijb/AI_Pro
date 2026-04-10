# 技能类型详解

## 目录

1. [三种类型概览](#三种类型概览)
2. [流程型详解](#流程型-workflow)
3. [知识型详解](#知识型-knowledge)
4. [资源型详解](#资源型-resource)
5. [混合类型](#混合类型)
6. [类型选择决策树](#类型选择决策树)

---

## 三种类型概览

| 类型 | 触发方式 | 前置字段 | 典型用途 | 例子 |
|------|----------|----------|----------|------|
| **流程型** | 用户显式 `/name` | `disable-model-invocation: true` | 有副作用的操作 | 部署、提交、生成报告 |
| **知识型** | 自动上下文触发 | 默认（可 `user-invocable: false`） | 领域知识、约定规范 | 代码风格、API 规范、语法参考 |
| **资源型** | 自动或显式 | 通常 `allowed-tools` | 脚本工具、模板生成 | 可视化、转换工具、代码生成器 |

---

## 流程型（Workflow）

### 特征

- 用户通过 `/name` 显式调用
- 包含副作用：部署、修改、发送消息等
- 需要精确的步骤序列
- 必须有错误处理和回退方案

### Frontmatter 配置

```yaml
---
name: deploy
description: 部署应用到生产环境
disable-model-invocation: true  # 防止自动触发
context: fork                   # 可选：在隔离环境运行
---
```

### 结构模板

```markdown
## 部署流程

执行以下步骤：

### 1. 前置检查
- [ ] 运行测试套件
- [ ] 验证构建产物
- [ ] 检查配置

### 2. 执行部署
执行部署脚本...

### 3. 验证
- [ ] 健康检查
- [ ] 日志审查

### 4. 回滚（如失败）
如果失败，执行回滚脚本...
```

### 示例：工作流型技能结构

```
deploy/
├── SKILL.md
└── scripts/
    └── deploy.sh
```

### 注意事项

1. **必须禁用自动触发** — `disable-model-invocation: true`
2. **步骤必须精确** — 每步有明确的输入输出
3. **错误处理** — 每个关键步骤后验证状态
4. **可恢复性** — 失败时提供回滚或重试机制

---

## 知识型（Knowledge）

### 特征

- Claude 根据上下文自动加载
- 领域知识、约定规范、语法参考
- 按主题组织，方便查阅
- 需要良好的可发现性

### Frontmatter 配置

```yaml
---
name: api-conventions
description: 本项目 API 设计规范与约定
user-invocable: false  # 可选：纯后台知识
paths: "src/api/**"    # 可选：路径限制
---
```

### 结构模板

```markdown
## API 设计规范

### RESTful 约定
- 资源命名使用复数名词
- 使用标准 HTTP 方法

### 错误响应格式
```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "..."
  }
}
```

### 分页规范
...
```

### 示例：知识型技能结构

```
api-conventions/
├── SKILL.md              # 主知识库
└── references/
    ├── rest.md           # REST 约定
    ├── graphql.md        # GraphQL 约定
    └── errors.md         # 错误处理
```

### 注意事项

1. **自动加载优化** — description 要有"推送性"，列出常见触发场景
2. **结构清晰** — 使用标题、列表、表格组织内容
3. **渐进式** — 常用内容在前，详细内容在参考文件
4. **路径限制** — 使用 `paths` 限制自动加载范围

---

## 资源型（Resource）

### 特征

- 提供可执行脚本或可嵌入模板
- 脚本需要充分测试
- 通常有 `allowed-tools` 限制
- 可靠性优先

### Frontmatter 配置

```yaml
---
name: codebase-visualizer
description: 生成代码库结构可视化
allowed-tools: Bash(python *)  # 限制可执行命令
---
```

### 结构模板

```markdown
## 代码库可视化

运行可视化脚本：

```bash
python ${CLAUDE_SKILL_DIR}/scripts/visualize.py .
```

这将生成 `codebase-map.html` 并在浏览器中打开。

### 输出说明
- 节点表示文件和目录
- 边表示导入关系
- 颜色表示文件类型
```

### 示例：资源型技能结构

```
codebase-visualizer/
├── SKILL.md
└── scripts/
    ├── visualize.py
    └── templates/
        └── node-template.html
```

### 脚本最佳实践

1. **使用 `${CLAUDE_SKILL_DIR}`** — 所有内部引用必须用此前缀
2. **错误处理** — 脚本失败时提供有意义的错误信息
3. **日志输出** — 长时间运行的任务应有进度提示
4. **依赖说明** — 明确所需 Python 包或系统依赖

---

## 混合类型

很多技能是混合类型，需要组合使用：

### 知识型 + 资源型

提供规范（知识）同时提供验证脚本（资源）：

```yaml
---
name: code-style
description: 代码风格检查与格式化
---
```

```
code-style/
├── SKILL.md
├── references/
│   ├── python.md
│   ├── js.md
│   └── go.md
└── scripts/
    ├── check.py
    └── format.py
```

### 流程型 + 资源型

提供部署流程同时打包部署脚本：

```yaml
---
name: deploy
description: 应用部署流程
disable-model-invocation: true
---
```

```
deploy/
├── SKILL.md
└── scripts/
    ├── deploy.sh
    └── rollback.sh
```

---

## 类型选择决策树

```
你的技能主要是什么？

├─ 执行操作（部署、提交、发送）？
│   └─ 是 → 流程型 + disable-model-invocation: true
│
├─ 提供知识或约定（规范、参考、指南）？
│   └─ 是 → 知识型
│
├─ 提供工具或模板（脚本、生成器）？
│   └─ 是 → 资源型 + allowed-tools
│
└─ 多个目的？
    └─ 混合类型，主类型决定触发方式
```

---

## 常见错误

### ❌ 错误：流程型没有禁用自动触发

```yaml
# 错误
name: deploy
description: 部署应用到生产环境
# 缺少 disable-model-invocation: true
```

```yaml
# 正确
name: deploy
description: 部署应用到生产环境
disable-model-invocation: true
```

### ❌ 错误：资源型脚本使用硬编码路径

```markdown
# 错误
运行: python scripts/generate.py

# 正确
运行: python ${CLAUDE_SKILL_DIR}/scripts/generate.py
```

### ❌ 错误：知识型内容过长

```markdown
# 错误：SKILL.md 超过 800 行

# 正确：拆分为 references/
SKILL.md (< 500 行)
references/
├── detail-a.md
└── detail-b.md
```

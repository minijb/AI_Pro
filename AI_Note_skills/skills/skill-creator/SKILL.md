---
name: skill-creator
description: 创建、修改和改进技能（skills），测量技能性能。当用户想要从头创建技能、修改或优化现有技能、运行测试验证技能效果、进行基准测试分析性能差异，或优化技能的触发描述时使用此技能。
---

# Skill Creator

创建、改进技能并衡量其效果的技能。

## 整体流程

创建技能的基本流程如下：

1. **确定目标** — 明确技能要做什么、解决什么问题
2. **编写初稿** — 根据类型指导写出 SKILL.md
3. **编写测试用例** — 创建 2-3 个真实场景的测试提示
4. **运行测试** — 使用 skill 执行测试，同时运行无 skill 的基准对比
5. **评估结果** — 通过 eval-viewer 定性评估 + 定量断言验证
6. **迭代改进** — 根据反馈优化技能
7. **扩大测试** — 增加更多测试用例，重复验证
8. **优化触发** — 使用描述优化工具提升触发准确性
9. **打包发布** — 打包为 .skill 文件

你的任务是判断用户处于哪个阶段，然后帮助推进。如果用户说"不需要测试，帮我直接改"，也可以灵活处理。

---

## 与用户沟通

Skill creator 会面对不同背景的用户。请注意：
- "评估"和"基准测试"等术语可以解释一下
- 如果用户明显是技术人员，可以直接使用术语
- 不确定时可以简短解释

---

## 创建技能

### 第一步：理解意图

首先理解用户的意图：
1. 这个技能要解决什么问题？
2. 什么情况下应该触发？（用户会怎么描述这个需求）
3. 期望的输出是什么？
4. 是否需要测试用例？客观可验证的技能（文件转换、数据提取、固定流程）需要测试；主观的（写作风格、设计）通常不需要。

### 第二步：明确类型

**Skill 有三种类型，选择正确的类型至关重要：**

**1. 流程型（Workflow）** — 步骤化操作指引
- 用户通过 `/name` 显式触发，适用于有副作用的操作
- 示例：部署、提交、生成报告、数据库迁移
- Frontmatter: `disable-model-invocation: true`
- 结构：清晰的步骤序列，每步有明确的输入输出
- 特点：必须用户显式调用，不自动加载

**2. 知识型（Knowledge）** — 领域知识与约定
- Claude 在相关工作时自动加载，内联到当前对话
- 示例：代码风格规范、API 设计模式、语言语法参考
- Frontmatter: 默认（允许自动加载）
- 结构：指南式内容，按主题组织，方便在工作时查阅
- 特点：Claude 可以根据上下文自动触发

**3. 资源型（Resource）** — 脚本、模板、工具库
- 通过 skill 调用执行脚本，或提供可嵌入的模板
- 示例：可视化脚本、数据转换工具、标准化模板
- Frontmatter: 通常配合 `allowed-tools` 限制工具权限
- 结构：`scripts/` 目录放可执行脚本，skill 内容作为调用说明
- 特点：脚本必须经过充分测试，可靠性优先

> **为什么要区分？** 流程型需要精确的步骤和错误处理；知识型需要良好的组织和可发现性；资源型需要可靠的脚本和清晰的调用接口。混淆类型会导致创建的 skill 结构混乱、不可维护。

详细示例见 `references/skill-types.md`。

### 第三步：编写 SKILL.md

根据用户意图填充 frontmatter 和正文：

**Frontmatter 必填字段：**
- **name**: 技能标识符（小写、kebab-case，最多64字符），将成为 `/slash-command`
- **description**: 触发条件和功能描述，这是触发机制的核心

**Frontmatter 可选字段：**
- `argument-hint` — 自动补全提示，如 `[issue-number]`
- `disable-model-invocation: true` — 仅用户通过 `/name` 调用
- `user-invocable: false` — 后台知识，不在菜单显示
- `allowed-tools` — 限制可用工具，如 `Read Grep Glob`
- `context: fork` + `agent` — 在隔离的子 agent 中运行
- `model` / `effort` — 覆盖模型或努力级别
- `paths` — glob 模式限制自动激活范围
- `hooks` — 技能级钩子
- `shell` — bash 或 powershell

完整字段说明见 `references/schemas.md`。

### 第四步：Skill 结构规范

```
skill-name/
├── SKILL.md (必须)
│   ├── YAML frontmatter (name, description 必须)
│   └── Markdown 正文
├── scripts/ (可选) — 可执行脚本
├── references/ (可选) — 按需加载的文档
└── assets/ (可选) — 模板、图标等资源
```

**渐进式加载：**
1. **元数据** (name + description) — 始终在上下文中 (~100词)
2. **SKILL.md 正文** — 技能触发时加载（理想 <500 行）
3. **Bundled resources** — 按需加载（脚本可执行但不自动加载）

**大文件处理：**
- SKILL.md 接近 500 行时，将详细内容移到 `references/` 目录
- 在 SKILL.md 中清晰说明何时读取哪个参考文件
- 超过 300 行的参考文件需要包含目录表

---

## 高级特性

详细说明见 `references/skill-features.md`。

### 字符串替换

使用以下占位符（实际使用时替换）：
- `$ARGUMENTS` — 传递给技能的所有参数
- `$0`, `$1` — 按位置获取参数
- `${CLAUDE_SESSION_ID}` — 当前会话 ID
- `${CLAUDE_SKILL_DIR}` — 技能目录路径

**重要：所有引用 skill 内部文件的路径必须使用 `${CLAUDE_SKILL_DIR}` 前缀！**

### 动态上下文注入（Init 加载问题修复）

使用 `` !\`command\` `` 在预处理阶段运行 shell 命令，输出替换占位符，为了防止本skill init 报错，本文档中所有此命令都添加了 `\`, 在创建skill的时候请删除它：

```markdown
## PR 上下文
- PR diff: !\`gh pr diff\`
- 变更文件: !\`gh pr diff --name-only\`
```

**Init 加载问题修复：**
1. 所有引用 skill 内部脚本或文件的路径必须使用 `${CLAUDE_SKILL_DIR}` 前缀
2. 例如：`python ${CLAUDE_SKILL_DIR}/scripts/generate.py`
3. 不要使用相对路径或硬编码绝对路径
4. 启用扩展思考：在技能内容中包含 `ultrathink` 关键词

**常见错误：**
```markdown
# 错误写法
运行: python scripts/generate.py

# 正确写法
运行: python ${CLAUDE_SKILL_DIR}/scripts/generate.py
```

### 子 Agent 执行

添加 `context: fork` 在隔离的子 agent 中运行技能：
- `agent: Explore` — 只读探索
- `agent: Plan` — 设计实现计划
- `agent: general-purpose` — 完整工具访问

仅对有明确任务指令的技能使用，纯参考内容不需要。

---

## 测试用例

编写完初稿后，创建 2-3 个真实场景的测试提示：
1. 分享给用户确认："这些测试用例看起来对吗？要不要添加更多？"
2. 用户确认后，保存到 `evals/evals.json`

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "用户的任务提示",
      "expected_output": "期望结果描述",
      "files": []
    }
  ]
}
```

完整 schema 见 `references/schemas.md`。

---

## 运行和评估测试

### 第一步：并行启动所有运行

为每个测试用例同时启动两个子 agent：
- **使用技能**: 执行 `eval-0/with_skill/outputs/`
- **基准对比**: 不使用技能执行 `eval-0/without_skill/outputs/`

```json
{
  "eval_id": 0,
  "eval_name": "描述性名称",
  "prompt": "用户任务提示",
  "assertions": []
}
```

### 第二步：编写断言

在运行进行时编写定量断言。好的断言：
- 客观可验证
- 描述清晰，让人一眼看出检查什么
- 主观输出（写作风格、设计质量）不适合断言

### 第三步：捕获计时数据

子 agent 完成后，任务通知包含 `total_tokens` 和 `duration_ms`，立即保存到 `timing.json`：

```json
{
  "total_tokens": 84852,
  "duration_ms": 23332,
  "total_duration_seconds": 23.3
}
```

### 第四步：评分、聚合、启动查看器

1. **评分**: 读取 `agents/grader.md`，对每个断言评分，保存到 `grading.json`
2. **聚合**: 运行 `python -m scripts.aggregate_benchmark <workspace> --skill-name <name>`
3. **分析**: 读取 `agents/analyzer.md` 的"分析基准结果"部分
4. **启动**: 运行 `eval-viewer/generate_review.py` 打开查看器

### 第五步：读取反馈

用户完成审查后，读取 `feedback.json`：
```json
{
  "reviews": [
    {"run_id": "eval-0-with_skill", "feedback": "图表缺少坐标轴标签", "timestamp": "..."}
  ],
  "status": "complete"
}
```

---

## 改进技能

### 如何思考改进

1. **从反馈中泛化** — 避免只针对特定测试用例的修改，思考如何让技能在更多场景有效
2. **保持提示简洁** — 删除没有价值的内容，让模型高效工作
3. **解释为什么** — 今天的 LLM 很聪明，解释原因比强制规则更有效
4. **寻找重复工作** — 如果所有测试用例都独立写了类似的脚本，说明应该将其打包到 skill 中

### 迭代循环

1. 应用改进到技能
2. 重新运行所有测试用例到 `iteration-<N+1>/`
3. 使用 `--previous-workspace` 启动审查器
4. 等待用户审查
5. 读取反馈，再次改进

重复直到：用户满意 / 反馈都为空 / 没有有意义的进步

---

## 高级：盲测对比

当需要更严格比较两个技能版本时使用：
1. 读取 `agents/comparator.md` 和 `agents/analyzer.md`
2. 独立 agent 评判质量，不透露哪个版本更好
3. 分析为什么获胜者获胜

---

## 描述优化

Description 是触发的核心。优化流程：

1. **生成测试查询**: 20 个查询，混合应该触发/不应该触发
2. **用户审查**: 使用 HTML 模板让用户审核查询
3. **运行优化循环**: `python -m scripts.run_loop --eval-set ... --skill-path ... --max-iterations 5`
4. **应用结果**: 更新 SKILL.md frontmatter

详细说明见"Description Optimization"部分。

---

## Claude.ai 特定说明

Claude.ai 没有子 agent：
- 测试用例需要手动按顺序执行
- 跳过基准测试，专注定性反馈
- 跳过描述优化的 CLI 工具

---

## Cowork 特定说明

- 子 agent 工作正常
- 无浏览器：使用 `--static <output_path>` 生成静态 HTML
- 反馈通过 `feedback.json` 下载读取

---

## 参考文件

- `agents/grader.md` — 如何评估断言
- `agents/comparator.md` — 如何进行盲测对比
- `agents/analyzer.md` — 如何分析为什么一个版本更好
- `references/schemas.md` — frontmatter 字段和 JSON schema
- `references/skill-features.md` — 高级特性详细指南
- `references/skill-types.md` — 技能类型详解与示例

---

## 核心循环总结

理解意图 → 编写/编辑 → 运行测试 → 评估（查看器 + 定量） → 重复 → 打包

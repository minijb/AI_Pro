---
name: wiki_folder_convention
description: wiki 文件夹命名规范、同步更新规则和 Agent 格式规范
type: project
---

# Wiki 文件夹命名规范与同步更新规则

> **重要规则**：每次修改 wiki 功能或文件夹结构时，必须同步更新 CLAUDE.md、skill 和 agent 文件。

---

## 一、文件夹命名规范

### Wiki 文件夹：`数字_名称`

| 文件夹 | 说明 | 位置 |
|--------|------|------|
| `00_日记` | 日常随手记 | `wiki/00_日记/` |
| `01_语言` | 编程语言笔记 | `wiki/01_语言/` |
| `02_编程工具` | IDE/编辑器/构建/版本控制 | `wiki/02_编程工具/` |
| `03_项目` | 个人/协作项目 | `wiki/03_项目/` |
| `04_领域` | AI/图形学/网络/物理 | `wiki/04_领域/` |
| `05_综合` | 跨领域综合分析 | `wiki/05_综合/` |
| `06_游戏开发` | 游戏引擎/渲染/物理 | `wiki/06_游戏开发/` |
| `_index` | 二级索引目录 | `wiki/_index/` |
| `07_misc` | 杂项/待研究问题 | `wiki/07_misc/` |

### Raw 文件夹

| 文件夹 | 说明 | 位置 |
|--------|------|------|
| `raw/_input/files` | 摄入入口（未分类源文件） | `raw/_input/files/` |
| `raw/_input/reports` | ingest 报告输出目录 | `raw/_input/reports/` |
| `raw/articles` | 网页文章 | `raw/articles/` |
| `raw/papers` | 论文 | `raw/papers/` |
| `raw/books` | 书籍 | `raw/books/` |
| `raw/videos` | 视频/字幕 | `raw/videos/` |
| `raw/podcasts` | 播客笔记 | `raw/podcasts/` |
| `raw/diary` | 日记 | `raw/diary/` |

### 命名原则

- Wiki 文件夹使用数字前缀，保持分类顺序
- `_index` 使用下划线前缀，表示特殊用途（二级索引）
- `_input` 使用下划线前缀，表示特殊用途（摄入入口）
- `07_misc` 使用 07，放在最后
- `_input/files/` 和 `_input/reports/` 是 `_input/` 的子目录

---

## 二、Agent 文件格式规范

### 正确格式（YAML Frontmatter）

```yaml
---
name: agent-name
description: 描述何时使用此 agent（包含触发词）
tools: Read, Write, Edit, Glob, Grep
skills:
  - obsidian-markdown
  - wiki-ingest
model: inherit
---

You are a Wiki [Role] specialist...
```

### 必须字段

| 字段 | 必填 | 说明 |
|------|------|------|
| `name` | 是 | agent 名称，使用小写字母和连字符 |
| `description` | 是 | 描述何时使用，包含触发词 |
| `tools` | 否 | 允许的工具列表 |
| `skills` | 否 | 预加载的 skill 列表 |
| `model` | 否 | 使用模型：`sonnet`/`opus`/`haiku`/`inherit` |

### Agent 与 Skill 对应关系

| Agent | Skill | 工具 |
|-------|-------|------|
| `wiki-ingest-agent` | `wiki-ingest`, `obsidian-markdown` | Read, Write, Edit, Glob, Grep |
| `wiki-query-agent` | `wiki-query`, `obsidian-markdown` | Read, Glob, Grep |
| `wiki-lint-agent` | `wiki-lint`, `obsidian-markdown` | Read, Glob, Grep, Write, Edit |
| `wiki-process-agent` | `wiki-process`, `obsidian-markdown`, `json-canvas` | Read, Write, Edit, Glob, Grep, Bash |
| `wiki-analyze-agent` | `wiki-analyze`, `obsidian-markdown` | Read, Write |

---

## 三、同步更新规则

> **核心原则**：wiki 结构变更必须同步到以下三类文件，否则会导致引用失效。

### 必须同步更新的文件

| 文件类型 | 路径 | 说明 |
|----------|------|------|
| **CLAUDE.md** | `CLAUDE.md` | 项目约定和目录结构文档 |
| **System Prompt** | `.claudian/system-prompt.md` | 对话上下文中的 wiki 结构定义 |
| **Skill 文件** | `.claude/skills/wiki-*/SKILL.md` | 5 个 wiki 操作 skill |
| **Agent 文件** | `.claude/agents/wiki-*-agent.md` | 5 个 wiki agent |
| **Index 文件** | `wiki/_index/*.md` | 索引文件中的内部链接 |

### 同步检查清单

每次修改 wiki 文件夹结构时，逐一检查：

- [ ] CLAUDE.md 中的目录结构树
- [ ] CLAUDE.md 中的 ingest 执行步骤
- [ ] system-prompt.md 中的目录结构速查
- [ ] system-prompt.md 中的分类放置规则
- [ ] 所有 5 个 skill 文件中的路径引用
- [ ] 所有 5 个 agent 文件中的路径引用
- [ ] `wiki/_index/*.md` 中的内部 wikilink
- [ ] `wiki/index.md` 中的索引说明
- [ ] `Memory/wiki_stats.md` 中的分类统计（如有变更）

### 常见修改场景

| 修改场景 | 需要更新的内容 |
|----------|---------------|
| 新增文件夹（wiki） | CLAUDE.md、system-prompt.md、所有 skill/agent、Memory/wiki_stats.md |
| 删除文件夹（wiki） | CLAUDE.md、system-prompt.md、所有 skill/agent、index 文件、Memory/wiki_stats.md |
| 重命名文件夹 | 所有包含旧路径的文件、Memory/wiki_stats.md |
| 修改分类编号 | 所有引用该分类的文件、Memory/wiki_stats.md |
| 修改 ingest 工作流 | wiki-ingest-agent.md、wiki-ingest SKILL.md、CLAUDE.md、system-prompt.md |

---

## 四、更新历史

| 日期 | 操作 | 说明 |
|------|------|------|
| 2026-04-12 | 初始化 | 建立文件夹命名规范和同步更新规则 |
| 2026-04-12 | 重命名 | `index` → `_index`，`misc` → `07_misc` |
| 2026-04-12 | Agent 格式 | 重写 5 个 agent 使用正确 YAML frontmatter 格式 |
| 2026-04-12 | Memory 增强 | 5 个 agent 新增详细 Memory 更新步骤，新增 wiki_stats.md |
| 2026-04-12 | _input 入口 | 新增 `raw/_input/` 摄入入口，修改 ingest 工作流 |
| 2026-04-12 | _input 分区 | `_input/` 拆分为 `files/` 和 `reports/` 两个子目录 |

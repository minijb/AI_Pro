# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## 项目概述

这是一个 Obsidian 保险库，通过 Claudaian 插件（v2.0.1）集成了 Claude Code。
Claude 的工作目录设置为 `AI_Note` 文件夹，即 Obsidian 保险库根目录。

**重要模式**：本保险库同时作为 **LLM Wiki**（个人知识库）运行，采用 Karpathy 的
[LLM Wiki 模式](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)，并针对**游戏开发者**职业进行了定制。

---

## 目录结构

```
AI_Note/                       # Obsidian 保险库（Claude 的工作目录）
├── .claude/                   # Claude Code 配置
│   ├── agents/                # 5 个 wiki agent 定义
│   └── skills/                # 10 个 skill 定义（见下方表格）
├── .claudian/                 # Claudaian 插件设置
│   └── claudian-settings.json
├── .obsidian/                 # Obsidian 配置和插件
│   └── plugins/claudian/
├── .startup/                  # 安装部署脚本（首次配置时使用）
├── .obsidian/                 # Obsidian 配置和插件
│   └── plugins/claudian/
├── raw/                       # 🌟 RAW SOURCES（归档后不可变）
│   ├── _input/
│   │   ├── files/             # 摄入入口（用户放入新文件）
│   │   └── reports/           # ingest 报告输出目录
│   ├── articles/              # 网页文章（Web Clipper 抓取）
│   ├── papers/ | books/ | videos/ | podcasts/ | diary/
│   ├── notes/                 # 个人随手笔记（对话记录、灵感、速记）
│   └── images/assets/         # 图片资产
├── wiki/                      # 🌟 THE WIKI（Claude 全权维护）
│   ├── index.md               # 主索引
│   ├── log.md                 # 时间日志（append-only）
│   ├── _index/                # 索引层：二级索引目录
│   │   ├── index_by_category.md / index_by_time.md
│   │   ├── index_00_日记.md ~ index_06_游戏开发.md
│   │   └── base/              # Obsidian Bases 数据库视图（.base 文件）
│   ├── notes/                 # 笔记层：分类内容目录
│   │   ├── 00_日记/ ~ 06_游戏开发/  # 用户查阅的详细笔记
│   │   └── 07_misc/           # 杂项/待研究问题
│   └── entities/              # 实体层：可搜索、可联想的结构化知识节点
│       ├── _index.md          # 实体层总索引
│       ├── objects/           # 实体页（具体事物：工具/语言/项目）
│       ├── concepts/          # 概念页（抽象概念：设计模式/架构思想）
│       ├── relations/         # 关系定义
│       │   ├── index.json     # 关系总表（供 Agent 批量查询）
│       │   └── *.relation.md  # 单个关系详情（含 Mermaid）
│       └── .base/             # 实体 Bases 视图
│           ├── entities_by_type.base
│           └── relations.base
├── Memory/                    # 跨会话上下文（按需加载）
│   ├── MEMORY.md              # 记忆索引
│   ├── raw_stats.md           # raw/ 各模块统计
│   ├── stats/                 # wiki 各子目录状态追踪（SUMMARY.md + 每目录一个文件）
│   ├── relationships/         # wiki 引用关系（SUMMARY.md + log.md + pages/每页一个文件）
│   ├── focus_tracking.md      # 作者关注焦点（近期/中期/很久之前）
│   └── reports.md             # 各模块健康报告
├── wiki_workflow.md           # 五个核心操作的详细流程（含 Mermaid 图）
├── wiki_workflow-ingest.canvas  # Ingest 流程 JSON Canvas 大图
└── wiki_workflow-query.canvas   # Query 流程 JSON Canvas 大图
```

---

## Claudaian 插件配置

- **模型**: haiku（LLM Wiki 工作流文档建议 effortLevel: high）
- **effortLevel**: high
- **permissionMode**: normal
- **systemPrompt**: 使用 `.claudian/system-prompt.md`

详细配置见 `AI_Note/.claudian/claudian-settings.json`。

---

## LLM Wiki 模式

### 三层架构

```
RAW SOURCES (归档后不可变)
    raw/_input/ → 用户放入新文件
    raw/{category}/ → ingest 后归档至此
    Claude 从 _input/ 读取，归档后不修改
           ↓
THE WIKI (Claude 拥有)
    wiki/ 目录，Claude 全权维护
    三层架构：_index（索引）+ notes（笔记）+ entities（实体概念）
           ↓
THE SCHEMA (CLAUDE.md + system-prompt.md)
    定义 wiki 结构、约定、工作流
```

### 五个核心操作（Skill 与 Agent）

| Skill | Agent | 触发词 | 说明 |
|-------|-------|--------|------|
| [[wiki-ingest]] | [[wiki-ingest-agent]] | "处理这个源"/"ingest" | 读取源 → 创建 wiki 页面 → 更新 index/log/Memory |
| [[wiki-query]] | [[wiki-query-agent]] | "关于 xxx"/"query" | 搜索 wiki → 综合答案 → 归档优质答案 |
| [[wiki-lint]] | [[wiki-lint-agent]] | "整理 wiki"/"lint" | 健康检查：矛盾/过时/孤立页面 |
| [[wiki-process]] | [[wiki-process-agent]] | "整理一下"/"精炼" | 精炼/合并/拆分/迁移已有内容 |
| [[wiki-analyze]] | [[wiki-analyze-agent]] | "分析这个"/"文档分析" | 深度分析源文档 → 生成报告 |

每个操作的详细流程（含 Mermaid 图）见 `wiki_workflow.md`。

### 格式与工具 Skill

| Skill | 用途 | 何时使用 |
|-------|------|---------|
| `obsidian-markdown` | Obsidian 风格 Markdown（wikilinks、callouts、embeds、frontmatter） | 创建/编辑任何 `.md` 文件 |
| `obsidian-bases` | Obsidian Bases 数据库视图（`.base` 文件） | 创建/编辑 `.base` 数据库视图 |
| `json-canvas` | JSON Canvas 可视化图（`.canvas` 文件） | 合并/拆分后可视化页面关系 |
| `emmylua-annotation` | EmmyLua 注解语法 | Lua 代码注解相关内容 |
| `skill-creator` | 创建和优化 Claude Code skill | 新建/修改/测试 skill |
| `wiki-structure` | Wiki 目录结构和 frontmatter 规范 | 创建 wiki 页面、检查结构、维护索引 |

> [!important] Agent 调用规则
> - 执行任何 wiki 操作时，必须调用对应的 Agent
> - 创建/编辑 `.md` 文件时，**必须使用** `obsidian-markdown` skill
> - 创建/编辑 `.base` 文件时，**必须使用** `obsidian-bases` skill
> - 可视化页面关系时，**必须使用** `json-canvas` skill
> - 所有 wiki 页面必须使用 Obsidian 格式：`[[wikilink]]`、`> [!note]` callout、标准 frontmatter

---

## 重要原则

### 关于 raw/ 和 wiki/ 目录

- **`raw/`**：源文档集合，分为两类：
  - `_input/files/`：**摄入入口**，用户放入未分类源文件的目录
  - `_input/reports/`：**报告目录**，每次 ingest 后生成报告存放于此
  - 各子目录（`articles/`、`papers/`、`books/` 等）：**归档目录**，文件被 ingest 后自动归档至此
  - **Claude 只向 `_input/files/` 读取，从不直接修改归档目录中的文件**
- **`wiki/`**：Claude 全权维护的知识库，**包括创建、更新、删除交叉引用**

### ingest 流程

1. **检查 & 归类**
   - 检查 `raw/_input/files/`（只检查此处）
   - 分析内容 → 移动到 `raw/{category}/`

2. **创建 wiki 页面**
   - 判断内容类型：note（笔记）→ `notes/00_xxx/`，entity（实体）→ `entities/objects/`，concept（概念）→ `entities/concepts/`
   - 添加 frontmatter（created/updated/description/type）
   - 实体/概念页：额外添加 entity_type/domain/aliases 字段
   - 建立交叉引用
   - 若创建实体/概念：同步更新 `entities/relations/index.json`

3. **更新索引**
   - `wiki/index.md`、`wiki/_index/index_by_category.md`、`wiki/_index/index_by_time.md`
   - 对应分类索引（如 `index_01_语言.md`，Bases 视图自动读取）

4. **更新日志 & 报告**
   - 追加 `wiki/log.md`（格式：`## [YYYY-MM-DD] ingest | Title`）
   - 生成报告到 `raw/_input/reports/`（格式：`{时间}report-{slug}.md`）

5. **更新 Memory**（按需加载）
   - `raw_stats.md`、`relationships/`、`stats/`、`focus_tracking.md`
   - 发现矛盾 → `> [!warning] 矛盾：[[page-a]] vs [[page-b]]`

### wiki 分类约定（00_xxx）

笔记层 `wiki/notes/` 下的分类目录：

| 分类 | 内容 | 示例 |
|------|------|------|
| 00_日记 | 每日随手记 | 日总结、学习反思 |
| 01_语言 | 编程语言学习笔记 | Lua/C++/Shaders |
| 02_编程工具 | IDE/编辑器/构建/版本控制 | VS Code/CMake/Git |
| 03_项目 | 个人/协作项目 | 引擎项目、工具开发 |
| 04_领域 | 跨领域知识 | AI/图形学/网络/物理 |
| 05_综合 | 跨领域分析/概览 | 专题综述、对比分析 |
| 06_游戏开发 | 游戏专项 | Unity/Unreal/渲染管线 |
| 07_misc | 不知道放哪儿的 | 后续 lint 时再整理 |

### 实体层约定（entities/）

实体层 `wiki/entities/` 下的结构化知识节点：

| 子目录 | type 值 | 说明 | 示例 |
|--------|---------|------|------|
| objects/ | entity | 具体实体 | Lua、Unity、CMake |
| concepts/ | concept | 抽象概念 | 状态机、ECS、闭包 |
| relations/ | relation | 关系定义 | Lua→implements→闭包 |

**实体 frontmatter 扩展字段**：

| 字段 | 适用 | 说明 |
|------|------|------|
| entity_type | entity | tool/language/framework/project/library |
| domain | concept | 所属领域 |
| aliases | entity/concept | 搜索别名列表 |
| related_notes | entity/concept | 关联的笔记层页面 |
| source | relation | 关系来源实体 |
| target | relation | 关系目标实体 |
| relation_type | relation | implements/uses/extends/depends_on/relates_to |

**关系类型**：

| 关系类型 | 含义 | 方向 |
|----------|------|------|
| implements | 实体实现概念 | entity → concept |
| uses | A 使用 B | entity → entity/concept |
| extends | A 扩展 B | entity/concept → entity/concept |
| depends_on | A 依赖 B | entity → entity |
| relates_to | 一般关联 | 任意 → 任意 |

### Memory 文件夹用途

- `Memory/` 保存跨会话的上下文信息，独立于 Obsidian 保险库
- 每次 ingest/lint/query 后更新对应 Memory 文件
- 按功能分割节省 token：不需要所有 Memory 内容一起加载
- **stats/**：wiki 各子目录的细粒度状态追踪（按二级/三级目录）
- **relationships/**：wiki 页面间的引用关系追踪
- **按需加载原则**：执行操作时只读取需要的 Memory 子文件

### Obsidian Bases 索引视图

每个分类索引页（`index_XX_xxx.md`）都内嵌了对应的 `.base` 数据库视图，提供交互式表格：

- **路径**：`wiki/_index/base/index_XX_xxx_notes.base`
- **索引单位**：**具体笔记文件**（`.md`），非子分类文件夹
- **字段**：索引（wikilink）、创建时间、更新时间、描述（从 frontmatter 自动读取）
- **嵌入方式**：`> [! Bases]-fold` callout + `![[base/xxx.base]]`
- **使用时**：确保每个 wiki 页面 frontmatter 包含 `created`、`updated`、`description` 字段
- **description 字段**：一句话描述（30 字以内），用于表格的「描述」列，是索引的重要组成部分
- **创建新 base**：参考 `.claude/skills/obsidian-bases/SKILL.md`

### 两级索引策略

- **先读 index.md** 决定需要哪个维度的索引
- 需要功能视图 → 读 `wiki/_index/index_by_category.md`
- 需要时间视图 → 读 `wiki/_index/index_by_time.md`
- 需要具体分类 → 读 `wiki/_index/index_XX_xxx.md`
- 按需加载，避免一次性加载所有索引

---

## Obsidian 核心插件

已启用的核心插件：file-explorer, global-search, switcher, graph, backlink,
canvas, outgoing-link, tag-pane, properties, page-preview, daily-notes, templates,
note-composer, command-palette, editor-status, bookmarks, outline, word-count,
file-recovery, sync, bases。

---

## 权威参考文档

| 文件 | 用途 |
|------|------|
| `wiki_workflow.md` | 五个核心操作的详细流程（含 Mermaid 流程图） |
| `README.md` | 用户使用指南（frontmatter 规范、快速开始） |
| `.claude/agents/*.md` | 各 agent 的具体执行步骤和 Memory 更新清单 |
| `.claude/skills/*/SKILL.md` | 各 skill 的格式规范和示例 |


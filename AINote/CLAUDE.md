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
AI_Pro/Note/
├── AI_Note/               # Obsidian 保险库（Claude 的工作目录）
│   ├── .obsidian/         # Obsidian 配置和插件
│   │   └── plugins/claudian/
│   ├── .claudian/         # Claudaian 插件设置
│   │   ├── claudian-settings.json
│   │   └── system-prompt.md  # LLM Wiki 专用 system prompt
│   ├── raw/               # 🌟 RAW SOURCES
│   │   ├── _input/         # 摄入入口
│   │   │   ├── files/      # 未分类源文件（放入此处等待摄入）
│   │   │   └── reports/   # ingest 报告输出目录
│   │   ├── articles/       # 网页文章（Web Clipper 抓取）
│   │   ├── papers/         # 论文
│   │   ├── books/          # 书籍
│   │   ├── videos/         # 视频/字幕
│   │   ├── podcasts/       # 播客笔记
│   │   ├── diary/          # 日记（每日随手记）
│   │   └── images/assets/  # 图片资产
│   └── wiki/              # 🌟 THE WIKI（Claude 全权维护）
│       ├── index.md               # 主索引
│       ├── _index/               # 🌟 二级索引目录
│       │   ├── index_by_category.md   # 功能索引：按主题分类
│       │   ├── index_by_time.md       # 时间索引：按更新时间归档
│       │   ├── index_00_日记.md       # 各分类详情索引
│       │   ├── index_01_语言.md
│       │   ├── index_02_编程工具.md
│       │   ├── index_03_项目.md
│       │   ├── index_04_领域.md
│       │   ├── index_05_综合.md
│       │   ├── index_06_游戏开发.md
│       │   └── base/                  # 🌟 Obsidian Bases 数据库视图
│       │       ├── index_00_日记_notes.base
│       │       ├── index_01_语言_notes.base
│       │       ├── index_02_编程工具_notes.base
│       │       ├── index_03_项目_notes.base
│       │       ├── index_04_领域_notes.base
│       │       ├── index_05_综合_notes.base
│       │       ├── index_06_游戏开发_notes.base
│       │       └── index_all_notes_by_time.base
│       ├── log.md                 # 时间日志（append-only）
│       ├── 00_日记/                # 日常记录
│       ├── 01_语言/                # 编程语言笔记
│       ├── 02_编程工具/             # IDE/编辑器/构建系统/版本控制
│       ├── 03_项目/                # 个人/协作项目
│       ├── 04_领域/                # AI/图形学/网络等跨领域知识
│       ├── 05_综合/                # 跨领域综合分析（综合/对比/概览）
│       ├── 06_游戏开发/             # 游戏引擎/渲染/物理/音频/UI
│       └── 07_misc/               # 杂项/待研究问题
├── Memory/                # 记忆文件夹（跨会话上下文）
│   ├── MEMORY.md          # 记忆索引
│   ├── raw_stats.md       # raw/ 各模块统计（数量/日期范围）
│   ├── stats/             # 📁 wiki 细粒度状态追踪
│   │   ├── SUMMARY.md     # 总览
│   │   └── {子目录}.md    # 每个 wiki 子目录一个状态文件
│   ├── relationships/     # 📁 wiki 引用关系追踪
│   │   ├── SUMMARY.md     # 总览
│   │   ├── log.md        # 变更日志
│   │   └── pages/        # 每个 wiki 页面一个关系文件
│   ├── focus_tracking.md # 作者关注焦点（近期/中期/很久之前）
│   └── reports.md        # 各模块健康报告
└── LLM_Wiki_Workflows.md
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
    按 00_xxx 主题分类，功能+时间两级索引
           ↓
THE SCHEMA (CLAUDE.md + system-prompt.md)
    定义 wiki 结构、约定、工作流
```

### 五个核心操作（Skill）与 Agent）

| Skill | Agent | 触发词 | 说明 |
|-------|-------|--------|------|
| [[wiki-ingest]] | [[wiki-ingest-agent]] | "处理这个源"/"ingest" | 读取源 → 创建 wiki 页面 → 更新 index/log/Memory |
| [[wiki-query]] | [[wiki-query-agent]] | "关于 xxx"/"query" | 搜索 wiki → 综合答案 → 归档优质答案 |
| [[wiki-lint]] | [[wiki-lint-agent]] | "整理 wiki"/"lint" | 健康检查：矛盾/过时/孤立页面 |
| [[wiki-process]] | [[wiki-process-agent]] | "整理一下"/"精炼" | 精炼/合并/拆分/迁移已有内容 |
| [[wiki-analyze]] | [[wiki-analyze-agent]] | "分析这个"/"文档分析" | 深度分析源文档 → 生成报告 |

> [!important] Agent 调用规则
> - 执行任何 wiki 操作时，必须调用对应的 Agent
> - 创建/编辑所有 markdown 文件时，**必须使用** `obsidian-markdown` skill（见 `.claude/skills/obsidian-markdown/SKILL.md`）
> - 创建/编辑 `.base` 数据库视图文件时，**必须使用** `obsidian-bases` skill（见 `.claude/skills/obsidian-bases/SKILL.md`）
> - 如需可视化页面关系（如合并/拆分后），**必须使用** `json-canvas` skill（见 `.claude/skills/json-canvas/SKILL.md`）
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

### 每次 ingest 必须执行

1. 检查 `raw/_input/files/`（只检查此处，不检查 raw/ 子目录）
2. 分析文件内容，判断类型和分类（article/paper/book/video/podcast/diary）
3. 将文件移动到 `raw/` 对应分类（如 `raw/articles/`）
4. 更新 `wiki/index.md`、`wiki/_index/index_by_category.md`、`wiki/_index/index_by_time.md`
5. 更新对应分类的索引文件（如 `wiki/_index/index_01_语言.md`，Bases 视图自动从 frontmatter 读取数据，无需手动更新）
6. 追加 `wiki/log.md`（格式：`## [YYYY-MM-DD] ingest | Title`）
7. 生成 ingest 报告到 `raw/_input/reports/`（格式：`{时间}report-{slug}.md`）
8. 更新 `Memory/raw_stats.md`（模块统计）
9. 更新 `Memory/relationships/`（引用关系）
10. 更新 `Memory/stats/` 中对应的子目录状态文件（分类统计）
11. 更新 `Memory/focus_tracking.md`（关注焦点）
12. 发现矛盾时主动标记

### wiki 分类约定（00_xxx）

| 分类 | 内容 | 示例 |
|------|------|------|
| 00_日记 | 每日随手记 | 日总结、学习反思 |
| 01_语言 | 编程语言学习笔记 | Lua/C++/Shaders |
| 02_编程工具 | IDE/编辑器/构建/版本控制 | VS Code/CMake/Git |
| 03_项目 | 个人/协作项目 | 引擎项目、工具开发 |
| 04_领域 | 跨领域知识 | AI/图形学/网络/物理 |
| 05_综合 | 跨领域分析/概览 | 专题综述、对比分析 |
| 06_游戏开发 | 游戏专项 | Unity/Unreal/渲染管线 |

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

## LLM Wiki 推荐社区插件

| 插件 | 用途 |
|------|------|
| **Dataview** | 对 frontmatter 运行动态查询 |
| **Obsidian Web Clipper** | 将网页转为 markdown（浏览器扩展）|
| **Templater** | 动态模板 |
| **QuickAdd** | 快速创建页面 |
| **Tracker** | 将 frontmatter 数据绘制为图表 |


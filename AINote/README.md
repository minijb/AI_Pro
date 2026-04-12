# AI_Note — LLM Wiki 使用指南

> 这是一个 Obsidian 保险库，通过 Claudaian 插件集成了 Claude Code，充当个人知识库（LLM Wiki）。

---

## 目录结构

```
AI_Note/
├── raw/                        # 🌟 源文档仓库（归档后不可变）
│   ├── _input/
│   │   ├── files/             # 🌟 放入新文件的地方（摄入入口）
│   │   └── reports/           # ingest 报告输出目录
│   ├── articles/              # 网页文章
│   ├── papers/                # 论文
│   ├── books/                 # 书籍
│   ├── videos/                 # 视频字幕/笔记
│   ├── podcasts/              # 播客笔记
│   └── diary/                 # 日记随手记
│
├── wiki/                       # 🌟 Claude 维护的知识库
│   ├── index.md               # 主索引
│   ├── _index/                # 🌟 二级索引
│   │   ├── base/             # 🌟 Obsidian Bases 数据库视图
│   │   ├── index_by_category.md   # 功能索引（按主题分类）
│   │   ├── index_by_time.md       # 时间索引（按更新时间）
│   │   ├── index_00_日记.md
│   │   ├── index_01_语言.md
│   │   ├── index_02_编程工具.md
│   │   ├── index_03_项目.md
│   │   ├── index_04_领域.md
│   │   ├── index_05_综合.md
│   │   └── index_06_游戏开发.md
│   ├── log.md                 # 操作时间日志（append-only）
│   ├── 00_日记/               # 日常随手记
│   ├── 01_语言/               # 编程语言笔记
│   ├── 02_编程工具/           # IDE/编辑器/构建工具/版本控制
│   ├── 03_项目/               # 个人/协作项目
│   ├── 04_领域/               # AI/图形学/网络/物理
│   ├── 05_综合/               # 跨领域综合分析
│   ├── 06_游戏开发/            # 游戏引擎/渲染/物理/音频/UI
│   └── 07_misc/               # 杂项/待研究问题
│
└── Memory/                     # 跨会话上下文（Claude 内部使用）
```

---

## 核心理念

**传统 RAG**：每次从零发现知识，无积累。

**LLM Wiki**：知识被编译一次并保持最新。交叉引用已存在，矛盾已被标记，综合反映你所读的一切。Wiki 随每个源和每个问题变得更加丰富。

---

## 快速开始

### 1. 摄入新内容

把源文件放入 `raw/_input/files/`，然后告诉 Claude：

> "处理这个源"

Claude 会：
1. 分析文件内容，确定类型和分类
2. 与你讨论核心要点
3. 创建 wiki 页面，建立交叉引用
4. 更新所有索引和日志

支持的源类型：文章、论文、书籍、视频字幕、播客笔记、日记。

### 2. 查询已有知识

直接问 Claude：

> "关于 XXX"
> "wiki 中有没有提到 XXX"
> "query"

Claude 会在 wiki 中检索，综合已有知识回答，并标注矛盾或缺失。

### 3. 整理已有内容

> "整理 wiki" / "lint"
> "精炼这两个页面" / "合并 XXX 和 XXX"

Claude 会执行健康检查、内容精炼、页面合并/拆分/迁移。

---

## wiki 分类规则（00_xxx）

| 分类 | 内容 | 示例 |
|------|------|------|
| `00_日记/` | 每日随手记、学习反思 | 日总结、灵感记录 |
| `01_语言/` | 编程语言学习笔记 | Lua/C++/Shaders 语法特性 |
| `02_编程工具/` | IDE/编辑器/构建/版本控制 | VS Code、CMake、Git |
| `03_项目/` | 个人/协作项目 | 引擎项目、工具开发 |
| `04_领域/` | 跨领域知识 | AI、图形学、网络、物理 |
| `05_综合/` | 跨领域综合分析 | 专题综述、对比分析 |
| `06_游戏开发/` | 游戏专项 | Unity/Unreal、渲染管线 |
| `07_misc/` | 不知道放哪儿的 | 后续 lint 时再整理 |

---

## 索引系统

### 二级索引

- **`wiki/_index/index_by_category.md`** — 功能索引，按主题分类浏览
- **`wiki/_index/index_by_time.md`** — 时间索引，按更新时间浏览

### Obsidian Bases 视图

每个分类索引页（如 `wiki/_index/index_01_语言.md`）都内嵌了 Obsidian Bases 数据库视图，以表格形式展示该分类下的所有笔记：

| 列 | 来源 |
|----|------|
| 索引 | wikilink 链接到笔记 |
| 创建时间 | frontmatter `created` |
| 更新时间 | frontmatter `updated` |
| 描述 | frontmatter `description` |

Bases 视图从笔记的 frontmatter 自动读取数据，**无需手动维护表格**。

---

## frontmatter 规范

每个 wiki 笔记必须包含以下 frontmatter 字段：

```yaml
---
title: 笔记标题
type: source | misc
tags: [tag1, tag2]
created: 2026-04-12
updated: 2026-04-12
description: 一句话描述（30 字以内，用于索引视图的描述列）
---
```

> [!important] `description` 字段
> - **必须填写**，不可省略
> - 30 字以内，一句话概括页面核心内容
> - 会显示在 Bases 索引视图的「描述」列，是索引的重要组成部分

---

## Obsidian 格式约定

- 使用 `[[wikilink]]` 代替 Markdown 链接（重命名时自动更新）
- 使用 callout 语法：`> [!note]`、`> [!warning]`、`> [!tip]`
- 图片/音视频使用嵌入语法：`![[image.png]]`、`![[video.mp4]]`

---

## 五个核心操作

| 操作 | 触发词 | 说明 |
|------|--------|------|
| **Ingest** | "处理这个源"/"ingest" | 源文档 → wiki 页面 → 更新索引 |
| **Query** | "关于 XXX"/"query" | 检索 wiki → 综合回答 → 归档优质答案 |
| **Lint** | "整理 wiki"/"lint" | 健康检查：矛盾/过时/孤立页面 |
| **Process** | "整理一下"/"精炼" | 精炼/合并/拆分/迁移已有内容 |
| **Analyze** | "分析这个"/"文档分析" | 深度分析源文档 → 生成报告 |

---

## 绝对规则

1. **源文件放入 `raw/_input/files/`，不要直接放到 wiki/ 下**
2. **`raw/` 归档后不可变**，Claude 不会修改归档文件
3. **每次 ingest 必须更新索引 + log.md**
4. **发现矛盾必须标记**，不可忽略
5. **好答案归档为 wiki 页面**，不消失在对话中
6. **不知道放哪里 → 先放 `07_misc/`**，后续整理时移动
7. **`description` 字段必须填写**，是索引的重要组成部分

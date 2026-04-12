---
name: wiki-ingest
description: >
  摄入新源文档到 LLM Wiki。触发词："处理这个源"、"ingest"、"加入 wiki"、"摄入"。
  流程：读取 raw/ → 讨论要点 → 创建 wiki 页面 → 更新 index/log → 更新 Memory/。
paths: "AI_Note/**/*"
---

# Wiki Ingest — 摄入新源

将 `raw/` 中的源文档摄入为 wiki 页面。每次执行此操作。

---

## 触发条件

用户说：
- "处理这个源"
- "ingest"
- "把这个加入 wiki"
- "摄入"
- 提供了一个文件路径

---

## 前置检查

1. 检查 `raw/_input/files/` 目录：
   - **为空**：告知用户先将文件放入 `_input/files/`
   - **有文件**：列出文件，逐一分析并归类
2. Ingest 永远只从 `_input/files/` 读取，不检查 `raw/` 子目录
3. 源文件格式：
   - PDF：先用 Read 工具读取
   - 网页：markdown 格式，直接读取
   - 图片：先确认是否有 OCR/描述文本

---

## 执行步骤

### 步骤 1：分析文件并归类

1. 读取 `raw/_input/files/` 中的每个文件
2. 判断内容类型：
   - 网页文章 → `raw/articles/`
   - 论文 → `raw/papers/`
   - 书籍 → `raw/books/`
   - 视频字幕/笔记 → `raw/videos/`
   - 播客笔记 → `raw/podcasts/`
   - 日记/随手记 → `raw/diary/`
   - 其他 → 询问用户确认分类
3. 提取 tags（3-5 个关键词）
4. 补充元数据（作者、日期、来源 URL）
5. 向用户确认归类结果

### 步骤 2：移动文件到归类目录

1. 将 `raw/_input/files/` 中的文件移动到对应 `raw/` 子目录
2. 如需要，编辑文件添加 frontmatter 元数据
3. 记录新路径供后续步骤使用

### 步骤 3：与用户讨论关键要点

- 识别核心信息、重要概念、相关实体
- 询问用户关注重点（"这篇文章你最关心哪部分？"）
- 确认摄入范围（全篇 / 部分 / 特定章节）

### 步骤 4：确定 wiki 放置位置

根据主题选择分类：

| 主题 | 放置位置 |
|------|---------|
| 日记/随手记 | `wiki/00_日记/` |
| 编程语言学习 | `wiki/01_语言/` |
| IDE/编辑器/工具 | `wiki/02_编程工具/` |
| 个人项目 | `wiki/03_项目/` |
| AI/图形/网络/物理 | `wiki/04_领域/` |
| 跨领域综合分析 | `wiki/05_综合/` |
| 游戏引擎/渲染/音效等 | `wiki/06_游戏开发/` |

### 步骤 5：创建 wiki 页面（无 sources/ 目录）

> [!warning] 重要变更
> wiki/ 下不再有 sources/ 目录。源摘要直接放入对应分类文件夹。

按顺序创建/更新页面：

1. **源摘要页**：直接放入对应分类，如 `wiki/01_语言/article-{slug}.md`
2. **其他内容**：直接放入对应的 00_xxx 分类文件夹

每个页面必须包含标准 frontmatter：
```yaml
---
title: 页面标题
type: source | misc
tags: [tag1, tag2]
created: 2026-04-11
updated: 2026-04-11
description: 一句话描述（30 字以内，用于 Bases 索引视图的描述列）
sources: [raw/xxx.md]
---
```

> [!important] `description` 字段要求
> - 必须填写，不可省略
> - 30 字以内，一句话概括页面核心内容
> - 会显示在 Bases 索引视图的「描述」列，是索引的重要组成部分
> - 每次更新页面时同步更新 `updated` 日期，`description` 内容如有变化也应更新

### 步骤 6：添加交叉引用

在相关页面之间添加 `[[wikilink]]` 引用：
- 源摘要页 → 关联概念页
- 概念页 → 源摘要页
- 相关概念之间双向链接

### 步骤 7：更新 index.md（必须）

在 `wiki/index.md` 中添加新页面条目，按分类归入对应 section。
在 `wiki/_index/index_by_category.md` 和 `wiki/_index/index_by_time.md` 中同步更新。

> [!tip] Bases 视图说明
> 各分类索引文件（`wiki/_index/index_XX_xxx.md`）已内嵌 Obsidian Bases 数据库视图，
> 通过 frontmatter 的 `created`、`updated`、`description` 字段自动驱动，
> **无需手动更新索引表格**，只需确保新建页面的 frontmatter 包含这三个字段即可。

### 步骤 8：追加 log.md（必须）

格式：`## [YYYY-MM-DD] ingest | Title`

追加到 `wiki/log.md`，包含：
- 来源路径
- 创建/更新的页面列表
- 关键备注

### 步骤 9：生成 ingest 报告（必须）

在 `raw/_input/reports/` 中生成报告：
1. 报告命名格式：`{YYYY-MM-DD-HHMM}report-{slug}.md`
2. 报告内容包含：源信息、摘要、关键要点、创建的 wiki 页面、相关页面链接

### 步骤 10：更新 Memory/（必须）

1. `Memory/raw_stats.md` — 更新对应模块的文档数+日期
2. `Memory/relationships/SUMMARY.md` — 添加新页面的引用关系到总览
3. `Memory/relationships/pages/{slug}.md` — 创建/更新对应页面的引用关系文件
4. `Memory/stats/SUMMARY.md` — 更新总览中的统计信息
5. `Memory/stats/{子目录}.md` — 更新对应子目录的状态文件
6. `Memory/focus_tracking.md` — 更新关注焦点（如与当前热点相关）

### 步骤 11：向用户报告

- 摘要处理结果
- 列出所有新建/更新的页面
- 提出 1-2 个值得进一步探索的问题

---

## 页面模板

### 源摘要页（放入对应分类文件夹）

> [!warning] 位置变更
> wiki/ 下不再有 sources/ 目录。源摘要直接放入对应分类，如 `wiki/01_语言/article-{slug}.md`。

```markdown
---
title: {标题}
type: source
tags: [{tag1}, {tag2}]
created: {YYYY-MM-DD}
updated: {YYYY-MM-DD}
source: raw/{category}/{filename}.md
source-type: {article|paper|book|video|podcast}
---

## 元信息

- **作者**：{作者}
- **类型**：{类型}
- **来源**：{URL 或来源描述}
- **发表/收录**：{日期}

## 一句话总结

{1-2 句话描述核心内容}

## 关键要点

1. {要点 1}
2. {要点 2}
3. {要点 3}

## 重要引用

> "{引用文本}"

## 相关 wiki 页面

- [[{相关概念}]]
- [[{相关实体}]]

## 与其他源的关系

- 相关：[[src-{xxx}]]
- 对比：[[src-{yyy}]]
```

---

## 绝对规则

1. **永远只从 `raw/_input/files/` 摄入，从不直接从 `raw/` 子目录摄入**
2. **摄入前必须将文件移动到 `raw/` 对应分类，`_input/files/` 必须保持清空**
3. **绝不修改 `raw/` 目录**（归档后的文件保持不变）
4. **每次 ingest 必须更新 `index.md`、`log.md`、`Memory/` 相关文件**
5. **每次 ingest 必须生成报告到 `raw/_input/reports/`**
6. **报告命名格式：`{YYYY-MM-DD-HHMM}report-{slug}.md`**
7. **不知道放哪里 → 放 `wiki/07_misc/`，后续 lint 时移动**
8. **多源摄入时逐一处理，每次都走完整流程**
9. **所有 wiki 页面 frontmatter 必须包含 `created`、`updated`、`description` 三个字段**，供 Bases 索引视图使用

---

## 相关 Skill

- [[wiki-query|查询流程]] — 摄入后如何检索和使用 wiki
- [[wiki-lint|整理流程]] — 定期维护 wiki 健康

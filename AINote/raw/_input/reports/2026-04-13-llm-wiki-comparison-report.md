# LLM Wiki System Comparison Report

**Date:** 2026-04-13
**Author:** Claude Code (via wiki-ingest-agent)

---

## 1. 本 Wiki 系统概述

本系统是基于 **Obsidian + Claudaian 插件 + LLM Wiki 模式** 构建的个人知识库，针对游戏开发者职业定制。

### 核心架构

```
raw/_input/files/  →  摄入入口（用户放入源文件）
raw/{category}/   →  归档目录（摄入后不可变）
wiki/              →  LLM 全权维护的知识库
Memory/            →  跨会话上下文（stats/relationships/focus_tracking）
```

### 五大核心操作

| 操作 | 触发词 | 功能 |
|------|--------|------|
| wiki-ingest | "处理这个源"/"ingest" | 读取源 → 创建 wiki 页面 → 更新索引/Memory |
| wiki-query | "关于 xxx"/"query" | 搜索 wiki → 综合答案 → 归档优质答案 |
| wiki-lint | "整理 wiki"/"lint" | 健康检查（矛盾/过时/孤立页面） |
| wiki-process | "整理一下"/"精炼" | 精炼/合并/拆分/迁移已有内容 |
| wiki-analyze | "分析这个"/"文档分析" | 深度分析源文档 → 生成报告 |

### 特色设计

- **三层架构**：RAW SOURCES（不可变）→ THE WIKI（LLM 拥有）→ THE SCHEMA（约定定义）
- **00_xxx 分类体系**：00_日记 / 01_语言 / 02_编程工具 / 03_项目 / 04_领域 / 05_综合 / 06_游戏开发 / 07_misc
- **双索引策略**：按分类索引 + 按时间索引，按需加载
- **Obsidian Bases**：数据库视图自动从 frontmatter 读取，无手动维护负担
- **Memory 分片**：stats/relationships/focus_tracking 按需加载，节省 token
- **矛盾主动标记**：`> [!warning] 矛盾：[[page-a]] vs [[page-b]]`
- **CLAUDE.md + system-prompt.md 双层 Schema**

---

## 2. 其他 LLM Wiki 系统

### 2.1 Karpathy LLM Wiki（原始模式）

**来源：** [Karpathy's LLM Wiki Gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)

| 特性 | 描述 |
|------|------|
| 核心理念 | 知识在摄入时编译并保持最新，而非查询时从零推导 |
| 核心操作 | Ingest / Query / Lint（三大件） |
| 维护者 | LLM 全权负责交叉引用、索引更新、矛盾标记 |
| 界面 | Obsidian（IDE 类比：Obsidian=IDE，LLM=程序员，wiki=代码库） |
| 辅助工具 | Marp（幻灯片）、Dataview（动态查询）、qmd（搜索） |
| 知识来源 | 浏览器剪辑器抓取网页文章为 markdown |
| 哲学继承 | Vannevar Bush's Memex (1945) 的现代实现 |

**关键洞察：** "LLM 不会厌倦、不会忘记更新交叉引用，可以一次触及 15 个文件。"

---

### 2.2 ChatGPT MD（Obsidian 插件）

**来源：** [bramses/chatgpt-md](https://github.com/bramses/chatgpt-md)

| 特性 | 描述 |
|------|------|
| 多模型支持 | OpenAI / OpenRouter.ai / Ollama（本地）/ LM Studio（本地） |
| per-note 配置 | frontmatter 覆盖全局默认（模型/温度/token 限制） |
| Agent 系统 | 可复用的 AI persona，定义为 Markdown 文件 + system prompt |
| AI Wizard | 从自然语言描述自动生成 agent |
| 工具调用 | Vault Search（文件名+内容搜索）/ File Read / Web Search（Brave API） |
| 隐私设计 | 零追踪，数据仅发往 AI API |
| 模板系统 | 支持对话模板、自动推断标题、注释块排除内容 |

**定位：** Obsidian 内直接对话 AI，工具调用能力强，但非系统性 wiki 管理。

---

### 2.3 Notion AI

**来源：** [Notion Product/AI](https://www.notion.com/product/ai)

| 特性 | 描述 |
|------|------|
| 企业搜索 | 跨 Slack / Google Drive / GitHub 搜索并综合答案 |
| AI Meeting Notes | 自动转录 + 摘要 + 洞察提取 |
| AI Writing | 内嵌写作辅助和草稿生成 |
| Research Mode | 生成详细报告和摘要 |
| Autofill | AI 自动填充数据库属性 |
| 知识库 | 集中式组织知识库 + 文档 + 数据库 |

**定位：** 团队协作导向，AI 功能深度集成到工作流中，但非个性化 wiki 系统。

---

### 2.4 Tana

**来源：** [tana.inc](https://tana.inc)

| 特性 | 描述 |
|------|------|
| 核心定位 | "Agentic Meeting Platform"——会议期间 AI agent 直接产出交付物 |
| 会议转工作 | 讨论实时生成 PR、用户旅程、特性规格、原型等 |
| 自构建知识图谱 | 捕获决策、理由、贡献者、时间线，赋予 agent 机构记忆 |
| compliance | SOC2（进行中）/ HIPAA（进行中）/ GDPR，数据可迁移，不在用户数据上训练 |

**定位：** 会议导向的 agentic 工作流，知识图谱随会议积累，非通用个人 wiki。

---

### 2.5 Obsidian Assistant（社区插件）

**来源：** [nicholasgriffintn/obsidian-assistant](https://github.com/nicholasgriffintn/obsidian-assistant)

| 特性 | 描述 |
|------|------|
| RAG 支持 | 检索增强生成（过滤器尚未实现） |
| 文章分析 | 报告生成和摘要 |
| 笔记转录 | 通过 API 转录 |
| 图像生成 | 通过 API 生成 |
| 成熟度 | v0.0.17，个人使用插件，功能尚在早期 |

**定位：** 个人 RAG 管道工具，成熟度低。

---

### 2.6 Roam Research

**来源：** [roamresearch.com](https://roamresearch.com)

| 特性 | 描述 |
|------|------|
| 核心模型 | 网络化思考（Networked Thought），块引用 + 双链 |
| AI 能力 | 页面中未发现显著内置 AI 功能 |
| 数据格式 | Markdown / Org-mode |
| 隐私 | 强调隐私，插件生态 |

**定位：** 结构化思考工具（大纲+双向链接），非 LLM wiki，无内置 AI 功能。

---

## 3. 功能对比表

| 功能维度 | **本系统** | Karpathy LLM Wiki | ChatGPT MD | Notion AI | Tana | Roam Research |
|---------|-----------|-------------------|------------|-----------|------|---------------|
| 三层架构（raw/wiki/schema） | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| 不可变归档（raw sources） | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| LLM 全权维护 wiki | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Ingest 操作 | ✅ | ✅ | ❌ | ❌（导入） | ❌ | ❌ |
| Query 操作 | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Lint 操作 | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Process 操作 | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Analyze 操作 | ✅ | ❌ | ❌ | ✅（Research Mode） | ❌ | ❌ |
| 交叉引用自动维护 | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| 矛盾主动标记 | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| 分类体系（00_xxx） | ✅ | ❌ | ❌ | ❌（数据库/标签） | ❌ | ❌（页面层级） |
| 双索引（分类+时间） | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Obsidian Bases 视图 | ✅ | ❌（Dataview） | ❌ | ❌ | ❌ | ❌ |
| Memory 分片机制 | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| 多模型支持 | ❌（单一 haiku） | ❌ | ✅ | ❌ | ❌ | ❌ |
| 本地模型支持 | ❌ | ❌ | ✅（Ollama/LM Studio） | ❌ | ❌ | ❌ |
| 工具调用（search/web） | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| Agent 系统 | ❌ | ❌ | ✅ | ❌ | ✅ | ❌ |
| 多用户协作 | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ |
| 会议 AI 集成 | ❌ | ❌ | ❌ | ✅（Meeting Notes） | ✅ | ❌ |
| RAG 管道 | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ |
| Obsidian 原生集成 | ✅（Claudaian） | ✅（IDE 隐喻） | ✅（插件） | ❌ | ❌ | ❌ |

---

## 4. 差异分析

### 4.1 本系统独有的优势

| 优势 | 说明 |
|------|------|
| **Process + Analyze 操作** | 五大操作覆盖更全（精炼/合并/拆分/迁移 + 深度源分析），Karpathy 原版仅三大件 |
| **矛盾主动标记** | `> [!warning] 矛盾` 语法直接标记，wiki-lint 发现后主动标记，其他系统均无此功能 |
| **Memory 分片** | stats/relationships/focus_tracking 按需加载，避免大上下文 token 浪费 |
| **双重索引体系** | index_by_category + index_by_time + 各分类 index_XX_xxx + Bases 视图，四层索引 |
| **归档强制不可变** | raw/{category}/ 归档后绝不修改，CLAUDE.md 明确规则，Karpathy 仅建议但无强制 |
| **职业定制化** | 针对游戏开发者的分类体系（06_游戏开发、02_编程工具等） |
| **Claudaian 插件集成** | Obsidian 内无缝运行 Claude Code，非外部工具调用 |

### 4.2 本系统的差距

| 差距 | 说明 |
|------|------|
| **多模型支持** | 目前仅使用 haiku，无法切换 GPT-4/Claude Sonnet 等高性能模型 |
| **本地模型** | 无 Ollama/LM Studio 支持，数据必须上云 |
| **工具调用** | ChatGPT MD 的 Vault Search / Web Search 工具，本系统无对应能力 |
| **多用户协作** | Notion/Tana/Roam 均支持多人，本系统为纯个人 wiki |
| **会议 AI 集成** | Tana 和 Notion 有实时会议 AI，本系统仅处理文件输入 |
| **RAG 管道** | 摄入即 wiki 化，无独立检索增强管道（但这也是 LLM Wiki 的设计选择） |
| **Agent 可复用性** | ChatGPT MD 的 agent-as-Markdown-file 机制更灵活，本系统的 agents 为固定配置 |

### 4.3 关键设计理念差异

- **本系统 vs Karpathy 原版：** 本系统在三大件基础上扩展为五大件，增加了 process 和 analyze，并加入 Memory 分片和矛盾标记机制。
- **本系统 vs ChatGPT MD：** ChatGPT MD 是"在 Obsidian 里对话 AI"，本系统是"AI 作为 wiki 管理员"——前者以 AI 为工具，后者以 AI 为管理者。
- **本系统 vs Notion/Tana：** 两者为团队协作工具，强调多用户和实时协作；本系统专注个人知识积累和长期维护。
- **本系统 vs Roam Research：** Roam 强调结构化思考和大纲组织，AI 功能薄弱；本系统以 AI 为核心驱动，结构服务于 AI 维护效率。

---

## 5. 总结与建议

### 5.1 核心定位确认

本系统是目前调研中**架构最完整的个人 LLM Wiki 实现**，在以下方面领先：

1. **不可变 raw source + LLM 全权维护 wiki** 的分层设计
2. **五大操作**（ingest/query/lint/process/analyze）覆盖知识库全生命周期
3. **矛盾主动标记 + 交叉引用自动维护** 解决了知识库腐败问题
4. **Memory 分片 + 双索引体系** 支撑长期大规模 wiki 可持续运营

### 5.2 短期改进建议

| 优先级 | 建议 | 理由 |
|--------|------|------|
| 高 | 支持多模型切换（GPT-4/Claude Sonnet） | 当前 haiku 能力受限，高质量 ingest/query 需要更强模型 |
| 高 | 增加 Web Search 工具调用 | query 操作时可实时搜索外部信息补充答案 |
| 中 | 支持本地模型（Ollama） | 隐私敏感场景的替代方案 |
| 中 | agent-as-Markdown-file 机制 | 借鉴 ChatGPT MD，提升 agent 复用灵活性 |
| 低 | 多用户协作支持 | 与本系统个人 wiki 定位冲突，暂不需要 |

### 5.3 长期演进方向

1. **RAG 混合模式**：在保持 LLM Wiki 核心的同时，引入可选 RAG 管道处理超大规模 wiki
2. **实时输入源**：集成浏览器剪辑器、会议转录等实时输入（参考 Tana/Notion）
3. **知识图谱可视化**：基于 Obsidian Canvas 和现有 relationships/Memory，构建 wiki 知识图谱可视化
4. **跨 wiki 协作**：多个 LLM Wiki 实例之间的知识共享机制

---

## 参考来源

- [Karpathy LLM Wiki Gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- [ChatGPT MD (bramses)](https://github.com/bramses/chatgpt-md)
- [Notion AI](https://www.notion.com/product/ai)
- [Tana](https://tana.inc)
- [Obsidian Assistant Plugin](https://github.com/nicholasgriffintn/obsidian-assistant)
- [Roam Research](https://roamresearch.com)

---
name: wiki-structure
description: 当创建或检查 wiki 页面、讨论 wiki 目录结构、维护 wiki 索引时触发。触发词：「wiki 结构」、「目录规范」、「创建 wiki 页面」、「检查 wiki 规范」。
---

# Wiki Structure — LLM Wiki 目录结构规范

本 skill 定义 AI_Note LLM Wiki 的目录结构和约定。所有 wiki 页面必须遵循此规范。

---

## 目录结构（三层架构）

```
wiki/                          # THE WIKI（Claude 全权维护）
├── index.md                  # 主索引
├── log.md                    # 时间日志（append-only）
├── _index/                   # 索引层
│   ├── index_by_category.md # 功能分类索引
│   ├── index_by_time.md     # 时间索引
│   ├── index_00_日记.md     # 各分类详细索引
│   ├── index_01_语言.md
│   ├── index_02_编程工具.md
│   ├── index_03_项目.md
│   ├── index_04_领域.md
│   ├── index_05_综合.md
│   ├── index_06_游戏开发.md
│   └── base/                # Obsidian Bases 数据库视图
│       ├── index_00_日记_notes.base
│       ├── index_01_语言_notes.base
│       ├── ...
│       └── index_all_notes_by_time.base
├── notes/                    # 笔记层：详细笔记
│   ├── 00_日记/
│   ├── 01_语言/
│   │   ├── 脚本语言/
│   │   └── 配置语言/
│   ├── 02_编程工具/
│   │   ├── 构建系统/
│   │   ├── 版本控制/
│   │   └── 编辑器/
│   ├── 03_项目/
│   ├── 04_领域/
│   │   ├── 人工智能/
│   │   ├── 图形学/
│   │   └── 网络/
│   ├── 05_综合/
│   ├── 06_游戏开发/
│   │   ├── 引擎/
│   │   ├── 渲染/
│   │   └── 物理/
│   └── 07_misc/
└── entities/                 # 实体层：可搜索、可联想的结构化知识节点
    ├── _index.md             # 实体层总索引
    ├── objects/              # 实体页（具体事物）
    │   └── _template.md
    ├── concepts/             # 概念页（抽象概念）
    │   └── _template.md
    ├── relations/            # 关系定义
    │   ├── index.json        # 关系总表（供 Agent 批量查询）
    │   └── *.relation.md     # 单个关系详情
    └── .base/                # 实体 Bases 视图
        ├── entities_by_type.base
        └── relations.base
```

---

## 分类规范（notes/00_xxx）

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

---

## 实体层规范（entities/）

### 实体 (objects/)

具体存在的工具、语言、项目、框架等。

| entity_type | 说明 | 示例 |
|-------------|------|------|
| tool | 工具软件 | VS Code, CMake, Git |
| language | 编程语言 | Lua, C++, GLSL |
| framework | 框架/引擎 | Unity, Unreal |
| project | 项目 | AINote, 自研引擎 |
| library | 库/包 | SDL2, ImGui |

### 概念 (concepts/)

抽象的设计模式、架构思想、算法等。

### 关系 (relations/)

实体与实体、实体与概念之间的关系。

| 关系类型 | 含义 | 方向 |
|----------|------|------|
| implements | 实体实现概念 | entity → concept |
| uses | A 使用 B | entity → entity/concept |
| extends | A 扩展 B | entity/concept → entity/concept |
| depends_on | A 依赖 B | entity → entity |
| relates_to | 一般关联 | 任意 → 任意 |

---

## Frontmatter 规范

### 笔记层页面（notes/）

```yaml
---
title: 页面标题
type: note
created: YYYY-MM-DD
updated: YYYY-MM-DD
description: 一句话描述（30 字以内）
related_entities: []  # 可选：关联的实体/概念
---
```

### 实体页（entities/objects/）

```yaml
---
title: 实体名称
type: entity
entity_type: tool|language|framework|project|library
created: YYYY-MM-DD
updated: YYYY-MM-DD
description: 一句话描述（≤30字）
aliases: []
tags: [entity]
related_notes: []
---
```

### 概念页（entities/concepts/）

```yaml
---
title: 概念名称
type: concept
domain: ""
created: YYYY-MM-DD
updated: YYYY-MM-DD
description: 一句话描述（≤30字）
aliases: []
tags: [concept]
related_notes: []
---
```

### 关系页（entities/relations/）

```yaml
---
title: 关系描述
type: relation
relation_type: implements|uses|extends|depends_on|relates_to
source: [[实体或概念]]
target: [[实体或概念]]
bidirectional: false
created: YYYY-MM-DD
description: 关系说明
---
```

### 必填字段

| 字段 | 必填 | 说明 |
|------|------|------|
| title | 是 | 页面标题 |
| type | 是 | note / entity / concept / relation |
| created | 是 | 创建日期，格式 YYYY-MM-DD |
| updated | 是 | 更新日期，格式 YYYY-MM-DD |
| description | 是 | 一句话描述，用于 Bases 索引 |

---

## Bases 索引规范

### 笔记层 Base

- **路径**：`wiki/_index/base/index_XX_分类_notes.base`
- **筛选**：`file.inFolder("wiki/notes/XX_分类/")`
- **属性**：title, created, updated, description

### 实体层 Base

- **实体索引**：`wiki/entities/.base/entities_by_type.base`
  - 筛选：`file.inFolder("wiki/entities/")` 且 `type == "entity" or type == "concept"`
  - 属性：title, entity_type, description, updated

- **关系索引**：`wiki/entities/.base/relations.base`
  - 筛选：`file.inFolder("wiki/entities/relations/")` 且 `type == "relation"`
  - 属性：title, relation_type, source, target

---

## 关系总表 (entities/relations/index.json)

JSON 格式存储所有关系，供 Agent 批量查询：

```json
{
  "version": "1.0",
  "last_updated": "YYYY-MM-DD",
  "relations": [
    {
      "id": "rel-001",
      "type": "uses",
      "source": "lua",
      "target": "状态机",
      "bidirectional": false,
      "description": "Lua 脚本使用状态机模式",
      "created": "YYYY-MM-DD",
      "source_note": "notes/01_语言/Lua_设计模式.md"
    }
  ]
}
```

---

## 页面创建检查清单

创建新的 wiki 页面时：

1. **确认类型** — note → notes/00_xxx/，entity → entities/objects/，concept → entities/concepts/
2. **检查目录结构** — 确认目标目录存在
3. **创建 frontmatter** — 包含对应类型的必填字段
4. **使用 wikilink** — 引用其他 wiki 页面用 `[[pagename]]` 格式
5. **建立交叉引用** — 新页面应在相关索引页中被引用
6. **更新索引** — 如有必要，在对应索引中添加条目
7. **更新关系** — 若创建实体/概念/关系，同步更新 `entities/relations/index.json`

---

## 迁移与重组

移动或重组 wiki 页面时：

1. **保持 frontmatter** — 迁移时保留所有元数据
2. **更新 created** — 不变（保留原始创建时间）
3. **更新 updated** — 改为迁移日期
4. **更新索引引用** — 同步更新所有引用该页面的索引
5. **更新 Base 筛选** — 若目录变更，更新对应 .base 文件的 inFolder 路径
6. **更新关系** — 若实体移动，同步更新 index.json 中的引用
7. **检查 backlinks** — 使用 Obsidian 反向链接确认无孤立引用

---

## 禁止事项

- ❌ 不要直接修改 `raw/` 归档目录中的文件
- ❌ 不要创建缺少 frontmatter 的 wiki 页面
- ❌ 不要跳过分类直接将页面放在 wiki/ 根目录（index.md、log.md 除外）
- ❌ 不要在笔记层使用实体层专有字段（entity_type、domain 等）
- ❌ 不要在实体层使用笔记层专有字段
- ❌ 不要修改 `entities/relations/index.json` 后忘记同步对应的 .relation.md 文件

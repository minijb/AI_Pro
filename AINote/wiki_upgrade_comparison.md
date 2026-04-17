# LLM Wiki 三层架构升级方案 — 对比报告

> 生成时间：2026-04-14
> 原始需求：将 wiki 层分为三个部分（_index、详细笔记、实体概念）

---

## 一、目标结构（两方案共同）

```
wiki/
├── _index/                      # 索引层
├── notes/                       # 详细笔记层（重命名自 00_xxx）
└── entities/                    # 实体概念层（新增）
    ├── entities/               # 实体页
    ├── concepts/               # 概念页
    ├── summaries/              # Summary 页
    └── relationships/          # 关系图谱
```

---

## 二、方案对比

| 维度 | Plan A（扁平化） | Plan B（结构化） |
|------|-----------------|-----------------|
| **实体存储** | 纯 .md 文件 + frontmatter `relationships:` 字段 | .md 文件 + .base 索引 + JSON 关系总表 |
| **关系存储** | frontmatter 内 `relationships:` 字段 | 独立 `relations/index.json` + `.base` 视图 |
| **可视化** | Mermaid 内联在 .md 中 | JSON → Mermaid 自动生成 + Bases 看板视图 |
| **Obsidian 搜索** | 依赖内置搜索 + frontmatter | Obsidian 搜索 + Bases 筛选视图 |
| **Agent 读取方式** | 直接读取 frontmatter relationships | 解析 JSON 文件 + 遍历 .base |
| **关系查询效率** | 需逐文件读取 | 一次读取 JSON 获取所有关系 |
| **实施复杂度** | **低**（纯重命名 + 新增 .md） | **中**（需创建 .base + JSON + 维护同步） |
| **维护成本** | 低 | 中（JSON 与 .base 需保持同步） |
| **迁移难度** | 低，只需目录重命名 | 中，需批量创建 .base 和 JSON |
| **学习曲线** | 低 | 中（需了解 Bases 语法） |

---

## 三、frontmatter Schema 对比

### Plan A — 关系内联在 frontmatter

```yaml
---
title: Lua
type: entity
subtype: language
relationships:
  implements: ["闭包", "元表"]
  uses: ["C API"]
  related: ["LuaJIT"]
---
```

**优点**：单一数据源，文件自包含
**缺点**：关系分散在各个文件中

### Plan B — 关系外置在 JSON

```yaml
# entities/relations/lua-uses-closure.relation.md
---
title: Lua 使用闭包
type: relation
source: [[lua]]
target: [[闭包]]
relation_type: implements
---
```

```json
// entities/relations/index.json
{
  "relations": [
    {"source": "lua", "target": "闭包", "type": "implements"}
  ]
}
```

**优点**：关系集中，可批量查询
**缺点**：需维护 JSON 与 .md 的同步

---

## 四、Bases 视图对比

### Plan A
- 使用现有的 `wiki/_index/base/` 视图
- 无需新增 Bases 视图
- 实体通过普通搜索查找

### Plan B
- 新增 `entities/.base/entities_by_type.base`
- 新增 `entities/.base/relations.base`
- 支持按类型筛选实体、按类型筛选关系

---

## 五、Agent 工作流影响

| Agent | Plan A | Plan B |
|-------|--------|--------|
| **ingest** | 识别类型后写入 frontmatter | 识别类型后写入 .md + 更新 JSON |
| **query** | 读取 frontmatter 联想 | 解析 JSON + .base 联想 |
| **lint** | 检查 frontmatter 完整性 | 检查 JSON 与 .md 一致性 |
| **process** | 直接修改 .md 文件 | 修改 .md + 同步更新 JSON |

---

## 六、推荐场景

| 方案 | 推荐场景 |
|------|---------|
| **Plan A** | 快速升级、团队规模小、关系简单、追求简单维护 |
| **Plan B** | 大量实体、复杂关系网络、需要强大可视化、团队有 Bases 使用经验 |

---

## 七、关键文件修改清单（两方案共同部分）

| 类别 | 文件 | 操作 |
|------|------|------|
| **核心配置** | `CLAUDE.md` | 修改：更新目录结构、frontmatter 规范 |
| **Skill** | `.claude/skills/wiki-structure/SKILL.md` | 修改：添加 entities 层规范 |
| **Agent** | `.claude/agents/wiki-ingest-agent.md` | 修改：支持 entity/concept 识别 |
| **Agent** | `.claude/agents/wiki-query-agent.md` | 修改：支持实体搜索/联想 |
| **Agent** | `.claude/agents/wiki-lint-agent.md` | 修改：检查实体完整性 |
| **Memory** | `Memory/relationships/SUMMARY.md` | 修改：支持实体关系统计 |
| **Wiki** | `wiki/00_xxx/` | 重命名 → `wiki/notes/00_xxx/` |
| **Wiki** | `wiki/entities/` | 新建：实体概念层 |

---

## 八、迁移步骤对比

### Plan A 迁移步骤

```
1. 创建 wiki/entities/ 目录结构
2. 创建模板文件 (_template.md)
3. 重命名 wiki/00_xxx/ → wiki/notes/00_xxx/
4. 更新 wiki/index.md 添加 entities 入口
5. 更新 _index/*.md 中的路径引用
6. 更新 CLAUDE.md 和 Agent 文件
7. 验证 wikilink 引用正确
```

### Plan B 迁移步骤

```
1. 创建 wiki/entities/ 目录结构
2. 创建 entities/.base/ Bases 视图
3. 创建 entities/relations/index.json
4. 重命名 wiki/00_xxx/ → wiki/notes/00_xxx/
5. 更新所有 wikilink 引用路径
6. 更新 _index/base/*.base 筛选路径
7. 更新 CLAUDE.md 和 Agent 文件
8. 验证 JSON 与 .md 一致性
9. 验证 Bases 视图正常显示
```

---

## 九、结论与建议

### 选择建议

| 你的情况 | 推荐方案 |
|----------|---------|
| 快速上线、简单使用 | **Plan A** |
| 已有复杂关系网络 | Plan B |
| 需要强大可视化 | Plan B |
| 团队有 Bases 使用经验 | Plan B |
| 后续可能扩展为复杂图谱 | **Plan B**（预留接口）|

### 混合方案（推荐）

采用 **Plan A 作为基础**，同时预留升级到 Plan B 的接口：

1. **当前实施**：Plan A 方式（纯 .md + frontmatter）
2. **预留接口**：
   - frontmatter 中关系字段使用标准化格式
   - `entities/relationships/` 目录结构与 Plan B 一致
   - 可在未来按需升级为 JSON + Bases 视图

这样可以：
- 快速上线使用
- 降低初期实施风险
- 保留后续升级选项

---

## 十、文件清单

| 文件名 | 说明 |
|--------|------|
| `wiki_upgrade_plan_a.md` | Plan A 详细方案 |
| `wiki_upgrade_plan_b.md` | Plan B 详细方案 |
| `wiki_upgrade_comparison.md` | 本对比报告 |

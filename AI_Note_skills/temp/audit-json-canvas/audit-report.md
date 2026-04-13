# JSON Canvas Skill 审计报告

> 审计时间: 2026-04-11 01:40
> 审计路径: `skills/json-canvas/`
> 审计维度: 完整性 | 一致性 | 质量 | 真实案例测试

---

## 1. 结构完整性

### 1.1 文件结构

```
skills/json-canvas/
├── SKILL.md               (288 行)
├── examples/              (7 个 .canvas 文件)
│   ├── basic-text-nodes.canvas
│   ├── vault-embedding.canvas
│   ├── project-board.canvas
│   ├── mind-map.canvas
│   ├── layout-tree.canvas
│   ├── layout-grid.canvas
│   └── layout-mindmap.canvas
└── references/
    ├── canvas-spec.md     (296 行)
    └── layout-algorithms.md (653 行)
```

✅ 符合 Skill 标准结构（有 SKILL.md + examples + references 三层）
✅ SKILL.md 包含完整 frontmatter（name, description, paths）
✅ 引用路径清晰（examples/ 和 references/ 均被 SKILL.md 引用）

### 1.2 示例覆盖矩阵

| 示例文件 | 布局类型 | 节点数 | 边数 | 包含类型 |
|---|---|---|---|---|
| `basic-text-nodes.canvas` | — | 4 | 3 | text(4) |
| `layout-grid.canvas` | — | 12 | 4 | group(3), text(7), file(1), link(1) |
| `layout-mindmap.canvas` | — | 8 | 7 | text(8) |
| `layout-tree.canvas` | — | 7 | 6 | text(7) |
| `mind-map.canvas` | — | 11 | 10 | text(11) |
| `project-board.canvas` | — | 12 | 3 | group(3), text(7), file(1), link(1) |
| `vault-embedding.canvas` | — | 7 | 4 | group(1), text(1), file(4), link(1) |

> 注：布局类型列未标注是因为示例文件名未体现布局类型（仅 layout-*.canvas 标注了类型）

---

## 2. Frontmatter 审计

```yaml
name: json-canvas
description: >
  Create and edit JSON Canvas (.canvas) files — the open format for infinite canvas / whiteboard data,
  originally created for Obsidian. Covers the full JSON Canvas 1.0 spec (nodes, edges, colors, groups)
  and Obsidian Canvas plugin integration (embedding vault notes, media, web pages, connections, groups).
  Trigger on: ".canvas files", "canvas", "whiteboard", "json canvas", "visual note", "mind map on canvas",
  "flowchart canvas", "node graph", "spatial layout", "infinite canvas", "Obsidian whiteboard",
  "canvas diagram", "brainstorm canvas", "tree diagram on canvas", "network graph on canvas",
  "resource list canvas", or any request to create/edit/generate .canvas files from structured content.
  Also trigger when users want to visually organize notes, create spatial layouts, or build
  node-and-edge diagrams in Obsidian — even if they don't explicitly mention "canvas".
paths: "**/*.canvas"
```

| 检查项 | 状态 | 说明 |
|---|---|---|
| name 格式 | ✅ | 小写 kebab-case，符合规范 |
| description 长度 | ⚠️ | 约 500 字符，略长；前 250 字符内触发关键词密度足够 |
| 触发词覆盖 | ✅ | 覆盖了 .canvas、canvas、whiteboard、mind map 等主流说法 |
| paths 字段 | ✅ | `**/*.canvas` 覆盖文件编辑场景 |
| disable-model-invocation | ❌ 未设置 | 知识型 skill，默认允许自动加载，符合预期 |
| user-invocable | ❌ 未设置 | 默认为 true（显示在菜单），对于知识型 skill 可能不需要 |

**建议：** 考虑添加 `user-invocable: false`，因为这是知识型 skill，不需要用户显式调用。

---

## 3. JSON 验证

对 7 个示例文件进行 JSON 语法验证和引用完整性检查：

| 文件 | JSON 有效 | 节点数 | 边数 | 重复 ID | 无效引用 |
|---|---|---|---|---|---|
| `basic-text-nodes.canvas` | ✅ | 4 | 3 | ✅ 无 | ✅ 无 |
| `layout-grid.canvas` | ✅ | 12 | 4 | ✅ 无 | ✅ 无 |
| `layout-mindmap.canvas` | ✅ | 8 | 7 | ✅ 无 | ✅ 无 |
| `layout-tree.canvas` | ✅ | 7 | 6 | ✅ 无 | ✅ 无 |
| `mind-map.canvas` | ✅ | 11 | 10 | ✅ 无 | ✅ 无 |
| `project-board.canvas` | ✅ | 12 | 3 | ✅ 无 | ✅ 无 |
| `vault-embedding.canvas` | ✅ | 7 | 4 | ✅ 无 | ✅ 无 |

**总体：** 所有示例 JSON 均有效，ID 唯一，引用的节点均存在。

---

## 4. 规范符合性

### 4.1 颜色格式

| 检查项 | 状态 | 详情 |
|---|---|---|
| Preset 色定义 | ✅ | 6 色定义清晰，与 canvas-spec.md 一致 |
| Hex 色格式 | ✅ | 文档规定 `#RRGGBB` 大写 |
| 混用情况 | ✅ | 示例文件中未发现 preset 色与 Hex 混用 |

### 4.2 中文引号

| 文档 | 规定 |
|---|---|
| SKILL.md | 使用 `『』`（中文双引号）和 `「」`（中文单引号） |
| canvas-spec.md | 同上 |

✅ 两处规定一致。但实际示例文件中无中文引号场景（因内容为英文）。

### 4.3 Group Z-Order

- SKILL.md: Group 节点**必须**放在 nodes 数组最前面
- canvas-spec.md: 数组中靠前的节点渲染在底层（z-index 更低）
- ✅ `vault-embedding.canvas`、`layout-grid.canvas`、`project-board.canvas` 均正确将 group 节点放在最前面

---

## 5. 一致性分析

### 5.1 文档间一致性

| 检查项 | SKILL.md | canvas-spec.md | layout-algorithms.md | 结果 |
|---|---|---|---|---|
| Preset 色定义 | ✅ | ✅ | N/A | ✅ 一致 |
| 节点类型 | text/file/link/group | text/file/link/group | N/A | ✅ 一致 |
| 通用常数 | 320/200/20/20px | 320/200/20/20px | 320/200/20/20px | ✅ 一致 |
| 中文引号规则 | 『』「」 | 『』「」 | N/A | ✅ 一致 |
| Group Z-Order | 必须在前 | 靠前=底层 | N/A | ✅ 一致 |
| Tree 布局公式 | x=±160 | N/A | x=±160 | ✅ 一致 |
| Edge fromEnd | N/A | 可设为 none/arrow | N/A | ⚠️ SKILL.md 未提及 |
| Timeline 布局 | 提到但未详述 | 未覆盖 | 未覆盖 | ⚠️ 缺失 |

### 5.2 文档与示例一致性

| 示例文件 | 与 SKILL.md 六步法对照 |
|---|---|
| `layout-mindmap.canvas` | ⚠️ 坐标不对齐 20px 网格 |
| `mind-map.canvas` | ⚠️ 坐标不对齐 20px 网格 |
| `layout-tree.canvas` | ⚠️ 节点间距过近（member01/02 水平重叠） |
| `layout-grid.canvas` | ⚠️ card02/03 在 Group 边缘，有重叠 |
| `vault-embedding.canvas` | ⚠️ y=250 非 20 的倍数 |

**结论：** 示例代码质量总体良好，但存在大量坐标不对齐 20px 网格的情况，与 SKILL.md 中"坐标对齐 20px 网格"的规范不符。

---

## 6. 质量问题

### 🔴 严重问题（影响生成质量）

**无严重问题** — 所有 JSON 有效，引用完整。

### 🟡 中等问题（文档/规范不一致）

#### Q1: 示例坐标不对齐网格
SKILL.md 和 layout-algorithms.md 均规定坐标为 20 的倍数，但以下示例违反此规定：

| 文件 | 违规节点数 | 典型违规值 |
|---|---|---|
| `layout-mindmap.canvas` | 10/8 个节点 | x=250, 590（不在网格上） |
| `mind-map.canvas` | 10/11 个节点 | x=-150, -650, 350 |
| `vault-embedding.canvas` | 1/7 个节点 | y=250 |

**影响：** 模型可能认为 20px 网格是"可选的"而非强制的。

#### Q2: 缺少 Timeline 布局
SKILL.md 在布局类型表中列出了 Timeline（时间线），但：
- `references/layout-algorithms.md` 未覆盖 Timeline
- 无 Timeline 示例文件

#### Q3: 缺少 fromEnd 字段说明
canvas-spec.md 定义了 `fromEnd` 字段（源端点样式），但 SKILL.md 的 Edge 示例中未展示此字段。

#### Q4: Group 节点缺少 background/backgroundStyle 示例
canvas-spec.md 定义了 Group 的 `background` 和 `backgroundStyle` 属性，但 SKILL.md 和所有示例中均未使用这两个字段。

### 🟢 轻微问题

#### Q5: 碰撞检测阈值差异
layout-algorithms.md 中的碰撞检测使用 40px 额外间距，但 SKILL.md 的 Step 5 使用的是 HORIZONTAL_SPACING=320px / VERTICAL_SPACING=200px 作为间距标准，两者的概念不完全对应。

#### Q6: 示例文件命名重复
`mind-map.canvas` 和 `layout-mindmap.canvas` 内容高度相似（都是 ML 主题的思维导图），但名称容易混淆。

#### Q7: ID 长度不统一
ID 长度从 3 位到 17 位不等，没有一致性标准。建议统一使用 16 位 hex（最接近"建议 16 位 hex"的说法）。

---

## 7. 真实案例测试

### 案例 1: 编程语言学习路线（Tree 布局）

使用 skill 的六步法生成了一个 10 节点、9 条边的学习路线 canvas。

**发现的问题：**
- 当同一层级有多个父节点，且每个父节点有多个叶子时，叶子节点容易在 x 方向重叠
- SKILL.md 中 Tree 布局公式未考虑多父节点场景下的 x 坐标分配

**生成的案例：** `real-case-learning-path.canvas`（见 temp 目录）

### 案例 2: 项目看板（Grid 布局）

生成了一个 10 节点、3 条边的 Kanban 看板。

**验证结果：** ✅ JSON 有效，边引用正确，无 ID 重复

**生成的案例：** `real-case-kanban.canvas`（见 temp 目录）

---

## 8. 总体评分

| 维度 | 评分 | 说明 |
|---|---|---|
| 结构完整性 | 9/10 | 缺少 Timeline 布局文件和示例 |
| 内容一致性 | 7/10 | 示例坐标不对齐网格，与规范不符 |
| JSON 质量 | 10/10 | 所有示例 JSON 有效，引用完整 |
| 规范符合性 | 8/10 | 缺少 fromEnd、backgroundStyle 示例 |
| 示例覆盖度 | 7/10 | 覆盖 4 种布局，缺 Timeline |
| Frontmatter | 8/10 | 建议添加 user-invocable |

**综合评分：8.2 / 10**

---

## 9. 改进建议

### 高优先级

1. **修复示例坐标对齐** — 所有示例文件的 x/y 坐标改为 20 的倍数
2. **补充 Timeline 布局** — 在 layout-algorithms.md 添加 Timeline 布局说明和示例
3. **统一 ID 长度** — 建议所有 ID 统一为 16 位 hex

### 中优先级

4. **添加 Group background 示例** — 在 layout-grid.canvas 或新建文件中展示 background/backgroundStyle
5. **补充 fromEnd 字段** — SKILL.md Edge 示例中添加 fromEnd: "none" 的展示
6. **区分 mind-map.canvas 与 layout-mindmap.canvas** — 合并或重新命名，避免混淆
7. **优化六步法 Tree 布局** — 增加多父节点场景的坐标计算说明

### 低优先级

8. **添加 user-invocable: false** — 明确这是纯知识型 skill
9. **精简 description** — 移除重复说法，控制在 400 字符内
10. **补充碰撞检测实际演示** — 在 layout-algorithms.md 中添加实际可运行的碰撞检测代码（非仅伪代码）

---

*报告生成完毕 | 共扫描 7 个示例文件，3 个文档，总计覆盖约 {sum(v for v in file_count.values())} 个逻辑行*

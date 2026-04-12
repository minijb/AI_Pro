---
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
---

# JSON Canvas Skill

Create well-structured `.canvas` files conforming to the [JSON Canvas 1.0 spec](https://jsoncanvas.org/spec/1.0/), with full support for Obsidian Canvas plugin features.

## Quick Examples

Read from `examples/` when you need concrete patterns:

| File | Demonstrates |
|---|---|
| `basic-text-nodes.canvas` | Text nodes, Markdown content, edges with labels |
| `vault-embedding.canvas` | File nodes (notes, images, PDFs), subpath linking |
| `mind-map.canvas` | Radial layout, color coding, hierarchical edges |
| `project-board.canvas` | Groups as swim lanes, link nodes, complex edge routing |
| `layout-tree.canvas` | Tree/hierarchical layout |
| `layout-grid.canvas` | Grid/kanban layout |
| `layout-tree.canvas` | Tree/hierarchical layout |
| `timeline.canvas` | Horizontal/vertical timeline |

---

## 核心工作流：六步创建法

> **遇到创建 canvas 的任务时，始终按此流程执行。**

### Step 1 — 分析内容 (Analyze)

- 提取主要内容节点（主题、章节、核心概念）
- 识别层级关系（父子、并列、交叉引用）
- 识别内容类型：短文本 / 长段落 / 代码 / 列表 / 图片
- 统计节点数量，预估画布规模

### Step 2 — 确定布局类型 (Determine Layout)

根据内容结构选择最佳布局：

| 布局类型 | 适用场景 | 特征 |
|---|---|---|
| **MindMap（思维导图）** | 头脑风暴、主题发散 | 中心节点 + 放射状分支 |
| **Tree（树状结构）** | 层级大纲、分类体系 | 上下或左右分层，父子对齐 |
| **Grid（网格式）** | 资源列表、看板、矩阵 | 分组容器，节点网格排列 |
| **Network（网状结构）** | 关系图、知识图谱 | 多对多连接，节点交错分布 |
| **Timeline（时间线）** | 项目阶段、历史事件 | 线性排列，带方向连接线 |

> 如不确定布局，**默认使用 MindMap**，最通用。

### Step 3 — 规划布局结构 (Plan Structure)

- 确定画布中心点（建议 x:0, y:0）
- 规划每层节点的位置：x, y, width, height
- 分配节点颜色（按层级或类型）
- 规划边的走向（fromSide / toSide）
- 使用**布局算法常数**计算间距（见 references/layout-algorithms.md）
- **多父节点场景**：当同一子节点被多个父节点引用时，先按第一个父节点计算 x坐标，其余父节点对应的连接边可使用 `fromSide: "top"` 或 `"bottom"` 以避免边交叉

### Step 4 — 生成 Canvas (Generate)

按以下顺序生成 JSON：

1. **Group 节点**（如有）— 放在最前面（z-index 最低）
2. **Text / File / Link 节点** — 按层级从中心向外排列
3. **Edge 连接** — 父子关系优先，再添加交叉引用

### Step 5 — 碰撞检测 (Collision Detection)

生成后验证：
- 所有节点中心间距 ≥ `HORIZONTAL_SPACING = 320px`（水平）
- 所有节点中心间距 ≥ `VERTICAL_SPACING = 200px`（垂直）
- 如有重叠，调整间距或节点尺寸

### Step 6 — 验证输出 (Validate)

输出前检查清单：
- [ ] 所有 `id` 唯一，无重复
- [ ] 所有 `edge.fromNode` / `edge.toNode` 引用有效 `node.id`
- [ ] 中文引号：`『』`（双引号），`「」`（单引号）
- [ ] 颜色格式统一（preset 色 或 `#RRGGBB`，不混用）
- [ ] Group 节点在 nodes 数组中排在 contained nodes 之前
- [ ] 无 Emoji（用颜色或文字标签替代）

---

## Node 尺寸标准

根据内容长度确定节点尺寸：

| 内容长度 | 宽度 | 高度 | 适用场景 |
|---|---|---|---|
| 短（< 30 字符） | 220px | 100px | 标签、术语 |
| 中等（30–80 字符） | 260px | 120px | 要点、列表 |
| 长（80–150 字符） | 320px | 140px | 说明、描述 |
| 超长（> 150 字符） | 320px | 180px | 段落、代码 |
| 文件嵌入 | 300–500px | 200–500px | 图片、PDF |
| 链接嵌入 | 400px | 300px | 网页 |

> 节点内边距自动包含在宽高中，无需额外计算。

---

## 配色方案

### Preset 色（推荐）

Preset 色在明/暗主题下自动适配，优先使用：

| 值 | 颜色 | 含义 | 适用 |
|---|---|---|---|
| `"1"` | 红 | 重要、紧急、警告 | 主节点、重点 |
| `"2"` | 橙 | 进行中、行动项 | 待处理 |
| `"3"` | 黄 | 笔记、问题、标注 | 辅助信息 |
| `"4"` | 绿 | 完成、积极、核心 | 中心节点、成功 |
| `"5"` | 青 | 信息、细节、工具 | 分支节点 |
| `"6"` | 紫 | 概念、抽象、扩展 | 叶子节点 |

### 自定义 Hex 色

使用 `#RRGGBB` 大写格式（如 `"#4A90E2"`）。**不要与 Preset 色混用**。

### 配色原则

- **层级配色**：中心用绿(4) → 分支用青(5) → 叶子用紫(6)
- **类型配色**：Text 用暖色，File 用冷色，Link 用中性色
- **保持克制**：同一画布不超过 4 种颜色

---

## 布局算法常数

生成坐标时使用以下常数（详见 `references/layout-algorithms.md`）：

```
HORIZONTAL_SPACING = 320px  // 节点中心最小水平间距
VERTICAL_SPACING   = 200px  // 节点中心最小垂直间距
NODE_PADDING       =  20px  // 节点到容器边缘
GRID_SIZE          =  20px  // 坐标对齐网格（坐标为 20 的倍数）
```

### 常见布局计算

**MindMap（从中心向右展开）：**
```
中心节点: x=0, y=0, width=300, height=120
第一层:   x=350, y=-200, 350, -50, 100 (等间距分布在 y 轴)
第二层:   x=750, 垂直堆叠
```

**Tree（从上到下）：**
```
根节点:   x=0, y=0
第1层:    x=-160, y=300; x=160, y=300  (±160 = width/2 + spacing/2)
第2层:    y=600，每层 y += 300
```

**Grid（Kanban 列）：**
```
列间距:   460px（group width 380 + 80px gap）
节点垂直间距: 180px
```

---

## 节点类型参考

详细 spec 见 `references/canvas-spec.md`（按需加载）。

### Text Node

```json
{
  "id": "abc123def4567890",
  "type": "text",
  "x": 0, "y": 0,
  "width": 320, "height": 140,
  "text": "# Title\n\nContent with **Markdown** and [[wikilinks]].",
  "color": "4"
}
```

### File Node

```json
{
  "id": "def456abc7890123",
  "type": "file",
  "x": 0, "y": 300,
  "width": 400, "height": 300,
  "file": "Notes/Meeting Notes.md",
  "subpath": "#ActionItems"
}
```

### Link Node

```json
{
  "id": "ghi789jkl0123456",
  "type": "link",
  "x": 0, "y": 650,
  "width": 400, "height": 300,
  "url": "https://example.com"
}
```

### Group Node

```json
{
  "id": "grp1abcdef0123456",
  "type": "group",
  "x": -50, "y": -50,
  "width": 600, "height": 400,
  "label": "Phase 1 - Planning",
  "color": "4"
}
```

> Group 节点必须放在 `nodes` 数组的**最前面**，以保证正确的 z-index。

### Edge 连接

```json
{
  "id": "edge01",
  "fromNode": "parent-id",
  "fromSide": "right",
  "toNode": "child-id",
  "toSide": "left",
  "toEnd": "arrow",
  "label": "relates to",
  "color": "3"
}
```

- `fromSide`/`toSide`：指定连接点（`top`/`right`/`bottom`/`left`）
- `toEnd`：`"arrow"`（默认）或 `"none"`
- `fromEnd`：`"none"`（默认）或 `"arrow"` — 用于双向关系
- `label`：复杂关系添加文字标签

**双向边示例：**
```json
{
  "id": "edge02",
  "fromNode": "node-a",
  "fromSide": "right",
  "toNode": "node-b",
  "toSide": "left",
  "fromEnd": "arrow",
  "toEnd": "arrow"
}
```

---

## Obsidian Canvas 操作速查

| 操作 | 方法 |
|---|---|
| 创建 Canvas | 命令面板 "Canvas: Create new canvas" |
| 添加文字卡片 | 双击画布空白处 |
| 添加笔记卡片 | 点击文档图标或从文件浏览器拖拽 |
| 添加媒体 | 点击图片图标或拖拽文件 |
| 添加网页 | 右键 > "Add web page" |
| 编辑卡片 | 双击；Esc 退出 |
| 删除 | 右键 > Delete 或 Delete 键 |
| 选择多个 | 框选，或 Shift+点击切换 |
| 移动 | 拖拽；Shift+拖拽锁定单轴 |
| 创建分组 | 选中卡片 > 右键 > "Create group" |
| 添加连接 | 悬停卡片边缘出现圆点，拖拽到目标 |
| 缩放适应 | Shift+1 适应全部，Shift+2 适应选中 |
| 平移 | Space+拖拽 / 滚轮 |

---

## 常见布局示例

详细示例代码见 `references/layout-algorithms.md`：

- **MindMap**：中心放射，适合头脑风暴
- **Tree**：上下分层，适合组织结构
- **Grid**：分组网格，适合看板、资源列表
- **Network**：自由分布，适合关系图谱

---

## 参考文件

| 文件 | 何时读取 |
|---|---|
| `references/canvas-spec.md` | 需查看完整 JSON Canvas 1.0 spec 时 |
| `references/layout-algorithms.md` | 需要布局算法详细计算或示例时 |

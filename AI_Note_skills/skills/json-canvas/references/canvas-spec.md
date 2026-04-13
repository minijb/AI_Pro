# JSON Canvas 1.0 规范

> 本文档是 JSON Canvas 1.0 规范的完整参考。创建 canvas 文件时按需查阅。

## 目录

- [顶级结构](#顶级结构)
- [节点类型](#节点类型)
- [边的类型](#边的类型)
- [颜色](#颜色)
- [坐标系统](#坐标系统)
- [Z-Order 层叠](#z-order-层叠)
- [验证规则](#验证规则)
- [中文文本处理](#中文文本处理)

---

## 顶级结构

`.canvas` 文件是标准 JSON，只包含两个可选数组：

```json
{
  "nodes": [],
  "edges": []
}
```

- `nodes`：画布上的所有视觉对象
- `edges`：节点之间的连接线

---

## 节点类型

所有节点共享以下属性：

| 属性 | 必填 | 类型 | 描述 |
|---|---|---|---|
| `id` | 是 | string | 唯一标识符（建议 16 位 hex） |
| `type` | 是 | string | `text` / `file` / `link` / `group` |
| `x` | 是 | integer | X 坐标（像素，原点 0,0 为画布中心） |
| `y` | 是 | integer | Y 坐标（负数 = 上方） |
| `width` | 是 | integer | 宽度（像素） |
| `height` | 是 | integer | 高度（像素） |
| `color` | 否 | canvasColor | 节点颜色 |

---

### Text Node（文本节点）

将 Markdown 格式的文本直接存储在画布上。

```json
{
  "id": "a1b2c3d4e5f67890",
  "type": "text",
  "x": 0,
  "y": 0,
  "width": 300,
  "height": 200,
  "text": "# Title\n\nThis is **bold** and a [[wikilink]].",
  "color": "4"
}
```

**支持的 Markdown 元素：**
- 标题（`#` 到 `######`）
- 粗体（`**text**`）、斜体（`*text*`）、删除线（`~~text~~`）
- 无序列表（`- item`）和有序列表（`1. item`）
- 代码块（\`\`\`language，支持语法高亮）
- 引用（`>`）
- 表格
- Wiki 链接（`[[note]]`）和嵌入（`![[image.png]]`）

**注意事项：**
- Text 节点不会出现在 Backlinks 中，直到通过右键 > "Convert to file..." 转换为文件

---

### File Node（文件节点）

嵌入保险库中的文件（笔记、图片、PDF、视频）。

```json
{
  "id": "b2c3d4e5f6a78901",
  "type": "file",
  "x": 400,
  "y": 0,
  "width": 400,
  "height": 300,
  "file": "Projects/My Project.md",
  "subpath": "#Overview"
}
```

| 属性 | 必填 | 描述 |
|---|---|---|
| `file` | 是 | 相对于保险库根目录的路径 |
| `subpath` | 否 | 链接到特定章节（`#Heading`）或块（`#^block-id`） |

**Tips：**
- 图片和 PDF 会渲染为预览
- 使用 `subpath` 可以显示长笔记的特定部分
- 从文件浏览器拖拽文件到画布可快速创建文件节点

---

### Link Node（链接节点）

以 iframe 形式嵌入外部网页。

```json
{
  "id": "c3d4e5f6a7b89012",
  "type": "link",
  "x": 0,
  "y": 300,
  "width": 400,
  "height": 300,
  "url": "https://example.com"
}
```

**注意事项：**
- Ctrl/Cmd+点击在浏览器中打开链接
- 并非所有网站都允许 iframe 嵌入（出于安全考虑）

---

### Group Node（分组节点）

用于组织和视觉分组的容器。放在分组内的节点在视觉上归属于它。

```json
{
  "id": "grp001a1b2c3d4e5",
  "type": "group",
  "x": -50,
  "y": -50,
  "width": 800,
  "height": 500,
  "label": "Phase 1 - Planning",
  "background": "Assets/bg-pattern.png",
  "backgroundStyle": "cover"
}
```

| 属性 | 必填 | 描述 |
|---|---|---|
| `label` | 否 | 分组上显示的文字标签 |
| `background` | 否 | 背景图片路径 |
| `backgroundStyle` | 否 | `cover`（填充，可能裁剪）/ `ratio`（保持比例）/ `repeat`（平铺） |

**关键规则：Group 节点必须出现在 `nodes` 数组的靠前位置（z-index 更低，渲染在底层）。**

---

## 边的类型

连接两个节点的线条：

```json
{
  "id": "edge01",
  "fromNode": "abc123def4567890",
  "fromSide": "right",
  "toNode": "def456abc7890123",
  "toSide": "left",
  "toEnd": "arrow",
  "color": "4",
  "label": "references"
}
```

| 属性 | 必填 | 类型 | 默认值 | 描述 |
|---|---|---|---|---|
| `id` | 是 | string | — | 唯一标识符 |
| `fromNode` | 是 | string | — | 源节点 id |
| `fromSide` | 否 | string | — | 源连接边：`top`/`right`/`bottom`/`left` |
| `fromEnd` | 否 | string | `"none"` | 源端点样式 |
| `toNode` | 是 | string | — | 目标节点 id |
| `toSide` | 否 | string | — | 目标连接边 |
| `toEnd` | 否 | string | `"arrow"` | 目标端点样式 |
| `color` | 否 | canvasColor | — | 线条颜色 |
| `label` | 否 | string | — | 线条上的文字标签 |

**端点样式：** `"none"`（无）或 `"arrow"`（箭头）

当 `fromSide`/`toSide` 省略时，Obsidian 自动选择最近的边。

---

## 颜色

`canvasColor` 类型支持两种格式：

### Preset 色（推荐）

| 值 | 颜色 | 含义 |
|---|---|---|
| `"1"` | 红 | 重要、警告 |
| `"2"` | 橙 | 进行中 |
| `"3"` | 黄 | 笔记、问题 |
| `"4"` | 绿 | 完成、积极 |
| `"5"` | 青 | 信息、细节 |
| `"6"` | 紫 | 概念、抽象 |

Preset 色自动适配明/暗主题。

### Hex 色

使用 `#RRGGBB` 大写格式，如 `"#4A90E2"` 或 `"#FF5722"`。

---

## 坐标系统

- **原点**：`0, 0` 是画布中心
- **X 轴**：向右增加，向左为负
- **Y 轴**：向下增加，向上为负
- **坐标对齐**：建议使用 20px 网格对齐（坐标为 20 的倍数）

```
← negative x ... 0 ... positive x →
         ↑
    negative y (0,0)
         ↓
    positive y
```

---

## Z-Order 层叠

节点的渲染顺序由其在 `nodes` 数组中的位置决定：
- **数组中靠前的节点**渲染在底层
- **数组中靠后的节点**渲染在顶层

**正确的 Z-Order 排列：**
```json
"nodes": [
  { "type": "group", ... },      // 最底层
  { "type": "group", ... },      // 次底层
  { "type": "text", ... },       // 中层
  { "type": "file", ... },      // 顶层
  { "type": "link", ... }       // 最顶层
]
```

---

## 验证规则

生成 JSON Canvas 时必须满足：

1. **唯一 ID**：所有节点和边的 id 不能重复
2. **有效引用**：所有 edge 的 `fromNode` / `toNode` 必须引用存在的节点 id
3. **必填字段**：每个节点必须有 `id`, `type`, `x`, `y`, `width`, `height`
4. **类型正确**：`type` 必须是 `text`/`file`/`link`/`group` 之一
5. **坐标为整数**：`x` 和 `y` 必须是整数
6. **颜色格式**：统一使用 preset 色字符串 或 `#RRGGBB` hex，不混用
7. **中文引号**：使用 `『』`（中文双引号）和 `「」`（中文单引号）代替英文引号

---

## 中文文本处理

JSON 中包含中文时，**必须使用中文引号**避免解析错误：

| 原文本 | JSON 中写作 |
|---|---|
| `他说："你好"` | `『他说：「你好」』` |
| `"标题"` | `『标题』` |

**错误示例：**
```json
{ "text": "他说："你好"" }    // ❌ JSON 解析失败
```

**正确示例：**
```json
{ "text": "『他说：「你好」』" }  // ✅
```

> 英文双引号 `"` 在 JSON 中需要转义为 `\"`，使用中文引号可以完全避免这个问题。

---

## 性能建议

- 节点数量建议控制在 **500 个以内**
- 背景图片建议使用压缩格式
- 文字内容保持简洁
- 边交叉影响可读性，尽量减少

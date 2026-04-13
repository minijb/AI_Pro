# 布局算法参考

> 本文档提供常用布局的详细算法、计算公式和示例代码。创建 canvas 时按需查阅。

## 目录

- [通用常数](#通用常数)
- [MindMap 布局](#mindmap-布局)
- [Tree 布局](#tree-布局)
- [Grid 布局](#grid-布局)
- [Timeline 布局](#timeline-布局)
- [Network 布局](#network-布局)
- [碰撞检测](#碰撞检测)
- [边缘标签与箭头](#边缘标签与箭头)
- [完整示例](#完整示例)

---

## 通用常数

所有布局共享以下间距常数：

```
HORIZONTAL_SPACING = 320px  // 节点中心之间的最小水平间距
VERTICAL_SPACING   = 200px  // 节点中心之间的最小垂直间距
NODE_PADDING       =  20px  // 节点到容器边缘的间距
GRID_SIZE          =  20px  // 坐标对齐网格（所有坐标为 20 的倍数）
MIN_NODE_WIDTH     = 220px  // 最小节点宽度
MIN_NODE_HEIGHT    = 100px  // 最小节点高度
```

---

## MindMap 布局

适用于头脑风暴、主题发散、层级概念图。

### 布局规则

- **中心节点**：位于原点 `x:0, y:0`，宽高较大
- **第一层分支**：围绕中心等角度分布，半径 400–600px
- **第二层叶子**：水平排列在分支外侧
- **垂直间距**：第一层节点之间至少 150px
- **水平间距**：叶子节点之间至少 100px

### 坐标计算公式

```
中心节点:  x = -width/2,  y = -height/2

第一层节点 i (共 n 个):
  angle_i = 2π × i / n - π/2   // 从顶部开始逆时针
  center_x = radius × cos(angle_i)
  center_y = radius × sin(angle_i)
  x = center_x - width/2
  y = center_y - height/2

第二层叶子节点:
  x = parent_x + parent_width/2 + HORIZONTAL_SPACING
  y = parent_y ± vertical_offset (交替上下)
```

### MindMap 示例（从原点向右展开）

```json
{
  "nodes": [
    {
      "id": "root001",
      "type": "text",
      "x": -150,
      "y": -60,
      "width": 300,
      "height": 120,
      "text": "# Central Topic\n\nMain concept",
      "color": "4"
    },
    {
      "id": "branch01",
      "type": "text",
      "x": 250,
      "y": -200,
      "width": 220,
      "height": 100,
      "text": "Branch 1\n\nFirst main idea",
      "color": "5"
    },
    {
      "id": "branch02",
      "type": "text",
      "x": 250,
      "y": -50,
      "width": 220,
      "height": 100,
      "text": "Branch 2\n\nSecond main idea",
      "color": "5"
    },
    {
      "id": "branch03",
      "type": "text",
      "x": 250,
      "y": 100,
      "width": 220,
      "height": 100,
      "text": "Branch 3\n\nThird main idea",
      "color": "5"
    },
    {
      "id": "leaf01",
      "type": "text",
      "x": 550,
      "y": -200,
      "width": 200,
      "height": 80,
      "text": "Detail A",
      "color": "6"
    },
    {
      "id": "leaf02",
      "type": "text",
      "x": 550,
      "y": -100,
      "width": 200,
      "height": 80,
      "text": "Detail B",
      "color": "6"
    }
  ],
  "edges": [
    {
      "id": "e1",
      "fromNode": "root001",
      "fromSide": "right",
      "toNode": "branch01",
      "toSide": "left",
      "toEnd": "arrow"
    },
    {
      "id": "e2",
      "fromNode": "root001",
      "fromSide": "right",
      "toNode": "branch02",
      "toSide": "left",
      "toEnd": "arrow"
    },
    {
      "id": "e3",
      "fromNode": "root001",
      "fromSide": "right",
      "toNode": "branch03",
      "toSide": "left",
      "toEnd": "arrow"
    },
    {
      "id": "e4",
      "fromNode": "branch01",
      "fromSide": "right",
      "toNode": "leaf01",
      "toSide": "left",
      "toEnd": "arrow"
    },
    {
      "id": "e5",
      "fromNode": "branch01",
      "fromSide": "right",
      "toNode": "leaf02",
      "toSide": "left",
      "toEnd": "arrow"
    }
  ]
}
```

---

## Tree 布局

适用于组织结构图、分类体系、决策树。

### 布局规则

- **根节点**：位于顶部中心 `x:0, y:0`
- **子节点**：根节点下方 300px，水平分布
- **层级对齐**：同层级节点 y 坐标相同
- **自动分配**：子节点 x 坐标根据兄弟数量均分

### 坐标计算公式

```
根节点:  x = -width/2, y = 0

第 i 层节点:
  y_i = i × VERTICAL_SPACING
  parent_count = 上一层节点数
  total_width = parent_count × HORIZONTAL_SPACING
  start_x = -total_width / 2

  每个节点 x = start_x + spacing × (index + 0.5)
```

### Tree 示例（从上到下两列）

```json
{
  "nodes": [
    {
      "id": "root01",
      "type": "text",
      "x": -160,
      "y": 0,
      "width": 320,
      "height": 120,
      "text": "# Project Root\n\nMain project or organization",
      "color": "4"
    },
    {
      "id": "child01",
      "type": "text",
      "x": -360,
      "y": 300,
      "width": 280,
      "height": 100,
      "text": "## Team Alpha\n\nFrontend development",
      "color": "5"
    },
    {
      "id": "child02",
      "type": "text",
      "x": 80,
      "y": 300,
      "width": 280,
      "height": 100,
      "text": "## Team Beta\n\nBackend development",
      "color": "5"
    },
    {
      "id": "leaf01",
      "type": "text",
      "x": -480,
      "y": 500,
      "width": 200,
      "height": 80,
      "text": "### UI Design",
      "color": "6"
    },
    {
      "id": "leaf02",
      "type": "text",
      "x": -240,
      "y": 500,
      "width": 200,
      "height": 80,
      "text": "### Frontend",
      "color": "6"
    },
    {
      "id": "leaf03",
      "type": "text",
      "x": 160,
      "y": 500,
      "width": 200,
      "height": 80,
      "text": "### API Dev",
      "color": "6"
    }
  ],
  "edges": [
    { "id": "e1", "fromNode": "root01", "fromSide": "bottom", "toNode": "child01", "toSide": "top", "toEnd": "arrow" },
    { "id": "e2", "fromNode": "root01", "fromSide": "bottom", "toNode": "child02", "toSide": "top", "toEnd": "arrow" },
    {id": "e3", "fromNode": "child01", "fromSide": "bottom", "toNode": "leaf01", "toSide": "top", "toEnd": "arrow" },
    { "id": "e4", "fromNode": "child01", "fromSide": "bottom", "toNode": "leaf02", "toSide": "top", "toEnd": "arrow" },
    { "id": "e5", "fromNode": "child02", "fromSide": "bottom", "toNode": "leaf03", "toSide": "top", "toEnd": "arrow" }
  ]
}
```

---

## Grid 布局

适用于资源列表、看板（Kanban）、矩阵数据、分类对比。

### 布局规则

- **Group 分组**：每个分组一个 Group 节点，作为容器
- **节点网格**：组内节点按网格排列，固定间距
- **列间距**：Group 宽度 + 80px gap
- **垂直间距**：节点之间至少 180px

### 坐标计算公式

```
组 x 坐标:  group_x = column_index × (GROUP_WIDTH + 80)
组内节点 x: node_x = group_x + padding + (col % cols) × (NODE_WIDTH + gap)
组内节点 y: node_y = group_y + padding + row × (NODE_HEIGHT + gap)
```

### Grid 示例（三列 Kanban）

```json
{
  "nodes": [
    {
      "id": "group01",
      "type": "group",
      "x": -40,
      "y": -40,
      "width": 380,
      "height": 820,
      "label": "Backlog",
      "color": "3"
    },
    {
      "id": "group02",
      "type": "group",
      "x": 420,
      "y": -40,
      "width": 380,
      "height": 820,
      "label": "In Progress",
      "color": "2"
    },
    {
      "id": "group03",
      "type": "group",
      "x": 880,
      "y": -40,
      "width": 380,
      "height": 820,
      "label": "Done",
      "color": "4"
    },
    {
      "id": "card01",
      "type": "text",
      "x": 0,
      "y": 0,
      "width": 300,
      "height": 140,
      "text": "## User Authentication\n\n- OAuth2 integration\n- Session management",
      "color": "1"
    },
    {
      "id": "card02",
      "type": "text",
      "x": 0,
      "y": 180,
      "width": 300,
      "height": 120,
      "text": "## API Rate Limiting\n\n- Token bucket algorithm",
      "color": "1"
    },
    {
      "id": "card03",
      "type": "text",
      "x": 460,
      "y": 0,
      "width": 300,
      "height": 140,
      "text": "## Database Migration\n\n- PostgreSQL → CockroachDB\n- Zero-downtime",
      "color": "2"
    },
    {
      "id": "card04",
      "type": "text",
      "x": 920,
      "y": 0,
      "width": 300,
      "height": 120,
      "text": "## CI/CD Pipeline\n\n- GitHub Actions setup\n- Auto-deploy",
      "color": "4"
    }
  ],
  "edges": [
    {
      "id": "e1",
      "fromNode": "card01",
      "fromSide": "right",
      "toNode": "card03",
      "toSide": "left",
      "label": "depends on",
      "color": "1"
    }
  ]
}
```

---

## Timeline 布局

适用于项目阶段、历史事件、流程步骤等线性有序的内容。

### 布局规则

- **线性排列**：节点沿水平轴（x 轴）依次排列
- **起点对齐**：所有节点 y 坐标相同（水平时间线），或 x 坐标相同（垂直时间线）
- **等间距**：节点中心之间水平间距 ≥ HORIZONTAL_SPACING
- **连接方向**：同向箭头（left→right 或 top→bottom），体现时间顺序

### 坐标计算公式

```
水平时间线（从左到右）：
  节点 i:  x_i = i × HORIZONTAL_SPACING,  y_i = 0

垂直时间线（从上到下）：
  节点 i:  x_i = 0,  y_i = i × VERTICAL_SPACING
```

### Timeline 示例（水平，2026 Q1 季度计划）

```json
{
  "nodes": [
    {
      "id": "tl001",
      "type": "text",
      "x": 0,
      "y": -60,
      "width": 300,
      "height": 120,
      "text": "# 2026 Q1 计划\n\n产品路线图与关键里程碑",
      "color": "4"
    },
    {
      "id": "tl002",
      "type": "text",
      "x": 320,
      "y": -60,
      "width": 280,
      "height": 120,
      "text": "## 1月\n\n- 用户调研\n- 需求文档 v1.0\n- 技术方案评审",
      "color": "5"
    },
    {
      "id": "tl003",
      "type": "text",
      "x": 640,
      "y": -60,
      "width": 280,
      "height": 120,
      "text": "## 2月\n\n- MVP 开发\n- 集成测试\n- 内部验收",
      "color": "2"
    },
    {
      "id": "tl004",
      "type": "text",
      "x": 960,
      "y": -60,
      "width": 280,
      "height": 120,
      "text": "## 3月\n\n- Beta 发布\n- 性能优化\n- 文档完善",
      "color": "1"
    }
  ],
  "edges": [
    { "id": "et1", "fromNode": "tl002", "fromSide": "left", "toNode": "tl003", "toSide": "right", "toEnd": "arrow", "color": "3" },
    { "id": "et2", "fromNode": "tl003", "fromSide": "left", "toNode": "tl004", "toSide": "right", "toEnd": "arrow", "color": "3" }
  ]
}
```

### 垂直 Timeline 示例（里程碑节点）

```json
{
  "nodes": [
    { "id": "m001", "type": "text", "x": 0,   "y": 0,   "width": 300, "height": 100, "text": "## 立项\n2026-01-15", "color": "4" },
    { "id": "m002", "type": "text", "x": 0,   "y": 300, "width": 300, "height": 100, "text": "## Alpha\n2026-03-01", "color": "2" },
    { "id": "m003", "type": "text", "x": 0,   "y": 600, "width": 300, "height": 100, "text": "## Beta\n2026-06-01", "color": "1" },
    { "id": "m004", "type": "text", "x": 0,   "y": 900, "width": 300, "height": 100, "text": "## 发布\n2026-09-01", "color": "4" }
  ],
  "edges": [
    { "id": "em1", "fromNode": "m001", "fromSide": "bottom", "toNode": "m002", "toSide": "top", "toEnd": "arrow", "color": "3" },
    { "id": "em2", "fromNode": "m002", "fromSide": "bottom", "toNode": "m003", "toSide": "top", "toEnd": "arrow", "color": "3" },
    { "id": "em3", "fromNode": "m003", "fromSide": "bottom", "toNode": "m004", "toSide": "top", "toEnd": "arrow", "color": "3" }
  ]
}
```

---

## Network 布局

适用于关系图谱、知识图谱、流程图等复杂多对多关系。

### 布局规则

- **自由分布**：节点位置根据关系密度自然分布
- **边交叉最小化**：相关节点靠近，减少边交叉
- **分区布局**：将高度关联的节点放在同一区域
- **中心节点**：最重要的节点放在画布中心

### 布局策略

1. **识别核心节点**：找出被引用最多的节点，放中心
2. **聚类分析**：将频繁互相引用的节点归为一组
3. **分区定位**：将节点群分布在画布的不同象限
4. **边优先**：先画边，再调整节点位置避免交叉

### Network 示例

```json
{
  "nodes": [
    {
      "id": "hub001",
      "type": "text",
      "x": 0,
      "y": 0,
      "width": 300,
      "height": 120,
      "text": "# Knowledge Hub\n\nCentral topic connecting all ideas",
      "color": "4"
    },
    {
      "id": "node01",
      "type": "text",
      "x": -400,
      "y": -200,
      "width": 260,
      "height": 100,
      "text": "## Concept A\n\nRelated to hub",
      "color": "5"
    },
    {
      "id": "node02",
      "type": "text",
      "x": 200,
      "y": -200,
      "width": 260,
      "height": 100,
      "text": "## Concept B\n\nAlso connected",
      "color": "5"
    },
    {
      "id": "node03",
      "type": "text",
      "x": -400,
      "y": 200,
      "width": 260,
      "height": 100,
      "text": "## Concept C\n\nCross-links to B",
      "color": "6"
    },
    {
      "id": "node04",
      "type": "text",
      "x": 200,
      "y": 200,
      "width": 260,
      "height": 100,
      "text": "## Concept D\n\nLeaf node",
      "color": "6"
    }
  ],
  "edges": [
    { "id": "e1", "fromNode": "hub001", "fromSide": "left", "toNode": "node01", "toSide": "right", "toEnd": "arrow" },
    { "id": "e2", "fromNode": "hub001", "fromSide": "right", "toNode": "node02", "toSide": "left", "toEnd": "arrow" },
    { "id": "e3", "fromNode": "hub001", "fromSide": "left", "toNode": "node03", "toSide": "right", "toEnd": "arrow" },
    { "id": "e4", "fromNode": "hub001", "fromSide": "right", "toNode": "node04", "toSide": "left", "toEnd": "arrow" },
    { "id": "e5", "fromNode": "node01", "fromSide": "bottom", "toNode": "node03", "toSide": "top", "toEnd": "arrow", "color": "3" },
    { "id": "e6", "fromNode": "node02", "fromSide": "bottom", "toNode": "node04", "toSide": "top", "toEnd": "arrow", "color": "3" },
    { "id": "e7", "fromNode": "node01", "fromSide": "right", "toNode": "node02", "toSide": "left", "toEnd": "arrow", "label": "related", "color": "3" }
  ]
}
```

---

## 碰撞检测

生成布局后，验证所有节点不重叠。

### 检测算法

```python
def has_collision(node_a, node_b):
    """检查两个节点是否碰撞"""
    # 节点中心
    center_a = (node_a.x + node_a.width/2, node_a.y + node_a.height/2)
    center_b = (node_b.x + node_b.width/2, node_b.y + node_b.height/2)

    # 中心间距
    dx = abs(center_a[0] - center_b[0])
    dy = abs(center_a[1] - center_b[1])

    # 最小允许间距
    min_dx = (node_a.width + node_b.width) / 2 + 40  # 40px 额外间距
    min_dy = (node_a.height + node_b.height) / 2 + 40

    return dx < min_dx or dy < min_dy

def validate_layout(nodes):
    """验证所有节点不碰撞"""
    for i, node_a in enumerate(nodes):
        for node_b in nodes[i+1:]:
            if has_collision(node_a, node_b):
                return False, (node_a.id, node_b.id)
    return True, None
```

### 碰撞解决

如检测到碰撞，按优先级调整：
1. **增大间距**：增加 HORIZONTAL_SPACING 或 VERTICAL_SPACING
2. **缩小节点**：减少 width 或 height（内容允许时）
3. **重新排列**：调整节点层级关系
4. **拆分布局**：将大组拆分为多个小组

---

## 边缘标签与箭头

### 边缘标签

在复杂关系中使用 `label` 字段添加文字说明：

```json
{
  "id": "e1",
  "fromNode": "node01",
  "toNode": "node02",
  "label": "depends on",
  "color": "3"
}
```

标签颜色建议：
- `"3"`（黄）：一般关系
- `"1"`（红）：依赖、阻塞
- `"4"`（绿）：启用、促进

### 箭头样式

| toEnd | 效果 |
|---|---|
| `"arrow"` | 目标端带箭头（默认） |
| `"none"` | 无箭头，用于双向或对称关系 |

```json
// 单向箭头（默认）
{ "toEnd": "arrow" }

// 无箭头
{ "toEnd": "none" }

// 两端都无箭头（装饰线）
{ "fromEnd": "none", "toEnd": "none" }
```

### 边的走向（fromSide / toSide）

| 布局类型 | 推荐 fromSide | 推荐 toSide | 原因 |
|---|---|---|---|
| MindMap | `right` | `left` | 从中心向外 |
| Tree（垂直） | `bottom` | `top` | 从上到下 |
| Tree（水平） | `right` | `left` | 从左到右 |
| Grid（同组） | `bottom` | `top` | 组内垂直连接 |
| Grid（跨组） | `right` | `left` | 列间水平连接 |
| Network | 自动或省略 | 自动或省略 | 自由分布 |

---

## 完整示例

### 资源列表（Grid + Group）

适合整理学习资料、工具列表、参考资料：

```json
{
  "nodes": [
    {
      "id": "grp_docs",
      "type": "group",
      "x": -50,
      "y": -50,
      "width": 500,
      "height": 600,
      "label": "Documentation",
      "color": "5"
    },
    {
      "id": "grp_tools",
      "type": "group",
      "x": 530,
      "y": -50,
      "width": 500,
      "height": 600,
      "label": "Tools",
      "color": "2"
    },
    {
      "id": "doc01",
      "type": "text",
      "x": 0,
      "y": 0,
      "width": 400,
      "height": 120,
      "text": "## Official Documentation\n\n[Link](https://example.com)\n\nPrimary reference material",
      "color": "5"
    },
    {
      "id": "doc02",
      "type": "text",
      "x": 0,
      "y": 160,
      "width": 400,
      "height": 120,
      "text": "## API Reference\n\nDetailed API endpoints and parameters",
      "color": "5"
    },
    {
      "id": "tool01",
      "type": "text",
      "x": 580,
      "y": 0,
      "width": 400,
      "height": 120,
      "text": "## VS Code Extension\n\nIDE integration for development",
      "color": "2"
    },
    {
      "id": "tool02",
      "type": "text",
      "x": 580,
      "y": 160,
      "width": 400,
      "height": 120,
      "text": "## CLI Tool\n\nCommand-line interface for automation",
      "color": "2"
    }
  ],
  "edges": [
    {
      "id": "e1",
      "fromNode": "doc01",
      "fromSide": "right",
      "toNode": "tool01",
      "toSide": "left",
      "label": "used by",
      "color": "3"
    }
  ]
}
```

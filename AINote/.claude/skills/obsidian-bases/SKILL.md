---
name: obsidian-bases
description: >
  创建和配置 Obsidian Base 文件（.base）—— 支持表格、卡片、列表和地图视图的类数据库视图。
  触发词："bases"、"base file"、"obsidian database"、"note database"、"table/card/list/map view"、
  使用属性组织/查询笔记。在创建 .base 文件、构建数据库视图、设置筛选/排序/分组视图、
  编写 Bases 公式，或在笔记中嵌入 base 视图时使用。
paths: "**/*.base"
---

# Obsidian Bases

Bases 是 Obsidian 的核心插件，用于创建类数据库视图。它允许用户按属性查看、编辑、排序、筛选和分组文件。所有数据都存储在标准 Markdown 文件及其 frontmatter 属性中——Bases 仅提供视图层。

## 文件格式

Base 以包含 YAML 的 `.base` 文件形式保存。也可以通过 `base` 代码块内联嵌入到笔记中。

## 根级 YAML 结构

```yaml
filters:       # 全局条件，缩小数据集范围（应用于所有视图）
formulas:      # 自定义计算属性
properties:    # 属性的显示配置
summaries:     # 自定义聚合公式
views:         # 视图配置列表
```

---

## 筛选器

筛选器用于限定显示哪些文件。可以在全局（根级）或每个视图中单独定义。全局筛选器和视图级筛选器通过 AND 逻辑合并。

### 筛选器连接词

- `and:` — 所有条件都必须满足
- `or:` — 至少有一个条件满足
- `not:` — 所有条件都不能满足

### 筛选器语法

```yaml
filters:
  and:
    - file.hasTag("project")
    - 'status != "done"'
  or:
    - file.inFolder("Work")
    - file.inFolder("Personal")
  not:
    - file.hasTag("archived")
```

筛选器支持嵌套：

```yaml
filters:
  or:
    - file.hasTag("tag")
    - and:
        - file.hasTag("book")
        - file.hasLink("Textbook")
    - not:
        - file.hasTag("archive")
```

### 常用筛选表达式

| 表达式 | 说明 |
|---|---|
| `file.hasTag("tagname")` | 文件包含指定标签（包含嵌套标签） |
| `file.inFolder("folder")` | 文件位于指定文件夹或子文件夹中 |
| `file.hasLink("filename")` | 文件链接到指定文件 |
| `file.hasProperty("prop")` | 文件包含指定属性 |
| `'property == "value"'` | 属性等于指定值 |
| `'property != "value"'` | 属性不等于指定值 |
| `'property > 5'` | 数值比较 |
| `'file.mtime > now() - "1 week"'` | 在过去一周内被修改 |

---

## 公式

公式用于根据现有数据创建计算属性。条件逻辑使用 `if()` 函数——三元运算符（`? :`）**不支持**。

```yaml
formulas:
  formatted_price: 'if(price, "$" + price.toFixed(2), "")'
  priority_score: "(impact * urgency) / effort"
  full_name: 'first_name + " " + last_name'
  overdue: 'if(due_date < now() && status != "Done", "Overdue", "")'
  deadline: 'start_date + "2w"'
  # 嵌套 if() 处理多个条件：
  level: 'if(score >= 90, "A", if(score >= 70, "B", "C"))'
```

### 属性引用

| 引用方式 | 示例 |
|---|---|
| 笔记属性（简写） | `price`, `status` |
| 笔记属性（显式） | `note.price`, `note["my prop"]` |
| 文件属性 | `file.name`, `file.size`, `file.mtime` |
| 公式属性 | `formula.formatted_price` |

公式不能引用自身（不支持循环引用）。

---

## 属性配置

控制属性的显示名称：

```yaml
properties:
  status:
    displayName: Status
  formula.formatted_price:
    displayName: "Price (USD)"
  file.ext:
    displayName: Extension
```

---

## 汇总

对结果集中所有笔记的属性值进行聚合计算。

### 内置汇总类型

| 汇总类型 | 输入类型 | 说明 |
|---|---|---|
| Average | 数值 | 算术平均值 |
| Sum | 数值 | 总和 |
| Min / Max | 数值 | 最小值 / 最大值 |
| Median | 数值 | 中位数 |
| Range | 数值 | 最大值减最小值 |
| Stddev | 数值 | 标准差 |
| Earliest / Latest | 日期 | 最早 / 最晚日期 |
| Range | 日期 | 最晚日期减最早日期 |
| Checked / Unchecked | 布尔值 | true / false 的计数 |
| Empty / Filled | 任意 | 空值 / 非空值的计数 |
| Unique | 任意 | 不重复值的计数 |

### 自定义汇总

```yaml
summaries:
  customAverage: 'values.mean().round(3)'
```

在汇总公式中，`values` 是该属性在所有笔记上的值列表。

---

## 视图

每个视图定义一种布局类型及其配置。

```yaml
views:
  - type: table          # table | cards | list | map
    name: "My View"
    limit: 10            # 最大显示行数
    groupBy:
      property: note.status
      direction: DESC    # ASC 或 DESC
    filters:             # 视图级筛选器（与全局筛选器通过 AND 合并）
      and:
        - 'status != "done"'
    order:               # 列/属性显示顺序
      - file.name
      - note.status
      - formula.priority_score
    summaries:
      note.price: Sum
      formula.priority_score: Average
```

> **注意：** YAML 语法中没有 `sortBy` 字段。排序只能通过 `groupBy`（同时分组和排序）或通过 Bases 界面配置实现。如果只需要排序而不需要分组，请在界面中配置，而不是写在 YAML 中。

### 视图类型

#### 表格视图
以行（文件）和列（属性）的形式展示文件。完整示例参见 `examples/table-task-tracker.base`。

设置项：行高（短 / 中 / 高 / 超高）。

#### 卡片视图
类似图库的网格布局，支持封面图片。完整示例参见 `examples/cards-reading-list.base`。

设置项：
- **卡片大小** — 每张卡片的宽度
- **图片属性** — 包含封面图片的属性（wiki 链接、URL 或十六进制颜色）
- **图片适应方式** — `cover`（填充并裁剪）或 `contain`（适应但不裁剪）
- **图片宽高比** — 默认为 1:1

#### 列表视图
带项目符号或编号的列表。完整示例参见 `examples/list-simple-notes.base`。

设置项：
- **标记类型** — 项目符号、数字或无标记
- **缩进属性** — 将属性显示为缩进的子项
- **分隔符** — 关闭缩进时分隔属性的字符（默认为逗号）

#### 地图视图
带标记的交互式地图，需安装 Maps 插件。完整示例参见 `examples/map-places.base`。

设置项：
- 内嵌高度、中心坐标、缩放限制
- 标记坐标、颜色、图标
- 背景地图瓦片

---

## 文件属性（所有文件均可用）

| 属性 | 类型 | 说明 |
|---|---|---|
| `file.name` | 字符串 | 文件名 |
| `file.path` | 字符串 | 完整文件路径 |
| `file.folder` | 字符串 | 文件夹路径 |
| `file.ext` | 字符串 | 文件扩展名 |
| `file.size` | 数值 | 文件大小 |
| `file.ctime` | 日期 | 创建时间 |
| `file.mtime` | 日期 | 修改时间 |
| `file.tags` | 列表 | 所有标签 |
| `file.links` | 列表 | 所有内部链接 |
| `file.backlinks` | 列表 | 反向链接（性能开销较大） |
| `file.embeds` | 列表 | 所有嵌入内容 |
| `file.properties` | 对象 | 所有 frontmatter 属性 |

---

## 运算符

### 算术运算符：`+`, `-`, `*`, `/`, `%`, `()`
### 比较运算符：`==`, `!=`, `>`, `<`, `>=`, `<=`
### 布尔运算符：`!`, `&&`, `||`

---

## 日期运算

时间单位：`y`/`year`、`M`/`month`、`d`/`day`、`w`/`week`、`h`/`hour`、`m`/`minute`、`s`/`second`

```yaml
# 示例
date + "1M"              # 加 1 个月
now() - "1 week"         # 1 周前
file.mtime > now() - "7d"  # 7 天内修改过
```

---

## 数据类型

- **字符串**： `"hello"` 或 `'world'`
- **数值**： `42`, `3.14`
- **布尔值**： `true`, `false`
- **日期**： `date("2025-01-01")`, `now()`, `today()`
- **列表**： `[1, 2, 3]`，通过 `property[0]` 访问元素
- **链接**： `link("filename")`, `link("filename", "display text")`

---

## 常用全局函数

| 函数 | 签名 | 说明 |
|---|---|---|
| `if()` | `if(condition, trueVal, falseVal?)` | 条件判断 |
| `now()` | `now()` | 当前日期时间 |
| `today()` | `today()` | 当前日期（时间为 0） |
| `date()` | `date("YYYY-MM-DD HH:mm:ss")` | 解析日期字符串 |
| `link()` | `link(path, display?)` | 创建链接 |
| `image()` | `image(path)` | 渲染图片 |
| `icon()` | `icon("lucide-name")` | 渲染 Lucide 图标 |
| `max()` / `min()` | `max(a, b, ...)` | 多个数值的最大值 / 最小值 |
| `number()` | `number(input)` | 转换为数值 |
| `list()` | `list(element)` | 包装为列表 |
| `html()` | `html(string)` | 渲染为 HTML |
| `escapeHTML()` | `escapeHTML(string)` | 转义 HTML 字符 |
| `duration()` | `duration("5h")` | 解析时间长度 |
| `file()` | `file(path)` | 获取文件对象 |
| `random()` | `random()` | 返回 0-1 之间的随机数 |

## 常用方法函数

**字符串**：`.contains()`, `.containsAll()`, `.containsAny()`, `.lower()`, `.title()`, `.replace()`, `.split()`, `.slice()`, `.trim()`, `.startsWith()`, `.endsWith()`, `.repeat()`, `.reverse()`, `.length`

**数值**：`.abs()`, `.ceil()`, `.floor()`, `.round(digits)`, `.toFixed(precision)`

**日期**：`.format("YYYY-MM-DD")`, `.relative()`, `.date()`, `.time()`, `.year`, `.month`, `.day`, `.hour`

**列表**：`.contains()`, `.filter(expr)`, `.map(expr)`, `.reduce(expr, acc)`, `.sort()`, `.join(sep)`, `.unique()`, `.flat()`, `.slice()`, `.reverse()`, `.length`

**文件**：`.hasTag()`, `.hasLink()`, `.hasProperty()`, `.inFolder()`, `.asLink()`

**链接**：`.asFile()`, `.linksTo(file)`

完整函数参考请参阅官方文档：https://obsidian.md/help/bases/functions

---

## `this` 对象

`this` 在不同上下文中的指向不同：
- **在 .base 文件中**：指向该 base 文件自身的属性
- **嵌入到笔记中时**：指向嵌入所在笔记的属性
- **在侧边栏中**：指向主内容区域当前激活的文件

常用模式：`file.hasLink(this.file)` —— 模拟反向链接面板。

---

## 创建 Base

### 作为独立文件
- 命令面板 → "Bases: Create new base"
- 在文件浏览器中右键文件夹 → "New base"
- 侧边栏按钮 → "Create new base"

### 内嵌到笔记中

**嵌入 .base 文件：**
```markdown
![[MyBase.base]]
![[MyBase.base#ViewName]]
```

**内联代码块：**
````markdown
```base
filters:
  and:
    - file.hasTag("project")
views:
  - type: table
    name: Projects
```
````

---

## 示例

参考 `examples/` 文件夹中的现成模板：

- [table-task-tracker.base](examples/table-task-tracker.base) — 任务管理，包含状态、优先级、截止日期和逾期检测
- [cards-reading-list.base](examples/cards-reading-list.base) — 阅读清单，以卡片布局展示封面图片
- [list-simple-notes.base](examples/list-simple-notes.base) — 简单的筛选笔记列表
- [map-places.base](examples/map-places.base) — 在交互式地图上展示地点
- [table-project-dashboard.base](examples/table-project-dashboard.base) — 使用公式和汇总的项目仪表板
- [embedded-inline.md](examples/embedded-inline.md) — 如何在笔记中内联嵌入 bases

---

> 参考来源：
> - https://obsidian.md/help/bases
> - https://obsidian.md/help/bases/create-base
> - https://obsidian.md/help/bases/views
> - https://obsidian.md/help/bases/syntax
> - https://obsidian.md/help/bases/functions
> - https://obsidian.md/help/formulas
> - https://obsidian.md/help/bases/views/cards
> - https://obsidian.md/help/bases/views/list
> - https://obsidian.md/help/bases/views/map
> - https://obsidian.md/help/bases/views/table

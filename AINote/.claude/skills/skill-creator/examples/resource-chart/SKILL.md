---
name: example-chart
description: >
  示例：生成数据可视化图表。当用户想要生成图表、可视化数据、创建报告图表时使用。
  触发场景：生成图表、可视化、数据报表、chart
allowed-tools: Bash(python *)
---

# 数据可视化工具

生成数据可视化图表。

## 使用方法

运行图表生成脚本：

```bash
python ${CLAUDE_SKILL_DIR}/scripts/generate.py \
  --input data.csv \
  --type bar \
  --output chart.html
```

## 参数说明

| 参数 | 说明 | 必须 | 默认值 |
|------|------|------|--------|
| `--input` | 输入数据文件 (CSV) | 是 | — |
| `--type` | 图表类型 (bar/line/pie) | 否 | bar |
| `--output` | 输出 HTML 文件 | 否 | chart.html |
| `--title` | 图表标题 | 否 | Data Chart |

## 输出说明

生成一个独立的 HTML 文件，包含：
- 使用 Chart.js 渲染
- 支持交互（悬停显示数值）
- 响应式布局
- 深色/浅色主题适配

## 支持的图表类型

- `bar` — 柱状图
- `line` — 折线图
- `pie` — 饼图
- `scatter` — 散点图

## 示例

### 柱状图

```bash
python ${CLAUDE_SKILL_DIR}/scripts/generate.py \
  --input sales.csv \
  --type bar \
  --title "季度销售" \
  --output sales-chart.html
```

### 折线图

```bash
python ${CLAUDE_SKILL_DIR}/scripts/generate.py \
  --input trends.csv \
  --type line \
  --title "用户增长趋势" \
  --output trends-chart.html
```

## 依赖

- Python 3.8+
- pandas
- jinja2

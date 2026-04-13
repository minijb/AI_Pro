# Agent 评估 JSON Schema 参考

本文档定义 agent-creator 评估系统中所有 JSON 文件的格式规范。

---

## 目录

1. [evals.json — 测试用例定义](#1-evalsjson)
2. [eval_metadata.json — 单测试元数据](#2-eval_metadatajson)
3. [grading.json — 评分结果](#3-gradingjson)
4. [timing.json — 计时数据](#4-timingjson)
5. [comparison.json — 盲比较结果](#5-comparisonjson)
6. [benchmark.json — 基准测试汇总](#6-benchmarkjson)
7. [目录结构](#7-目录结构)

---

## 1. evals.json

测试用例集合。定义用于评估 agent-creator skill 的测试提示和预期。

```json
{
  "skill_name": "agent-creator",
  "evals": [
    {
      "id": 1,
      "name": "api-monitor-agent",
      "prompt": "创建一个 API 监控 agent，需要运行 curl 检查端点健康状态",
      "expected_output": "包含正确 frontmatter 和监控工作流的 agent 文件",
      "expectations": [
        "Agent 的 tools 字段包含 Bash（用于 curl）",
        "Agent 的 tools 字段不包含 Edit 或 Write（只读需求）",
        "系统提示包含编号的工作流步骤",
        "Description 包含中英文触发短语"
      ],
      "files": []
    }
  ]
}
```

| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `skill_name` | string | 是 | 被测试的 skill 名称 |
| `evals[].id` | integer | 是 | 唯一标识 |
| `evals[].name` | string | 否 | 描述性名称 |
| `evals[].prompt` | string | 是 | 用户的创建需求 |
| `evals[].expected_output` | string | 是 | 期望结果描述 |
| `evals[].expectations` | string[] | 否 | 可验证的预期标准列表 |
| `evals[].files` | string[] | 否 | 输入文件路径 |

---

## 2. eval_metadata.json

每个测试用例目录下的元数据文件。

```json
{
  "eval_id": 1,
  "eval_name": "api-monitor-agent",
  "prompt": "创建一个 API 监控 agent...",
  "assertions": [
    "Agent 的 tools 字段包含 Bash",
    "系统提示包含编号步骤"
  ]
}
```

---

## 3. grading.json

由 grader agent 生成的评分结果。字段名必须严格遵守以下规范（评估查看器依赖这些字段名）。

```json
{
  "expectations": [
    {
      "text": "Agent 的 tools 字段包含 Bash",
      "passed": true,
      "evidence": "frontmatter 中 tools: Bash, Read, Grep, Glob"
    }
  ],
  "summary": {
    "passed": 4,
    "failed": 1,
    "total": 5,
    "pass_rate": 0.80
  },
  "frontmatter_validation": {
    "name_valid": true,
    "description_quality": "good",
    "tools_appropriate": true,
    "model_appropriate": true,
    "issues": []
  },
  "system_prompt_validation": {
    "has_role_definition": true,
    "has_workflow_steps": true,
    "has_output_format": true,
    "has_boundaries": true,
    "is_focused": true,
    "issues": []
  },
  "claims": [
    {
      "claim": "Agent 能运行 curl 命令",
      "type": "factual",
      "verified": true,
      "evidence": "tools 包含 Bash，系统提示指示使用 curl"
    }
  ],
  "eval_feedback": {
    "suggestions": [],
    "overall": "评估标准覆盖充分"
  }
}
```

**关键字段说明：**

| 字段 | 说明 |
|------|------|
| `expectations[].text` | 原始预期标准文本 |
| `expectations[].passed` | 布尔值：是否通过 |
| `expectations[].evidence` | 支持判定的具体证据 |
| `summary.pass_rate` | 通过率（0.0 ~ 1.0） |
| `frontmatter_validation` | Agent 特有：frontmatter 结构验证 |
| `system_prompt_validation` | Agent 特有：系统提示质量验证 |

---

## 4. timing.json

执行计时数据。在 subagent 任务完成通知中捕获。

```json
{
  "total_tokens": 25376,
  "duration_ms": 101042,
  "total_duration_seconds": 101.0
}
```

---

## 5. comparison.json

由 comparator agent 生成的盲比较结果。

```json
{
  "winner": "A",
  "reasoning": "Agent A 工具权限更精确且 description 包含双语触发词",
  "rubric": {
    "A": {
      "frontmatter": {"tools_match": 5, "description_quality": 5, "model_choice": 4},
      "system_prompt": {"workflow_clarity": 5, "output_format": 4, "boundaries": 5},
      "frontmatter_score": 4.7,
      "system_prompt_score": 4.7,
      "overall_score": 9.4
    },
    "B": {
      "frontmatter": {"tools_match": 3, "description_quality": 2, "model_choice": 4},
      "system_prompt": {"workflow_clarity": 3, "output_format": 3, "boundaries": 2},
      "frontmatter_score": 3.0,
      "system_prompt_score": 2.7,
      "overall_score": 5.7
    }
  },
  "output_quality": {
    "A": {"score": 9, "strengths": [], "weaknesses": []},
    "B": {"score": 6, "strengths": [], "weaknesses": []}
  }
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `winner` | "A" / "B" / "TIE" | 胜出方 |
| `reasoning` | string | 判定理由 |
| `rubric` | object | 按维度的详细评分 |
| `overall_score` | number | 综合分数（1-10） |

---

## 6. benchmark.json

由 `scripts/aggregate_benchmark.py` 生成的汇总统计。

```json
{
  "metadata": {
    "skill_name": "agent-creator",
    "timestamp": "2026-04-10T10:30:00Z",
    "evals_run": [1, 2, 3, 4]
  },
  "runs": [
    {
      "eval_id": 1,
      "eval_name": "api-monitor-agent",
      "configuration": "with_skill",
      "result": {
        "pass_rate": 0.80,
        "passed": 4,
        "failed": 1,
        "total": 5,
        "time_seconds": 101.0,
        "tokens": 25376
      },
      "expectations": [
        {"text": "...", "passed": true, "evidence": "..."}
      ]
    }
  ],
  "run_summary": {
    "with_skill": {
      "pass_rate": {"mean": 0.85, "stddev": 0.05, "min": 0.80, "max": 0.90},
      "time_seconds": {"mean": 95.0, "stddev": 12.0, "min": 80.0, "max": 110.0},
      "tokens": {"mean": 28000, "stddev": 3000, "min": 25000, "max": 32000}
    },
    "without_skill": {
      "pass_rate": {"mean": 0.45, "stddev": 0.10, "min": 0.30, "max": 0.55},
      "time_seconds": {"mean": 82.0, "stddev": 15.0, "min": 65.0, "max": 100.0},
      "tokens": {"mean": 22000, "stddev": 4000, "min": 18000, "max": 27000}
    },
    "delta": {
      "pass_rate": "+0.40",
      "time_seconds": "+13.0",
      "tokens": "+6000"
    }
  },
  "notes": []
}
```

**关键约束：**
- `configuration` 必须为 `"with_skill"` 或 `"without_skill"`
- `result.pass_rate` 在 run 级别，不在顶层
- `expectations` 数组中每个元素必须有 `text`、`passed`、`evidence` 字段

---

## 7. 目录结构

评估工作区的推荐目录结构：

```
<workspace>/
├── iteration-1/
│   ├── eval-1-api-monitor/
│   │   ├── eval_metadata.json
│   │   ├── with_skill/
│   │   │   ├── outputs/
│   │   │   │   └── api-monitor.md
│   │   │   ├── grading.json
│   │   │   └── timing.json
│   │   └── without_skill/
│   │       ├── outputs/
│   │       │   └── api-monitor.md
│   │       ├── grading.json
│   │       └── timing.json
│   ├── eval-2-security-scanner/
│   │   └── ...
│   ├── benchmark.json
│   └── benchmark.md
├── iteration-2/
│   └── ...
└── feedback.json
```

**命名规则：**
- eval 目录使用描述性名称：`eval-1-api-monitor` 而非 `eval-0`
- outputs 目录存放生成的 agent 文件
- 每个 configuration 下独立存放 grading 和 timing

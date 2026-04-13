# Temp - Skill 测试工作区

本文件夹用于存放 skill 测试的用例、输出和报告。支持多轮复用。

## 目录结构

```
temp/
├── README.md              # 本文件
├── test-cases/            # 测试用例定义（JSON + 描述）
├── outputs/               # 各测试用例的实际输出
│   ├── test-1/            # 测试用例 1 的输出
│   ├── test-2/            # 测试用例 2 的输出
│   ├── test-3/            # 测试用例 3 的输出
│   └── test-4/            # 测试用例 4 的输出
├── evals/                 # 评估数据（evals.json, grading 等）
└── reports/               # 检查报告
```

## 使用约定

- 每次测试迭代在 `outputs/` 下按 test-N 组织
- 报告按 `skill名-日期` 命名存放在 `reports/` 下
- `test-cases/` 中的用例可跨迭代复用
- `evals/` 存放结构化评估数据

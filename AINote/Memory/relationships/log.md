---
name: memory_relationships_log
description: wiki 引用关系变更日志
type: reference
---

# Relationships Log — 引用关系变更日志

> 按时间顺序记录所有引用关系的增删改
> 由 ingest/lint 等操作触发自动追加

---

## 更新历史

| 时间 | 页面 | 变化类型 | 详情 |
|------|------|----------|------|
| 2026-04-12 | — | 初始化 | 创建关系追踪系统 |

---

## 变化类型说明

| 类型 | 含义 |
|------|------|
| `add_link` | 新增出站引用 |
| `remove_link` | 删除出站引用 |
| `page_created` | 新页面创建 |
| `page_deleted` | 页面删除 |
| `link_broken` | 引用目标不存在 |
| `link_fixed` | 修复了断链 |

---

> [!tip] 日志格式规范
> 每条记录格式：`## [YYYY-MM-DD HH:mm] {变化类型} | {页面} | {详情}`

---
name: example-api
description: >
  示例：本项目 API 设计规范。当用户编写 API 代码、设计接口、讨论 REST 约定时使用。
  触发场景：API endpoint、RESTful、设计接口、路由定义
paths: "**/api/**/*.ts, **/routes/**"
---

# API 设计规范

本项目使用 RESTful API 设计规范。

## 快速参考

| 资源 | 端点 | 方法 |
|------|------|------|
| 用户 | `/api/users` | GET, POST |
| 单用户 | `/api/users/{id}` | GET, PUT, DELETE |

详细规范见 `references/` 目录。

## REST 约定

### 命名规范

- 使用复数名词：`/users` 而非 `/user`
- 小写字母和连字符：`/user-profiles`
- 嵌套资源限制两层：`/users/{id}/posts`

### HTTP 方法

- GET — 读取资源（幂等、安全）
- POST — 创建资源
- PUT — 完整更新资源
- PATCH — 部分更新资源
- DELETE — 删除资源（幂等）

### 状态码

- 200 OK — 成功
- 201 Created — 创建成功
- 400 Bad Request — 请求错误
- 401 Unauthorized — 未认证
- 403 Forbidden — 无权限
- 404 Not Found — 资源不存在
- 500 Internal Server Error — 服务器错误

## 响应格式

### 成功响应

```json
{
  "data": { ... },
  "meta": { "page": 1, "total": 100 }
}
```

### 错误响应

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input",
    "details": [...]
  }
}
```

详细示例和分页规范见 `references/` 目录。

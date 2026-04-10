# REST API 详细约定

## 分页规范

### 请求参数

```
GET /api/users?page=1&limit=20&sort=name&order=asc
```

| 参数 | 类型 | 说明 |
|------|------|------|
| page | int | 页码，从 1 开始 |
| limit | int | 每页数量，最大 100 |
| sort | string | 排序字段 |
| order | string | 排序方向：asc / desc |

### 响应格式

```json
{
  "data": [...],
  "meta": {
    "page": 1,
    "limit": 20,
    "total": 150,
    "total_pages": 8
  },
  "links": {
    "first": "/api/users?page=1",
    "prev": null,
    "next": "/api/users?page=2",
    "last": "/api/users?page=8"
  }
}
```

## 过滤与搜索

### 过滤参数

```
GET /api/users?status=active&role=admin
```

### 搜索参数

```
GET /api/users?search=john&fields=name,email
```

## 版本控制

### URL 版本

```
/api/v1/users
/api/v2/users
```

### 响应头版本

```
Accept: application/vnd.api+json; version=2.0
```

## 认证

所有需要认证的端点需要在请求头中携带 Token：

```
Authorization: Bearer <token>
```

## 限流

响应头包含限流信息：

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640995200
```

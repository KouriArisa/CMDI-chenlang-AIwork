# API 接口文档

## 1. 基本说明

- 基础路径：`/api/todos/`
- 数据格式：`application/json`
- 字符编码：`UTF-8`
- 响应格式：统一 JSON 包装

统一成功响应结构：

```json
{
  "success": true,
  "code": "SUCCESS",
  "message": "请求成功。",
  "data": {}
}
```

统一失败响应结构：

```json
{
  "success": false,
  "code": "VALIDATION_ERROR",
  "message": "请求参数校验失败。",
  "data": null,
  "errors": {}
}
```

## 2. 枚举值说明

### 2.1 状态 status

| 值 | 含义 |
| --- | --- |
| `pending` | 未完成 |
| `completed` | 已完成 |

### 2.2 优先级 priority

| 值 | 含义 |
| --- | --- |
| `low` | 低 |
| `medium` | 中 |
| `high` | 高 |

## 3. 数据字段说明

单个待办事项对象：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | integer | 主键 ID |
| `title` | string | 标题 |
| `description` | string | 描述 |
| `status` | string | 状态值 |
| `status_label` | string | 状态中文名 |
| `priority` | string | 优先级值 |
| `priority_label` | string | 优先级中文名 |
| `due_date` | string \| null | 截止日期，格式 `YYYY-MM-DD` |
| `completed_at` | string \| null | 完成时间，ISO 8601 |
| `created_at` | string | 创建时间，ISO 8601 |
| `updated_at` | string | 更新时间，ISO 8601 |

## 4. 接口列表

### 4.1 查询待办列表

- 路径：`/api/todos/`
- 方法：`GET`

请求参数：

| 参数 | 必填 | 类型 | 说明 |
| --- | --- | --- | --- |
| `status` | 否 | string | 按状态筛选，取值 `pending` / `completed` |
| `priority` | 否 | string | 按优先级筛选，取值 `low` / `medium` / `high` |

响应示例：

```json
{
  "success": true,
  "code": "SUCCESS",
  "message": "请求成功。",
  "data": {
    "items": [
      {
        "id": 1,
        "title": "整理阶段文档",
        "description": "补齐 API 与部署文档",
        "status": "pending",
        "status_label": "未完成",
        "priority": "high",
        "priority_label": "高",
        "due_date": "2026-03-28",
        "completed_at": null,
        "created_at": "2026-03-24T10:15:00+08:00",
        "updated_at": "2026-03-24T10:15:00+08:00"
      }
    ],
    "count": 1
  }
}
```

### 4.2 创建待办事项

- 路径：`/api/todos/`
- 方法：`POST`

请求体参数：

| 参数 | 必填 | 类型 | 说明 |
| --- | --- | --- | --- |
| `title` | 是 | string | 标题，最长 100 字符 |
| `description` | 否 | string | 描述 |
| `status` | 否 | string | 状态，默认 `pending` |
| `priority` | 否 | string | 优先级，默认 `medium` |
| `due_date` | 否 | string | 截止日期，格式 `YYYY-MM-DD` |

请求示例：

```json
{
  "title": "编写接口文档",
  "description": "补齐阶段 8 文档",
  "priority": "medium",
  "due_date": "2026-03-30"
}
```

响应示例：

```json
{
  "success": true,
  "code": "CREATED",
  "message": "待办事项创建成功。",
  "data": {
    "id": 2,
    "title": "编写接口文档",
    "description": "补齐阶段 8 文档",
    "status": "pending",
    "status_label": "未完成",
    "priority": "medium",
    "priority_label": "中",
    "due_date": "2026-03-30",
    "completed_at": null,
    "created_at": "2026-03-24T10:20:00+08:00",
    "updated_at": "2026-03-24T10:20:00+08:00"
  }
}
```

### 4.3 查询待办详情

- 路径：`/api/todos/{todo_id}/`
- 方法：`GET`

路径参数：

| 参数 | 必填 | 类型 | 说明 |
| --- | --- | --- | --- |
| `todo_id` | 是 | integer | 待办事项 ID |

响应示例：

```json
{
  "success": true,
  "code": "SUCCESS",
  "message": "请求成功。",
  "data": {
    "id": 1,
    "title": "整理阶段文档",
    "description": "补齐 API 与部署文档",
    "status": "pending",
    "status_label": "未完成",
    "priority": "high",
    "priority_label": "高",
    "due_date": "2026-03-28",
    "completed_at": null,
    "created_at": "2026-03-24T10:15:00+08:00",
    "updated_at": "2026-03-24T10:15:00+08:00"
  }
}
```

### 4.4 全量更新待办事项

- 路径：`/api/todos/{todo_id}/`
- 方法：`PUT`

请求体参数：

| 参数 | 必填 | 类型 | 说明 |
| --- | --- | --- | --- |
| `title` | 否 | string | 标题 |
| `description` | 否 | string | 描述 |
| `status` | 否 | string | 状态 |
| `priority` | 否 | string | 优先级 |
| `due_date` | 否 | string | 截止日期，格式 `YYYY-MM-DD` |

说明：

- 当前实现允许只提交部分字段。
- 请求体不能为空。
- 不支持未定义字段。

请求示例：

```json
{
  "title": "完善阶段文档",
  "status": "completed"
}
```

响应示例：

```json
{
  "success": true,
  "code": "SUCCESS",
  "message": "待办事项更新成功。",
  "data": {
    "id": 1,
    "title": "完善阶段文档",
    "description": "补齐 API 与部署文档",
    "status": "completed",
    "status_label": "已完成",
    "priority": "high",
    "priority_label": "高",
    "due_date": "2026-03-28",
    "completed_at": "2026-03-24T10:25:00+08:00",
    "created_at": "2026-03-24T10:15:00+08:00",
    "updated_at": "2026-03-24T10:25:00+08:00"
  }
}
```

### 4.5 部分更新待办事项

- 路径：`/api/todos/{todo_id}/`
- 方法：`PATCH`

请求体参数与 `PUT` 一致，响应结构也一致。

### 4.6 删除待办事项

- 路径：`/api/todos/{todo_id}/`
- 方法：`DELETE`

响应示例：

```json
{
  "success": true,
  "code": "SUCCESS",
  "message": "待办事项删除成功。",
  "data": null
}
```

### 4.7 切换待办状态

- 路径：`/api/todos/{todo_id}/toggle/`
- 方法：`POST`

说明：

- `pending` 会切换为 `completed`
- `completed` 会切换为 `pending`

响应示例：

```json
{
  "success": true,
  "code": "SUCCESS",
  "message": "状态切换成功。",
  "data": {
    "id": 1,
    "title": "完善阶段文档",
    "description": "补齐 API 与部署文档",
    "status": "completed",
    "status_label": "已完成",
    "priority": "high",
    "priority_label": "高",
    "due_date": "2026-03-28",
    "completed_at": "2026-03-24T10:25:00+08:00",
    "created_at": "2026-03-24T10:15:00+08:00",
    "updated_at": "2026-03-24T10:25:00+08:00"
  }
}
```

## 5. 错误码说明

| 错误码 | HTTP 状态码 | 说明 |
| --- | --- | --- |
| `VALIDATION_ERROR` | `400` | 请求参数不合法、字段缺失、字段值非法、包含未知字段 |
| `INVALID_JSON` | `400` | 请求体不是合法 JSON，或 JSON 根节点不是对象 |
| `TODO_NOT_FOUND` | `404` | 指定 ID 的待办事项不存在 |
| `NOT_FOUND` | `404` | API 路径不存在 |
| `INTERNAL_SERVER_ERROR` | `500` | 未处理的服务端异常 |

## 6. 错误响应示例

### 6.1 非法 JSON

```json
{
  "success": false,
  "code": "INVALID_JSON",
  "message": "请求体不是合法的 JSON。",
  "data": null
}
```

### 6.2 参数校验失败

```json
{
  "success": false,
  "code": "VALIDATION_ERROR",
  "message": "请求参数校验失败。",
  "data": null,
  "errors": {
    "title": [
      {
        "message": "This field is required.",
        "code": "required"
      }
    ]
  }
}
```

### 6.3 待办事项不存在

```json
{
  "success": false,
  "code": "TODO_NOT_FOUND",
  "message": "ID 为 9999 的待办事项不存在。",
  "data": null
}
```

# Django 待办事项 CRUD 应用设计文档

## 1. 项目概述

### 1.1 业务场景

本项目选择“待办事项管理”作为业务场景，构建一个基于 Python + Django 的简单 CRUD 应用。

用户可以在系统中创建待办事项、查看待办事项列表、修改待办事项内容、删除待办事项，并根据完成状态管理自己的日常任务。

### 1.2 设计目标

本项目以“简单、清晰、满足考核核心要求”为原则，采用最小可用方案实现：

- 业务场景明确
- 功能点聚焦 CRUD 核心
- 数据模型简洁
- 便于后续用 Django 快速落地

## 2. 功能需求分析

### 2.1 用户角色

当前版本采用单用户模式，不设计注册、登录、权限管理等复杂功能。

系统默认只有一个使用者，重点放在待办事项的增删改查能力上。

### 2.2 功能需求说明

#### 2.2.1 新增待办事项

用户可以创建一条新的待办事项，录入以下信息：

- 标题
- 详细描述
- 截止日期
- 优先级

#### 2.2.2 查看待办事项列表

用户可以查看所有待办事项，并在列表中直观看到：

- 标题
- 当前状态
- 优先级
- 截止日期
- 创建时间

#### 2.2.3 查看待办事项详情

用户可以查看某一条待办事项的完整信息。

#### 2.2.4 修改待办事项

用户可以编辑已有待办事项的内容，包括：

- 标题
- 描述
- 截止日期
- 优先级
- 完成状态

#### 2.2.5 删除待办事项

用户可以删除不再需要的待办事项。

#### 2.2.6 标记完成/未完成

用户可以快速切换待办事项的完成状态，用于日常任务管理。

## 3. 核心功能点

本项目的核心功能点如下：

- 待办事项新增
- 待办事项列表展示
- 待办事项详情查看
- 待办事项编辑
- 待办事项删除
- 待办事项完成状态切换

可选扩展功能如下，但不作为当前版本必做内容：

- 按状态筛选待办事项
- 按优先级排序
- 搜索待办事项

## 4. 技术方案

### 4.1 技术选型

- 后端框架：Django
- 开发语言：Python 3
- 数据库：MySQL 8.0
- 前端方案：Django Template

### 4.2 架构说明

采用 Django 的 MVT 架构：

- Model：定义待办事项数据结构
- View：处理待办事项的业务逻辑
- Template：渲染列表页、详情页、表单页

该方案适合教学和考核场景，开发成本低，结构清晰，易于维护。

### 4.3 数据库实现说明

项目数据库使用 MySQL 8.0，推荐通过 Django ORM + Migration 管理表结构。

如果考核要求同时提交手写 SQL 建表脚本，则使用 `schema/create_todo_item.sql` 中提供的 MySQL 版本脚本。

## 5. 数据模型设计

### 5.1 实体说明

本项目核心实体为 `TodoItem`，用于保存一条待办事项。

### 5.2 字段设计

| 字段名 | 类型 | 是否必填 | 说明 |
| --- | --- | --- | --- |
| id | BigAutoField | 是 | 主键 |
| title | CharField(100) | 是 | 待办事项标题 |
| description | TextField | 否 | 待办事项详细描述 |
| status | CharField(20) | 是 | 状态：pending / completed |
| priority | CharField(20) | 是 | 优先级：low / medium / high |
| due_date | DateField | 否 | 截止日期 |
| completed_at | DateTimeField | 否 | 完成时间 |
| created_at | DateTimeField | 是 | 创建时间 |
| updated_at | DateTimeField | 是 | 更新时间 |

### 5.3 Django Model 设计示例

```python
from django.db import models
from django.db.models import Q


class TodoStatus(models.TextChoices):
    PENDING = "pending", "未完成"
    COMPLETED = "completed", "已完成"


class TodoPriority(models.TextChoices):
    LOW = "low", "低"
    MEDIUM = "medium", "中"
    HIGH = "high", "高"


class TodoItem(models.Model):
    title = models.CharField("标题", max_length=100)
    description = models.TextField("描述", blank=True)
    status = models.CharField(
        "状态",
        max_length=20,
        choices=TodoStatus.choices,
        default=TodoStatus.PENDING,
    )
    priority = models.CharField(
        "优先级",
        max_length=20,
        choices=TodoPriority.choices,
        default=TodoPriority.MEDIUM,
    )
    due_date = models.DateField("截止日期", null=True, blank=True)
    completed_at = models.DateTimeField("完成时间", null=True, blank=True)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        db_table = "todo_item"
        ordering = ["-created_at"]
        constraints = [
            models.CheckConstraint(
                condition=Q(status__in=TodoStatus.values),
                name="todo_item_status_valid",
            ),
            models.CheckConstraint(
                condition=Q(priority__in=TodoPriority.values),
                name="todo_item_priority_valid",
            ),
        ]
        indexes = [
            models.Index(fields=["status"], name="todo_item_status_idx"),
            models.Index(fields=["due_date"], name="todo_item_due_date_idx"),
        ]

    def __str__(self):
        return self.title
```

### 5.4 数据库表结构示意

表名：`todo_item`

| 列名 | 数据类型 | 约束 |
| --- | --- | --- |
| id | bigint | 主键，自增 |
| title | varchar(100) | 非空 |
| description | text | 可空 |
| status | varchar(20) | 非空，默认 `pending` |
| priority | varchar(20) | 非空，默认 `medium` |
| due_date | date | 可空 |
| completed_at | datetime | 可空 |
| created_at | datetime | 非空 |
| updated_at | datetime | 非空 |

## 6. 页面与功能映射

| 页面 | 路径示例 | 功能说明 |
| --- | --- | --- |
| 待办列表页 | `/todos/` | 展示所有待办事项 |
| 新增页 | `/todos/create/` | 创建待办事项 |
| 详情页 | `/todos/<id>/` | 查看待办事项详情 |
| 编辑页 | `/todos/<id>/edit/` | 修改待办事项 |
| 删除页 | `/todos/<id>/delete/` | 删除待办事项 |
| 状态切换 | `/todos/<id>/toggle/` | 切换完成/未完成状态 |

## 7. 基本业务流程

### 7.1 新增流程

1. 用户进入新增页面
2. 填写标题、描述、截止日期、优先级
3. 提交表单
4. 系统保存数据并跳转到待办列表页

### 7.2 修改流程

1. 用户在列表页选择某条待办事项
2. 进入编辑页面
3. 修改内容并提交
4. 系统更新数据并返回详情页或列表页

### 7.3 删除流程

1. 用户在列表页或详情页点击删除
2. 系统进行删除确认
3. 删除成功后返回列表页

## 8. 第一阶段实现范围

为保证项目简单可控，第一阶段只实现以下内容：

- 单用户待办事项 CRUD
- 状态切换
- MySQL 数据存储
- Django 模板页面渲染

暂不实现以下内容：

- 用户登录注册
- 多用户数据隔离
- REST API
- 标签分类
- 文件上传

## 9. 交付物清单

当前第一步已输出以下文件：

- `docs/DESIGN.md`：设计文档
- `schema/todo_item_model.py`：Django 数据模型定义
- `schema/create_todo_item.sql`：MySQL 建表脚本

## 10. 结论

本项目选择“待办事项管理”作为简单 CRUD 应用场景，使用 Django 作为开发框架，能够较好满足课程或考核中对需求分析、功能拆分、数据建模和设计文档输出的要求。

当前设计方案具备以下特点：

- 业务清晰，容易理解
- 功能简单，适合快速实现
- 数据模型稳定，便于直接进入编码阶段
- 符合 Django 项目的标准开发方式

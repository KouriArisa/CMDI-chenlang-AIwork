# Django Todo App

基于 Django + MySQL 的待办事项 CRUD 项目，提供页面端与 JSON API 两套访问方式，适合作为课程作业、考核项目和后续功能扩展的基础骨架。

## 项目简介

本项目实现了一个简单的待办事项管理系统，支持以下能力：

- 待办事项新增、查询、修改、删除
- 待办事项状态切换
- 页面端 CRUD 操作
- 统一结构的 JSON API 响应
- 基于服务层与仓储层的解耦设计

## 技术栈

- Python 3.13
- Django 5.2
- MySQL 8.0
- mysqlclient 2.2
- python-dotenv 1.0+
- Ruff / Black

## 快速启动

### 1. 创建虚拟环境

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
```

### 2. 配置环境变量

```bash
cp .env.example .env
```

请至少修改以下配置：

- `DJANGO_SECRET_KEY`
- `MYSQL_DATABASE`
- `MYSQL_USER`
- `MYSQL_PASSWORD`
- `MYSQL_HOST`
- `MYSQL_PORT`

### 3. 初始化数据库

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 4. 启动项目

```bash
python manage.py runserver
```

启动后可访问：

- 页面端：`http://127.0.0.1:8000/todos/`
- API：`http://127.0.0.1:8000/api/todos/`
- 管理后台：`http://127.0.0.1:8000/admin/`

## 目录结构

```text
.
├── apps/
│   └── todos/
│       ├── api/              # JSON API 视图、表单、响应
│       ├── contracts/        # 接口定义与 DTO
│       ├── repositories/     # 仓储层实现
│       ├── services/         # 业务服务层
│       ├── tests/            # 单元测试与集成测试
│       ├── forms.py          # 页面表单
│       ├── models.py         # Django 模型
│       ├── urls.py           # 页面路由
│       └── views.py          # 页面视图
├── config/
│   ├── settings/             # Django 配置
│   ├── middleware.py         # API 异常处理中间件
│   └── urls.py               # 全局路由
├── docs/
│   ├── API.md                # API 接口文档
│   ├── DEPLOY.md             # 部署文档
│   ├── DESIGN.md             # 设计文档
│   ├── ENV_SETUP.md          # 环境搭建文档
│   ├── OPTIMIZATION.md       # 阶段 7 优化说明
│   └── REFACTOR.md           # 阶段 6 重构说明
├── schema/                   # 数据模型定义与建表脚本
├── static/                   # 静态资源
├── templates/                # 页面模板
├── .env.example
├── manage.py
├── requirements.txt
└── requirements-dev.txt
```

## 文档索引

- API 文档：`docs/API.md`
- 部署文档：`docs/DEPLOY.md`
- 环境搭建：`docs/ENV_SETUP.md`
- 设计文档：`docs/DESIGN.md`

## 常用命令

```bash
python manage.py test --settings=config.settings.test
ruff check .
python -m compileall manage.py config apps schema
```

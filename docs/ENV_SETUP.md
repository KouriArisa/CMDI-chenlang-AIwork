# 环境搭建文档

## 1. 环境要求

- Python 3.13
- MySQL 8.0
- pip 24+
- 建议使用虚拟环境 `.venv`

## 2. 创建虚拟环境

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
```

如果安装 `mysqlclient` 失败，通常是本机缺少 MySQL 开发库。macOS 可先尝试：

```bash
brew install mysql pkg-config
```

## 3. 创建 MySQL 数据库

登录 MySQL 后执行：

```sql
CREATE DATABASE todo_app
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

CREATE USER 'todo_user'@'localhost' IDENTIFIED BY 'change-this-password';
GRANT ALL PRIVILEGES ON todo_app.* TO 'todo_user'@'localhost';
FLUSH PRIVILEGES;
```

如果你使用的是远程数据库或 Docker 中的 MySQL，请把连接信息同步写入 `.env`。

## 4. 配置环境变量

复制示例配置：

```bash
cp .env.example .env
```

项目已通过 `python-dotenv` 自动加载根目录下的 `.env` 文件，无需手动执行额外导出命令。

建议至少检查以下变量：

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG`
- `DJANGO_ALLOWED_HOSTS`
- `MYSQL_DATABASE`
- `MYSQL_USER`
- `MYSQL_PASSWORD`
- `MYSQL_HOST`
- `MYSQL_PORT`

## 5. 初始化 Django 项目

```bash
source .venv/bin/activate
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

启动后访问：

- 应用首页：`http://127.0.0.1:8000/`
- 管理后台：`http://127.0.0.1:8000/admin/`

## 6. 常用开发命令

```bash
source .venv/bin/activate
python manage.py test
ruff check .
black --check .
```

## 7. 目录说明

- `apps/todos/`：待办事项业务代码
- `config/settings/`：Django 配置
- `templates/`：页面模板
- `static/`：静态资源
- `docs/`：设计与环境文档
- `schema/`：提交用模型定义与 SQL 脚本

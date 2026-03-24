# 部署文档

## 1. 部署方式

本项目支持两种部署方式：

- Docker Compose 容器化部署
- Linux 单机部署（Gunicorn + Nginx + systemd）

如果你只是为了快速启动项目，优先使用 Docker Compose。

## 2. Docker Compose 部署

### 2.1 准备环境变量

复制示例配置：

```bash
cp .env.example .env
```

建议至少修改以下变量：

- `DJANGO_SECRET_KEY`
- `MYSQL_PASSWORD`
- `MYSQL_ROOT_PASSWORD`
- `DJANGO_ALLOWED_HOSTS`

### 2.2 启动服务

```bash
docker compose up --build -d
```

启动后可访问：

- 页面端：`http://127.0.0.1:8000/todos/`
- API：`http://127.0.0.1:8000/api/todos/`
- 健康检查：`http://127.0.0.1:8000/health/`

### 2.3 停止服务

```bash
docker compose down
```

如果你还想删除数据库卷：

```bash
docker compose down -v
```

### 2.4 容器化结构说明

- `Dockerfile`
  - 使用多阶段构建
  - 构建阶段安装编译依赖并打 wheel
  - 运行阶段只保留运行时依赖
  - 内置 HTTP 健康检查

- `docker-compose.yml`
  - `app`：Django 应用容器
  - `db`：MySQL 8.4 数据库容器
  - 数据库健康检查通过后再启动应用

- `scripts/start.sh`
  - 启动前检测关键环境变量
  - 等待数据库可用
  - 自动执行 `migrate` 与 `collectstatic`
  - 启动 Gunicorn

## 3. Linux 单机部署

### 3.1 服务器准备

安装系统依赖：

```bash
sudo apt update
sudo apt install -y python3.13 python3.13-venv python3-pip pkg-config default-libmysqlclient-dev nginx
```

如果你的发行版没有 `python3.13` 包，请改用服务器已有的 Python 3.13 可执行文件。

### 3.2 获取项目代码

```bash
mkdir -p /srv/django-todo
cd /srv/django-todo
git clone <your-repo-url> app
cd app
```

### 3.3 创建虚拟环境并安装依赖

```bash
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3.4 配置 MySQL

登录 MySQL 后执行：

```sql
CREATE DATABASE todo_app
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

CREATE USER 'todo_user'@'127.0.0.1' IDENTIFIED BY 'replace-with-strong-password';
GRANT ALL PRIVILEGES ON todo_app.* TO 'todo_user'@'127.0.0.1';
FLUSH PRIVILEGES;
```

### 3.5 配置环境变量

复制并编辑环境文件：

```bash
cp .env.example .env
```

建议生产环境至少配置为：

```dotenv
DJANGO_SETTINGS_MODULE=config.settings.local
DJANGO_SECRET_KEY=replace-with-strong-secret-key
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=your-domain.com,server-ip

MYSQL_DATABASE=todo_app
MYSQL_USER=todo_user
MYSQL_PASSWORD=replace-with-strong-password
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
```

说明：

- `MYSQL_PASSWORD` 不能保留为示例占位值，否则 Django 启动会被拒绝
- `DJANGO_ALLOWED_HOSTS` 必须包含实际域名或服务器 IP

### 3.6 初始化数据库与静态资源

```bash
source .venv/bin/activate
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

### 3.7 测试 Gunicorn 启动

```bash
source .venv/bin/activate
gunicorn config.wsgi:application --bind 127.0.0.1:8000
```

确认浏览器可通过反向代理访问前，再进入 systemd 配置。

### 3.8 配置 systemd

创建 `/etc/systemd/system/django-todo.service`：

```ini
[Unit]
Description=Django Todo App
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/srv/django-todo/app
Environment="PATH=/srv/django-todo/app/.venv/bin"
ExecStart=/srv/django-todo/app/.venv/bin/gunicorn config.wsgi:application --bind 127.0.0.1:8000
Restart=always

[Install]
WantedBy=multi-user.target
```

启动服务：

```bash
sudo systemctl daemon-reload
sudo systemctl enable django-todo
sudo systemctl start django-todo
sudo systemctl status django-todo
```

### 3.9 配置 Nginx

创建 `/etc/nginx/sites-available/django-todo`：

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location /static/ {
        alias /srv/django-todo/app/staticfiles/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

启用配置：

```bash
sudo ln -s /etc/nginx/sites-available/django-todo /etc/nginx/sites-enabled/django-todo
sudo nginx -t
sudo systemctl reload nginx
```

### 3.10 发布后检查

建议依次检查：

- `systemctl status django-todo`
- `sudo journalctl -u django-todo -n 100`
- `sudo nginx -t`
- `curl http://127.0.0.1:8000/health/`
- 浏览器访问首页 `/todos/`

## 4. 常见问题

### 4.1 `mysqlclient` 安装失败

缺少 MySQL 开发库或 `pkg-config`。在 Debian/Ubuntu 可执行：

```bash
sudo apt install -y pkg-config default-libmysqlclient-dev
```

### 4.2 启动时报 `MYSQL_PASSWORD is still set to the example placeholder`

说明 `.env` 中仍然保留了示例密码，占位值需要替换成真实密码。

### 4.3 静态资源 404

通常是以下原因之一：

- 没有执行 `python manage.py collectstatic --noinput`
- Nginx `alias` 路径与 `STATIC_ROOT` 不一致
- Nginx 没有重新加载

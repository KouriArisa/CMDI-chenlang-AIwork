# Django Todo App

一个基于 Django + MySQL 的待办事项 CRUD 项目骨架，适合作为课程作业、考核项目或后续功能迭代的起点。

## 当前项目结构

```text
.
├── AGENTS.md
├── CLAUDE.md
├── apps/
│   └── todos/
├── config/
│   └── settings/
├── docs/
│   ├── DESIGN.md
│   └── ENV_SETUP.md
├── schema/
├── static/
├── templates/
├── .env.example
├── manage.py
├── pyproject.toml
├── requirements.txt
└── requirements-dev.txt
```

## 快速开始

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```

更完整的环境配置步骤见 `docs/ENV_SETUP.md`。

# 阶段 6 重构说明

## 1. 重构目标

本次重构围绕“面向接口编程”和“依赖注入”展开，目标是降低 Django ORM、视图层、业务层之间的直接耦合，形成更清晰的分层结构。

## 2. 重构前问题

- 页面视图 `apps/todos/views.py` 直接依赖 `TodoItem` 模型和 Django 通用 Model View。
- 服务接口与仓储接口直接暴露 Django `TodoItem`，抽象层泄漏了基础设施实现。
- API 层已有服务注入能力，但页面层没有接入同一套依赖注入方案。
- 页面表单使用 `ModelForm`，页面提交流程仍然直接耦合 ORM。

## 3. 重构后结构

### 3.1 接口与 DTO

- `apps/todos/contracts/dto.py`
  - 新增 `TodoData`，作为跨层传输对象。
  - 保留 `TodoQuery` 作为查询参数对象。

- `apps/todos/contracts/repositories.py`
  - 仓储接口改为返回 `TodoData`，不再暴露 Django Model。

- `apps/todos/contracts/services.py`
  - 服务接口改为返回 `TodoData`，进一步隔离上层模块与 ORM。

### 3.2 依赖注入

- `apps/todos/mixins.py`
  - 提取 `TodoServiceResolverMixin`，统一管理 service resolver。

- `apps/todos/dependencies.py`
  - 继续作为依赖注入入口，负责创建具体仓储与服务实例。

### 3.3 解耦结果

- `apps/todos/repositories/todo_repository.py`
  - 具体仓储负责 ORM 查询与 DTO 映射。

- `apps/todos/services/todo_service.py`
  - 服务层只依赖仓储接口，不直接操作 ORM。

- `apps/todos/views.py`
  - 页面视图改为依赖服务接口，不再直接操作 `TodoItem`。

- `apps/todos/forms.py`
  - 页面表单改为普通 `Form`，不再依赖 `ModelForm`。

## 4. 验证结果

本次重构后已执行以下验证：

- `ruff check .`
- `python -m compileall manage.py config apps schema`
- `python manage.py test --settings=config.settings.test`

## 5. 重构收益

- 视图层与 ORM 解耦，更容易替换存储实现。
- 服务层可通过假仓储进行单元测试，依赖注入链路更清晰。
- API 层和页面层统一走服务接口，架构风格一致。
- DTO 作为跨层契约，降低模块之间的隐式依赖。

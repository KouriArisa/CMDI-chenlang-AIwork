# 阶段 7 优化说明

## 1. 审查结果

本轮主要检查了以下问题：

- AI 味代码：过于泛化的命名，如 `data`
- 代码坏味道：重复字段定义、重复测试替身、同请求内重复查询
- 魔法值：日期格式、空选项值等硬编码

## 2. 优化内容

### 2.1 收敛表单重复代码

文件：[apps/todos/api/forms.py](/Users/kouriarisa/code_space/CMDI-chenlang-AIwork/apps/todos/api/forms.py)

- 提取 `BaseTodoPayloadForm`，复用创建/更新表单的公共字段与校验逻辑
- 提取 `DATE_INPUT_FORMAT`、`EMPTY_CHOICE` 常量
- 把校验函数参数从泛化命名 `data` / `name` 调整为更具体的 `submitted_data` / `field_name`

### 2.2 优化接口与仓储命名

文件：

- [apps/todos/contracts/repositories.py](/Users/kouriarisa/code_space/CMDI-chenlang-AIwork/apps/todos/contracts/repositories.py)
- [apps/todos/repositories/todo_repository.py](/Users/kouriarisa/code_space/CMDI-chenlang-AIwork/apps/todos/repositories/todo_repository.py)
- [apps/todos/services/todo_service.py](/Users/kouriarisa/code_space/CMDI-chenlang-AIwork/apps/todos/services/todo_service.py)

- 将泛化命名 `data` 改为 `attributes` / `changes`
- 将 `_build_create_data` 改为 `_build_create_attributes`
- 减少阅读时对“这是创建属性还是更新字段”的歧义

### 2.3 减少页面层重复查询

文件：[apps/todos/views.py](/Users/kouriarisa/code_space/CMDI-chenlang-AIwork/apps/todos/views.py)

- 在 `TodoLookupMixin` 中引入 `cached_property`
- 详情、编辑、删除页面在单次请求中复用同一个 `todo`
- 避免 `get_initial()` 与 `get_context_data()` 重复调用服务层

### 2.4 清理测试重复代码

文件：

- [apps/todos/tests/fakes.py](/Users/kouriarisa/code_space/CMDI-chenlang-AIwork/apps/todos/tests/fakes.py)
- [apps/todos/tests/test_dependency_injection.py](/Users/kouriarisa/code_space/CMDI-chenlang-AIwork/apps/todos/tests/test_dependency_injection.py)
- [apps/todos/tests/test_web_views.py](/Users/kouriarisa/code_space/CMDI-chenlang-AIwork/apps/todos/tests/test_web_views.py)

- 提取共享 `FakeTodoService`
- 删除两份重复的测试替身定义

## 3. 验证结果

已执行并通过：

- `ruff check .`
- `python3 -m compileall manage.py config apps schema`
- `python3 manage.py test --settings=config.settings.test`

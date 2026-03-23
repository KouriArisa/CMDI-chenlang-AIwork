# Claude 协作约定

## 技术栈及版本

- Python 3.13
- Django 5.2
- MySQL 8.0
- mysqlclient 2.2
- Django Template

## 编码规范

- 保持模块职责单一，优先复用 Django 官方推荐结构。
- 表单校验写在 `forms.py`，模型约束写在 `models.py`，路由聚合在 `urls.py`。
- 新增文件默认使用 ASCII；仅在中文文案、模板展示中使用中文。
- 不添加未说明的降级逻辑、模拟数据或静默 fallback。

## 输出约定

- 回答与提交说明默认使用中文。
- 涉及命令时给出可直接执行的命令。
- 涉及配置修改时，明确说明影响的环境变量或依赖文件。

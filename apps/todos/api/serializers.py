from apps.todos.models import TodoItem


def serialize_todo(todo: TodoItem) -> dict[str, object]:
    return {
        "id": todo.id,
        "title": todo.title,
        "description": todo.description,
        "status": todo.status,
        "status_label": todo.get_status_display(),
        "priority": todo.priority,
        "priority_label": todo.get_priority_display(),
        "due_date": _serialize_date(todo.due_date),
        "completed_at": _serialize_datetime(todo.completed_at),
        "created_at": _serialize_datetime(todo.created_at),
        "updated_at": _serialize_datetime(todo.updated_at),
    }


def serialize_todo_list(todos: list[TodoItem]) -> list[dict[str, object]]:
    return [serialize_todo(todo) for todo in todos]


def _serialize_date(value) -> str | None:
    if value is None:
        return None
    return value.isoformat()


def _serialize_datetime(value) -> str | None:
    if value is None:
        return None
    return value.isoformat()

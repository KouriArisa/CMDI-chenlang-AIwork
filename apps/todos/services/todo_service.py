from collections.abc import Mapping
from typing import Any

from apps.todos.contracts.dto import TodoData, TodoQuery
from apps.todos.contracts.repositories import TodoRepository
from apps.todos.exceptions import TodoNotFoundError
from apps.todos.models import TodoPriority, TodoStatus


class DefaultTodoService:
    def __init__(self, *, repository: TodoRepository) -> None:
        self._repository = repository

    def list_todos(self, *, query: TodoQuery) -> list[TodoData]:
        return self._repository.list(query=query)

    def get_todo(self, *, todo_id: int) -> TodoData:
        return self._get_or_raise(todo_id=todo_id)

    def create_todo(self, *, payload: Mapping[str, Any]) -> TodoData:
        data = self._build_create_data(payload=payload)
        return self._repository.create(data=data)

    def update_todo(self, *, todo_id: int, payload: Mapping[str, Any]) -> TodoData:
        self._get_or_raise(todo_id=todo_id)
        return self._repository.update(todo_id=todo_id, data=dict(payload))

    def delete_todo(self, *, todo_id: int) -> None:
        self._get_or_raise(todo_id=todo_id)
        self._repository.delete(todo_id=todo_id)

    def toggle_status(self, *, todo_id: int) -> TodoData:
        todo = self._get_or_raise(todo_id=todo_id)
        next_status = self._get_next_status(current_status=todo.status)
        return self._repository.update(todo_id=todo_id, data={"status": next_status})

    def _build_create_data(self, *, payload: Mapping[str, Any]) -> dict[str, Any]:
        data = dict(payload)
        data.setdefault("description", "")
        data["status"] = data.get("status") or TodoStatus.PENDING
        data["priority"] = data.get("priority") or TodoPriority.MEDIUM
        return data

    def _get_or_raise(self, *, todo_id: int) -> TodoData:
        todo = self._repository.get_by_id(todo_id=todo_id)
        if todo is None:
            raise TodoNotFoundError(todo_id=todo_id)
        return todo

    def _get_next_status(self, *, current_status: str) -> str:
        if current_status == TodoStatus.PENDING:
            return TodoStatus.COMPLETED
        return TodoStatus.PENDING

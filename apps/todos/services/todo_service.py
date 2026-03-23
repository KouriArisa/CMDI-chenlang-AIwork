from collections.abc import Mapping
from typing import Any

from apps.todos.contracts.dto import TodoQuery
from apps.todos.contracts.repositories import TodoRepository
from apps.todos.exceptions import TodoNotFoundError
from apps.todos.models import TodoItem, TodoPriority, TodoStatus


class DefaultTodoService:
    def __init__(self, *, repository: TodoRepository) -> None:
        self._repository = repository

    def list_todos(self, *, query: TodoQuery) -> list[TodoItem]:
        filters = self._build_filters(query=query)
        return self._repository.list(filters=filters)

    def get_todo(self, *, todo_id: int) -> TodoItem:
        return self._get_or_raise(todo_id=todo_id)

    def create_todo(self, *, payload: Mapping[str, Any]) -> TodoItem:
        data = self._build_create_data(payload=payload)
        return self._repository.create(data=data)

    def update_todo(self, *, todo_id: int, payload: Mapping[str, Any]) -> TodoItem:
        todo = self._get_or_raise(todo_id=todo_id)
        return self._repository.update(todo=todo, data=dict(payload))

    def delete_todo(self, *, todo_id: int) -> None:
        todo = self._get_or_raise(todo_id=todo_id)
        self._repository.delete(todo=todo)

    def toggle_status(self, *, todo_id: int) -> TodoItem:
        todo = self._get_or_raise(todo_id=todo_id)
        next_status = self._get_next_status(current_status=todo.status)
        return self._repository.update(todo=todo, data={"status": next_status})

    def _build_filters(self, *, query: TodoQuery) -> dict[str, str]:
        filters: dict[str, str] = {}
        if query.status:
            filters["status"] = query.status
        if query.priority:
            filters["priority"] = query.priority
        return filters

    def _build_create_data(self, *, payload: Mapping[str, Any]) -> dict[str, Any]:
        data = dict(payload)
        data.setdefault("description", "")
        data["status"] = data.get("status") or TodoStatus.PENDING
        data["priority"] = data.get("priority") or TodoPriority.MEDIUM
        return data

    def _get_or_raise(self, *, todo_id: int) -> TodoItem:
        todo = self._repository.get_by_id(todo_id=todo_id)
        if todo is None:
            raise TodoNotFoundError(todo_id=todo_id)
        return todo

    def _get_next_status(self, *, current_status: str) -> str:
        if current_status == TodoStatus.PENDING:
            return TodoStatus.COMPLETED
        return TodoStatus.PENDING

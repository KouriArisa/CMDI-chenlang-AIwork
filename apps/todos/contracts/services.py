from collections.abc import Callable, Mapping
from typing import Any, Protocol

from apps.todos.contracts.dto import TodoQuery
from apps.todos.models import TodoItem


class TodoService(Protocol):
    def list_todos(self, *, query: TodoQuery) -> list[TodoItem]: ...

    def get_todo(self, *, todo_id: int) -> TodoItem: ...

    def create_todo(self, *, payload: Mapping[str, Any]) -> TodoItem: ...

    def update_todo(self, *, todo_id: int, payload: Mapping[str, Any]) -> TodoItem: ...

    def delete_todo(self, *, todo_id: int) -> None: ...

    def toggle_status(self, *, todo_id: int) -> TodoItem: ...


TodoServiceResolver = Callable[[], TodoService]

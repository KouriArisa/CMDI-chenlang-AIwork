from collections.abc import Callable, Mapping
from typing import Any, Protocol

from apps.todos.contracts.dto import TodoData, TodoQuery


class TodoService(Protocol):
    def list_todos(self, *, query: TodoQuery) -> list[TodoData]: ...

    def get_todo(self, *, todo_id: int) -> TodoData: ...

    def create_todo(self, *, payload: Mapping[str, Any]) -> TodoData: ...

    def update_todo(self, *, todo_id: int, payload: Mapping[str, Any]) -> TodoData: ...

    def delete_todo(self, *, todo_id: int) -> None: ...

    def toggle_status(self, *, todo_id: int) -> TodoData: ...


TodoServiceResolver = Callable[[], TodoService]

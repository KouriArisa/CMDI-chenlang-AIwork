from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from apps.todos.contracts.dto import TodoData, TodoQuery
from apps.todos.contracts.repositories import TodoRepository
from apps.todos.models import TodoItem


class DjangoTodoRepository(TodoRepository):
    def list(self, *, query: TodoQuery) -> list[TodoData]:
        queryset = self._apply_query(query=query)
        return [self._to_data(todo) for todo in queryset]

    def get_by_id(self, *, todo_id: int) -> TodoData | None:
        todo = TodoItem.objects.filter(pk=todo_id).first()
        if todo is None:
            return None
        return self._to_data(todo)

    def create(self, *, attributes: Mapping[str, Any]) -> TodoData:
        todo = TodoItem.objects.create(**dict(attributes))
        return self._to_data(todo)

    def update(self, *, todo_id: int, changes: Mapping[str, Any]) -> TodoData:
        todo = TodoItem.objects.get(pk=todo_id)
        updated_fields = []
        for field_name, field_value in changes.items():
            setattr(todo, field_name, field_value)
            updated_fields.append(field_name)
        todo.save(update_fields=self._build_update_fields(updated_fields=updated_fields))
        todo.refresh_from_db()
        return self._to_data(todo)

    def delete(self, *, todo_id: int) -> None:
        TodoItem.objects.filter(pk=todo_id).delete()

    def _apply_query(self, *, query: TodoQuery):
        queryset = TodoItem.objects.all()
        if query.status:
            queryset = queryset.filter(status=query.status)
        if query.priority:
            queryset = queryset.filter(priority=query.priority)
        return queryset

    def _build_update_fields(self, *, updated_fields: list[str]) -> list[str]:
        fields = set(updated_fields)
        fields.add("updated_at")
        if "status" in fields:
            fields.add("completed_at")
        return sorted(fields)

    def _to_data(self, todo: TodoItem) -> TodoData:
        return TodoData(
            id=todo.id,
            title=todo.title,
            description=todo.description,
            status=todo.status,
            status_label=todo.get_status_display(),
            priority=todo.priority,
            priority_label=todo.get_priority_display(),
            due_date=todo.due_date,
            completed_at=todo.completed_at,
            created_at=todo.created_at,
            updated_at=todo.updated_at,
        )

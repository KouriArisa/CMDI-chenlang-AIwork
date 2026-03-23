from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from apps.todos.contracts.repositories import TodoRepository
from apps.todos.models import TodoItem


class DjangoTodoRepository(TodoRepository):
    def list(self, *, filters: Mapping[str, Any]) -> list[TodoItem]:
        queryset = TodoItem.objects.all()
        if filters.get("status"):
            queryset = queryset.filter(status=filters["status"])
        if filters.get("priority"):
            queryset = queryset.filter(priority=filters["priority"])
        return list(queryset)

    def get_by_id(self, *, todo_id: int) -> TodoItem | None:
        return TodoItem.objects.filter(pk=todo_id).first()

    def create(self, *, data: Mapping[str, Any]) -> TodoItem:
        return TodoItem.objects.create(**dict(data))

    def update(self, *, todo: TodoItem, data: Mapping[str, Any]) -> TodoItem:
        updated_fields = []
        for field_name, field_value in data.items():
            setattr(todo, field_name, field_value)
            updated_fields.append(field_name)
        todo.save(update_fields=self._build_update_fields(updated_fields=updated_fields))
        return todo

    def delete(self, *, todo: TodoItem) -> None:
        todo.delete()

    def _build_update_fields(self, *, updated_fields: list[str]) -> list[str]:
        fields = set(updated_fields)
        fields.add("updated_at")
        if "status" in fields:
            fields.add("completed_at")
        return sorted(fields)

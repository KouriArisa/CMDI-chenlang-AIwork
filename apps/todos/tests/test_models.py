from django.test import TestCase

from apps.todos.models import TodoItem, TodoStatus


class TodoItemModelTests(TestCase):
    def test_completed_status_sets_completed_at(self):
        todo = TodoItem.objects.create(
            title="完成 Django 项目骨架",
            status=TodoStatus.COMPLETED,
        )

        self.assertIsNotNone(todo.completed_at)

    def test_pending_status_clears_completed_at(self):
        todo = TodoItem.objects.create(
            title="整理需求",
            status=TodoStatus.COMPLETED,
        )
        todo.status = TodoStatus.PENDING
        todo.save()

        self.assertIsNone(todo.completed_at)

import json

from django.test import TestCase
from django.urls import reverse

from apps.todos.models import TodoItem, TodoPriority, TodoStatus


class TodoApiTests(TestCase):
    def setUp(self) -> None:
        self.list_url = reverse("todo_api:list_create")
        self.todo = TodoItem.objects.create(
            title="整理接口需求",
            description="补齐分层架构",
            priority=TodoPriority.HIGH,
        )

    def test_list_api_returns_unified_payload(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertTrue(body["success"])
        self.assertEqual(body["data"]["count"], 1)
        self.assertEqual(body["data"]["items"][0]["id"], self.todo.id)

    def test_create_api_creates_todo(self):
        payload = {
            "title": "编写 CRUD API",
            "description": "返回统一 JSON",
            "priority": TodoPriority.MEDIUM,
        }

        response = self.client.post(
            self.list_url,
            data=json.dumps(payload),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        body = response.json()
        self.assertEqual(body["code"], "CREATED")
        self.assertEqual(TodoItem.objects.count(), 2)

    def test_detail_api_returns_single_todo(self):
        response = self.client.get(self._detail_url(todo_id=self.todo.id))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["data"]["title"], self.todo.title)

    def test_update_api_updates_todo(self):
        payload = {"title": "整理接口测试", "status": TodoStatus.COMPLETED}

        response = self.client.patch(
            self._detail_url(todo_id=self.todo.id),
            data=json.dumps(payload),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.todo.refresh_from_db()
        self.assertEqual(self.todo.title, "整理接口测试")
        self.assertEqual(self.todo.status, TodoStatus.COMPLETED)
        self.assertIsNotNone(self.todo.completed_at)

    def test_delete_api_deletes_todo(self):
        response = self.client.delete(self._detail_url(todo_id=self.todo.id))

        self.assertEqual(response.status_code, 200)
        self.assertFalse(TodoItem.objects.filter(pk=self.todo.id).exists())

    def test_toggle_api_switches_status(self):
        response = self.client.post(self._toggle_url(todo_id=self.todo.id))

        self.assertEqual(response.status_code, 200)
        self.todo.refresh_from_db()
        self.assertEqual(self.todo.status, TodoStatus.COMPLETED)

    def test_not_found_returns_unified_error(self):
        response = self.client.get(self._detail_url(todo_id=9999))

        self.assertEqual(response.status_code, 404)
        body = response.json()
        self.assertFalse(body["success"])
        self.assertEqual(body["code"], "TODO_NOT_FOUND")

    def test_invalid_json_returns_unified_error(self):
        response = self.client.post(
            self.list_url,
            data="{invalid-json",
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["code"], "INVALID_JSON")

    def _detail_url(self, *, todo_id: int) -> str:
        return reverse("todo_api:detail", kwargs={"todo_id": todo_id})

    def _toggle_url(self, *, todo_id: int) -> str:
        return reverse("todo_api:toggle", kwargs={"todo_id": todo_id})

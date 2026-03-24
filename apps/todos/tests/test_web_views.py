from django.test import RequestFactory, SimpleTestCase, TestCase
from django.urls import reverse

from apps.todos.models import TodoItem, TodoPriority, TodoStatus
from apps.todos.tests.fakes import FakeTodoService
from apps.todos.views import TodoListView


class TodoWebDependencyInjectionTests(SimpleTestCase):
    def test_list_view_uses_injected_service_resolver(self):
        factory = RequestFactory()
        fake_service = FakeTodoService()
        view = TodoListView.as_view(service_resolver=lambda: fake_service)

        response = view(factory.get("/todos/"))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(fake_service.list_called)


class TodoWebViewTests(TestCase):
    def setUp(self) -> None:
        self.todo = TodoItem.objects.create(
            title="整理页面视图",
            description="接入服务层",
            priority=TodoPriority.HIGH,
        )

    def test_list_page_renders_service_backed_data(self):
        response = self.client.get(reverse("todos:list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.todo.title)

    def test_detail_page_renders_todo(self):
        response = self.client.get(reverse("todos:detail", kwargs={"pk": self.todo.id}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.todo.description)

    def test_update_page_updates_todo(self):
        payload = {
            "title": "整理页面依赖注入",
            "description": "重构页面层",
            "status": self.todo.status,
            "priority": self.todo.priority,
            "due_date": "",
        }

        response = self.client.post(
            reverse("todos:edit", kwargs={"pk": self.todo.id}),
            data=payload,
        )

        self.assertEqual(response.status_code, 302)
        self.todo.refresh_from_db()
        self.assertEqual(self.todo.title, "整理页面依赖注入")

    def test_toggle_view_redirects_after_service_call(self):
        response = self.client.post(
            reverse("todos:toggle", kwargs={"pk": self.todo.id}),
        )

        self.assertEqual(response.status_code, 302)
        self.todo.refresh_from_db()
        self.assertEqual(response.headers["Location"], reverse("todos:list"))
        self.assertEqual(self.todo.status, TodoStatus.COMPLETED)

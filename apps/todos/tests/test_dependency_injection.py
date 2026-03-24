from django.test import RequestFactory, SimpleTestCase

from apps.todos.api.views import TodoCollectionApiView


class FakeTodoService:
    def __init__(self) -> None:
        self.list_called = False

    def list_todos(self, *, query):
        self.list_called = True
        return []

    def get_todo(self, *, todo_id: int):
        raise NotImplementedError

    def create_todo(self, *, payload):
        raise NotImplementedError

    def update_todo(self, *, todo_id: int, payload):
        raise NotImplementedError

    def delete_todo(self, *, todo_id: int):
        raise NotImplementedError

    def toggle_status(self, *, todo_id: int):
        raise NotImplementedError


class TodoApiDependencyInjectionTests(SimpleTestCase):
    def test_collection_view_uses_injected_service_resolver(self):
        factory = RequestFactory()
        fake_service = FakeTodoService()
        view = TodoCollectionApiView.as_view(
            service_resolver=lambda: fake_service,
        )

        response = view(factory.get("/api/todos/"))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(fake_service.list_called)

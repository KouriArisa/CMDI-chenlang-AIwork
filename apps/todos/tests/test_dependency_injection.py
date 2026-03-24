from django.test import RequestFactory, SimpleTestCase

from apps.todos.api.views import TodoCollectionApiView
from apps.todos.tests.fakes import FakeTodoService


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

from django.core.exceptions import ImproperlyConfigured

from apps.todos.contracts.services import TodoService, TodoServiceResolver


class TodoServiceResolverMixin:
    service_resolver: TodoServiceResolver | None = None
    service: TodoService

    def dispatch(self, request, *args, **kwargs):
        self.service = self._resolve_service()
        return super().dispatch(request, *args, **kwargs)

    def _resolve_service(self) -> TodoService:
        if self.service_resolver is None:
            raise ImproperlyConfigured("Todo service resolver is not configured.")
        return self.service_resolver()

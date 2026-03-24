import json
from http import HTTPStatus

from django import forms
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpRequest, QueryDict
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from apps.todos.api.forms import TodoCreateForm, TodoListQueryForm, TodoUpdateForm
from apps.todos.api.responses import success_response
from apps.todos.api.serializers import serialize_todo, serialize_todo_list
from apps.todos.contracts.dto import TodoQuery
from apps.todos.contracts.services import TodoService, TodoServiceResolver
from apps.todos.exceptions import InvalidJSONError, RequestValidationError


@method_decorator(csrf_exempt, name="dispatch")
class JsonApiView(View):
    service_resolver: TodoServiceResolver | None = None
    service: TodoService

    def dispatch(self, request: HttpRequest, *args, **kwargs):
        self.service = self._resolve_service()
        return super().dispatch(request, *args, **kwargs)

    def _resolve_service(self) -> TodoService:
        if self.service_resolver is None:
            raise ImproperlyConfigured("Todo API service resolver is not configured.")
        return self.service_resolver()

    def parse_json_body(self, request: HttpRequest) -> dict[str, object]:
        if not request.body:
            return {}
        try:
            payload = json.loads(request.body)
        except json.JSONDecodeError as exc:
            raise InvalidJSONError() from exc
        if not isinstance(payload, dict):
            raise InvalidJSONError(message="请求体必须是 JSON 对象。")
        return payload

    def validate_form(
        self,
        *,
        form_class: type[forms.Form],
        data: dict[str, object] | QueryDict,
    ) -> dict[str, object]:
        self._raise_for_unknown_fields(form_class=form_class, data=data)
        form = form_class(data=data)
        if form.is_valid():
            return dict(form.cleaned_data)
        raise RequestValidationError(details=form.errors.get_json_data())

    def _raise_for_unknown_fields(
        self,
        *,
        form_class: type[forms.Form],
        data: dict[str, object] | QueryDict,
    ) -> None:
        unknown_fields = sorted(set(data.keys()) - set(form_class.base_fields))
        if not unknown_fields:
            return
        raise RequestValidationError(
            message="请求包含不支持的字段。",
            details={"fields": unknown_fields},
        )


class TodoCollectionApiView(JsonApiView):
    http_method_names = ["get", "post"]

    def get(self, request: HttpRequest):
        query_data = self.validate_form(form_class=TodoListQueryForm, data=request.GET)
        todo_query = TodoQuery(
            status=query_data.get("status") or None,
            priority=query_data.get("priority") or None,
        )
        todos = self.service.list_todos(query=todo_query)
        data = {"items": serialize_todo_list(todos), "count": len(todos)}
        return success_response(data=data)

    def post(self, request: HttpRequest):
        payload = self.parse_json_body(request)
        cleaned_data = self.validate_form(form_class=TodoCreateForm, data=payload)
        todo = self.service.create_todo(payload=cleaned_data)
        return success_response(
            data=serialize_todo(todo),
            message="待办事项创建成功。",
            code="CREATED",
            status=HTTPStatus.CREATED,
        )


class TodoDetailApiView(JsonApiView):
    http_method_names = ["get", "put", "patch", "delete"]

    def get(self, request: HttpRequest, todo_id: int):
        todo = self.service.get_todo(todo_id=todo_id)
        return success_response(data=serialize_todo(todo))

    def put(self, request: HttpRequest, todo_id: int):
        return self._update(request=request, todo_id=todo_id)

    def patch(self, request: HttpRequest, todo_id: int):
        return self._update(request=request, todo_id=todo_id)

    def delete(self, request: HttpRequest, todo_id: int):
        self.service.delete_todo(todo_id=todo_id)
        return success_response(message="待办事项删除成功。")

    def _update(self, *, request: HttpRequest, todo_id: int):
        payload = self.parse_json_body(request)
        cleaned_data = self.validate_form(form_class=TodoUpdateForm, data=payload)
        updates = {field: cleaned_data[field] for field in payload}
        if not updates:
            raise RequestValidationError(message="至少提供一个可更新字段。")
        todo = self.service.update_todo(todo_id=todo_id, payload=updates)
        return success_response(data=serialize_todo(todo), message="待办事项更新成功。")


class TodoToggleStatusApiView(JsonApiView):
    http_method_names = ["post"]

    def post(self, request: HttpRequest, todo_id: int):
        todo = self.service.toggle_status(todo_id=todo_id)
        return success_response(data=serialize_todo(todo), message="状态切换成功。")

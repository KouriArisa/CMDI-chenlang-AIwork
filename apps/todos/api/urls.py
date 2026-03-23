from django.urls import path

from apps.todos.api.views import (
    TodoCollectionApiView,
    TodoDetailApiView,
    TodoToggleStatusApiView,
)
from apps.todos.dependencies import get_todo_service

app_name = "todo_api"

urlpatterns = [
    path(
        "",
        TodoCollectionApiView.as_view(service_resolver=get_todo_service),
        name="list_create",
    ),
    path(
        "<int:todo_id>/",
        TodoDetailApiView.as_view(service_resolver=get_todo_service),
        name="detail",
    ),
    path(
        "<int:todo_id>/toggle/",
        TodoToggleStatusApiView.as_view(service_resolver=get_todo_service),
        name="toggle",
    ),
]

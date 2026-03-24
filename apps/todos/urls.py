from django.urls import path

from apps.todos.dependencies import get_todo_service
from apps.todos.views import (
    TodoCreateView,
    TodoDeleteView,
    TodoDetailView,
    TodoListView,
    TodoToggleStatusView,
    TodoUpdateView,
)

app_name = "todos"

urlpatterns = [
    path("", TodoListView.as_view(service_resolver=get_todo_service), name="list"),
    path(
        "create/",
        TodoCreateView.as_view(service_resolver=get_todo_service),
        name="create",
    ),
    path(
        "<int:pk>/",
        TodoDetailView.as_view(service_resolver=get_todo_service),
        name="detail",
    ),
    path(
        "<int:pk>/edit/",
        TodoUpdateView.as_view(service_resolver=get_todo_service),
        name="edit",
    ),
    path(
        "<int:pk>/delete/",
        TodoDeleteView.as_view(service_resolver=get_todo_service),
        name="delete",
    ),
    path(
        "<int:pk>/toggle/",
        TodoToggleStatusView.as_view(service_resolver=get_todo_service),
        name="toggle",
    ),
]

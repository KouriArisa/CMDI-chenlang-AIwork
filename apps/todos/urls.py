from django.urls import path

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
    path("", TodoListView.as_view(), name="list"),
    path("create/", TodoCreateView.as_view(), name="create"),
    path("<int:pk>/", TodoDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", TodoUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete/", TodoDeleteView.as_view(), name="delete"),
    path("<int:pk>/toggle/", TodoToggleStatusView.as_view(), name="toggle"),
]

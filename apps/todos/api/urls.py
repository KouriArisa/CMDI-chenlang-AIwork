from django.urls import path

from apps.todos.api.views import (
    TodoCollectionApiView,
    TodoDetailApiView,
    TodoToggleStatusApiView,
)

app_name = "todo_api"

urlpatterns = [
    path("", TodoCollectionApiView.as_view(), name="list_create"),
    path("<int:todo_id>/", TodoDetailApiView.as_view(), name="detail"),
    path("<int:todo_id>/toggle/", TodoToggleStatusApiView.as_view(), name="toggle"),
]

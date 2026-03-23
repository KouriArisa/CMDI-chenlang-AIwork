from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/todos/", include("apps.todos.api.urls")),
    path("todos/", include("apps.todos.urls")),
    path("", RedirectView.as_view(pattern_name="todos:list", permanent=False)),
]

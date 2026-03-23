from django.contrib import admin

from apps.todos.models import TodoItem


@admin.register(TodoItem)
class TodoItemAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "priority", "due_date", "created_at")
    list_filter = ("status", "priority")
    search_fields = ("title", "description")
    ordering = ("-created_at",)

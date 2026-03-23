from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from apps.todos.forms import TodoItemForm
from apps.todos.models import TodoItem, TodoStatus


class TodoListView(ListView):
    model = TodoItem
    template_name = "todos/todo_list.html"
    context_object_name = "todos"


class TodoDetailView(DetailView):
    model = TodoItem
    template_name = "todos/todo_detail.html"
    context_object_name = "todo"


class TodoCreateView(CreateView):
    model = TodoItem
    form_class = TodoItemForm
    template_name = "todos/todo_form.html"
    success_url = reverse_lazy("todos:list")


class TodoUpdateView(UpdateView):
    model = TodoItem
    form_class = TodoItemForm
    template_name = "todos/todo_form.html"

    def get_success_url(self) -> str:
        return reverse_lazy("todos:detail", kwargs={"pk": self.object.pk})


class TodoDeleteView(DeleteView):
    model = TodoItem
    template_name = "todos/todo_confirm_delete.html"
    success_url = reverse_lazy("todos:list")


class TodoToggleStatusView(View):
    http_method_names = ["post"]

    def post(self, request, pk):
        todo = get_object_or_404(TodoItem, pk=pk)
        todo.status = self._get_next_status(todo.status)
        todo.save(update_fields=["status", "completed_at", "updated_at"])
        return redirect("todos:list")

    def _get_next_status(self, current_status: str) -> str:
        if current_status == TodoStatus.PENDING:
            return TodoStatus.COMPLETED
        return TodoStatus.PENDING

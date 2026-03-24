from datetime import timedelta
from functools import cached_property

from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.timezone import localdate
from django.views import View
from django.views.generic import FormView, TemplateView

from apps.todos.contracts.dto import TodoData, TodoQuery
from apps.todos.exceptions import TodoNotFoundError
from apps.todos.forms import TodoForm
from apps.todos.mixins import TodoServiceResolverMixin
from apps.todos.models import TodoPriority, TodoStatus


class TodoLookupMixin:
    @cached_property
    def todo(self) -> TodoData:
        todo_id = self.kwargs["pk"]
        try:
            return self.service.get_todo(todo_id=todo_id)
        except TodoNotFoundError as exc:
            raise Http404(str(exc)) from exc


class TodoListView(TodoServiceResolverMixin, TemplateView):
    template_name = "todos/todo_list.html"

    def get_context_data(self, **kwargs) -> dict[str, object]:
        context = super().get_context_data(**kwargs)
        todos = self.service.list_todos(query=TodoQuery())
        context["todos"] = todos
        context["summary"] = self._build_summary(todos=todos)
        context["today"] = localdate()
        return context

    def _build_summary(self, *, todos: list[TodoData]) -> dict[str, int]:
        summary = {
            "total": len(todos),
            "pending": 0,
            "completed": 0,
            "high_priority": 0,
            "due_soon": 0,
        }
        due_soon_threshold = localdate() + timedelta(days=3)
        for todo in todos:
            if todo.status == TodoStatus.PENDING:
                summary["pending"] += 1
            else:
                summary["completed"] += 1
            if todo.priority == TodoPriority.HIGH:
                summary["high_priority"] += 1
            if (
                todo.due_date
                and todo.status == TodoStatus.PENDING
                and todo.due_date <= due_soon_threshold
            ):
                summary["due_soon"] += 1
        return summary


class TodoDetailView(TodoServiceResolverMixin, TodoLookupMixin, TemplateView):
    template_name = "todos/todo_detail.html"

    def get_context_data(self, **kwargs) -> dict[str, object]:
        context = super().get_context_data(**kwargs)
        context["todo"] = self.todo
        return context


class TodoCreateView(TodoServiceResolverMixin, FormView):
    template_name = "todos/todo_form.html"
    form_class = TodoForm

    def get_context_data(self, **kwargs) -> dict[str, object]:
        context = super().get_context_data(**kwargs)
        context["is_edit_mode"] = False
        return context

    def form_valid(self, form: TodoForm) -> HttpResponse:
        self.service.create_todo(payload=form.cleaned_data)
        return redirect("todos:list")


class TodoUpdateView(TodoServiceResolverMixin, TodoLookupMixin, FormView):
    template_name = "todos/todo_form.html"
    form_class = TodoForm

    def get_initial(self) -> dict[str, object]:
        return {
            "title": self.todo.title,
            "description": self.todo.description,
            "status": self.todo.status,
            "priority": self.todo.priority,
            "due_date": self.todo.due_date,
        }

    def get_context_data(self, **kwargs) -> dict[str, object]:
        context = super().get_context_data(**kwargs)
        context["is_edit_mode"] = True
        context["todo"] = self.todo
        return context

    def form_valid(self, form: TodoForm) -> HttpResponse:
        todo = self.service.update_todo(
            todo_id=self.kwargs["pk"],
            payload=form.cleaned_data,
        )
        return redirect("todos:detail", pk=todo.id)


class TodoDeleteView(TodoServiceResolverMixin, TodoLookupMixin, TemplateView):
    template_name = "todos/todo_confirm_delete.html"

    def get_context_data(self, **kwargs) -> dict[str, object]:
        context = super().get_context_data(**kwargs)
        context["object"] = self.todo
        return context

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        self.service.delete_todo(todo_id=self.kwargs["pk"])
        return redirect("todos:list")


class TodoToggleStatusView(TodoServiceResolverMixin, View):
    http_method_names = ["post"]

    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        self.service.toggle_status(todo_id=pk)
        next_url = reverse("todos:list")
        return redirect(next_url)

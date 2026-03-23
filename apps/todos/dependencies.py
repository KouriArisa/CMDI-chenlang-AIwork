from apps.todos.repositories.todo_repository import DjangoTodoRepository
from apps.todos.services.todo_service import TodoService


def get_todo_service() -> TodoService:
    return TodoService(repository=DjangoTodoRepository())

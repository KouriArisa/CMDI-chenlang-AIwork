from apps.todos.contracts.repositories import TodoRepository
from apps.todos.contracts.services import TodoService
from apps.todos.repositories.todo_repository import DjangoTodoRepository
from apps.todos.services.todo_service import DefaultTodoService


def get_todo_repository() -> TodoRepository:
    return DjangoTodoRepository()


def get_todo_service(*, repository: TodoRepository | None = None) -> TodoService:
    todo_repository = repository or get_todo_repository()
    return DefaultTodoService(repository=todo_repository)

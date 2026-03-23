from http import HTTPStatus
from typing import Any


class AppError(Exception):
    def __init__(
        self,
        *,
        message: str,
        code: str,
        status_code: int,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details


class RequestValidationError(AppError):
    def __init__(
        self,
        *,
        message: str = "请求参数校验失败。",
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            message=message,
            code="VALIDATION_ERROR",
            status_code=HTTPStatus.BAD_REQUEST,
            details=details,
        )


class InvalidJSONError(AppError):
    def __init__(self, *, message: str = "请求体不是合法的 JSON。") -> None:
        super().__init__(
            message=message,
            code="INVALID_JSON",
            status_code=HTTPStatus.BAD_REQUEST,
        )


class TodoNotFoundError(AppError):
    def __init__(self, *, todo_id: int) -> None:
        super().__init__(
            message=f"ID 为 {todo_id} 的待办事项不存在。",
            code="TODO_NOT_FOUND",
            status_code=HTTPStatus.NOT_FOUND,
        )

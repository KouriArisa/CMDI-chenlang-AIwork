import logging
from http import HTTPStatus

from django.http import Http404

from apps.todos.api.responses import error_response
from apps.todos.exceptions import AppError

logger = logging.getLogger(__name__)


class ApiExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        if not self._is_api_request(path=request.path):
            return None
        return self._build_error_response(exception=exception)

    def _build_error_response(self, *, exception: Exception):
        if isinstance(exception, AppError):
            return error_response(
                message=exception.message,
                code=exception.code,
                status=exception.status_code,
                errors=exception.details,
            )
        if isinstance(exception, Http404):
            return error_response(
                message="请求的资源不存在。",
                code="NOT_FOUND",
                status=HTTPStatus.NOT_FOUND,
            )
        logger.exception("Unhandled API exception")
        return error_response(
            message="服务器内部错误。",
            code="INTERNAL_SERVER_ERROR",
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
        )

    def _is_api_request(self, *, path: str) -> bool:
        return path.startswith("/api/")

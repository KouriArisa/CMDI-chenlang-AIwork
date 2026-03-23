from collections.abc import Mapping
from http import HTTPStatus
from typing import Any

from django.http import JsonResponse


def build_response_payload(
    *,
    success: bool,
    code: str,
    message: str,
    data: Any = None,
    errors: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    payload = {
        "success": success,
        "code": code,
        "message": message,
        "data": data,
    }
    if errors is not None:
        payload["errors"] = dict(errors)
    return payload


def success_response(
    *,
    data: Any = None,
    message: str = "请求成功。",
    code: str = "SUCCESS",
    status: int = HTTPStatus.OK,
) -> JsonResponse:
    payload = build_response_payload(
        success=True,
        code=code,
        message=message,
        data=data,
    )
    return JsonResponse(payload, status=status, json_dumps_params={"ensure_ascii": False})


def error_response(
    *,
    message: str,
    code: str,
    status: int,
    errors: Mapping[str, Any] | None = None,
) -> JsonResponse:
    payload = build_response_payload(
        success=False,
        code=code,
        message=message,
        data=None,
        errors=errors,
    )
    return JsonResponse(payload, status=status, json_dumps_params={"ensure_ascii": False})

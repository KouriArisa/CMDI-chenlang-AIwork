from http import HTTPStatus

from django.db import connections
from django.db.utils import OperationalError
from django.http import JsonResponse


def health_check(request):
    try:
        with connections["default"].cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
    except OperationalError:
        return JsonResponse(
            {"status": "error", "database": "unavailable"},
            status=HTTPStatus.SERVICE_UNAVAILABLE,
        )
    return JsonResponse(
        {"status": "ok", "database": "ok"},
        status=HTTPStatus.OK,
    )

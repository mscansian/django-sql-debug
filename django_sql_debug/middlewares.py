from django.db import connections

from .sql import wrap_cursor, unwrap_cursor


class DebugSQLMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        for connection in connections.all():
            wrap_cursor(connection)

        try:
            return self.get_response(request)
        finally:
            for connection in connections.all():
                unwrap_cursor(connection)

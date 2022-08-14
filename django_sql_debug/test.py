from contextlib import contextmanager

from django.db import connection

from .sql import wrap_cursor, unwrap_cursor


class DebugSQLTestCaseMixin:
    def setUp(self):
        super().setUp()
        wrap_cursor(connection)

    def tearDown(self):
        unwrap_cursor(connection)
        super().tearDown()


@contextmanager
def debug_sql():
    wrap_cursor(connection)
    yield
    unwrap_cursor(connection)

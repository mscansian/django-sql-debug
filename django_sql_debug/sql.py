from time import time

from django.conf import settings

from .output import write, write_header


def wrap_cursor(connection):
    if not hasattr(connection, "_djdt_cursor"):
        connection._djdt_cursor = connection.cursor
        connection._djdt_chunked_cursor = connection.chunked_cursor

        def cursor(*args, **kwargs):
            wrapper = CursorWrapper
            return wrapper(connection._djdt_cursor(*args, **kwargs), connection)

        def chunked_cursor(*args, **kwargs):
            cursor = connection._djdt_chunked_cursor(*args, **kwargs)
            if not isinstance(cursor, CursorWrapper):
                wrapper = CursorWrapper
                return wrapper(cursor, connection)
            return cursor

        connection.cursor = cursor
        connection.chunked_cursor = chunked_cursor
        return cursor


def unwrap_cursor(connection):
    if hasattr(connection, "_djdt_cursor"):
        # Sometimes the cursor()/chunked_cursor() methods of the DatabaseWrapper
        # instance are already monkey patched before wrap_cursor() is called.  (In
        # particular, Django's SimpleTestCase monkey patches those methods for any
        # disallowed databases to raise an exception if they are accessed.)  Thus only
        # delete our monkey patch if the method we saved is the same as the class
        # method.  Otherwise, restore the prior monkey patch from our saved method.
        if connection._djdt_cursor == getattr(connection.__class__, 'cursor', None):
            del connection.cursor
        else:
            connection.cursor = connection._djdt_cursor
        del connection._djdt_cursor
        if connection._djdt_chunked_cursor == getattr(connection.__class__, 'chunked_cursor', None):
            del connection.chunked_cursor
        else:
            connection.chunked_cursor = connection._djdt_chunked_cursor
        del connection._djdt_chunked_cursor


class CursorWrapper:
    def __init__(self, cursor, db):
        self.cursor = cursor
        self.db = db

        self._params_enabled = getattr(settings, 'SQL_DEBUG_ENABLE_PARAMS', True)
        self._perform_enabled = getattr(settings, 'SQL_DEBUG_ENABLE_PERFORMANCE', True)
        self._explain_enabled = getattr(settings, 'SQL_DEBUG_ENABLE_EXPLAIN', True)

    def _record(self, method, sql, params):
        write('')
        write_header('SQL QUERY', '=', '=', color='\033[91m')
        write(sql)

        if self._params_enabled and params:
            write_header('params', '- ', ' -', color='\033[92m')
            write(params)

        start_time = time()
        try:
            try:
                results = method(sql, params)
            finally:
                stop_time = time()
        except Exception:
            raise
        else:
            if self._explain_enabled and sql.startswith('SELECT'):
                if self.db.vendor in ['postgresql', 'mysql']:
                    try:
                        cursor = self.db._cursor()
                        write_header('explain', '- ', ' -', color='\033[93m')
                        cursor.execute(f'EXPLAIN ANALYZE {sql}', params)
                        for row in cursor.fetchall():
                            write(row[0])
                    finally:
                        cursor.close()
        finally:
            if self._perform_enabled:
                write_header('performance', '- ', ' -', color='\033[94m')
                duration = (stop_time - start_time) * 1000
                write(f'duration: {duration:.4f}ms')
            write('', color='\033[00m')
        return results

    def callproc(self, procname, params=None):
        return self._record(self.cursor.callproc, procname, params)

    def execute(self, sql, params=None):
        return self._record(self.cursor.execute, sql, params)

    def executemany(self, sql, param_list):
        return self._record(self.cursor.executemany, sql, param_list)

    def __getattr__(self, attr):
        return getattr(self.cursor, attr)

    def __iter__(self):
        return iter(self.cursor)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

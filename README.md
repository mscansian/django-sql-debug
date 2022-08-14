[![PyPI version](https://badge.fury.io/py/django-sql-debug.svg)](https://badge.fury.io/py/django-sql-debug)

# django-sql-debug
Output in the console the executed SQL of queries made by Django's ORM.

**This is a development tool that should only be used in a local environment and never included in production code.**

## Features
- Print executed SQL to the console
- Automatically runs `EXPLAIN ANALYSE`
- Allows for debugging of single query, function, test or the entire application

## Why not use django-debug-toolbar?
[Django Debug Toolbar](https://github.com/jazzband/django-debug-toolbar) is great if you are developing an html website
using Django. However, since it is focused on displaying the queries using HTML code inject in the webpage it is not
suitable if you are developing a REST API or need to view the queries being run in a unit test. This lib was inspired
by the weakenesses of Django Debug Toolbar on these use cases.

## Supported database
Below are the supported databases. If your database is not included it just means it has not being tested and is not
guaranteed to work.

- PostgreSQL


## Installation
```
pip install django-sql-debug
```

## Examples
There are many ways to use the library. You can set the scope of the debug using one of the examples below.

### Debugging a small segment of code
```
from django_sql_debug import debug_sql


with @debug_sql():
    SomeModel.objects.get(id=5)  # will be captured
SomeModel.objects.get(id=5)  # will not be captured

```

### Debugging a single function or test
```
from django_sql_debug import debug_sql


class MyTest(TestCase):
    @debug_sql()
    def test_will_show_executed_sql(self):
        SomeModel.objects.get(id=5)

    def test_will_not_show_executed_sql(self):
        SomeModel.objects.create(name='test')
```

### Debugging an entire TestCase
```
from django_sql_debug import DebugSQLTestCaseMixin


class MyTest(DebugSQLTestCaseMixin, TestCase):
    def test_will_show_executed_sql(self):
        SomeModel.objects.get(id=5)

    def test_will_also_show_executed_sql(self):
        SomeModel.objects.create(name='test')
```

### Debugging an entire application
Add `django_sql_debug` to the `INSTALLED_APPS` and `MIDDLEWARES`.

```
INSTALLED_APPS = [
    'django_sql_debug',

    ...
]

MIDDLEWARE = [
    'django_sql_debug.DebugSQLMiddleware',

    ...
]
```


## Configuration
You can change some configurations in Django's `settings.py`

- SQL_DEBUG_ENABLE_PARAMS: Include the SQL parameters section in the debug log (default: True)
- SQL_DEBUG_ENABLE_PERFORMANCE: Include the SQL performance section in the debug log (default: True)
- SQL_DEBUG_ENABLE_EXPLAIN: Run `EXPLAIN` command on supported databases (default: True)

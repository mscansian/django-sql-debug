# django-sql-debug
Allow users to see in the console all SQL queries made by the Django ORM.

## Examples
### Debugging a single query
```
from django_sql_debug import debug_sql


with @debug_sql():
    SomeModel.objects.get(id=5)  # will be captured
SomeModel.objects.get(id=5)  # will not be captured

```

### Debugging a single test
```
from django_sql_debug import debug_sql


class MyTest(TestCase):
    @debug_sql()
    def test_will_show_executed_sql(self):
        SomeModel.objects.get(id=5)

    def test_will_not_show_executed_sql(self):
        SomeModel.objects.create(name='test')
```

### Debugging you entire Test class
You can wrap your entire TestCase class to output the SQL executed.

```
from django_sql_debug import DebugSQLTestCaseMixin


class MyTest(DebugSQLTestCaseMixin, TestCase):
    def test_will_show_executed_sql(self):
        SomeModel.objects.get(id=5)

    def test_will_also_show_executed_sql(self):
        SomeModel.objects.create(name='test')
```

### Debugging the entire application
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

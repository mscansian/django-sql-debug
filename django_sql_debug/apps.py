from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DebugToolbarConfig(AppConfig):
    name = "django_sql_debug"
    verbose_name = _("Django SQL Debug")

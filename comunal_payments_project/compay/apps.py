from django.apps import AppConfig


class CompayConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "compay"
    verbose_name = 'Расчет коммунальных платежей'
    ordering = []
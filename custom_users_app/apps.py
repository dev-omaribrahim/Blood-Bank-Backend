from django.apps import AppConfig


class CustomUsersAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'custom_users_app'
    verbose_name = "حسابات العاملين"

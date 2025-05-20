from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField' # helps in auto discovering app config
    name = 'users'

    def ready(self):
        import users.signals # triggers signals.py when app loads
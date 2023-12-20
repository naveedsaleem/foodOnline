from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    # override the ready function so that signal can from signal file
    def ready(self):
        import accounts.signals

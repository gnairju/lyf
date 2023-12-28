from django.apps import AppConfig


class ProviderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'provider'

    def ready(self):
        import provider.signals  # Import the signals module when the app is ready
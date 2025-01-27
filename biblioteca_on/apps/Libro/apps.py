from django.apps import AppConfig


class LibroConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.Libro'

    def ready(self):
        import apps.Libro.signals

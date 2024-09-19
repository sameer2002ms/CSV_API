from django.apps import AppConfig

class CsvappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'csvapp'

    def ready(self):
        import csvapp.tasks  # This will ensure tasks are loaded when the app is ready
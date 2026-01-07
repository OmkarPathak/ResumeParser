from django.apps import AppConfig


class ParserAppConfig(AppConfig):
    name = 'parser_app'

    def ready(self):
        import parser_app.signals

from django.apps import AppConfig


class WebsiteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'website'

    def ready(self):
        try:
            from django.template.context import BaseContext

            def _base_context_copy(self):
                duplicate = self.__class__.__new__(self.__class__)
                duplicate.__dict__.update(self.__dict__)
                duplicate.dicts = self.dicts[:]
                return duplicate

            BaseContext.__copy__ = _base_context_copy
        except Exception:
            pass

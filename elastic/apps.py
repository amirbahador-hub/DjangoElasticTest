from django.apps import AppConfig
from django.conf import settings

from elasticsearch_dsl.connections import connections


class ElasticConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'elastic'

    def ready(self):
        if settings.ES_ACTIVE:
            connections.configure(**settings.ES_CONNECTIONS)
            import elastic.signals

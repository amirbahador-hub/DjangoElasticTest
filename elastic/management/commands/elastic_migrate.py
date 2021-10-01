from __future__ import print_function
from django.core.management.base import BaseCommand
from elasticsearch_dsl.connections import connections
from elastic.index import index
import json
from django.conf import settings


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        es = connections.get_connection()
        index.delete(ignore=404)
        index.create()
        mapping = index.get_mapping()
        m_path = str(settings.BASE_DIR) + "/elastic" + "/mappings" + "/mapping.json"
        # print("template schema:", json.dumps(mapping, indent=4))
        with open(m_path, 'w', encoding='utf-8') as f:
            json.dump(mapping, f, ensure_ascii=False, indent=4)
        # print(index.get_mapping())

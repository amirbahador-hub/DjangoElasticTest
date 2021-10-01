from __future__ import print_function

import time
from django.core.management.base import BaseCommand
from elasticsearch_dsl.connections import connections
from elastic.index import index
import json
from django.conf import settings
from api.models import ProductPicture, Product
from elasticsearch.helpers import parallel_bulk


def elastic_normalizer(item):
    product = item.product
    vendor_product = product.vendor_products.order_by("discounted_price").first()
    category = product.category
    categories = category.get_children(self_include=True)
    picture = ProductPicture.objects.filter(is_main=True, product=product).first()

    return {
        "title": product.title,
        "slug": product.slug,
        "brand": {
                "id": product.brand.id,
                "name": product.brand.name,
                "en_name": product.brand.en_name,
                "slug": product.brand.slug
        },
        "picture": {
            "thumbnail": picture.thumbnail,
            "large": picture.large,
        },
        "category":  {
                "id": category.id,
                "name": category.name,
                "title": category.title,
                "slug": category.slug,
            },

        "categories": [
            {
                "id": cat.id,
                "name": cat.name,
                "title": cat.title,
                "slug": cat.slug,
            }
            for cat in categories
        ],
        "click": 0,
        "created_at": product.created_at,
        "prices": vendor_product.price,
        "discount": vendor_product.discount,
        "discount_difference": vendor_product.price - vendor_product.discounted_price,
        "discounted_price": vendor_product.discounted_price,
        "is_exist": product.is_exist_check(),
        "tags": [],
        "vendor": [
            {
                "id": vendor.user.id,
                "name": vendor.name,
                "title": vendor.title,
                "slug": vendor.slug,
            }
            for vendor in product.vendors.all()
        ],
        "view": 0
    }


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        es = connections.get_connection()
        index.delete(ignore=404)
        index.create()
        self.verbose_run(chunk_size=100)

    def verbose_run(self, chunk_size):
        print('Indexing Started')
        start = time.time()
        data = Product.objects.filter(state='published')

        op_type = "index"
        index = settings.ES_INDEX
        _type = "_doc"
        obj = [
            {
                "_op_type": op_type,
                "_id": f"{doc.id}",
                "_index": index,
                "_type": _type,
                "_source": elastic_normalizer(doc),
            }
            for doc in data
        ]
        client = connections.get_connection()
        rs = parallel_bulk(client, obj, chunk_size=chunk_size)

        print('DONE\nIndexing in %.2f seconds' % (
             time.time() - start
        ))


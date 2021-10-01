from django.conf import settings
from elasticsearch_dsl import (
    Document, Date, Text, Object, Index, InnerDoc,
    Keyword, Float, SearchAsYouType, Boolean, Integer, Completion,
)

from .analyzers import shingle, reverse, auto_complete, autocomplete_search


class Brand(InnerDoc):
    id = Keyword()
    name = Text()
    slug = Keyword()


class Tag(InnerDoc):
    id = Keyword()
    name = Text()
    picture = Keyword()


class Category(InnerDoc):
    id = Keyword()
    name = Text()


class Vendor(InnerDoc):
    id = Keyword()
    name = Text()
    slug = Keyword()
    quantity = Integer()
    state = Integer()


class Product(Document):
    id = Keyword
    brand = Object(Brand)
    vendor = Object(Brand)
    title = Text(
        fields={
            'raw': Keyword(),
            'shin': Text(analyzer=shingle),
            'rev': Text(analyzer=reverse),
            'suggest': SearchAsYouType(max_shingle_size=3),
            'suggest_completion': Completion(),
            'auto': Text(analyzer=auto_complete, search_analyzer=autocomplete_search),

        }
    )
    created_at = Date()
    price = Float()
    discounted_price = Float()
    discount_difference = Float()
    discount = Float()
    view = Integer()
    click = Integer()
    is_exist = Boolean()
    slug = Keyword()
    categories = Object(Category, multi=True)
    tags = Object(Tag, multi=True)

    class Index:
        name = settings.ES_PRODUCTS_INDEX

    class Meta:
        doc_type = 'product'

    def save(self, **kwargs):
        # self.created_at = datetime.now()
        return super(Product, self).save(**kwargs)

    def __repr__(self):
        return '<Product: {}>'.format(
            self.title,
        )


# create an index and register the doc types
index = Index(settings.ES_PRODUCTS_INDEX)
index.settings(number_of_shards=1, number_of_replicas=1)
index.document(Product)

from django.db.models.signals import post_save, post_delete, pre_delete, pre_save
from django.dispatch import receiver
from django.utils.text import slugify
# from api.models import Product, VendorProducts, VendorProductsStatus, Category, Vendor, Brand


# @receiver(pre_save, sender=Product)
# def update_elastic(sender, instance, *args, **kwargs):
#     if instance.slug:
#         pass


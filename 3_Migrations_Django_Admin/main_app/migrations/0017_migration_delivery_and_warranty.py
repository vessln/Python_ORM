from django.db import migrations
from django.utils import timezone


def set_delivery_warranty(apps, schema_editor):
    order_model = apps.get_model('main_app', 'Order')
    all_orders = order_model.objects.all()

    for order in all_orders:
        if order.status == "Pending":
            order.delivery = order.order_date + timezone.timedelta(days=3)
            order.save()
        elif order.status == "Completed":
            order.warranty = "24 months"
            order.save()
        elif order.status == "Canceled":
            order.delete()


def reverse_delivery_warranty_to_default(apps, schema_editor):
    order_model = apps.get_model('main_app', 'Order')
    all_orders = order_model.objects.all()

    default_warranty = order_model._meta.get_field("warranty").default

    for order in all_orders:
        if order.status == "Pending":
            order.delivery = None
        elif order.status == "Completed":
            order.warranty = default_warranty

    order_model.objects.bulk_update(all_orders, ["delivery"])
    order_model.objects.bulk_update(all_orders, ["warranty"])


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0016_order'),
    ]

    operations = [
        migrations.RunPython(set_delivery_warranty, reverse_code=reverse_delivery_warranty_to_default)
    ]

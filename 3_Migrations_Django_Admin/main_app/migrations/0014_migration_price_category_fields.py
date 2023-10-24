from django.db import migrations


def set_new_price(apps, schema_editor):
    COEF_PRICE = 120

    phone_model = apps.get_model("main_app", "Smartphone")
    all_phones = phone_model.objects.all()

    for phone in all_phones:
        phone.price = len(phone.brand) * COEF_PRICE

    phone_model.objects.bulk_update(all_phones, ["price"])


def set_category_by_price(apps, schema_editor):
    phone_model = apps.get_model("main_app", "Smartphone")
    all_phones = phone_model.objects.all()

    for phone in all_phones:
        if phone.price >= 750:
            phone.category = "Expensive"
        else:
            phone.category = "Cheap"

    phone_model.objects.bulk_update(all_phones, ["category"])


def set_both_price_and_category(apps, schema_editor):
    set_new_price(apps, schema_editor)
    set_category_by_price(apps, schema_editor)


def reverse_both(apps, schema_editor):
    phone_model = apps.get_model("main_app", "Smartphone")
    all_phones = phone_model.objects.all()

    default_price = phone_model._meta.get_field("price").default
    default_category = phone_model._meta.get_field("category").default

    for phone in all_phones:
        phone.price = default_price
        phone.category = default_category

    phone_model.objects.bulk_update(all_phones, ["price"])
    phone_model.objects.bulk_update(all_phones, ["category"])


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0013_smartphone'),
    ]

    operations = [
        migrations.RunPython(set_both_price_and_category, reverse_code=reverse_both)
    ]

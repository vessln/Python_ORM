from django.db import migrations


def set_rarity_for_item(apps, schema_editor):
    item_model = apps.get_model("main_app", "Item")

    all_items = item_model.objects.all()

    for item in all_items:
        if item.price <= 10:
            item.rarity = "Rare"
        elif 11 <= item.price <= 20:
            item.rarity = "Very Rare"
        elif 21 <= item.price <= 30:
            item.rarity = "Extremely Rare"
        elif item.price >= 31:
            item.rarity = "Mega Rare"

    item_model.objects.bulk_update(all_items, ["rarity"])


def reverse_rarity_to_default(apps, schema_editor):
    item_model = apps.get_model("main_app", "Item")
    all_items = item_model.objects.all()

    default_rarity = item_model._meta.get_field("rarity").default

    for item in all_items:
        item.rarity = default_rarity

    item_model.objects.bulk_update(all_items, ["rarity"])


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0011_item'),
    ]

    operations = [
        migrations.RunPython(set_rarity_for_item, reverse_code=reverse_rarity_to_default)
    ]

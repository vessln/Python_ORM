from django.db import migrations


def save_unique_brands(apps, schema_editor):
    shoe = apps.get_model("main_app", "Shoe")
    unique_brands = apps.get_model("main_app", "UniqueBrands")

    only_unique_names = shoe.objects.values_list("brand", flat=True).distinct()

    create_unique_brands = [unique_brands(brand_name=name) for name in only_unique_names]

    unique_brands.objects.bulk_create(create_unique_brands)


def remove_unique_brands(apps, schema_editor):
    unique_brands = apps.get_model("main_app", "UniqueBrands")

    unique_brands.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_uniquebrands'),
    ]

    operations = [
        migrations.RunPython(save_unique_brands, reverse_code=remove_unique_brands)
    ]

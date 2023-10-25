from django.db import migrations


def set_correct_group_by_age(apps, schema_editor):
    person_table = apps.get_model("main_app", "Person")

    all_persons = person_table.objects.all()

    for person_obj in all_persons:
        if person_obj.age <= 12:
            person_obj.age_group = "Child"
        elif 13 <= person_obj.age <= 17:
            person_obj.age_group = "Teen"
        elif person_obj.age >= 18:
            person_obj.age_group = "Adult"

    person_table.objects.bulk_update(all_persons, ["age_group"])


def reverse_set_correct_group(apps, schema_editor):
    person_table = apps.get_model("main_app", "Person")
    all_persons = person_table.objects.all()

    default_age_group = person_table._meta.get_field("age_group").default

    for p in all_persons:
        p.age_group = default_age_group

    person_table.objects.bulk_update(all_persons, ["age_group"])


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0009_person'),
    ]

    operations = [
        migrations.RunPython(set_correct_group_by_age, reverse_code=reverse_set_correct_group)
    ]

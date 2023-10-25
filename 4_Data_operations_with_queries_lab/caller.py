import os
import django
from datetime import date

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Student

# def add_students():
#     Student.objects.create(
#         student_id="FC5204",
#         first_name="John",
#         last_name="Doe",
#         birth_date="1995-05-15",
#         email="john.doe@university.com"
#     )
#     Student.objects.create(
#         student_id="FE0054",
#         first_name="Jane",
#         last_name="Smith",
#         birth_date=None,
#         email="jane.smith@university.com"
#     )
#
#     student_3 = Student(
#         student_id="FH2014",
#         first_name="Alice",
#         last_name="Johnson",
#         birth_date="1998-02-10",
#         email="alice.johnson@university.com"
#     )
#     student_3.save()
#
#     student_4 = Student(
#         student_id="FH2015",
#         first_name="Bob",
#         last_name="Wilson",
#         birth_date="1996-11-25",
#         email="bob.wilson@university.com"
#     )
#     student_4.save()
#
# add_students()


def get_students_info():
    all_students = []
    students_records = Student.objects.all()

    for student in students_records:
        all_students.append(f"Student №{student.student_id}: {student.first_name} "
                            f"{student.last_name}; Email: {student.email}")

    return "\n".join(all_students)

# print(get_students_info())


def update_students_emails():
    students_records = Student.objects.all()

    for student in students_records:
        new = student.email.replace("university.com", "uni-students.com")
        student.email = new
        student.save()

# update_students_emails()
# for student_ in Student.objects.all():
#     print(student_.email)


def truncate_students():
    Student.objects.all().delete()

# truncate_students()
# print(Student.objects.all())
# print(f"Number of students: {Student.objects.count()}")







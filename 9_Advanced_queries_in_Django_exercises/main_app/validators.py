from django.core.exceptions import ValidationError


def correct_rating_validator(value):
    if value < 0.0 or value > 10.0:
        raise ValidationError("The rating must be between 0.0 and 10.0")


def correct_year_validator(value):
    if value < 1990 or value > 2023:
        raise ValidationError("The release year must be between 1990 and 2023")
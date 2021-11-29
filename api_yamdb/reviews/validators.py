from django.core.exceptions import ValidationError
from django.utils import timezone


def year_validator(value):
    if value > timezone.now().year or value <= 0:
        raise ValidationError(
            f'{value} is not valid year!'
        )

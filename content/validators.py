import datetime

from django.core.exceptions import ValidationError


def validate_year(year):
    """
    Валидация, что переданный пользователем год не в будущем.
    """

    now = datetime.datetime.now()
    if year > now.year:
        return ValidationError('Полиция времени! Медленно выйдите из Машины!')

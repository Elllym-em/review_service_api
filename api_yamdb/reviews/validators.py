import datetime as dt
import re

from django.core.exceptions import ValidationError


def validate_year(value):
    year = dt.date.today().year
    if value > year:
        raise ValidationError(
            'Год выпуска не может быть больше текущего.'
        )
    return value


def validate_username(name):
    if name == 'me':
        raise ValidationError('Имя пользователя "me" использовать запрещено!')
    if not re.compile(r'^[\w.@+-]+').fullmatch(name):
        raise ValidationError(
            'Можно использовать только буквы, цифры и символы @.+-_".')

from django.core.exceptions import ValidationError


def validate_letters_numbers_and_dashes_only(value):
    for ch in value:
        if ch.isalpha() or ch.isalnum() or ch == '-':
            continue
        raise ValidationError('The username must contain only letters, digits and dashes')


def validate_only_letters(value):
    for ch in value:
        if not ch.isalpha():
            raise ValidationError('The first name must contain only letters')

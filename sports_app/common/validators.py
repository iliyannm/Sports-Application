from django.core.exceptions import ValidationError


# username validator for the User model
def validate_letters_numbers_and_dashes_only(value):
    for ch in value:
        if ch.isalpha() or ch.isalnum() or ch == '-':
            continue
        raise ValidationError('The username must contain only letters, digits and dashes')


# first and last name validator for the Profile model
def validate_only_letters(value):
    for ch in value:
        if not ch.isalpha():
            raise ValidationError('The first name must contain only letters')


# category validator for the ArticleSportCategory model
def validate_letters_numbers_and_spaces_only(value):
    for ch in value:
        if ch.isalpha() or ch.isalnum() or ch == ' ':
            continue
        raise ValidationError('The category must contain only letters, digits and spaces')

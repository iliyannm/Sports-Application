from django.contrib.auth import models as auth_models
from django.core.validators import MinLengthValidator
from django.db import models

from sports_app.accounts.managers import SportsAppUserManager
from sports_app.common.validators import validate_letters_numbers_and_dashes_only, validate_only_letters


class SportsAppUser(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    USERNAME_MIN_LENGTH = 5
    USERNAME_MAX_LENGTH = 20

    username = models.CharField(
        max_length=USERNAME_MAX_LENGTH,
        unique=True,
        validators=(
            validate_letters_numbers_and_dashes_only,
            MinLengthValidator(USERNAME_MIN_LENGTH),
        )
    )

    date_joined = models.DateTimeField(
        auto_now_add=True,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    USERNAME_FIELD = 'username'

    objects = SportsAppUserManager()


class Profile(models.Model):
    FIRST_NAME_MIN_LENGTH = 3
    FIRST_NAME_MAX_LENGTH = 20
    LAST_NAME_MIN_LENGTH = 3
    LAST_NAME_MAX_LENGTH = 20

    MALE = 'Male'
    FEMALE = 'Female'
    DO_NOT_SHOW = 'Do not show'

    GENDERS = [(x, x) for x in (MALE, FEMALE, DO_NOT_SHOW)]

    first_name = models.CharField(
        null=False,
        blank=False,
        max_length=FIRST_NAME_MAX_LENGTH,
        validators=(
            MinLengthValidator(FIRST_NAME_MIN_LENGTH),
            validate_only_letters,
        )
    )

    last_name = models.CharField(
        null=False,
        blank=False,
        max_length=LAST_NAME_MAX_LENGTH,
        validators=(
            MinLengthValidator(LAST_NAME_MIN_LENGTH),
            validate_only_letters,
        )
    )

    picture = models.ImageField(
        null=True,
        blank=True,
    )

    email = models.EmailField(
        null=True,
        blank=True,
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True,
    )

    gender = models.CharField(
        null=True,
        blank=True,
        max_length=max(len(x) for x, y in GENDERS),
        choices=GENDERS,
        default=DO_NOT_SHOW,
    )

    user = models.OneToOneField(
        SportsAppUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

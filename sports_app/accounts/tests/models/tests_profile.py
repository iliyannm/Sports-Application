from django.core.exceptions import ValidationError
from django.test import TestCase

from sports_app.accounts.models import Profile


class ProfileTests(TestCase):

    def test_profile_create__when_first_name_contains_digit__expect_to_fail(self):
        first_name = 'Iliyan1'
        profile = Profile(
            first_name=first_name,
            last_name='Maznikov',
        )

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            profile.save()

        self.assertIsNotNone(context.exception)

    def test_profile_create__when_first_name_contains_question_mark__expect_to_fail(self):
        first_name = 'Iliy?an'
        profile = Profile(
            first_name=first_name,
            last_name='Maznikov',
        )

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            profile.save()

        self.assertIsNotNone(context.exception)

    def test_profile_create__when_first_name_contains_space__expect_to_fail(self):
        first_name = 'Iliy an'
        profile = Profile(
            first_name=first_name,
            last_name='Maznikov',
        )

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            profile.save()

        self.assertIsNotNone(context.exception)

    def test_profile_create__when_first_name_is_empty__expect_to_fail(self):
        first_name = ''
        profile = Profile(
            first_name=first_name,
            last_name='Maznikov',
        )

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            profile.save()

        self.assertIsNotNone(context.exception)

    def test_profile_create__when_last_name_is_empty__expect_to_fail(self):
        first_name = 'Iliyan'
        profile = Profile(
            first_name=first_name,
            last_name='',
        )

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            profile.save()

        self.assertIsNotNone(context.exception)

    def test_profile_full_name__when_valid__expect_correct_full_name(self):
        profile = Profile(
            first_name='Iliyan',
            last_name='Maznikov',
        )

        self.assertEqual('Iliyan Maznikov', profile.full_name)

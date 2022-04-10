from sports_app.accounts.forms import CreateAccountForm
from django.test import TestCase


class AccountFormTests(TestCase):
    def test_create_account_form_save_when_valid(self):
        data = {
            'username': 'iliyan',
            'password1': 'Password1.',
            'password2': 'Password1.',
            'first_name': 'Iliyan',
            'last_name': 'Maznikov'
        }

        form = CreateAccountForm(data)

        self.assertTrue(form.is_valid())

    def test_create_account_form_fail__when_the_two_passwords_do_not_match(self):
        data = {
            'username': 'iliyan',
            'password1': 'Password1.',
            'password2': 'Password2.',
            'first_name': 'Iliyan',
            'last_name': 'Maznikov'
        }

        form = CreateAccountForm(data)

        self.assertFalse(form.is_valid())

    def test_create_account_form_fail__when_the_username_contains_percentage(self):
        data = {
            'username': 'iliyan%',
            'password1': 'Password1.',
            'password2': 'Password2.',
            'first_name': 'Iliyan',
            'last_name': 'Maznikov'
        }

        form = CreateAccountForm(data)

        self.assertFalse(form.is_valid())

    def test_create_account_form_fail__when_the_password_is_too_small(self):
        data = {
            'username': 'iliyan%',
            'password1': 'pass',
            'password2': 'pass',
            'first_name': 'Iliyan',
            'last_name': 'Maznikov'
        }

        form = CreateAccountForm(data)

        self.assertFalse(form.is_valid())
from django.contrib.auth import get_user_model
from django import test
from django.urls import reverse

from sports_app.accounts.models import Profile

UserModel = get_user_model()


class ProfileViewTests(test.TestCase):
    VALID_USER_CREDENTIALS = {
        'username': 'iliyano',
        'password': 'Password1-',
    }

    VALID_PROFILE_DATA = {
        'first_name': 'Iliyan',
        'last_name': 'Maznikov',
    }

    @staticmethod
    def __create_user(**credentials):
        return UserModel.objects.create_user(**credentials)

    def __create_valid_user_and_profile(self):
        user = self.__create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(
            **self.VALID_PROFILE_DATA,
            user=user,
        )

        return (user, profile)

    def __get_response_for_profile(self, profile):
        return self.client.get(reverse('profile details', kwargs={'pk': profile.pk}))

    def test_get__login_user_expect_correct_template(self):
        response = self.client.get(reverse('login user'))

        self.assertTemplateUsed(response, 'accounts/login_page.html')

    def test_get__change_password_view(self):
        response = self.client.get(reverse('change password'))

        self.assertTemplateUsed('accounts/change_password.html')

    def test_when_opening_not_existing_profile_return_404(self):
        response = self.client.get(reverse('profile details', kwargs={'pk': 1,}))

        self.assertTemplateUsed('404.html')

    def test_expect_correct_template__when_create_valid_user_and_profile(self):
        user = UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(
            **self.VALID_PROFILE_DATA,
            user=user,
        )

        response = self.client.get(reverse('profile details', kwargs={'pk': profile.pk}))

        self.assertTemplateUsed('accounts/profile_details.html')

    def test_when_user_is_owner__expect_is_owner_to_be_true(self):
        _, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)

        response = self.__get_response_for_profile(profile)

        self.assertTrue(response.context['is_owner'])

    def test_when_user_is_not_owner__expect_is_owner_to_be_false(self):
        _, profile = self.__create_valid_user_and_profile()
        credentials = {
            'username': 'iliyan2',
            'password': '12345qwe',
        }

        self.__create_user(**credentials)

        self.client.login(**credentials)

        response = self.__get_response_for_profile(profile)

        self.assertFalse(response.context['is_owner'])

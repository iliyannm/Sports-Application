from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

from sports_app.accounts.models import Profile

User = get_user_model()


class Command(BaseCommand):
    help = 'Creates only staff user (no admin permissions)'

    def handle(self, *args, **kwargs):
        user = User(
            username=input('Username:'),
            is_staff=True,
        )

        user.set_password((input('Password:')))

        my_group = Group.objects.get(name='staff_group')

        user.full_clean()

        user.save()

        # my_group.user_set.add(user)

        user.groups.add(my_group)

        user.save()

        profile = Profile(
            first_name=input('First name:'),
            last_name=input('Last name:'),
            user_id=user.id
        )

        profile.full_clean()

        profile.save()

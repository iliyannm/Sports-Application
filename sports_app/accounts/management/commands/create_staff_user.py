from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand

from sports_app.accounts.models import Profile


class Command(BaseCommand):
    help = 'Creates only staff user (no admin permissions)'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.UserModel = get_user_model()

    def handle(self, *args, **kwargs):
        user = self.UserModel(
            username=input("Username:"),
            is_staff=True,
        )
        user.set_password(input("Password:"))

        user.full_clean()
        user.save()

        staff_group, created = Group.objects.get_or_create(
            name="staff_group"
        )

        change_article_perm = Permission.objects.filter(codename="change_article").first()
        delete_article_perm = Permission.objects.filter(codename="delete_article").first()
        view_article_perm = Permission.objects.filter(codename="view_article").first()
        staff_group.permissions.add(change_article_perm)
        staff_group.permissions.add(delete_article_perm)
        staff_group.permissions.add(view_article_perm)

        staff_group.user_set.add(user)

        profile = Profile(
            first_name=input('First name:'),
            last_name=input('Last name:'),
            user=user
        )

        profile.full_clean()
        profile.save()

        self.stdout.write("Staff user created successfully!")

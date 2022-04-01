from django.contrib import admin

from sports_app.accounts.models import Profile, SportsAppUser


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')


@admin.register(SportsAppUser)
class UserModel(admin.ModelAdmin):
    list_display = ('username',)

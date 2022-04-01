from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth import forms as auth_forms

from sports_app.accounts.models import Profile
from sports_app.common.helpers import BootstrapFormMixin
from sports_app.main.models import Article

UserModel = get_user_model()


class CreateAccountForm(BootstrapFormMixin, auth_forms.UserCreationForm):
    first_name = forms.CharField(
        max_length=Profile.FIRST_NAME_MAX_LENGTH,
    )

    last_name = forms.CharField(
        max_length=Profile.LAST_NAME_MAX_LENGTH,
    )

    def save(self, commit=True):
        user = super().save(commit=commit)

        profile = Profile(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            user=user,
        )

        if commit:
            profile.save()
        return user

    class Meta:
        model = get_user_model()
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name')


class EditProfileForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    class Meta:
        model = Profile
        exclude = ('user',)
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter first name',
                }
            ),

            'last_name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter last name',
                }
            ),

            # 'picture': forms.ImageField(
            #     # attrs={
            #     #     'placeholder': 'Upload photo',
            #     # }
            # ),

            'email': forms.EmailInput(
                attrs={
                    'placeholder': 'Enter email',
                }
            ),

            'gender': forms.Select(
                choices=Profile.GENDERS,
            ),

            'date_of_birth':forms.DateInput(
                attrs={
                    'min': '1920-01-01',
                }
            )
        }


class DeleteProfileForm(forms.ModelForm):
    def save(self, commit=True):
        articles = list(self.instance.article_set.all())
        Article.objects.filter(user__in=articles).delete()
        self.instance.delete()

        return self.instance

    class Meta:
        model = UserModel
        fields = ()
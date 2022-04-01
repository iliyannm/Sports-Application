from django.contrib.auth import views as auth_views, login, get_user_model
from django.contrib.auth import mixins as auth_mixins
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic as views

from sports_app.accounts.forms import CreateAccountForm, EditProfileForm, DeleteProfileForm
from sports_app.accounts.models import Profile
from sports_app.common.view_mixins import RedirectToDashboard
from sports_app.main.models import Article

UserModel = get_user_model()


class UserRegistrationView(RedirectToDashboard, views.CreateView):
    form_class = CreateAccountForm
    template_name = 'accounts/profile_create.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, *args, **kwargs):
        result = super().form_valid(*args, **kwargs)
        login(self.request, self.object)
        return result


class UserLoginView(auth_views.LoginView):
    template_name = 'accounts/login_page.html'
    success_url = reverse_lazy('dashboard')

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        return super().get_success_url()


class UserLogoutView(auth_views.LogoutView):
    pass


class ChangePasswordView(auth_views.PasswordChangeView):
    template_name = 'accounts/change_password.html'


class ProfileDetailsView(auth_mixins.LoginRequiredMixin, views.DetailView, auth_mixins.PermissionRequiredMixin):
    model = Profile
    template_name = 'accounts/profile_details.html'
    context_object_name = 'profile'

    def get_permission_required(self):
        self.permission_required = (
            'sports_app.view_profile',
        )

        if self.permission_required is None:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} is missing the "
                f"permission_required attribute. Define "
                f"{self.__class__.__name__}.permission_required, or override "
                f"{self.__class__.__name__}.get_permission_required()."
            )
        if isinstance(self.permission_required, str):
            perms = (self.permission_required,)
        else:
            perms = self.permission_required
        return perms

    def has_permission(self):
        perms = self.get_permission_required()
        return self.request.user.has_perms(perms)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        articles = list(Article.objects.filter(user_id=self.object.user_id))
        total_articles_count = len(articles)

        context.update({
            'total_articles_count': total_articles_count,
            'is_owner': self.object.user_id == self.request.user.id,
            'articles': articles,
            'has_perm': self.has_permission(),
        })

        return context


class EditProfileView(views.UpdateView, auth_mixins.PermissionRequiredMixin):
    form_class = EditProfileForm
    template_name = 'accounts/profile_edit.html'
    context_object_name = 'profile'
    model = Profile

    def get_permission_required(self):
        self.permission_required = (
            'sports_app.change_profile',
        )

        if self.permission_required is None:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} is missing the "
                f"permission_required attribute. Define "
                f"{self.__class__.__name__}.permission_required, or override "
                f"{self.__class__.__name__}.get_permission_required()."
            )
        if isinstance(self.permission_required, str):
            perms = (self.permission_required,)
        else:
            perms = self.permission_required
        return perms

    def has_permission(self):
        perms = self.get_permission_required()
        return self.request.user.has_perms(perms)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        articles = list(Article.objects.filter(user_id=self.object.user_id))
        total_articles_count = len(articles)

        context.update({
            'total_articles_count': total_articles_count,
            'is_owner': self.object.user_id == self.request.user.id,
            'articles': articles,
            'has_perm': self.has_permission(),
        })

        return context

    def form_valid(self, form):
        profile = form.save()
        return redirect('profile details', pk=profile.pk)


class DeleteProfileView(views.DeleteView, auth_mixins.PermissionRequiredMixin):
    form_class = DeleteProfileForm
    template_name = 'accounts/profile_delete.html'
    context_object_name = 'profile'
    model = UserModel
    success_url = reverse_lazy('dashboard')

    def get_permission_required(self):
        self.permission_required = (
            'sports_app.delete_profile',
        )

        if self.permission_required is None:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} is missing the "
                f"permission_required attribute. Define "
                f"{self.__class__.__name__}.permission_required, or override "
                f"{self.__class__.__name__}.get_permission_required()."
            )
        if isinstance(self.permission_required, str):
            perms = (self.permission_required,)
        else:
            perms = self.permission_required
        return perms

    def has_permission(self):
        perms = self.get_permission_required()
        return self.request.user.has_perms(perms)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'is_owner': self.object.id == self.request.user.id,
            'has_perm': self.has_permission(),
        })

        return context

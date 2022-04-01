from django.urls import path, reverse_lazy
from django.views.generic import RedirectView

from sports_app.accounts.views import UserRegistrationView, UserLoginView, UserLogoutView, EditProfileView, \
    DeleteProfileView, ProfileDetailsView, ChangePasswordView

urlpatterns = (
    path('login/', UserLoginView.as_view(), name='login user'),
    path('logout/', UserLogoutView.as_view(next_page=reverse_lazy('dashboard')), name='logout user'),
    path('profile/create/', UserRegistrationView.as_view(), name='create profile'),
    path('profile/edit/<int:pk>', EditProfileView.as_view(), name='edit profile'),
    path('profile/delete/<int:pk>', DeleteProfileView.as_view(), name='delete profile'),
    path('profile/details/<int:pk>', ProfileDetailsView.as_view(), name='profile details'),
    path('change-password/', ChangePasswordView.as_view(), name='change password'),
    path('password-change-done/', RedirectView.as_view(url=reverse_lazy('dashboard')), name='password_change_done'),
)

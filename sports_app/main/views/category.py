from django.contrib.auth import mixins as auth_mixins
from django.urls import reverse_lazy
from django.views import generic as views

from sports_app.main.forms import CreateCategoryForm


class CreateCategoryView(auth_mixins.LoginRequiredMixin, views.CreateView):
    form_class = CreateCategoryForm
    template_name = 'main/create_category.html'
    success_url = reverse_lazy('create article')

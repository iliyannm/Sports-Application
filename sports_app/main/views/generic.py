from django.shortcuts import render
from django.views import generic as views

from sports_app.main.models import Article


class DashboardView(views.ListView):
    model = Article
    template_name = 'main/dashboard.html'
    context_object_name = 'articles'
    ordering = ('-publication_date',)


def page_not_found_view(request, exception):
    return render(request, 'main/404.html', status=404)

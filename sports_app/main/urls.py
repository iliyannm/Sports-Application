from django.urls import path

from sports_app.main.views.articles import CreateArticleView, EditArticleView, DeleteArticleView, ArticleDetailsView
from sports_app.main.views.category import CreateCategoryView
from sports_app.main.views.generic import DashboardView

urlpatterns = (
    path('', DashboardView.as_view(), name='dashboard'),

    path('article/create/', CreateArticleView.as_view(), name='create article'),
    path('article/edit/<int:pk>/', EditArticleView.as_view(), name='edit article'),
    path('article/delete/<int:pk>/', DeleteArticleView.as_view(), name='delete article'),
    path('article/details/<int:pk>/', ArticleDetailsView.as_view(), name='article details'),

    path('category/create/', CreateCategoryView.as_view(), name='create category'),
)

from django.contrib import admin

from sports_app.main.models import Article, ArticleComment, ArticleSportCategory


class ArticleInlineAdmin(admin.StackedInline):
    model = Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')


@admin.register(ArticleComment)
class ArticleCommentAdmin(admin.ModelAdmin):
    pass


@admin.register(ArticleSportCategory)
class ArticleSportCategoryAdmin(admin.ModelAdmin):
    pass

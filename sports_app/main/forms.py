from django import forms
from django.contrib.auth import mixins as auth_mixins

from sports_app.common.helpers import BootstrapFormMixin
from sports_app.main.models import Article, ArticleComment, ArticleSportCategory


class CreateArticleForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self._init_bootstrap_form_controls()

    def save(self, commit=True):
        article = super().save(commit=False)
        article.user = self.user
        if commit:
            article.save()

        return article

    class Meta:
        model = Article
        fields = ('title', 'photo', 'description', 'article_category')


class EditArticleForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    class Meta:
        model = Article
        exclude = ('user',)


class DeleteArticleForm(BootstrapFormMixin, forms.ModelForm):
    def save(self, commit=True):
        self.instance.delete()

        return self.instance

    class Meta:
        model = Article
        fields = ()


class CreateCommentForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = ArticleComment
        fields = ('comment',)


class CreateCategoryForm(auth_mixins.LoginRequiredMixin, BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = ArticleSportCategory
        fields = ('category',)

from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic as views
from django.contrib.auth import mixins as auth_mixins

from sports_app.accounts.models import Profile
from sports_app.main.forms import CreateArticleForm, EditArticleForm, DeleteArticleForm, CreateCommentForm
from sports_app.main.models import Article, ArticleComment, ArticleSportCategory


class CreateArticleView(auth_mixins.LoginRequiredMixin, views.CreateView):
    form_class = CreateArticleForm
    template_name = 'main/create_article.html'
    success_url = reverse_lazy('dashboard')

    # def dispatch(self, request, *args, **kwargs):
    #     if not request.user.is_authenticated:
    #         return HttpResponseRedirect(reverse('login user'))
    #
    #     return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class EditArticleView(views.UpdateView, auth_mixins.PermissionRequiredMixin):
    template_name = 'main/edit_article.html'
    form_class = EditArticleForm
    model = Article

    def get_permission_required(self):
        self.permission_required = (
            'sports_app.change_article',
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
            'is_owner': self.object.user_id == self.request.user.id,
            'has_perm': self.has_permission(),
        })

        return context

    def form_valid(self, form):
        article = form.save()
        return redirect('article details', pk=article.pk)


class DeleteArticleView(views.DeleteView, auth_mixins.PermissionRequiredMixin):
    form_class = DeleteArticleForm
    template_name = 'main/delete_article.html'
    context_object_name = 'article'
    model = Article
    success_url = reverse_lazy('dashboard')

    def get_permission_required(self):
        self.permission_required = (
            'sports_app.delete_article',
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
            'is_owner': self.object.user_id == self.request.user.id,
            'has_perm': self.has_permission(),
        })

        return context


class ArticleDetailsView(auth_mixins.LoginRequiredMixin, views.DetailView, auth_mixins.PermissionRequiredMixin):
    model = Article
    template_name = 'main/article_details.html'
    context_object_name = 'article'

    # def get_permission_required(self):
    #     self.permission_required = (
    #         'sports_app.view_article',
    #     )
    #
    #     if self.permission_required is None:
    #         raise ImproperlyConfigured(
    #             f"{self.__class__.__name__} is missing the "
    #             f"permission_required attribute. Define "
    #             f"{self.__class__.__name__}.permission_required, or override "
    #             f"{self.__class__.__name__}.get_permission_required()."
    #         )
    #     if isinstance(self.permission_required, str):
    #         perms = (self.permission_required,)
    #     else:
    #         perms = self.permission_required
    #     return perms
    #
    # def has_permission(self):
    #     perms = self.get_permission_required()
    #     return self.request.user.has_perms(perms)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        comments = ArticleComment.objects.filter(article_to_comment_id=self.object.id)
        category = ArticleSportCategory.objects.get(id=self.object.article_category_id)

        creator = Profile.objects.get(user_id=self.object.user_id)

        profiles = set()

        com_len = len(comments)

        for com in comments:
            pro = Profile.objects.get(user_id=com.user_id)
            profiles.add(pro)

        if not self.request.user.has_perms('sports_app.view_article'):
            redirect('dashboard')

        context.update({
            'is_owner': self.object.user_id == self.request.user.id,
            'comments': comments,
            'profiles': profiles,
            'category': category,
            'com_len': com_len,
            'creator': creator,
            'has_perm': self.request.user.has_perms('sports_app.view_article'),
        })

        if self.request.user.is_authenticated:
            context['comment_form'] = CreateCommentForm(instance=self.request.user)

        return context

    def post(self, request, *args, **kwargs):
        new_comment = ArticleComment(
            comment=request.POST.get('comment'),
            user=self.request.user,
            article_to_comment=self.get_object()
        )

        new_comment.save()
        return self.get(self, request, *args, **kwargs)

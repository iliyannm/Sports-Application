from django.contrib.auth.models import Group
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic as views
from django.contrib.auth import mixins as auth_mixins, get_user_model

from sports_app.accounts.models import Profile
from sports_app.main.forms import CreateArticleForm, EditArticleForm, DeleteArticleForm, CreateCommentForm
from sports_app.main.models import Article, ArticleComment, ArticleSportCategory

User = get_user_model()


class CreateArticleView(auth_mixins.LoginRequiredMixin, views.CreateView):
    form_class = CreateArticleForm
    template_name = 'main/create_article.html'
    success_url = reverse_lazy('dashboard')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class EditArticleView(views.UpdateView):
    template_name = 'main/edit_article.html'
    form_class = EditArticleForm
    model = Article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        staff_group = Group.objects.filter(name="staff_group").first()

        context.update({
            'is_owner': self.object.user_id == self.request.user.id,
            'has_perm': staff_group in self.request.user.groups.all(),
            'is_superuser': self.request.user.is_superuser,
        })

        return context

    def form_valid(self, form):
        article = form.save()
        return redirect('article details', pk=article.pk)


class DeleteArticleView(views.DeleteView):
    form_class = DeleteArticleForm
    template_name = 'main/delete_article.html'
    context_object_name = 'article'
    model = Article
    success_url = reverse_lazy('dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        staff_group = Group.objects.filter(name="staff_group").first()

        context.update({
            'is_owner': self.object.user_id == self.request.user.id,
            'has_perm': staff_group in self.request.user.groups.all(),
            'is_superuser': self.request.user.is_superuser,
        })

        return context


class ArticleDetailsView(auth_mixins.LoginRequiredMixin, views.DetailView):
    model = Article
    template_name = 'main/article_details.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        comments = ArticleComment.objects.filter(article_to_comment_id=self.object.id)
        category = ArticleSportCategory.objects.get(id=self.object.article_category_id)

        creator = Profile.objects.get(user_id=self.object.user_id)

        comentators_ids = comments.values_list("user_id", flat=True)
        comentator_profiles = Profile.objects.filter(
            user_id__in=comentators_ids
        )

        staff_group = Group.objects.filter(name="staff_group").first()

        context.update({
            'is_owner': self.object.user_id == self.request.user.id,
            'comments': comments,
            'profiles': comentator_profiles,
            'category': category,
            'com_len': comments.count(),
            'creator': creator,
            'has_perm': staff_group in self.request.user.groups.all(),
            'comment_form': CreateCommentForm(instance=self.request.user),
            'is_superuser': self.request.user.is_superuser,
        })

        return context

    def post(self, request, *args, **kwargs):
        new_comment = ArticleComment(
            comment=request.POST.get('comment'),
            user=self.request.user,
            article_to_comment=self.get_object()
        )

        new_comment.save()
        return self.get(self, request, *args, **kwargs)

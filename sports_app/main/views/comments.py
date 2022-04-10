from django.views import generic as views

from sports_app.main.forms import CreateCommentForm


class CreateCommentView(views.CreateView):
    form_class = CreateCommentForm
    template_name = 'main/article_details.html'
    context_object_name = 'article'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super().form_valid(form)
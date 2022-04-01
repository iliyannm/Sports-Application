from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()


class ArticleSportCategory(models.Model):
    CATEGORY_MAX_LENGTH = 30

    category = models.CharField(
        max_length=CATEGORY_MAX_LENGTH,
        unique=True,
    )

    def __str__(self):
        return self.category


class Article(models.Model):
    TITLE_MAX_LENGTH = 200

    title = models.CharField(
        max_length=TITLE_MAX_LENGTH,
        unique=True,
    )

    publication_date = models.DateTimeField(
        auto_now_add=True,
    )

    photo = models.ImageField()

    description = models.TextField()

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    article_category = models.ForeignKey(
        ArticleSportCategory,
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('user', 'title')

    def __str__(self):
        return self.title


class ArticleComment(models.Model):

    comment = models.TextField()

    article_to_comment = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.comment

from django.db import models


class Category(models.Model):
    name = models.CharField(
        max_length=40,
        unique=True,
    )

    slug = models.SlugField(
        unique=True,
    )

    def active_articles_list(self):
        return self.article_set.filter(
            is_active=True,
            is_private=False
        )

    def get_absolute_url(self):
        return reverse(
            'CategoryDefaultView',
            args=[
            str(
                self.slug
                )
            ]
        )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Article(models.Model):
    category = models.ForeignKey(Category)

    name = models.CharField(
        max_length=40,
        unique=True,
    )

    slug = models.SlugField()

    is_active = models.BooleanField(
        default=True,
    )

    is_private = models.BooleanField()

    content = models.TextField()

    upvotes = models.PositiveIntegerField(
        default=0,
        editable=False,
    )

    downvotes = models.PositiveIntegerField(
        default=0,
        editable=False,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def get_absolute_url(self):
        return reverse(
            'ArticleDefaultView',
            args=[
            str(
                self.slug
                )
            ]
        )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        unique_together = ('category', 'slug')

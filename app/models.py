from django.db import models


class Category(models.Model):
    name = models.CharField(
        max_length=40,
        unique=True,
    )

    slug = models.SlugField(
        unique=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


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

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        unique_together = ('category', 'slug')

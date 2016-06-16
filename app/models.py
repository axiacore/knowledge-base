from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.module_loading import import_string


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
        )

    def get_absolute_url(self):
        return reverse(
            'category_detail',
            args=[self.slug]
        )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class ActiveArticlesManager(models.Manager):
    def get_queryset(self):
        return super(ActiveArticlesManager, self).get_queryset().filter(
            is_active=True,
        )


class PublicArticlesManager(ActiveArticlesManager):
    def get_queryset(self):
        return super(PublicArticlesManager, self).get_queryset().filter(
            is_private=False,
        )


class Article(models.Model):
    category = models.ForeignKey(Category)

    name = models.CharField(
        max_length=50,
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

    objects = models.Manager()

    active = ActiveArticlesManager()

    public = PublicArticlesManager()

    @property
    def content_markdown(self):
        markdownify = import_string(settings.MARKDOWNX_MARKDOWNIFY_FUNCTION)
        return markdownify(self.content)

    def get_absolute_url(self):
        return reverse(
            'article_detail',
            args=[self.category.slug, self.slug]
        )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        unique_together = ('category', 'slug')

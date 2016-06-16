from django.test import TestCase
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse

from .models import Category
from .models import Article


class CategoryTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Category A',
            slug='catageory-a'
        )


class ArticleTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Category A',
            slug='catageory-a'
        )
        self.article_1 = Article.objects.create(
            category=self.category,
            name='Article one name',
            slug='article-one-name',
            is_active=True,
            is_private=False,
            content='Article one content'
            )
        self.article_2 = Article.objects.create(
            category=self.category,
            name='Article two name',
            slug='article-two-name',
            is_active=True,
            is_private=True,
            content='Article twoo content'
            )
        self.article_3 = Article.objects.create(
            category=self.category,
            name='Article three name',
            slug='article-three-name',
            is_active=False,
            is_private=False,
            content='Article three content'
            )

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
            slug='catagory-a'
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

        def test_public_article_view(self):
            response = self.client.get(reverse(
                    'article_detail',
                    args=[self.article_1.slug]
                ))
            self.assertEqual(response.status_code, 200)

        def test_unlogin_private_article_view(self):
            response = self.client.get(reverse(
                    'article_detail',
                    args=[self.article_2.slug]
                ))
            self.assertEqual(response.status_code, 400)

        def test_login_private_article_view(self):
            self.client.login(username='admin', password='demo')
            response = self.client.get(reverse(
                    'article_detail',
                    args=[self.article_2.slug]
                ))
            self.assertEqual(response.status_code, 200)


        def test_unactive_article(self):
            response = self.client.get(reverse(
                    'article_detail',
                    args=[self.article_3.slug]
                ))
            self.assertEqual(response.status_code, 400)

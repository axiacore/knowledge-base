from django.contrib.auth.models import User
from django.test import TestCase

from .models import Article
from .models import Category


class CategoryTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Category',
            slug='category',
        )


class ArticleTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='pass')

        self.category = Category.objects.create(
            name='Category',
            slug='category',
        )

        self.article_1 = Article.objects.create(
            category=self.category,
            name='Active and public article',
            slug='active-and-public',
            is_active=True,
            is_private=False,
            content='Article one content'
        )

        self.article_2 = Article.objects.create(
            category=self.category,
            name='Active and private article',
            slug='active-and-private',
            is_active=True,
            is_private=True,
            content='Article two content'
        )

        self.article_3 = Article.objects.create(
            category=self.category,
            name='Non active article',
            slug='non-active-article',
            is_active=False,
            is_private=False,
            content='Article three content'
        )

    def test_public_article_view(self):
        """Test a public article can be viewed"""
        response = self.client.get(self.article_1.get_absolute_url())
        self.assertContains(response, self.article_1.name)

    def test_private_article_view(self):
        """Test a private article cannot be viewed by an unauthenticated user
        """
        response = self.client.get(self.article_2.get_absolute_url())
        self.assertEqual(response.status_code, 404)

    def test_private_article_view_authenticated(self):
        """Test a private article can be viewed by an authenticated user"""
        self.client.login(username='user', password='pass')
        response = self.client.get(self.article_2.get_absolute_url())
        self.assertContains(response, self.article_2.name)

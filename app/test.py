from django.test import TestCase
from django.template.defaultfilters import slugify

from .models import Category
from .models import Article


class CategoryTest(TestCase):
    """docstring for Category"""
    def setUp(self):
        self.category = Category.objects.create(
            name='Clientes',
            slug=slugify('Clientes')
        )


class ArticleTest(object):
    """docstring for ArticleTest"""
    def setUp(self):
        self.article_1 = Article.objects.create(
            category=2,
            name='Como hacer test en django',
            slug=slugify('Como hacer test en django'),
            is_active=True,
            is_private=False,
            content='Lorem ipsum dolor sit amet, consectetur adipisicing elit. Beatae quibusdam incidunt, earum pariatur excepturi accusantium minus nulla dolorum laborum, quam natus quos consequatur. Provident, dolores accusamus reprehenderit, repellendus quas delectus. Publio Cornelio Scipion Africanus.'
            )
        self.article_2 = Article.objects.create(
            category=2,
            name='Como probar test en django',
            slug=slugify('Como probar test en django'),
            is_active=True,
            is_private=True,
            content='Lorem ipsum dolor sit amet, consectetur adipisicing elit. Beatae quibusdam incidunt, earum pariatur excepturi accusantium minus nulla dolorum laborum, quam natus quos consequatur. Provident, dolores accusamus reprehenderit, repellendus quas delectus. Gaius Iulius Caesar.'
            )
        self.article_3 = Article.objects.create(
            category=2,
            name='Como no hacer test en django',
            slug=slugify('Como no hacer test en django'),
            is_active=False,
            is_private=False,
            content='Lorem ipsum dolor sit amet, consectetur adipisicing elit. Beatae quibusdam incidunt, earum pariatur excepturi accusantium minus nulla dolorum laborum, quam natus quos consequatur. Provident, dolores accusamus reprehenderit, repellendus quas delectus. Gaius Marcius Coriolanus.'
            )


from django.contrib import admin
from django.db import models

from .models import Article
from .models import Category

from markdownx.widgets import AdminMarkdownxWidget


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
    ]

    list_editable = ['name']

    prepopulated_fields = {'slug': ('name',)}


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'category',
        'upvotes',
        'downvotes',
        'is_active',
        'is_private',
    ]

    prepopulated_fields = {'slug': ('name',)}

    list_filter = [
        'category',
        'is_active',
        'is_private',
    ]

    list_editable = [
        'name',
        'category'
    ]

    search_fields = [
        'name',
        'content',
    ]

    formfield_overrides = {
        models.TextField: {'widget': AdminMarkdownxWidget},
    }

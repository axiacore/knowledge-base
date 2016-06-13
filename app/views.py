from django.views.generic import ListView

from .models import Category


class HomeView(ListView):
    template_name = 'home.html'
    model = Category
    context_object_name = 'category_list'

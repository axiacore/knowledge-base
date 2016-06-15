from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.postgres.search import SearchVector
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _
from django.views.generic import DetailView
from django.views.generic import FormView
from django.views.generic import ListView

from itsdangerous import BadSignature
from itsdangerous import BadTimeSignature
from itsdangerous import URLSafeTimedSerializer

from .forms import LoginForm
from .forms import SearchForm
from .models import Article
from .models import Category


class HomeView(ListView):
    template_name = 'home.html'

    def get_queryset(self):
        if self.request.user.is_authenticated():
            return Article.active.all()

        return Article.public.all()

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['form'] = SearchForm()
        return context


class CategoryDetailView(DetailView):
    model = Category


class ArticleDetailView(DetailView):
    model = Article

    def get_object(self):
        return get_object_or_404(
            Article,
            slug=self.kwargs['slug'],
            category__slug=self.kwargs['category_slug'],
        )


class SearchResultsListView(ListView):
    model = Article
    template_name = 'app/search_results_list.html'

    def get_queryset(self):
        search = self.request.GET.get('text', '')
        return Article.objects.annotate(
            search=SearchVector(
                'content',
                'name',
                config=settings.SEARCH_LANGS[
                    settings.LANGUAGE
                ]
            )
        ).filter(
            search=search
        )[:20]

    def get_context_data(self, **kwargs):
        context = super(SearchResultsListView, self).get_context_data(**kwargs)
        context['form'] = SearchForm(self.request.GET)
        return context


class ArticleUpVoteView(DetailView):
    model = Article

    def get(self, request, *args, **kwargs):
        article = self.get_object()
        voted_list = request.session.get('voted_article_list', [])

        if article.id not in voted_list:
            voted_list.append(article.id)
            request.session['voted_article_list'] = voted_list
            article.upvotes = F('upvotes') + 1
            article.save()
            return JsonResponse({'already_voted': False})

        return JsonResponse({'already_voted': True})


class ArticleDownVoteView(DetailView):
    model = Article

    def get(self, request, *args, **kwargs):
        article = self.get_object()
        voted_list = request.session.get('voted_article_list', [])

        if article.id not in voted_list:
            voted_list.append(article.id)
            request.session['voted_article_list'] = voted_list
            article.downvotes = F('downvotes') + 1
            article.save()
            return JsonResponse({'already_voted': False})

        return JsonResponse({'already_voted': True})


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        if request.GET.get('key'):
            serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
            try:
                user_id = serializer.loads(
                    request.GET.get('key'),
                    max_age=60 * 2,     # Signature expires after 2 minutes
                )
                user = get_object_or_404(User, id=user_id)
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)

                return redirect('home')
            except (BadSignature, BadTimeSignature):
                return redirect('login')

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        email = form.cleaned_data['email']
        user = User.objects.get(email__iexact=email)
        safe = URLSafeTimedSerializer(settings.SECRET_KEY)
        url = '{site}{path}?key={key}'.format(
            site=settings.SITE_URL,
            path=reverse('login'),
            key=safe.dumps(user.id),
        )

        send_mail(
            _('Link to login into the Knowledge Base'),
            url,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
            html_message=render_to_string(
                'login_email.html', {'url': url}
            ),
        )

        return redirect('home')

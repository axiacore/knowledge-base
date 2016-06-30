from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.postgres.search import SearchQuery
from django.contrib.postgres.search import SearchVector
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.db.models import F
from django.http import Http404
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _
from django.views.generic import DetailView
from django.views.generic import FormView
from django.views.generic import ListView
from django.shortcuts import render
from django.contrib import messages
from django.core.mail.message import EmailMessage
from django.contrib.sites.models import Site

from itsdangerous import BadSignature
from itsdangerous import BadTimeSignature
from itsdangerous import URLSafeTimedSerializer

from .forms import LoginForm
from .forms import SearchForm
from .forms import FeedbackForm
from .models import Article
from .models import Category


class HomeView(ListView):
    template_name = 'home.html'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            queryset = Article.actives.all()
        else:
            queryset = Article.publics.all()

        return queryset.order_by('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SearchForm()
        return context


class CategoryDetailView(DetailView):
    model = Category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            context['article_list'] = Article.actives.filter(
                category=self.get_object(),
            )
        else:
            context['article_list'] = Article.publics.filter(
                category=self.get_object(),
            )

        return context


class ArticleDetailMixin(DetailView):
    model = Article

    def get_object(self):
        if self.request.user.is_authenticated:
            article = Article.actives.filter(
                slug=self.kwargs['slug'],
                category__slug=self.kwargs['category_slug'],
            ).first()
        else:
            article = Article.publics.filter(
                slug=self.kwargs['slug'],
                category__slug=self.kwargs['category_slug'],
            ).first()

        if not article:
            raise Http404

        return article

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailMixin, self).get_context_data(**kwargs)
        voted_list = self.request.session.get('voted_article_list', [])

        context.update({
            'feedback_form': FeedbackForm(),
            'already_voted': self.object.id in voted_list,
        })

        return context


class ArticleDetailView(ArticleDetailMixin):
    pass


class ArticleDetailFeedbackView(ArticleDetailMixin):
    def post(self, request, *args, **kwargs):
        """ Sends the feedback email to admin.
        """
        obj = self.get_object()
        form = FeedbackForm(request.POST)
        if not form.is_valid():
            return render(request, 'app/article_detail.html', {
                'feedback_form': form,
                'object': obj,
                'already_voted': False,
                'display_form': True,
            })

        base_url = 'http://{0}'.format(Site.objects.get_current().domain)
        email = form.cleaned_data['email']
        email_message = EmailMessage(
            subject=_('New feedback from article {0}'.format(obj.name)),
            body=render_to_string('feedback_email.html', {
                'feedback_message': form.cleaned_data['description'],
                'feedback_email': email,
                'article': obj,
                'base_url': base_url,
            }),
            to=[settings.SUPPORT_EMAIL],
            reply_to=[email],
        )
        email_message.content_subtype = 'html'
        email_message.send()

        messages.success(
            request,
            _('Thank you for sending your feedback!')
        )
        return redirect(obj)


class SearchResultsListView(ListView):
    model = Article
    template_name = 'app/article_search.html'

    def get_queryset(self):
        search_query = SearchQuery(
            self.request.GET.get('q', ''),
            config=settings.SEARCH_LANGS[settings.LANGUAGE_CODE],
        )

        vector = SearchVector(
            'name',
            'content',
            config=settings.SEARCH_LANGS[settings.LANGUAGE_CODE],
        )

        if self.request.user.is_authenticated:
            queryset = Article.actives.all()
        else:
            queryset = Article.publics.all()

        return queryset.annotate(search=vector,).filter(search=search_query)

    def get_context_data(self, **kwargs):
        context = super(SearchResultsListView, self).get_context_data(**kwargs)
        context['form'] = SearchForm(self.request.GET)
        return context


class ArticleUpVoteView(ArticleDetailView):
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


class ArticleDownVoteView(ArticleDetailView):
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
                    max_age=60 * 2,  # Signature expires after 2 minutes
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
        user = User.objects.get(username=email)
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

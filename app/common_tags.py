from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def get_conditional_articles(context, query_set):
    if context.user.is_authenticated():
        return query_set

    return query_set.filter(
        is_private=False
    )

from django import template
from django.template.defaultfilters import stringfilter
from ..models import Post

register = template.Library()


@register.simple_tag
def total_posts():
    return Post.objects.count()


@register.filter()
@stringfilter
def huilovanie(value):
    return "Хуйло" + value

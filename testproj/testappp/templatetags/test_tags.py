__author__ = 'lex'
from django import template
register = template.Library()
from django.core import urlresolvers
from django.contrib.contenttypes.models import ContentType


@register.simple_tag
def edit_link(model):
    content_type = ContentType.objects.filter(
        name__iexact=model.__class__.__name__
    )[0]
    str = urlresolvers.reverse(
        'admin:{0}_{1}_change'.format(
            content_type.app_label,
            content_type.model
        ),
        args=(model.id,)
    )
    print str
    return str

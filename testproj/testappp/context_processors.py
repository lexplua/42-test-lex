__author__ = 'lex'
from django.conf import settings


def setting_adder(request):
    return {
        'settings': settings,
    }
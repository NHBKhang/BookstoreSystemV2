from django.test import TestCase
from django.core.cache import cache


def clear_cache():
    cache.clear()

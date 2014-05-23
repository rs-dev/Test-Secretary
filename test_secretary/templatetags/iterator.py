from django import template

register = template.Library()


@register.filter
def next(value):
    return value.__next__()

from django import template

register = template.Library()

@register.filter
def num_format(num, fmt=","):
    if not isinstance(num, int) and not isinstance(num, float):
        return num
    return format(num, fmt)
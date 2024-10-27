from django import template

register = template.Library()

@register.filter
def num_format(num):
    if not isinstance(num, int) and not isinstance(num, float):
        return num
    return f"{num:,}"
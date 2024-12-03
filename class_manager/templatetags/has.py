from django import template

register = template.Library()

@register.filter
def has(obj, att):
    if isinstance(obj, dict):
        return att.strip() in obj
    return hasattr(obj, att.strip())
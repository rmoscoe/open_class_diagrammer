from django import template

register = template.Library()

@register.filter
def sanitize(text):
    opening = text.replace("<", "&lt;")
    return opening.replace(">", "&gt;")
from django import template

register = template.Library()

@register.filter
def has(obj, att):
    if isinstance(obj, dict):
        att_in_obj = att.strip() in obj
        return att_in_obj
    obj_has_att = hasattr(obj, att.strip())
    return obj_has_att
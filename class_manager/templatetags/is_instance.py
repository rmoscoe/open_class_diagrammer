from django import template
from django.db.models.query import QuerySet
from ..models import *

register = template.Library()

@register.filter
def is_instance(obj, type_names):
    type_names = type_names.split("|")
    types = {
        'int': int,
        'float': float,
        'str': str,
        'bool': bool,
        'complex': complex,
        'list': list,
        'tuple': tuple,
        'range': range,
        'set': set,
        'dict': dict,
        'queryset': QuerySet,
        'project': Project,
        'module': Module,
        'class': Class,
        'property': Property,
        'method': Method,
        'relationship': Relationship,
        'none': None
    }
    
    def check_type(obj, type_name):
        lc_name = type_name.lower().strip()
        if lc_name not in types:
            for v in types.values():
                if isinstance(obj, v):
                    return False
            return True
        return isinstance(obj, types.get(lc_name))
    
    for type_name in type_names:
        if check_type(obj, type_name):
            return True
    return False

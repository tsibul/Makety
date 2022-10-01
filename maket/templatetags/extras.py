from django import template
register = template.Library()


@register.filter
def replace_value(value, name):
    name = str(name)
    return value.replace('**', name)
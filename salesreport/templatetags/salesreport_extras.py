from django import template

register = template.Library()


@register.filter
def replace_val(value, name):
    name = str(name)
    return value.replace('**', name)


@register.filter
def print_name_to_string_(inp, output):
    return inp.replace('**', output)

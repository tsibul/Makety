from django import template
register = template.Library()


@register.filter
def replace_value(value, name):
    name = str(name)
    return value.replace('**', name)


@register.filter
def print_name_to_string_(input, output):
    output = output.replace(' ', '_').replace(',', '').replace('+', '_')
    return input.replace('**', output)

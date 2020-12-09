from django import template
register = template.Library()

@register.filter(name="mod")
def mod(value):
    result = value %12 +1
    return result

@register.filter(name="cut")
def cut(value):
    distance = str(value)
    result = distance[:10]
    return result
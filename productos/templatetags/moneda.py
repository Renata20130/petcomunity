from django import template

register = template.Library()

@register.filter
def clp(value):
    try:
        value = int(value)
        return "${:,.0f}".format(value).replace(",", ".")
    except:
        return value

from django import template

register = template.Library()


@register.filter
def jdate(value, format):
    """
    format date based on given format
    """
    return value.strftime(format)

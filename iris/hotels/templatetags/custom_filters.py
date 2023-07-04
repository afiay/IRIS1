from django import template

register = template.Library()

@register.filter
def get_range(value):
    return range(value)

@register.filter
def get_value_from_dict(dictionary, key):
    return dictionary.get(key)

@register.filter
def split_weekheader(weekheader):
    return weekheader.split()
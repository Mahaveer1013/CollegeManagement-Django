from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    print('custom filter', dictionary, key)
    print(dictionary.get(key))
    return dictionary.get(key)

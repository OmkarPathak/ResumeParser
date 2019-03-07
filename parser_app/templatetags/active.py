from django import template
from django.shortcuts import reverse

register = template.Library()

@register.simple_tag
def add_active(request, name, slug):
    if slug:
        path = reverse(name, kwargs={'slug': slug})
    else :
        path = reverse(name)
    print(path)
    if request.path == path:
        return "active"
    return ""

@register.filter(name='add_css')
def add_css(field, css):
    """Removes all values of arg from the given string"""
    return field.as_widget(attrs={"class": css})

@register.filter
def index(List, i):
    return List[int(i)]
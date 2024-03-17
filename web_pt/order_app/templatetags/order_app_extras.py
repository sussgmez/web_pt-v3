from django import template
register = template.Library()

@register.filter
def is_none(value):
    if value == None or value == "": return "---- ----"
    else : return value

@register.filter
def if_input_none(value):
    if value == None or value == "": return ""
    else : return value

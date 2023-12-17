from django import template


register = template.Library()


@register.filter()
def censor(string):
    if isinstance(string, str):
        return f'{string[0]}' + '*' * (len(string)-1)
    else:
        raise TypeError

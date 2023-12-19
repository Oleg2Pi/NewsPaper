from django import template


register = template.Library()

STRING_NOT = [
    'дискриминация',
]

ZNAKI = ',.;!?-'

@register.filter()
def censor(text):
    if isinstance(text, str):
        text1 = []
        for string in text.split():
            for string_not in STRING_NOT:
                if string.lower().startswith(string_not[:-4]):
                    if string[-1] in ZNAKI:
                        string = string[0] + '*' * len(string[1:-1]) + string[-1]
                    else:
                        string = string[0] + '*' * len(string[1:-1])
            text1.append(string)
    else:
        raise TypeError
    
    return " ".join(text1)

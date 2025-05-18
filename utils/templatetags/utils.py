import string
from django import template
from django.template.defaultfilters import stringfilter

words_dict = {
    "acao": "ação",
    "liquidacoes": "liquidações",
    "gestao": "gestão",
    "ciencia": "ciência",
    "relatorio": "relatório",
}

register = template.Library()


@register.filter(is_safe=True)
@stringfilter
def split(value: str, splitchar: str):
    parts = value.split(splitchar)[1:]

    if value[-1] == "/":
        return parts[:-1]

    return parts


@register.filter(is_safe=True)
@stringfilter
def get_nth_part_of_url(value: str, n: int):
    print(value)
    idx = 1
    for _ in range(0, n):
        idx += value[idx:].find("/") + 1

    return value[:idx]


@register.filter(is_safe=True)
@stringfilter
def format_path(value: str):
    value = value.replace("_", " ")

    words = value.split()
    for i, word in enumerate(words):
        new_word = words_dict.get(word)
        if new_word is not None:
            words[i] = new_word

    return string.capwords(" ".join(words))


register.tag("split", split)
register.tag("format_path", format_path)
register.tag("get_nth_part_of_url", get_nth_part_of_url)

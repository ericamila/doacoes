from django import template

register = template.Library()

@register.filter(name="admin")
def is_admin(user):
    if hasattr(user, "situacao") and hasattr(user, "tipo_usuario"):
        print(user.situacao, user.tipo_usuario)
        return user.situacao == 0 and user.tipo_usuario == 0
    return False

@register.filter(name="representante_de_municipio")
def is_representante_de_municipo(user):
    if hasattr(user, "situacao") and hasattr(user, "tipo_usuario"):
        return user.situacao == 0 and user.tipo_usuario == 1
    return False

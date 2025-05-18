from django.contrib.auth.decorators import user_passes_test


def is_admin(user):
    return user.is_authenticated and user.situacao == 0 and user.tipo_usuario == 0


admin_required = user_passes_test(is_admin)

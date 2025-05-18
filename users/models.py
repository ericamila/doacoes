from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from utils.models import Municipio


class Usuario(AbstractUser, models.Model):
    cpf = models.CharField(max_length=11, unique=True)
    codigo_sei = models.CharField(max_length=50)
    telefone = models.CharField(max_length=15)
    tipo_usuario = models.IntegerField(
        choices=[
            (0, "Administrador"),
            (1, "Representante de Município"),
        ],
        default=1,
    )
    situacao = models.IntegerField(
        choices=[
            (0, "Ativo"),
            (1, "Inativo"),
            (2, "Pendente"),
        ],
        default=2,
    )
    municipios = models.ForeignKey(Municipio, null=True, on_delete=models.SET_NULL)
    removido_em = models.DateTimeField(null=True, blank=True)

    # Adicione os related_names para evitar conflitos
    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_set",  # Nome único para evitar conflito
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions_set",  # Nome único para evitar conflito
        blank=True
    )

    class Meta:
        db_table = "usuarios"

    def __str__(self):
        return self.first_name

from django.db import models
from django.utils import timezone

LISTA_CATEGORIAS = (("Especial", "Especial"),)


# Create your models here.
class Project(models.Model):
    nome = models.CharField(max_length=200, null=True, blank=True)
    ano = models.IntegerField(default=timezone.now().year)
    tipo_de_transferencia = models.CharField(
        max_length=50, choices=LISTA_CATEGORIAS, default="Especial"
    )
    codigo = models.CharField(max_length=100, null=True, unique=True)
    orgao_de_origem = models.CharField(max_length=200, null=True)
    orgao_repassador = models.CharField(max_length=200, null=True)
    unidade_gestora = models.CharField(max_length=100, null=True)
    unidade_orcamentaria = models.CharField(max_length=200, null=True)
    data_inicial_ciencia = models.DateField()
    data_final_ciencia = models.DateField()
    descricao = models.TextField(max_length=1000, blank=True)
    removido_em = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "projects"
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def __str__(self):
        return f'{self.ano}/{self.codigo}'


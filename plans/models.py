from django.db import models

# Create your models here.
from django.db import models

from proposals.models import Proposal
from utils.models import PoliticaPublica


# Create your models here.

# Modelo para PLANOS
class Plan(models.Model):
    codigo = models.CharField(max_length=50, null=False)
    descricao_politicas_publicas = models.TextField(null=False)
    proposal = models.ForeignKey(Proposal, on_delete=models.CASCADE)
    politicas_publicas = models.ManyToManyField(PoliticaPublica)
    removido_em = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "plans"
        verbose_name = "Plano"
        verbose_name_plural = "Planos"

    def __str__(self):
        return f"{self.codigo} - {self.descricao_politicas_publicas[:50]}"



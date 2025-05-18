from django.db import models
from projects.models import Project
from utils.models import ContaBancaria, Parlamentar, Municipio, PoliticaPublica


# Modelo da propostas
class Proposal(models.Model):
    ano = models.IntegerField()
    codigo = models.CharField(max_length=100)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    valor_custeio = models.DecimalField(max_digits=8, decimal_places=2)
    valor_investimento = models.DecimalField(max_digits=8, decimal_places=2)
    parlamentar = models.ForeignKey(Parlamentar, on_delete=models.CASCADE)
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE)
    conta_bancaria = models.ForeignKey(
        ContaBancaria, null=True, blank=True, on_delete=models.SET_NULL
    )
    descricao = models.TextField()
    ciente = models.BooleanField(default=False)
    data_ciencia = models.DateTimeField(null=True, blank=True)
    sei_remocao_ciente = models.CharField(max_length=100, null=True, blank=True)
    data_remocao_ciente = models.DateTimeField(null=True, blank=True)
    removido_em = models.DateTimeField(null=True, blank=True)

    def get_valor_total(self):
        return self.valor_custeio + self.valor_investimento

    class Meta:
        db_table = "proposals"
        verbose_name = "Proposta"
        verbose_name_plural = "Propostas"

    def __str__(self):
        return f'{self.ano}-{self.codigo} - {self.parlamentar.nome}'

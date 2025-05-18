from django.db import models
from plans.models import Plan

# Create your models here.
class Commitment(models.Model):
    codigo = models.TextField(null=False) 
    processo = models.TextField(null=False)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    data = models.DateField(null=False)
    valor = models.DecimalField(max_digits=12, decimal_places=2, null=False)
    valor_estornado = models.DecimalField(max_digits=12, decimal_places=2, null=False)
    situacao = models.CharField(
        max_length=30,
        choices=[
            ('Pendente', 'Pendente'),
            ('Concluido', 'Concluído'),
            ('Estornado Parcialmente', 'Estornado Parcialmente'),
            ('Estornado Totalmente', 'Estornado Totalmente'),
        ],
        null=False,
    )
    removido_em = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "commitments"
        verbose_name = "Empenho"
        verbose_name_plural = "Empenhos"

    def __str__(self):
        return f"Empenho {self.codigo} - {self.situacao}"


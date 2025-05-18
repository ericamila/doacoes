from django.db import models
from commitments.models import Commitment


class Settlement(models.Model):
    codigo = models.TextField(null=False)
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
    commitment = models.ForeignKey(Commitment, on_delete=models.CASCADE)
    data = models.DateField(null=False)
    valor = models.DecimalField(max_digits=12, decimal_places=2, null=False)
    valor_estornado = models.DecimalField(max_digits=12, decimal_places=2, null=False)
    removido_em = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "settlement"
        verbose_name = "Liquidação"
        verbose_name_plural = "Liquidações"

    def __str__(self):
        return f"Liquidação {self.codigo} - {self.situacao}"

from django.db import models
from settlement.models import Settlement

# Create your models here.
class Payment(models.Model):
    codigo = models.TextField(null=False)
    ordem_bancaria = models.TextField(null=False)
    settlement = models.ForeignKey(Settlement, on_delete=models.CASCADE)
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
        db_table = "payments"
        verbose_name = "Payment"
        verbose_name_plural = "Payments"

    def __str__(self):
        return f"Payment {self.codigo} - {self.situacao}"
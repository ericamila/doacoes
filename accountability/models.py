from django.db import models
from plans.models import Plan


# Define o caminho de upload baseado no ID do Accountability.
def upload_to_relatorio(instance, filename):
    return f"documentos/{instance.accountability.id}/{filename}"


class Accountability(models.Model):
    valor_executado = models.DecimalField(max_digits=12, decimal_places=2, null=False)
    natureza_despesa = models.CharField(max_length=50, null=False, choices=[
        ("investimento", "Investimento"),
        ("custeio", "Custeio"), ])
    descricao = models.TextField(null=False)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    data_criacao = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)
    removido_em = models.DateTimeField(null=True, blank=True)

    def get_valor_executado_custeio(self):
        if self.natureza_despesa == "custeio":
            return self.valor_executado
        return 0

    def get_valor_executado_investimento(self):
        if self.natureza_despesa == "investimento":
            return self.valor_executado
        return 0

    class Meta:
        db_table = "accountabilities"
        verbose_name = "Relatório de Gestão"
        verbose_name_plural = "Relatórios de Gestão"

    def __str__(self):
        return f"Relatório {self.id} - Valor Executado: {self.valor_executado}"


# Modelo para DOCUMENTOS
class Document(models.Model):
    nome = models.CharField(max_length=255, null=False)
    caminho = models.FileField(upload_to=upload_to_relatorio, null=False)  # Gerencia o upload de arquivos
    tamanho = models.IntegerField(null=False, blank=True)
    accountability = models.ForeignKey(Accountability, on_delete=models.CASCADE)
    removido_em = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "documents"
        verbose_name = "Documento"
        verbose_name_plural = "Documentos"

    def __str__(self):
        return self.nome
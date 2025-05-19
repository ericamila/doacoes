from django.db import models
from plans.models import Plan
from django.contrib.auth import get_user_model

Usuario = get_user_model()

# Define o caminho de upload baseado no ID do Accountability.
def upload_to_accountability(instance, filename):
    return f"documentos/{instance.accountability.id}/{filename}"

# Define o caminho de upload para documentos históricos
def upload_to_accountability_history(instance, filename):
    return f"documentos_history/{instance.accountability_history.id}/{filename}"


class Accountability(models.Model):
    NATUREZA_CHOICES = [
        ("investimento", "Investimento"),
        ("custeio", "Custeio"),
    ]
    
    valor_executado = models.DecimalField(max_digits=12, decimal_places=2, null=False)
    natureza_despesa = models.CharField(max_length=50, null=False, choices=NATUREZA_CHOICES)
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
        verbose_name = "Prestação de Contas"
        verbose_name_plural = "Prestações de Contas"

    def __str__(self):
        return f"Relatório {self.id} - Valor Executado: {self.valor_executado}"


# Modelo para DOCUMENTOS
class Document(models.Model):
    nome = models.CharField(max_length=255, null=False)
    caminho = models.FileField(upload_to=upload_to_accountability, null=False)  # Gerencia o upload de arquivos
    tamanho = models.IntegerField(null=False, blank=True)
    accountability = models.ForeignKey(Accountability, on_delete=models.CASCADE)
    removido_em = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "documents"
        verbose_name = "Documento"
        verbose_name_plural = "Documentos"

    def __str__(self):
        return self.nome


# Modelo para histórico de prestação de contas
class AccountabilityHistory(models.Model):
    # Campos originais da prestação de contas
    valor_executado = models.DecimalField(max_digits=12, decimal_places=2, null=False)
    natureza_despesa = models.CharField(max_length=50, null=False, choices=Accountability.NATUREZA_CHOICES)
    descricao = models.TextField(null=False)
    data_criacao = models.DateTimeField()
    
    # Campos específicos para histórico
    current_version = models.ForeignKey(Accountability, on_delete=models.CASCADE, related_name='history_versions')
    version_date = models.DateTimeField(auto_now_add=True)
    version_user = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    version_number = models.IntegerField(default=1)
    
    class Meta:
        db_table = "accountability_history"
        verbose_name = "Histórico de Prestação de Contas"
        verbose_name_plural = "Históricos de Prestação de Contas"
        ordering = ['-version_date']

    def __str__(self):
        return f"Histórico {self.version_number} do Relatório {self.current_version.id}"
    
    def get_natureza_despesa_display(self):
        return dict(Accountability.NATUREZA_CHOICES).get(self.natureza_despesa, self.natureza_despesa)


# Modelo para histórico de documentos
class DocumentHistory(models.Model):
    # Campos originais do documento
    nome = models.CharField(max_length=255, null=False)
    caminho = models.FileField(upload_to=upload_to_accountability_history, null=False)
    tamanho = models.IntegerField(null=False)
    data_upload = models.DateTimeField(auto_now_add=True)
    
    # Referência para o histórico da prestação de contas
    accountability_history = models.ForeignKey(AccountabilityHistory, on_delete=models.CASCADE, related_name='documents')
    original_document_id = models.IntegerField()  # ID do documento original para rastreamento
    
    class Meta:
        db_table = "document_history"
        verbose_name = "Histórico de Documento"
        verbose_name_plural = "Históricos de Documentos"

    def __str__(self):
        return f"Histórico do documento {self.original_document_id} - {self.nome}"

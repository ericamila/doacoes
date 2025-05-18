from django.db import models
from django.utils import timezone


# Modelo do MUNICIPIO
class Municipio(models.Model):
    nome = models.CharField(max_length=200, null=True, blank=True)
    codigo = models.CharField(max_length=100, null=True, unique=True)
    uf = models.CharField(max_length=2, null=True)
    cnpj = models.CharField(max_length=50, null=True, unique=True)
    removido_em = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "municipios"
        verbose_name = "Município"
        verbose_name_plural = "Municípios"

    def __str__(self):
        return f'{self.nome} - {self.cnpj}'


# Modelo do PARLAMENTAR
class Parlamentar(models.Model):
    nome = models.CharField(max_length=200, null=True, blank=True)
    ano = models.IntegerField(null=False, blank=True, default=timezone.now().year)
    removido_em = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "parlamentares"
        verbose_name = "Parlamentar"
        verbose_name_plural = "Parlamentares"

    def __str__(self):
        return self.nome


# Modelo do BANCO
class Banco(models.Model):
    codigo = models.CharField(max_length=10, null=True, unique=True)
    nome = models.CharField(max_length=200, null=True, blank=True)
    removido_em = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "bancos"
        verbose_name = "Banco"
        verbose_name_plural = "Bancos"

    def __str__(self):
        return f'{self.codigo} - {self.nome}'


# Modelo da CONTA_BANCARIA
class ContaBancaria(models.Model):
    banco = models.ForeignKey(Banco, on_delete=models.CASCADE)
    agencia = models.CharField(max_length=100, null=True)
    conta = models.CharField(max_length=100, null=True)
    removido_em = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "contas_bancarias"
        verbose_name = "Conta Bancária"
        verbose_name_plural = "Contas Bancárias"

    def __str__(self):
        return f"{self.banco} - {self.agencia} - {self.conta}"


# Modelo de POLITICAS_PUBLICAS
class PoliticaPublica(models.Model):
    ano = models.IntegerField(null=False)
    codigo = models.CharField(max_length=50, unique=True, null=False)
    nome = models.CharField(max_length=255, unique=True, null=False)
    removido_em = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "politicas_publicas"
        verbose_name = "Política Pública"
        verbose_name_plural = "Políticas Públicas"

    def __str__(self):
        return f"{self.codigo} - {self.nome}"



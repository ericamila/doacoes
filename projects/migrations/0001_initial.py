# Generated by Django 5.2.1 on 2025-05-16 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(blank=True, max_length=200, null=True)),
                ('ano', models.IntegerField(default=2025)),
                ('tipo_de_transferencia', models.CharField(choices=[('Especial', 'Especial')], default='Especial', max_length=50)),
                ('codigo', models.CharField(max_length=100, null=True, unique=True)),
                ('orgao_de_origem', models.CharField(max_length=200, null=True)),
                ('orgao_repassador', models.CharField(max_length=200, null=True)),
                ('unidade_gestora', models.CharField(max_length=100, null=True)),
                ('unidade_orcamentaria', models.CharField(max_length=200, null=True)),
                ('data_inicial_ciencia', models.DateField()),
                ('data_final_ciencia', models.DateField()),
                ('descricao', models.TextField(blank=True, max_length=1000)),
                ('removido_em', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Project',
                'verbose_name_plural': 'Projects',
                'db_table': 'projects',
            },
        ),
    ]

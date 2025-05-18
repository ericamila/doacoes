from django import forms

from projects.models import LISTA_CATEGORIAS, Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ["nome", "removido_em"]  # Exclui os campos do formulário
        labels = {
            "ano": "Ano",
            "tipo_de_transferencia": "Modalidade de Transferência",
            "codigo": "Código",
            "orgao_de_origem": "Órgão de Origem",
            "orgao_repassador": "Órgão Repassador",
            "unidade_gestora": "Unidade Gestora",
            "unidade_orcamentaria": "Unidade Orçamentária",
            "data_inicial_ciencia": "Data Inicial de Registro de Ciência",
            "data_final_ciencia": "Data Final de Registro de Ciência",
            "descricao": "Descrição",
        }
        widgets = {
            "ano": forms.NumberInput(attrs={"class": "form-control", "col": "4"}),
            "tipo_de_transferencia": forms.Select(
                choices=LISTA_CATEGORIAS, attrs={"class": "form-control", "col": "4"}
            ),
            "codigo": forms.TextInput(attrs={"class": "form-control", "col": "4"}),
            "orgao_de_origem": forms.TextInput(
                attrs={"class": "form-control", "col": "6"}
            ),
            "orgao_repassador": forms.TextInput(
                attrs={"class": "form-control", "col": "6"}
            ),
            "unidade_gestora": forms.TextInput(
                attrs={"class": "form-control", "col": "4"}
            ),
            "unidade_orcamentaria": forms.TextInput(
                attrs={"class": "form-control", "col": "8"}
            ),
            "data_inicial_ciencia": forms.DateInput(
                format="%Y-%m-%d",
                attrs={"class": "form-control", "type": "date", "col": "6"},
            ),
            "data_final_ciencia": forms.DateInput(
                format="%Y-%m-%d",
                attrs={"class": "form-control", "type": "date", "col": "6"},
            ),
            "descricao": forms.Textarea(attrs={"class": "form-control", "col": "12"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Formata os campos de data corretamente no formulário
        if self.instance and self.instance.pk:
            self.fields["data_inicial_ciencia"].initial = (
                self.instance.data_inicial_ciencia.strftime("%Y-%m-%d")
                if self.instance.data_inicial_ciencia
                else ""
            )
            self.fields["data_final_ciencia"].initial = (
                self.instance.data_final_ciencia.strftime("%Y-%m-%d")
                if self.instance.data_final_ciencia
                else ""
            )
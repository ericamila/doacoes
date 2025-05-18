from django import forms
from proposals.models import Proposal


# Formulário da Propostas
class ProposalForm(forms.ModelForm):
    class Meta:
        model = Proposal
        exclude = ["removido_em", "conta_bancaria", "ciente", "sei_remocao_ciente", "data_remocao_ciente",
                   "data_ciencia"]  # Exclui os campos do formulário
        labels = {
            "ano": "Ano",
            "codigo": "Código",
            "project": "Project",
            "valor_custeio": "Valor de Custeio",
            "valor_investimento": "Valor de Investimento",
            "parlamentar": "Parlamentar",
            "municipio": "Município",
            "descricao": "Descrição",
        }
        widgets = {
            "ano": forms.NumberInput(attrs={"class": "form-control", "col": "3"}),
            "codigo": forms.TextInput(attrs={"class": "form-control", "col": "4"}),
            "project": forms.Select(attrs={"class": "form-control", "col": "5"}),
            "valor_custeio": forms.NumberInput(attrs={"class": "form-control", "col": "3"}),
            "valor_investimento": forms.NumberInput(attrs={"class": "form-control", "col": "3"}),
            "parlamentar": forms.Select(attrs={"class": "form-control", "col": "3"}),
            "municipio": forms.Select(attrs={"class": "form-control", "col": "3"}),
            "descricao": forms.Textarea(attrs={"class": "form-control", "col": "12"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields["ano"].initial = self.instance.ano
            self.fields["codigo"].initial = self.instance.codigo
            self.fields["project"].initial = self.instance.programa
            self.fields["valor_custeio"].initial = self.instance.valor_custeio
            self.fields["valor_investimento"].initial = self.instance.valor_investimento
            self.fields["parlamentar"].initial = self.instance.parlamentar
            self.fields["municipio"].initial = self.instance.municipio
            self.fields["descricao"].initial = self.instance.descricao





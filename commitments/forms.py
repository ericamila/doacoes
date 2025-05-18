from django import forms
from commitments.models import Commitment


# Formulário do EMPENHO
class CommitmentForm(forms.ModelForm):
    class Meta:
        model = Commitment
        exclude = ["removido_em"] 
        labels = {
            "codigo": "Código",
            "processo": "Processo",
            "plan": "Plano de Ação",
            "valor": "Valor",
            "valor_estornado": "Valor Estornado",
            "situacao": "Situação",
            "data": "Data",
        }
        widgets = {
            "codigo": forms.TextInput(attrs={"class": "form-control", "col": "3", 'disabled': 'disabled'}),
            "processo": forms.TextInput(attrs={"class": "form-control", "col": "6", 'disabled': 'disabled'}),
            "plan": forms.TextInput(attrs={"class": "form-control", "col": "3", 'disabled': 'disabled'}),
            "valor": forms.NumberInput(attrs={"class": "form-control", "col": "4", 'disabled': 'disabled'}),
            "valor_estornado": forms.NumberInput(attrs={"class": "form-control", "col": "4", 'disabled': 'disabled'}),
            "situacao": forms.TextInput(attrs={"class": "form-control", "col": "4", 'disabled': 'disabled'}),
            "data": forms.DateInput(format="%Y-%m-%d", attrs={"class": "form-control", "type": "date", "col": "4",
                                                              'disabled': 'disabled'}),

        }
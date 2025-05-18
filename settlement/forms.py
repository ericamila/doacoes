from django import forms
from settlement.models import Settlement


# Formulário da LIQUIDACAO
class SettlementForm(forms.ModelForm):
    class Meta:
        model = Settlement
        exclude = ["removido_em"]  # Exclui os campos do formulário
        labels = {
            "codigo": "Código",
            "situacao": "Situação",
            "commitment": "Commitment",
            "valor": "Valor",
            "valor_estornado": "Valor Estornado",
            "data": "Data",
        }
        widgets = {
            "codigo": forms.TextInput(attrs={"class": "form-control", "col": "4", 'disabled': 'disabled'}),
            "situacao": forms.TextInput(attrs={"class": "form-control", "col": "4", 'disabled': 'disabled'}),
            "commitment": forms.TextInput(attrs={"class": "form-control", "col": "4", 'disabled': 'disabled'}),
            "valor": forms.NumberInput(attrs={"class": "form-control", "col": "4", 'disabled': 'disabled'}),
            "valor_estornado": forms.NumberInput(attrs={"class": "form-control", "col": "4", 'disabled': 'disabled'}),
            "data": forms.DateInput(format="%Y-%m-%d", attrs={"class": "form-control", "type": "date", "col": "4",
                                                              'disabled': 'disabled'}),
        }
from django import forms

from utils.models import ContaBancaria

class ContaBancariaForm(forms.ModelForm):
    class Meta:
        model = ContaBancaria
        exclude = ["removido_em"]
        labels = {
            "banco": "Banco",
            "agencia": "Agência",
            "conta": "Conta"
        }
        widgets = {
            "banco": forms.Select(attrs={"class": "form-control", "col": "4"}),
            "agencia": forms.TextInput(attrs={"class": "form-control", "col": "4"}),
            "conta": forms.TextInput(attrs={"class": "form-control", "col": "4"}),
        }
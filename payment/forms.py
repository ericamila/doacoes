from django import forms
from payment.models import Payment


# Formulário do PAGAMENTO
class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        exclude = ["removido_em"]  # Exclui os campos do formulário
        labels = {
            "codigo": "Código",
            "ordem_bancaria": "Ordem Bancária",
            "settlement": "Liquidação",
            "data": "Data",
            "valor": "Valor",
            "valor_estornado": "Valor Estornado",
            "situacao": "Situação",

        }
        widgets = {
            "codigo": forms.TextInput(attrs={"class": "form-control", "col": "4", 'disabled': 'disabled'}),
            "ordem_bancaria": forms.TextInput(attrs={"class": "form-control", "col": "4", 'disabled': 'disabled'}),
            "settlement": forms.TextInput(attrs={"class": "form-control", "col": "4", 'disabled': 'disabled'}),
            "data": forms.DateInput(format="%Y-%m-%d", attrs={"class": "form-control", "type": "date", "col": "4",
                                                              'disabled': 'disabled'}),
            "valor": forms.NumberInput(attrs={"class": "form-control", "col": "4", 'disabled': 'disabled'}),
            "valor_estornado": forms.NumberInput(attrs={"class": "form-control", "col": "4", 'disabled': 'disabled'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Sobrescreve o campo 'situacao' para exibir get_situacao_display
        if self.instance and self.instance.pk:
            self.fields['situacao'] = forms.CharField(
                initial=self.instance.get_situacao_display(),
                label=self.fields['situacao'].label,
                widget=forms.TextInput(attrs={"class": "form-control", "col": "4", 'disabled': 'disabled'})
            )
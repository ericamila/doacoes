
from django import forms

from plans.models import Plan
from utils.models import PoliticaPublica


class PlanForm(forms.ModelForm):
    politicas = forms.ModelMultipleChoiceField(
        queryset=PoliticaPublica.objects.filter(removido_em=None),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    class Meta:
        model = Plan
        exclude = ["removido_em", "descricao_politicas_publicas", "codigo", "porposal, politicas_publicas_plans"]  # Exclui os campos do formulário
        fields = ["politicas"]
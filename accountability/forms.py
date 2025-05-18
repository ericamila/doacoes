from django import forms
from django.forms import ValidationError
from accountability.models import Accountability


class AccountabilityForm(forms.ModelForm):
    class Meta:
        model = Accountability
        exclude = ["removido_em"]  # Exclui os campos do formulário
        labels = {
            "valor_executado": "Valor Executado",
            "natureza_despesa": "Natureza da Despesa",
            "descricao": "Descrição",
        }
        widgets = {
            "valor_executado": forms.NumberInput(attrs={"class": "form-control", "col": "4"}),
            "natureza_despesa": forms.Select(attrs={"class": "form-control", "col": "4"}),
            "descricao": forms.Textarea(attrs={"class": "form-control", "col": "12"}),
        }
        fields = ["valor_executado", "natureza_despesa", "descricao"]


# DOCUMENTO
class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result


class DocumentForm(forms.Form):
    arquivos = MultipleFileField()

    def clean_arquivos(self):
        arquivos = self.files.getlist("arquivos")
        extensoes_permitidas = [".jpg", ".jpeg", ".png", ".tiff", ".xls", ".xlsx", ".csv", ".pdf"]

        if not arquivos:
            raise ValidationError("É obrigatório enviar pelo menos um arquivo.")

        for arquivo in arquivos:
            if not any(arquivo.name.lower().endswith(ext) for ext in extensoes_permitidas):
                raise ValidationError(
                    f"O arquivo '{arquivo.name}' não é permitido. Apenas arquivos de imagem, .xls, .xlsx, .csv e .pdf são aceitos.")

        return arquivos

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm as DjangoPasswordChangeForm

from users.models import Usuario
from utils.models import Municipio


class UsuarioForm(UserCreationForm):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={"class": "form-control"},
        ),
    )

    password1 = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(
            attrs={"class": "form-control"},
        ),
    )

    first_name = forms.CharField(
        label="Nome Completo",
        widget=forms.TextInput(
            attrs={"class": "form-control"},
        ),
    )

    cpf = forms.CharField(
        label="CPF",
        widget=forms.TextInput(
            attrs={"class": "form-control"},
        ),
    )

    telefone = forms.CharField(
        label="Telefone",
        widget=forms.TextInput(
            attrs={"class": "form-control"},
        ),
    )

    codigo_sei = forms.CharField(
        label="Código do Pedido",
        widget=forms.TextInput(
            attrs={"class": "form-control"},
        ),
    )

    municipio = forms.ModelChoiceField(
        label="Município",
        queryset=Municipio.objects.all().order_by("nome"),
        widget=forms.Select(
            attrs={"class": "form-select"},
        ),
    )

    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = [
            "first_name",
            "email",
            "password1",
            "cpf",
            "telefone",
            "municipio",
            "codigo_sei",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove o campo  password2
        self.fields.pop("password2", None)

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if Usuario.objects.filter(username=email).exists():
            raise forms.ValidationError("Este email já está cadastrado.")
        return email


class UsuarioLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Email",
        widget=forms.EmailInput(
            attrs={"class": "form-control"},
        ),
    )

    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(
            attrs={"class": "form-control"},
        ),
    )

    class Meta:
        model = Usuario
        fields = ["username", "password"]


class PasswordChangeForm(DjangoPasswordChangeForm):
    """
    Formulário para alteração de senha com estilos Bootstrap.
    """
    old_password = forms.CharField(
        label="Senha atual",
        widget=forms.PasswordInput(
            attrs={"class": "form-control"},
        ),
    )
    
    new_password1 = forms.CharField(
        label="Nova senha",
        widget=forms.PasswordInput(
            attrs={"class": "form-control"},
        ),
    )
    
    new_password2 = forms.CharField(
        label="Confirme a nova senha",
        widget=forms.PasswordInput(
            attrs={"class": "form-control"},
        ),
    )

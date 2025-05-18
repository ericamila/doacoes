from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm as DjangoPasswordChangeForm
from django.contrib.auth.forms import PasswordResetForm as DjangoPasswordResetForm
from django.contrib.auth.forms import SetPasswordForm as DjangoSetPasswordForm
from django.core.exceptions import ValidationError

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
        required=False,
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
            "situacao",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove o campo password2
        self.fields.pop("password2", None)
        
        # Adiciona o campo de situação
        self.fields['situacao'] = forms.ChoiceField(
            label="Situação",
            choices=Usuario._meta.get_field('situacao').choices,
            widget=forms.Select(attrs={"class": "form-select"}),
        )
        
        # Se estiver editando um usuário existente
        if self.instance and self.instance.pk:
            # Torna o campo de senha opcional
            self.fields['password1'].required = False
            
            # Preenche o campo de situação com o valor atual
            self.initial['situacao'] = self.instance.situacao

    def clean_email(self):
        email = self.cleaned_data.get("email")
        # Se estiver editando um usuário existente, não validar o email como único
        if self.instance and self.instance.pk and self.instance.email == email:
            return email
            
        if Usuario.objects.filter(username=email).exists():
            raise forms.ValidationError("Este email já está cadastrado.")
        return email
        
    def save(self, commit=True):
        user = super().save(commit=False)
        
        # Se estiver editando um usuário existente
        if self.instance and self.instance.pk:
            # Atualiza os campos
            user.first_name = self.cleaned_data.get('first_name')
            user.cpf = self.cleaned_data.get('cpf')
            user.telefone = self.cleaned_data.get('telefone')
            user.municipio = self.cleaned_data.get('municipio')
            user.codigo_sei = self.cleaned_data.get('codigo_sei')
            user.situacao = self.cleaned_data.get('situacao')
            
            # Só atualiza a senha se uma nova senha foi fornecida
            password = self.cleaned_data.get('password1')
            if password:
                user.set_password(password)
        else:
            # Novo usuário
            user.username = self.cleaned_data.get('email')
            user.email = self.cleaned_data.get('email')
            user.set_password(self.cleaned_data.get('password1'))
            
        if commit:
            user.save()
        return user


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

    error_messages = {
        'invalid_login': "Email ou senha incorretos. Por favor, tente novamente.",
        'inactive': "Esta conta está inativa. Entre em contato com o administrador.",
    }

    def confirm_login_allowed(self, user):
        if user.situacao != 0:  # 0 = Ativo
            raise ValidationError(
                self.error_messages['inactive'],
                code='inactive',
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


class PasswordResetForm(DjangoPasswordResetForm):
    """
    Formulário para solicitação de recuperação de senha com estilos Bootstrap.
    """
    email = forms.EmailField(
        label="Email",
        max_length=254,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control form-control-lg",
                "placeholder": "Digite seu email cadastrado",
            }
        ),
    )


class SetPasswordForm(DjangoSetPasswordForm):
    """
    Formulário para definição de nova senha com estilos Bootstrap.
    """
    new_password1 = forms.CharField(
        label="Nova senha",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control form-control-lg",
                "placeholder": "Digite sua nova senha",
            }
        ),
    )
    
    new_password2 = forms.CharField(
        label="Confirme a nova senha",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control form-control-lg",
                "placeholder": "Confirme sua nova senha",
            }
        ),
    )

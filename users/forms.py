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

    municipios = forms.ModelChoiceField(
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
            "tipo_usuario",
            "situacao",
            "municipios",
            "codigo_sei",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove o campo  password2, situacao e tipo_usuario do formulário
        self.fields.pop("password2", None)
        self.fields.pop("situacao", None)
        self.fields.pop("tipo_usuario", None)
               
        # Se estiver editando um usuário existente remove o campo de senha
        if self.instance and self.instance.pk:
            self.fields.pop("password1", None)
            
            # Adiciona o campo de situação
            self.fields['situacao'] = forms.ChoiceField(
                initial=self.instance.situacao,
                required=False,
                label="Situação",
                choices=Usuario._meta.get_field('situacao').choices,
                widget=forms.Select(attrs={"class": "form-select"}),
            )
            
            # Adiciona o campo de tipo_usuario
            self.fields['tipo_usuario'] = forms.ChoiceField(
                initial=self.instance.tipo_usuario,
                required=False,
                label="Tipo de Usuário",
                choices=Usuario._meta.get_field('tipo_usuario').choices,
                widget=forms.Select(attrs={"class": "form-select"}),
            )


    def clean_email(self):
        email = self.cleaned_data.get("email")
        # Se estiver editando um usuário existente, não validar o email como único
        if self.instance and self.instance.pk and self.instance.email == email:
            return email
            
        if Usuario.objects.filter(username=email).exists():
            raise forms.ValidationError("Este email já está cadastrado.")
        return email
        
        
    def save(self, commit=True):
        # Se estiver editando um usuário existente
        if self.instance and self.instance.pk:
            user = self.instance
            # Atualiza os campos
            user.first_name = self.cleaned_data.get('first_name')
            user.cpf = self.cleaned_data.get('cpf')
            user.telefone = self.cleaned_data.get('telefone')
            user.municipios = self.cleaned_data.get('municipios')
            user.codigo_sei = self.cleaned_data.get('codigo_sei')
            user.situacao = self.cleaned_data.get('situacao')
            user.tipo_usuario = self.cleaned_data.get('tipo_usuario')
            
            if commit:
                user.save()
            return user
        else:
            # Novo usuário
            user = super().save(commit=False)
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

from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UsuarioForm, PasswordChangeForm

Usuario = get_user_model()  # Obtém o modelo de usuário personalizado


def signup_view(request):
    """
    Função para cadastro de novos usuários.
    
    Args:
        request: Objeto HttpRequest
        
    Returns:
        HttpResponse: Renderiza o template de cadastro ou redireciona para login
    """
    if request.method == "POST":
        form = UsuarioForm(request.POST)

        if form.is_valid():
            user = form.save(
                commit=False
            )  # Não salva ainda para adicionar campos adicionais
            user.first_name = form.cleaned_data["first_name"]
            user.username = form.cleaned_data["email"]
            user.email = form.cleaned_data["email"]
            user.cpf = form.cleaned_data["cpf"]
            user.telefone = form.cleaned_data["telefone"]
            user.set_password(form.cleaned_data["password1"])

            user.save()

            messages.success(request, "Usuário cadastrado com sucesso.")
            return redirect("users:login")
        else:
            messages.error(request, "Erro ao cadastrar o usuário. Verifique os campos.")

    else:
        form = UsuarioForm()

    return render(
        request,
        "users/new.html",  # Corrigido o caminho do template
        {
            "form": form,
        },
    )


@login_required
def profile_view(request):
    """
    Função para visualização e edição do perfil do usuário logado.
    
    Args:
        request: Objeto HttpRequest
        
    Returns:
        HttpResponse: Renderiza o template de perfil
    """
    user = request.user
    
    if request.method == "POST":
        form = UsuarioForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil atualizado com sucesso.")
        else:
            messages.error(request, "Erro ao atualizar o perfil. Verifique os campos.")
    else:
        form = UsuarioForm(instance=user)
    
    return render(
        request,
        "users/profile.html",
        {
            "form": form,
            "user": user,
        },
    )


@login_required
def password_change_view(request):
    """
    Função para alteração de senha do usuário logado.
    
    Args:
        request: Objeto HttpRequest
        
    Returns:
        HttpResponse: Renderiza o template de alteração de senha ou redireciona para perfil
    """
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Senha alterada com sucesso.")
            return redirect("users:profile")
        else:
            messages.error(request, "Erro ao alterar a senha. Verifique os campos.")
    else:
        form = PasswordChangeForm(request.user)
    
    return render(
        request,
        "users/password_change.html",
        {
            "form": form,
        },
    )

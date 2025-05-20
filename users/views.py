from datetime import timezone
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (
    PasswordResetView, 
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
from .forms import UsuarioForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse_lazy

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

@login_required
def lists(request):
    users = Usuario.objects.filter(removido_em=None)
    obj = request.GET.get("obj")  # Implementa o mecanismo de busca

    if obj:
        # Busca por email ou nome
        users = users.filter(email__icontains=obj) | users.filter(first_name__icontains=obj)
        # Busca por situação textual
        situacoes = dict(Usuario._meta.get_field('situacao').choices)
        situacao_map = {v.lower(): k for k, v in situacoes.items()}
        obj_lower = obj.lower()
        if obj_lower in situacao_map:
            users = users | Usuario.objects.filter(situacao=situacao_map[obj_lower])
    else:
        users = users.order_by('first_name')

    paginator = Paginator(users, 10)  # Define 10 itens fixos por página
    page_number = request.GET.get("page")

    try:
        page_obj = paginator.get_page(page_number)
    except (PageNotAnInteger, EmptyPage):
        page_obj = paginator.get_page(1)

    return render(
        request,
        "users/list.html",
        {
            "users": page_obj,
            "page_obj": page_obj,
        },
    )

@login_required
def detail(request, pk):
    user = get_object_or_404(Usuario, pk=pk)
    return render(request, "users/detail.html", {"user": user})

@login_required
def edit(request, pk):
    user = get_object_or_404(Usuario, pk=pk)
    
    # Verificar se o usuário atual é administrador ou está editando seu próprio perfil
    if not (request.user.is_superusestaffr or request.user.is_) and request.user.pk != user.pk:
        messages.error(request, "Você não tem permissão para editar este usuário.")
        return redirect("users:lists")

    if request.method == "POST":
        form = UsuarioForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuário atualizado com sucesso.")
            return redirect("users:lists")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Erro no campo {field}: {error}")
    else:
        form = UsuarioForm(instance=user)

    return render(
        request,
        "users/edit.html",
        {
            "form": form,
            "user": user,
        },
    )

@login_required
def remove(request, pk):
    user = get_object_or_404(Usuario, pk=pk)
    
    # Verificar se o usuário atual é administrador
    if not (request.user.is_superuser or request.user.is_staff):
        messages.error(request, "Você não tem permissão para remover usuários.")
        return redirect("users:lists")
        
    user.removido_em = timezone.now()
    user.save()
    messages.success(request, "Usuário removido com sucesso.")
    return redirect("users:lists")

# Views customizadas para reset de senha
class CustomPasswordResetView(PasswordResetView):
    """
    View customizada para solicitação de recuperação de senha.
    """
    template_name = 'registration/password_reset_form.html'
    form_class = PasswordResetForm
    email_template_name = 'registration/password_reset_email.html'
    success_url = reverse_lazy('users:password_reset_done')
    
    def form_valid(self, form):
        messages.success(self.request, "Um email com instruções para redefinir sua senha foi enviado.")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Erro ao solicitar redefinição de senha. Verifique o email informado.")
        return super().form_invalid(form)

class CustomPasswordResetDoneView(PasswordResetDoneView):
    """
    View customizada para confirmação de envio de email de recuperação de senha.
    """
    template_name = 'registration/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """
    View customizada para confirmação de nova senha.
    """
    template_name = 'registration/password_reset_confirm.html'
    form_class = SetPasswordForm
    success_url = reverse_lazy('users:password_reset_complete')
    
    def form_valid(self, form):
        messages.success(self.request, "Sua senha foi alterada com sucesso.")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Erro ao redefinir senha. Verifique os campos.")
        return super().form_invalid(form)

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    """
    View customizada para confirmação de alteração de senha.
    """
    template_name = 'registration/password_reset_complete.html'

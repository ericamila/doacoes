from django.shortcuts import render, redirect
from .forms import UsuarioForm
from django.contrib.auth import get_user_model
from django.contrib import messages

Usuario = get_user_model()  # Obtém o modelo de usuário personalizado


def signup_view(request):
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
        "new.html",
        {
            "form": form,
        },
    )

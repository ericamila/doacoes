from datetime import datetime
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from plans.models import Plan
from accountability.forms import DocumentForm, AccountabilityForm
from accountability.models import Document, Accountability


# Create your views here.
def lists(request):
    accountabilities = Accountability.objects.filter(removido_em=None)
    for accountability in accountabilities:
        accountability.documentos = Document.objects.filter(removido_em=None, accountability=accountability)
    return render(request, 'accountability/list.html', {'accountabilities': accountabilities})


@login_required
def new(request, id):
    try:
        plan = get_object_or_404(Plan, pk=id)

        accountability = Accountability.objects.create(
            valor_executado=request.POST.get('valor_executado'),
            natureza_despesa=request.POST.get('natureza_despesa'),
            descricao=request.POST.get('descricao'),
            plan=plan,
            data_criacao=datetime.now(),
        )

        register_document(request, accountability.id)
        accountability.save()

        messages.success(request, "Prestação de Contas criado com sucesso.")
        return accountability

    except Exception as e:
        print(f"Erro ao criar plano de ação: {e}")
        messages.error(request, "Erro ao criar relatório de gestão.")
        return None


@login_required
def edit(request, id):
    accountability = get_object_or_404(Accountability, pk=id)

    if request.method == "POST":
        form = AccountabilityForm(request.POST, request.FILES, instance=accountability)

        if form.is_valid():
            form.save()

            # Adicionar novos arquivos
            arquivos = request.FILES.getlist('arquivos')
            for arquivo in arquivos:
                Document.objects.create(
                    accountability=accountability,
                    caminho=arquivo,
                    nome=arquivo.name,
                    tamanho=arquivo.size,
                )

            messages.success(request, "Prestação de Contas atualizada com sucesso.")
        else:
            messages.error(request, "Erro ao atualizar o relatório de gestão. Verifique os campos.")

    else:
        form = AccountabilityForm(instance=accountability)

    return accountability


@login_required
def remover_accountability(request, id):
    accountability = get_object_or_404(Accountability, pk=id)

    if request.method == "POST":
        accountability.removido_em = datetime.now()
        accountability.save()

    return accountability


@login_required
def register_document(request, accountability_id):
    accountability = get_object_or_404(Accountability, pk=accountability_id)

    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            arquivos = request.FILES.getlist("arquivos")  # Obtém a lista de arquivos enviados
            for arquivo in arquivos:
                try:
                    documento = Document(
                        accountability=accountability,
                        caminho=arquivo,
                        nome=arquivo.name,
                        tamanho=arquivo.size,
                    )
                    documento.save()
                except Exception as e:
                    messages.error(request, f"Erro ao salvar o arquivo {arquivo.name}.")
            # TODO: verificar retornos e redirecionamentos
            return redirect("/planos-de-acao/plano-de-acao.html#accountability")
        else:
            messages.error(request, form.errors)
    else:
        form = DocumentForm()
    # return form
    return render(request, "accountability/modal_registrar_accountability.html", {"form": form, "accountability": accountability})


@login_required
def remove_document(request, documento_id):
    try:
        documento = get_object_or_404(Document, pk=documento_id)
        documento.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
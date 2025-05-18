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
    relatorios = Accountability.objects.filter(removido_em=None)
    for relatorio in relatorios:
        relatorio.documentos = Document.objects.filter(removido_em=None, accountability=relatorio)
    return render(request, 'accountability/list.html', {'relatorios': relatorios})


@login_required
def new(request, id):
    try:
        plano_de_acao = get_object_or_404(Plan, pk=id)

        accountability = Accountability.objects.create(
            valor_executado=request.POST.get('valor_executado'),
            natureza_despesa=request.POST.get('natureza_despesa'),
            descricao=request.POST.get('descricao'),
            plano_de_acao=plano_de_acao,
            data_criacao=datetime.now(),
        )

        register_document(request, accountability.id)
        accountability.save()

        messages.success(request, "Relatório de Gestão criado com sucesso.")
        return accountability

    except Exception as e:
        print(f"Erro ao criar plano de ação: {e}")
        messages.error(request, "Erro ao criar relatório de gestão.")
        return None


@login_required
def edit(request, id):
    relatorio = get_object_or_404(Accountability, pk=id)

    if request.method == "POST":
        form = AccountabilityForm(request.POST, request.FILES, instance=relatorio)

        if form.is_valid():
            form.save()

            # Adicionar novos arquivos
            arquivos = request.FILES.getlist('arquivos')
            for arquivo in arquivos:
                Document.objects.create(
                    accountability=relatorio,
                    caminho=arquivo,
                    nome=arquivo.name,
                    tamanho=arquivo.size,
                )

            messages.success(request, "Relatório de Gestão atualizado com sucesso.")
        else:
            messages.error(request, "Erro ao atualizar o relatório de gestão. Verifique os campos.")

    else:
        form = AccountabilityForm(instance=relatorio)

    return render(request, 'accountability/edit.html', {'form': form, 'relatorio': relatorio})


@login_required
def remover_accountability(request, id):
    relatorio = get_object_or_404(Accountability, pk=id)

    if request.method == "POST":
        relatorio.removido_em = datetime.now()
        relatorio.save()

    return relatorio


@login_required
def register_document(request, relatorio_id):
    relatorio = get_object_or_404(Accountability, pk=relatorio_id)

    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            arquivos = request.FILES.getlist("arquivos")  # Obtém a lista de arquivos enviados
            for arquivo in arquivos:
                try:
                    documento = Document(
                        accountability=relatorio,
                        caminho=arquivo,
                        nome=arquivo.name,
                        tamanho=arquivo.size,
                    )
                    documento.save()
                except Exception as e:
                    messages.error(request, f"Erro ao salvar o arquivo {arquivo.name}.")
            # TODO: verificar retornos e redirecionamentos
            return redirect("/planos-de-acao/plano-de-acao.html#relatorio-gestao")
        else:
            messages.error(request, form.errors)
    else:
        form = DocumentForm()
    # return form
    return render(request, "accountability/modal_registrar_relatorio.html", {"form": form, "relatorio": relatorio})


@login_required
def remove_document(request, documento_id):
    try:
        documento = get_object_or_404(Document, pk=documento_id)
        documento.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
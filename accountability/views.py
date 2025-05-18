from datetime import datetime
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.urls import reverse
from plans.models import Plan
from accountability.forms import DocumentForm, AccountabilityForm
from accountability.models import Document, Accountability
import logging

# Configurar logging
logger = logging.getLogger(__name__)

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
        logger.error(f"Erro ao criar plano de ação: {e}")
        messages.error(request, "Erro ao criar relatório de gestão.")
        return None


@login_required
def edit(request, id):
    accountability = get_object_or_404(Accountability, pk=id)
    plan_id = accountability.plan.id

    if request.method == "POST":
        form = AccountabilityForm(request.POST, instance=accountability)

        if form.is_valid():
            form.save()

            # Verificar se há arquivos no request
            logger.info(f"FILES: {request.FILES}")
            logger.info(f"POST: {request.POST}")
            
            # Adicionar novos arquivos
            if 'arquivos' in request.FILES:
                arquivos = request.FILES.getlist('arquivos')
                logger.info(f"Arquivos encontrados: {len(arquivos)}")
                
                for arquivo in arquivos:
                    try:
                        logger.info(f"Processando arquivo: {arquivo.name}, tamanho: {arquivo.size}")
                        documento = Document(
                            accountability=accountability,
                            caminho=arquivo,
                            nome=arquivo.name,
                            tamanho=arquivo.size,
                        )
                        documento.save()
                        logger.info(f"Arquivo salvo com sucesso: {arquivo.name}")
                    except Exception as e:
                        logger.error(f"Erro ao salvar arquivo {arquivo.name}: {e}")
                        messages.error(request, f"Erro ao salvar o arquivo {arquivo.name}: {e}")
            else:
                logger.warning("Nenhum arquivo encontrado no request")

            messages.success(request, "Prestação de Contas atualizada com sucesso.")
            return redirect(reverse('plans:detail', kwargs={'id': plan_id}) + '#accountability')
        else:
            logger.error(f"Erros de formulário: {form.errors}")
            messages.error(request, "Erro ao atualizar o relatório de gestão. Verifique os campos.")
            return redirect(reverse('plans:detail', kwargs={'id': plan_id}) + '#accountability')

    # Se for GET, redireciona para a página de detalhes do plano com o modal aberto
    return redirect(reverse('plans:detail', kwargs={'id': plan_id}) + '#accountability')


@login_required
def remove(request, id):
    accountability = get_object_or_404(Accountability, pk=id)
    plan_id = accountability.plan.id

    if request.method == "POST":
        accountability.removido_em = datetime.now()
        accountability.save()
        messages.success(request, "Prestação de Contas removida com sucesso.")
    
    return redirect(reverse('plans:detail', kwargs={'id': plan_id}) + '#accountability')


@login_required
def register_document(request, accountability_id):
    accountability = get_object_or_404(Accountability, pk=accountability_id)
    plan_id = accountability.plan.id

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
            
            messages.success(request, "Documentos adicionados com sucesso.")
            return redirect(reverse('plans:detail', kwargs={'id': plan_id}) + '#accountability')
        else:
            messages.error(request, form.errors)
            return redirect(reverse('plans:detail', kwargs={'id': plan_id}) + '#accountability')
    else:
        form = DocumentForm()
    
    return render(request, "accountability/modal_registrar_accountability.html", {"form": form, "accountability": accountability})


@login_required
def remove_document(request, documento_id):
    try:
        documento = get_object_or_404(Document, pk=documento_id)
        documento.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

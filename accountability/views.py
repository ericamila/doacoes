from datetime import datetime
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.urls import reverse
from django.core.files.base import ContentFile
from plans.models import Plan
from accountability.forms import DocumentForm, AccountabilityForm
from accountability.models import Document, Accountability, AccountabilityHistory, DocumentHistory
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


def create_accountability_history(accountability, user):
    """
    Cria uma versão histórica da prestação de contas e seus documentos.
    
    Args:
        accountability: Objeto Accountability a ser versionado
        user: Usuário que está realizando a edição
        
    Returns:
        AccountabilityHistory: Objeto de histórico criado
    """
    try:
        # Determinar o número da versão
        version_number = AccountabilityHistory.objects.filter(
            current_version=accountability
        ).count() + 1
        
        # Criar o registro histórico
        history = AccountabilityHistory(
            valor_executado=accountability.valor_executado,
            natureza_despesa=accountability.natureza_despesa,
            descricao=accountability.descricao,
            data_criacao=accountability.data_criacao,
            current_version=accountability,
            version_user=user,
            version_number=version_number
        )
        history.save()
        
        logger.info(f"Criado histórico versão {version_number} para prestação de contas {accountability.id}")
        
        # Copiar os documentos
        for doc in Document.objects.filter(accountability=accountability, removido_em=None):
            try:
                # Copiar o arquivo físico
                file_content = doc.caminho.read()
                
                doc_history = DocumentHistory(
                    nome=doc.nome,
                    tamanho=doc.tamanho,
                    accountability_history=history,
                    original_document_id=doc.id
                )
                doc_history.caminho.save(doc.nome, ContentFile(file_content))
                doc_history.save()
                
                logger.info(f"Documento {doc.id} ({doc.nome}) copiado para histórico")
            except Exception as e:
                logger.error(f"Erro ao copiar documento {doc.id} para histórico: {e}")
        
        return history
    except Exception as e:
        logger.error(f"Erro ao criar histórico para prestação de contas {accountability.id}: {e}")
        return None


@login_required
def edit(request, id):
    accountability = get_object_or_404(Accountability, pk=id)
    plan_id = accountability.plan.id

    if request.method == "POST":
        # Criar versão histórica antes de atualizar
        history = create_accountability_history(accountability, request.user)
        if history:
            logger.info(f"Histórico criado com sucesso: versão {history.version_number}")
        else:
            logger.warning("Falha ao criar histórico da prestação de contas")
            
        form = AccountabilityForm(request.POST, request.FILES, instance=accountability)

        if form.is_valid():
            form.save()

            # Verificar se há arquivos no request
            logger.info(f"FILES: {request.FILES}")
            logger.info(f"POST: {request.POST}")
            
            # Adicionar novos arquivos
            register_document(request, accountability.id)

            messages.success(request, "Prestação de Contas atualizada com sucesso.")
        else:
            logger.error(f"Erros de formulário: {form.errors}")
            messages.error(request, "Erro ao atualizar o relatório de gestão. Verifique os campos.")

    # Se for GET, redireciona para a página de detalhes do plano com o modal aberto
    return redirect(reverse('plans:detail', kwargs={'id': plan_id}) + '#accountability')


@login_required
def view_accountability(request, id):
    """
    Visualiza uma prestação de contas com seu histórico de versões.
    """
    accountability = get_object_or_404(Accountability, pk=id)
    
    # Buscar documentos
    documentos = Document.objects.filter(accountability=accountability, removido_em=None)
    
    # Buscar histórico de versões
    history_versions = AccountabilityHistory.objects.filter(
        current_version=accountability
    ).order_by('-version_date')
    
    # Carregar documentos para cada versão histórica
    for version in history_versions:
        version.documentos = DocumentHistory.objects.filter(accountability_history=version)
    
    return render(request, 'accountability/view.html', {
        'accountability': accountability,
        'documentos': documentos,
        'history_versions': history_versions,
        'current_version': accountability,  # Para comparação
    })


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
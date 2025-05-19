from datetime import datetime
from django.shortcuts import render
from proposals.forms import ProposalForm
from proposals.models import Proposal
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from plans.forms import PlanForm
from plans.views import new as new_plan
from utils.forms import ContaBancariaForm
from utils.models import Banco, ContaBancaria



# Propostas
def lists(request):
    proposals_list = Proposal.objects.filter(removido_em=None)
    obj = request.GET.get("obj")  # Implementa o mecanismo de busca

    if obj:
        proposals_list = proposals_list.filter(project__codigo__icontains=obj) | proposals_list.filter(
            parlamentar__nome__icontains=obj)
    else:
        proposals_list = proposals_list.order_by("codigo")

    paginator = Paginator(proposals_list, 10)  # Define 10 itens fixos por página
    page_number = request.GET.get("page")

    try:
        page_obj = paginator.get_page(page_number)
    except (PageNotAnInteger, EmptyPage):
        page_obj = paginator.get_page(1)

    return render(
        request,
        "proposals/list.html",
        {
            "proposals": page_obj,
            "page_obj": page_obj,
        },
    )


# Leitura de Proposta
def detail(request, id):
    proposal = get_object_or_404(Proposal, pk=id)
    form = ProposalForm(instance=proposal)
    contaForm = ContaBancariaForm()
    plano_acao_form = PlanForm()

    return render(
        request,
        "proposals/detail.html",
        {
            "proposal_form": form,
            "proposal": proposal,
            "conta_form": contaForm,
            "plano_acao_form": plano_acao_form,
        },
    )


# Criação de Proposta
@login_required
def new(request):
    if request.method == "POST":
        form = ProposalForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Proposta enviada com sucesso!")
            return redirect("proposals:new")
        else:
            messages.error(request, "Erro ao salvar o proposal. Verifique os campos.")
    else:
        form = ProposalForm()

    return render(request, "proposals/new.html", {"proposal_form": form})


# Atualização de Proposta
@login_required
def edit(request, id):
    proposal = get_object_or_404(Proposal, pk=id)

    if request.method == "POST":
        form = ProposalForm(request.POST, instance=proposal)

        if form.is_valid():
            form.save()
            messages.success(request, "Proposta atualizada com sucesso!")
        else:
            messages.error(request, "Erro ao salvar a proposal. Verifique os campos.")

    else:
        form = ProposalForm(instance=proposal)

    return render(request, "proposals/edit.html", {"proposal_form": form, "proposal": proposal})


# Remoção de Proposta
@login_required
def remove(request, id):
    proposal = get_object_or_404(Proposal, pk=id)

    # TODO: Alterar mecanismo de remoção
    if request.method == "POST":
        proposal.removido_em = datetime.now()
        proposal.save()

    return redirect("proposals:lists")


@login_required
def registrar_ciencia(request, id):
    proposal = get_object_or_404(Proposal, pk=id)

    if request.method == "POST":
        banco_id = request.POST.get("banco")
        agencia = request.POST.get("agencia")
        conta = request.POST.get("conta")

        # Verifica se os campos da conta bancária foram preenchidos
        if banco_id and agencia and conta:
            try:
                # Busca a instância do Banco
                banco = Banco.objects.get(pk=banco_id)
            except Banco.DoesNotExist:
                messages.error(request, "Banco inválido.")
                return redirect("proposals:detail", id=proposal.id)

            # Cria ou obtém a conta bancária
            conta_bancaria, created = ContaBancaria.objects.get_or_create(
                banco=banco,
                agencia=agencia,
                conta=conta
            )
            # Associa a conta bancária à proposal
            proposal.conta_bancaria = conta_bancaria
            proposal.ciente = True  # Marca o campo ciente como True
            proposal.data_ciencia = datetime.now()
            proposal.save()

            # Pega a lista de políticas públicas selecionadas
            politicas = request.POST.getlist("politicas")

            # Registra plano de ação 
            new_plan(request, proposal.id, politicas)

            messages.success(request, "Ciência registrada com sucesso!")
        else:
            messages.error(request, "Todos os campos da conta bancária devem ser preenchidos.")

    return redirect("proposals:detail", id=proposal.id)


def remover_ciencia(request, id):
    proposal = get_object_or_404(Proposal, pk=id)
    print(request.POST.get("sei_remocao_ciente"))
    # Verifica se o método da requisição é POST

    if request.method == "POST":
        proposal.ciente = False  # Marca o campo ciente como False
        proposal.sei_remocao_ciente = request.POST.get("sei_remocao_ciente")
        proposal.data_remocao_ciente = datetime.now()
        proposal.save()
        messages.success(request, "Ciência removida com sucesso!")
    else:
        messages.error(request, "Erro ao remover a ciência.")

    return redirect("proposals:detail", id=proposal.id)

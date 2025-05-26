from datetime import datetime
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from proposals.models import Proposal
from commitments.models import Commitment
from settlement.models import Settlement
from payment.models import Payment
from accountability.models import Document, Accountability
from plans.models import Plan
from accountability.forms import DocumentForm, AccountabilityForm
from accountability.views import new
from utils.models import PoliticaPublica
from django.contrib import messages
from google_sheets_utils import load_data_from_sheets
from accountability.views import new as new_accountability



def lists(request):
    plan = Plan.objects.filter(removido_em=None)
    obj = request.GET.get("obj")  # Implementa o mecanismo de busca

    if obj:
        plan = plan.filter(codigo__icontains=obj) | plan.filter(proposal__municipio__nome__icontains=obj) | plan.filter(
            proposal__codigo__icontains=obj) | plan.filter(
            proposal__parlamentar__nome__icontains=obj)
    else:
        plan = plan.order_by("codigo")

    paginator = Paginator(plan, 10)  # Define 10 itens fixos por página
    page_number = request.GET.get("page")

    try:
        page_obj = paginator.get_page(page_number)
    except (PageNotAnInteger, EmptyPage):
        page_obj = paginator.get_page(1)

    return render(
        request,
        "plans/list.html",
        {
            "plans": page_obj,
            "page_obj": page_obj,
        }
    )


def detail(request, id):
    plan = get_object_or_404(Plan, pk=id)

    # Obter os commitments, liquidações e payments relacionados ao plano
    commitments = Commitment.objects.filter(plan=plan, removido_em=None)
    settlements = Settlement.objects.filter(commitment__plan=plan, removido_em=None)
    payments = Payment.objects.filter(settlement__commitment__plan=plan, removido_em=None)
    accountabilities = Accountability.objects.filter(plan=plan, removido_em=None)

    politicas_publicas = plan.politicas_publicas.all()
    accountability_form = AccountabilityForm()
    documento_form = DocumentForm()

    # Calcular valores executados
    investimento_executado = 0
    custeio_executado = 0
    for accountability in accountabilities:
        accountability.documentos = Document.objects.filter(removido_em=None, accountability=accountability)
        investimento_executado = investimento_executado + accountability.get_valor_executado_investimento()
        custeio_executado = custeio_executado + accountability.get_valor_executado_custeio()

    valor_total = plan.proposal.get_valor_total()
    total_valor_executado = investimento_executado + custeio_executado
    executado_percentual = (total_valor_executado / valor_total) * 100 if valor_total > 0 else 0

    return render(
        request,
        "plans/detail.html",
        {
            "plan": plan,
            "politicas_publicas": politicas_publicas,
            "accountability_form": accountability_form,
            "documento": documento_form,
            "commitments": commitments,
            "settlements": settlements,
            "payments": payments,
            "accountabilities": accountabilities,
            "valor_total": valor_total,
            "total_valor_executado": total_valor_executado,
            "investimento_executado": investimento_executado,
            "custeio_executado": custeio_executado,
            "executado_percentual": executado_percentual,
        },
    )


@login_required
def new(request, proposal_id, politicas):
    try:
        proposal = get_object_or_404(Proposal, pk=proposal_id)

        # cria um novo Plano associado a uma proposal 
        plan = Plan.objects.create(
            codigo=f"{proposal.ano}{proposal.id}-{proposal.project.id}-{proposal.parlamentar.id}",  # TODO: ALTERAR A LÓGICA
            descricao_politicas_publicas="verificar",
            proposal=proposal
        )

        # Salva as políticas públicas associadas ao Plano
        for politica_id in politicas:
            try:
                politica = PoliticaPublica.objects.get(pk=politica_id)
                plan.politicas_publicas.add(politica)
            except PoliticaPublica.DoesNotExist:
                print(f"Política pública com ID {politica_id} não encontrada.")

        plan.save()
        return plan

    except Exception as e:
        print(f"Erro ao criar Plano: {e}")
        return None


@login_required
def remove(request, id):
    plan = get_object_or_404(Plan, pk=id)
    plan.removido_em = datetime.now()
    plan.save()
    messages.success(request, "Plano removido com sucesso!")
    return redirect("plans:lists")


@login_required
def registrar_accountability(request, id):
    plano_acao = get_object_or_404(Plan, pk=id)

    if request.method == "POST":
        new_accountability(request, id)
    else:  # TODO: verificar abaixo
        messages.error(request, "Erro ao criar relatório de gestão. Verifique os campos.")

    return redirect("plans:detail", id=plano_acao.id)


def load_datas(request):
    print("Carregando dados...")
    if request.method == 'POST':
        data = load_data_from_sheets()
        if data:
            try:
                # Limpar dados existentes (opcional, dependendo da sua necessidade)
                Commitment.objects.all().delete()
                Settlement.objects.all().delete()
                Payment.objects.all().delete()

                # Carregar os dados na base de dados
                for commitment_data in data.get('EMPENHOS', []):
                    # Busca a instância de Plan pelo ID
                    plano_id = commitment_data.get('plan')
                    if plano_id:
                        try:
                            plano = get_object_or_404(Plan, pk=plano_id)
                            commitment_data['plan'] = plano
                        except Plan.DoesNotExist:
                            messages.error(request, f'plan com ID {plano_id} não encontrada.')
                            # Aqui você pode escolher como lidar com o erro:
                            # 1. Pular este Plano:
                            continue
                            # 2. Atribuir None e permitir que o banco de dados trate (se o campo for nulo):
                            # commitment_data['plan'] = None
                    else:
                        commitment_data['plan'] = None  # atribui none se o valor não existir na planilha

                    Commitment.objects.create(**commitment_data)
                    print(f"Commitment criado: {commitment_data}")

                for settlement_data in data.get('LIQUIDACOES', []):
                    # Certifique-se de que 'EMPENHO' seja um objeto EMPENHOS
                    commitment_id = settlement_data.get('commitment')
                    if commitment_id:
                        try:
                            commitment = get_object_or_404(Commitment, pk=commitment_id)
                            settlement_data['commitment'] = commitment
                        except Commitment.DoesNotExist:
                            messages.error(request, f'Commitment com ID {commitment_id} não encontrado.')
                            # Aqui você pode escolher como lidar com o erro:
                            # 1. Pular este Commitment:
                            continue
                            # 2. Atribuir None e permitir que o banco de dados trate (se o campo for nulo):
                            # settlement_data['commitment'] = None
                    else:
                        settlement_data['commitment'] = None

                    Settlement.objects.create(**settlement_data)
                    print(f"Liquidação criada: {settlement_data}")

                for payment_data in data.get('PAGAMENTOS', []):
                    # Certifique-se de que 'LIQUIDACAO' seja um objeto LIQUIDACOES
                    settlement_id = payment_data.get('settlement')
                    if settlement_id:
                        try:
                            settlement = get_object_or_404(Settlement, pk=settlement_id)
                            payment_data['settlement'] = settlement
                        except Settlement.DoesNotExist:
                            messages.error(request, f'Liquidação com ID {settlement_id} não encontrada.')
                            # Aqui você pode escolher como lidar com o erro:
                            # 1. Pular este Commitment:
                            continue
                            # 2. Atribuir None e permitir que o banco de dados trate (se o campo for nulo):
                            # payment_data['settlement'] = None
                    else:
                        payment_data['settlement'] = None

                    Payment.objects.create(**payment_data)
                    print(f"Payment criado: {payment_data}")

                messages.success(request, 'Dados do carregados com sucesso!')
            except Exception as e:
                messages.error(request, f'Erro ao carregar os dados: {e}')
        else:
            messages.error(request, 'Falha ao ler os dados da planilha.')
    return redirect("plans:lists")

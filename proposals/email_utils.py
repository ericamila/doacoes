from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from users.models import Usuario
import logging

logger = logging.getLogger(__name__)

def find_representative_for_municipio(municipio):
    """Encontra o usuário representante ativo para um determinado município."""
    try:
        # Assumindo que o campo em Usuario que liga ao município se chama 'municipios'
        # e que o tipo de usuário Representante é 1 e Ativo é 0
        representative = Usuario.objects.filter(
            municipios=municipio,
            tipo_usuario=1, 
            situacao=0
        ).first()
        return representative
    except Exception as e:
        logger.error(f"Erro ao buscar representante para o município {municipio.id}: {e}")
        return None

def send_proposal_notification(proposal, notification_type):
    """Envia notificação por email sobre uma proposta para o representante do município."""
    municipio = proposal.municipio
    representative = find_representative_for_municipio(municipio)

    if not representative:
        logger.warning(f"Nenhum representante ativo encontrado para o município {municipio.nome} (ID: {municipio.id}) para a proposta {proposal.id}")
        return

    if not representative.email:
        logger.warning(f"Representante {representative.get_full_name()} (ID: {representative.id}) não possui email cadastrado.")
        return

    subject = ""
    html_template = ""
    context = {
        'representative_name': representative.first_name or representative.username,
        'proposal_code': proposal.codigo,
        'project_name': proposal.project.nome,
        'municipio_name': municipio.nome,
        'proposal_id': proposal.id,
        'project_deadline': proposal.project.data_final_ciencia,
        'site_url': settings.SITE_URL # Adicione SITE_URL nas suas settings
    }

    if notification_type == 'new_pending':
        subject = f"Nova Proposta Pendente de Aceite: {proposal.codigo}"
        html_template = 'emails/new_proposal_pending.html'
        logger.info(f"Preparando notificação 'new_pending' para {representative.email}")
    elif notification_type == 'deadline_approaching':
        subject = f"Prazo para Aceite da Proposta {proposal.codigo} se Aproximando"
        html_template = 'emails/deadline_approaching.html'
        logger.info(f"Preparando notificação 'deadline_approaching' para {representative.email}")
    elif notification_type == 'acceptance_removed':
        subject = f"Aceite Removido da Proposta: {proposal.codigo}"
        html_template = 'emails/acceptance_removed.html'
        logger.info(f"Preparando notificação 'acceptance_removed' para {representative.email}")
    else:
        logger.error(f"Tipo de notificação desconhecido: {notification_type}")
        return

    try:
        html_message = render_to_string(html_template, context)
        send_mail(
            subject,
            '', # Plain text message (optional, can be generated from html)
            settings.DEFAULT_FROM_EMAIL, # Email remetente configurado nas settings
            [representative.email],
            html_message=html_message,
            fail_silently=False,
        )
        logger.info(f"Email de notificação '{notification_type}' enviado com sucesso para {representative.email} sobre a proposta {proposal.id}")
    except Exception as e:
        logger.error(f"Falha ao enviar email de notificação '{notification_type}' para {representative.email} sobre a proposta {proposal.id}: {e}")


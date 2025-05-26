from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from proposals.models import Proposal
from proposals.email_utils import send_proposal_notification
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Verifica propostas com prazo de aceite próximo e envia notificações por email."

    def add_arguments(self, parser):
        parser.add_argument(
            '--days', 
            type=int, 
            default=7, 
            help='Número de dias de antecedência para notificar sobre o prazo.'
        )

    def handle(self, *args, **options):
        days_threshold = options["days"]
        today = timezone.now().date()
        deadline_threshold_date = today + timedelta(days=days_threshold)

        self.stdout.write(f"Verificando propostas com prazo de aceite até {deadline_threshold_date.strftime('%d/%m/%Y')}...")

        # Filtrar propostas que:
        # 1. Não foram removidas
        # 2. Ainda não têm ciência registrada (ciente=False)
        # 3. Têm data final de ciência definida no projeto
        # 4. A data final de ciência está dentro do limite de dias especificado
        proposals_to_notify = Proposal.objects.filter(
            removido_em__isnull=True,
            ciente=False,
            project__data_final_ciencia__isnull=False,
            project__data_final_ciencia__date__lte=deadline_threshold_date,
            project__data_final_ciencia__date__gte=today # Evita notificar sobre prazos já passados
        )

        count = 0
        for proposal in proposals_to_notify:
            try:
                self.stdout.write(f"Enviando notificação para proposta {proposal.codigo} (Prazo: {proposal.project.data_final_ciencia.strftime('%d/%m/%Y')})...")
                send_proposal_notification(proposal, notification_type="deadline_approaching")
                count += 1
            except Exception as e:
                logger.error(f"Erro ao enviar notificação de prazo para proposta {proposal.id}: {e}")
                self.stderr.write(self.style.ERROR(f"Erro ao notificar proposta {proposal.id}: {e}"))

        self.stdout.write(self.style.SUCCESS(f"Verificação concluída. {count} notificações de prazo enviadas."))


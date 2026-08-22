from django.db import transaction

from .models import Ticket, TicketActivity, TicketSequence


class TicketService:

    @staticmethod
    @transaction.atomic
    def create_ticket(*,customer,category,subject,description,priority=Ticket.Priority.MEDIUM):
        sequence = (TicketSequence.objects.select_for_update().get(pk=1))
        sequence.last_number+=1
        sequence.save(update_fields=["last_number"])

        ticket_number = f"SUP-{sequence.last_number}"

        ticket = Ticket.objects.create(
            ticket_number=ticket_number,
            customer=customer,
            category=category,
            subject=subject,
            description=description,
            priority=priority,
            status=Ticket.Status.OPEN,
        )

        TicketActivity.objects.create(
            ticket=ticket,
            actor= customer,
            action="TICKET_CREATED",
            new_value={
                "status": Ticket.Status.OPEN,
            },
        )

        return ticket

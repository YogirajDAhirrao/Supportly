from django.db import transaction

from .models import Ticket, TicketActivity, TicketSequence
from apps.users.models import User


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

    @staticmethod
    @transaction.atomic
    def assign_ticket(*, ticket, agent, actor):
        if agent.role != User.Role.SUPPORT_AGENT:
            raise ValueError("User is not a support agent.")

        old_agent = ticket.assigned_agent

        ticket.assigned_agent = agent
        ticket.status = Ticket.Status.ASSIGNED

        ticket.save(
            update_fields=[
                "assigned_agent",
                "status",
                "updated_at",
            ]
        )

        TicketActivity.objects.create(
            ticket=ticket,
            actor=actor,
            action="TICKET_ASSIGNED",
            old_value={
                "assigned_agent": (
                    str(old_agent.id)
                    if old_agent
                    else None
                )
            },
            new_value={
                "assigned_agent": str(agent.id),
            },
        )

        return ticket

from django.db import transaction

from django.utils import timezone
from .models import Ticket, TicketActivity, TicketSequence
from apps.users.models import User
from .models import Ticket, TicketActivity


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

    @staticmethod
    @transaction.atomic
    def update_status(*,ticket,new_status,actor):
        old_status = ticket.status
        if old_status == new_status:
            raise ValueError("Ticket is alredy in this status")

        allowed_transaction = {
            Ticket.Status.OPEN:{
                Ticket.Status.ASSIGNED,
            },
            Ticket.Status.ASSIGNED:{
                Ticket.Status.IN_PROGRESS
            },
            Ticket.Status.IN_PROGRESS: {
            Ticket.Status.RESOLVED,
            },
            Ticket.Status.RESOLVED: {
            Ticket.Status.CLOSED,
            },
            Ticket.Status.CLOSED: set(),
        }

        if new_status not in allowed_transaction.get(old_status,set(),):
            raise ValueError( f"Cannot change ticket status " 
                            f"from {old_status} to {new_status}.")

        if actor.role == User.Role.SUPPORT_AGENT:
            if ticket.assigned_agent_id != actor.id:
                raise PermissionError("You are not assigned to this ticket")

        elif actor.role != User.Role.SUPPORT_ADMIN:
            raise PermissionError("You do not have permission to update this ticket")

        ticket.status = new_status

        if new_status == Ticket.Status.RESOLVED:
            ticket.resolved_at = timezone.now()

        if new_status == Ticket.Status.CLOSED:
            ticket.closed_at = timezone.now()

        ticket.save(
            update_fields = [
                "status",
                "resolved_at",
                "closed_at",
                "updated_at",
            ]
        ) 

        TicketActivity.objects.create(ticket=ticket,actor=actor,action = "STATUS CHANGED",old_value = {"status":old_status},new_value = {"status":new_status})   

        return ticket

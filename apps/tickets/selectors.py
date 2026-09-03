from django.db.models import QuerySet

from apps.users.models import User

from .models import Ticket, Message


def get_visible_tickets(user: User) -> QuerySet[Ticket]:
    queryset = (
        Ticket.objects
        .select_related(
            "customer",
            "assigned_agent",
            "category",
        )
        .order_by("-created_at")
    )

    if user.role == User.Role.SUPPORT_ADMIN:
        return queryset

    if user.role == User.Role.SUPPORT_AGENT:
        return queryset.filter(
            assigned_agent=user,
        )

    if user.role == User.Role.CUSTOMER:
        return queryset.filter(
            customer=user,
        )

    return queryset.none()


def get_ticket_for_user(
    user: User,
    ticket_id,
) -> Ticket | None:

    queryset = (
        Ticket.objects
        .select_related(
            "customer",
            "assigned_agent",
            "category",
        )
    )

    if user.role == User.Role.SUPPORT_ADMIN:
        return queryset.filter(
            id=ticket_id,
        ).first()

    if user.role == User.Role.SUPPORT_AGENT:
        return queryset.filter(
            id=ticket_id,
            assigned_agent=user,
        ).first()

    if user.role == User.Role.CUSTOMER:
        return queryset.filter(
            id=ticket_id,
            customer=user,
        ).first()

    return None

def get_ticket_messages(ticket):
    return Message.objects.filter(ticket=ticket).select_related("sender").order_by("created_at")
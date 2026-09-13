from .emails import send_ticket_assigned_email


class NotificationService:

    @staticmethod
    def ticket_assigned(ticket):
        send_ticket_assigned_email(ticket)
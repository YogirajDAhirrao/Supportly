from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_ticket_assigned_email(ticket):
    agent = ticket.assigned_agent
    customer = ticket.customer

    context = {
        "ticket_id": ticket.id,
        "ticket_subject": ticket.subject,
        "ticket_priority": ticket.priority,
        "customer_name": customer.get_full_name(),
        "agent_name": agent.get_full_name(),
    }

    # Email to agent
    agent_html = render_to_string(
        "emails/ticket_assigned_agent.html",
        {
            **context,
            "agent_name": agent.get_full_name(),
        },
    )

    agent_email = EmailMultiAlternatives(
        subject=f"Ticket #{ticket.id} assigned to you",
        body="A support ticket has been assigned to you.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[agent.email],
    )

    agent_email.attach_alternative(agent_html, "text/html")
    agent_email.send()

    # Email to customer
    customer_html = render_to_string(
        "emails/ticket_assigned_customer.html",
        {
            **context,
            "customer_name": customer.get_full_name(),
        },
    )

    customer_email = EmailMultiAlternatives(
        subject=f"Agent assigned to your ticket #{ticket.id}",
        body="An agent has been assigned to your support ticket.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[customer.email],
    )

    customer_email.attach_alternative(customer_html, "text/html")
    customer_email.send()

def send_ticket_status_changed_email(
    ticket,
    old_status,
    new_status,
):
    customer = ticket.customer

    context = {
        "ticket_id": ticket.ticket_number,
        "ticket_subject": ticket.subject,
        "customer_name": customer.get_full_name(),
        "old_status": old_status,
        "new_status": new_status,
    }

    customer_html = render_to_string(
        "emails/ticket_status_changed.html",
        context,
    )

    customer_email = EmailMultiAlternatives(
        subject=f"Ticket {ticket.ticket_number} status updated",
        body=(
            f"Your ticket {ticket.ticket_number} "
            f"status changed from {old_status} to {new_status}."
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[customer.email],
    )

    customer_email.attach_alternative(
        customer_html,
        "text/html",
    )

    customer_email.send()   

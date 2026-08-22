from django.contrib import admin

from .models import Category, Message, Ticket, TicketActivity


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        "ticket_number",
        "subject",
        "customer",
        "assigned_agent",
        "category",
        "priority",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "priority",
        "category",
    )

    search_fields = (
        "ticket_number",
        "subject",
        "description",
        "customer__email",
    )

    readonly_fields = (
        "ticket_number",
        "created_at",
        "updated_at",
        "resolved_at",
        "closed_at",
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "ticket",
        "sender",
        "created_at",
    )

    search_fields = (
        "ticket__ticket_number",
        "content",
        "sender__email",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )


@admin.register(TicketActivity)
class TicketActivityAdmin(admin.ModelAdmin):
    list_display = (
        "ticket",
        "actor",
        "action",
        "created_at",
    )

    list_filter = ("action",)

    search_fields = (
        "ticket__ticket_number",
        "actor__email",
        "action",
    )

    readonly_fields = ("created_at",)
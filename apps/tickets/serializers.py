from rest_framework import serializers

from .models import Category, Ticket
from .service import TicketService
from apps.users.models import User


class TicketCreateSerializer(serializers.Serializer):
    category_id = serializers.UUIDField()
    subject = serializers.CharField(max_length=255)
    description = serializers.CharField()
    priority = serializers.ChoiceField(
        choices=Ticket.Priority.choices,
        default=Ticket.Priority.MEDIUM,
    )

    def validate_category_id(self, value):
        if not Category.objects.filter(id=value).exists():
            raise serializers.ValidationError(
                "Category does not exist."
            )

        return value

    def create(self, validated_data):
        customer = self.context["request"].user

        category = Category.objects.get(
            id=validated_data["category_id"]
        )

        return TicketService.create_ticket(
            customer=customer,
            category=category,
            subject=validated_data["subject"],
            description=validated_data["description"],
            priority=validated_data["priority"],
        )


class TicketSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    customer = serializers.StringRelatedField()
    assigned_agent = serializers.StringRelatedField()

    class Meta:
        model = Ticket
        fields = [
            "id",
            "ticket_number",
            "customer",
            "assigned_agent",
            "category",
            "subject",
            "description",
            "priority",
            "status",
            "created_at",
            "updated_at",
            "resolved_at",
            "closed_at",
        ]
class AssignTicketSerializer(serializers.Serializer):
    agent_id = serializers.IntegerField()

    def validate_agent_id(self, value):
        try:
            agent = User.objects.get(
                id=value,
                role=User.Role.SUPPORT_AGENT,
                is_active=True,
            )
        except User.DoesNotExist:
            raise serializers.ValidationError(
                "Active support agent not found."
            )

        return value

    def save(self, **kwargs):
        ticket = self.context["ticket"]
        actor = self.context["request"].user

        agent = User.objects.get(
            id=self.validated_data["agent_id"]
        )

        return TicketService.assign_ticket(
            ticket=ticket,
            agent=agent,
            actor=actor,
        )  

class TicketStatusSerilaizer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Ticket.Status.choices)          
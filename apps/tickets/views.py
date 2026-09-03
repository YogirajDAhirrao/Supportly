from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from apps.users.models import User
from .serializers import TicketCreateSerializer, TicketSerializer, AssignTicketSerializer, MessageSerializer, TicketStatusSerilaizer
from .models import Ticket
from .permissions import isSupportAdmin
from .serializers import *
from .selectors import get_visible_tickets,get_ticket_for_user, get_ticket_messages


class TicketListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tickets = get_visible_tickets(request.user)

        serializer = TicketSerializer(
            tickets,
            many=True,
        )

        return Response(serializer.data)

    def post(self, request):
        serializer = TicketCreateSerializer(
            data=request.data,
            context={"request": request},
        )

        serializer.is_valid(raise_exception=True)

        ticket = serializer.save()

        return Response(
            TicketSerializer(ticket).data,
            status=status.HTTP_201_CREATED,
        )

class TicketAssignView(APIView):
    permission_classes = [
        IsAuthenticated,
        isSupportAdmin,
    ]

    def post(self, request, ticket_id):
        ticket = get_object_or_404(
            Ticket,
            id=ticket_id,
        )

        serializer = AssignTicketSerializer(
            data=request.data,
            context={
                "request": request,
                "ticket": ticket,
            },
        )

        serializer.is_valid(raise_exception=True)

        ticket = serializer.save()

        return Response(
            TicketSerializer(ticket).data,
            status=status.HTTP_200_OK,
        )    

class TicketDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,ticket_id):
        ticket = get_ticket_for_user(request.user,ticket_id)

        if ticket is None:
            return Response({
                "detail":"Ticket not found."
            },
            status=status.HTTP_404_NOT_FOUND,)    

        serializer = TicketSerializer(ticket)

        return Response(serializer.data)

class TicketStatusView(APIView):
    permission_classes = [IsAuthenticated]
    def patch(self,request,ticket_id):
        ticket = get_object_or_404(Ticket,id=ticket_id)

        serializers = TicketStatusSerilaizer(data = request.data)

        serializers.is_valid(raise_exception=True)

        try:
            ticket = TicketService.update_status(
                ticket=ticket,
                new_status=serializers.validated_data['status'],
                actor=request.user,
            )    
        except ValueError as exc:
            return Response({
                "detail": str(exc)
            },
            status=status.HTTP_400_BAD_REQUEST,)  

        return Response(TicketSerializer(ticket).data)

class TicketMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, ticket_id):
        ticket = get_ticket_for_user(
            request.user,
            ticket_id,
        )

        if ticket is None:
            return Response(
                {"detail": "Ticket not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        messages = get_ticket_messages(ticket)

        serializer = MessageSerializer(
            messages,
            many=True,
        )

        return Response(serializer.data)

    def post(self, request, ticket_id):
        ticket = get_ticket_for_user(
            request.user,
            ticket_id,
        )

        if ticket is None:
            return Response(
                {"detail": "Ticket not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = MessageSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True
        )

        try:
            message = TicketService.create_message(
                ticket=ticket,
                sender=request.user,
                content=serializer.validated_data["content"],
            )

        except ValueError as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            MessageSerializer(message).data,
            status=status.HTTP_201_CREATED,
        )
    

      
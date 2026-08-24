from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from apps.users.models import User
from .serializers import TicketCreateSerializer, TicketSerializer
from .models import Ticket
from .permissions import isSupportAdmin
from .serializers import *


class TicketListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tickets = request.user.created_tickets.all()

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
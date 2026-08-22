from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import TicketCreateSerializer, TicketSerializer


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
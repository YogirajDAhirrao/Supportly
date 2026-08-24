from django.urls import path

from .views import TicketListCreateView, TicketAssignView


urlpatterns = [
    path(
        "",
        TicketListCreateView.as_view(),
        name="ticket-list-create",
    ),
    path("<uuid:ticket_id>/assign/",TicketAssignView.as_view(),name="ticket-assign")
]
from django.urls import path

from .views import TicketListCreateView, TicketAssignView, TicketDetailView


urlpatterns = [
    path(
        "",
        TicketListCreateView.as_view(),
        name="ticket-list-create",
    ),
      path(
        "<uuid:ticket_id>/",
        TicketDetailView.as_view(),
        name="ticket-detail",
    ),
    path("<uuid:ticket_id>/assign/",TicketAssignView.as_view(),name="ticket-assign")
]
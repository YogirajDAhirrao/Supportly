from django.urls import path

from .views import TicketListCreateView, TicketAssignView, TicketDetailView, TicketStatusView


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
    path("<uuid:ticket_id>/assign/",TicketAssignView.as_view(),name="ticket-assign"),
    path(
    "<uuid:ticket_id>/status/",
    TicketStatusView.as_view(),
    name="ticket-status",
),

]
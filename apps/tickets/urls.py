from django.urls import path

from .views import TicketListCreateView


urlpatterns = [
    path(
        "",
        TicketListCreateView.as_view(),
        name="ticket-list-create",
    ),
]
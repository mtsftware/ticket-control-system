from django.urls import path
from . import views
urlpatterns = [
    path('create-ticket/', views.create_ticket_view, name='create_ticket'),
    path('ticket-list/', views.ticket_list_view, name='ticket_list'),
    path('check-ticket/', views.check_ticket_view, name='check_ticket'),
]
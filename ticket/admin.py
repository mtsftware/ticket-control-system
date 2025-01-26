from django.contrib import admin
from .models import Ticket

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'created_at', 'qr_code')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'qr_code')
    readonly_fields = ('id', 'created_at', 'qr_code')

# Register your models here.

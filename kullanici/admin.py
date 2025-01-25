from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Kullanici)
class KullaniciAdmin(admin.ModelAdmin):
    list_display = ('identity_no', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('identity_no', 'email', 'first_name', 'last_name')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    ordering = ('identity_no',)
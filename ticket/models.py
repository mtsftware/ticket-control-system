from django.db import models
from django.db import models
from kullanici.models import Kullanici
import uuid
class Ticket(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(Kullanici, on_delete=models.CASCADE, related_name="tickets")
    created_at = models.DateTimeField(auto_now_add=True)
    qr_code = models.CharField(max_length=255, unique=True, blank=True)
    STATUS_CHOICES = [
        ("active", "Active"),
        ("used", "Used"),
        ("expired", "Expired"),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="active")
    def __str__(self):
        return f"Bilet - {self.created_at} ({self.user.username})"

# Create your models here.

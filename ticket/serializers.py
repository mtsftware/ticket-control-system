from rest_framework import serializers
from .models import Ticket
import uuid

class TicketSerializer(serializers.ModelSerializer):
    qr_code = serializers.CharField(read_only=True)
    class Meta:
        model = Ticket
        fields = ['id', 'user', 'created_at', 'qr_code', 'status']
        read_only_fields = ['id', 'created_at', 'qr_code']
    def create(self, validated_data):
        validated_data['qr_code'] = str(uuid.uuid4())
        return super().create(validated_data)
    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance
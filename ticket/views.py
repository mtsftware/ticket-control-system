from rest_framework.response import Response
from ticket.models import Ticket
from ticket.serializers import TicketSerializer
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view
from rest_framework import status
from django.shortcuts import get_object_or_404

@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes([IsAuthenticated])
def create_ticket_view(request):
    try:
        user = request.user
    except Exception as e:
        return Response({"error": str(e)},status=status.HTTP_401_UNAUTHORIZED)
    data = {
        "status": 'active',
        "user": user.id,
    }
    serializer = TicketSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes([IsAuthenticated])
def ticket_list_view(request):
    try:
        user = request.user
    except Exception as e:
        return Response({"error": str(e)},status=status.HTTP_401_UNAUTHORIZED)
    tickets = Ticket.objects.filter(user=user.id)
    if tickets.exists():
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes([IsAuthenticated])
def check_ticket_view(request):
    try:
        user = request.user
        if not user.is_staff and not user.is_superuser:
            return Response({"error": "Bu işlem için yetkiniz yok"}, status=status.HTTP_403_FORBIDDEN)
        qr_code = request.data.get('qr_code')
        if not qr_code:
            return Response({"error": "QR kod gerekli"}, status=status.HTTP_400_BAD_REQUEST)
        ticket = get_object_or_404(Ticket, qr_code=qr_code)
        if ticket.status in ['used', 'expired']:
            return Response({'error': 'Bu bilet daha önce kullanılmış veya süresi dolmuş'},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = TicketSerializer(ticket)
        serializer.update(ticket, request.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Create your views here.

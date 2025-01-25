from django.db.migrations import serializer
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .serializers import KullaniciSerializer, KullaniciLoginSerializer
from django.contrib.auth import authenticate

# Create your views here.
@api_view(['POST'])
def register_view(request):
    if request.method == 'POST':
        serializer = KullaniciSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['POST'])
def login_view(request):
    user = authenticate(request, identity_no=request.data['identity_no'], password=request.data['password'])
    if user is None:
        return Response({"error": 'Invalid Credentials'},status=status.HTTP_401_UNAUTHORIZED)
    token, create = Token.objects.get_or_create(user=user)
    serializer = KullaniciLoginSerializer(instance=user)
    data = serializer.data
    data['token'] = str(token.key)
    return Response(data, status=status.HTTP_200_OK)
@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes([IsAuthenticated])
def user_detail_view(request):
    try:
        user = request.user
    except Exception as e:
        return Response({"error": str(e)},status=status.HTTP_401_UNAUTHORIZED)
    serializer = KullaniciSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)
@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes([IsAuthenticated])
def logout_view(request):
    try:
        request.user.auth_token.delete()
        return Response("Logged out successfully", status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

from rest_framework import viewsets, permissions
from .models import ProfileData
from django.contrib.auth import get_user_model
from .permissions import IsUserOrReadOnly
from .serializers import UserSerializer, ProfileDataSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsUserOrReadOnly, permissions.IsAuthenticated,)
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class ProfileDataViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = ProfileData.objects.all()
    serializer_class = ProfileDataSerializer
    lookup_field = 'username'


class UserAvatarAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated, IsUserOrReadOnly)
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = ProfileDataSerializer

    @staticmethod  # Проверить работает ли со статик методом
    def post(request):
        serializer = ProfileDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod  # Проверить работает ли со статик методом
    def delete(request):
        obj = ProfileData.objects.filter(username=request.user)
        obj.avatar.delete()

    def perform_create(self, serializer):
        serializer.save(username=self.request.user)

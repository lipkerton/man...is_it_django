from djoser.views import UserViewSet
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    CustomUserSerializer,
    CustomUserCreateSerializer,
    AuthTokenSerializer,
    AvatarSerializer
)
from .models import User


class CreateToken(APIView):

    def post(self, request, *args, **kwargs):
        serializer = AuthTokenSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'auth_token': token.key,
        })


class DeleteToken(APIView):

    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomUserViewSet(UserViewSet):

    queryset = User.objects.all()
    serializer_class = CustomUserSerializer

    def create(self, request):

        serializer = CustomUserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AvatarViewSet(viewsets.ViewSet):

    permission_classes = (IsAuthenticated,)

    def get_user(self, id):

        try:
            user = User.objects.get(pk=id)
            return user
        except User.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def update(self, request):

        user = self.get_user(request.user.id)
        serializer = AvatarSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(user, serializer.validated_data)
        return Response({"avatar": user.avatar.url}, status=status.HTTP_200_OK)

    def destroy(self, request):

        user = self.get_user(request.user.id)
        user.avatar.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

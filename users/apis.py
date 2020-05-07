from django.contrib.auth import login, logout
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated, NotFound
from rest_framework.generics import GenericAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from nabard.permissions import IsOwnerOrReadOnly
from nabard.exceptions import BadRequest

from .models import User
from .serializers import UserSerializer


class UserAPIView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        login(self.request, user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise NotAuthenticated()
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class UserRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    lookup_field = "username"

    permission_classes = (IsOwnerOrReadOnly,)


class AuthAPIView(GenericAPIView):
    serializer_class = UserSerializer

    def find_user(self):
        if self.request.data.get("username"):
            user = User.objects.filter(username=self.request.data["username"]).first()
        elif self.request.data.get("email"):
            user = User.objects.filter(email=self.request.data["email"]).first()
        else:
            raise BadRequest(detail=_('"username" or "email" is required'))
        if not user:
            raise NotFound(detail=_("user not found"))
        return user

    def authenticate(self, user):
        if not user.check_password(self.request.data.get("password", "")):
            raise AuthenticationFailed(detail=_("password does not match"))

    def post(self, request):
        user = self.find_user()
        self.authenticate(user)
        login(self.request, user)
        serializer = self.get_serializer(instance=user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)

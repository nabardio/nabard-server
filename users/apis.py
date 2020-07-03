from django.contrib.auth import login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated, NotFound, PermissionDenied
from rest_framework.generics import GenericAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from nabard.permissions import IsOwnerOrReadOnly
from nabard.exceptions import BadRequest, InvalidToken

from .models import User
from .serializers import UserSerializer
from .tokens import account_activation_token


class UserAPIView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.is_active = False
        user.save()
        self._send_email_verification(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise NotAuthenticated()
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    def _send_email_verification(self, user):
        current_site = get_current_site(self.request)
        mail_subject = "Active your account"
        message = render_to_string("active-account-email.html", {
            "user": user,
            "domain": current_site,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": account_activation_token.make_token(user),
        })
        email = EmailMessage(mail_subject, message, to=[user.email])
        email.send()


class ActivateUserAccount(GenericAPIView):
    def get(self, request, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(kwargs["uidb64"]))
            user = User.objects.get(pk=uid)
            account_activation_token.check_token_with_exception(user, kwargs["token"])
            user.is_active = True
            user.save()
            login(request, user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except (OverflowError, User.DoesNotExist, KeyError, InvalidToken, UnicodeDecodeError):
            raise BadRequest(detail=_("Invalid activation link"))


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
        if not user.is_active:
            raise PermissionDenied(detail=_("your account is not active"))

    def post(self, request):
        user = self.find_user()
        self.authenticate(user)
        login(self.request, user)
        serializer = self.get_serializer(instance=user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)

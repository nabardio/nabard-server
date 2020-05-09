from django.urls import path

from .apis import UserRetrieveUpdateDestroyAPIView, UserAPIView, AuthAPIView, \
    ActivateUserAccount

urlpatterns = [
    path("auth/", AuthAPIView.as_view(), name="auth"),
    path(
        "<str:username>/",
        UserRetrieveUpdateDestroyAPIView.as_view(),
        name="retrieve-update-destroy",
    ),
    path("", UserAPIView.as_view(), name="profile-register"),
    path(
        "auth/activate/<str:uidb64>/<str:token>/",
        ActivateUserAccount.as_view(),
        name="activate-account",
    ),
]

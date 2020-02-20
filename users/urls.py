from django.urls import path

from .apis import UserRetrieveUpdateDestroyAPIView, UserAPIView, AuthAPIView

urlpatterns = [
    path("auth/", AuthAPIView.as_view(), name="auth"),
    path(
        "<str:username>/",
        UserRetrieveUpdateDestroyAPIView.as_view(),
        name="retrieve-update-destroy",
    ),
    path("", UserAPIView.as_view(), name="register"),
]

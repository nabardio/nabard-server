from django.urls import path

from .apis import (
    RobotListCreateAPIView,
    RobotRetrieveUpdateDestroyAPIView,
    RobotCodeAPIView,
)

urlpatterns = [
    path(
        "<str:pk>/",
        RobotRetrieveUpdateDestroyAPIView.as_view(),
        name="retrieve-update-destroy",
    ),
    path("<str:pk>/code/", RobotCodeAPIView.as_view(), name="code"),
    path("", RobotListCreateAPIView.as_view(), name="list-create"),
]

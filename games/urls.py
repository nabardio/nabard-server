from django.urls import path

from .apis import GameListAPIView, GameRetrieveAPIView

urlpatterns = [
    path("<str:pk>/", GameRetrieveAPIView.as_view(), name="retrieve"),
    path("", GameListAPIView.as_view(), name="list"),
]

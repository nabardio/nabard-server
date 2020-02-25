from django.urls import path

from .apis import MatchListCreateAPIView, MatchRetrieveAPIView

urlpatterns = [
    path("<str:pk>/", MatchRetrieveAPIView.as_view(), name="retrieve"),
    path("", MatchListCreateAPIView.as_view(), name="list-create"),
]

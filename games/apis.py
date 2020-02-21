from rest_framework.generics import RetrieveAPIView, ListAPIView

from .serializers import GameSerializer
from .models import Game
from nabard.paginators import get_cursor_paginator


class GameListAPIView(ListAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    pagination_class = get_cursor_paginator()


class GameRetrieveAPIView(RetrieveAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

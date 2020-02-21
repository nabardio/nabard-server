from rest_framework.generics import ListAPIView, RetrieveAPIView

from nabard.paginators import get_cursor_paginator

from .models import Game
from .serializers import GameSerializer


class GameListAPIView(ListAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    pagination_class = get_cursor_paginator()


class GameRetrieveAPIView(RetrieveAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

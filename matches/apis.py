from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from nabard.paginators import get_cursor_paginator
from nabard.permissions import IsOwnerOrReadOnly

from .models import Match
from .serializers import MatchSerializer


class MatchListCreateAPIView(ListCreateAPIView):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    pagination_class = get_cursor_paginator()
    permission_class = (IsAuthenticatedOrReadOnly,)


class MatchRetrieveAPIView(RetrieveDestroyAPIView):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    permission_class = (IsOwnerOrReadOnly,)

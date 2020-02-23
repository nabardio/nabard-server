from rest_framework.generics import (
    GenericAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from nabard.filters import IsOwnerFilter
from nabard.paginators import get_cursor_paginator
from nabard.permissions import IsOwnerOrReadOnly

from .models import Robot
from .serializers import RobotSerializer


class RobotListCreateAPIView(ListCreateAPIView):
    queryset = Robot.objects.all()
    serializer_class = RobotSerializer
    pagination_class = get_cursor_paginator()
    filter_backends = [IsOwnerFilter]
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class RobotCodeAPIView(GenericAPIView):
    parser_classes = (MultiPartParser,)
    queryset = Robot.objects.all()
    serializer_class = RobotSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def put(self, request, *args, **kwargs):
        f = request.FILES["file"]
        robot = self.get_object()
        robot.code = f
        robot.save()
        return Response(status=HTTP_204_NO_CONTENT)


class RobotRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Robot.objects.all()
    serializer_class = RobotSerializer
    permission_class = (IsOwnerOrReadOnly,)

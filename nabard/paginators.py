from rest_framework.pagination import CursorPagination


def get_cursor_paginator(ordering="-created_at"):
    class CursorPaginator(CursorPagination):
        pass

    CursorPaginator.ordering = ordering
    return CursorPaginator

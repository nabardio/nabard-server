from rest_framework.filters import BaseFilterBackend


class IsOwnerFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        owner = request.query_params.get("owner", None)
        return queryset.filter(owner__pk=owner) if owner else queryset

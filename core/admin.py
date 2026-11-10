class ActiveObjectsAutocompleteMixin:
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        if request.path.endswith("/autocomplete/"):
            queryset = queryset.filter(deleted_at__isnull=True)
        return queryset, use_distinct

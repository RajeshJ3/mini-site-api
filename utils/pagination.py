from rest_framework.pagination import PageNumberPagination
import math


class BasicPagination(PageNumberPagination):
    page_size_query_param = 'limit'


class PaginationHandlerMixin(object):
    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        else:
            pass
        return self._paginator

    def paginate_queryset(self, queryset):

        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)

    def get_pagination_data(self, qs, limit_val, serializer_class):
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_paginated_response(
                serializer_class(page, many=True).data)
        else:
            serializer = serializer_class(qs, many=True)

        data = serializer.data

        if limit_val:
            end_page = math.ceil(len(qs)/int(limit_val))
            next_url = data["next"]
            previous_url = data["previous"]
            total_records = len(qs)
            output = data['results']
        else:
            end_page = None
            next_url = None
            previous_url = None
            total_records = len(qs)
            output = data

        return end_page, next_url, previous_url, total_records, output
